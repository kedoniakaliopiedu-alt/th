---
diff: ''          # set at runtime: diff text, when scope = "diff"; empty otherwise
paths: ''         # set at runtime: list of file paths, when scope = "skill" | "files"; empty otherwise
scope: ''         # set at runtime: "diff" | "skill" | "files"
target: ''        # set at runtime: human name of what is reviewed (e.g. "thai-tasks")
intent_file: ''   # set at runtime: path to the stated intent, or empty
review_mode: ''   # set at runtime: "full" (intent known) | "no-intent"
---

# Step 1: gather context

## RULES

- Speak Russian to the user.
- The prompt that triggered this workflow IS the intent — not a hint.
- Do not modify any files. This step is read-only.

## INSTRUCTIONS

### 1. Find the review target

The conversation before this skill was triggered IS your starting point — not a blank
slate. Check in this order and stop as soon as the target is identified.

**Tier 1 — explicit argument.** Did the user name a target in this message?

- **A skill name** («аудит thai-tasks», «отревьюй skill-writer») → `{scope}` = `skill`,
  `{target}` = that skill. The material is every file under `.claude/skills/<name>/`.
- **A file path** (a `SKILL.md`, a `references/*.md`, a course file, a script) →
  `{scope}` = `files`, `{target}` = those paths.
- **A change reference** — «мои правки», «что я наменяла», a commit SHA, a branch →
  `{scope}` = `diff`. Also scan for the mode:
  - «незакоммиченное» / «рабочая копия» / «всё что изменила» → `git diff HEAD`
  - «застейдженное» → `git diff --cached`
  - «ветка» / «против main» → branch diff (extract the base if named)
  - «последние N коммитов» / `<sha>..<sha>` → commit range
- **A chapter or topic** («проверь главу 3», «тема 6.1») → `{scope}` = `files`, resolved by
  Glob over `Thai A2/**` / `Thai B1/**` / `Helpers/**`.

**Tier 2 — recent conversation.** Do the last few messages reveal what should be reviewed?
A skill that was just edited, a file just written by `skill-writer`, a change list produced
by `skill-brainstorm`. Apply the same routing as Tier 1.

**Tier 3 — a change list from a brainstorm.** Glob `.claude/brainstorms/*/изменения.md`.
If exactly one exists and is newer than the last review in `.claude/reviews/`, suggest it:
«Нашёл лист правок `<путь>` от <дата>. Ревьюим то, что по нему сделано?» If confirmed, set
`{intent_file}` to it and continue the cascade to find the diff. If declined, fall through.

**Tier 4 — current git state.** Check the branch and whether the working tree is dirty.
- Dirty tree → confirm: «Вижу незакоммиченные изменения в <N> файлах — ревьюим их?»
- Clean tree, branch is not `main` → confirm reviewing the branch diff against `main`.
- Clean tree on `main` → fall through.

**Tier 5 — ask.** Fall through to instruction 2.

Never ask extra questions beyond what the cascade prescribes. If a tier identified the
target, skip the rest and go to instruction 3.

### 2. HALT and ask

Ask, in Russian: **«Что ревьюим?»** Present these options:

1. **Незакоммиченные изменения** — staged + unstaged
2. **Только застейдженное**
3. **Ветку против базовой** (ask which base)
4. **Скилл целиком** (ask which one)
5. **Конкретные файлы** (ask for paths)

### 3. Build the material

The layers read the material themselves, in their own contexts. **Your job here is to
determine what the material is, not to hold it.** Never read a file into this session just to
pass it on — a copy here is a copy paid again in every layer.

- `scope` = `diff` → build `{diff}` as text; a diff is compact and the layers need it
  verbatim. Leave `{paths}` empty.
  - uncommitted → `git diff HEAD`
  - staged → `git diff --cached`
  - branch → verify the base branch exists first; HALT and ask if it doesn't
  - commit range → verify it resolves; HALT and ask if it doesn't
  - Untracked new files are invisible to `git diff` — list them with
    `git ls-files --others --exclude-standard` and append each via
    `git diff --no-index /dev/null <path>`. A brand-new `references/` file is exactly the
    kind of thing worth reviewing, and it is the easiest to miss.
- `scope` = `skill` → `{paths}` = every file under `.claude/skills/<target>/` (Glob, do not
  read them). Leave `{diff}` empty. Note in the summary that this is a full-file audit, not a
  diff: findings about pre-existing text are in scope here, whereas in a diff review they are
  `defer` by default.
- `scope` = `files` → `{paths}` = the named paths, verified to exist. Leave `{diff}` empty.

Verify the material is non-empty — a non-empty `{diff}`, or a `{paths}` list with at least one
existing file. If empty, HALT and say there is nothing to review.

### 4. Set the intent context

The analog of a spec here is a statement of *what the change was supposed to do*.

- If `{intent_file}` is already set (Tier 1 or 3): verify it exists and is readable, set
  `{review_mode}` = `full`.
- Otherwise ask: **«Есть ли лист правок, задача или описание, ради чего это менялось?»**
  - yes → set `{intent_file}`, verify readable, `{review_mode}` = `full`
  - no → `{review_mode}` = `no-intent`

Whatever the answer, always load these as the standing contract — they play the role a spec
plays elsewhere, and they exist for every review:

- `CLAUDE.md` — project rules that override everything;
- `.claude/skills/MAP.md` — skill boundaries and hand-offs;
- for a skill under review: its own `SKILL.md` frontmatter `description`, which is the
  contract for *when the skill fires*.

### 5. Size check

If the material is large — `{diff}` over roughly 2000 lines, or `{paths}` over roughly 150 KB
by `wc -c` (each layer reads all of it) — warn the user and offer to chunk the review by file
group (e.g. one skill's `SKILL.md` + its `references/` per run).

- Chunking → agree on the first group, narrow `{diff}` / `{paths}` to it, and list the
  remaining groups so she can note them for follow-up runs.
- Declining → proceed with the whole thing.

### CHECKPOINT

Present a summary before proceeding, in Russian: what is being reviewed — the list of file
paths, plus lines added/removed if it's a diff — `{scope}`, `{review_mode}`, and which contract
documents were loaded. **HALT** and wait for confirmation.

## NEXT

Read fully and follow `./step-02-review.md`.
