# Checking answers

How to review the user's answers. Sits on top of the rules in `thai-learning` (practice vs
test, annotating unknown words) — this file details the review itself.

**Everything the user reads stays in Russian**, including the templates quoted below. The
four category names are also data: they are written into `progress.json` as `category`, so
they must appear exactly as spelled here.

## Tone notation

The user marks tones like this, over the vowel of the syllable:

| Тон | Знак |
|---|---|
| Средний (สามัญ) | *без знака* |
| Низкий (เอก) | ` |
| Нисходящий (โท) | ˆ |
| Высокий (ตรี) | ´ |
| Восходящий (จัตวา) | ˇ |

Use **exactly this scheme** when giving transcription and when reviewing tones. Never mark
the mid tone.

## Verify tones against an authoritative source only

Your own knowledge of a word's tone is **not sufficient**. Before judging a tone in the
user's answer right or wrong, check an authoritative source — first of all the dictionary
at http://thai-language.com/dict/search. This applies to every tone judgement, in practice
and in tests alike. Never rule from memory: tones are easy to confuse, and a wrong verdict
undermines trust in the whole review.

## Order of review: hints first, answer second

The review runs in two steps (the rule comes from `thai-learning`; the order here is
mandatory).

**Step 1 — hints.** Do not hand over the correct version straight away. For each mistake,
name *what* is wrong and steer with a leading question or a reminder of the rule, without
revealing the answer.

> Пример: «В слове для "рис" тон не средний. Посмотри на класс первой согласной и на
> тоновый знак — какой тон они дают в закрытом слоге?»

Let the user try to fix it from the hint.

**Step 2 — the correct version with an explanation.** If the hints did not work (the
mistake repeats, or the user asks), give the correct version and unpack it:

- **what exactly** was wrong in the user's answer;
- **why it is otherwise** — which rule applies and how it produces the right form.

> Пример: «Правильно кхâау (нисходящий). У тебя был средний. ข — высокий класс, знак
> ้ (ไม้โท) на высоком классе в этом слоге даёт нисходящий тон, а не средний.»

In **tests** there are no hints (see thai-learning): verdict and review straight away.

## Scoring by category

Score a productive answer not with one mark but **across four categories** — that shows
where the gap actually is, and it feeds the progress file.

| Категория | Что проверяем |
|---|---|
| **Словарный запас** | правильно ли выбраны слова, подходят ли по смыслу и ситуации |
| **Грамматика** | порядок слов (SVO), частицы, конструкции, счётные слова, маркеры времени |
| **Орфография** | верное тайское написание: согласные, гласные, знаки, пробелы/их отсутствие |
| **Тоны** | верные тоны (сверять по авторитетному источнику, см. выше) |

Output format for reviewing a productive task:

```
Разбор задания N

Твой ответ: [что прислал пользователь]

📖 Словарный запас: [верно / замечание]
🧩 Грамматика: [верно / замечание]
✍️ Орфография: [верно / замечание]
🎵 Тоны: [верно / замечание — со сверкой по источнику]

[Если есть ошибки → сначала подсказки по шагу 1; при необходимости → правильный
вариант с объяснением по шагу 2.]

Итог: [краткий вывод + одно правило-закрепление]
```

For atomic single-skill tasks the full four-category table is overkill — score the relevant
category only, but the order «подсказка → ответ с объяснением» always holds.

## The naturalness lens (beyond correctness)

The four categories check whether the answer is **correct**. But a productive answer can be
grammatically right and still not sound Thai — a calque, bookish phrasing, the wrong
register. So for productive tasks (conversational ones especially) add a separate line:

```
🗣 Естественнее: «{как сказал бы носитель}» — {почему живее/уместнее}
```

Important: this is **not a mistake** and does not lower any of the four category scores —
correct stays correct. It is a pointer on how to sound like a native rather than like a
textbook. Give it when there is something to improve; if the answer already sounds natural,
say so («звучит натурально»). Idiomaticity and register are a B1 skill from the mission, so
the lens matters.

## Feeding the tracker

After the review, update `progress.json` by the rules in
**references/progress-and-spiral.md**:

- for every element involved — rate the answer 0–5 and apply **SM-2** (updating
  repetitions, interval, easiness_factor, mastery);
- record every mistake in the **pattern database** (`mistakes`): the category is one of the
  four above, `--topic` is the topic the mistake belongs to (mandatory — without it the
  mistakes workflow cannot assemble a block for that topic), plus an example «твой ответ →
  правильный». This is where the spiral (get_due) picks weak spots from, with priority.

## Next — the mistakes workflow

Reviewing answers ends by handing over to skill **thai-mistakes**: a report on the whole
sheet (✅ / 🟡 / ❌ + the correct version + a one-line «почему», a summary and a breakdown by
category), then a mini-diagnostic of the topic and a drill block matched to the mistake
type. The two-round rule, the drill modes and the report format live there.

The checking categories (Словарный запас / Грамматика / Орфография / Тоны) are the same
values as `category` in the mistake database — keep them in step.
