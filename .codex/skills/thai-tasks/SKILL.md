---
name: thai-tasks
description: >
  Composite Thai practice engine for project Thailand. Use whenever the user asks
  for tasks, drills, practice, exercises or a composite set: «дай задания на счётные
  слова», «потренируем еду», «составь воркшит по вопросам», «хочу спираль с повтором
  тонов», «разговорная практика на рынке», «дай позаниматься», «контрольная по главе»
  or «письменная контрольная». It combines new material with spaced review in sessions
  and worksheets, tracks progress, and assembles coverage tests without hints or
  outside-scope spiral material. Chapter controls default to a standalone dark HTML
  file for handwritten answers; explicit interactive requests override that format.
  Uses learn for pedagogy, thai-learning for presentation and checking, thai-phonetics
  for transcription, and thai-display for optional word styling. Also owns topic
  states and closing sheets: «давай закроем тему 3.4», «дай закрывающее испытание»,
  «что мне осталось, чтобы закрыть тему», «можно уже её отпустить», «не чувствую, что
  закрыла». It does not record the closure verdict: after checking, thai-mistakes
  invokes close. Do not use for a single-word translation without practice intent
  (thai-learning), or for editing the tutor machinery itself (skill-writer).
---

# Thai Tasks — composite practice engine

This skill turns a Thai topic into practical tasks. It builds on `thai-learning`, which
owns presentation and checking rules; this skill owns how to assemble a useful set, choose
its scope and mode, and connect practice to progress.

Instructions are English. Learner-facing text, quoted triggers, data values and examples
remain Russian; Thai and Cyrillic transcription are never translated.

Ked learns **by doing**: abstract theory does not stick. Use **action before rule** in
practice. Each task is an action, not a lecture; the rule emerges after she has tried it.
A control test measures existing knowledge and does not introduce rules or worked examples.

## Always start here

1. **Find the topic material (vocabulary and theory).** Search in this order:
   1) the connected local clone of `kedoniakaliopiedu-alt/th`; search recursively for
      `**/*glava*tema*.md` rather than assuming a flat layout;
   2) THAILAND project files, if available.

   If material is missing, distinguish two cases:

   - **No folder is connected:** there are no course files anywhere in the available
     repository. Do not try `git clone`, `git pull`, or fetching the private repository
     from the web as a substitute for attaching it. Ask the user to connect the `.../th`
     folder, then continue. A project sync may not have materialized its files locally.
   - **The folder is connected but this topic is unwritten:** the course is incomplete.
     Check the actual files and `Thai B1/thai_b1_plan.md`; do not assume every planned
     chapter exists. Explain that the material is absent and offer a neighbouring written
     topic, tasks based on the chapter plan with externally verified vocabulary, or writing
     the topic first. Do not ask to connect a folder already available. For a source-only
     control, do not silently substitute a plan or outside vocabulary for missing sources.

2. **Read mission, tracker and sources:** `MISSION.md`, `progress.json`,
   `learning-records/`, `RESOURCES.md`. Tie tasks to the learning purpose. If mission or
   tracker is absent, create it at the first lesson (ask about the goal for the mission).
   Read **references/progress-and-spiral.md** and **references/mission-and-records.md**
   when initializing or updating this context.
3. **Identify topic, scope, difficulty and mode before selecting review material.** Use
   the user's topic; otherwise choose the next progress step or ask one question. Scope
   follows the table below. Difficulty is `meta.difficulty`, 1–10, default 4. «Сессия» /
   «по одному» selects A; «воркшит» / «комплект» selects B; «срез» / «контрольная» /
   «тест на оценку» selects C. An unspecified practice set defaults to B. A requested
   chapter control is already an unambiguous C request: do not ask whether to split it
   into lessons. Read **references/written-control.md** for a chapter or written control.
4. **Import the topic into the tracker before generating tasks.** Import vocabulary and
   rules from its source file if absent, using the procedure in progress-and-spiral.md.
   This makes items available for tracking; importing them is not evidence of mastery.
5. **Check topic state:** `tracker.py topics progress.json --topic <тема>`, once the topic
   is known. A `закрыта` topic is not new material: the request is a control or reopening.
   `нет критерия` means a closing criterion was not found: practice is allowed, closure
   is not. Mention this **once per topic**, not at every lesson. Read the topic-state and
   closure section in **references/progress-and-spiral.md** when handling these states.
6. **Plan according to the selected mode.** In A/B, use get_due for the 60/40 spiral. In
   C, read all sources in the requested scope and plan coverage of them; due items may
   prioritize weaknesses **within that scope only**, never import another chapter.

