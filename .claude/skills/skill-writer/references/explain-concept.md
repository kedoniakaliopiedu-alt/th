# Объяснить механизм (ОК)

Loaded when the user wants to *understand* how something in the instrument works — «объясни,
как устроена спираль», «почему thai-mistakes спрашивает самооценку до вердикта», «что делает
tracker.py при record», «как связаны эти скиллы». The deliverable is understanding, not a
file.

Output is Russian.

## What separates this from just answering

The answer must come from **what the code and the documents actually say**, not from what a
system like this usually does. Two rules:

- **Read before explaining.** Open the `SKILL.md`, the `references/` file, the script. This
  repository's mechanics are specific — SM-2 with a mistake database layered on top, a 60/40
  spiral woven into new-topic exercises rather than run as a separate block, a two-round
  drill closure criterion. A generic explanation of spaced repetition would be true and
  useless.
- **Name the file, with its full path.** Every claim should be traceable to a place she can
  open: `.claude/skills/thai-tasks/references/progress-and-spiral.md` says X;
  `.claude/skills/thai-tasks/scripts/tracker.py` implements Y. A bare `references/…` is
  ambiguous — seven skills have one.

If the documents and the script disagree, that is the most valuable thing you can report.
Say so plainly and offer to route it to `skill-review`.

## Process

1. **Locate the mechanism** — which skill owns it, which reference file holds the full
   version, which script implements it. `.claude/skills/MAP.md` is the map.
2. **Read all three layers** where they exist: the summary in `SKILL.md`, the detail in
   `references/`, the implementation in `scripts/`. The interesting part is usually where
   they differ in emphasis.
3. **Explain by the reason, then the mechanism.** Start with the problem the mechanism
   exists to solve — «самооценка спрашивается до вердикта, потому что уверенная ошибка и
   угаданное попадание требуют разного обращения» — then how it does it. Depth follows what
   she asked; do not lecture past the question.
4. **Show, where showing beats telling.** A short worked example — one item going through
   `record` with quality 3 vs quality 5 — lands better than a paragraph about easiness
   factors. A diagram beats prose for anything with more than three moving parts: switch to
   `mermaid-gen.md`.
5. **Close the loop.** End by naming what she can now do that she couldn't: change the
   parameter, spot the failure, decide whether to keep the mechanic.

## Boundaries

- This explains **the instrument**. A question about the Thai language itself — why a tone
  behaves that way, what a particle does — is `thai-learning` or `thai-tasks`, not this.
- Do not use it as a back door into redesigning the mechanism. If the explanation reveals
  that it should work differently, say so and hand off to `skill-brainstorm`.

## Output

A conversational explanation, in Russian, with file references she can open. No document is
written unless she asks for one — and then it goes through `write-document.md`.
