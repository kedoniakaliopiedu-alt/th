# Wrap-up: synthesis & artifacts

Load this when the user signals she's spent or the topic is mined out. `{W}/.memlog.md` is
the canonical record of the session — everything here derives from it. Communicate and
write every artifact in Russian.

## Synthesis

In Facilitator mode this is the one place your own creative contribution is welcome; in
Creative Partner and Ideate-for-me you've been contributing all along, so just keep going.
Run it in two moves, in order:

1. **Hand her the mirror first.** Reflect a vivid sampling of *her* ideas back —
   deliberately including the odd, random or buried ones from earlier, not just the recent
   obvious ones (in Creative Partner mode the `(... by user)` tags tell you which were
   hers). Ask what she sees now: conclusions, synergies, themes, the few that actually
   matter. Let her connect first; her own pattern-recognition is the point.
2. **Then add the connections she would miss.** Not new raw ideas — the non-obvious links:
   this idea from technique one quietly solves that tension from technique four; these three
   are one idea wearing three hats; this wildcard is the real breakthrough.

Record the insights and chosen directions, then close the log:

```bash
S=.claude/skills/skill-brainstorm
python3 $S/scripts/memlog.py append --workspace {W} --type insight --text "<инсайты + выбранные направления>"
python3 $S/scripts/memlog.py append --workspace {W} --type event   --text "сессия завершена"
```

Log the closing entry **even if she declines every artifact below** — otherwise the session
keeps being offered for resume.

## Artifacts

In **Ideate for me**, the HTML keepsake is the deliverable you promised — produce it
automatically, no asking; the others stay opt-in. In **Facilitator** and **Creative
Partner**, every artifact is opt-in: each is a fresh, token-expensive generation, so ask
what she wants, recommend the keepsake as the default, and generate only what she picks.
Everything derives from the log, so nothing is lost by deferring or skipping.

**Delegate each artifact to a subagent** (if permission was granted at activation). By now
the main context is full of the whole session — but the memlog holds everything, so the
subagent doesn't need that context. Spawn one per requested artifact, telling it only: the
spec below, the memlog path `{W}/.memlog.md` as its sole source (read it in full), the
output path, "всё содержимое пиши по-русски", and "return ONLY the written file path".

- **HTML-страница сессии (recommended default).** A single self-contained `brainstorm.html`
  in `{W}` — a genuine creative artifact, not a report poured into a template. There is no
  template on purpose: let *this* session's subject and energy drive the visual language.
  Give each technique its own treatment, invent visualizations that fit the ideas, render
  the synthesis as the climax. Inline all CSS and JS; no external dependencies. Open it once
  complete.
- **Лист правок (`изменения.md`).** The project-specific artifact and usually the most
  useful one: the short-list turned into concrete work, grouped by target file — which
  `SKILL.md` or `references/*.md` changes, what the change is in one sentence, and what
  signal will show it worked. This is the file `skill-writer` picks up to actually write the
  edits, and `skill-review` uses to check them afterwards. Keep it tight; no session bloat.
- **Новые техники.** If the session used invented techniques and one is worth keeping, offer
  to append it to `{S}/assets/extra-techniques.json` (same shape as the existing entries:
  `category`, `technique_name`, `description`, `provenance`, `good_for`, `audience`), then
  regenerate the composer page:
  `python3 $S/scripts/brain.py --extra $S/assets/extra-techniques.json html --out $S/assets/brain-selector.html`
- **Anything else the context suggests** — a checklist, a topic plan, a one-pager — produced
  from the same source. Offer real options based on what she seemed to need, and ask if she
  wants something you haven't thought of.

## Handing off

After producing what she chose, tell her the artifact paths and name the next step
explicitly, since this skill deliberately doesn't make edits itself:

- ready-to-write changes → **`skill-writer`** (`«давай напишем правки из листа»`);
- changes already written and needing an audit → **`skill-review`**;
- an idea that turned out to need more divergence → offer a fresh session on the narrower
  topic, and name it.

## Cleaning up afterwards

The workspace exists to carry a session across interruptions and into the next skill. Once
the ideas have landed as code or documents, it stops being a resource and becomes debris —
and `изменения.md` becomes actively harmful: `skill-review`'s step 1 globs
`.claude/brainstorms/*/изменения.md` and will propose reviewing work that is already done.

So when the user comes back and says the changes are written — or you can see the edits in
the repository yourself — **offer to remove the workspace**, naming what dies with it:

> Правки из листа внесены. Журнал сессии и лист правок больше ни на что не влияют, а лист
> вдобавок будет всплывать в ревью как незакрытая работа. Удалить папку
> `.claude/brainstorms/<тема>-<дата>/`? Если она закоммичена, всё достаётся обратно из
> истории: `git show <sha>:<путь>`.

Rules for that offer:

- **Offer, never delete on your own.** The keepsake is hers; she may want to keep it.
- **Only after the ideas have landed.** A session whose changes nobody wrote yet still needs
  its log — that is exactly what a resume reads.
- **Say what is recoverable.** Committed artifacts come back from git; uncommitted ones do
  not, and she should know which case she is in before answering.
- If she keeps it, do not ask again in the same session.
