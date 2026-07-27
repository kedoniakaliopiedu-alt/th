# House style for this repository's documents

The standard both `write-document.md` and `validate-doc.md` measure against. It is
descriptive, not aspirational: it is drawn from how `thai-tasks`, `thai-mistakes` and
`thai-handwriting` are actually written.

## Every document

- **Russian prose, always.** Markdown, not ASCII art frames. Real lists, real tables, real
  headings — the file is read rendered as often as raw.
- **Lines wrap around 90 characters.** Long unbroken paragraphs are hard to diff and hard to
  review; the existing files all wrap.
- **Say the thing, then the reason.** Rule first, justification after, in the same
  paragraph. The existing files do this consistently («Читать тайский с картинки на глаз
  нельзя: страница целиком распознаётся заметно хуже…»), and it is why they are short.
- **No hedging in normative text.** «обычно», «по возможности», «желательно» in a rule means
  the rule will be skipped. If it is genuinely optional, say what decides.
- **One idea per bullet.** A bullet that needs a semicolon and an «а также» is two bullets.

## SKILL.md specifically

### Frontmatter

Only two fields, `name` and `description`. `name` matches the directory name exactly.

`description` is **the trigger contract** — it is the only part the model sees before
deciding to load the skill, so it carries the whole burden of firing at the right time. It
must contain:

1. what the skill is, in one clause;
2. **when to use it**, with concrete user phrasings in quotes — real ones the user actually
   types, in Russian;
3. **when NOT to use it**, naming the sibling skill that should fire instead.

That third part is not optional here. Seven skills share one repository and several are
adjacent; without an explicit exclusion the wrong one fires. Compare `thai-tasks`
(«Не использовать для простого перевода одного слова… тогда достаточно thai-learning») and
`thai-mistakes`.

### Body

- Open with **what the skill is and what it is not**, in two or three sentences, before any
  procedure.
- Then **«С чего всегда начинать»** — the ordered preflight: what to read, what to check,
  what to resolve, before generating anything.
- Then the mechanics, in the order they are used.
- End with a **checklist** the model can run before delivering. `thai-tasks` ends with
  eleven numbered items; that checklist is what makes the skill reproducible.
- Cross-references use the arrow form the repository already uses: `→ Правила транскрипции:
  см. skill **thai-phonetics**`. Name the file when it is a `references/` file, name the
  skill when it is a skill.

### Length and progressive disclosure

`SKILL.md` is the always-loaded summary; `references/*.md` is loaded on demand. Move a
section into `references/` when it is (a) long, and (b) needed only in one branch of the
work — the checking procedure, the exercise catalogue, the output format. Leave in
`SKILL.md`: the trigger logic, the preflight, the core principles, and a one-line pointer to
each reference file with **when to read it**.

A pointer without a "when" is the common defect: `→ см. references/checking.md` tells the
model nothing about whether now is the time.

## references/*.md

- Start with one line saying **when this file gets loaded**. It is read out of context, so
  it cannot assume the reader knows why.
- No frontmatter.
- Self-contained: do not require the reader to hold `SKILL.md` in memory to follow it.
- Where the parent `SKILL.md` summarizes a rule, this file gives the full version — they
  must not contradict. When you change one, check the other in the same edit.

## Scripts

Only the Python standard library, 3.8+, fully offline — no network calls, no third-party
packages. A module docstring that states what the script is for and lists its commands; the
docstring is the interface documentation, since `--help` renders it.

## Course files (`Thai A2/**`, `Thai B1/**`, `Helpers/**`)

Naming: `glavaN_temaM_*.md` for A2, `b1_glavaN_temaM_*.md` for B1. Structure inside:
`Глава` → `Тема N.M` → `Подтема N.M.K`, each with **Словарный запас**, **Теория/конструкции**
and **Практические упражнения**.

The critical constraint: **`thai-tasks` takes vocabulary and rules from these files but
deliberately does not reuse the examples in «Практические упражнения»** — it generates fresh
ones. So write that section as *illustration of the rule*, not as a bank of exercises meant
to be served to the learner, and never put anything there that must not be reused verbatim.

Vocabulary presentation: `**тайское**` · *транскрипция* — перевод. Transcription is Cyrillic
only, per `thai-phonetics`; the tone mark sits over the **vowel**, never over a consonant.
Tone marks: ` (низкий) ˆ (нисходящий) ´ (высокий) ˇ (восходящий); mid tone unmarked.

## What must never appear in learner-facing text

Spiral percentages, mastery values, SM-2 internals, difficulty numbers, skill names, source
citations, and any methodological aside. These belong to the model, not to her page. This is
the leak `skill-review`'s Blind Hunter layer looks for, and it is worth self-checking before
handing a document over.
