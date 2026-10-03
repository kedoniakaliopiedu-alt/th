# Written control test for handwritten answers

Read when assembling a chapter control test or any explicitly written control test.
This is the default delivery profile inside mode C, not a fourth teaching mode.
Instruction prose is English; every heading, instruction and label delivered to the
learner is Russian. This file implements the user's written-test brief and subsequent
preferences for an actual file and a dark theme.

## Trigger and precedence

«Контрольная по главе N», «письменная контрольная» and «контрольная в HTML» select this
profile. HTML is a sheet to read; answers are handwritten on separate paper and then
photographed into `Handwriting/`. Do not ask again whether it should be interactive.
An explicit request for an interactive test, chat delivery, another theme or another
length overrides the corresponding default. A short «срез по теме» keeps its requested
scale; do not expand every mini-test into 25–35 tasks. Sessions and ordinary worksheets
keep their existing rules in `scope-and-modes.md` and `output-format.md`.

For this profile, the numbered parts, continuous task numbers and static HTML below
replace generic worksheet layout, Markdown-only output, the generic control-test header,
and vocabulary/transcription presentation. No-hint checking and control thresholds remain
owned by `thai-learning`; report and mistake handling remain owned by `thai-mistakes`.
Closing tests also retain the extra requirements in `scope-and-modes.md`.

## Read the source before composing

1. Resolve the level and chapter from the request or established context. Read **all**
   lesson files in the requested scope in full, including vocabulary and theory. Existing
   tests are layout references, not evidence that a word was taught.
2. Make an internal coverage map: source topic → vocabulary/construction → task IDs.
   Cover each source topic and the requested skills: vocabulary, Thai spelling, reading,
   grammar, sentence building, meaning, translation and independent writing.
3. Use only the named chapter's taught vocabulary and constructions. Build new sentences
   and situations; do not copy exercise examples verbatim. Difficulty comes from combining
   known material, not importing an unfamiliar word.
4. Disable the 60/40 spiral. The tracker can prioritise weaknesses **within** the requested
   scope; an overdue word from another chapter is not permission to include it.
5. If files are missing or insufficient, state the precise gap and request the missing
   material or a narrower scope. Do not invent chapter content, silently use a chapter
   plan as a taught lesson, or pad a short source to reach the target length.

Unfamiliar Thai is not a default escape hatch. Rewrite the situation using taught material.
If a user-authorised scenario genuinely requires a supporting word, apply `thai-learning`'s
⚑ rule, exclude that word from assessment, and ensure the note reveals no tested answer.

## Composition: production from memory first

For a full chapter aim for **25–35 top-level tasks**, not 25–35 HTML controls. Count actual
answer units too: avoid inflating a nominally short test with dozens of hidden subitems.
Use subitems only for independently answerable cases and keep each task's requested volume
explicit. A short source or an explicit user limit takes precedence over the target.

Use these approximate shares as planning guidance, not mechanical quotas:

| Primary purpose | Share |
|---|---|
| Russian → Thai, including active vocabulary | 30–40% |
| Independent Thai sentence production | 20–25% |
| Grammar application | 10–15% |
| Thai → Russian / reading comprehension | 10–15% |
| Error correction, dialogues and other tasks | Remainder |

Assign each answer unit one primary purpose when checking the balance; do not count a
single dialogue under several headings to manufacture the target. The resulting sheet
must require more Thai produced from memory than recognition. Prefer a Russian meaning or
situation over choosing an answer. No multiple choice in the default profile; add it only
when explicitly requested for a specific diagnostic purpose.

Cover these ten functions with separate, clearly named parts when the source supports them:

1. **Активная лексика — русский → тайский.** Russian meanings; write Thai from memory.
   No first letters, word lengths, transliteration, answer bank or other spelling hints.
2. **Тайское письмо.** Recall learned spellings; do not make this mechanical copying.
   Reserve any supplied misspellings for the error-correction pool below.
3. **Грамматика.** Recall/apply taught constructions: translate, transform or write an
   example. A named Thai construction is allowed only when recalling that construction
   is not the thing being tested; otherwise describe the intended meaning in Russian.
4. **Построение предложений.** Include both a shuffled-word task and Russian-only
   situations. Situations requiring a complete sentence from memory must outnumber
   shuffled-word tasks.
5. **Перевод — русский → тайский.** A substantial part, progressing from short sentences
   to combinations of taught vocabulary and grammar; no answer hints in parentheses.
6. **Чтение и перевод — тайский → русский.** A smaller part using separate target words
   and phrases so the supplied Thai does not answer production tasks elsewhere.
7. **Диалоги и реальные ситуации.** Brief everyday contexts, independently written
   replies or a short dialogue; specify roles, purpose and number of turns.
8. **Исправление ошибок.** State the intended meaning and the number of errors. Ask to
   rewrite the entire sentence correctly. Verify the proposed correction before issuing.
9. **Активное воспроизведение без подсказок.** Recall words, questions or different
   sentences without an answer bank. State a concrete count and topic.
10. **Свободное письмо.** Finish with 2–4 harder tasks: a short text, description or
    mini-dialogue combining several chapter elements. Specify the length and observable
    requirements in short sentences. This is an assessment, not a mistake drill: the
    `thai-mistakes` ban on free-writing drills does not prohibit this section.

