# Self-study topic and practice materials

Read this file when creating or revising a teaching topic or when `thai-mistakes` uses its
shared presentation rules for a self-study practice file. It owns the learner-facing
teaching rhythm, not the choice or scope of remediation content. File placement, names and
links come only from `../../assessment-artifacts.md`. Formal controls are excluded: they follow
`written-control.md` and must never expose answers before completion.

## Teaching rhythm

Divide the material into small coherent parts. A part normally contains:

1. one short explanation suitable for copying into a notebook;
2. a few natural examples;
3. a compact practice block for that part;
4. prewritten self-check answers.

Let the material determine the size. Do not impose a universal minute limit, exercise
count, difficulty ladder or mastery threshold. Teach the base rule with ordinary examples
first; introduce an important exception as the next separate part.

For a new construction, combine recognition in examples, work from a model and independent
construction in the order that suits the construction. Vary task type and everyday
context. Do not turn a section into a long run of near-identical sentences.

Use clear headings, short blocks, useful comparison tables and restrained highlighting.
When revising an existing course topic, first identify and preserve its useful heading
order, rule boxes and vocabulary-table columns unless the request explicitly changes one of
them. Avoid terminology that is not needed to carry out the task.

## HTML topic standard

Use `Thai A2/_prototypes/topic-style.html` as the canonical structure,
`Thai A2/_shared/style.css` as the canonical stylesheet and
`Thai A2/_shared/topic.js` for adaptive example rows. Do not copy an older topic's local
CSS or fit script into a new file: the shared assets keep the chapter consistent. A topic
is a standalone HTML document linked to those assets and contains no Markdown source copy.

The visible page has this order:

1. the topic title and links to related controls;
2. an untitled, single-column table of contents;
3. the subtopics;
4. no visible goal block and no final «Резюме по теме».

Keep the closing criterion in a hidden `<section class="topic-exit" hidden>` with the exact
heading «Тема закрыта, если ты можешь» and a list of 3–5 observable actions. The tracker
reads those list items; hiding the section keeps service data out of the learner's page.

Each subtopic contains four primary `h3` sections in this order: **Словарный запас**, a
specific rule or construction name, **Якоря**, and **Практические упражнения**. Do not use
«Теория» as a visible heading. Promote meaningful divisions inside the rule section to
real `h4` headings, include them in the table of contents, and wrap their following content
in `.inner-topic`. No heading ends with punctuation.

The table of contents has no title, background panel, numbering or columns. A subtopic is a
collapsible `.toc-group`; its rule section is a nested collapsible `.toc-subgroup`; the
inner `h4` links sit in `.toc-inner`. Use the shared CSS chevron markup shown in the
prototype. Align the table of contents with the subtopic headings and use the same modest
space above and below it.

Use `.heading-block` around each primary section. Its heading has its own horizontal inset,
and the section content is inset once more relative to that heading. An `.inner-topic`
repeats the same relationship between an `h4` and its content. Keep equal top and bottom
space around `h3`, `h4`, and every coloured block.

Colour communicates the role of a block:

- `.rule`: background `#00416a`, text `#b9d9eb`, only for a rule;
- `.example`: background `#26382d`, text `#b7d4a9`;
- `.lakorn-example`: background `#5b3256`, text `#e8adf7`;
- `.note`: the neutral panel style, including «Не путай».

Headings stay outside coloured blocks. Tables, examples, notes and lakorn examples are
siblings after the relevant rule, never children of `.rule`. Use equal `22px 24px` inner
padding for coloured blocks and remove the border from rule and example blocks. Tables span
the available width and have square corners. Paragraphs are justified and have no first-line
indent.

Examples use the system font for Thai, Russian and numbers. Do not put learner-facing
examples in `<pre>` or `<code>`. Put each semantic unit on one line with
`.example-lines > .example-unit`; use `.example-list > .example-item` when the unit has
several aligned parts. Keep the whole unit on one line. The prototype's fit script chooses
the largest font size up to the surrounding body size that fits every unit without
horizontal scrolling; use that approach for every example block, not for a selected case.
Add `.fit-lines` to any other compact formula whose semantic units must also remain on one
line, and mark each unit with `.example-unit`.

Exercises use `.task` cards. Put the instruction and any item list in
`<b class="task-prompt">`, with `.task-instruction` and `.task-items` on separate lines.
Every card contains a native `<details>` answer with the shared chevron and the label
«Показать ответ». Keep that label normal weight and smaller than body text. During a
structure-only migration, use «здесь будет ответ» rather than inventing a key that was not
present in the source.

## Self-check is not assessment

Every exercise inside a teaching topic or practice file has a prepared answer. Hide it
behind native `<details>` in HTML. Inside the disclosure show:

