#!/usr/bin/env python3
"""Журнал сверки: какие файлы проверены по словарю и какие изменились после этого.

Состояние хранится в `journal.json` рядом со скиллом. Ключ строки — путь файла, признак изменения — хеш содержимого: правка любой
буквы разводит хеш, и строка сама помечается как требующая повторной сверки. Помнить
руками ничего не нужно.

Только стандартная библиотека, офлайн.

Команды:
    python3 journal.py status              показать состояние и пересчитать колонку «Статус»
    python3 journal.py status --stale      только те, что ждут проверки
    python3 journal.py mark ФАЙЛ…          отметить файлы как сверенные сейчас
    python3 journal.py init                завести журнал по всем файлам курса

Состояние — `journal.json` (машинный формат: доступ по пути, читается одним разбором).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys
from typing import Dict, List, Optional, Tuple

SKILL = pathlib.Path(__file__).resolve().parents[1]
JOURNAL = SKILL / "journal.json"
ROOT = SKILL.parents[2]
# Всё, где живёт транскрипция: материал курса, справочники и те скиллы,
# в примерах которых стоят тайские слова с кириллицей.
WATCHED = ("Thai A2", "Thai B1", "Helpers",
           ".codex/skills/thai-phonetics",
           ".codex/skills/thai-handwriting/references",
           ".codex/skills/thai-tasks/references",
           ".codex/skills/thai-mistakes",
           ".codex/skills/thai-learning",
           ".codex/skills/thai-display",
           ".codex/skills/thai-handwriting",
           ".codex/skills/thai-tasks",
           ".codex/skills/thai-verify")

THAI = re.compile(r"[฀-๿]+")
SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
TRANSCR_COL = re.compile(r"инициал|финал|чтение|транскрип|краткий|долгий|кирилл", re.I)
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|[^|]*\|\s*(\S+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$")

STATUS_OK = "проверен"
STATUS_NO = "не проверен"


class Entry:
    def __init__(self, path: str, digest: str, date: str, note: str) -> None:
        self.path = path
        self.digest = digest
        self.date = date
        self.note = note


def digest_of(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def transcription_rows(text: str) -> List[int]:
    """Номера строк-таблиц с транскрипционной колонкой.

    Разбор дублирует `phonetics.transcription_cells`, но без импорта: скрипт лежит
    в другом скилле, и тянуть его туда по sys.path — хрупче, чем повторить десять строк.
    """
    rows: List[int] = []
    header: Optional[List[str]] = None
    cols: List[int] = []
    for n, line in enumerate(text.split("\n"), 1):
        if line.startswith("#") or not line.lstrip().startswith("|"):
            header, cols = None, []
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if SEP.match(line):
            cols = [i for i, h in enumerate(header or []) if TRANSCR_COL.search(h)]
            header = None
            continue
        if not cols:
            header = cells
            continue
        rows.append(n)
    return rows


def rows_in(path: pathlib.Path) -> Tuple[int, int]:
    """Сколько в файле сверяемых строк: всего с тайским и однословных."""
    lines = path.read_text(encoding="utf-8").split("\n")
    total = single = 0
    for n in transcription_rows("\n".join(lines)):
        words = THAI.findall(lines[n - 1])
        if not words:
            continue
        total += 1
        if len(words) == 1:
            single += 1
    return total, single


def watched_files() -> List[pathlib.Path]:
    out: List[pathlib.Path] = []
    for folder in WATCHED:
        base = ROOT / folder
        if base.exists():
            out += sorted(base.rglob("*.md"))
    for extra in ("progress.json", "AGENTS.md", "AGENTS.md", "RESOURCES.md",
                  ".codex/skills/README.md"):
        path = ROOT / extra
        if path.exists():
            out.append(path)
    # папки в WATCHED перекрываются (thai-tasks и thai-tasks/references) — дедуп по пути
    seen: Dict[str, pathlib.Path] = {}
    for path in out:
        seen.setdefault(str(path.resolve()), path)
    return sorted(seen.values())


def load() -> Dict[str, Entry]:
    if not JOURNAL.exists():
        return {}
    raw = json.loads(JOURNAL.read_text(encoding="utf-8"))
    return {k: Entry(k, v["digest"], v["date"], v["note"])
            for k, v in raw.get("files", {}).items()}


def save(entries: Dict[str, Entry]) -> None:
    files: Dict[str, Dict[str, str]] = {}
    checked = 0
    for e in sorted(entries.values(), key=lambda x: x.path):
        full = ROOT / e.path
        ok = full.exists() and e.digest != "—" and e.digest == digest_of(full)
        checked += ok
        files[e.path] = {"status": STATUS_OK if ok else STATUS_NO,
                         "digest": e.digest, "date": e.date, "note": e.note}
    payload: Dict[str, object] = {
        "_": "Журнал сверки по словарю. Ведёт scripts/journal.py, руками не править. "
             "status пересчитывается при каждом запуске: digest — хеш содержимого на момент "
             "сверки, разошёлся — файл снова «не проверен».",
        "checked": checked,
        "total": len(files),
        "files": files,
    }
    JOURNAL.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def status_of(entry: Optional[Entry], path: pathlib.Path) -> str:
    if entry is None or entry.digest == "—":
        return STATUS_NO
    return STATUS_OK if entry.digest == digest_of(path) else STATUS_NO


def cmd_status(args: argparse.Namespace) -> int:
    entries = load()
    save(entries)                      # колонка «Статус» пересчитывается при каждом взгляде
    counts = {STATUS_OK: 0, STATUS_NO: 0}
    shown: List[str] = []
    for path in watched_files():
        rel = str(path.relative_to(ROOT))
        st = status_of(entries.get(rel), path)
        counts[st] += 1
        if args.stale and st == STATUS_OK:
            continue
        mark = {STATUS_OK: "✔", STATUS_NO: "·"}[st]
        shown.append(f"  {mark} {rel}")
    print(" · ".join(f"{k}: {v}" for k, v in counts.items()))
    if shown:
        print("\n".join(shown[:60]))
        if len(shown) > 60:
            print(f"  … ещё {len(shown) - 60}")
    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    entries = load()
    today = datetime.date.today().isoformat()
    for raw in args.files:
        path = pathlib.Path(raw)
        if not path.exists():
            print(f"нет файла: {raw}", file=sys.stderr)
            continue
        rel = str(path.resolve().relative_to(ROOT))
        if args.note:
            note = args.note
        else:
            total, single = rows_in(path)
            note = f"строк с тайским {total}, из них однословных {single}"
        entries[rel] = Entry(rel, digest_of(path), today, note)
        print(f"отмечен: {rel}")
    save(entries)
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    entries = load()
    for path in watched_files():
        rel = str(path.relative_to(ROOT))
        entries.setdefault(rel, Entry(rel, "—", "—", "не сверялся"))
    save(entries)
    print(f"в журнале файлов: {len(entries)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status", help="состояние журнала")
    s.add_argument("--stale", action="store_true", help="только ждущие проверки")
    s.set_defaults(func=cmd_status)
    m = sub.add_parser("mark", help="отметить файлы как сверенные")
    m.add_argument("files", nargs="+")
    m.add_argument("--note", default="", help="заметка вместо автоматической")
    m.set_defaults(func=cmd_mark)
    i = sub.add_parser("init", help="завести журнал по всем файлам")
    i.set_defaults(func=cmd_init)
    args = ap.parse_args()
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