The user may specify another order. Otherwise progress from simple recall through
application to independent writing, ending with free writing. If source scope does not
support a function, disclose the limitation instead of inventing material to fill it.
Label difficulty in Russian: 🟢 Базовый / 🟡 Средний / 🔴 Сложный. These mean recall,
application in a new sentence, and independent combination of learned material.

## Prevent answers leaking between tasks

Before rendering, compare the internal expected answers with **all supplied Thai anywhere
on the sheet**, including passages, shuffled words, misspellings, examples and instructions.
Partition target vocabulary and model phrases between production and supplied-Thai tasks.
Common function words may recur; the exact target spelling or model answer being recalled
must not be supplied in another task. Reusing a learner-produced word later is not a leak.

Moving a revealing reading passage to the bottom is not protection: a static file remains
scrollable. First replace the revealing example with other taught material. If the source
is too small to separate targets, reduce overlapping tasks or disclose the coverage limit;
do not claim that a «не подсматривай» instruction makes the answers inaccessible.

No glossary, answer key, solutions, revealing transcription, solved examples or hidden
answers in HTML comments, data attributes, CSS or collapsed sections. Keep any working
solutions separate from the delivered file; do not attach them unless requested after the
attempt. Check every task internally, accepting alternative valid answers rather than
requiring one model phrase.

## Stable handwriting addresses and assessment

Use headings such as «Часть 1. Активная лексика — русский → тайский» and continuous task
numbers **1–N across the whole sheet**. Independent cases use Latin **a), b), c)**; the
answer address is **5c**. Do not restart numbering per part or switch to worksheet A1/B1.
Two separately required sentences are labelled subitems before delivery, not invented as
12a/12b at grading time. For a connected text, distinguish its requirement list from
separate answers: «Ответ — один текст под номером 26».

Define the scoring units and denominator before delivery, following
`thai-mistakes/references/report-format.md`. For connected writing, state whether each
listed requirement is a scored unit; do not count the whole text again on top of them.
This prevents a different denominator being improvised when the photographs arrive.
Specify whether numerals must be words or digits wherever that distinction is assessed.

Example of learner-facing layout (replace placeholders with source-grounded tasks):

```text
Часть 1. Активная лексика — русский → тайский
1. 🟢 Базовый. Напишите каждое слово по-тайски.
   a) [русское значение]
   b) [другое русское значение]

Часть 2. Тайское письмо
2. 🟡 Средний. [Одно конкретное действие.]
   [Точный формат ответа.]
```

## Build and deliver the actual file

Create one UTF-8 HTML file with embedded CSS, responsive layout and no external runtime
requirements. No JavaScript, forms, input fields, radio buttons, checkboxes, dropdowns,
«Проверить» buttons or interactive answers. No large blank answer areas: writing happens
on separate paper. Use semantic headings and lists, generous line height and Thai fonts
with local fallbacks; Thai text should be about 25–28 px on screen.

Inspect neighbouring HTML files and match their dark theme. If none exists, use this
project palette: background `#0e131a`, cards `#151b24`, text `#e7ebf1`, muted `#a9b3c1`,
borders `#2a323d`, accent `#8fb0e4`. Set `color-scheme: dark`; provide a white, readable
`@media print` style. Separate sections without decorative clutter.

The page begins with (substitute the actual chapter):

> **Контрольная работа — Глава N**
>
> Имя: __________
>
> Дата: __________
>
> Выполните все задания письменно от руки на отдельном листе. Нумеруйте ответы строго
> в соответствии с номерами заданий. Не используйте переводчик или учебные материалы.
> После выполнения сфотографируйте работу и загрузите фотографии в папку Handwriting.

Save beside the chapter material, e.g. `Thai A2/Chapter 3/thai_chapter_3_test.html`.
For a different scope use an equally unambiguous name. Preserve a test that already has
answers or a report: a new attempt needs a distinct filename, not an overwritten source
sheet. For an explicit edit to an existing sheet, update that file.

Deliver a clickable link to the completed file and a brief Russian status. Do not paste
HTML into chat as a substitute for creating the file. Only return source code instead
when the current user explicitly requests code-only delivery.

## Verify before saying it is ready

1. Confirm the file exists, is nonempty and contains the complete intended sheet.
2. Check coverage, production balance, absence of answer leaks, every numbered task and
   every subitem. Solve all tasks internally; replace unsolvable or ambiguous items.
3. Inspect the delivered HTML for forbidden controls, scripts, keys and placeholders.
   Check Thai font fallbacks, responsive CSS and print styles.
4. Open the file with an authorised browser capability and inspect the start, a middle
   section and the end for Thai rendering and readable layout. If browser access is
   unavailable or blocked, obey the restriction, perform file checks and explicitly
   report that visual verification remains incomplete. Never bypass a browser block.
5. Run `git diff --check` for tracked edits; check a new untracked file for whitespace
   issues too. Do not claim success merely because generation was attempted.

When answers arrive, keep the source sheet unchanged. Today's `Handwriting/` files go
through **thai-handwriting**, then **thai-mistakes** supplies the full report and tracker
updates. Use the original IDs and predeclared scoring units. This profile does not replace
handwriting verification, dictionary tone checks, or the requirement to resend a complete
corrected report.
