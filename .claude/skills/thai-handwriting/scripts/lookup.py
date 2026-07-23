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

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

THAI_RUN = re.compile(r"[ก-๛]+")
THAI_ONE = "[ก-๛]"


def repo_root(start: Path) -> Path:
    """Корень проекта — ближайший каталог вверх, где лежит progress.json или .git."""
    for d in [start, *start.parents]:
        if (d / "progress.json").exists() or (d / ".git").exists():
            return d
    return start


def load_lexicon(root: Path):
    """Возвращает (словарь из progress.json, частоты слов в материалах)."""
    known = {}
    progress = root / "progress.json"
    if progress.exists():
        try:
            items = json.loads(progress.read_text(encoding="utf-8")).get("items", {})
            for word, meta in items.items():
                known[word] = {
                    "translation": (meta or {}).get("translation", ""),
                    "translit": (meta or {}).get("translit", ""),
                    "topic": (meta or {}).get("topic", ""),
                }
        except (json.JSONDecodeError, OSError) as e:
            print(f"lookup: не читается progress.json ({e})", file=sys.stderr)

    freq = Counter()
    for md in root.rglob("*.md"):
        if ".git" in md.parts:
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        freq.update(THAI_RUN.findall(text))
    return known, freq


def build_regex(pattern: str) -> re.Pattern:
    out, i = [], 0
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


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pattern", help="шаблон слова (? * [..] или regex)")
    ap.add_argument("--sub", action="store_true", help="искать вхождение, а не слово целиком")
    ap.add_argument("--limit", type=int, default=20, help="сколько кандидатов показать")
    ap.add_argument("--root", default=None, help="корень проекта (по умолчанию — найти сам)")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else repo_root(Path.cwd())
    known, freq = load_lexicon(root)
    rx = build_regex(args.pattern)
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
        info = known.get(word, {})
        gloss = info.get("translation", "")
        translit = info.get("translit", "")
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
