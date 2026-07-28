---
name: skill-review
description: >
  Adversarial review of this repository's own skills and course material — parallel
  review layers plus structured triage. Reviews SKILL.md files, their references/,
  the scripts under .claude/skills/*/scripts/ and the lesson files under Thai A2/ and
  Thai B1/. Use when the user asks to review, audit or check the instrument itself:
  «отревьюй скилл», «проверь, что я написала в SKILL.md», «разбери мои правки»,
  «аудит thai-tasks», «что не так с этим скиллом». Do NOT use to check the
  learner's answers to exercises — that is thai-mistakes.
---

# Skill Review — adversarial review of the instrument

**Goal:** review changes to this repository's skills and material adversarially. No noise,
no filler.

**Output language: Russian.** Every message to the user, every finding, every file this
workflow writes is in Russian, regardless of the language of these instructions.

Subagents are an important part of this workflow — the review layers are designed to run
blind and in parallel. If you need explicit user permission to run them, **ask once now for
the whole run**. If subagents are unavailable, `steps/step-02-review.md` explains the
fallback.

## Path conventions

- `{S}` = `.claude/skills/skill-review` — the skill root.
- `{diff}` — the material under review, built in step 1.
- `{report}` = `.claude/reviews/ревью-{цель}-{ГГГГ-ММ-ДД}.md` — where findings land.
- `{deferred}` = `.claude/reviews/отложено.md` — the running list of parked findings.

## Workflow architecture

This uses **step-file architecture** for disciplined execution:

- **Micro-file design** — each step is self-contained and followed exactly.
- **Just-in-time loading** — load only the current step file.
- **Sequential enforcement** — complete steps in order, no skipping.
- **State tracking** — persist progress in in-memory variables declared in each step's
  frontmatter.

### Step processing rules

1. **READ COMPLETELY** — read the entire step file before acting.
2. **FOLLOW SEQUENCE** — execute sections in order.
3. **WAIT FOR INPUT** — halt at checkpoints and wait for the user.
4. **LOAD NEXT** — when directed, read the next step file fully and follow it.

### Critical rules (no exceptions)

- **NEVER** load multiple step files at once.
- **ALWAYS** read the whole step file before executing it.
- **NEVER** skip steps or optimize the sequence.
- **ALWAYS** halt at checkpoints and wait for the user.

## On activation

1. Ask for subagent permission once, as described above.
2. Load `.claude/skills/README.md` — the map of skills, what each owns, and how they hand
   off to each other. Carry it as a fact for the whole run: most severe findings in this
   repository are boundary violations between skills, and you cannot see them without the
   map.
3. Load `CLAUDE.md` — the project's non-negotiable rules (images always go through
   `thai-handwriting`; Cyrillic-only transcription; tones verified against an authoritative
   source; progress written through `tracker.py`). A change that contradicts `CLAUDE.md` is
   a `high` finding by definition.
4. Greet the user in Russian and state what the review will cover.

## First step

Read fully and follow: `steps/step-01-gather-context.md`.

Adapted from bmad-code-review (BMAD Method, MIT) — see `ATTRIBUTION.md`.
