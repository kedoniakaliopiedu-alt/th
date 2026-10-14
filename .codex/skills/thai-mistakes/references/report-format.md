# Graded report format

Load this file after checking any worksheet, control or test. The report reproduces the
entire original sheet with literal learner answers, verdicts, corrections and weighted
scores, so it can be read without the original submission.

Everything quoted as learner-facing output remains in Russian.

## Rules

1. **Repeat the full sheet.** Keep the original numbering, section headings and subitem
   letters. Do not shorten or rephrase the tasks; otherwise the report cannot be checked
   against the work that was actually completed.

2. **Mark every assessed item.** A subitem such as 7a or 7b receives its own verdict.

   | Marker | Meaning |
   |---|---|
   | ✅ | all assessed components are correct |
   | 🟡 | at least one component is correct and at least one needs correction |
   | ❌ | no assessed component is correct, or the answer is missing |

3. **Show the answer and correction.** For ✅, show the learner's literal answer. For 🟡
   and ❌, also show `→ **Верно:** …` and one concise `Почему` line.

   Every 🟡 or ❌ item must include the full correct answer in the requested format. This
   includes `?`, `не знаю` and blank answers. If the correct answer is not yet verified,
   mark the item `сверяю` and return after checking; never issue an unsupported verdict.

4. **Verify tones.** A tone verdict requires the `thai-verify` protocol and
   thai-language.com. Memory is not evidence.

5. **Use content-based points.** The maximum score is declared before delivery and comes
   from visible assessed components, not from the difficulty label or the number of the
   task. Use these units:

   - one recalled word, number or independent choice: normally 1 point;
   - each separately required sentence or communicative move: normally 1 point;
   - each required explanation, contrast or justification: normally 1 point;
   - each explicit requirement in connected writing: normally 1 point;
   - a dense sentence may contain several points only when those components are named in
     the task or its predeclared rubric.

   Difficulty labels describe the kind of thinking and never set the score. A short task
   may cost more than a long-looking one when it tests more independent content, and a
   difficult integrated sentence may remain one point when it has only one assessed target.

6. **Calculate partial credit from completed components.** Do not convert markers through
   a fixed formula such as `✅ = 1, 🟡 = 0.5, ❌ = 0`. Add the points earned for the actual
   components. A local spelling, particle or word-order error affects only its component;
   it does not automatically halve the whole task. Fractions such as 0.5 are allowed for a
   component whose meaning is present but whose form has one local defect.

   Show `earned / maximum` beside every task. The denominator is the sum of all declared
   task maxima, and the percentage is `earned ÷ maximum`, rounded to the nearest whole
   percent.

7. **Accept valid conversational Thai.** A grammatical, semantically appropriate and
   natural conversational form receives full credit even when a textbook gives a more
   neutral or formal alternative. Register lowers the score only when the task explicitly
   requests a different register or the answer is inappropriate to the stated situation.
   Present a neutral alternative as `Также возможно`, never as a correction.

8. **Include the breakdown.** Report the four categories `Словарный запас`, `Грамматика`,
   `Орфография`, `Тоны`, plus any genuinely relevant extra category such as register. Add
   `В работу` with the topics selected for remediation.

   If calibration was collected, put `Калибровка` immediately after the total. Mark a
   guessed answer with **(?)** and a confident error with **(!)**. A guess does not change
   points, but its tracker quality is 3 instead of 5.

9. **Use Cyrillic transcription.** Tone marks sit over the vowel, following
   `thai-phonetics`.

10. **Hide internal mechanics.** Never expose `frequency`, `mastery`, tracker mode names or
    internal difficulty numbers.

## Template

```markdown
📋 **ОТЧЁТ — Глава 3, срез · 2026-07-27**

**Разминка**

1. Прочитай слова и запиши транскрипцию кириллицей: ตื่น, ลุก, อาบน้ำ
   **Стоимость: 3 балла**
   ✅ **3 / 3 · Твой ответ:** ты̀н, лу́к, а̀п-наа́м

2. Какое обращение подойдёт?
   - а) к пожилой продавщице на рынке
     ❌ **0 / 1 · (!) Твой ответ:** คุณ → **Верно:** ป้า
     *Почему: คุณ — нейтральное обращение; в заданной рыночной ситуации ожидалось ป้า.*
   - б) к официанту моложе тебя
     ✅ **1 / 1 · (?) Твой ответ:** น้อง

**Сборка**

3. Напиши по-тайски две реплики: вопрос о цене и согласие продавца.
   **Стоимость: 2 балла — по одному за каждую реплику.**
   🟡 **1,5 / 2 · Твой ответ:** ตัวนี้เท่าไหร่คะ; ได้สิค่ะ
   → **Верно:** ตัวนี้เท่าไหร่คะ; ได้สิคะ
   *Почему: разговорное ได้สิ подходит; снято 0,5 только за написание конечной частицы.*

**Итог: 5,5 / 7 · 79%**

**Калибровка:** ты ожидала 6 из 7 — оценка близкая. Пункт 2а ты считала надёжным, но
он неверный; пункт 2б был угадан и вернётся раньше.

| Категория | Баллы | Где просело |
|---|---:|---|
| 📖 Словарный запас | 1/2 | обращение к старшей продавщице |
| 🧩 Грамматика | 2/2 | — |
| ✍️ Орфография | 2,5/3 | написание สิคะ |
| 🎵 Тоны | не оценивались | — |

**В работу:** обращения по ситуации; написание สิคะ.
```

## A report with no errors

Keep the full sheet and summary. Do not invent a mistake to justify remediation.

```markdown
**Итог: 18 / 18 · 100%** — ошибок нет, отрабатывать нечего.

Что дальше: следующий шаг по программе — [тема].
```

A clean sheet with guessed answers remains 100%, but guessed items receive tracker quality
3 and return sooner. Do not create a mistake record or raise difficulty from such a sheet.

## Second-round report

Use a distinct heading:

```markdown
📋 **ОТЧЁТ — работа над ошибками, круг 2 · тема 2.1**
```

For every previous error, add `снята` or `повторилась`; that result feeds
`attempt --result ok|fail`.

## Correcting an issued report

Any correction requires a complete replacement report. Partial patches force the learner
to maintain a mental diff and leave totals, categories and tracker entries inconsistent.

When the learner says `ты неверно понял`, `я написала другое` or disputes a verdict:

1. **Recheck the source.** For handwriting, return to a close crop through
   `thai-handwriting`; verify project transcription in `thai-phonetics/references/*` and
   tones through the authoritative source.
2. **Recalculate every dependency.** Update the verdict, correct answer, explanation,
   earned points, maximum if the rubric itself was wrong, total, percentage, category
   breakdown, calibration, remediation list and tracker entries.
3. **Resend the entire report from the top.** Never send only the changed item or say the
   rest is unchanged.
4. Precede it with one Russian sentence naming what was reconsidered and why.

This applies on every correction round and to worksheets, controls, remediation sheets and
word lists.

## Literal answers and project references

Show the learner's literal answer for every item, including `?` and blank markers. Before
marking spelling or transcription wrong, check `thai-phonetics/references/*`; project
choices such as ก → «г» deliberately differ from generic outside charts.
