# Проверить документ (ПД)

Loaded when the user wants a document checked against the house standard. This is the
lighter, single-document check; a full adversarial audit across skills is `skill-review`.
Say so if the request is really the latter.

Output is Russian. **Read `skill-doc-standards.md` before checking anything** — it is the
standard you check against, and it is not loaded until you get here.

## Process

### 1. Load the document in full

Plus whatever it cannot be judged without: for a `SKILL.md`, its `references/` files and the
descriptions of its sibling skills; for a `references/` file, its parent `SKILL.md`; for a
course file, the chapter plan and a neighbouring topic file.

### 2. Check against the standard

Work through these in order. The first three are where real defects cluster.

**Trigger contract** (`SKILL.md` only)
- Does `description` name concrete Russian user phrasings, or only abstract categories?
- Does it say when **not** to use the skill, and name the sibling that should fire instead?
- Write five user phrasings on the boundary with the nearest sibling skill. For how many is
  the correct skill genuinely unambiguous? Anything less than five is a finding.

**Executability**
- Any requirement without a criterion («качественно», «естественно», «интересно»)?
- Any format rule without an example block?
- Any reference pointer without a "when to read it"?
- Any hedge («обычно», «по возможности», «желательно») in normative text?
- Any named file, script, command or skill that does not exist? Check, don't assume.

**Consistency**
- Does the summary in `SKILL.md` contradict the full version in `references/`?
- Does anything contradict `AGENTS.md`? That outranks the document.
- Does it duplicate a mechanic that already lives in another skill — creating two copies
  that will diverge at the next edit?

**Structure**
- Preflight section present and ordered? Checklist at the end?
- Is anything long and branch-specific still sitting in `SKILL.md` instead of `references/`?
- Is anything essential to the trigger decision hidden in `references/`, where it is loaded
  too late to matter?

**Prose**
- Lines wrapped ~90 chars, real Markdown lists and tables, Russian throughout the
  human-facing text?
- Rule-then-reason, one idea per bullet?

**Learner-facing leakage**
- Would any part of this reach the learner's page carrying methodology — spiral percentages,
  mastery, difficulty numbers, skill names, source citations?

**Thai correctness** (course files and any document quoting Thai)
- Transcription Cyrillic only? Tone mark over the vowel?
- Is any tone, spelling or meaning asserted without a source? Flag it as needing
  verification rather than confirming it from memory.

### 3. Report

A prioritized list, in Russian, most severe first. Each item:

- **what is wrong** — one line;
- **where** — file and line or section heading;
- **why it matters** — the consequence, concretely («модель прочитает это двумя способами и
  в разных прогонах выдаст разное»), not «это неясно»;
- **the fix** — the replacement wording, when it is unambiguous.

Severity, same scale as `skill-review`: `высокая` if a lesson goes wrong or a `AGENTS.md`
rule is broken; `средняя` if behaviour degrades or varies between runs; `низкая` for wording
and formatting.

End with the count and an offer: apply the unambiguous fixes now, or leave them as a list.

## Output

A prioritized list of specific, actionable findings — and nothing else. No praise section,
no summary of what the document does well unless she asks.
