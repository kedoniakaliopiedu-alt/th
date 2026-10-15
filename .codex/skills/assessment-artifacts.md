# Course artifact contract

This file is the single source of truth for the filesystem structure, names and relative
links of course topics, controls, checked reports and remediation. `thai-tasks` owns topic
and control content; `thai-mistakes` owns report and remediation content. This contract owns
where those HTML files live and how existing files link to one another.

Instructions are English. Learner-facing labels and navigation remain Russian.

## HTML only

Every learner-facing course file is HTML. Do not create Markdown topic sources, Markdown
worksheets or Markdown reports. A migrated Markdown topic is converted in full: preserve its
text, heading order, tables, examples and exercises, then apply the shared stylesheet.
Deleting the source `.md` is part of the migration.

Use one `Thai A2/_shared/style.css` beside the chapter directories. Every course HTML links
to it by a relative path. Do not copy a stylesheet into a chapter or a practice directory.
Thai text inherits the ordinary system font. Do not add `@font-face`, downloaded fonts, a
special Thai font or a Thai-specific `font-family`. The shared style supports a dark screen
theme, a readable print theme and narrow screens.

## Chapter layout

A chapter has exactly three top-level artifact directories. Topic materials live directly
inside `practice/`; controls and reports are flat collections.

```text
Chapter 3/
├── control/
│   ├── C3_test_2026-10-03.html
│   └── C3_test_2026-10-13.html
├── practice/
│   ├── 01_numbers_and_classifiers.html
│   ├── 02_time.html
│   ├── 03_calendar_and_seasons.html
│   ├── 04_daily_routine.html
│   ├── C3_test_2026-10-03/
│   │   ├── index.html
│   │   └── 01_numbers_and_shopping.html
│   └── C3_test_2026-10-13/
│       ├── index.html
│       └── 01_calendar_spelling.html
└── reports/
    ├── C3_test_2026-10-03_report.html
    └── C3_test_2026-10-13_report.html
```

There is no chapter `index.html`, no `control/chapter|topic|subtopic` subdivision and no
practice companion directory. Empty artifact directories may contain one `.gitkeep` until
the first real file is created.

## Topic material

A topic is `NN_semantic_slug.html` directly under `practice/`. `NN` is its two-digit order
inside the chapter. Put subtopics inside that one file as stable modules `#m01`, `#m02`, and
so on. Existing supplemental HTML pages for that topic are preserved inside the same file as
`#supplement01`, `#supplement02`, and so on; never discard them merely because the converted
topic already covers similar material. A chapter migration converts every source topic in
the named chapter to this format and removes its `.md` source.

The topic links to existing controls that assess it. Link a module to a subtopic control
when one exists; at the end of the file link the latest topic control and chapter control.
Do not create a new control merely because Markdown was converted to equivalent HTML:
presentation-only migration does not change assessed content.

## Control names and placement

Every control is one dated HTML file directly in `control/`. The date is the date that form
was created and is mandatory. A new attempt creates a new file; never overwrite history.

Use these exact forms:

```text
C3_test_2026-10-03.html          # chapter control
C3_T1_test_2026-10-03.html       # topic 3.1 control
C3_T1_S2_test_2026-10-03.html    # subtopic 3.1.2 control
```

`C`, `T` and `S` are uppercase. Chapter, topic and subtopic numbers are not zero-padded.
The filename contains no extra type synonyms such as `diagnostic`, `review`, `srez` or
`kontrolnaya`. Scope is encoded by the `C/T/S` prefix.

An initial control and a control created after remediation follow the same rule. A recheck
is therefore another flat dated control, not a nested artifact and not a `_recheck` file.
Its content is limited to the practice it checks, but its storage is identical to any other
control.

## Reports

A checked report is one HTML file directly in `reports/`. Copy the exact source-control
basename and add `_report`:

```text
control/C3_test_2026-10-13.html
reports/C3_test_2026-10-13_report.html
```

The report links to its source control and to the practice directory created from it, when
that practice exists. It preserves every learner answer, score and historical verdict.

## Remediation directories

Create remediation only after a completed control has been checked and its report exists.
The remediation directory is named exactly after the source control basename:

```text
control/C3_test_2026-10-03.html
practice/C3_test_2026-10-03/
```

Each remediation directory contains:

- `index.html` — route, scope and links to its modules;
- one or more numbered thematic HTML files such as `01_numbers_and_shopping.html`;
- no local stylesheet and no nested `control/`, `reports/` or `practice/` directories.

Split remediation by coherent teaching theme. `index.html` is navigation, not a duplicate
copy of every module. When the historical remediation exists as one indivisible page and
cannot be separated without changing its content, it may remain entirely in `index.html`.

A remediation control is created automatically with the remediation and stored as the next
dated flat file in `control/`. Do not put answers, explanations or links to hidden keys in
that control. If the control later produces gaps, its own remediation receives a new root
folder named after that control:

```text
control/C3_test_2026-10-13.html
practice/C3_test_2026-10-13/
```

## Relative links

Every link is relative and points to an existing file. Never link to a planned artifact.

- A topic links to the latest existing control for its module/topic and to the latest
  chapter control.
- A control links to the topic files or remediation directory it assesses.
- A report links to its exact source control and to its remediation `index.html`, if one
  exists.
- A remediation `index.html` links to its source control, its report and all module files.
- Every remediation module links back to `index.html` and may link to its exact source
  control and report.
- A later control created for remediation links back to that remediation `index.html`.

## Migration of legacy artifacts

Migration is opt-in and limited to the chapter or cycle named by the user.

1. Convert every named Markdown topic to styled HTML without changing its content, then
   delete the Markdown source.
2. Merge existing topic and subtopic HTML into the matching numbered topic file at their
   existing section boundaries, retaining their text, exercises and hidden answers.
3. Identify controls, reports and remediation from their content and actual links, not from
   legacy filenames.
4. Give every historical control its creation date. Use repository history or the dated
   report/cycle when the file itself omits it; record unresolved dates instead of guessing.
5. Preserve learner answers, recorded errors, scores and historical assessment results.
6. Move each remediation under the basename of its source control and split only at
   existing thematic boundaries.
7. If historical content appears wrong, retain it and report the concern separately.

## Pre-delivery check

Confirm that the chapter contains no `.md` learning files; topic HTML preserves the source
text and structure; every control name has the correct scope and creation date; every
report copies its control basename; every remediation directory copies its source-control
basename; all relative links and fragments resolve; no legacy nested ecosystem remains;
and every HTML uses the shared stylesheet and system Thai font. Render representative topic,
control, report and remediation pages on wide and narrow screens. Run `git diff --check`.
