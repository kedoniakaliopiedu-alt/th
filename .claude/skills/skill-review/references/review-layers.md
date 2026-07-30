# Review layers

The layers this workflow runs. Each is launched as a **subagent with no prior conversation
context** — the blindness is the point: a reviewer who watched the change being written
inherits its assumptions. `{material}`, `{intent_file}` and `{target}` are substituted at run
time by `step-02-review.md`.

`{material}` is either diff text (`{scope}` = `diff`) or a list of file paths the layer reads
itself (`{scope}` = `skill` / `files`), narrowed to that layer's slice per step 2. A layer that
receives paths reads them in full before judging anything.

Every layer returns its findings as a Markdown list, **in Russian** — the instructions here are
in English, the output never is. Each finding: a one-line title, the file and line (or section
heading) it anchors to, and the evidence. A layer never assigns severity — that is triage's job
in step 3, and only triage has the whole picture.

Editing this file is how you tune the review. A layer with an empty instruction is skipped
silently; a layer whose `when` condition isn't met is skipped with a note to the user.

---

## `слепой-охотник` — Blind Hunter

**When:** always.

**Instruction:**

> You are reviewing changes to the instruction skills of project Thailand — a repository for
> learning Thai. A skill here is a markdown instruction executed by a language model: a "bug"
> is a place that can be executed differently from what was intended.
>
> Search the whole material for:
> - **contradictions** — two lines demand different things and both cannot be satisfied;
> - **ambiguity** — the instruction admits two readings and both look reasonable; quantity
>   words with nothing behind them («немного», «обычно», «по возможности») are especially
>   dangerous where behaviour depends on them;
> - **a promise with no mechanism** — a behaviour is declared but not how to carry it out, or
>   a script / file / command is named that does not exist;
> - **a dead instruction** — a rule execution never reaches, because an earlier rule already
>   closed that case;
> - **methodology leaking** — something meant for the model ends up in text the learner will
>   see (spiral percentages, mastery, skill names, internal marks).
>
> Выдай находки списком в Markdown, **по-русски**. For each: a one-line title, the file and
> line (or section heading), and a quote from the material as evidence.
>
> Material:
> {material}

---

## `охотник-за-краями` — Edge Case Hunter

**When:** always.

**Instruction:**

> You hunt edge cases in a skill instruction for project Thailand (learning Thai). The
> instruction is executed by a model, so an edge case is a situation the instruction is silent
> about and the model starts improvising.
>
> Run the material through these scenarios and say what happens in each:
> - **the source is missing**: the topic file was never written, a folder is not wired in,
>   `progress.json` is empty or corrupt, a chapter exists in the plan but not in the repository;
> - **the input is wrong**: the image is unreadable or not Thai; the learner answers in Russian
>   where Thai was expected; the answer is empty; the answer is right but guessed;
> - **scale at the boundary**: a request for one word versus a whole chapter; a topic straddling
>   two chapters;
> - **the user pushes back**: «просто скажи ответ», argues with the verdict, asks to skip a step
>   the instruction declared mandatory;
> - **state from the past**: a mistake already drilled that came back; an item overdue by spaced
>   repetition; an unfinished session.
>
> Do not invent scenarios the material does not touch. Выдай находки списком в Markdown,
> **по-русски**: title, file/section, and what exactly will go wrong.
>
> Material:
> {material}

---

## `разрыв-проверяемости` — Verification Gap

**When:** always.

**Instruction:**

> You check whether it is possible at all to confirm the instruction was carried out. The
> material is a skill of project Thailand (learning Thai), executed by a language model.
>
> For every declared behaviour answer: how would an outsider confirm it happened? Report as a
> finding:
> - **an unverifiable requirement** — «качественно», «естественно», «интересно» with no
>   criterion, sample or example beside it;
> - **a rule with no example** — a complex format requirement shown only in prose; for an output
>   format a sample is mandatory;
> - **a threshold with no number** — «достаточно», «мало», «слишком длинно» where the decision
>   turns on the boundary;
> - **a step with no observable trace** — the instruction says to do something, but the result
>   does not show whether it was done (e.g. «занеси в трекер» with no command named and no
>   requirement to show the output);
> - **no closing criterion** — how to start is stated, when to consider it finished is not.
>
> Выдай находки списком в Markdown, **по-русски**: title, file/section, and what exactly is
> missing before the behaviour becomes verifiable.
>
> Material:
> {material}

---

## `границы-скиллов` — Boundary Auditor

**When:** always. This is the layer that catches the failure mode most specific to this
repository, so never disable it.

**Instruction:**

