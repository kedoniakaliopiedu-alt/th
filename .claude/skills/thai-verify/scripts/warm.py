#!/usr/bin/env python3
"""Прогрев кэша словаря: заранее скачать страницы thai-language.com по всей лексике.

Кэш наполняется лениво — по одному слову за занятие, — и к моменту, когда сайт или DNS
отваливаются, в нём лежит лишь то, что случайно спрашивали. Тогда сверка невозможна, а по
правилу проекта тон без словаря не оценивается: занятие встаёт. Скрипт закрывает разрыв
заранее, скачивая ответы на слова из `progress.json` пачкой.

Протокол запроса — тот же, что в SKILL.md, раздел 1: POST с `emode=1&tmode=2`.
Ключ кэша — md5 слова в UTF-8, как у страниц, сложенных вручную раньше.

Страница «нет результатов» в кэш не идёт: иначе слово выглядело бы сверенным, не будучи им.
Такие слова печатаются отдельным списком — это кандидаты в `references/irregulars.md`.

Прогон идемпотентен: уже скачанное пропускается, прерванный прогон продолжается запуском
той же команды.

Команды:
    python3 warm.py status                 сколько лексики уже в кэше (офлайн)
    python3 warm.py warm                   скачать недостающее
    python3 warm.py warm --limit 50        первые 50 недостающих
    python3 warm.py warm ไก่ เจดีย์          только эти слова
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, List, Tuple, cast

SKILL = pathlib.Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[2]
PROGRESS = ROOT / "progress.json"
# Вне репозитория и вне папки сессии: сессия чистится, а полторы тысячи запросов
# к волонтёрскому сайту повторять нельзя (SKILL.md, раздел 1).
CACHE = pathlib.Path.home() / ".cache" / "thai-dict"
URL = "http://www.thai-language.com/dict"
PAUSE = 1.6
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
THAI_FIRST, THAI_LAST = "฀", "๿"
THAI_CLASS = f"[{THAI_FIRST}-{THAI_LAST}]"


def is_thai(word: str) -> bool:
    return any(THAI_FIRST <= ch <= THAI_LAST for ch in word)


def normalize(key: str) -> "str | None":
    """Ключ трекера → слово для запроса, или None, если это вообще не слово.

    В трекере рядом со словами лежат шаблоны гласных (`เ–ีย`), названия групп финалей
    и ключи с приклеенным глоссом (`จันทร์ (понедельник)`). Отправить такое в словарь —
    получить «нет результатов» и записать живое слово в несуществующие: страница пустая
    не потому, что слова нет, а потому, что спросили не слово.
    """
    s = re.sub(r"\s+—.*$", "", key)                     # хвост-пояснение после тире
    inner = re.findall(r"\(([^)]*)\)", s)
    s = re.sub(r"\([^)]*\)", " ", s).strip()           # скобки с глоссом или транскрипцией
    if not re.search(THAI_CLASS, s):                    # тайское спряталось в скобках
        s = next((g.strip() for g in inner if re.search(THAI_CLASS, g)), "")
    if any(ch in s for ch in "–-/·,"):                  # шаблон гласной, а не слово
        return None
    return s if re.fullmatch(f"{THAI_CLASS}+([ ]{THAI_CLASS}+)*", s) else None


def queryable(words: List[str]) -> "Tuple[List[str], List[str]]":
    """Разделить ключи на «можно спросить» (без повторов) и «не слово»."""
    good: List[str] = []
    skipped: List[str] = []
    for key in words:
        word = normalize(key)
        if word is None:
            skipped.append(key)
        elif word not in good:
            good.append(word)
    return good, skipped


def cache_path(word: str) -> pathlib.Path:
    return CACHE / (hashlib.md5(word.encode("utf-8")).hexdigest() + ".html")


def vocabulary(progress: pathlib.Path) -> List[str]:
    """Тайские ключи трекера — вся лексика, которую занятие может спросить."""
    data = cast("dict[str, Any]", json.loads(progress.read_text(encoding="utf-8")))
    items = cast("dict[str, Any]", data.get("items") or {})
    return [w for w in items if is_thai(w)]


def fetch(word: str) -> str:
    """Один запрос по протоколу SKILL.md. GET отдаёт «нет результатов», нужен POST."""
    body = urllib.parse.urlencode(
        {"search": word, "emode": "1", "tmode": "2"}, encoding="utf-8"
    ).encode("ascii")
    req = urllib.request.Request(URL, data=body, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = cast(bytes, resp.read())
    return raw.decode("utf-8", "replace")


def cmd_status(args: argparse.Namespace) -> int:
    keys = vocabulary(cast(pathlib.Path, args.progress))
    words, skipped = queryable(keys)
    have = [w for w in words if cache_path(w).exists()]
    total = len(words)
    share = (100 * len(have) // total) if total else 0
    print(f"Записей в трекере: {len(keys)}, из них слов: {total}")
    print(f"Есть в кэше:       {len(have)} ({share}%)")
    print(f"Не хватает:        {total - len(have)}")
    print(f"Не слова:          {len(skipped)} (шаблоны гласных, названия групп) — не спрашиваются")
    print(f"Кэш: {CACHE}")
    return 0


def cmd_warm(args: argparse.Namespace) -> int:
    given = cast("List[str]", args.words)
    words, _ = queryable(given or vocabulary(cast(pathlib.Path, args.progress)))
    todo = [w for w in words if not cache_path(w).exists()]
    limit = cast("int | None", args.limit)
    if limit is not None:
        todo = todo[:limit]
    CACHE.mkdir(parents=True, exist_ok=True)

    pause = cast(float, args.pause)
    print(f"к загрузке: {len(todo)} из {len(words)} (пауза {pause} с)", flush=True)
    saved = 0
    missing: List[str] = []
    failed: List[Tuple[str, str]] = []

    for i, word in enumerate(todo, 1):
        try:
            html = fetch(word)
        except (urllib.error.URLError, OSError) as exc:
            failed.append((word, f"{type(exc).__name__}: {exc}"))
            time.sleep(pause * 3)          # сеть шатается — отступить, а не долбить
            continue
        if "class=th" not in html:         # «нет результатов» кэшировать нельзя
            missing.append(word)
        else:
            cache_path(word).write_text(html, encoding="utf-8")
            saved += 1
        if i % 25 == 0:
            print(f"  [{i}/{len(todo)}] сохранено {saved}", flush=True)
        time.sleep(pause)

    print(f"\nсохранено: {saved} | нет в словаре: {len(missing)} | сетевых ошибок: {len(failed)}")
    if missing:
        print("Нет в словаре (кандидаты в references/irregulars.md):")
        print("  " + " ".join(missing))
    if failed:
        print("Не скачаны — повторить запуск позже:")
        for word, why in failed[:10]:
            print(f"  {word}: {why}")
    return 1 if failed else 0


def main(argv: "List[str] | None" = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--progress", type=pathlib.Path, default=PROGRESS, help="файл трекера (по умолчанию progress.json в корне)")
    sub = p.add_subparsers(dest="cmd", required=True)

    st = sub.add_parser("status", help="сколько лексики уже в кэше (офлайн)")
    st.set_defaults(func=cmd_status)

    wm = sub.add_parser("warm", help="скачать недостающие страницы")
    wm.add_argument("words", nargs="*", help="конкретные слова; без них — вся лексика трекера")
    wm.add_argument("--limit", type=int, default=None, help="взять не больше N недостающих")
    wm.add_argument("--pause", type=float, default=PAUSE, help="пауза между запросами, с (не меньше 1.5)")
    wm.set_defaults(func=cmd_warm)

    args = p.parse_args(argv)
    func: Any = args.func
    return cast(int, func(args))


if __name__ == "__main__":
    sys.exit(main())
