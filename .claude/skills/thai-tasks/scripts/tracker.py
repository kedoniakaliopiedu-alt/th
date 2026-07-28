#!/usr/bin/env python3
"""
tracker.py — учёт прогресса для skill thai-tasks (SM-2 + база ошибок).

Только стандартная библиотека Python 3.8+. Один файл-состояние: progress.json.
Логика полностью соответствует references/progress-and-spiral.md.

Команды:
  due        — что пора повторить (get_due) для 40% спирали
  record     — применить SM-2 к элементу по качеству ответа 0–5
  mistake    — записать/обновить паттерн ошибки
  mistakes   — список паттернов с фильтрами (для skill thai-mistakes)
  drill-plan — план работы над ошибками: группы по темам, режимы, объём
  attempt    — итог круга отработки (снята / повторилась)
  import     — импортировать словарь из glava-файла в трекер
  progress   — краткий обзор прогресса
  set-meta   — обновить meta (difficulty, recent_accuracy)
  topics     — состояния тем: что в работе, что закрыто, что мешает закрыть
  blockers   — что мешает закрыть конкретную тему (не больше трёх пунктов)
  close      — итог закрывающего испытания темы (ворота проверяются здесь)
  lesson     — отметить занятие по теме: только эта команда двигает паузу

Примеры:
  python3 tracker.py due progress.json
  python3 tracker.py record progress.json "ข้าว" 5
  python3 tracker.py record progress.json "счётные слова จาน/ที่" 2 --type rule --topic 6.1.2
  python3 tracker.py mistake progress.json "тон_закрытый_слог_высокий_класс" \
        --category Тоны --topic 6.1 --your средний --correct нисходящий --context "ข้าว"
  python3 tracker.py mistakes progress.json --topic 6.1
  python3 tracker.py drill-plan progress.json
  python3 tracker.py attempt progress.json "тон_закрытый_слог_высокий_класс" --result ok
  python3 tracker.py import progress.json glava6_tema1_eda.md --topic 6.1
  python3 tracker.py progress progress.json
  python3 tracker.py set-meta progress.json --difficulty 5 --recent-accuracy 0.68
  python3 tracker.py topics progress.json
  python3 tracker.py blockers progress.json 3.4
  python3 tracker.py close progress.json 3.4 --result ok \
        --production --no-hints --calibrated --accuracy 0.9
"""

from __future__ import annotations  # аннотации ленивые: скрипт идёт на Python 3.8+

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from collections.abc import Callable
from datetime import date, datetime, timedelta
from typing import Any, NoReturn, TypedDict, cast

DATE_FMT = "%Y-%m-%d"


# ---------- форма файла состояния ----------
#
# progress.json описан здесь как набор TypedDict, а не безымянных словарей: каждое
# поле разбросано по двум десяткам функций, и без объявленной формы проверяющий типов
# видит у любой записи «строка или число или список или None» — а значит молчит и там,
# где поле перепутано на самом деле.
#
# Что проверяется в рантайме и что нет. `load` проверяет КАРКАС: верхний уровень —
# объект, четыре раздела — объекты, каждая запись в них — объект; иначе отказ с
# объяснением, без записи. ПОЛНОТУ ПОЛЕЙ внутри записи не проверяет никто: ошибки
# добивает `normalize_mistake` в местах обращения, у элементов и тем недостающие поля
# читаются через `.get` с умолчанием. То есть набор полей — договор между кодом и
# `progress-and-spiral.md`, и файл, отредактированный руками, может ему не
# соответствовать, не вызвав ни одной жалобы.

class Attempt(TypedDict):
    """Одна попытка закрывающего испытания темы."""
    date: str
    result: str
    accuracy: float | None
    counted: bool
    blocked_by: list[str]
    # Гасится ли круг. У новых попыток проставляется сразу, но записи, сделанные
    # прежними версиями, поля не имеют и не мигрируются — поэтому читается оно
    # по-прежнему через `.get` (см. counted_days).
    voided: bool


class TopicRec(TypedDict):
    """Состояние темы: путь от «в работе» до «закрыта» и обратно."""
    title: str
    status: str
    exit_task: str
    core: list[str]
    attempts: list[Attempt]
    closed_on: str | None
    reopened_on: str | None
    next_control: str | None
    control_step: int
    closed_at_difficulty: int | None
    suspicion: int
    last_lesson: str
    last_shake: str


class Item(TypedDict):
    """Слово или правило под SM-2."""
    translation: str
    translit: str
    type: str
    topic: str
    repetitions: int
    interval_days: int
    easiness_factor: float
    due_date: str
    last_seen: str
    mastery: int
    consecutive_correct: int
    consecutive_incorrect: int


class Example(TypedDict):
    """Живой пример ошибки: что было написано и что следовало."""
    your_answer: str
    correct_answer: str
    context: str
    date: str


class Mistake(TypedDict):
    """Паттерн ошибки и ход его отработки."""
    category: str
    subcategory: str
    topic: str
    frequency: int
    status: str
    last_occurred: str
    next_review: str
    examples: list[Example]
    notes: str
    mode: str
    rounds: int
    drill_ok: int
    last_drill: str


class Meta(TypedDict):
    difficulty: int
    target_success: list[float]
    recent_accuracy: float
    updated: str


class Data(TypedDict):
    """Весь progress.json."""
    meta: Meta
    items: dict[str, Item]
    mistakes: dict[str, Mistake]
    topics: dict[str, TopicRec]


class TopicLevel(TypedDict):
    """Срез уровня темы по её ядру — то, что показывают `topics` и `blockers`."""
    core: int
    median: float
    worst: int
    repeated_share: float
    last_seen: str


class DrillGroup(TypedDict):
    """Ошибки одной темы, собранные в один блок отработки (`drill-plan`)."""
    topic: str
    mistakes: list[dict[str, Any]]
    modes: list[str]


class VocabEntry(TypedDict):
    """Слово темы для режима «запоминание слов» — то, из чего собирается дрилл."""
    item: str
    translation: str
    translit: str
    mastery: int

# Интервалы SM-2 задаются формулой в cmd_record; фиксированы только первые два
# повторения (1 день и 6 дней).
def new_item() -> Item:
    """Свежая запись слова или правила."""
    return {
        "translation": "", "translit": "", "type": "word", "topic": "",
        "repetitions": 0, "interval_days": 0, "easiness_factor": 2.5,
        "due_date": "1970-01-01", "last_seen": "1970-01-01",
        "mastery": 0, "consecutive_correct": 0, "consecutive_incorrect": 0,
    }


# Режимы отработки ошибок (skill thai-mistakes). Категория → режим дрилла.
# Порядок важен: первое совпадение подстроки в категории (в нижнем регистре) выигрывает.
MODE_BY_CATEGORY = (
    (("чтен", "кластер"), "spelling"),
    (("лекс", "словар"), "vocab"),
    (("тон", "произнош", "фонет"), "tones"),
    (("орфогр", "написан", "класс согл"), "spelling"),
    (("грамм", "конструкц", "порядок слов", "частиц", "счётн", "счетн"), "grammar"),
    (("регистр", "обращ", "вежлив", "прагмат", "этикет"), "register"),
    (("термин", "формулиров", "инструкц"), "reference"),
)

