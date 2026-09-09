# Project Thailand — Codex working rules

A repository for learning Thai: lesson material (`Thai A2/`, `Thai B1/`, `Helpers/`), the
progress tracker (`progress.json`) and the tutor skills in `.codex/skills/` (overview —
`.codex/skills/README.md`). Codex uses this `AGENTS.md` as the project entry point and
reads the relevant skill file directly from that library.

Instructions here are in English; **everything the user reads is in Russian** (see «Working
on the skills themselves»).

## Skill routing in Codex

Do not assume that a skill is active merely because it exists. On a matching request, read
the complete `SKILL.md` for the indicated skill before acting, then read only the references
it requires. The trigger map and boundaries are in `.codex/skills/MAP.md`.

- Thai tasks, drills or practice → `thai-tasks`; checked answers or error review →
  `thai-mistakes`; handwritten Thai → `thai-handwriting`; pronunciation or Cyrillic
  transcription → `thai-phonetics`; tone verification → `thai-verify`.
- Work on the tutor system itself → `skill-brainstorm`, `skill-writer`, or `skill-review`,
  according to the map.
- General tutoring can use `learn`; `teach` remains opt-in only.

Use paths exactly as written under `.codex/skills/`; they are project data and the sole
source of the tutor workflow.

## Images

**The trigger is the `Handwriting/` folder, not the presence of a picture.** An image in the
message is not by itself a reason to start the pipeline — the user also pastes ordinary
screenshots, and answering those with a recognition run is wrong. Before deciding anything
about a picture, look in the folder:

```bash
find Handwriting -maxdepth 1 -type f ! -name README.md -newermt "$(date +%F)"
```

- **Today's files are there** → invoke `thai-handwriting` and work **only over those
  files**, never over the picture embedded in the message.
- **Empty** → do not run the pipeline. If the picture is clearly handwritten Thai to be
  read or checked, offer `scripts/intake` (it lifts the image from the clipboard into
  `Handwriting/`), and after it lands, go through the folder. If it is an ordinary
  screenshot — just answer, no skill.
- Files older than today do not count: they belong to a finished session. Treat them as
  absent, and clean them when new work starts.

Once the skill is running, reading Thai off an image by eye, bypassing its pipeline, is
still forbidden: a whole page is recognized markedly worse than one sliced into lines, and
an unflagged guess breaks the learning loop — the review then runs on a misread word.

**The command «clean photo»** (even with no image in the message) → clear the `Handwriting/`
folder with `.codex/skills/thai-handwriting/scripts/clean`. Details are in the
`thai-handwriting` skill.

## Thai

- Tasks, drills, practice → `thai-tasks` (it pulls in the rest itself).
- **Answers checked — go straight to `thai-mistakes`**: a report over the sheet
  (✅ / 🟡 / ❌ + the correct version) and drilling the mistakes as a whole topic. Do not
  substitute an ad-hoc review of your own.
- **Tasks are worded in plain, concrete language.** No linguistic metalanguage (แม่/«мать»,
  มาตรา, คำเป็น/คำตาย, IPA), no term the course has not taught, no «охарактеризуй» /
  «определи природу» abstractions. Ask about what can be seen or heard («на какой звук
  заканчивается», «какой значок стоит над буквой»), offer options as real sounds rather than
  codes, keep the instruction to one short sentence and the answer format to a second. The
  test before issuing: someone who knows the words but no grammar terms understands on first
  reading what to do and what to send. If not — rewrite the item; do not bolt an explanation
  of the term onto it. A turn spent decoding the question teaches no Thai.
- Transcription is Cyrillic only, per `thai-phonetics`.
- **Tones are verified against thai-language.com before any verdict, never from memory** —
  the query protocol and how to pick among several entries are in `thai-verify`. It is the
  project's only tone source and has no substitute: while the dictionary is unreachable the
  tone is not graded at all — the item is postponed. Which source owns which question
  (word / single sign / vocabulary) is divided up in `RESOURCES.md`, and a conflict between
  them is marked «спорно» and kept off the learner's sheet.
- Progress and mistakes are written to `progress.json` through
  `.codex/skills/thai-tasks/scripts/tracker.py`.

## Corrections and reports

Learned the hard way, 2026-07-29 — a graded report went through six rounds of patches
because corrections were sent as deltas instead of the whole thing, and because verdicts
were issued on a first-pass, low-confidence reading instead of a checked one.

- **Any correction to a report, sheet, or list is a full resend, never a delta.** The user
  should never have to hold a mental diff between messages. Fix the item internally, then
  output the entire document again from the top — every time, no exceptions, no matter how
  small the fix.
