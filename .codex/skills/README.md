# Thai project skills

The set of skills that turn Codex into a personal Thai tutor for this repository.
Practice-first teaching: deliberate composite tasks, a spiral with spaced repetition,
production рус→тай, a serious tone with no gamification.

Written in English; **everything the learner sees is in Russian**. Names in Russian quotes
below — statuses, section headings, category values — are literals the code or the parser
matches on, so they are quoted exactly and never translated.

## The map

**Who owns what, and where the turn goes next, is in [`MAP.md`](MAP.md)** — the roles of both
layers, the connection diagrams, the `thai-tasks` / `thai-mistakes` boundary, the meta loop and
the fate of its artifacts. That is the file the meta skills load: deliberately small, and the
one place a zone or a hand-off is described. This README is the operator's handbook — the
tracker, the toolchains, how to run things.

**[`assessment-artifacts.md`](assessment-artifacts.md)** is the shared contract for HTML
topic files, flat controls and reports, control-named practice directories, dates and
relative links. `thai-tasks` and `thai-mistakes` link to it; their pedagogy stays in their
own references.

**[`content-sources.md`](content-sources.md)** is the shared evidence contract used while
authoring course material. It assigns separate sources to lexical meaning, grammar,
examples and register, classifies long-form grammars and FSI material as secondary evidence,
and keeps external research from leaking new material into a source-only control.

## Where the theory lives

The lesson material sits in this same repository:

- `Thai A2/Chapter N/practice/NN_*.html`
- `Thai B1/Chapter N/practice/NN_*.html`

Legacy chapters may still contain `glavaN_temaM_*.md` until their explicit migration; do not
create new Markdown topic files.
- `Helpers/*.md` — extra references (e.g. directional particles)

thai-tasks searches **recursively** and takes vocabulary and rules from these files (it does
not reuse the examples from the «Практические упражнения» section — it generates fresh ones).

**A topic's closing criterion comes from its own file and is never invented separately.**
`import` picks it up into `exit_task`, looking in two places in order:

1. the section **«Тема закрыта, если ты можешь»** — an explicit criterion, when written;
2. **«Резюме по теме»** — the «К концу темы ты должна уметь» list that already ends all 36
   written files. That *is* the ready criterion: actions rather than knowledge, in exactly
   the right shape.

The parser takes only list items under the matching heading (stripping ✅ marks), so a
section formatted as a bold line or a table will not be picked up. New HTML topics keep the
explicit section hidden because it is service data; legacy visible summaries remain a
migration fallback. A topic where neither was found gets the status «нет критерия» and
cannot be closed.

## Progress tracker

thai-tasks keeps `progress.json` (in the project root) via the script
`thai-tasks/scripts/tracker.py` — Python 3.8+ standard library only, fully offline.