MODE_TITLES = {
    "vocab": "запоминание слов",
    "tones": "тоновый дрилл",
    "grammar": "трансформации",
    "spelling": "восстановление написания",
    "register": "регистр и уместность",
    "reference": "справка без дрилла",
    "general": "смешанный",
}

# ---------- состояния темы (критерий закрытия) ----------

def new_topic() -> TopicRec:
    """Свежая запись темы.

    Функция, а не словарь-константа: `dict(КОНСТАНТА)` копирует поверхностно, и списки
    `core`/`attempts` оказались бы общими у всех тем. Прежний код от этого спасался
    тем, что `get_topic` пересобирал оба списка сразу после копирования — работало, но
    держалось на памяти о двух строчках в другом месте файла. Фабрика снимает вопрос:
    ошибиться негде.
    """
    return {
        "title": "", "status": "in_progress", "exit_task": "", "core": [],
        "attempts": [], "closed_on": None, "reopened_on": None,
        "next_control": None, "control_step": 0, "closed_at_difficulty": None,
        "suspicion": 0, "last_lesson": "", "last_shake": "",
    }

TOPIC_STATUS_RU = {
    "no_criterion": "нет критерия",
    "in_progress": "в работе",
    "testing": "на испытании",
    "closed": "закрыта",
    "returned": "вернулась",
}

# Ворота закрытия: пауза с последнего занятия, минимальный mastery по худшему
# элементу ядра, результат испытания, два успешных круга. Прочие ворота (доля
# продукции, отсутствие подсказок, совпадение с калибровкой) вычислить из данных
# нельзя — это свойства самого листа, их подтверждают флаги `close`.
# Пауза меряется по `last_lesson` темы, а не по `last_seen` элементов: запись
# результатов испытания через `record` иначе обнуляла бы паузу сама.
CLOSE_PAUSE_DAYS = 7
CLOSE_MIN_MASTERY = 2
CLOSE_ROUNDS = 2
# Порог сдачи самого испытания — наследует контрольные thai-learning.
CLOSE_MIN_ACCURACY = 0.85
# Сколько блокеров показываем человеку: длинный список — не список, а приговор.
BLOCKERS_SHOWN = 3
# Сколько элементов закрытых тем поднимать фоном в задания по другим темам.
BACKGROUND_LIMIT = 4
# Ядро темы: правила целиком + слова добором до этого размера.
CORE_SIZE = 18
# Редкий контроль после закрытия.
CONTROL_STEPS = [90, 180, 365]
# Сколько ошибок по закрытой теме до переоткрытия: 1 — подозрение, 2 — вернулась.
SUSPICION_LIMIT = 2

# Mastery растёт после трёх верных подряд, а не пяти: пять подряд по одному элементу
# практически не набирается между интервалами SM-2, и критерий поверх такой шкалы мёртв.
MASTERY_UP_AFTER = 3
MASTERY_DOWN_AFTER = 3

# Интервалы после успешного круга отработки: 1-й ок → +3д, 2-й → +7д, дальше +16д.
DRILL_INTERVALS = {1: 3, 2: 7}
DRILL_INTERVAL_LONG = 16
# Сколько кругов за одно занятие максимум (дальше — на следующее занятие).
MAX_ROUNDS_PER_DAY = 2


def today() -> date:
    return date.today()


def mode_for(category: str | None, override: str | None = None) -> str:
    """Режим отработки по категории ошибки."""
    if override:
        return override
    cat = (category or "").lower()
    for keys, mode in MODE_BY_CATEGORY:
        if any(k in cat for k in keys):
            return mode
    return "general"


def normalize_mistake(m: Any, category: str | None = None) -> Mistake:
    """Добить старую запись ошибки полями, которые нужны работе над ошибками.

    Вход намеренно `Any`: сюда попадает и запись прямо из JSON (форма неизвестна), и
    пустой словарь для новой ошибки, и уже полная `Mistake`. Смысл функции ровно в том,
    чтобы привести всё это к одной форме — объявить вход строже значило бы требовать
    гарантию, которую эта функция как раз и выдаёт.
    """
    m.setdefault("category", category or "")
    m.setdefault("subcategory", "")
    m.setdefault("topic", "")
    m.setdefault("frequency", 0)
    m.setdefault("status", "active")
    m.setdefault("last_occurred", "")
    m.setdefault("next_review", "")
    m.setdefault("examples", [])
    m.setdefault("notes", "")
    m.setdefault("mode", "")
    m.setdefault("rounds", 0)        # всего кругов отработки
    m.setdefault("drill_ok", 0)      # подряд успешных кругов
    m.setdefault("last_drill", "")   # дата последнего круга
    # setdefault выше довёл запись до полного набора полей Mistake — приведение
    # опирается на это, а не на веру: до него форма записи из JSON неизвестна.
    return cast(Mistake, m)


def nfc(key: str) -> str:
    """Ключ элемента в канонической форме NFC.

    Тайские тоновые знаки и нижние гласные переставляются нормализацией, поэтому одно
    и то же слово, набранное в разном порядке, давало два разных ключа словаря —
    и mastery расходился по ним. Нормализуем в одной точке: на входе в трекер.
    """
    return unicodedata.normalize("NFC", key)


def merge_denormalized_keys(items: dict[str, Item]) -> list[str]:
    """Свести накопленные до нормализации дубли к одному ключу.

    При коллизии историю берём у той записи, где её больше, а описательные поля —
    у той, где они непустые. Раньше проигравшая запись выбрасывалась целиком, и
    полная карточка, столкнувшись с голым дублём с большей историей, теряла перевод,
    транскрипцию и тему: слово оставалось в выдаче, но собрать по нему задание было
    уже нельзя.

    Возвращает список слитых ключей, а не счётчик: молчаливое слияние по имени
    невозможно проверить, а называть изменённое слово — единственный способ заметить,
    что тронули не то.
    """
    merged: list[str] = []
    for key in list(items):
        canon = nfc(key)
        if canon == key:
            continue
        existing = items.get(canon)
        candidate = items.pop(key)
        if existing is None:
            items[canon] = candidate
        else:
            rich, poor = ((existing, candidate)
                          if (existing.get("repetitions", 0), existing.get("mastery", 0))
                          >= (candidate.get("repetitions", 0), candidate.get("mastery", 0))
                          else (candidate, existing))
            # Поля перечислены поимённо, а не циклом по списку имён: у TypedDict
            # ключ-переменная не проверяется, и цикл пришлось бы глушить type: ignore.
            if not rich.get("translation") and poor.get("translation"):
                rich["translation"] = poor["translation"]
            if not rich.get("translit") and poor.get("translit"):
                rich["translit"] = poor["translit"]
            if not rich.get("topic") and poor.get("topic"):
                rich["topic"] = poor["topic"]
            items[canon] = rich
        merged.append(canon)
    return merged


