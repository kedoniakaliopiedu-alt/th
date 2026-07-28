#!/usr/bin/env python3
"""Второй OCR-движок: Typhoon OCR 1.5 (тайская vision-модель) через локальный Ollama.

Даёт независимое от Apple Vision чтение — «третье мнение» там, где Vision слаб на
рукописи. Офлайн: обращается к ollama на 127.0.0.1:11434, в сеть не ходит.

    python3 typhoon.py строка.png              # прочитать один файл
    python3 typhoon.py --dir /tmp/th           # все line-*.png из каталога thaiocr lines
    python3 typhoon.py --compare /tmp/th        # рядом: Vision (из lines.json) и Typhoon

Режимы взаимоисключающие: указать одновременно файл и каталог — ошибка, а не молчаливый
выбор одного из них.

HEIC конвертируется в PNG автоматически (через sips). Требует запущенного `ollama serve`
и модели `scb10x/typhoon-ocr1.5-3b` (ollama pull ...).
"""

from __future__ import annotations  # аннотации ленивые: скрипт идёт на Python 3.8+

import argparse
import base64
import json
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "scb10x/typhoon-ocr1.5-3b"
HOST = "http://127.0.0.1:11434"
# Модель работает ТОЛЬКО с этим промптом (ограничение обучения), иначе выдаёт мусор.
PROMPT = ("Below is an image of a document page. Extract all text from the image "
          "exactly as written. Return only the raw text, preserving line breaks. "
          "Do not translate, summarize, or explain.")

# Форматы, которые движок читает сам; остальное (HEIC с телефона) конвертируем.
READY_SUFFIXES = {".png", ".jpg", ".jpeg"}


def to_png(path: Path) -> Path:
    """HEIC/прочее → PNG во временный файл; PNG/JPEG отдаёт как есть."""
    if path.suffix.lower() in READY_SUFFIXES:
        return path
    out = Path(tempfile.gettempdir()) / (path.stem + "_typhoon.png")
    subprocess.run(["sips", "-s", "format", "png", str(path), "--out", str(out)],
                   check=True, capture_output=True)
    return out


class OcrFailed(Exception):
    """Не прочиталась одна картинка. Пакетный прогон это переживает, см. main."""


def vision_lines(directory: Path) -> dict[int, str | None]:
    """Чтения Apple Vision из lines.json (каталог, собранный `thaiocr lines`)."""
    src = directory / "lines.json"
    if not src.is_file():
        sys.exit(f"typhoon: в {directory} нет lines.json — это каталог, который "
                 f"собирает `thaiocr lines`. Сначала нарежь страницу на строки, "
                 f"либо укажи каталог с готовой нарезкой.")
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
        return {ln["index"]: ln.get("vision_text") for ln in data["lines"]}
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        sys.exit(f"typhoon: {src} не разобран ({e}) — пересобери каталог "
                 f"`thaiocr lines`.")


def line_index(path: Path) -> int | None:
    """Номер строки из имени `line-<N>.png`; None, если имя не такое.

    В каталоге нарезки заводятся и посторонние файлы — ручной кроп, обрезка. Раньше
    любой такой файл ронял всё сравнение на `int()`.
    """
    parts = path.stem.split("-")
    if len(parts) < 2 or not parts[1].isdigit():
        return None
    return int(parts[1])


def ocr(path: Path, timeout: int = 300) -> str:
    img = to_png(path)
    b64 = base64.b64encode(img.read_bytes()).decode()
    payload = json.dumps({
        "model": MODEL, "prompt": PROMPT, "images": [b64], "stream": False,
        "options": {"temperature": 0.1, "top_p": 0.6, "repeat_penalty": 1.1},
    }).encode()
    req = urllib.request.Request(f"{HOST}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    # HTTPError — подкласс URLError, поэтому ловится первым: «ollama не запущен» и
    # «ollama ответил ошибкой» лечатся по-разному. Внутри HTTPError причину называет
    # только сам ollama (в теле ответа): 404 — нет модели, 400 — не разобрал картинку.
    # Гадать по коду нельзя, поэтому тело показываем, а совет даём лишь на 404.
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        # Ollama жив и ответил — значит виновата эта картинка или эта модель, а не
        # весь прогон: поднимаем ошибку, пакет её переживёт.
        detail = (e.read() or b"").decode("utf-8", "replace").strip()
        hint = f" Если модели нет: `ollama pull {MODEL}`" if e.code == 404 else ""
        raise OcrFailed(f"ollama ответил {e.code} {e.reason}"
                        f"{': ' + detail if detail else ''}{hint}") from e
    except urllib.error.URLError as e:
        # Соединения нет — следующая картинка тоже не прочитается, продолжать незачем.
        sys.exit(f"typhoon: ollama недоступен на {HOST} — запусти `ollama serve` ({e})")
    try:
        return json.loads(body).get("response", "").strip()
    except (ValueError, AttributeError) as e:
        raise OcrFailed(f"ollama вернул не JSON ({e})") from e


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?", help="файл изображения")
    ap.add_argument("--dir", help="каталог с line-*.png")
    ap.add_argument("--compare", help="каталог thaiocr lines: показать Vision и Typhoon рядом")
    args = ap.parse_args()

    # Режимы проверяем явно, а не по порядку: раньше `typhoon.py файл.jpg --dir …`
    # молча обрабатывал каталог и игнорировал файл.
    chosen = [name for name, value in (("файл", args.image), ("--dir", args.dir),
                                       ("--compare", args.compare)) if value]
    if not chosen:
        ap.error("нужен файл, --dir или --compare")
    if len(chosen) > 1:
        ap.error("нужен ровно один режим, а указаны: " + ", ".join(chosen))

    # Пакетные режимы не обрываются на одной плохой строке: иначе половина страницы
    # печаталась бы и выглядела как целая. Нечитаемые перечисляются в конце, и код
    # возврата отличает частичный прогон от полного.
    if args.compare or args.dir:
        directory = Path(args.compare or args.dir)
        if not directory.is_dir():
            sys.exit(f"typhoon: каталог {directory} не найден")
        vision = vision_lines(directory) if args.compare else {}
        files = sorted(directory.glob("line-*.png"))
        if not files:
            sys.exit(f"typhoon: в {directory} нет файлов line-*.png — "
                     f"похоже, нарезка ещё не собрана (`thaiocr lines`)")
        failed: list[str] = []
        for f in files:
            idx = line_index(f)
            try:
                text = ocr(f)
            except OcrFailed as e:
                failed.append(f"{f.name}: {e}")
                text = "— не прочитано, см. ниже"
            if not args.compare:
                print(f"{f.name}: {text}")
                continue
            print(f"=== {f.name} ===")
            if idx is None:
                # Посторонний файл в каталоге нарезки: читаем, но сопоставлять не с чем.
                print("  vision : — (имя не вида line-<число>.png, строка не сопоставлена)")
            else:
                print(f"  vision : {vision.get(idx)}")
            print(f"  typhoon: {text}")
        if failed:
            print(f"\nне прочитано {len(failed)} из {len(files)}:", file=sys.stderr)
            for line in failed:
                print(f"  {line}", file=sys.stderr)
            sys.exit(1)
        return

    try:
        print(ocr(Path(args.image)))
    except OcrFailed as e:
        sys.exit(f"typhoon: {e}")


if __name__ == "__main__":
    main()