1. `Ответ:` or `Один естественный вариант:` with the complete answer;
2. only when useful, a brief `Почему:` or `Что проверить:` line.

When the learner's result differs, the file supplies the key and explanation only. It does
not award ✅/🟡/❌, calculate a score, infer an error pattern or automatically append a new
remediation block. Formal verdicts begin after a control and belong to `thai-mistakes`.

For a recall task, keep the target form out of view until the disclosure is opened. After a
failed recall, the self-study cycle is: inspect the full answer, close it, reproduce it,
then meet the item again later in a different short task.

Canonical minimal block:

```html
<section id="m01">
  <h2>Короткая связная часть</h2>
  <p>Одно короткое объяснение.</p>
  <p><span lang="th">[пример]</span> — [перевод].</p>
  <div class="task">
    <p><b>Напиши по-тайски: [русская ситуация].</b></p>
    <details>
      <summary>Показать ответ</summary>
      <p><b>Ответ:</b> <span lang="th">[полный ответ]</span></p>
      <p><b>Почему:</b> [одна полезная проверка].</p>
    </details>
  </div>
</section>
```

The visible example must not contain the exact answer recalled in the task. A different
correct model may precede it; the target itself stays inside the closed key.

## Writing and the learner's notebook

Show a correct spelling before asking for production from memory. Spread short handwritten
actions across the parts of the topic: copy or annotate once while learning, then write
from a Russian meaning or situation after the model has been hidden. Do not collect all
writing into one large copying block.

The notebook is both an encoding action and a quick reference. Present rules as compact,
accurate blocks that can be copied and found again. Do not assume that the learner will
systematically review the notebook.

The learner handles speaking, listening and repeated oral practice independently. Do not
add required speaking, listening, voice-input checks or oral repetition to course files.
Use project transcription only where another skill requires it. Voice input is not tone
evidence; `thai-verify` owns tone verdicts.

## Vocabulary coverage

The complete new vocabulary of a topic is a learning goal, not a reference appendix. An
overview may appear first, but teach the words through small meaningful groups alongside
the relevant parts. Follow `vocabulary-acquisition.md` for word-level memory mechanics.

Reuse each word naturally across different contexts and task types as often as the material
supports. Do not enforce a mechanical exposure quota. Every target word must appear in at
least one active task, and across the topic every word must at some point be recalled or
used productively without a visible model. A vocabulary table, worked example or a single
recognition choice does not meet that goal by itself.

Before declaring the topic material complete, audit the full vocabulary list against the
exercises. No target word may remain only in the overview or examples. Re-schedule a word
into a later part or subsequent review when another immediate use would be artificial.

For easily confused words or constructions, use all three supports when useful:

- a short comparison table;
- clearly different real-life situations;
- a minimal pair of almost identical examples where one element changes.

## Sources and naturalness

For new or substantively revised material, follow `../../content-sources.md`: assign
lexicon, grammar, example and register evidence to sources suited to those roles. Two pages
from one site do not count as independent evidence, and a corpus hit does not prove a rule
by itself. Keep an internal claim ledger and add a concise Russian footer naming only the
sources actually consulted and the role each served.

Prefer natural, varied everyday situations. Derive fresh level-appropriate examples from
manually checked corpus patterns; do not copy a sentence merely because it is authentic.
A short verified quotation from a song, series or post may be used only when the exact text
serves the teaching goal and its rights permit it. Keep formal, neutral and conversational
evidence separate, because normal colloquial language is not an error and noisy web spelling
is not automatically a neutral model.

## Controls prepared with material

When creating a new topic or module, also prepare controls from the same taught scope:

- a new or substantively changed module → a new dated subtopic control for that module;
- a new topic or a change that affects several modules or the topic's completion goal → a
  new dated topic control;
- a change to chapter-wide required vocabulary, constructions or completion coverage → a
  new dated chapter control.

Spelling, layout or broken-link fixes that do not alter what is taught do not require a new
control. Record this check in the final work report as either the controls created or
«содержание контроля не затронуто». An issued control is historical evidence: create a new
dated file instead of overwriting it.

Controls follow `written-control.md` and contain no examples, keys, explanations or hidden
answers. Place them and connect the module/topic links under
`../../assessment-artifacts.md`. Preparing a control with material does not authorise a
future practice; practice is created only after a completed control and report.

## Completion check

Confirm that the material uses short coherent parts, base rule before exceptions, visible
models before hidden recall, distributed handwriting, varied tasks and contexts, a key for
every exercise, no assessment verdicts, no required oral work, and active exercise coverage
for every target word. Confirm that applicable controls were prepared or rechecked without
creating any future remediation placeholder.