def parse_date(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except (ValueError, TypeError):
        return date(1970, 1, 1)


def check_shape(data: Any) -> None:
    """Проверить каркас разобранного трекера. Бросает ValueError с описанием беды.

    Отдельной функцией, а не строчками внутри `load`: `isinstance` сужает тип, и это
    сужение растекалось бы по всему `load`, лишая `data` совместимости с `Data`.
    Здесь оно заперто в своей области видимости.
    """
    if not isinstance(data, dict):
        raise ValueError("на верхнем уровне {}, а нужен объект".format(
            type(data).__name__))
    sections = cast("dict[str, Any]", data)
    for name in ("meta", "items", "mistakes", "topics"):
        if name in sections and not isinstance(sections[name], dict):
            raise ValueError("«{}» — {}, а нужен объект".format(
                name, type(sections[name]).__name__))
    for name in ("items", "mistakes", "topics"):
        section: Any = sections.get(name)
        for key, rec in cast("dict[str, Any]", section or {}).items():
            if not isinstance(rec, dict):
                raise ValueError("запись «{}» в «{}» — {}, а нужен объект".format(
                    key, name, type(rec).__name__))


def load(path: str) -> tuple[Data, list[str]]:
    """Прочитать трекер. Возвращает (данные, ключи, слитые миграцией NFC).

    Слияние денормализованных ключей меняет данные, поэтому список слитого уходит
    наружу, а не тонет внутри чтения: `main` сообщает о нём в stderr.

    На диск слияние попадает только из пишущей команды — читающая остаётся читающей.
    Плата за это известна: пока не выполнена ни одна пишущая команда, миграция
    пересчитывается на каждом запуске. Так дешевле, чем позволить `due` переписывать
    трекер и его резервную копию.
    """
    if not os.path.exists(path):
        return {"meta": {"difficulty": 4, "target_success": [0.6, 0.7],
                         "recent_accuracy": 0.0, "updated": today().strftime(DATE_FMT)},
                "items": {}, "mistakes": {}, "topics": {}}, []
    def broken(reason: str) -> "NoReturn":
        """Отказаться работать с испорченным трекером, назвав причину.

        Одна точка выхода на все виды порчи: неразбираемый JSON и разбираемый, но не
        той формы, лечатся одинаково — руками или из копии, — и различать их в выводе
        незачем.
        """
        backup = path + ".bak"
        hint = (" Последняя целая копия: {}.".format(backup)
                if os.path.exists(backup) else "")
        print("{} повреждён и не прочитан ({}).{}\n"
              "Ничего не записываю: почини файл или восстанови копию."
              .format(path, reason, hint), file=sys.stderr)
        sys.exit(2)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data: Any = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        broken(str(e))
    except OSError as e:
        # Файл существует, но не читается: права, оборванная ссылка, каталог вместо файла.
        print("{} не открылся ({}). Ничего не записываю.".format(path, e), file=sys.stderr)
        sys.exit(2)

    # Каркас проверяется до первого обращения к полям. Без этого `{"items": []}` —
    # синтаксически корректный JSON — падал бы AttributeError уже внутри команды,
    # трейсбеком вместо объяснения; а `{"items": {"ไป": null}}` пролезал ещё дальше.
    try:
        check_shape(data)
    except ValueError as e:
        broken(str(e))

    data.setdefault("meta", {"difficulty": 4, "target_success": [0.6, 0.7],
                             "recent_accuracy": 0.0, "updated": today().strftime(DATE_FMT)})
    data.setdefault("items", {})
    data.setdefault("mistakes", {})
    data.setdefault("topics", {})
    # Приведение опирается на проверки выше: четыре раздела на месте и все они словари
    # словарей. Полноту полей внутри записей оно НЕ обещает — см. комментарий к схеме.
    checked = cast(Data, data)
    return checked, merge_denormalized_keys(checked["items"])


def save(path: str, data: Data) -> None:
    """Атомарная запись: сначала во временный файл, потом подмена.

    Прямая запись в `open(path, "w")` усекает трекер до того, как в него что-то
    попало: обрыв на середине уничтожает и словарь, и историю ошибок, а
    восстанавливать неоткуда. Поэтому пишем рядом и подменяем одним `os.replace`,
    предварительно отложив предыдущую версию в `.bak`.
    """
    data["meta"]["updated"] = today().strftime(DATE_FMT)
    directory = os.path.dirname(os.path.abspath(path))
    # Подмести хвосты от прошлых аварийных обрывов: подмена не состоялась,
    # временный файл остался.
    for stale in os.listdir(directory):
        if stale.startswith(".tracker-") and stale.endswith(".json"):
            try:
                os.remove(os.path.join(directory, stale))
            except OSError:
                pass
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tracker-", suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        if os.path.exists(path):
            shutil.copy2(path, path + ".bak")
        os.replace(tmp, path)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)


# ---------- темы: состояние, ядро, ворота закрытия ----------

def get_topic(data: Data, tp: str, title: str | None = None,
              create: bool = True) -> TopicRec:
    """Запись темы с добитыми полями. create=False — не заводить новую (чтение)."""
    if not create and tp not in data["topics"]:
        return new_topic()
    rec = new_topic()
    rec.update(data["topics"].get(tp, {}))
    # Записи старых версий могли хранить здесь null — нормализуем в список.
    rec["attempts"] = list(rec.get("attempts") or [])
    rec["core"] = list(rec.get("core") or [])
    if title and not rec["title"]:
        rec["title"] = title
    data["topics"][tp] = rec
    return rec


def counted_days(rec: TopicRec) -> set[str]:
    """Даты засчитанных кругов испытания — только те, что не погашены сбоем."""
    return {a["date"] for a in rec.get("attempts", [])
            if a.get("counted") and not a.get("voided")}


def void_rounds(rec: TopicRec) -> None:
    """Погасить засчитанные круги: после сбоя тема начинает испытание заново."""
    for a in rec.get("attempts", []):
        if a.get("counted"):
            a["voided"] = True


def topic_status(rec: TopicRec) -> str:
    """Тема без критерия закрытия честно показывается как «нет критерия».

    Отклонённые попытки статус не меняют — иначе одна неудачная попытка
    заставила бы таблицу состояний врать.
    """
    st = rec.get("status", "in_progress")
    if st == "in_progress" and not rec.get("exit_task") and not counted_days(rec):
        return "no_criterion"
    return st


def topic_items(data: Data, tp: str) -> dict[str, Item]:
    return {k: it for k, it in data["items"].items() if it.get("topic", "") == tp}


def topic_core(data: Data, tp: str, rec: TopicRec) -> list[str]:
    """Ядро темы: правила целиком, слова добором. Размеченное вручную — в приоритете.

    Ручная разметка проверяется на принадлежность теме: элемент чужой темы в ядре
    считал бы ворота по чужим данным.
    """
    items = topic_items(data, tp)
    marked = [k for k in rec.get("core", []) if k in items]
    if marked:
        return marked
    rules = [k for k, it in items.items()
             if it.get("type", "word") in ("rule", "construction")]
    words = [k for k in items if k not in rules]
    return rules + words[:max(0, CORE_SIZE - len(rules))]


def median(xs: list[int]) -> float:
    xs = sorted(xs)
    if not xs:
        return 0
    mid = len(xs) // 2
    return xs[mid] if len(xs) % 2 else (xs[mid - 1] + xs[mid]) / 2


def topic_level(data: Data, tp: str, rec: TopicRec) -> TopicLevel:
    """Уровень темы по ядру: медиана mastery, худший элемент, доля повторённых.

    Среднее арифметическое прячет мёртвый хвост, поэтому его здесь нет.
    """
    core = topic_core(data, tp, rec)
    items = [data["items"][k] for k in core if k in data["items"]]
    if not items:
        return {"core": 0, "median": 0, "worst": 0, "repeated_share": 0.0,
                "last_seen": "1970-01-01"}
    mastery = [it.get("mastery", 0) for it in items]
    repeated = sum(1 for it in items if it.get("repetitions", 0) >= 2)
    seen = max((it.get("last_seen", "1970-01-01") for it in items),
               default="1970-01-01")
    return {
        "core": len(items),
        "median": median(mastery),
        "worst": min(mastery),
        "repeated_share": round(repeated / len(items), 2),
        "last_seen": seen,
    }


