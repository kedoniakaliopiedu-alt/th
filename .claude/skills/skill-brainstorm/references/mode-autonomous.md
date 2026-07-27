# Stance: Ideate for me (`Придумай за меня`)

The user handed you the topic and wants to see what you come up with on your own, then look
at the result. You become the brainstormer — this is the one stance where the ideas are
yours to generate.

- **Run a real divergent session yourself.** If the user supplied techniques (a composed
  paste from the selector page), honor those first; otherwise pick and run techniques on
  your own via `brain.py` — *you* choose, no menu for the user. Capture each idea to the
  memlog with `--type idea --by coach`, mark each technique switch with a `technique`
  entry, shift the creative domain every ~10 ideas, aim past 100. Push past the obvious.
- **Don't pepper the user with questions** — this is your run. One quick confirm of topic
  and goal up front is plenty.
- **Ground yourself before you generate.** Read what the topic actually touches: the target
  skill's `SKILL.md` and its `references/`, the relevant course file under `Thai A2/` or
  `Thai B1/`, and the mistake patterns in `progress.json` (via
  `.claude/skills/thai-tasks/scripts/tracker.py progress progress.json`). A hundred ideas
  invented against a wrong picture of the instrument are a hundred wasted ideas.
- **When it's mined out, synthesize and produce the keepsake.** Go to `## Wrap-up`
  (`references/finalize.md`): record the insights, log `(event) сессия завершена`, and
  **auto-generate the HTML keepsake — don't ask first; it is the result you promised to
  show them.** Offer the other artifacts after.
- **Then offer to keep going together.** They may want to push an idea further or react to
  what you found — if so, switch into Facilitator or Creative Partner (load that frame),
  **record the switch in the memlog** (`memlog.py set --workspace {W} --key mode --value
  <фасилитатор|со-творец>`), and continue from the same log.

Everything you write for the user — and every memlog entry — is in Russian.
