#!/usr/bin/env python3
"""
tracker.py — учёт прогресса для skill thai-tasks (SM-2 + база ошибок).

Только стандартная библиотека Python 3.8+. Один файл-состояние: progress.json.
Логика полностью соответствует references/progress-and-spiral.md.

Команды:
  due       — что пора повторить (get_due) для 40% спирали
  record    — применить SM-2 к элементу по качеству ответа 0–5
  mistake   — записать/обновить паттерн ошибки
  import    — импортировать словарь из glava-файла в трекер
  progress  — краткий обзор прогресса
  set-meta  — обновить meta (difficulty, recent_accuracy)

Примеры:
  python3 tracker.py due progress.json
  python3 tracker.py record progress.json "ข้าว" 5
  python3 tracker.py record progress.json "счётные слова จาน/ที่" 2 --type rule --topic 6.1.2
  python3 tracker.py mistake progress.json "тон_закрытый_слог_высокий_класс" \
        --category Тоны --your средний --correct нисходящий --context "ข้าว"
  python3 tracker.py import progress.json glava6_tema1_eda.md --topic 6.1
  python3 tracker.py progress progress.json
  python3 tracker.py set-meta progress.json --difficulty 5 --recent-accuracy 0.68
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

DATE_FMT = "%Y-%m-%d"

# Интервалы SM-2 задаются формулой; таблица ниже — только для reps 1 и 2.
DEFAULT_ITEM = {
    "translation": "", "type": "word", "topic": "",
    "repetitions": 0, "interval_days": 0, "easiness_factor": 2.5,
    "due_date": "1970-01-01", "last_seen": "1970-01-01",
    "mastery": 0, "consecutive_correct": 0, "consecutive_incorrect": 0,
}


def today():
    return date.today()


def parse_date(s):
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except (ValueError, TypeError):
        return date(1970, 1, 1)


def load(path):
    if not os.path.exists(path):
        return {"meta": {"difficulty": 4, "target_success": [0.6, 0.7],
                         "recent_accuracy": 0.0, "updated": today().strftime(DATE_FMT)},
                "items": {}, "mistakes": {}}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("meta", {"difficulty": 4, "target_success": [0.6, 0.7],
                             "recent_accuracy": 0.0, "updated": today().strftime(DATE_FMT)})
    data.setdefault("items", {})
    data.setdefault("mistakes", {})
    return data


def save(path, data):
    data["meta"]["updated"] = today().strftime(DATE_FMT)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def interval_for(mastery):
    """Резервная таблица (используется в due для элементов без due_date)."""
    return {0: 0, 1: 1, 2: 3, 3: 7, 4: 14, 5: 30}.get(mastery, 1)


# ---------- команды ----------

def cmd_due(data, args):
    t = today()
    due_items = []
    for key, it in data["items"].items():
        dd = parse_date(it.get("due_date", "1970-01-01"))
        if dd <= t:
            due_items.append((key, it))
    # приоритет: низкий mastery, затем ранняя due_date
    due_items.sort(key=lambda kv: (kv[1].get("mastery", 0),
                                   parse_date(kv[1].get("due_date", "1970-01-01"))))

    due_mistakes = []
    for key, m in data["mistakes"].items():
        if m.get("status", "active") != "active":
            continue
        if parse_date(m.get("next_review", "1970-01-01")) <= t:
            due_mistakes.append((key, m))
    due_mistakes.sort(key=lambda kv: -kv[1].get("frequency", 0))

    limit = args.limit
    out = {
        "mistakes_due": [
            {"pattern": k, "category": m.get("category", ""),
             "frequency": m.get("frequency", 0)}
            for k, m in (due_mistakes[:limit] if limit else due_mistakes)
        ],
        "items_due": [
            {"item": k, "type": it.get("type", "word"),
             "topic": it.get("topic", ""), "mastery": it.get("mastery", 0),
             "translation": it.get("translation", "")}
            for k, it in (due_items[:limit] if limit else due_items)
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_record(data, args):
    key = args.item
    it = data["items"].get(key, dict(DEFAULT_ITEM))
    if args.type:
        it["type"] = args.type
    if args.topic:
        it["topic"] = args.topic
    if args.translation:
        it["translation"] = args.translation

    q = args.quality
    ef = it.get("easiness_factor", 2.5)
    reps = it.get("repetitions", 0)
    interval = it.get("interval_days", 0)
    cc = it.get("consecutive_correct", 0)
    ci = it.get("consecutive_incorrect", 0)
    mastery = it.get("mastery", 0)

    if q >= 3:
        reps += 1
        if reps == 1:
            interval = 1
        elif reps == 2:
            interval = 6
        else:
            interval = round(interval * ef)
        cc += 1
        ci = 0
    else:
        reps = 0
        interval = 1
        ci += 1
        cc = 0

    ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    ef = max(1.3, ef)

    if cc >= 5:
        mastery = min(5, mastery + 1)
    elif ci >= 3:
        mastery = max(0, mastery - 1)

    t = today()
    it.update({
        "repetitions": reps, "interval_days": interval,
        "easiness_factor": round(ef, 3),
        "last_seen": t.strftime(DATE_FMT),
        "due_date": (t + timedelta(days=interval)).strftime(DATE_FMT),
        "consecutive_correct": cc, "consecutive_incorrect": ci,
        "mastery": mastery,
    })
    data["items"][key] = it
    print(f"OK: {key} → mastery {mastery}, интервал {interval}д, "
          f"следующий повтор {it['due_date']} (EF {it['easiness_factor']})")


def cmd_mistake(data, args):
    key = args.pattern
    t = today()
    m = data["mistakes"].get(key, {
        "category": args.category or "", "subcategory": "", "frequency": 0,
        "status": "active", "last_occurred": "", "next_review": "",
        "examples": [], "notes": args.notes or "",
    })
    if args.category:
        m["category"] = args.category
    if args.notes:
        m["notes"] = args.notes
    m["frequency"] = m.get("frequency", 0) + 1
    m["status"] = "active"
    m["last_occurred"] = t.strftime(DATE_FMT)
    # слабое место должно вернуться скоро
    m["next_review"] = (t + timedelta(days=1)).strftime(DATE_FMT)
    if args.your or args.correct:
        m["examples"].append({
            "your_answer": args.your or "", "correct_answer": args.correct or "",
            "context": args.context or "", "date": t.strftime(DATE_FMT),
        })
    data["mistakes"][key] = m
    print(f"OK: паттерн «{key}» — частота {m['frequency']}, "
          f"следующий повтор {m['next_review']}")


def cmd_resolve(data, args):
    key = args.pattern
    if key in data["mistakes"]:
        data["mistakes"][key]["status"] = "resolved"
        print(f"OK: паттерн «{key}» помечен resolved")
    else:
        print(f"нет такого паттерна: {key}", file=sys.stderr)


# Таблица словаря в glava-файлах: | тайский | транскрипция | перевод |
ROW_RE = re.compile(r"^\|(.+)\|(.+)\|(.+)\|\s*$")
HEADER_WORDS = {"тайский", "транскрипция", "перевод", "term", ""}


def clean_cell(s):
    s = s.strip()
    s = s.replace("**", "").strip()
    return s


def cmd_import(data, args):
    if not os.path.exists(args.source):
        print(f"файл не найден: {args.source}", file=sys.stderr)
        sys.exit(1)
    added, skipped = 0, 0
    with open(args.source, "r", encoding="utf-8") as f:
        for line in f:
            mm = ROW_RE.match(line)
            if not mm:
                continue
            thai = clean_cell(mm.group(1))
            translit = clean_cell(mm.group(2))
            translation = clean_cell(mm.group(3))
            # пропустить заголовки и разделители таблиц
            if thai.lower() in HEADER_WORDS or set(thai) <= set("-: "):
                continue
            # тайский должен содержать тайские символы
            if not re.search(r"[฀-๿]", thai):
                continue
            if thai in data["items"]:
                skipped += 1
                continue
            it = dict(DEFAULT_ITEM)
            it.update({
                "translation": translation, "type": "word",
                "topic": args.topic or "",
                "due_date": today().strftime(DATE_FMT),  # сразу due
                "last_seen": "1970-01-01",
            })
            # транскрипцию храним в notes-поле translation? оставим отдельно:
            it["translit"] = translit
            data["items"][thai] = it
            added += 1
    print(f"Импорт из {os.path.basename(args.source)}: добавлено {added}, "
          f"пропущено (уже были) {skipped}")


def stars(m):
    return "⭐" * m + "☆" * (5 - m)


def cmd_progress(data, args):
    meta = data["meta"]
    t = today()
    items = data["items"]
    # средний mastery по темам
    by_topic = {}
    for it in items.values():
        tp = it.get("topic", "") or "—"
        by_topic.setdefault(tp, []).append(it.get("mastery", 0))
    due_count = sum(1 for it in items.values()
                    if parse_date(it.get("due_date", "1970-01-01")) <= t)
    active_mistakes = [(k, m) for k, m in data["mistakes"].items()
                       if m.get("status", "active") == "active"]

    print(f"Прогресс — тайский · сложность {meta.get('difficulty', 4)} · "
          f"точность (новое): {int(meta.get('recent_accuracy', 0) * 100)}%")
    print(f"Слов/правил в трекере: {len(items)}\n")
    print("Темы (средний mastery):")
    for tp in sorted(by_topic):
        vals = by_topic[tp]
        avg = round(sum(vals) / len(vals)) if vals else 0
        print(f"  {tp:<10} {stars(avg)}  ({avg}/5, {len(vals)} эл.)")
    print(f"\nПора повторить (due): {due_count}")
    if active_mistakes:
        print("Активные слабые места:")
        for k, m in sorted(active_mistakes, key=lambda kv: -kv[1].get("frequency", 0)):
            print(f"  • {m.get('category','')}: {k} — {m.get('frequency',0)}×")


def cmd_set_meta(data, args):
    if args.difficulty is not None:
        data["meta"]["difficulty"] = args.difficulty
    if args.recent_accuracy is not None:
        data["meta"]["recent_accuracy"] = args.recent_accuracy
    print(f"OK: meta обновлена → {json.dumps(data['meta'], ensure_ascii=False)}")


def main():
    p = argparse.ArgumentParser(description="Трекер прогресса thai-tasks (SM-2 + ошибки)")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("due", help="что пора повторить")
    d.add_argument("path")
    d.add_argument("--limit", type=int, default=None)

    r = sub.add_parser("record", help="SM-2 по качеству ответа 0–5")
    r.add_argument("path")
    r.add_argument("item")
    r.add_argument("quality", type=int, choices=range(0, 6))
    r.add_argument("--type", choices=["word", "rule", "construction"])
    r.add_argument("--topic")
    r.add_argument("--translation")

    m = sub.add_parser("mistake", help="записать паттерн ошибки")
    m.add_argument("path")
    m.add_argument("pattern")
    m.add_argument("--category")
    m.add_argument("--your")
    m.add_argument("--correct")
    m.add_argument("--context")
    m.add_argument("--notes")

    rv = sub.add_parser("resolve", help="закрыть паттерн ошибки")
    rv.add_argument("path")
    rv.add_argument("pattern")

    im = sub.add_parser("import", help="импорт словаря из glava-файла")
    im.add_argument("path")
    im.add_argument("source")
    im.add_argument("--topic")

    pr = sub.add_parser("progress", help="обзор прогресса")
    pr.add_argument("path")

    sm = sub.add_parser("set-meta", help="обновить meta")
    sm.add_argument("path")
    sm.add_argument("--difficulty", type=int)
    sm.add_argument("--recent-accuracy", type=float, dest="recent_accuracy")

    args = p.parse_args()
    data = load(args.path)

    handlers = {
        "due": cmd_due, "record": cmd_record, "mistake": cmd_mistake,
        "resolve": cmd_resolve, "import": cmd_import, "progress": cmd_progress,
        "set-meta": cmd_set_meta,
    }
    handlers[args.cmd](data, args)

    # команды, меняющие состояние, сохраняют файл
    if args.cmd in {"record", "mistake", "resolve", "import", "set-meta"}:
        save(args.path, data)


if __name__ == "__main__":
    main()