def topic_blockers(data: Data, tp: str, rec: TopicRec) -> list[tuple[str, str]]:
    """Что мешает закрыть тему. Возвращает пары (код, текст) — полный набор.

    Код нужен для решения (жёсткий блокер или мягкий), текст — для показа.
    Решение по подстроке текста ломалось бы от любой переформулировки.
    """
    out: list[tuple[str, str]] = []
    if not rec.get("exit_task"):
        out.append(("no_criterion",
                    "в файле темы не нашлось критерия: ни секции «Тема закрыта, "
                    "если ты можешь», ни списка «должна уметь» в «Резюме по теме»"))
    lvl = topic_level(data, tp, rec)
    if not lvl["core"]:
        out.append(("no_core", "лексика темы не импортирована в трекер"))

    active = [k for k, m in data["mistakes"].items()
              if m.get("topic", "") == tp
              and m.get("status", "active") in ("active", "critical")]
    if active:
        out.append(("mistakes",
                    "активные ошибки по теме: " + ", ".join(sorted(active)[:3])))

    if lvl["core"] and lvl["worst"] < CLOSE_MIN_MASTERY:
        out.append(("mastery",
                    "в ядре темы ({} эл.) есть элементы с mastery {}, нужен минимум {} "
                    "по худшему".format(lvl["core"], lvl["worst"], CLOSE_MIN_MASTERY)))

    last_lesson = rec.get("last_lesson") or ""
    if not last_lesson:
        out.append(("no_lesson", "по теме ещё не отмечено ни одного занятия "
                                 "(tracker.py lesson <тема>)"))
    else:
        pause = (today() - parse_date(last_lesson)).days
        if pause < CLOSE_PAUSE_DAYS:
            out.append(("pause", "прошло {} дн. с последнего занятия по теме, "
                                 "нужно {}".format(pause, CLOSE_PAUSE_DAYS)))

    closed_at = rec.get("closed_at_difficulty")
    if closed_at is not None:
        grew = data["meta"].get("difficulty", 4) - closed_at
        if grew > 0:
            out.append(("difficulty",
                        "сложность выросла на {} с момента закрытия — "
                        "нужно переподтверждение".format(grew)))

    # Счётчик кругов показываем последним и только когда всё остальное снято: пока
    # мешает что-то ещё, «кругов 1 из 2» — не то, что нужно делать дальше.
    if not out and len(counted_days(rec)) < CLOSE_ROUNDS:
        out.append(("rounds", "успешных кругов испытания {} из {} "
                              "(второй — через интервал)".format(
                                  len(counted_days(rec)), CLOSE_ROUNDS)))
    return out


def hard_blockers(blockers: list[tuple[str, str]]) -> list[str]:
    """Жёсткие — всё, кроме счётчика кругов. Отбор по коду, не по тексту."""
    return [t for c, t in blockers if c != "rounds"]


def show_blockers(blockers: list[tuple[str, str]]) -> list[str]:
    """Для показа человеку — не длиннее трёх пунктов: длинный список это приговор."""
    return [t for _, t in blockers][:BLOCKERS_SHOWN]


def topic_shake(data: Data, tp: str, reason: str = "") -> str | None:
    """Ошибка по теме: снимает право на закрытие, закрытую двигает к возврату.

    За одно занятие тема получает не больше одного удара: штатный конвейер на один
    промах вызывает и `record`, и `mistake`, и без этого ступень «под подозрением»
    была бы недостижима.
    """
    if not tp:
        return None
    rec = get_topic(data, tp)
    t = today()
    stamp = t.strftime(DATE_FMT)
    already = rec.get("last_shake") == stamp
    rec["last_shake"] = stamp

    if topic_status(rec) in ("closed", "returned"):
        if already:
            return None
        rec["suspicion"] = rec.get("suspicion", 0) + 1
        if rec["suspicion"] >= SUSPICION_LIMIT:
            was_closed = rec["status"] == "closed"
            rec["status"] = "returned"
            rec["suspicion"] = 0
            void_rounds(rec)
            if was_closed:
                rec["reopened_on"] = stamp
            rec["closed_on"] = None
            rec["next_control"] = None
            rec["closed_at_difficulty"] = None
            return "тема {} переоткрыта ({})".format(tp, reason or "ошибка по теме")
        return "тема {} под подозрением ({}/{})".format(
            tp, rec["suspicion"], SUSPICION_LIMIT)

    if topic_status(rec) == "testing":
        rec["status"] = "in_progress"
        void_rounds(rec)
        return "тема {} снята с испытания, круги обнулены".format(tp)
    return None


def all_topics(data: Data) -> list[str]:
    """Все известные темы: из записей, из элементов и из ошибок."""
    tps = set(data["topics"])
    tps |= {it.get("topic", "") for it in data["items"].values()}
    tps |= {m.get("topic", "") for m in data["mistakes"].values()}
    return sorted(tp for tp in tps if tp)


def cmd_lesson(data: Data, args: argparse.Namespace) -> None:
    """Отметить занятие по теме. Двигает только паузу, ничего больше.

    Тема должна быть известна — та же защита от опечатки в номере, что и в `close`:
    занятие отмечается после `import`, поэтому заводить тему отсюда нечем и незачем.
    """
    if args.topic not in all_topics(data):
        print("темы {} в трекере нет — проверь номер (`tracker.py topics`). "
              "Если тема новая, сперва импортируй её лексику "
              "(`tracker.py import`).".format(args.topic), file=sys.stderr)
        sys.exit(1)
    rec = get_topic(data, args.topic, title=args.title)
    rec["last_lesson"] = today().strftime(DATE_FMT)
    print("OK: занятие по теме {} отмечено {}".format(args.topic, rec["last_lesson"]))


def cmd_topics(data: Data, args: argparse.Namespace) -> None:
    """Таблица состояний тем — статус словами, без звёздочек и процентов."""
    tps = all_topics(data)
    if args.topic:
        if args.topic not in tps:
            print("тема {} в трекере не заведена — импортируй её лексику "
                  "(tracker.py import)".format(args.topic))
            return
        tps = [args.topic]
    if not tps:
        print("тем в трекере нет")
        return
    print("{:<8} {:<14} {:<6} {:<9} что дальше".format(
        "тема", "статус", "ядро", "медиана"))
    for tp in tps:
        rec = get_topic(data, tp, create=False)
        lvl = topic_level(data, tp, rec)
        st = topic_status(rec)
        blockers = topic_blockers(data, tp, rec)
        if st == "closed":
            tail = "контроль {}".format(rec.get("next_control") or "—")
        else:
            shown = show_blockers(blockers)
            tail = shown[0] if shown else "готова к испытанию"
        print("{:<8} {:<14} {:<6} {:<9} {}".format(
            tp, TOPIC_STATUS_RU.get(st, st), lvl["core"], lvl["median"], tail))


