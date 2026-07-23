#!/usr/bin/env python3
"""Второй OCR-движок: Typhoon OCR 1.5 (тайская vision-модель) через локальный Ollama.

Даёт независимое от Apple Vision чтение — «третье мнение» там, где Vision слаб на
рукописи. Офлайн: обращается к ollama на 127.0.0.1:11434, в сеть не ходит.

    python3 typhoon.py строка.png              # прочитать один файл
    python3 typhoon.py --dir /tmp/th           # все line-*.png из каталога thaiocr lines
    python3 typhoon.py --compare /tmp/th        # рядом: Vision (из lines.json) и Typhoon

HEIC конвертируется в PNG автоматически (через sips). Требует запущенного `ollama serve`
и модели `scb10x/typhoon-ocr1.5-3b` (ollama pull ...).
"""

import argparse
import base64
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

MODEL = "scb10x/typhoon-ocr1.5-3b"
HOST = "http://127.0.0.1:11434"
# Модель работает ТОЛЬКО с этим промптом (ограничение обучения), иначе выдаёт мусор.
PROMPT = ("Below is an image of a document page. Extract all text from the image "
          "exactly as written. Return only the raw text, preserving line breaks. "
          "Do not translate, summarize, or explain.")


def to_png(path: Path) -> Path:
    """HEIC/прочее → PNG во временный файл; PNG/JPEG отдаёт как есть."""
    if path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        return path
    out = Path(tempfile.gettempdir()) / (path.stem + "_typhoon.png")
    subprocess.run(["sips", "-s", "format", "png", str(path), "--out", str(out)],
                   check=True, capture_output=True)
    return out


def ocr(path: Path, timeout: int = 300) -> str:
    img = to_png(path)
    b64 = base64.b64encode(img.read_bytes()).decode()
    payload = json.dumps({
        "model": MODEL, "prompt": PROMPT, "images": [b64], "stream": False,
        "options": {"temperature": 0.1, "top_p": 0.6, "repeat_penalty": 1.1},
    }).encode()
    req = urllib.request.Request(f"{HOST}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()).get("response", "").strip()
    except urllib.error.URLError as e:
        sys.exit(f"typhoon: ollama недоступен на {HOST} — запусти `ollama serve` ({e})")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?", help="файл изображения")
    ap.add_argument("--dir", help="каталог с line-*.png")
    ap.add_argument("--compare", help="каталog thaiocr lines: показать Vision и Typhoon рядом")
    args = ap.parse_args()

    if args.compare:
        d = Path(args.compare)
        vision = {l["index"]: l.get("vision_text")
                  for l in json.loads((d / "lines.json").read_text())["lines"]}
        for f in sorted(d.glob("line-*.png")):
            idx = int(f.stem.split("-")[1])
            print(f"=== {f.name} ===")
            print(f"  vision : {vision.get(idx)}")
            print(f"  typhoon: {ocr(f)}")
        return

    if args.dir:
        for f in sorted(Path(args.dir).glob("line-*.png")):
            print(f"{f.name}: {ocr(f)}")
        return

    if not args.image:
        ap.error("нужен файл, --dir или --compare")
    print(ocr(Path(args.image)))


if __name__ == "__main__":
    main()
