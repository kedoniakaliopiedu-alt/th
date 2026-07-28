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

That third part is not optional here. A dozen skills share one repository and several
are adjacent; without an explicit exclusion the wrong one fires. Compare `thai-tasks`
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

## Language of instructions

Instruction prose migrates to English **opportunistically**: when you are already rewriting
a file for a real reason, translate it whole in the same pass. Never run a translation
sweep for its own sake — the measured saving is ~26% of that file's tokens, and a wrong word
in a tuned instruction costs more than it buys.

What **never** gets translated, in any file:

- anything the learner reads — task sheets, report templates, hint examples, the
  «Естественнее» line, headings quoted into her output;
- values that are also **data**: the four checking categories (Словарный запас / Грамматика /
  Орфография / Тоны) are written into `progress.json` as `category`, and the mistake modes
  are matched by Russian substrings in `tracker.py`;
- trigger phrases quoted in a `description` — they are what the user actually types;
- Thai text and Cyrillic transcription, obviously.

A translated file therefore ends up mixed, and that is correct, not sloppy. State the rule
once at the top of the file so the next reader does not "fix" the Russian parts.

## references/*.md

- Start with one line saying **when this file gets loaded**. It is read out of context, so
  it cannot assume the reader knows why.
- No frontmatter.
- Self-contained: do not require the reader to hold `SKILL.md` in memory to follow it.
- Where the parent `SKILL.md` summarizes a rule, this file gives the full version — they
  must not contradict. When you change one, check the other in the same edit.

## Scripts

Only the Python standard library, 3.8+, and no third-party packages. Offline means nothing
reaches the internet; talking to a service on `127.0.0.1` is allowed and is how `typhoon.py`
uses the local Ollama. A module docstring that states what the script is for and lists its
commands; the docstring is the interface documentation, since `--help` renders it.

Type annotations are expected but not enforced by anything in the workflow: `pyrightconfig.json`
in the project root checks the scripts in `strict` mode, and `npx pyright --stats` should
report every script found and zero errors. It is a convenience, not a gate — nothing breaks
if it is never run, and pyright is deliberately not a project dependency. Read the file count
as well as the error count; the config explains why in a comment.

Because 3.8 is the floor, keep builtin generics (`dict[str, str]`, `list[int]`) inside
annotations, where `from __future__ import annotations` makes them lazy. A generic evaluated
at runtime — a module-level alias, a `functools.cache` decorator — needs 3.9 and does not
belong here; use `typing.Dict` and `functools.lru_cache(maxsize=None)` instead.

## Course files (`Thai A2/**`, `Thai B1/**`, `Helpers/**`)

Naming: `glavaN_temaM_*.md` for A2, `b1_glavaN_temaM_*.md` for B1. Structure inside:
`Глава` → `Тема N.M` → `Подтема N.M.K`, each with **Словарный запас**, **Теория/конструкции**
and **Практические упражнения**.

The critical constraint: **`thai-tasks` takes vocabulary and rules from these files but
deliberately does not reuse the examples in «Практические упражнения»** — it generates fresh
ones. So write that section as *illustration of the rule*, not as a bank of exercises meant
to be served to the learner, and never put anything there that must not be reused verbatim.

Every topic file ends with a closing criterion — what `thai-tasks` reads to know when the
topic may leave the spiral. The existing 36 files already carry it as «Резюме по теме» →
«К концу темы ты должна уметь», and the parser reads that section as a fallback, so nothing
has to be retrofitted. When writing a **new** topic, either keep that summary in the same
shape or use the explicit heading below; the parser prefers the explicit one. Without
either, the topic is stuck at «нет критерия» and can never be closed. The format is strict:
the parser (`read_exit_task` inside `tracker.py`, reached through `tracker.py import`) takes
only list items under a markdown heading, so a bolded line or a table yields nothing.

```markdown
## Тема закрыта, если ты можешь

1. Рассказать свой день с временем
2. Ответить на вопрос «во сколько ты встаёшь»
3. Заказать две порции риса и уточнить остроту
```

3–5 items, each phrased as an **action**, not as knowledge («заказать две порции риса», not
«знать счётные слова»). Write it together with the topic, before any lesson on it: the
engine has to know the target in advance for backward design to mean anything.

Vocabulary presentation: `**тайское**` · *транскрипция* — перевод. Transcription is Cyrillic
only, per `thai-phonetics`; the tone mark sits over the **vowel**, never over a consonant.
Tone marks: ` (низкий) ˆ (нисходящий) ´ (высокий) ˇ (восходящий); mid tone unmarked.

## What must never appear in learner-facing text

Spiral percentages, mastery values, SM-2 internals, difficulty numbers, skill names, source
citations, and any methodological aside. These belong to the model, not to her page. This is
the leak `skill-review`'s Blind Hunter layer looks for, and it is worth self-checking before
handing a document over.
