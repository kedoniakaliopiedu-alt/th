---
name: thai-learning
description: >
  General rules for presenting and checking Thai learning tasks. Use for requests such
  as «дай задание», «сделай контрольную», «проверь мои ответы» and «дай подсказку» about
  alphabet, tones, pronunciation, vocabulary or grammar. Use it together with thai-tasks
  to assemble a set; after a completed sheet is checked, thai-mistakes owns the full
  report and remediation. For a simple single-word translation, answer directly instead.
---

# Thai Learning Skill

This skill defines how Codex presents Thai tasks and checks answers in project Thailand.
It owns general pedagogy; `thai-tasks` assembles complete sheets and `thai-mistakes`
produces the full graded report after answers are checked.

## Always start here

1. Identify whether this is practice or a control: practice permits a hint before the
   answer, while a control does not.
2. Read `thai-tasks/references/checking.md` before checking any learner answer. It owns
   categories, naturalness, conversational variants and tracker hand-off.
3. For a written or chapter control, read
   `thai-tasks/references/written-control.md` before authoring it. It owns coverage,
   scoring units and the saved HTML format.
4. Verify every tone through `thai-verify`; memory is never enough for a tone verdict.

## General principles

- Everything the learner reads is in **Russian**.
- Pronunciation transcription is **Cyrillic only**, following `thai-phonetics`. English may
  accompany it only while studying the alphabet itself at Level 1.
- Tone marks sit over the stressed vowel: mid has no mark; `` ` `` low; `ˆ` falling; `´`
  high; `ˇ` rising.
- Multisyllabic transcription uses hyphens: **ма-лай**, **са-ва-дии**.
- Vocabulary format is **тайский → кириллическая транскрипция — русский перевод**.
- Thai script is mandatory; Latin transliteration never replaces it.
- The tone is friendly and pressure-free. Learning should feel exploratory.
- A natural conversational form receives full credit when it is grammatical, preserves
  the required meaning and fits the situation. Do not penalize it merely because a
  textbook, neutral or formal alternative exists. Register lowers the score only when the
  task explicitly requires another register or the chosen form is inappropriate to the
  stated interlocutor and situation.

→ Sound system and transcription: see **thai-phonetics**.

→ Tone verification: see **thai-verify** before every tone verdict.

## Level structure

Tasks progress gradually. Move to the next level only after the current one is stable.
These levels organize teaching; they do **not** determine a task's point value in a control.

### Level 1 — writing and reading foundations

- 44 consonants and their classes;
- short and long vowels;
- final consonants;
- special signs such as ไม้ไต่คู้ and ไม้หันอากาศ.

### Level 2 — tones and pronunciation

- the five tones;
- consonant class, tone mark and syllable type;
- open and closed syllables;
- vowel length and its effect on tone.

### Level 3 — words and reading

- basic vocabulary such as greetings, numbers, colours, food and family;
- reading simple syllables and words without spaces;
- words from lakorns, songs and everyday phrases.

### Level 4 — grammar and phrases

- SVO sentence order without inflection;
- politeness particles such as ครับ and ค่ะ;
- questions with ไหม, หรือเปล่า, อะไร and ที่ไหน;
- time markers such as แล้ว, จะ and กำลัง;
- classifiers.

## Task formats

Use contextual and structured tasks in roughly equal measure.

### Contextual tasks

Base them on real material: lines from lakorns or songs, social posts and ordinary scenes.

> Вот фраза из лакорна: **ฉันรักเธอ**
>
> Что здесь написано? Попробуй прочитать и перевести.

### Structured tasks

Use familiar forms such as fill the gap, translate, match and choose the correct tone.

> Какой тон у слова **ข้าว**?
>
> (а) средний  (б) низкий  (в) нисходящий  (г) восходящий

## Handling mistakes in practice

These steps apply to **practice only**, never to a control.

1. After an incorrect answer, do not reveal the correct answer immediately.
2. Give one hint: remind the rule, identify what to recheck, or ask a leading question.
3. If the second answer is still wrong, give the full correct answer and explanation.
4. Finish with the rule in one sentence.

> Почти! Посмотри на класс первой согласной — она высокого класса. Как это влияет на тон
> в закрытом слоге с краткой гласной?

## Controls

### Principles

- A mini-control follows a small block; a final control follows the main block.
- Hints are unavailable and answers cannot be retried before grading.
- Check every answer and report a percentage after completion.
- Every error receives an explanation through the `thai-mistakes` workflow.
- Set each task's exact maximum score from its visible assessed components before delivery.
  A word, separate sentence, required contrast, communicative move or explicit content
  requirement may be one component. Difficulty labels never set the score.
- Award partial credit for completed components. A local spelling or particle error affects
  only the component it belongs to; it does not automatically halve the entire task.

### Passing thresholds

| Type | Threshold |
|---|---:|
| Мини-контроль | **80%** |
| Итоговый контроль | **90%** |

### If the control is not passed

1. Say clearly: «Тест не сдан — X%. Порог: Y%.»
2. Identify the concrete gaps.
3. Give targeted practice for those gaps.
4. Run a new control on the same material.
5. Repeat until the threshold is reached; do not move to the next block first.

### Learner-facing structure

```text
🔒 КОНТРОЛЬНАЯ РАБОТА — [название блока]
Заданий: N | Баллов: M | Подсказки: недоступны | Порог: X%

Задание 1. [текст] — [стоимость] балл(а/ов)
Задание 2. [текст] — [стоимость] балл(а/ов)
```

After all answers:

```text
📊 РЕЗУЛЬТАТ: X / M баллов — XX%
Статус: СДАН ✓ / НЕ СДАН ✗

РАЗБОР ОШИБОК:
— Задание N: твой ответ / правильный ответ
  Баллы: выполненные компоненты / полная стоимость
  Правило: [объяснение]
```

The full report format and weighted calculation live in
`thai-mistakes/references/report-format.md`; read it whenever grading a completed sheet.

## One practice task

```text
[Тема задания]
[Тайский текст — всегда крупно и чётко]
[Задание на русском]
[Место для ответа пользователя]
```

After the answer:

```text
[Оценка: верно / почти / неверно]
[Подсказка ИЛИ объяснение]
[Правило — одно предложение-закрепление]
```

## Unfamiliar words and constructions

If a task contains a word or construction that has not been taught in the current or an
older block, add a short note immediately after it. This applies to practice and controls;
the note gives reference information without revealing the tested answer.

> ⚑ **[слово/конструкция]** — [краткое объяснение на русском]
> *[кириллическая транскрипция]*

Example:

> Прочитай и переведи: **กำลังกิน**
>
> ⚑ **กำลัง** — маркер действия в процессе («сейчас делает») *гам-ланг*

## Additional rules

- Give one task at a time unless the user asks for a set.
- Follow a topic proposed by the user immediately without unnecessary questions.
- Use lakorns and songs as motivating context when they fit the learning goal.
- Treat recognition from a real context as evidence of learning without turning it into
  praise theatre.

## Checklist

1. The mode is clear: practice with hints or control without hints.
2. All learner-facing text is Russian and transcription is Cyrillic.
3. Tones were verified through `thai-verify` before any verdict.
4. Natural conversational Thai was accepted unless the task explicitly tested register.
5. A control shows exact content-based points; difficulty labels do not set weight.
6. Partial credit follows completed components rather than a fixed half-score.
7. Checked answers hand off to `thai-mistakes` for the complete report and remediation.
