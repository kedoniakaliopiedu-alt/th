# Thai project skills

The set of skills that turn Claude into a personal Thai tutor for this repository.
Practice-first teaching: deliberate composite tasks, a spiral with spaced repetition,
production рус→тай, a serious tone with no gamification.

Written in English; **everything the learner sees is in Russian**. Names in Russian quotes
below — statuses, section headings, category values — are literals the code or the parser
matches on, so they are quoted exactly and never translated.

The skills fall into two layers. **Teaching** ones (`thai-*`, `learn`, `teach`) run the
lesson. **Meta** ones (`skill-*`) service the instrument itself: invent a mechanic, write a
document, review what was written. The teaching layer is about Thai, the meta layer about
the repository; do not mix them up — every meta skill states in its `description` what it is
**not**.

## Cast and roles

| Skill | Role |
|---|---|
| **thai-tasks** | The main engine. Assembles composite practical tasks on any topic, keeps the progress tracker (SM-2), the 60/40 spiral, three modes (session / worksheet / test). |
| **thai-mistakes** | The lesson's second beat: self-assessment calibration before the verdict, a report over the checked sheet (✅/🟡/❌), writing mistakes to the tracker, drilling a whole topic in the mode matching the mistake type, a counterexample against misconceptions, the two-round rule. |
| **thai-learning** | Rules for presenting tasks and checking answers, level structure, tests. |
| **thai-phonetics** | Cyrillic transcription of Thai sounds, tone marks (` ˆ ´ ˇ). |
| **thai-display** | Word styling by consonant class. Optional — only when a class breakdown is wanted. |
| **thai-handwriting** | Reading Thai off images, handwriting above all: notebook photos, whiteboards, signs. Pipeline «preprocess → slice into lines → read → orthographic filters → dictionary». |
| **learn** | Base pedagogy: diagnose, one step per turn, a hint instead of a ready answer. |
| **teach** | Learning space: mission, learning-records, resources, glossary (formats). |

The meta layer — work on the instrument itself:

| Skill | Role |
|---|---|
| **skill-brainstorm** | Brainstorming over skill mechanics and exercise formats. Three stances (facilitator / creative partner / ideate-for-me), a catalog of 122 techniques, a session log on disk, resuming. |
| **skill-review** | Adversarial review of skills, references, scripts and course files: parallel blind layers + structured triage. |
| **skill-writer** | Technical writer: write a document, validate it against the standard, explain a mechanism, draw a mermaid diagram. |
| **python-best-practices** | Vendor skill (installed 2026-07-28, commit `aaa9e2a`): 70 Python engineering rules with an impact level each. Consulted when writing or reviewing the scripts; it is a rule book, not part of the loop below, and its own sources are never edited — they are replaced wholesale on update. |

## How they connect

There are three entry points, each firing on its own trigger; below each is what it leans on.

```
thai-tasks        ← tasks, drills, practice are asked for
├── learn            — pedagogy of the dialogue
├── thai-learning    — rules of presenting and checking
├── thai-phonetics   — transcription and tones
└── thai-display     — styling by class (optional)
        │
        ↓ answers checked — hands the turn over
        │
thai-mistakes     ← answers checked; or a direct «разбери ошибки»
├── thai-tasks       — tracker, task catalog, generation rules
├── thai-learning    — checking rules
└── thai-phonetics   — transcription

thai-handwriting  ← the message contains an image
├── thai-phonetics   — transcription of what was read
├── thai-learning    — reviewing language errors in handwritten work
├── thai-display     — styling the words reviewed
└── thai-tasks       — tracker: record a recurring handwriting defect
```

The `tasks → mistakes` arrow is a handover, not subordination: feedback is the stronger
half, and `thai-mistakes` borrows the tracker, the task catalog and the generation rules
from the engine.

The boundary between them is **the moment of the verdict**, and closing a topic is cut
along the same line: the engine keeps topic states, assembles the closing sheet and sets its
properties (share of production, the trap, the forecast before the first task); the mistakes
workflow checks, reports and records the outcome with `close`.

`teach` is deliberately absent from the diagram: it is a vendor skill (Matt Pocock) locked
against auto-invocation (`disable-model-invocation: true`). Its practices — mission,
learning-records, resources — are rewritten for this project in
`thai-tasks/references/mission-and-records.md`, and the engine goes there rather than to the
skill.

The meta layer is closed into its own loop and does not overlap the teaching one:

```
skill-brainstorm  ← «давай поштурмим», «накидай идей», «придумаем формат»
        │  change list (.claude/brainstorms/<тема>/изменения.md)
        ↓
skill-writer      ← «напиши скилл», «перепиши SKILL.md», «объясни, как устроено»
        │  written files
        ↓
skill-review      ← «отревьюй мои правки», «аудит thai-tasks»
        │  report (.claude/reviews/) + findings that warrant a rewrite
        └──────────→ back into brainstorm or writer
```

The loop is not mandatory: any of the three runs on its own. Brainstorming edits nothing,
the writer decides nothing for the author, the review writes nothing without an explicit
choice.

The loop's artifacts — the session log, the change list, the review report — live exactly
until the work has landed as code. After that brainstorm and review **offer to delete them
themselves**: nobody opens a closed report, and an abandoned `изменения.md` additionally
surfaces in the next review as unfinished work. They are deleted only by consent and only
when nothing is left open; anything committed comes back from history
(`git show <sha>:<путь>`).

## Where the theory lives

The lesson material sits in this same repository:

- `Thai A2/Chapter N/glavaN_temaM_*.md`
- `Thai B1/Chapter N/b1_glavaN_temaM_*.md`
- `Helpers/*.md` — extra references (e.g. directional particles)

thai-tasks searches **recursively** and takes vocabulary and rules from these files (it does
not reuse the examples from the «Практические упражнения» section — it generates fresh ones).

**A topic's closing criterion comes from its own file and is never invented separately.**
`import` picks it up into `exit_task`, looking in two places in order:

1. the section **«Тема закрыта, если ты можешь»** — an explicit criterion, when written;
2. **«Резюме по теме»** — the «К концу темы ты должна уметь» list that already ends all 36
   written files. That *is* the ready criterion: actions rather than knowledge, in exactly
   the right shape.

The parser takes only list items under a markdown heading (stripping ✅ marks), so a section
formatted as a bold line or a table will not be picked up. A topic where neither was found
gets the status «нет критерия» and cannot be closed.

## Progress tracker

thai-tasks keeps `progress.json` (in the project root) via the script
`thai-tasks/scripts/tracker.py` — Python 3.8+ standard library only, fully offline.

```bash
# import a topic's vocabulary
python3 .claude/skills/thai-tasks/scripts/tracker.py import progress.json "Thai A2/Chapter 3/glava3_tema4_rasporyadok.md" --topic 3.4
# what is due for review
python3 .claude/skills/thai-tasks/scripts/tracker.py due progress.json
# apply SM-2 after an answer (quality 0–5)
python3 .claude/skills/thai-tasks/scripts/tracker.py record progress.json "ตื่น" 5
# record a mistake pattern
python3 .claude/skills/thai-tasks/scripts/tracker.py mistake progress.json "тон_финаль" --category Тоны --topic 3.4 --your ... --correct ...
# drill plan (topics, modes, volume) and the outcome of a drill round
python3 .claude/skills/thai-tasks/scripts/tracker.py drill-plan progress.json
python3 .claude/skills/thai-tasks/scripts/tracker.py attempt progress.json "тон_финаль" --result ok
# topic states: what is closed, what blocks closing, the outcome of a closing test
python3 .claude/skills/thai-tasks/scripts/tracker.py lesson progress.json 3.4
python3 .claude/skills/thai-tasks/scripts/tracker.py topics progress.json
python3 .claude/skills/thai-tasks/scripts/tracker.py blockers progress.json 3.4
python3 .claude/skills/thai-tasks/scripts/tracker.py close progress.json 3.4 --result ok \
    --accuracy 0.9 --production --no-hints --calibrated
# progress overview
python3 .claude/skills/thai-tasks/scripts/tracker.py progress progress.json
```

The full mechanics (SM-2, get_due, the mistake database, auto-import, the difficulty dial)
are in `thai-tasks/references/progress-and-spiral.md`.

**Topic states.** A topic is an object with its own status, not a bag of words:
«нет критерия» → «в работе» → «на испытании» → «закрыта» → «вернулась». Closing demands
seven gates at once: a pause of 7+ days since the last lesson (by the `lesson` mark, not by
element dates), zero active mistakes on the topic, `mastery ≥ 2` on the weakest core
element, a test result of at least 85% — plus three flags about the sheet: ≥70% production,
no hints, the forecast matching the fact. Two rounds are needed, on different days; a
setback voids the rounds already counted. A closed topic does not vanish: it leaves the
spiral for rare control (90 → 180 → 365 days), and its vocabulary moves into the
`background` key of the `due` output — mandatory backdrop in tasks on other topics. A
mistake on a closed topic first puts it under suspicion, the second reopens it — not back to
the start but into a drill on the pattern that knocked it down; a topic takes at most one
hit per lesson. A topic without a closing criterion has the status «нет критерия» and cannot
be closed — visible in `topics`.

**The topic core** — rules and constructions in full plus words topped up to 18 elements (for
a small topic the core is the whole topic). The threshold is measured over it, not over all
eighty elements.

The mastery growth threshold is three correct in a row, not five: five on one element
between SM-2 intervals is practically never accumulated.

## Handwriting recognition

The whole thai-handwriting toolchain runs offline. The main path uses what is built into
macOS, nothing to install:

```bash
S=.claude/skills/thai-handwriting/scripts

$S/intake                                                              # photo from clipboard → Handwriting/ + slicing
$S/thaiocr lines фото.jpg /tmp/th --scale 4 --words-from progress.json  # slice into lines
$S/thaiocr prep  фото.jpg /tmp/clean.png --deskew --mono --scale 2      # straighten and clean
$S/thaiocr crop  фото.jpg /tmp/zoom.png --rect 400,120,300,90 --scale 6 # zoom into a fragment
python3 $S/lookup.py "?ับ"                                             # dictionary candidates
$S/clean                                                               # clear Handwriting/ («clean photo»)
```

`thaiocr` is Swift over Vision (OCR `th-TH`) and CoreImage (preprocessing); it builds itself
on first run. Vision is strong on print and unreliable on handwriting, hence the main mode
is `lines`: the page is cut into lines with upscaling and each is read separately.

There is a **second engine** — `thai-handwriting/scripts/typhoon.py` (Typhoon OCR 1.5 via a
local Ollama) — for an independent cross-check over the whole page. On this handwriting it
measured weaker than Vision, so it is not treated as truth; details and measurements are in
`thai-handwriting/references/calibration.md`. A third one (Thai-TrOCR, `trocr.py` plus a
torch venv) was measured worse than both and removed on 2026-07-28 — the measurements stay
in `calibration.md` so it does not get re-added.

## Type checking

`pyrightconfig.json` in the project root checks the skills' Python in `strict` mode. It is
optional — nothing in the workflow requires it, and pyright is not a project dependency —
but it is what keeps the annotations honest:

```bash
npx pyright --stats     # «Found 5 source files» + «0 errors»
```

Read the file count, not just the error count: `exclude` here deliberately omits `**/.*`
(the whole codebase lives under `.claude/`), and restoring that default makes pyright
analyse **zero** files while still reporting «0 errors». The config says so in a comment;
do not silence that warning.

## How to use it

Start the engine and name a topic at any scale:

```
/thai-tasks составь задания на тему Глава 3 · Тема 3.4 — Распорядок дня
/thai-tasks потренируем счётные слова
/thai-tasks дай разговорную практику на рынке
/thai-tasks покажи прогресс
```

The scale of the request drives the volume: a rule (≤5, warm-up + assembly) → a subtopic
(all blocks) → a topic (a collection of subtopics) → a chapter (a plan by topics).

## Working on mistakes

After any tasks are checked, **thai-mistakes** takes over:

0. calibration — one question **before** the verdict is shown: how many do you think are
   right, and which did you guess. A confident mistake goes into drilling first; a guessed
   hit is written to the tracker as quality 3, not 5;
1. a report over the whole sheet — the tasks as they were, with ✅ / 🟡 / ❌, the correct
   version and a «почему» line, then a summary N/Y, %, a breakdown by category and the
   calibration line;
2. mistakes go into `progress.json` with their topic;
3. a mini-diagnostic of the topic (3–5 questions) — where else the holes are;
4. the rule explained from your mistake, and a drill block: 3 tasks for the topic's first
   mistake, +1 for each further one, capped at 10. If the mistake is systemic, a
   counterexample comes first: a case where your own rule refutes itself;
5. the mode is picked by mistake type: vocabulary memorization / tone drill /
   transformations / restoring spelling / register and appropriateness;
6. a mistake is cleared once you have both stated what was wrong in the old reasoning and
   passed a fresh trap case. Correct answers alone are not enough;
7. the mistake recurred — a second round, reassembled (rule inductively, smaller steps).
   Still not cleared — first thing next lesson, status `critical`.

Reference files: `thai-mistakes/references/report-format.md` (report format),
`thai-mistakes/references/drill-modes.md` (drill modes),
`thai-mistakes/references/misconceptions.md` (types of misconception, the counterexample
method, the closing criterion).

## thai-tasks reference files

- `thai-tasks/references/exercise-catalog.md` — the menu of task types (atomic →
  integrative → composite), including inductive rule derivation, etymology/morphemes,
  narratives.
- `thai-tasks/references/scope-and-modes.md` — output volume by request scale (rule →
  subtopic → topic → chapter), the three output modes, the worksheet template, the test and
  the closing trial.
- `thai-tasks/references/checking.md` — order of review: hints → answer, scoring across 4
  categories (Словарный запас / Грамматика / Орфография / Тоны), the naturalness lens, tone
  verification.
- `thai-tasks/references/progress-and-spiral.md` — tracker, SM-2, spiral, auto-import, the
  1–10 difficulty dial, the 60–70% target success rate.
- `thai-tasks/references/output-format.md` — sheet layout (lettered blocks, numbering,
  lists, vocabulary presentation, transcription) and the checklist for unambiguous task
  wording.
- `thai-tasks/references/speaking-and-live.md` — conversational practice in text and live
  material from the browser (Claude in Chrome).
- `thai-tasks/references/mission-and-records.md` — mission, learning-records, trusted
  sources.

## The meta layer: working on the skills

Three skills service the instrument itself. Adapted from
[BMAD Method](https://github.com/bmad-code-org/bmad-method) (MIT); what exactly was taken
and what was rewritten is in each skill's `ATTRIBUTION.md`.

```
/skill-brainstorm придумаем форматы заданий на счётные слова
/skill-writer     перепиши SKILL.md у thai-display
/skill-review     аудит thai-tasks
```

**skill-brainstorm.** A session runs in one of three stances: facilitator (supplies no ideas
of its own, only squeezes out yours), creative partner (throws in its own, marking
authorship), ideate-for-me (runs the whole thing and shows the result). Stance and technique
batch are picked on an offline composer page, which has to be opened and its result pasted
back into the chat:

```bash
S=.claude/skills/skill-brainstorm
open $S/assets/brain-selector.html                       # pick the stance and the techniques

# regenerate the page if the catalog was edited
python3 $S/scripts/brain.py --extra $S/assets/extra-techniques.json \
  html --out $S/assets/brain-selector.html

python3 $S/scripts/brain.py --extra $S/assets/extra-techniques.json categories
python3 $S/scripts/brain.py --extra $S/assets/extra-techniques.json list --category методика
```

The catalog holds 108 general BMAD techniques plus 14 of our own in the **«методика»**
category (`assets/extra-techniques.json`): «Инверсия ошибки», «Обратная спираль», «Провал
скилла», «Триггерный стресс-тест» and others written for designing exercises and skills. The
session is logged to `.claude/brainstorms/<тема>-<дата>/.memlog.md` — a session survives an
interruption and resumes from the same place.

**skill-review.** Seven layers, each a subagent with no conversation context: the blind hunter
(contradictions and ambiguity), the edge hunter (what happens when material is missing or
the learner answers unexpectedly), the verification gap, skill boundaries (`CLAUDE.md`
violations and territory grabs), the pedagogy auditor (thai-tasks' three pillars), the script
reviewer, and the intent auditor (only when a statement of intent was given). Layers are
edited in `references/review-layers.md` without touching the steps themselves. Findings go through triage — dedup, reading the file **before** assigning
severity, routing into «решение / правка / отложить / шум» — and land in `.claude/reviews/`.

**skill-writer.** Four operations: write a document, validate it against the standard,
explain a mechanism, draw a mermaid diagram. The house documentation standard is in
`references/skill-doc-standards.md`: the `description` contract (including the mandatory
"when NOT to use"), progressive disclosure through `references/`, a checklist at the end of
a `SKILL.md`, and the ban on methodology leaking into text the learner reads.

## Notes

- Transcription is strictly Cyrillic; the tone mark sits over the vowel.
- Tones are verified against an authoritative source (thai-language.com) before any verdict,
  never from memory.
- The Lithuanian skills (`lithuanian-*`) belong to the separate LT project and are not
  needed here.