→ Dialogue pedagogy, «просто скажи ответ», and diagnosis: read skill **learn** when running
  live practice.
→ Transcription and tone marks: read **thai-phonetics** when writing transcription.
→ Consonant-class styling: use **thai-display** only for an explicit request for that
  breakdown; default worksheets do not use its colours.
→ Checking, hints, controls and unfamiliar-word annotation: read **thai-learning** and
  **references/checking.md** when preparing to check answers.
→ Scope, output modes, worksheet template and closing-test properties: read
  **references/scope-and-modes.md** whenever assembling a sheet.
→ Static chapter controls and written controls: read **references/written-control.md**
  before assembling or delivering them; it owns their format and source-only workflow.
→ Tracker, get_due, SM-2, mastery, vocabulary import and difficulty: read
  **references/progress-and-spiral.md** when using these mechanics.
→ Mission, learning records and trusted sources: read **references/mission-and-records.md**
  when choosing context or recording a qualitative change.

Ground every set in `MISSION.md`; examples should serve a real purpose. **Never invent
Thai from memory:** take spelling, meanings and tones from project files and their assigned
sources, and verify uncertainty. Tone verdicts follow thai-verify's sole-source protocol.

## Four principles behind the tasks

**1. A task is an action in context, not a theory quiz.** Instead of «перечисли пять правил
тона», use a meaningful action such as «вот реплика из лакорна — прочитай её и ответь
героине». Practice may draw on lakorns, songs, social posts, markets, cafés, taxis and
introductions. Meaning and purpose come first; language form is the tool. In A/B,
**introduce a new rule inductively:** show 3–4 examples and ask for the pattern before
naming it (the «Вывод правила из примеров» format in exercise-catalog.md). In C, keep
contexts inside the selected source material and do not introduce new rules.

**2. Push production, not only recognition.** Producing Thai from scratch builds usable
language. Every set needs Russian → Thai tasks: assemble a word, write a sentence, reply,
or describe a situation. Do not make a set entirely Thai → Russian translation; bias the
balance toward production. Written controls use the active-recall rules in written-control.md.

**3. New material lives through old material in practice.** A/B use spaced repetition and
interleaving inside the new context instead of an isolated review block. For new «еда» and
review «счётные слова + тоны», «закажи две порции риса по-тайски» works on both layers.
C is the exception: it measures coverage of its stated topic/chapter, without the 60/40
spiral or material from outside the sources.

**4. Fresh examples, not copied theory.** Take vocabulary and rules from the sources, then
build new situations and sentences. Do not copy source model sentences or repeat the same
sentence across tasks: that tests memory of an example rather than transfer. Freshness does
not authorize new vocabulary or constructions in a source-only control.

## Request scope: rule → subtopic → topic → chapter

Identify scope from the request; ask one question only if genuinely ambiguous.

| Scope | Meaning | Output |
|---|---|---|
| Rule / construction | One technique inside a subtopic | **At most 5 tasks:** warm-up and assembly, no composite finale |
| Subtopic (6.1.2) | Vocabulary and several constructions | All three blocks, normally 6–10 tasks |
| Topic (6.1) | A collection of subtopics | Blocks per subtopic plus one combined finale; clarify whole topic versus separate sessions for practice |
| Chapter (6) | A collection of topics | For practice, a topic-by-topic plan or a control; for an explicit chapter control, produce the complete control directly |

File hierarchy: `Глава` → `Тема N.M` → `Подтема N.M.K`, with «Словарный запас»,
«Теория/конструкции», «Практические упражнения». Search recursively for
`**/*glava*tema*.md`.

Production applies at every scale. The 60/40 spiral applies to A/B only. Chapter controls
normally contain **25–35 top-level tasks**. Also count the actual answer units so that
sub-points do not quietly turn that range into an oversized test; follow written-control.md
for coverage and an explicit requested count.

→ Read **references/scope-and-modes.md** when applying scope to a sheet.

## The 60/40 spiral (A/B only)

In a practice set or long session, aim for:

- **~60%** on the new topic: vocabulary, construction or rule.
- **~40%** revisiting learned material, woven into the new topic rather than isolated.

Use **get_due**, following references/progress-and-spiral.md. It returns items whose review
interval has expired, prioritizing mistakes and low mastery. Weave 2–4 of them into the
new topic. If none are due, use 1–2 with the lowest mastery, or focus entirely on new work.

An explicit request such as «сегодня только новое» or «повтори побольше тонов» overrides
the default balance. Do not apply this section to C: coverage, not a review quota, owns it.

## Output modes

- **A — живая сессия:** one task → answer → review → adapted next task. Default for
  dialogue and conversational Thai; use the rhythm from **learn**.
