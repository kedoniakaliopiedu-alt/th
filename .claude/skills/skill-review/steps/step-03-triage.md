# Step 3: triage

## RULES

- Speak Russian to the user.
- This step still modifies nothing.

## INSTRUCTIONS

### 1. Normalize

Flatten findings from all layers into one list. Each finding gets:

- `id` — sequential integer;
- `source` — the layer `id` that produced it (e.g. `слепой-охотник`), or merged sources
  joined with `+`;
- `title` — one-line summary, Russian;
- `detail` — full description, Russian;
- `location` — file and line, or file and section heading.

### 2. Deduplicate

Merge only findings that make the **same claim** and require the **same action**. Both
conditions, not one. When merging:

- use the most specific finding as the base (prefer one with a precise location over a
  prose-only one);
- append unique detail, reasoning or locations from the others into the surviving `detail`;
- set `source` to the merged sources.

Then evaluate each remaining finding **independently**. Do not reject a finding because a
related one was rejected.

### 3. Read before rating

Before assigning severity, **open the file at each finding's location and read enough
around it to judge whether the problem is actually reachable.** In this repository that
means specifically:

- a rule that looks contradictory may be resolved by an earlier «сначала / прежде всего»
  ordering clause elsewhere in the same `SKILL.md`;
- a gap in a `SKILL.md` may be filled by its `references/` file — the top-level file is
  deliberately a summary, and a "missing detail" that lives in `references/` is not a
  finding;
- a behaviour that looks unspecified may be mandated by `CLAUDE.md` for the whole project;
- a script that looks fragile may be guarded by the caller.

Severity reflects the real consequence at a real call site, not the worst theoretical
reading. A finding you could not verify by reading is downgraded, not kept on suspicion.

### 4. Assign severity

Rate by consequence **for the learner**, since she is the ultimate consumer of everything
here. Disregard any severity a subagent suggested: the layers run under deliberate
information asymmetry and cannot see the whole picture.

- `high` — **intolerable.** A lesson goes wrong: wrong Thai reaches her as correct, a
  `CLAUDE.md` rule is broken, progress data is corrupted or lost, a mandated step can be
  skipped without anyone noticing.
- `medium` — **tolerable.** The instrument works but degrades: a worksheet comes out
  malformed, a skill fires when a sibling should have, a rule is ambiguous enough that two
  runs behave differently.
- `low` — **cosmetic or none.** Wording, formatting, tidiness.

The asymmetry is deliberate: a wrong tone presented confidently is `high` even though it is
one character, while an ugly heading is `low` even if it is on every page.

### 5. Route

Put each finding in exactly one bucket:

- **`решение`** (decision_needed) — an ambiguous choice only the user can make; the fix
  cannot be written correctly without knowing her intent. Only possible when
  `{review_mode}` = `full`.
- **`правка`** (patch) — fixable without further input; the correct fix is unambiguous.
- **`отложить`** (defer) — real, but pre-existing and not caused by this change. In a
  `skill` scope full-file audit this bucket is used sparingly: there is no "current change"
  to be outside of, so pre-existing problems are in scope by definition — defer only what is
  genuinely a separate project.
- **`шум`** (dismiss) — false positive, or already handled elsewhere.

If `{review_mode}` = `no-intent` and a finding would be `решение`, reclassify it as
`правка` (if the fix is unambiguous) or `отложить` (if not).

### 6. Drop the noise

Drop every `шум` finding. Record the count for the summary.

### 7. Report gaps honestly

- If `{failed_layers}` is non-empty, say which layers failed **before** announcing results.
- If zero findings remain **and** `{failed_layers}` is non-empty, warn that the review may
  be incomplete — do not announce a clean review.
- If zero findings remain and every layer ran: «✅ Чисто — все слои прошли без находок.»

## NEXT

Read fully and follow `./step-04-present.md`.