```bash
# import a topic's vocabulary
python3 .codex/skills/thai-tasks/scripts/tracker.py import progress.json \
    "Thai A2/Chapter 3/practice/04_daily_routine.html" --topic 3.4
# what is due for review
python3 .codex/skills/thai-tasks/scripts/tracker.py due progress.json
# apply SM-2 after an answer (quality 0–5)
python3 .codex/skills/thai-tasks/scripts/tracker.py record progress.json "ตื่น" 5
# weak exact word without reopening its whole topic
python3 .codex/skills/thai-tasks/scripts/tracker.py record progress.json "พฤศจิกายน" 1 \
    --topic 3.3 --item-only
# record a mistake pattern
python3 .codex/skills/thai-tasks/scripts/tracker.py mistake progress.json "тон_финаль" --category Тоны --topic 3.4 --your ... --correct ...
# reclassify remediation without recording another occurrence
python3 .codex/skills/thai-tasks/scripts/tracker.py mistake-mode progress.json "тон_финаль" tones \
    --reason "несколько слов нарушают одно правило тона"
# drill plan (topics, modes, volume) and the outcome of a drill round
python3 .codex/skills/thai-tasks/scripts/tracker.py drill-plan progress.json
python3 .codex/skills/thai-tasks/scripts/tracker.py attempt progress.json "тон_финаль" --result ok
# topic states: what is closed, what blocks closing, the outcome of a closing test
python3 .codex/skills/thai-tasks/scripts/tracker.py lesson progress.json 3.4
python3 .codex/skills/thai-tasks/scripts/tracker.py topics progress.json
python3 .codex/skills/thai-tasks/scripts/tracker.py blockers progress.json 3.4
python3 .codex/skills/thai-tasks/scripts/tracker.py close progress.json 3.4 --result ok \
    --accuracy 0.9 --production --no-hints --calibrated
# progress overview
python3 .codex/skills/thai-tasks/scripts/tracker.py progress progress.json
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

## Transcription reference

`thai-phonetics/scripts/phonetics.py` reads the same `references/*.md` the model reads —
there is deliberately no second copy of the data. Stdlib only, offline.

```bash
S=.codex/skills/thai-phonetics/scripts
python3 $S/phonetics.py sign ร            # class, initial, final, example
python3 $S/phonetics.py finals т          # every sign that yields this final
python3 $S/phonetics.py check             # validate the reference files
python3 $S/phonetics.py check --course    # …and scan Thai A2/B1/Helpers as well
```

`check` catches what the eye misses: latin homoglyphs wearing tone marks (`â` for `а̂`),
leftover macrons, `å`, `ɣ`, and any drift between `SKILL.md` and `consonants.md`. Sections
headed «Требует сверки» or «Расхождения с источником» are exempt on purpose — they exist to
keep the disputed material visible. `--course` is still noisy: course tables use headers the
scanner does not know yet, so read its output as leads, not as a verdict.

## Dictionary cache

`thai-verify/scripts/warm.py` fills the local cache of thai-language.com pages ahead of time,
so a lesson survives the site or DNS going down. Stdlib only — and the one script here that
deliberately goes online, since removing that dependency is its whole point.

```bash
W=.codex/skills/thai-verify/scripts/warm.py
python3 $W status            # how much of the vocabulary is cached — offline
python3 $W warm              # download what is missing (~1.6 s per word, 617 words ≈ 17 min)
python3 $W warm --limit 50   # a smaller batch
```

The cache lives in `~/.cache/thai-dict`, keyed by md5 of the word; the session folder is wiped
and must not hold it. Runs are idempotent, so an interrupted batch is resumed by repeating the
command. Words the dictionary has no entry for are printed as a list rather than cached —
caching a "no results" page would make an unverified word look verified.

## Handwriting recognition

The whole thai-handwriting toolchain runs offline. The main path uses what is built into
macOS, nothing to install:

```bash
S=.codex/skills/thai-handwriting/scripts

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
npx pyright --stats     # «Found N source files» + «0 errors»
```

Read the file count, not just the error count: `exclude` here deliberately omits `**/.*`
(the whole codebase lives under `.codex/`), and restoring that default makes pyright
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
2. mistakes go into `progress.json` with their category, topic and remediation mode;
3. rules and broad gaps produce thematic modules, while an exact word that repeatedly
   fails produces a compact memory module only for the target lexemes; both belong to one
   dated practice HTML when they come from the same report;
4. live work is opt-in: thematic gaps receive a mini-diagnostic and rule drill; lexeme gaps
   receive an error trace, one retrieval hook, fading support and delayed production;
5. a misconception is cleared after the old reasoning is corrected and a fresh trap case
   is passed; a lexeme round is cleared after two separated recalls without a visible model;
6. a repeated mistake gets a rebuilt second round. Still not cleared — first thing next
   lesson, status `critical`.

Reference files: `thai-mistakes/references/report-format.md` (report format),
`thai-mistakes/references/thematic-html-modules.md` (self-study practice modules with
built-in answers), `thai-mistakes/references/drill-modes.md` (live drill modes),
`thai-mistakes/references/lexeme-memory.md` (focused retention cycle for exact words that
repeatedly fail),
`thai-mistakes/references/misconceptions.md` (types of misconception, the counterexample
method, the closing criterion).

## thai-tasks reference files

Chapter control tests default to a saved, static HTML sheet with a dark screen theme and
handwritten answers submitted through `Handwriting/`. Ask for an interactive test explicitly
when that is wanted. Ordinary worksheets and live sessions retain their own formats.

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
- `thai-tasks/references/written-control.md` — written chapter controls: source coverage,
  active recall, no answer leaks, continuous task IDs, static dark HTML file and checks.
- `thai-tasks/references/output-format.md` — sheet layout (lettered blocks, numbering,
  lists, vocabulary presentation, transcription) and the checklist for unambiguous task
  wording.
- `thai-tasks/references/speaking-and-live.md` — conversational practice in text and live
  material from the browser (Codex browser).
- `thai-tasks/references/mission-and-records.md` — mission, learning-records, trusted
  sources.

## Работа над системой

Идеи и варианты обсуждай прямо с Codex — отдельного навыка или каталога техник для
мозгового штурма больше нет. Исторические записи в `.codex/brainstorms/` сохранены.

- `skill-writer` — короткие правила проекта для редактирования навыков, справочников и
  учебных материалов; обязательного стиля оформления нет.
- `skill-review` — отдельный процесс для критического аудита изменений, файлов и навыков.

## Notes

- Transcription is strictly Cyrillic; the tone mark sits over the vowel.
- Tones are verified against an authoritative source (thai-language.com) before any verdict,
  never from memory.
- `RESOURCES.md` in the project root divides the sources by zone: the dictionary owns the
  word (spelling, meaning, tone), thai-alphabet.com owns the single sign (class, positional
  reading, sound), and the course files own the taught scope. `content-sources.md` adds
  separate evidence roles for lexicon, grammar, examples and register while authoring.
  A conflict is marked «спорно» and never reaches the learner's sheet.
- The Lithuanian skills (`lithuanian-*`) belong to the separate LT project and are not
  needed here.