def cmd_blockers(data: Data, args: argparse.Namespace) -> None:
    tp = args.topic
    rec = get_topic(data, tp, create=False)
    lvl = topic_level(data, tp, rec)
    print("Тема {} — {} (ядро {} эл., медиана mastery {}, худший {}, "
          "повторено {:.0%})".format(
              tp, TOPIC_STATUS_RU.get(topic_status(rec), topic_status(rec)),
              lvl["core"], lvl["median"], lvl["worst"], lvl["repeated_share"]))
    blockers = topic_blockers(data, tp, rec)
    if not blockers:
        print("Мешающего нет — тему можно вести на закрывающее испытание.")
        return
    print("Мешает закрыть:")
    for b in show_blockers(blockers):
        print("  • {}".format(b))
    hidden = len(blockers) - len(show_blockers(blockers))
    if hidden > 0:
        print("  (и ещё {} — покажу, когда снимешь эти)".format(hidden))


def cmd_close(data: Data, args: argparse.Namespace) -> None:
    """Фиксирует попытку закрытия. Ворота проверяются здесь, а не на глаз."""
    tp = args.topic
    # Закрывать можно только известную тему. Раньше опечатка в номере заводила новую
    # запись, и «9.9» навсегда оседала в `topics` со статусом «нет критерия» — снять
    # её можно было только правкой файла руками.
    if tp not in all_topics(data):
        print("темы {} в трекере нет — проверь номер (`tracker.py topics`). "
              "Если тема новая, сперва импортируй её лексику "
              "(`tracker.py import`).".format(tp), file=sys.stderr)
        sys.exit(1)
    rec = get_topic(data, tp, title=args.title)
    t = today()
    stamp = t.strftime(DATE_FMT)
    was_closed = topic_status(rec) == "closed"

    blockers = topic_blockers(data, tp, rec)
    hard = hard_blockers(blockers)
    # ворота, которые нельзя вычислить из данных — свойства самого испытания
    if not args.production:
        hard.append("не подтверждена доля продукции ≥70% (--production)")
    if not args.no_hints:
        hard.append("не подтверждено отсутствие подсказок (--no-hints)")
    if not args.calibrated:
        hard.append("самооценка не сошлась с результатом (--calibrated)")
    if args.result == "ok":
        if args.accuracy is None:
            hard.append("не указан результат испытания (--accuracy)")
        elif args.accuracy < CLOSE_MIN_ACCURACY:
            hard.append("результат {:.0%}, нужно не меньше {:.0%}".format(
                args.accuracy, CLOSE_MIN_ACCURACY))

    counted = args.result == "ok" and not hard
    attempt: Attempt = {
        "date": stamp, "result": str(args.result),
        "accuracy": args.accuracy, "counted": counted,
        "blocked_by": hard, "voided": False,
    }
    rec["attempts"].append(attempt)

    if args.result == "fail":
        # Провал контроля закрытой темы — это откат, а не «остаётся в работе».
        void_rounds(rec)
        if was_closed:
            rec["status"] = "returned"
            rec["reopened_on"] = stamp
            rec["closed_on"] = None
            rec["next_control"] = None
            rec["closed_at_difficulty"] = None
            rec["suspicion"] = 0
            print("Контроль по теме {} провален — тема вернулась в работу.".format(tp))
        else:
            rec["status"] = "in_progress"
            print("Попытка закрытия темы {}: провал. Тема остаётся в работе.".format(tp))
        print("Возврат идёт не на старт: собери отработку по паттерну, "
              "который её уронил (thai-mistakes).")
        return

    if hard:
        # Отклонённая попытка остаётся в истории, но статус не трогает: она не
        # событие в жизни темы, а неудачный запрос.
        print("Попытка закрытия темы {} не засчитана — ворота не пройдены:".format(tp))
        for b in hard[:BLOCKERS_SHOWN]:
            print("  • {}".format(b))
        return

    if was_closed:
        # Контроль пройден — следующий шаг лестницы 90 → 180 → 365.
        step = min(rec.get("control_step", 0) + 1, len(CONTROL_STEPS) - 1)
        rec["control_step"] = step
        rec["next_control"] = (t + timedelta(days=CONTROL_STEPS[step])).strftime(DATE_FMT)
        rec["suspicion"] = 0
        print("Контроль по теме {} пройден. Следующий — {}.".format(
            tp, rec["next_control"]))
        return

    days = counted_days(rec)
    if len(days) < CLOSE_ROUNDS:
        rec["status"] = "testing"
        print("Круг {} из {} по теме {} пройден. Второй — через интервал, "
              "не сегодня.".format(len(days), CLOSE_ROUNDS, tp))
        return

    rec["status"] = "closed"
    rec["closed_on"] = stamp
    rec["suspicion"] = 0
    rec["control_step"] = 0
    rec["closed_at_difficulty"] = data["meta"].get("difficulty", 4)
    rec["next_control"] = (t + timedelta(days=CONTROL_STEPS[0])).strftime(DATE_FMT)
    print("Тема {} закрыта. Из спирали уходит, лексика остаётся обязательным "
          "фоном в заданиях по другим темам.".format(tp))
    print("Контрольная проверка: {}.".format(rec["next_control"]))


# ---------- команды ----------

def closed_topics(data: Data) -> set[str]:
    """Темы, ушедшие из спирали: их элементы не выдаются как самостоятельный повтор."""
    return {tp for tp, rec in data["topics"].items()
            if topic_status(rec) == "closed"}


