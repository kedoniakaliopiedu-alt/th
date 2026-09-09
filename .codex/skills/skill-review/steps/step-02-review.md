---
failed_layers: ''  # set at runtime: comma-separated names of layers that failed or returned empty
---

# Step 2: review

## RULES

- Speak Russian to the user.
- All review subagents must run at the same model capability as the current session.
- Run subagents synchronously: launch them together, then wait for all results before
  continuing.

## INSTRUCTIONS

1. Load `../references/review-layers.md`. It defines the layers, their `when` conditions,
   and each one's full instruction.

2. For each layer, decide whether it is active:
   - empty instruction → drop it silently (it was deliberately disabled);
   - `when` condition present and not satisfied by the current context (`{scope}`,
     `{review_mode}`, what file types the material actually contains) → drop it and tell the
     user, e.g. «Ревьюер скриптов пропущен — скриптов в изменениях нет.»;
   - otherwise → active.

   If no layer is active, HALT with the blocking condition «нет активных слоёв ревью».

3. **Give each layer only its own slice.** A layer that cannot act on a file gains nothing
   from receiving it, and every extra file is paid again in that layer's context. Narrow
   `{paths}` per layer before launching — the `when` conditions already say who cares about
   what:

   | Layer | Gets |
   |---|---|
   | `ревьюер-скриптов` | only `*.py`, `*.swift` and shell scripts from `{paths}` |
   | `методический-аудитор` | only `thai-*` skill files and `Thai A2/` · `Thai B1/` · `Helpers/` material |
   | `границы-скиллов` | the `SKILL.md` of every skill in `{paths}` (it reads `MAP.md` and `AGENTS.md` itself) |
   | all others | the whole of `{paths}` |

   When `{scope}` = `diff` there is nothing to narrow: pass `{diff}` whole to every layer.

4. Run all active layers **in parallel**: substitute `{material}` — the `{diff}` text, or that
   layer's slice of `{paths}` — plus `{intent_file}` and `{target}` into the layer's
   instruction, then launch one subagent per layer with no prior conversation context,
   following the instruction verbatim. A layer given paths reads those files itself — do not
   read them here.

   **If subagents are unavailable**, write each active layer's fully-substituted prompt to
   `.codex/reviews/промпты/<layer-id>.md` and HALT. Ask the user to run each in a separate
   session — ideally in a different model — and paste the findings back. When findings are
   pasted, treat them as those layers' output and resume from this point.

5. **Layer failure handling.** If a layer fails, times out, or returns nothing, append its
   name to `{failed_layers}` (comma-separated) and proceed with the remaining layers. Do not
   silently retry a layer more than once.

6. Collect all findings, keeping track of which layer `id` produced each one.

## What not to do here

- **Do not judge yet.** This step gathers; step 3 decides. Resist the pull to dismiss a
  finding while reading it — a layer that looks wrong from here is often right once the
  surrounding file is read, and that reading happens in triage.
- **Do not merge findings yet.** Deduplication is step 3's job and depends on the full set.
- **Do not fix anything.** No file is modified before step 4, and then only with the user's
  explicit choice.

## NEXT

Read fully and follow `./step-03-triage.md`.