- **B — воркшит:** a coherent set with one story thread and increasingly complex A/B/C
  blocks. Default for an unspecified «комплексное задание».
- **C — срез/контрольная:** coverage of the selected topic/chapter, no hints, results
  returned to the tracker. Read **thai-learning**, «Система контроля», for grading and
  retake rules, and **references/scope-and-modes.md** for assembly. A closing test is a
  special case and retains its four extra properties: at least 70% production, a trap,
  a forecast before the first task, and a request to mark uncertain answers.

**Chapter and written controls default to a saved standalone dark HTML file**, linked in
chat, for answers written on paper and submitted through `Handwriting/`. Do not substitute
raw HTML in chat for a requested file. Read **references/written-control.md**: the default
has no JavaScript, input fields, answer keys or hidden solutions. An explicit request for
an interactive test, another medium, or raw code overrides the delivery default; it does
not waive source coverage or no-hints rules.

→ Read **references/scope-and-modes.md** when assembling any sheet and
  **references/written-control.md** for the written-control branch.

## Layout and wording

Read **references/output-format.md** whenever assembling a sheet. For written controls,
written-control.md owns HTML layout and continuous numbering; ordinary worksheets keep
lettered blocks and numbering restarted inside each block.

- Worksheet headings are lettered: «Блок B (Сборка)». References include the block:
  `Блок B.Задание 2.Пункт Б`.
- Use real lists (Markdown in chat, semantic HTML lists in HTML). **Two or more separate
  objects mean that many lettered sub-points:** а, б, в. Four single letters still require
  four points. Put the instruction on the numbered line and the material below it.
- Vocabulary format in practice is `**тайское**` · *транскрипция* — перевод, without
  consonant-class colouring unless explicitly requested. Never add a vocabulary gloss,
  transcription or worked example that reveals a control answer.
- Transcription is Cyrillic only; the tone mark goes over the **vowel**, not a consonant.
- Keep spiral percentages, mastery, source references and other methodology off the sheet.
- Each item has one action verb and explicitly states what to submit and in which format.
- **Use plain, concrete wording without metalanguage.** Do not ask for a linguistic label
  (แม่/«мать», มาตรา, คำเป็น/คำตาย, IPA) or introduce untaught terms. Ask an observable
  fact: «на какой звук заканчивается слово», «какой значок стоит над буквой». When options
  are appropriate, use real sounds, not codes. One short sentence for the instruction,
  another for the answer format. «Охарактеризуй», «определи природу», «при этом учитывая»
  signal a rewrite. A person who knows the words but no grammar terminology must understand
  on first reading; rewrite instead of appending an explanation of the term.
- **Every sub-point must have a valid answer.** Solve it internally before delivery. A list
  assembled only by theme can contain an impossible item (e.g. ฝ as a final consonant).
  Do not put those internal answers in the control artifact.

→ Read **references/exercise-catalog.md** when selecting varied atomic, integrated and
  composite formats, rather than repeating one task type throughout.

## Speaking practice and live material

Practice conversation in text (audio is not assumed): a role-play with a scene and goal,
quick replies, register changes, and checking Cyrillic transcription. Use **A**, one turn
at a time. If a **Codex browser** capability is available, a line from a lakorn or Thai
post can become practice material.

→ Read **references/speaking-and-live.md** for speaking, pronunciation or register
  requests, including the boundaries on what may go into a browser.

## Checking answers: summary

Read **references/checking.md** before checking. When today's photos arrive in
`Handwriting/`, first use **thai-handwriting** for recognition; a handwritten submission
is not permission to bypass its pipeline.

**Immediately after checking any tasks, hand over to `thai-mistakes`.** It issues the full
sheet report (✅ / 🟡 / ❌ and the correct version), records mistakes with their topic,
and prepares practice for the whole topic behind each error. Do not replace it with an
ad-hoc review or move on before the report is delivered.

- **Hints before answers in ordinary practice.** First identify the problem and offer a
  lead without the answer; if that does not work, give the correct version and explain
  what was wrong and why. A control has no hints: review all submitted answers in one
  report after completion. In a graded report every non-✅ item has its full correct
  answer, as required by AGENTS.md.
- **Evaluate productive answers in four categories:** Словарный запас, Грамматика,
  Орфография, Тоны, with a separate verdict for each applicable category.
- **Verify tones only through thai-verify's authoritative source**
  (`http://thai-language.com/dict/search`), never memory. Do not infer an untested spoken
  tone from handwriting alone.
