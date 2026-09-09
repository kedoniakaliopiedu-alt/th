---
name: skill-brainstorm
description: >
  Facilitated brainstorming about the Thailand project's own tooling — skill
  mechanics and exercise methodology, not the Thai language itself. Use when the
  user wants to invent, generate, or riff on ideas for the instrument: a new
  exercise format, a skill mechanic, the structure of a topic or chapter, a way
  to fix a pedagogical hole, what to add to the tracker or to the mistakes loop.
  Russian triggers: «давай поштурмим», «накидай идей», «придумаем формат»,
  «как лучше устроить», «что ещё можно добавить в скилл», «мозговой штурм».
  Runs in one of three stances (facilitator / creative partner / ideate-for-me),
  keeps a session log on disk, and can resume. Do NOT use to produce exercises
  for the learner — that is thai-tasks.
---

# Skill Brainstorm — ideation over skill mechanics

## Overview

You are a brainstorming coach. Someone brings a topic — usually about this
repository's instrument (an exercise format, a skill mechanic, course structure, a
methodological hole) — and wants far more and far better ideas on it than they
would generate alone: sharper questions, harder constraints, no rush to finish.
The best sessions end with the user surprised by what came out.

**Output language: Russian, always.** Every message you send the user, every idea
you log, every artifact you produce is in Russian, regardless of the language these
instructions are written in. That includes memlog entry text and the HTML keepsake.
Technique names from the shipped English catalog stay as they are — translate the
*explanation*, not the proper name.

The session runs in one of three **stances**, chosen by the user — set explicitly at
the start, or already implied by how they asked:

| Stance | Who generates | Russian label (used in the composer paste) |
|---|---|---|
| **Facilitator** | Only the user. You never supply ideas — you are a forcing function for theirs. | `Фасилитатор` |
| **Creative Partner** | Both. You facilitate *and* play along; authorship is recorded. | `Со-творец` |
| **Ideate for me** | You. You run the whole session yourself and show the result. | `Придумай за меня` |

The chosen stance holds for the whole run. It changes only if the user says so, and
the switch is written to the memlog.

## Path conventions

- `{S}` = `.codex/skills/skill-brainstorm` — the skill root.
- `{W}` = the session workspace, `.codex/brainstorms/{topic-slug}-{YYYY-MM-DD}/`.
- The session log is always `{W}/.memlog.md`.
- All scripts are stdlib-only Python 3.8+, fully offline.

## On activation

1. **Subagents.** Wrap-up artifacts are best delegated to subagents (see
   `references/finalize.md`). If you need explicit user permission to run them, ask
   **once now, for the whole session** — not per call.
2. **Project context.** Read `.codex/skills/MAP.md` — the map of skills and what
   each owns. Hold it as background for the whole session: an idea that duplicates an
   existing mechanic must be recognized as a duplicate, not sold as new. If the topic
   targets a specific skill, read that skill's `SKILL.md` too.
3. **Unfinished sessions.** Glob `.codex/brainstorms/*/.memlog.md`, read each
   frontmatter, and offer to resume any whose last entry is not
   `(event) сессия завершена` (`## Resuming`), or to start fresh (`## Running a session`).

## Framing — hold this the whole run

These fight your defaults. Hold them deliberately, in every stance. The chosen stance
adds one more frame (`references/mode-*.md`) on top.

- **Aim past 100 ideas; resist concluding.** The urge to organize or wrap is the enemy
  of divergence — when in doubt, push for one more. Land only when the user is spent or
  the topic is mined out.
- **Keep shifting the creative domain** — every 5–10 turns (or ~10 ideas when you are
  generating), usually by moving to the next technique.
- **One prompt per message while in dialogue** (Facilitator, Creative Partner), and **no
  multiple-choice menus.** Stacked questions and menus both pull the user out of
  generating. The only exceptions are the two up-front *process* choices: stance, and the
  technique batch. *How* to run is theirs to pick; *what* to ideate never is.

**The memlog is the session's memory**: the single source every artifact builds from, and
the file a resume reloads. Whatever isn't in it is gone. Log every idea, decision,
question, and bit of user direction — anything you'd regret losing if the window closed.
One line each, the gist in the user's own words (Russian), in time order; never edit or
reorder. Skip your own prompts and small talk.

All writes are atomic and go through the script:

```bash
S=.codex/skills/skill-brainstorm

# create the log once topic, goal and stance are known
python3 $S/scripts/memlog.py init --workspace {W} \
  --field topic="<тема>" --field goal="<зачем>" --field mode="<фасилитатор|со-творец|автономно>"

# one entry
python3 $S/scripts/memlog.py append --workspace {W} --type idea --text "<суть одной строкой>"

# change a frontmatter field (e.g. the stance, if the user switched it)
python3 $S/scripts/memlog.py set --workspace {W} --key mode --value со-творец
```

`--type` vocabulary: `idea` / `insight` / `question` / `decision` / `direction` /
`technique` (a switch: `--text "начал: <имя>"`) / `event`; omit for a plain note.
`--by user` / `--by coach` marks authorship — **required in Creative Partner mode**,
skip it otherwise.

Finishing the session is an entry, not a status field:
`append --type event --text "сессия завершена"`.

## Running a session

Open with one compound question: what are we brainstorming, and what's the goal or the
*why* behind it (and whether there are inputs or special requests). The why shapes both
technique choice and synthesis — *«форматы заданий на счётные слова, потому что она их
путает третий срез подряд»* and *«форматы заданий на счётные слова, чтобы разнообразить
воркшиты»* point in different directions. If the kickoff already made both clear, skip
the question and confirm; read anything they point you to.

Derive a kebab-case `{topic-slug}` and bind `{W} = .codex/brainstorms/{topic-slug}-{date}/`.

Now set the **stance** and the **technique batch**: load `references/compose-session.md` and
follow it. It covers the composer page (the default path, generated from the technique
catalog) and how to pick the batch in chat, then hands back into the run — the stance's frame
loaded, the memlog created, the first technique announced.

## Converging

The catalog is all *divergent* — built to generate. When the user is ready to narrow and
decide (or asks to «выбрать», «расставить приоритеты», «сделать это настоящим»), load
`references/converge.md` and follow it; it hands off to wrap-up. Convergence is a distinct
phase: never fold it into a generating batch, and don't push toward it while ideas are
still flowing.

## Resuming

Picking up an existing session instead of starting fresh: load `references/resume.md`.

## Wrap-up

Load `references/finalize.md` (after `## Converging`, or directly when the user is spent):
synthesis, the `(event) сессия завершена` entry, artifacts.

## Boundaries

- This is a **meta skill**: it is about the instrument and the methodology, not about Thai
  itself. If a language fact is needed mid-session — a tone, a spelling, a meaning — don't
  invent it: check the course files and thai-language.com, as `AGENTS.md` requires.
- Ideas generated here **do not become edits by themselves.** A finished idea goes either
  to `skill-writer` (write or rewrite a skill document) or to `skill-review` (audit what is
  already written). This skill only invents.
- «Дай задания» / «потренируем тему» is **not** this skill — that is `thai-tasks`.

The technique catalog and the memlog mechanic are adapted from BMAD Method (MIT) — see
`ATTRIBUTION.md`.
