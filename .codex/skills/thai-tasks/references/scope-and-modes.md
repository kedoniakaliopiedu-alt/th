# Request scope and output modes

Read when assembling a sheet: this file sets the volume for each request size and selects
one of three modes. Task types live in `exercise-catalog.md`; general presentation lives in
`output-format.md`. Chapter control tests and explicitly written controls additionally load
`written-control.md`, whose file delivery and layout override the generic worksheet format.
Instructions are English; learner-facing examples and literals remain Russian.

## Request scope: rule → subtopic → topic → chapter

Thailand material is hierarchical. Identify the requested scope before selecting volume;
ask one question only if neither the request nor context resolves it.

The source structure is `Глава` → `Тема N.M` → `Подтема N.M.K`, containing
«Словарный запас», «Теория/конструкции» and «Практические упражнения». Files are under
`Thai A2/Chapter N/glavaN_temaM_*.md`, `Thai B1/Chapter N/b1_glavaN_temaM_*.md`, with
supporting references in `Helpers/*.md`. Search recursively using `**/*glava*tema*.md`.
Take vocabulary and rules, but generate fresh examples rather than copying the source's
«Практические упражнения» verbatim.

**One rule / construction** — one technique within a subtopic, such as classifiers
จาน/ที่, dish + ingredient, degrees of spiciness, กำลัง or questions with ไหม.
Give **at most 5 tasks**: warm-up and assembly, without a final composite task. Exercise
the rule from different angles, with at least one productive Russian → Thai task.

**Subtopic**, e.g. 6.1.2 «Заказ в ресторане» — vocabulary plus several constructions.
Use warm-up → assembly → composite. Give 1–2 warm-up/assembly tasks per construction,
then 1–2 composite tasks; this normally yields 6–10 tasks.

**Topic**, e.g. 6.1 «Еда и рестораны» — a group of subtopics.
For ordinary practice, expand each subtopic as above and finish with one task combining
subtopics. If not already specified, establish whether to cover the topic at once or in
separate sessions. An explicit control-test request selects C without this practice choice.

**Chapter**, e.g. Chapter 6 — a group of topics.
For an unspecified practice request, offer a topic-by-topic plan or a chapter control test.
For «контрольная по главе», assemble the requested complete test immediately using
`written-control.md`; do not replace the deliverable with a plan or ask the settled choice
again. Its full-chapter default is 25–35 top-level tasks, subject to source sufficiency.

All scopes prioritise production. The 60/40 spiral applies to practice modes A/B; mode C
uses coverage of the requested scope instead.

## Mode A — live session, one task at a time

Default for dialogue practice and conversational Thai. Follow `thai-learning`:
one task → user answer → feedback → next task adapted to that answer. Keep `learn`'s
rhythm: one step per turn, hints before answers, support when stuck, and its handling of
«просто скажи». Production and spiral still apply, distributed across the session.

## Mode B — worksheet, the whole set at once

This is the default for «комплексное задание» when no other mode is specified. Give a
connected set with one narrative thread and increasing difficulty. Scope determines volume
and blocks: a rule gets warm-up + assembly; a subtopic/topic gets all three.

Use real Markdown, not ASCII frames; presentation details are in `output-format.md`:

```markdown
🎯 **КОМПЛЕКС — [тема] · уровень [N] · [N заданий]**

**Сквозная нить:** [короткий сюжет]
**Новое:** [что вводим] · **Повтор:** [что подмешиваем]

**Блок A (Разминка)**

1. [задание]
2. [задание]
   - [пример/подпункт — отдельным пунктом списка, не в строку]
   - [ещё пункт]

**Блок B (Сборка)**

1. [задание]
2. [задание]

**Блок C (Комплексное)**

1. [задание — продуктивное, с реальной целью]
2. [перевод небольшого текста/диалога рус→тай]

📝 Ответы помечай буквой блока и номером: «A2», «B1.б». Разбор — после твоих ответов.
```

Block headings carry ordered letters: «Блок A», «Блок B», «Блок C». An optional
name appears only in parentheses, e.g. «Блок A (Разминка)». Do not add methodological
explanations such as «(атомарные — по одному правилу)» to the learner's sheet.

Restart numbering at 1 within each block. The address is the pair of block letter and task
number, never the number alone. See `output-format.md` for subitem references. This mode's
numbering does not apply to the written-control profile.

The order atomic → integration → composite is required: start simply and combine material
at the end. A full Russian → Thai text/dialogue translation of 3–6 turns makes a useful
final task combining vocabulary, word order, particles, constructions and tones. Alternate
it with situation dialogues and descriptions. Keep examples fresh in every block.

## Mode C — assessment / control test

Select for «срез», «контрольная», a graded test or a whole-chapter assessment.
Read `thai-learning`, «Система контроля», for thresholds, no-hint checking and retakes.
For chapter controls or explicitly written controls also read `written-control.md`:
static dark HTML file, handwritten answers, continuous task IDs, production-first design.
An explicit request for another delivery format overrides that default.

The engine owns two assessment responsibilities:

- **Coverage instead of the 60/40 spiral.** Cover every subtopic in the requested scope.
  Use `get_due` only to prioritise overdue/weak elements inside that scope; mix task types
  without importing another chapter's material.
- **Results must return to the tracker after answers are checked.** Hand off to
  `thai-mistakes` for the full report, `record` for each assessed element (not just errors),
  `mistake` for patterns, and `set-meta --recent-accuracy`. Generating a test does not
  establish an achieved score or close a topic.

Short assessments outside the written-control profile retain worksheet layout without
hints or inline analysis; feedback arrives in one report after all answers. The written
profile uses its own header and layout instead of the generic `🔒` template. The ⚑ rule
for genuinely necessary unfamiliar support remains applicable, but it must never reveal
an assessed answer; the written profile first rewrites tasks using taught material.

## Closing test for a topic

A special case of C, not a fourth mode. This skill assembles the sheet; `thai-mistakes`
checks it, reports and records the closing outcome. The boundary remains the verdict.
The written delivery profile, when applicable, does not remove these extra requirements:

1. **At least 70% productive tasks.** This does not ban Thai → Russian: receptive topics
   such as letters, vowels, tones and reading still require complete coverage.
2. **At least one trap for a typical misconception in the topic.** See
   `thai-mistakes/references/misconceptions.md` when choosing it. Without a trap, the sheet
   may only test recall of the previous explanation.
3. **Forecast before the first task.** Ask once and wait before issuing the sheet:

   > Считаешь эту тему закрытой — и сколько из N, по-твоему, сдашь?

   Only before seeing tasks/results is the forecast uncontaminated. If the user declines,
   continue without insisting and do not set `--calibrated`.
4. **Ask the learner to mark uncertain answers** in the header. Example:

   > 7. [ответ] — *(не уверена)*

Then follow answers → checking → `thai-mistakes`. For closing gates, flags and failure
handling, read `references/progress-and-spiral.md`, «Состояния темы и закрытие».