- **«You misread that» / «I wrote something else» starts a fixed sequence**: re-check
  against the source (a zoomed crop for handwriting, `thai-phonetics/references/*` for
  spelling and transcription, an authoritative dictionary for tone) → recompute everything
  that hung off the item (marker, correct version, score, percentage, the category
  breakdown, «Калибровка», «В работу», tracker entries) → **resend the whole report from the
  top**. Never «here is the fixed item 4, the rest is unchanged» — and this holds on the
  third round of corrections exactly as on the first.
- **Every non-✅ item carries the correct answer.** A 🟡 or ❌ is never shipped without
  «→ **Верно:** …» — including items she skipped or answered «не знаю», and including ones
  whose correct version already appeared earlier in the sheet. Give it in full, in the
  format the task asked for, not as a fragment. The only exception is not knowing it
  yourself: then mark the item as being checked and come back with the answer, rather than
  writing ❌ with nothing next to it.
- **Show the user's literal answer for every item, including skipped ones.** If they wrote
  `?` or marked a flag, show that mark — never paraphrase a skip as «нет ответа» or invent
  wording they didn't write.
- **Before flagging an orthography, transliteration, or tone as wrong, check the project's
  own reference files** (`thai-phonetics/references/*`) — not memory, not a generic IPA
  chart, not a lesson file's rough intro table. This project makes deliberate, documented
  choices (e.g. ก → «г», explained in `consonants.md`) that diverge from outside sources on
  purpose; contradicting them from memory is a false «error».
- **On handwriting, a first low-res pass is not a verdict.** Before marking anything ❌ or
  🟡, crop and zoom the specific answer region — tone marks and diacritics are the first
  thing lost at page-level resolution, and a missed mark produces a false negative, not a
  real mistake. Two visually similar letters in this handwriting (ฎ/ฏ, ย/ญ) are not to be
  guessed apart — crop closer or flag uncertain, never assert.
- **A student's own notation can already answer a question.** If her transcription
  convention encodes an answer (e.g. doubling a vowel letter for length), take that as the
  answer — don't mark it incomplete for not restating in prose what the notation already
  shows.

## Working on the skills themselves

The meta layer is separate from the teaching one: `skill-*` work on the instrument,
`thai-*` on Thai. Who owns what, and where a turn goes next, is in
`.codex/skills/MAP.md`; the commands are in `.codex/skills/README.md`.

- Invent a mechanic, an exercise format, the structure of a topic → `skill-brainstorm`.
- Write or rewrite a `SKILL.md`, a reference, a topic file; explain a mechanism; draw a
  diagram → `skill-writer`.
- Check what was written — your own edits, a whole skill, a script, a course file →
  `skill-review`.

**Output language is Russian, always**, even when the skill itself is written in English:
instructions are written however is convenient, but everything a human sees, and everything
that lands in an artifact, is in Russian.

**Instructions migrate to English gradually — in passing, not as a campaign.** When you are
editing a skill file for a real reason, translate it whole in the same pass; never run a
translation sweep just to save tokens. Cyrillic costs roughly twice as much as English in
tokens, yet the measurement on `checking.md` came out at only 26%: a fifth of the text has
to stay Russian, and the price of an accidental error in a tuned instruction outweighs the
gain. What is never translated — in
`skill-writer/references/skill-doc-standards.md`.

## Checks

Editing data or a script is not finished until the matching check has run. Both are offline,
stdlib only; the full command set is in `.codex/skills/README.md`.

- Touched `thai-phonetics/references/*.md`, its `data/*.json`, or a transcription in a course
  file → `python3 .codex/skills/thai-phonetics/scripts/phonetics.py check`. It catches what
  the eye does not: latin homoglyphs wearing tone marks (`â` for `а̂`), leftover macrons, and
  drift between a `SKILL.md` and `consonants.md`. `--course` also scans `Thai A2/`, `Thai B1/`
  and `Helpers/`, but reads as leads rather than a verdict — course tables use headers the
  scanner does not know yet.
- Touched a script under `.codex/skills/*/scripts/` → `npx pyright --stats` (`strict`, 3.8).
  Read the file count, not only the error count: an empty file set also reports «0 errors».
  Why `exclude` must not gain `**/.*` is in `pyrightconfig.json` — do not silence it.

## Console output

The user sees every check, script run and sandbox experiment in the terminal in full, so
the noise is the command itself, not the report. Run them quietly:

- no `echo "=== … ==="` banners, no `ls -l`, no byte counts, no before/after dumps — that
  framing is for a human, but the decision from it is yours to make, not theirs;
- silence the rest (`>/dev/null`), and take from a script the one line that carries the
  verdict;
- what goes to the chat is a **status**: what was checked and how it ended. Details only if
  the check failed or they were asked for outright.

The same principle on the teaching side: `tracker.py` output is not copied to the learner
but retold (`thai-tasks`, «Итог занятия»).

The rules in this file outrank any skill. A change that contradicts them is a high-severity
finding in `skill-review`, not a licence to rewrite the rule on the fly.