def cmd_due(data: Data, args: argparse.Namespace) -> None:
    t = today()
    closed = closed_topics(data)
    due_items: list[tuple[str, Item]] = []
    background: list[tuple[str, Item]] = []
    for key, it in data["items"].items():
        dd = parse_date(it.get("due_date", "1970-01-01"))
        if dd > t:
            continue
        if it.get("topic", "") in closed:
            # Закрытая тема не даёт собственных заданий, но её лексика обязана
            # появляться фоном в заданиях по другим темам.
            background.append((key, it))
        else:
            due_items.append((key, it))
    # приоритет: низкий mastery, затем ранняя due_date
    due_items.sort(key=lambda kv: (kv[1].get("mastery", 0),
                                   parse_date(kv[1].get("due_date", "1970-01-01"))))
    # Фон режется до BACKGROUND_LIMIT, поэтому его тоже надо упорядочить: иначе в
    # задание попадали первые попавшиеся по порядку словаря, а не самые слабые.
    background.sort(key=lambda kv: (kv[1].get("mastery", 0),
                                    parse_date(kv[1].get("due_date", "1970-01-01"))))

    due_mistakes: list[tuple[str, Mistake]] = []
    for key, m in data["mistakes"].items():
        if m.get("status", "active") not in ("active", "critical"):
            continue
        if parse_date(m.get("next_review", "1970-01-01")) <= t:
            due_mistakes.append((key, m))
    # критические (пережившие два круга отработки) — вперёд, затем по частоте
    due_mistakes.sort(key=lambda kv: (kv[1].get("status") != "critical",
                                      -kv[1].get("frequency", 0)))

    limit = args.limit
    out: dict[str, list[dict[str, Any]]] = {
        "mistakes_due": [
            {"pattern": k, "category": m.get("category", ""),
             "topic": m.get("topic", ""), "status": m.get("status", "active"),
             "mode": mode_for(m.get("category", ""), m.get("mode")),
             "frequency": m.get("frequency", 0)}
            for k, m in (due_mistakes[:limit] if limit else due_mistakes)
        ],
        "items_due": [
            {"item": k, "type": it.get("type", "word"),
             "topic": it.get("topic", ""), "mastery": it.get("mastery", 0),
             "translation": it.get("translation", "")}
            for k, it in (due_items[:limit] if limit else due_items)
        ],
        "background": [
            {"item": k, "type": it.get("type", "word"),
             "topic": it.get("topic", ""), "mastery": it.get("mastery", 0),
             "translation": it.get("translation", "")}
            for k, it in background[:BACKGROUND_LIMIT]
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_record(data: Data, args: argparse.Namespace) -> None:
    key = nfc(args.item)
    it = data["items"].get(key, new_item())
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

    # Серия обнуляется после сдвига уровня: иначе mastery рос бы на каждом верном
    # ответе начиная с третьего, и каждый следующий уровень доставался бы за один
    # ответ вместо новой серии.
    if cc >= MASTERY_UP_AFTER:
        mastery = min(5, mastery + 1)
        cc = 0
    elif ci >= MASTERY_DOWN_AFTER:
        mastery = max(0, mastery - 1)
        ci = 0

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
    if q < 3:
        note = topic_shake(data, it.get("topic", ""), f"ошибка в «{key}»")
        if note:
            print(note)


def cmd_mistake(data: Data, args: argparse.Namespace) -> None:
    key = args.pattern
    t = today()
    # Заготовка под новый паттерн: normalize_mistake заполняет её через setdefault,
    # поэтому словарь нужен свежий на каждый вызов.
    blank: dict[str, Any] = {}
    m = normalize_mistake(data["mistakes"].get(key, blank), args.category)
    if args.category:
        m["category"] = args.category
    if args.topic:
        m["topic"] = args.topic
    if args.mode:
        m["mode"] = args.mode
    if args.notes:
        m["notes"] = args.notes
    m["frequency"] = m.get("frequency", 0) + 1
    # повторная ошибка после успешного круга обнуляет зачёт отработки
    m["drill_ok"] = 0
    if m["status"] != "critical":
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
          f"режим {mode_for(m['category'], m['mode'])}, "
          f"следующий повтор {m['next_review']}")
    note = topic_shake(data, m.get("topic", ""), f"паттерн «{key}»")
    if note:
        print(note)


def cmd_resolve(data: Data, args: argparse.Namespace) -> None:
    key = args.pattern
    if key in data["mistakes"]:
        data["mistakes"][key]["status"] = "resolved"
        print(f"OK: паттерн «{key}» помечен resolved")
    else:
        print(f"нет такого паттерна: {key}", file=sys.stderr)


def mistake_view(key: str, m: Mistake) -> dict[str, Any]:
    """Компактное представление паттерна для JSON-выдачи."""
    return {
        "pattern": key,
        "category": m.get("category", ""),
        "topic": m.get("topic", ""),
        "mode": mode_for(m.get("category", ""), m.get("mode")),
        "status": m.get("status", "active"),
        "frequency": m.get("frequency", 0),
        "rounds": m.get("rounds", 0),
        "drill_ok": m.get("drill_ok", 0),
        "last_occurred": m.get("last_occurred", ""),
        "next_review": m.get("next_review", ""),
        "last_example": (m.get("examples") or [{}])[-1],
        "notes": m.get("notes", ""),
    }


def select_mistakes(data: Data, status: str | None = None, topic: str | None = None,
                    category: str | None = None,
                    due_only: bool = False) -> list[tuple[str, Mistake]]:
    t = today()
    out: list[tuple[str, Mistake]] = []
    for key, m in data["mistakes"].items():
        m = normalize_mistake(m)
        st = m.get("status", "active")
        if status:
            if status != st:
                continue
        elif st not in ("active", "critical"):
            continue
        if topic and m.get("topic", "") != topic:
            continue
        if category and category.lower() not in (m.get("category", "") or "").lower():
            continue
        if due_only and parse_date(m.get("next_review", "1970-01-01")) > t:
            continue
        out.append((key, m))
    # критические вперёд, затем частые, затем свежие
    out.sort(key=lambda kv: (kv[1].get("status") != "critical",
                             -kv[1].get("frequency", 0),
                             parse_date(kv[1].get("last_occurred", "1970-01-01"))))
    return out


def cmd_mistakes(data: Data, args: argparse.Namespace) -> None:
    sel = select_mistakes(data, status=args.status, topic=args.topic,
                          category=args.category, due_only=args.due)
    if args.limit:
        sel = sel[:args.limit]
    print(json.dumps([mistake_view(k, m) for k, m in sel],
                     ensure_ascii=False, indent=2))


def cmd_drill_plan(data: Data, args: argparse.Namespace) -> None:
    """План работы над ошибками: группировка по темам, режимы, объём заданий.

    Объём: 3 задания за первую ошибку темы + 1 за каждую следующую, потолок 10.
    Повторная ошибка (frequency >= 2) весит как две — старое тяжелее свежего.
    """
    sel = select_mistakes(data, topic=args.topic, category=args.category,
                          due_only=args.due)
    groups: dict[str, DrillGroup] = {}
    for key, m in sel:
        topic = m.get("topic", "")
        gid = topic or "cat:" + (m.get("category", "") or "—")
        g = groups.setdefault(gid, {"topic": topic, "mistakes": [], "modes": []})
        g["mistakes"].append(mistake_view(key, m))
        mode = mode_for(m.get("category", ""), m.get("mode"))
        if mode not in g["modes"]:
            g["modes"].append(mode)

    out: list[dict[str, Any]] = []
    for gid, g in groups.items():
        weight = sum(2 if mm["frequency"] >= 2 else 1 for mm in g["mistakes"])
        tasks = min(10, 3 + max(0, weight - 1))
        drill_modes = [md for md in g["modes"] if md != "reference"]
        entry: dict[str, Any] = {
            "group": gid,
            "topic": g["topic"],
            "modes": g["modes"],
            "mode_titles": [MODE_TITLES.get(md, md) for md in g["modes"]],
            "tasks": tasks if drill_modes else 0,
            "critical": any(mm["status"] == "critical" for mm in g["mistakes"]),
            "second_round": any(mm["rounds"] >= 1 for mm in g["mistakes"]),
            "mistakes": g["mistakes"],
        }
        if "vocab" in g["modes"] and g["topic"]:
            pool: list[VocabEntry] = [
                {"item": k, "translation": it.get("translation", ""),
                 "translit": it.get("translit", ""), "mastery": it.get("mastery", 0)}
                for k, it in data["items"].items()
                if it.get("topic", "") == g["topic"] and it.get("type", "word") == "word"
            ]
            pool.sort(key=lambda x: x["mastery"])
            entry["vocab_pool"] = pool
        out.append(entry)

    out.sort(key=lambda g: (not g["critical"], -g["tasks"]))
    print(json.dumps({"date": today().strftime(DATE_FMT), "groups": out},
                     ensure_ascii=False, indent=2))


def cmd_attempt(data: Data, args: argparse.Namespace) -> None:  # noqa: C901
    """Итог круга отработки: ok — ошибка снята в этом круге, fail — повторилась."""
    key = args.pattern
    if key not in data["mistakes"]:
        print(f"нет такого паттерна: {key}", file=sys.stderr)
        sys.exit(1)
    t = today()
    m = normalize_mistake(data["mistakes"][key])
    rounds_today = m.get("last_drill", "") == t.strftime(DATE_FMT)
    m["rounds"] = m.get("rounds", 0) + 1
    m["last_drill"] = t.strftime(DATE_FMT)

    if args.result == "ok":
        m["drill_ok"] = m.get("drill_ok", 0) + 1
        gap = DRILL_INTERVALS.get(m["drill_ok"], DRILL_INTERVAL_LONG)
        m["next_review"] = (t + timedelta(days=gap)).strftime(DATE_FMT)
        if m["drill_ok"] >= 2:
            m["status"] = "resolved"
            msg = (f"паттерн «{key}» закрыт (resolved): два чистых круга подряд. "
                   f"История сохранена.")
        else:
            m["status"] = "active"
            msg = (f"паттерн «{key}» — круг чистый ({m['drill_ok']}/2), "
                   f"контрольная проверка {m['next_review']}")
    else:
        m["drill_ok"] = 0
        m["frequency"] = m.get("frequency", 0) + 1
        m["last_occurred"] = t.strftime(DATE_FMT)
        if rounds_today:
            # два круга за занятие не помогли — дальше только в следующий раз
            m["status"] = "critical"
            m["next_review"] = (t + timedelta(days=1)).strftime(DATE_FMT)
            msg = (f"паттерн «{key}» — второй круг за занятие не снял ошибку. "
                   f"Статус critical, перегрев не лечит: следующий заход "
                   f"{m['next_review']}, первым в спирали.")
        else:
            m["next_review"] = t.strftime(DATE_FMT)
            msg = (f"паттерн «{key}» повторился (частота {m['frequency']}). "
                   f"Положен второй круг — с другой стороны и мельче шагом.")
    if args.context:
        m["examples"].append({
            "your_answer": args.your or "", "correct_answer": args.correct or "",
            "context": args.context, "date": t.strftime(DATE_FMT),
        })
    data["mistakes"][key] = m
    print("OK: " + msg)
    if args.result == "fail":
        note = topic_shake(data, m.get("topic", ""), f"провал круга по «{key}»")
        if note:
            print(note)


# Таблица словаря в glava-файлах. Колонок бывает больше трёх («| Тайский | Транскрипция |
# Значение | Часы |»), поэтому строку разбираем по разделителям, а не одной жадной
# регуляркой: жадная склеивала первые две колонки в один ключ.
ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
THAI_RE = re.compile(r"[\u0e00-\u0e7f]")
HEADER_WORDS = {"тайский", "транскрипция", "перевод", "term", ""}


# Критерий закрытия ищем в двух местах, в этом порядке. Первый — явная секция для
# новых тем; второй — «Резюме по теме», которое во всех 36 написанных файлах уже
# заканчивается списком «К концу темы ты должна уметь». Отдельно сочинять критерий
# не надо: он давно написан, просто под другим заголовком.
EXIT_HEADING = "Тема закрыта, если ты можешь"
EXIT_HEADING_FALLBACK = "Резюме по теме"
# Пункт секции: нумерованный или маркированный список.
EXIT_ITEM_RE = re.compile(r"^(?:[-*+]|\d+[.)])\s+")
# Декор в начале пункта резюме: галочки, маркеры, лишние пробелы.
EXIT_DECOR_RE = re.compile(r"^[\s✅✔☑•▪–—-]+")


def read_exit_task(path: str) -> str:
    """Критерий закрытия темы из её файла.

    Берём только пункты списка под markdown-заголовком: таблицы, комментарии и прочий
    текст в критерий не попадают, иначе им открывались бы ворота. Явная секция
    «Тема закрыта, если ты можешь» имеет приоритет; если её нет — «Резюме по теме»,
    где список «К концу темы ты должна уметь» и есть готовый критерий.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print("не удалось прочитать {}: {}".format(path, e), file=sys.stderr)
        return ""
    except UnicodeDecodeError:
        print("файл {} не в UTF-8 — секция критерия не прочитана".format(path),
              file=sys.stderr)
        return ""

    found: dict[str, list[str]] = {EXIT_HEADING: [], EXIT_HEADING_FALLBACK: []}
    grab: str | None = None
    fenced = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if stripped.startswith("#"):
            low = stripped.lower()
            grab = None
            for heading in found:
                if heading.lower() in low:
                    grab = heading
            continue
        if grab and EXIT_ITEM_RE.match(stripped):
            item = EXIT_DECOR_RE.sub("", EXIT_ITEM_RE.sub("", stripped)).strip()
            if item:
                found[grab].append(item)
    items = found[EXIT_HEADING] or found[EXIT_HEADING_FALLBACK]
    return " · ".join(items).strip()


def clean_cell(s: str) -> str:
    s = s.strip()
    s = s.replace("**", "").strip()
    return s


def cmd_import(data: Data, args: argparse.Namespace) -> None:
    if not os.path.exists(args.source):
        print(f"файл не найден: {args.source}", file=sys.stderr)
        sys.exit(1)
    added, skipped = 0, 0
    with open(args.source, "r", encoding="utf-8") as f:
        for line in f:
            mm = ROW_RE.match(line)
            if not mm:
                continue
            cells = [clean_cell(c) for c in mm.group(1).split("|")]
            if len(cells) < 3:
                continue
            # Тайское слово не всегда в первой колонке: бывает «| Час | Тайский |
            # Транскрипция | Смысл |». Ищем колонку с тайским, остальное — вокруг неё.
            idx = next((i for i, c in enumerate(cells) if THAI_RE.search(c)), None)
            if idx is None:
                continue
            thai = cells[idx]
            nxt = cells[idx + 1] if idx + 1 < len(cells) else ""
            translit = "" if THAI_RE.search(nxt) else nxt
            rest = [c for i, c in enumerate(cells)
                    if c and i != idx and (not translit or c != translit)]
            translation = " · ".join(rest)
            # пропустить заголовки и разделители таблиц
            if thai.lower() in HEADER_WORDS or set(thai) <= set("-: "):
                continue
            thai = nfc(thai)
            if thai in data["items"]:
                skipped += 1
                continue
            it = new_item()
            it.update({
                "translation": translation, "translit": translit, "type": "word",
                "topic": args.topic or "",
                "due_date": today().strftime(DATE_FMT),  # сразу due
                "last_seen": "1970-01-01",
            })
            data["items"][thai] = it
            added += 1
    print(f"Импорт из {os.path.basename(args.source)}: добавлено {added}, "
          f"пропущено (уже были) {skipped}")

    if not args.topic:
        return
    rec = get_topic(data, args.topic)
    exit_task = read_exit_task(args.source)
    if exit_task:
        rec["exit_task"] = exit_task
        if rec["status"] == "no_criterion":
            rec["status"] = "in_progress"
    elif not rec["exit_task"] and rec["status"] == "in_progress" and not rec["attempts"]:
        rec["status"] = "no_criterion"
        print(f"Тема {args.topic}: в файле нет секции «{EXIT_HEADING}» — "
              f"статус «нет критерия», закрыть её нельзя.")


def stars(m: int) -> str:
    return "⭐" * m + "☆" * (5 - m)


def cmd_progress(data: Data, args: argparse.Namespace) -> None:
    meta = data["meta"]
    t = today()
    items = data["items"]
    # средний mastery по темам
    by_topic: dict[str, list[int]] = {}
    for it in items.values():
        tp = it.get("topic", "") or "—"
        by_topic.setdefault(tp, []).append(it.get("mastery", 0))
    due_count = sum(1 for it in items.values()
                    if parse_date(it.get("due_date", "1970-01-01")) <= t)
    active_mistakes = [(k, m) for k, m in data["mistakes"].items()
                       if m.get("status", "active") in ("active", "critical")]

    print(f"Прогресс — тайский · сложность {meta.get('difficulty', 4)} · "
          f"точность (новое): {int(meta.get('recent_accuracy', 0) * 100)}%")
    print(f"Слов/правил в трекере: {len(items)}\n")
    print("Темы (медиана mastery по ядру):")
    for tp in sorted(by_topic):
        rec = get_topic(data, tp, create=False)
        lvl = topic_level(data, tp, rec)
        med = int(lvl["median"])
        print(f"  {tp:<10} {stars(med)}  ({lvl['median']}/5 по ядру из {lvl['core']}, "
              f"{len(by_topic[tp])} эл.) — "
              f"{TOPIC_STATUS_RU.get(topic_status(rec), topic_status(rec))}")
    closed = [tp for tp, r in data["topics"].items() if r.get("status") == "closed"]
    if closed:
        print("Закрыто: " + ", ".join(sorted(closed)))
    print(f"\nПора повторить (due): {due_count}")
    if active_mistakes:
        print("Активные слабые места:")
        for k, m in sorted(active_mistakes,
                           key=lambda kv: (kv[1].get("status") != "critical",
                                           -kv[1].get("frequency", 0))):
            mark = " ‼️ critical" if m.get("status") == "critical" else ""
            print(f"  • {m.get('category','')}: {k} — {m.get('frequency',0)}×{mark}")


def cmd_set_meta(data: Data, args: argparse.Namespace) -> None:
    if args.difficulty is not None:
        data["meta"]["difficulty"] = args.difficulty
    if args.recent_accuracy is not None:
        data["meta"]["recent_accuracy"] = args.recent_accuracy
    print(f"OK: meta обновлена → {json.dumps(data['meta'], ensure_ascii=False)}")


def add_cmd(sub: Any, name: str, handler: Callable[[Data, argparse.Namespace], None],
            writes: bool, descr: str) -> argparse.ArgumentParser:
    """Зарегистрировать команду вместе с обработчиком и признаком записи.

    `sub` объявлен как Any намеренно: точный тип — `argparse._SubParsersAction`,
    приватный, публичного псевдонима argparse не даёт.

    «Меняет ли команда файл» — свойство самой команды, поэтому объявляется здесь,
    рядом с ней. Раньше это жило отдельным множеством имён в конце main, параллельно
    таблице обработчиков: два перечисления одних и тех же строк рассыхаются молча —
    новая пишущая команда, забытая во втором списке, просто не сохранила бы результат.

    Первым позиционным аргументом у всех команд идёт путь к трекеру — он тоже здесь.
    """
    sp = sub.add_parser(name, help=descr)
    sp.add_argument("path")
    sp.set_defaults(func=handler, writes=writes)
    return sp


def main() -> None:
    p = argparse.ArgumentParser(description="Трекер прогресса thai-tasks (SM-2 + ошибки)")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = add_cmd(sub, "due", cmd_due, False, "что пора повторить")
    d.add_argument("--limit", type=int, default=None)

    r = add_cmd(sub, "record", cmd_record, True, "SM-2 по качеству ответа 0–5")
    r.add_argument("item")
    r.add_argument("quality", type=int, choices=range(0, 6))
    r.add_argument("--type", choices=["word", "rule", "construction"])
    r.add_argument("--topic")
    r.add_argument("--translation")

    m = add_cmd(sub, "mistake", cmd_mistake, True, "записать паттерн ошибки")
    m.add_argument("pattern")
    m.add_argument("--category")
    m.add_argument("--topic", help="тема ошибки (например 6.1.2) — по ней собирается дрилл")
    m.add_argument("--mode", choices=sorted(MODE_TITLES), help="режим отработки вручную")
    m.add_argument("--your")
    m.add_argument("--correct")
    m.add_argument("--context")
    m.add_argument("--notes")

    ms = add_cmd(sub, "mistakes", cmd_mistakes, False, "список паттернов ошибок (JSON)")
    ms.add_argument("--topic")
    ms.add_argument("--category")
    ms.add_argument("--status", choices=["active", "critical", "resolved"])
    ms.add_argument("--due", action="store_true", help="только те, что пора повторить")
    ms.add_argument("--limit", type=int, default=None)

    dp = add_cmd(sub, "drill-plan", cmd_drill_plan, False,
                 "план работы над ошибками (JSON)")
    dp.add_argument("--topic")
    dp.add_argument("--category")
    dp.add_argument("--due", action="store_true")

    at = add_cmd(sub, "attempt", cmd_attempt, True, "итог круга отработки ошибки")
    at.add_argument("pattern")
    at.add_argument("--result", choices=["ok", "fail"], required=True)
    at.add_argument("--your")
    at.add_argument("--correct")
    at.add_argument("--context")

    rv = add_cmd(sub, "resolve", cmd_resolve, True, "закрыть паттерн ошибки")
    rv.add_argument("pattern")

    im = add_cmd(sub, "import", cmd_import, True, "импорт словаря из glava-файла")
    im.add_argument("source")
    im.add_argument("--topic")

    add_cmd(sub, "progress", cmd_progress, False, "обзор прогресса")

    sm = add_cmd(sub, "set-meta", cmd_set_meta, True, "обновить meta")
    sm.add_argument("--difficulty", type=int)
    sm.add_argument("--recent-accuracy", type=float, dest="recent_accuracy")

    ls = add_cmd(sub, "lesson", cmd_lesson, True,
                 "отметить занятие по теме (двигает паузу)")
    ls.add_argument("topic")
    ls.add_argument("--title")

    tp = add_cmd(sub, "topics", cmd_topics, False, "состояния тем")
    tp.add_argument("--topic")

    bl = add_cmd(sub, "blockers", cmd_blockers, False, "что мешает закрыть тему")
    bl.add_argument("topic")

    cl = add_cmd(sub, "close", cmd_close, True, "попытка закрытия темы")
    cl.add_argument("topic")
    cl.add_argument("--result", choices=["ok", "fail"], required=True)
    cl.add_argument("--accuracy", type=float, default=None,
                    help="доля верного 0..1; при --result ok обязателен")
    cl.add_argument("--title")
    cl.add_argument("--production", action="store_true",
                    help="не меньше 70%% заданий листа продуктивные (рус→тай, сборка)")
    cl.add_argument("--no-hints", action="store_true", dest="no_hints",
                    help="подсказок не было")
    cl.add_argument("--calibrated", action="store_true",
                    help="прогноз ученицы разошёлся с фактом не больше чем на 1 пункт")

    args = p.parse_args()
    data, merged = load(args.path)
    if merged:
        print("нормализовано ключей (NFC): {}".format(", ".join(merged)), file=sys.stderr)

    args.func(data, args)

    # Пишет только та команда, которая объявила себя пишущей. Слияние ключей NFC сюда
    # не добавляется намеренно: иначе `due` — первая команда занятия — переписывала бы
    # трекер и затирала `.bak`, ту самую «последнюю целую копию», на которую ссылается
    # сообщение об ошибке в `load`.
    if args.writes:
        save(args.path, data)


if __name__ == "__main__":
    main()