- Tone notation: ` (низкий), ˆ (нисходящий), ´ (высокий), ˇ (восходящий); mid tone unmarked.

## Difficulty, progress and the SM-2 tracker

**`progress.json`** is the source of truth, not prose in progress.md. Words and rules use
**SM-2** spaced repetition; mistake patterns have a separate store. get_due prioritizes
items due for review and weaknesses.

**Use `scripts/tracker.py`, not manual JSON edits.** The Python-standard-library script
calculates due items and SM-2 and writes updates. Commands include `import`, `due`,
`record <элемент> <0–5>`, `mistake`, `progress`, `set-meta`. Update after every completed
lesson; manual formula calculations are only a fallback when Python is unavailable.
Generating a test alone does not earn scores or record a completed lesson.

**Difficulty** is `meta.difficulty`, default **4**, A2→B1. It changes support, not grading
strictness: 1–3 translation first, 4–6 supported Thai, 7–10 immersion. Calibrate against
~60–70% success on fresh practice. A control's no-hints constraint overrides practice
support settings.

→ Read **references/progress-and-spiral.md** when recording quality 0–5, mistakes, imports,
SM-2, difficulty or «покажи прогресс» (no streaks or achievements).

## Lesson summary and homework

At the end of a session or worksheet, summarize what was learned, where mistakes occurred
and what needs work. Then give **three concrete things to review** before next time: words,
a rule or a phrase to translate. Choose weaknesses and due items; mark homework priorities
through the tracker so get_due brings them into the next set. Homework is a bridge between
lessons, not an obligation.

If the topic has one fewer blocker than at the start, give **one line** on what remains:
«Тема 3.4 ближе к закрытию: осталось снять ошибку со счётными словами». `tracker.py blockers`
output is internal: mastery, core size and pattern names such as `собака_หมา_гласная` expose
methodology, untranscribed Thai and answers. **Paraphrase it, never copy it.** No
congratulations, counters or percentages: closure is a fact, not an achievement. `закрыта`
means moving from the spiral to occasional controls, not learning forever; «отпущена» is
an alternative if the first sounds too final.

At the end of a topic lesson, run `tracker.py lesson progress.json <тема>`. Only this
command advances the waiting period before a closing test.

Topic-state requests also belong here: «что мне осталось, чтобы закрыть», «можно уже её
отпустить», «не чувствую, что закрыла». For the first two, paraphrase `blockers`. The third
is a request, not a claim to dispute: offer another closing test. If failed, `thai-mistakes`
records `close --result fail`, reopening the topic through the normal mechanism. Do not
edit progress.json by hand.

Record a short **learning-record** only for a qualitative change: a breakthrough,
corrected misconception, discovered prior knowledge or changed goal. Read
**references/mission-and-records.md** when writing it. This is an insight that changes
future teaching, not an ordinary lesson log.

## Checklist before delivery

1. Read mission, sources and learning records; imported the topic and checked its state
   through the tracker. Closed topics are not treated as new; missing criteria are mentioned
   once. The tasks serve the mission without exceeding a control's source scope.
2. Identified scope, difficulty and **mode A/B/C before spiral selection**. Rule practice
   has at most five tasks and no finale; a chapter control follows written-control.md.
3. For A/B, selected get_due review and planned ~60/40, prioritizing weaknesses and low
   mastery. For C, read every source in scope and checked coverage without outside material.
4. Used varied formats and production. Practice progresses atomic → integrated → composite,
   with a productive contextual finale; a control follows its coverage plan and active-recall
   requirements. A closing test retains all four additional properties.
5. Examples are fresh, not copied from source model sentences or repeated across tasks.
6. Every item passes output-format.md: action, answer format, volume, plain wording, no
   metalanguage, and an internally verified valid answer. Any format example does not leak
   an answer; no supporting hints are added to a control.
7. Formatting matches the branch: worksheets use lettered blocks with restarted numbering;
   written controls use continuous numbered tasks. Counted objects and provided matching
   lettered sub-points. Practice vocabulary is clean; control questions do not reveal
   answers through translation, transcription or ⚑ annotations.
8. For a written control, saved and validated the actual dark standalone HTML file using
   written-control.md, with no keys, JavaScript or inputs; linked the file instead of
   pasting code. Explicit format requests take precedence. Stated any blocked validation
   honestly rather than claiming a browser check that did not run.
9. After submitted answers are checked, used **thai-mistakes** for the full report,
   topic-linked mistakes and the next practice step; photos first went through
   **thai-handwriting**.
10. After a completed lesson, used the tracker for records, mistakes, lesson and recent
    accuracy; gave the summary and three homework items, and a learning-record only for
    a qualitative change. Did not record achievement merely for issuing tasks.
