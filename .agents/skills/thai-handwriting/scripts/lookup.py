#!/usr/bin/env python3
"""Подбор кандидатов по неуверенно прочитанному слову.

Ищет по словарю проекта: ключи progress.json + все тайские слова из учебных материалов
(*.md). Отвечает на вопрос «какие реальные слова совпадают с тем, что я разобрал».

Шаблон:
    ?        любая одна тайская буква/знак
    [กถ]     одна из перечисленных
    *        любое число букв
    остальное — как есть (поддерживается и обычный regex)

Примеры:
    python3 lookup.py "?ับ"              # вторая буква не разобрана
    python3 lookup.py "[กถ]ิน"           # выбор между ก и ถ
    python3 lookup.py --sub "ตื่น"       # где встречается кусок
    python3 lookup.py "ไป*" --limit 30

Только стандартная библиотека, офлайн.
"""

from __future__ import annotations  # аннотации ленивые: скрипт идёт на Python 3.8+

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, TypedDict, cast

THAI_RUN = re.compile(r"[ก-๛]+")
THAI_ONE = "[ก-๛]"


class Entry(TypedDict):
    """Что известно о слове из progress.json — ровно то, что печатает строка выдачи."""
    translation: str
    translit: str

# Каталоги внутри проекта, которые не являются учебными материалами: тайского в них
# нет, а прочитанными они попадают в частоты и портят ранжирование. Дерево при этом
# всё равно обходится целиком — `rglob` не умеет обрезать ветки, и экономится чтение
# файлов, а не обход.
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".cache"}


def nfc(word: str) -> str:
    """Каноническая форма слова — та же, что у ключей трекера (`tracker.nfc`)."""
    return unicodedata.normalize("NFC", word)


def repo_root(start: Path) -> Path:
    """Корень проекта — ближайший каталог вверх, где лежит progress.json или .git."""
    for d in [start, *start.parents]:
        if (d / "progress.json").exists() or (d / ".git").exists():
            return d
    return start


def load_lexicon(root: Path) -> tuple[dict[str, Entry], Counter[str]]:
    """Возвращает (словарь из progress.json, частоты слов в материалах)."""
    known: dict[str, Entry] = {}
    progress = root / "progress.json"
    if progress.exists():
        # UnicodeDecodeError — подкласс ValueError, а не OSError, поэтому перечислен
        # отдельно. Форма проверяется явно: `{"items": []}` разбирается как корректный
        # JSON и раньше падал AttributeError уже после except.
        try:
            parsed: Any = json.loads(progress.read_text(encoding="utf-8"))
            items_obj: Any = (cast("dict[str, Any]", parsed).get("items")
                              if isinstance(parsed, dict) else None)
            if not isinstance(items_obj, dict):
                raise ValueError("нет объекта «items»")
            for word, meta in cast("dict[str, Any]", items_obj).items():
                rec = cast("dict[str, Any]", meta if isinstance(meta, dict) else {})
                known[nfc(word)] = {
                    "translation": rec.get("translation", ""),
                    "translit": rec.get("translit", ""),
                }
        except (ValueError, OSError) as e:
            # Не падаем: словарь из progress.json — подспорье, а материалы (*.md)
            # читаются независимо и одни дают полезную выдачу.
            print(f"lookup: progress.json не прочитан ({e}) — ищу только по материалам",
                  file=sys.stderr)

    freq: Counter[str] = Counter()
    for md in root.rglob("*.md"):
        # Смотрим путь ОТНОСИТЕЛЬНО корня: `md.parts` содержит и каталоги выше проекта,
        # так что репозиторий, лежащий, например, внутри `~/.cache`, отбрасывал бы сам
        # себя целиком — и скрипт уверенно печатал бы «нет кандидатов».
        if SKIP_DIRS.intersection(md.relative_to(root).parts):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        # Ключи трекера нормализованы в NFC, слова из материалов — нет. Без этого
        # одно и то же слово показывалось двумя визуально неотличимыми кандидатами,
        # и только у одного был перевод.
        freq.update(nfc(w) for w in THAI_RUN.findall(text))
    return known, freq


def build_regex(pattern: str) -> re.Pattern[str]:
    out: list[str] = []
    i = 0
    while i < len(pattern):
        ch = pattern[i]
        if ch == "?":
            out.append(THAI_ONE)
        elif ch == "*":
            out.append(THAI_ONE + "*")
        elif ch == "[":
            j = pattern.find("]", i)
            if j == -1:
                out.append(re.escape(ch))
            else:
                out.append(pattern[i:j + 1])
                i = j
        else:
            out.append(ch)
        i += 1
    return re.compile("".join(out))


def main() -> None:
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pattern", help="шаблон слова (? * [..] или regex)")
    ap.add_argument("--sub", action="store_true", help="искать вхождение, а не слово целиком")
    ap.add_argument("--limit", type=int, default=20, help="сколько кандидатов показать")
    ap.add_argument("--root", default=None, help="корень проекта (по умолчанию — найти сам)")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else repo_root(Path.cwd())
    # Шаблон разбираем до чтения материалов: незачем обходить весь репозиторий,
    # чтобы упасть на первой же компиляции регулярки.
    try:
        # Шаблон приводим к той же форме, что и словарь: набранный с переставленными
        # знаками, он иначе не совпал бы ни с одним ключом.
        rx = build_regex(nfc(args.pattern))
    except re.error as e:
        # Совет — про конкретную поломку, а не про класс символов: regex поддерживается
        # намеренно, и `ก(ิ|ี)น` — рабочий шаблон. Раньше здесь предлагалось экранировать
        # скобки, что сломало бы такой шаблон вместо того, чтобы починить незакрытый.
        sys.exit(f"lookup: шаблон «{args.pattern}» не разобран как регулярное выражение: "
                 f"{e}.\nЧаще всего это незакрытая круглая скобка — квадратные "
                 f"скобки шаблона разбираются отдельно и до этой ошибки не доходят. "
                 f"Если скобка нужна буквально, экранируй именно её: \\(")
    known, freq = load_lexicon(root)
    match = rx.search if args.sub else rx.fullmatch

    candidates = {w for w in list(known) + list(freq) if match(w)}
    if not candidates:
        print(f"нет кандидатов под «{args.pattern}» в материалах {root}")
        print("это сигнал: чтение, скорее всего, неверное — либо слово ещё не проходили")
        return

    # сначала слова из активного словаря, потом по частоте в материалах
    ranked = sorted(candidates, key=lambda w: (w not in known, -freq.get(w, 0), w))
    print(f"кандидатов: {len(ranked)}   (корень: {root})\n")
    for word in ranked[:args.limit]:
        mark = "★" if word in known else " "
        info = known.get(word)
        gloss = info["translation"] if info else ""
        translit = info["translit"] if info else ""
        tail = f"  [{translit}]" if translit else ""
        count = freq.get(word, 0)
        seen = f"  ×{count}" if count else ""
        print(f"{mark} {word:<18}{gloss}{tail}{seen}")
    if len(ranked) > args.limit:
        print(f"\n… ещё {len(ranked) - args.limit}; ★ — есть в progress.json")
    else:
        print("\n★ — есть в progress.json (активный словарь)")


if __name__ == "__main__":
    main()
