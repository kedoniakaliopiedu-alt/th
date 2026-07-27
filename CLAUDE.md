# Project Thailand — working rules

A repository for learning Thai: lesson material (`Thai A2/`, `Thai B1/`, `Helpers/`), the
progress tracker (`progress.json`) and the tutor skills in `.claude/skills/` (overview —
`.claude/skills/README.md`).

Instructions here are in English; **everything the user reads is in Russian** (see «Working
on the skills themselves»).

## Images

**An image arrived — the very first thing to invoke is the `thai-handwriting` skill.** No
exceptions: a photo of a notebook, a screenshot, a sign, a textbook page, a frame from a
whiteboard. This holds even when the message carries no text at all, or when the request
sounds like «переведи» / «проверь» / «что тут написано».

Reading Thai off an image by eye, bypassing the skill's pipeline, is forbidden: a whole page
is recognized markedly worse than one sliced into lines, and an unflagged guess breaks the
learning loop — the review then runs on a misread word.

**The command «clean photo»** (even with no image in the message) → clear the `Handwriting/`
folder with `.claude/skills/thai-handwriting/scripts/clean`. Details are in the
`thai-handwriting` skill.

## Thai

- Tasks, drills, practice → `thai-tasks` (it pulls in the rest itself).
- **Answers checked — go straight to `thai-mistakes`**: a report over the sheet
  (✅ / 🟡 / ❌ + the correct version) and drilling the mistakes as a whole topic. Do not
  substitute an ad-hoc review of your own.
- Transcription is Cyrillic only, per `thai-phonetics`.
- Tones are verified against an authoritative source before any verdict, never from memory.
- Progress and mistakes are written to `progress.json` through
  `.claude/skills/thai-tasks/scripts/tracker.py`.

## Working on the skills themselves

The meta layer is separate from the teaching one: `skill-*` work on the instrument,
`thai-*` on Thai.

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
