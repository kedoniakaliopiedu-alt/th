# Converging: narrow & decide

Load this when divergence is spent and the user wants to narrow the field — or asks to
«решить», «расставить приоритеты», «выбрать», «сделать это настоящим». The whole catalog is
*divergent* by design; this is the deliberate opposite phase, and keeping the two apart is
the point. Never run convergence while ideas are still flowing, and never let it leak into
a generating batch — premature judgment is what kills good ideas.

`{W}/.memlog.md` is the canonical record; everything here works from it. Communicate in
Russian.

**Stance holds.** In **Facilitator** you run the convergence *on the user's verdicts* — you
structure and prompt, she judges; never rank for her. In **Creative Partner** you weigh in
too, each call logged by author. In **Ideate for me** you converge yourself and show the
result, then offer to keep going.

## How to run it

First, reflect the field back: pull the live candidates from the memlog (include the odd
and buried ones, not just the recent obvious ones) so there's a concrete set to work on.
Then pick **one** convergence move that fits the goal — don't hand the user a menu of
methods; choose the one that suits *this* decision and name it. Run it to a result, log the
outcome, and stop when a clear short-list or single direction emerges.

Pick by what the decision needs:

- **Кластеризация по смыслу** — many scattered ideas: group them into themes, name each
  cluster, surface the through-line. Often the right *first* move, to turn a pile into a
  handful.
- **Польза / трудоёмкость** — when the goal is action: place each candidate on impact vs
  effort; harvest high-impact / low-effort first, park the rest.
- **Новизна / польза / выполнимость** — when novelty matters: score each 1–10 on new,
  useful, feasible; the totals expose the quiet winners and the dazzling-but-doomed.
- **Жёсткое ранжирование** — when you just need a ranked top-N: make the ideas compete, no
  ties.
- **Плюс / минус / интересно** — when one strong candidate needs pressure-testing before
  commitment.
- **MoSCoW** — when scoping a build: Must / Should / Could / Won't-this-time.

Two or three moves chained is fine (e.g. cluster → score the clusters); more than that is
usually over-processing.

Log the surviving directions and the reasoning:

```bash
python3 .claude/skills/skill-brainstorm/scripts/memlog.py append --workspace {W} \
  --type decision --text "<суть одной строкой>"
```

(add `--by` in Creative Partner mode).

## A filter this project earns the right to apply

Before a direction is declared a winner, it has to survive three questions specific to this
repository. Ask them out loud; they belong to the user's judgment, not yours:

1. **Куда это ляжет?** Which skill owns it — `thai-tasks`, `thai-mistakes`, the tracker, a
   `references/` file? An idea nobody owns quietly never ships.
2. **Что оно вытесняет?** The instrument is already dense. If a mechanic is added, what gets
   simpler or gets deleted? An honest "ничего" is allowed once, not routinely.
3. **Как узнаем, что сработало?** A visible signal — accuracy in `progress.json`, a mistake
   pattern that stops recurring, a worksheet that stops needing manual fixes. No signal
   means it can never be judged later.

Candidates that pass go into the short-list; the rest are logged as `decision` with the
reason they were parked, so a future session doesn't re-invent them.

## Then finalize

Once a short-list or direction is settled, **load `references/finalize.md`** and run it last
— synthesis and artifacts build on the decisions you just logged. Convergence narrows;
finalize captures and ships. Do not log `(event) сессия завершена` here — that belongs to
finalize.
