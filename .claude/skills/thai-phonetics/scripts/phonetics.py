#!/usr/bin/env python3
"""Справка и проверка по справочникам thai-phonetics.

Читает те же markdown-файлы, что и модель (`references/*.md`), — второго источника
данных в проекте нет. Только стандартная библиотека, офлайн.

Команды:
    python3 phonetics.py sign ร            знак: класс, чтение в инициали и финали
    python3 phonetics.py finals т          все знаки, дающие эту финаль
    python3 phonetics.py word ตลาด         слово в локальном словаре (data/dictionary.json)
    python3 phonetics.py check             проверить справочники на целостность
    python3 phonetics.py check --course    плюс проверить файлы курса на чужие знаки

`check` ловит то, что руками ловится плохо: знаки вне системы (макрон, å, ɣ, латиница)
в транскрипционных колонках, расхождение SKILL.md со справочником, пропавшие файлы.
Разделы «Требует сверки» и «Расхождения с источником» проверку не проходят намеренно —
они существуют ровно для того, чтобы держать спорное на виду.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import AbstractSet, Dict, List, Optional, Sequence, Tuple

SKILL = Path(__file__).resolve().parents[1]
REFS = SKILL / "references"
DATA = SKILL / "data"
ROOT = SKILL.parents[2]
COURSE = ("Thai A2", "Thai B1", "Helpers")

REQUIRED = ("alphabet.md", "consonants.md", "vowels.md", "clusters.md",
            "silent-letters.md", "irregulars.md")
REQUIRED_DATA = ("alphabet.json", "consonants.json", "vowels.json", "clusters.json",
                 "silent-letters.json")

THAI = re.compile(r"[฀-๿]")
SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
# колонки, которые содержат транскрипцию, а не перевод и не комментарий
TRANSCR_COL = re.compile(r"инициал|финал|чтение|транскрип|краткий|долгий|кирилл", re.I)
# разделы, где чужие знаки лежат намеренно
TOLERANT = re.compile(r"требует сверки|расхождени|оттенк|без данных|не решает", re.I)

IPA_CELL = re.compile(r"^[\[/].*[\]/]$")   # [k̚], /kʰ/ — чужая нотация, а не наша запись
TONE_MARKS = "̀́̂̌"          # ` ´ ˆ ˇ
VOWELS = set("аиыуэоӭӧȯo")   # латинская o — база знака ȯ
ALIEN = {"̄": "макрон", "å": "å", "ɣ": "ɣ"}


class Row:
    """Строка таблицы согласных."""

    def __init__(self, sign: str, cls: str, sub: Optional[str], initial: str,
                 final: str, example: str, also: Optional[List[str]] = None) -> None:
        self.sign = sign
        self.cls = cls
        self.sub = sub
        self.initial = initial
        self.final = final
        self.example = example
        self.also = also or []


def cells(line: str) -> Optional[List[str]]:
    body = line.strip()
    if not body.startswith("|"):
        return None
    body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def read(name: str) -> str:
    path = REFS / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def tables() -> Dict[str, Dict[str, Dict[str, str]]]:
    """Справочные таблицы из data/*.json. Markdown больше не разбирается.

    Файл на справочник: alphabet, consonants, vowels, clusters, silent-letters.
    Ключи внутри не пересекаются, поэтому склеиваются в один словарь.
    """
    out: Dict[str, Dict[str, Dict[str, str]]] = {}
    for path in sorted(DATA.glob("*.json")):
        if path.name == "dictionary.json":
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        for key, value in raw.items():
            if isinstance(value, dict) and key != "_":
                out[key] = value
    return out


def parse_consonants() -> List[Row]:
    out: List[Row] = []
    for sign, r in tables().get("consonants", {}).items():
        also = r.get("also_heard")
        out.append(Row(sign, str(r["class"]), r.get("subclass"), str(r["initial"]),
                       str(r["final"]), str(r["example"]),
                       also if isinstance(also, list) else None))
    return out


def cmd_sign(args: argparse.Namespace) -> int:
    wanted = args.sign.strip()
    for r in parse_consonants():
        if r.sign == wanted:
            fin = r.final if r.final != "—" else "в финали не встречается"
            label = f"{r.cls} класс" + (f", {r.sub}" if r.sub else "")
            print(f"{r.sign} · {label}")
            print(f"  инициаль: {r.initial}")
            print(f"  финаль:   {fin}")
            print(f"  пример:   {r.example}")
            if r.also:
                print(f"  слышится также как: {', '.join(r.also)}  — в запись не идёт")
            return 0
    print(f"{wanted}: в справочнике нет. Подставлять близкий эквивалент нельзя —"
          f" сверь знак по источнику и допиши строку.", file=sys.stderr)
    return 1


def cmd_word(args: argparse.Namespace) -> int:
    """Слово в локальном словаре: спрашивать thai-language.com повторно не нужно."""
    path = DATA / "dictionary.json"
    if not path.exists():
        print("нет data/dictionary.json — словарь ещё не собран", file=sys.stderr)
        return 1
    data = json.loads(path.read_text(encoding="utf-8"))
    hit = data.get("words", {}).get(args.word.strip())
    if hit is None:
        print(f"{args.word}: в локальном словаре нет — сверять по источнику "
              f"(см. skill thai-verify)", file=sys.stderr)
        return 1
    print(f"{args.word}")
    print(f"  словарь:     {hit['dictionary']}")
    print(f"  наша запись: {hit['ours'] or '— не сверена'}")
    if not hit["tones_ok"]:
        print("  ⚠ тоны нашей записи расходятся со словарём")
    return 0


def cmd_finals(args: argparse.Namespace) -> int:
    wanted = args.sound.strip()
    hits = [r for r in parse_consonants() if r.final == wanted]
    if not hits:
        known = sorted({r.final for r in parse_consonants() if r.final != "—"})
        print(f"финали «{wanted}» в справочнике нет. Есть: {', '.join(known)}", file=sys.stderr)
        return 1
    print(f"финаль «{wanted}» дают {len(hits)} знаков:")
    for r in hits:
        sub = f", {r.sub}" if r.sub else ""
        print(f"  {r.sign}  ({r.cls} класс{sub}, в инициали {r.initial})")
    return 0


def clusters_of(value: str) -> List[str]:
    """Строка, разбитая на кластеры «база + её комбинирующие знаки»."""
    out: List[str] = []
    for ch in unicodedata.normalize("NFD", value):
        if unicodedata.combining(ch) and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def check_cell(value: str, allowed: AbstractSet[str]) -> Optional[str]:
    """Первая претензия к ячейке или None.

    Кластер годится, если он либо целиком есть в алфавите (ȯ — самостоятельный знак),
    либо его база есть в алфавите, а все навешанные знаки — тоновые (а̀, ѝ). Латиница
    с диакритикой (â, ò) не проходит ни по одному условию.
    """
    ok = set(allowed)
    for cluster in clusters_of(value):
        base, marks = cluster[0], cluster[1:]
        # ȯ — цельный знак, собранный из латинской o и точки: ищем самый длинный
        # префикс кластера, который есть в алфавите, остальное считаем знаками тона
        for cut in range(len(cluster), 0, -1):
            if unicodedata.normalize("NFC", cluster[:cut]) in ok:
                base, marks = cluster[:cut], cluster[cut:]
                break
        if not marks and unicodedata.normalize("NFC", base) in ok:
            continue
        for mark in marks:
            if mark in ALIEN:
                return ALIEN[mark]
        if not base.isalpha():
            continue
        if base in ALIEN:
            return ALIEN[base]
        if base not in ok:
            return f"знак «{unicodedata.normalize('NFC', cluster)}» вне системы"
        stray = [m for m in marks if m not in TONE_MARKS]
        if stray:
            return f"чужая диакритика над «{base}»"
        # тоновый знак — строго над гласной, см. alphabet.md
        if any(m in TONE_MARKS for m in marks) and base not in VOWELS:
            return f"тоновый знак над согласной «{base}»"
    return None


def transcription_cells(text: str, skip_tolerant: bool = True) -> List[Tuple[int, str]]:
    """Ячейки колонок, названных транскрипционными в шапке своей же таблицы.

    Единственное место, которое решает, что в файле транскрипция, а что перевод или
    примечание. И сборка алфавита, и проверка ходят через него — иначе они разойдутся.
    """
    found: List[Tuple[int, str]] = []
    tolerant = False
    header: Optional[List[str]] = None
    cols: List[int] = []
    for n, line in enumerate(text.split("\n"), 1):
        if line.startswith("#"):
            tolerant = bool(TOLERANT.search(line))
            header, cols = None, []
            continue
        cs = cells(line)
        if cs is None:
            header, cols = None, []
            continue
        if SEP.match(line):
            cols = [i for i, h in enumerate(header or []) if TRANSCR_COL.search(h)]
            header = None
            continue
        if not cols:
            header = cs
            continue
        if tolerant and skip_tolerant:
            continue
        for i in cols:
            if i >= len(cs) or THAI.search(cs[i]) or IPA_CELL.match(cs[i]):
                continue
            found.append((n, cs[i]))
    return found


def scan_alien(text: str, where: str, alphabet: Sequence[str]) -> List[str]:
    """Чужие знаки в транскрипционных колонках; терпимые разделы пропускаются."""
    problems: List[str] = []
    allowed = set(alphabet) | set(TONE_MARKS) | set(" -–—/()·,.?…")
    for n, value in transcription_cells(text):
        bad = check_cell(value, allowed)
        if bad:
            problems.append(f"{where}:{n}: {bad}, в «{value}»")
    return problems


def alphabet() -> List[str]:
    """Буквы, из которых может состоять транскрипция — по инвентарю из tables.json."""
    return sorted(tables().get("alphabet", {}))


def vowel_signs() -> Dict[str, str]:
    """Тайский знак гласной → наша запись. Ключ один на знак, а не «ึ / ื»."""
    data = tables()
    out: Dict[str, str] = {}
    for key in ("simple", "diphthongs"):
        for thai, row in data.get(key, {}).items():
            out[thai] = row["cyrillic"]
    return out


def declared_alphabet() -> Dict[str, str]:
    return {sign: r["code"] for sign, r in tables().get("alphabet", {}).items()}


def check_declaration(used: Sequence[str]) -> List[str]:
    """Инвентарь из alphabet.md против букв, реально стоящих в таблицах."""
    problems: List[str] = []
    declared = declared_alphabet()
    if not declared:
        return ["alphabet.md: таблица «Буквы» не разобралась"]
    for sign, code in declared.items():
        expected = f"U+{ord(sign):04X}" if len(sign) == 1 else "составной"
        if code.strip().upper() != expected:
            problems.append(f"alphabet.md: у «{sign}» записан {code}, а на деле {expected}")
    for ch in used:
        if ch not in declared:
            problems.append(f"«{ch}» стоит в таблицах, но не объявлен в alphabet.md")
    for ch in declared:
        if ch not in set(used):
            problems.append(f"«{ch}» объявлен в alphabet.md, но нигде не используется")
    return problems


def check_frame() -> List[str]:
    """Общая рамка справочника: см. раздел «Справочники» в SKILL.md."""
    problems: List[str] = []
    for name in REQUIRED:
        text = read(name)
        if not text:
            continue
        lines = text.split("\n")
        heads = [ln for ln in lines if ln.startswith("## ")]
        if not lines[0].startswith("# "):
            problems.append(f"{name}: нет заголовка первой строкой")
        if "Читать этот файл" not in text and "Читать, когда" not in text:
            problems.append(f"{name}: нет строки «Читать этот файл, когда…»")
        if "**Откуда взято.**" not in text:
            problems.append(f"{name}: нет раздела «Откуда взято»")
        if not heads or heads[-1] != "## Чего этот файл не решает":
            problems.append(f"{name}: последним разделом должен быть «Чего этот файл не решает»")
        body = [h for h in heads
                if h not in ("## Чего этот файл не решает", "## Требует сверки")]
        for i, head in enumerate(body, 1):
            if not head.startswith(f"## {i}. "):
                problems.append(f"{name}: раздел «{head[3:]}» должен идти под номером {i}")
                break
    return problems


def check_skill_matches(rows: List[Row]) -> List[str]:
    """Таблица особых правил в SKILL.md не должна расходиться со справочником."""
    problems: List[str] = []
    by_sign = {r.sign: r for r in rows}
    for line in (SKILL / "SKILL.md").read_text(encoding="utf-8").split("\n"):
        cs = cells(line)
        if not cs or len(cs) < 3 or not THAI.search(cs[0]):
            continue
        for sign in re.findall(r"[฀-๿]+", cs[0]):
            row = by_sign.get(sign)
            if row is None:
                continue
            if cs[1] != row.initial or cs[2] != row.final:
                problems.append(
                    f"SKILL.md: {sign} → {cs[1]} / {cs[2]}, "
                    f"а в consonants.md {row.initial} / {row.final}")
    return problems


def cmd_check(args: argparse.Namespace) -> int:
    problems: List[str] = []
    for name in REQUIRED:
        if not (REFS / name).exists():
            problems.append(f"нет файла references/{name}")
    for name in REQUIRED_DATA:
        if not (DATA / name).exists():
            problems.append(f"нет файла data/{name}")
    rows = parse_consonants()
    if not rows:
        problems.append("consonants.md: таблицы согласных не разобрались")
    seen: Dict[str, int] = {}
    for r in rows:
        seen[r.sign] = seen.get(r.sign, 0) + 1
    for sign, n in seen.items():
        if n > 1:
            problems.append(f"consonants.md: знак {sign} встречается {n} раза")
    letters = alphabet()
    for name in ("consonants.md", "vowels.md", "clusters.md", "silent-letters.md"):
        problems += scan_alien(read(name), name, letters)
    problems += check_frame()
    problems += check_declaration(letters)
    problems += check_skill_matches(rows)

    if args.course:
        for folder in COURSE:
            base = ROOT / folder
            if not base.exists():
                continue
            for path in sorted(base.rglob("*.md")):
                problems += scan_alien(path.read_text(encoding="utf-8"),
                                       str(path.relative_to(ROOT)), letters)

    print(f"знаков в таблице согласных: {len(rows)}")
    print(f"букв в алфавите транскрипции: {len(letters)}")
    if not problems:
        print("проверка пройдена")
        return 0
    print(f"\nнайдено проблем: {len(problems)}")
    for p in problems:
        print("  ", p)
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_sign = sub.add_parser("sign", help="справка по знаку")
    p_sign.add_argument("sign")
    p_sign.set_defaults(func=cmd_sign)

    p_word = sub.add_parser("word", help="слово в локальном словаре")
    p_word.add_argument("word")
    p_word.set_defaults(func=cmd_word)

    p_fin = sub.add_parser("finals", help="какие знаки дают эту финаль")
    p_fin.add_argument("sound")
    p_fin.set_defaults(func=cmd_finals)

    p_chk = sub.add_parser("check", help="проверить справочники")
    p_chk.add_argument("--course", action="store_true",
                       help="проверить заодно файлы курса")
    p_chk.set_defaults(func=cmd_check)

    args = ap.parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
