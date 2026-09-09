# Написать документ (НД)

Loaded when the user wants a document authored or rewritten: a new skill, a `references/`
file, a course topic file, a README section, a rewrite of something that grew crooked.

Output is Russian. **Read `skill-doc-standards.md` before writing a line** — it is the standard
this operation is measured against, and it is not loaded until you get here.

## Process

### 1. Establish intent

Multi-turn conversation until scope, reader and purpose are genuinely clear — one question
at a time, not a questionnaire. Three things must be settled before you write a line:

- **Who reads it** (see the audience table in `SKILL.md` — model, author, or learner);
- **What it must let the reader do** that they cannot do now;
- **What it deliberately does not cover**, and which existing document covers that instead.

If the answer to any of these is a decision nobody has made — what a mechanic should
actually do — stop and hand off to `skill-brainstorm`. Do not invent the decision inside the
prose; a document that quietly settles an open question is how skills drift.

### 2. Ground yourself in the repository

Never write from a blank slate. Read, in this order:

- the closest existing analogue — a new skill is written against `thai-mistakes`, a new
  reference against `thai-tasks/references/checking.md`, a new course file against a
  neighbouring `glavaN_temaM_*.md`;
- everything the new document will interact with: the skills that hand off to it, the
  scripts it names, the files it points at;
- for course material: the chapter plan (`Thai B1/thai_b1_plan.md`) and the actual
  vocabulary sources. Verify Thai against the course files and thai-language.com — never
  from memory.

Delegate heavy research to a subagent when it would otherwise flood context (surveying many
course files, reading a large script), asking it to return only what is relevant.

### 3. Draft

Write it whole, in the structure `skill-doc-standards.md` prescribes for that document type.
Specifics that matter more than they look:

- **Write the frontmatter `description` last**, after the body exists — it is the trigger
  contract, and you cannot state when a skill fires until you know what it does. Then check
  it against every sibling skill's description for overlap.
- **Every rule gets its reason** in the same paragraph. A rule without one gets rationalized
  away at execution time.
- **Every format requirement gets an example.** A prose description of a layout is not
  executable; the existing skills all show a template block.
- **Every reference pointer gets a "when"**: `→ читай, когда собираешь лист`, not just a
  path.
- **End with a checklist** if this is a `SKILL.md` — numbered, each item checkable, covering
  the preflight and the delivery conditions.

### 4. Review before handing over

Run `validate-doc.md` against your own draft. Then, specifically:

- reread it as the *executing model*: where could two readings both be reasonable?
- reread it as the *learner*: did any methodology leak into what she would see?
- diff it against what you replaced, if anything: did a rule silently disappear?

Delegate this pass to a subagent when the draft is long — a fresh reader catches ambiguity
the author cannot see.

### 5. Wire it in

A document nobody links to is invisible. Before declaring done:

- add or update its line in `.codex/skills/MAP.md` — the table of roles and the connection
  diagram — and in `.codex/skills/README.md` if it adds a command, a toolchain or a
  reference-file list the operator runs;
- update `AGENTS.md` if the document introduces a rule that overrides default behaviour;
- update the parent `SKILL.md` pointer if you wrote a `references/` file;
- if you wrote a course file, check whether `thai-tasks` can find it by its Glob pattern
  (`**/*glava*tema*.md`) — a correctly written file with a wrong name is invisible to the
  engine.

## Output

The finished document, plus a short summary in Russian of what was written, what was wired
in, and anything you could not verify and left for her to check.
