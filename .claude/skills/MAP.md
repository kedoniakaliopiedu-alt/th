# Skill map — zones and hand-offs

What each skill owns and where the turn goes next. This is the file the meta skills load;
the operator's handbook (tracker commands, OCR toolchain, pyright, usage) is `README.md`.

Names in Russian quotes — statuses, section headings, category values — are literals the code
or the parser matches on; never translated.

Two layers. **Teaching** (`thai-*`, `learn`, `teach`) runs the lesson. **Meta** (`skill-*`)
services the instrument itself. The teaching layer is about Thai, the meta layer about the
repository; do not mix them up — every meta skill states in its `description` what it is
**not**.

## Teaching layer

| Skill | Role |
|---|---|
| **thai-tasks** | The engine. Composite tasks on any topic; owns the tracker (SM-2), the 60/40 spiral, the three modes (session / worksheet / test), topic states and the closing sheet. |
| **thai-mistakes** | The lesson's second beat: calibration before the verdict, the report over the sheet (✅/🟡/❌), mistakes into the tracker, drilling a whole topic in the mode matching the mistake type, the two-round rule. |
| **thai-learning** | Rules for presenting tasks and checking answers, level structure, tests. |
| **thai-phonetics** | The single source of transcription. `SKILL.md` holds the assembly order (syllables → initial/cluster → silent letters → vowel → final → tone, verified); five data files hold the rest: `consonants.md`, `vowels.md`, `clusters.md`, `silent-letters.md`, `irregulars.md`. A sign with no data is reported missing, never approximated. |
| **thai-verify** | Checking a word against thai-language.com: how to query, how to pick the right entry among several, how their tone letters map onto ours. Owns the truth; `thai-phonetics` owns how the truth is written down. |
| **thai-display** | Word styling by consonant class. Optional. |
| **thai-handwriting** | Reading Thai off the photos in `Handwriting/`, handwriting above all. Fires on today's files in that folder — not on any image in the message. |
| **learn** | Base pedagogy: diagnose, one step per turn, a hint instead of a ready answer. |
| **teach** | Learning space: mission, learning-records, resources, glossary. |

## Meta layer

| Skill | Role |
|---|---|
| **skill-brainstorm** | Ideation over skill mechanics and exercise formats. Invents; edits nothing. |
| **skill-review** | Adversarial review of skills, references, scripts and course files. Writes nothing without an explicit choice. |
| **skill-writer** | Technical writer: write, validate, explain, diagram. Decides nothing for the author. |
| **python-best-practices** | Vendor rule book consulted when writing or reviewing scripts. Not part of the loop. |

## How they connect

Three teaching entry points, each firing on its own trigger; below each is what it leans on.

```
thai-tasks        ← tasks, drills, practice are asked for
├── learn            — pedagogy of the dialogue
├── thai-learning    — rules of presenting and checking
├── thai-phonetics   — transcription and tones
│   └── thai-verify  — the dictionary behind every tone
└── thai-display     — styling by class (optional)
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
├── thai-display     — styling the words reviewed
└── thai-tasks       — tracker: record a recurring handwriting defect
```

The `tasks → mistakes` arrow is a handover, not subordination: feedback is the stronger half,
and `thai-mistakes` borrows the tracker, the task catalog and the generation rules from the
engine. The boundary between them is **the moment of the verdict**, and closing a topic is cut
along the same line: the engine keeps topic states, assembles the closing sheet and sets its
properties (share of production, the trap, the forecast before the first task); the mistakes
workflow checks, reports and records the outcome with `close`.

`teach` is absent from the diagram on purpose: a vendor skill locked against auto-invocation
(`disable-model-invocation: true`), rewritten for this project in
`thai-tasks/references/mission-and-records.md` — the engine goes there, not to the skill.

The meta layer is closed into its own loop and does not overlap the teaching one:

```
skill-brainstorm  ← «давай поштурмим», «накидай идей», «придумаем формат»
        │  change list (.claude/brainstorms/<тема>/изменения.md)
        ↓
skill-writer      ← «напиши скилл», «перепиши SKILL.md», «объясни, как устроено»
        │  written files
        ↓
skill-review      ← «отревьюй мои правки», «аудит thai-tasks»
        │  report (.claude/reviews/) + findings that warrant a rewrite
        └──────────→ back into brainstorm or writer
```

The loop is not mandatory: any of the three runs on its own.

The loop's artifacts — the session log, the change list, the review report — live until the
work has landed as code. After that brainstorm and review **offer to delete them**: nobody
opens a closed report, and an abandoned `изменения.md` surfaces in the next review as
unfinished work. Only by consent, only when nothing is left open; committed artifacts come
back from history (`git show <sha>:<путь>`).