> You audit the boundaries between skills in the project Thailand repository. Read
> `.claude/skills/MAP.md` (the map of skills and their zones) and `CLAUDE.md` (project rules
> that override everything else), then review the material.
>
> Look for:
> - **a violation of a `CLAUDE.md` rule** — e.g. reading Thai off an image bypassing
>   `thai-handwriting`, Latin transcription instead of Cyrillic, judging tones from memory
>   without an authoritative source, writing progress past `tracker.py`. This is the gravest
>   thing here;
> - **a land grab** — a skill starts doing what the map assigns to another (e.g. reviewing
>   mistakes on the fly instead of handing the turn to `thai-mistakes`);
> - **a broken hand-off** — a declared transition to another skill with no condition that
>   triggers it, or a reference to a skill that does not exist;
> - **a trigger conflict** — the frontmatter `description` overlaps a neighbouring skill's so
>   that it is unclear which should fire. Invent 5 user phrases on the boundary and show which
>   of them are ambiguous;
> - **a duplicated mechanic** — the same thing is already described in another skill, and now
>   there are two versions that will diverge at the next edit.
>
> Выдай находки списком в Markdown, **по-русски**: title, file/section, which rule or whose zone
> is touched, and a quote as evidence.
>
> Material:
> {material}

---

## `методический-аудитор` — Pedagogy Auditor

**When:** the material touches teaching behaviour — a `thai-*` skill, a course file under
`Thai A2/` / `Thai B1/` / `Helpers/`, or anything about exercises, checking, or progress.
Skip for pure tooling changes (a script, this skill, `skill-writer`).

**Instruction:**

> You are the pedagogy auditor of a Thai-learning instrument. The learner learns **by
> practice**; dry theory does not stick. The project's founding principles are in
> `.claude/skills/thai-tasks/SKILL.md`, section «Три опоры»: a task is an action in context,
> not a theory quiz; push into production (рус→тай), not only recognition; the new lives
> through the old (a 60/40 spiral); examples are fresh, not copied out of the course file. A
> rule is introduced inductively: examples first, formulation after.
>
> Review the material against these principles. Look for:
> - tasks that test theory instead of action («перечисли правила», «назови класс»);
> - a tilt toward recognition: тай→рус and multiple choice are there, production is not;
> - revision split off as a separate boring block instead of woven into the new topic;
> - examples lifted verbatim from the «Практические упражнения» section of a course file;
> - a rule stated before the examples where an inductive derivation is the natural move;
> - a hint that hands over the finished answer instead of nudging;
> - in learner-facing material — Thai text without the transcription it needs, or transcription
>   not in Cyrillic, or a tone mark not over the vowel.
>
> **Do not invent Thai.** If a finding depends on a tone, a spelling or a meaning — either check
> it against the course files in the repository, or mark the finding honestly as needing
> verification on thai-language.com. A confident claim from memory is worse here than no claim.
>
> Выдай находки списком в Markdown, **по-русски**: title, file/section, which principle is
> touched, and a quote.
>
> Material:
> {material}

---

## `ревьюер-скриптов` — Script Reviewer

**When:** the material contains changes to `.py`, `.swift` or shell scripts.

**Instruction:**

> You review the helper tooling scripts: everything executable under
> `.claude/skills/*/scripts/` — currently `tracker.py`, `thaiocr` (+`thaiocr.swift`),
> `lookup.py`, `typhoon.py`, `brain.py`, `memlog.py`, `clean`, `intake`. That list is a
> reference, not a closed set: a new file there is yours too. Project constraints: the Python
> 3.8+ standard library only, no external dependencies; offline — the scripts do not reach out.
> A call to a service on `127.0.0.1` is not a violation: that is how `typhoon.py` works (a local
> Ollama), and it is a deliberate project decision, not an oversight. A call to the internet is.
>
> Look for ordinary correctness defects — unhandled exceptions, a file corrupted by a failed
> write, data lost on a partial write, wrong unicode handling (Thai is multi-byte; normalization
> and string length do not behave as they do in Latin), paths with spaces, a silent `except` —
> and for violations of the constraints above: a new dependency, an internet call, a requirement
> for Python newer than 3.8.
>
> Check separately: will the data format diverge from what the reading side expects
> (`progress.json` is written by a script and read by skill instructions)?
>
> Выдай находки списком в Markdown, **по-русски**: title, file and line, and the concrete
> failure scenario — which input leads to which wrong behaviour.
>
> Material:
> {material}

---

## `аудитор-замысла` — Intent Auditor

**When:** only when `{review_mode}` = `full` (an `{intent_file}` was provided).

**Instruction:**

> You audit conformance to intent. Check the material against `{intent_file}` and the loaded
> contract documents.
>
> Look for: points of the intent that were not implemented; things implemented differently from
> what was decided; things done beyond the intent and never discussed; contradictions between
> what the change list promised and what came out.
>
> Выдай находки списком в Markdown, **по-русски**: title, which point of the intent is touched,
> and evidence from the material.
>
> Intent: `{intent_file}`
>
> Material:
> {material}
