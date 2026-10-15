---
name: skill-writer
description: >
  Project-specific guidance for writing or revising Codex skills, references, and Thai
  course materials. Use when asked to edit a SKILL.md, project documentation, or a course
  topic. For learner exercises use thai-tasks; for answer checking use thai-mistakes; for an
  adversarial audit use skill-review.
---

# Writing project documents

This is a short project checklist, not a required prose style or a separate writing workflow.
Codex can make ordinary edits directly; use these rules to preserve project-specific
boundaries.

## Before editing

1. Read `AGENTS.md` and `.codex/skills/MAP.md`.
2. Read the target and only the connected files needed to understand its links, behavior, or
   format.
3. Ask the user only if a substantive decision is genuinely unresolved; do not invent course
   content or settle a design choice silently.

## Project contracts

- Keep all learner-facing text in Russian.
- For Thai spelling and transcription, follow `thai-phonetics`; verify tones through
  `thai-verify` and the sources assigned in `RESOURCES.md`.
- For a new or substantially revised course topic, follow
  `.codex/skills/content-sources.md` and
  `.codex/skills/thai-tasks/references/topic-materials.md`.
- For course artifact paths, names, and links, follow
  `.codex/skills/assessment-artifacts.md`.
- Prefer clear, concise, task-focused instructions. There is no mandatory outline, line
  width, checklist, or house prose style for every skill or document.
- Update `MAP.md`, `.codex/skills/README.md`, or `AGENTS.md` only when the change affects
  routing, shared contracts, or operator guidance.
- For exercises, grading, and error review, use `thai-tasks` and `thai-mistakes`; do not
  replace their workflows with a course document.

After editing, check links and references that the change affected. Run the project check
required by `AGENTS.md` when changing Thai transcription or a skill script.
