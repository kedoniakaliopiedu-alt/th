# Skill map — zones and hand-offs

What each skill owns and where the turn goes next. This is the file the meta skills load;
the operator's handbook (tracker commands, OCR toolchain, pyright, usage) is `README.md`.

Names in Russian quotes — statuses, section headings, category values — are literals the code
or the parser matches on; never translated.

Two layers. **Teaching** (`thai-*`, `learn`) runs the lesson. **Meta** (`skill-*`)
services the instrument itself. The teaching layer is about Thai, the meta layer about the
repository; do not mix them up — every meta skill states in its `description` what it is
**not**.

`assessment-artifacts.md` is the shared filesystem contract for topics, controls, reports,
practice ecosystems, names and relative links. It does not own teaching, grading, report
content or remediation choice; the skills below link to it instead of repeating those rules.

`content-sources.md` is the shared evidence contract for course authoring: source roles,
register separation, corpus-to-example workflow and rights. It validates lesson content but
does not enlarge the taught scope of a control.

## Teaching layer

| Skill | Role |
|---|---|
| **thai-tasks** | The engine for fresh tasks and teaching material. It owns the tracker implementation (SM-2), the 60/40 spiral, the three modes (session / worksheet / test), topic states and the closing sheet. Chapter controls default to a static dark HTML file for handwritten answers (`thai-tasks/references/written-control.md`). Its `topic-materials.md` supplies shared self-study presentation rules but does not choose remediation content. |
| **thai-mistakes** | The second beat after formal checking, or a direct review of explicitly named prior errors/tracker history: calibration before an unrevealed verdict, the report over the sheet (✅/🟡/❌), the single tracker write for that result, then route each gap by cause. It owns remediation scope and content. Rules and broad gaps receive thematic modules; repeatedly forgotten exact words receive compact lexeme-memory modules. |
| **thai-learning** | Rules for presenting tasks and checking answers, level structure, tests. |
| **thai-phonetics** | The single source of transcription. `SKILL.md` holds the assembly order (syllables → initial/cluster → silent letters → vowel → final → tone, verified); five data files hold the rest: `consonants.md`, `vowels.md`, `clusters.md`, `silent-letters.md`, `irregulars.md`. A sign with no data is reported missing, never approximated. |
| **thai-verify** | Checking a word against thai-language.com: how to query, how to pick the right entry among several, how their tone letters map onto ours. Owns the truth; `thai-phonetics` owns how the truth is written down. |
| **thai-handwriting** | Reading Thai off the photos in `Handwriting/`, handwriting above all. Fires on today's files in that folder — not on any image in the message. |
| **learn** | Base pedagogy: diagnose, one step per turn, a hint instead of a ready answer. |

## Working on the instrument

| Skill | Role |
|---|---|
| **skill-review** | Adversarial review of skills, references, scripts and course files. Writes nothing without an explicit choice. |
| **skill-writer** | Project-specific guidance for authoring skills, references and course materials. |

Discuss ideas directly with Codex; use `skill-writer` when editing project documents and
`skill-review` when an adversarial audit is wanted.

## Teaching hand-offs

The teaching entry points and what each relies on:

```
thai-tasks        ← tasks, drills, practice are asked for
├── learn            — pedagogy of the dialogue
├── thai-learning    — rules of presenting and checking
├── thai-phonetics   — transcription and tones
│   └── thai-verify  — the dictionary behind every tone
        │
        ↓ answers checked — hands the turn over
        │
thai-mistakes     ← answers checked; or a direct «разбери ошибки»
├── thai-tasks       — tracker, task catalog, generation rules
├── thai-learning    — checking rules
└── thai-phonetics   — transcription

thai-handwriting  ← `Handwriting/` holds files dated today (an image in the message is not a trigger)
├── thai-phonetics   — transcription of what was read
├── thai-learning    — reviewing language errors in handwritten work
└── thai-tasks       — tracker: record a recurring handwriting defect
```

The `tasks → mistakes` arrow is a handover, not subordination: feedback is the stronger half,
and `thai-mistakes` borrows the tracker, the task catalog and the generation rules from the
engine. The boundary between them is **the moment of the verdict**, and closing a topic is cut
along the same line: the engine keeps topic states, assembles the closing sheet and sets its
properties (share of production, the trap, the forecast before the first task); the mistakes
workflow checks, reports and records the outcome with `close`.

Ideas and design trade-offs are discussed in the conversation, not stored in a dedicated
brainstorm workflow. Existing files in `.codex/brainstorms/` are historical records.
