---
name: thai-mistakes
description: >
  Thai error-review workflow for project Thailand. Use it ALWAYS immediately after checking
  the learner's answers to a diagnostic, control, worksheet or practice: it asks for
  calibration before the verdict, produces the full checked report, records results and
  creates remediation artifacts. Also use for direct requests that explicitly refer to
  prior errors or tracker history, such as «работа над ошибками», «разбери мои ошибки»,
  «потренируй слабые места из прошлого среза» and «что я до сих пор путаю».
  Rule and topic gaps receive standalone thematic HTML lessons; a word that is repeatedly
  misspelled, cannot be produced or «никак не запоминается» receives a compact lexeme-memory
  cycle instead. Live drills remain opt-in when the learner explicitly asks to work in chat.
  Do not use to create a fresh task set before any answers exist; that is thai-tasks.
---

# Thai Mistakes — error review and remediation

This is the second beat of a lesson. `thai-tasks` presents and checks tasks;
`thai-mistakes` turns the result into a **full report**, a **remediation route** and tracker
data that determines what returns later.

The default principle is: **a mistake reveals a gap, and the kind of gap sets its scope**.
A transferable rule or a broad vocabulary weakness opens the smallest useful root topic.
Repeated failure on one exact learned word opens a focused memory cycle for that lexeme;
it does not justify reteaching the whole topic.

## Always start here

1. With a fresh unchecked batch, keep the verdict hidden and ask the calibration question
   in step 0. If feedback has already been revealed, record that calibration is unavailable
   and do not ask retrospectively.
2. Read `references/report-format.md` before producing the report.
3. Classify each non-correct answer by both location and cause:
   - category: vocabulary, grammar, spelling, tones or another report category;
   - route: thematic gap, exact-lexeme memory gap, misconception or reference problem.
4. Record every formally assessed element and every real assessment mistake before
   generating remediation. A first miss while a word is being taught and a discrepancy in
   autonomous self-check are learning events, not mistake patterns.
5. For a written sheet, read `references/thematic-html-modules.md`; when any item uses the
   exact-lexeme route, also read `references/lexeme-memory.md`.
6. Read `../assessment-artifacts.md` before saving or linking a report or practice file;
   it is the sole contract for artifact paths, names, control-named practice directories and links.
7. For live work requested in chat, read `references/drill-modes.md`; for a systematic
   false rule, also read `references/misconceptions.md`.
8. Verify tones through `thai-verify` before any verdict. Never grade a tone from memory.

## When it runs

- **Automatically:** immediately after any checked diagnostic, control, worksheet, practice
  set or live session. Produce the report even when there are no errors.
- **Directly:** for a request that explicitly points to previous errors or the tracker, such
  as «работа над ошибками по последнему срезу» or «что я до сих пор путаю». With no fresh
  sheet, take due patterns from `drill-plan --due`.

If there are no errors, give the report and clean-result summary, skip remediation and hand
back to `thai-tasks` for the next program step.

## Pipeline

With a fresh sheet, run steps 0–3 in order; steps 4–7 apply only when the learner explicitly
asks for live work in chat. With no fresh sheet, do not invent `N`, literal answers or a
report: skip steps 0–1, load existing patterns and continue from route selection in step 2.

### 0. Calibration before the verdict

The answers already exist and the verdict is still hidden. Ask exactly one short question
and wait. If per-answer feedback has already revealed the result, skip this step:

> Прежде чем открою проверку: сколько из N, по-твоему, верно — и какие пункты ты
> **угадала**, а не знала?

Do not offer options. If the learner declines or asks to see the check immediately, continue
to step 1 and omit the calibration line from the report.

### 1. Full checked report

Repeat the entire original sheet and annotate each answer with ✅ / 🟡 / ❌, the correct
version and one-line reason. Follow `references/report-format.md`.

Two rules are absolute:

- every 🟡 and ❌ includes the full correct answer in the format requested by the task,
  including literal skips such as `?`, «не знаю» and blanks;
- any correction to an issued report triggers a complete resend from the top after
  rechecking and recomputing every dependent score, percentage and breakdown.

### 2. Tracker update and route selection

Before remediation, run `record` for every formally assessed element and `mistake` for every
real assessment error. This workflow owns those writes after the hand-off; `thai-tasks`
must not write the same result first. `--topic` remains mandatory because it locates the
material, even when remediation is lexeme-specific. A correct answer admitted as a guess
receives quality 3, not 5.

Choose the route from evidence:

| Evidence | Route |
|---|---|
| One exact learned word fails in separated later work, or the learner says it systematically will not stick | `--mode lexeme` |
| Several words from one topic are broadly weak | `vocab` |
| Several errors share a rule or construction | thematic mode such as `grammar`, `spelling` or `tones` |
| The learner consistently applies a false rule | thematic mode plus `misconceptions.md` |
| The task wording or an unknown term caused the miss | `reference` |

Keep report category and remediation mode separate. A word may be an `Орфография` error in
the report and still use `--mode lexeme` because memorising its exact written form is the
right intervention.

Before treating `?`, «не знаю», a blank or Russian text as a lexeme gap, rule out an unclear
instruction or answer-format problem; those use `reference`. One first-learning miss is not
enough unless the learner explicitly identifies a recurring memory problem.

The lexeme route does not shake, block or reopen the whole topic by itself. Record its weak answer
with `record ... --item-only`; the item still returns through `due` and `attempt`. Reopen a
topic only when separate evidence shows that a transferable rule or several core elements
have failed.

### 3. Files after a written sheet

For thematic gaps, group mistakes by the smallest useful root topic and create modules
inside the source control’s practice directory under `references/thematic-html-modules.md`. The trigger
error occupies a short opening block; the lesson then teaches the whole root topic.

For `lexeme` gaps, create one compact memory module containing only the fresh target words.
Follow `references/lexeme-memory.md`: literal error trace, one useful retrieval hook per
word, reconstruction with fading support, delayed production and adaptive returns. Do not
add a theory lecture or neighbouring vocabulary.

When both routes occur, place the thematic and lexeme modules in the same practice
directory. Give exact-word work its own compact module and link it from `index.html`;
do not present it as another whole-topic lesson.

Creating a file does not count as a successful drill. Do not call `attempt` or close a
pattern until the learner demonstrates retrieval in assessed work.

### 4. Live mini-diagnostic

Run this step only on an explicit request to work in chat.

For a thematic route, ask 3–5 quick questions on nearby cases not used in the original
sheet. Add confirmed gaps and leave clean areas alone. Skip this when the topic is tiny or
the learner asks to start immediately.

For a `lexeme` route, do not diagnose the topic. Establish only what fails: meaning →
word, the middle of the spelling, a confusing pair, or production despite successful
recognition.

### 5. Explanation or memory setup

For a thematic first round, explain from the learner's error in 3–5 lines:

> твой вариант → почему он не работает → правило одной фразой → как было бы верно

On a second thematic round, work inductively: give 3–4 examples, let the learner formulate
the pattern, then check it.

When a systematic error reflects a false rule, use a counterexample before explanation.
Ask how the learner reasoned, construct a case where that rule visibly fails and let her
locate the mismatch. The full method and completion criteria are in
`references/misconceptions.md`.

For `lexeme`, there is normally no rule to explain. Show the literal wrong and correct forms,
identify the first unstable fragment and choose one retrieval hook that reconstructs the
Thai spelling. Then hide the word. Read `references/lexeme-memory.md` for the full sequence.

### 6. Drill block

Use the mode returned by `drill-plan` and follow `references/drill-modes.md`. Preserve the
source format: a worksheet produces a batch; a live one-at-a-time session stays
one-at-a-time.

Free composition of a dialogue, story or text is forbidden in a live drill. Use bounded
tasks with verifiable answers. Every mode includes productive Russian → Thai work.

For `lexeme`, use only the failed words. Recognition, choice and supplied chunks are
scaffolds; the block must finish with unprompted production after intervening tasks.

### 7. Round result

Record each pattern with `attempt --result ok|fail`.

For a misconception, `ok` requires both: the learner states what was wrong in the former
reasoning and solves a new trap case. For an ordinary knowledge gap, new correct cases are
enough.

For `lexeme`, `ok` requires two correct productive recalls without a visible model,
separated by other tasks. Choosing from options, copying and one correct answer immediately
after exposure are insufficient.

Then apply the two-round rule below.

## Calibration

Compare the step-0 estimate with the actual result:

| Самооценка | Факт | Что это | Что делать |
|---|---|---|---|
| уверена | ✅ | честное владение | обычный маршрут, `record` 5 |
| **уверена** | **❌** | **иллюзия беглости** | назвать в отчёте и поставить первой в отработку |
| угадала | ✅ | узнавание, не владение | ошибки нет; `record` 3 вместо 5 |
| не уверена | ❌ | честная дыра | обычный маршрут |

Treat «угадала» as useful information, never as misconduct. The lower quality value makes
the item return sooner; it is not a penalty.

A large overall mismatch also matters. Overestimation calls for slower work and more
diagnosis; underestimation calls for showing the concrete answers that were genuinely
correct.

## Volume

For thematic groups, take the volume from `drill-plan`:

- 3 tasks for the first mistake in a topic;
- +1 for every additional mistake;
- a pattern with `frequency ≥ 2` counts as two;
- maximum 10 tasks per topic.

If all groups exceed about 15 tasks, take the two heaviest themes first and leave the rest
scheduled.

For `lexeme`, the unit is the target word, not the topic. Take a small coherent set that the
learner can distinguish and reproduce without turning the page into a list. Give each word
separated retrieval under `references/lexeme-memory.md`. Never fill the set with other topic
words merely to reach a task count.

## Modes

`drill-plan` chooses a mode from the category unless `--mode` overrides it.

| Evidence or category | Mode | Core action |
|---|---|---|
| exact word repeatedly not retained | `lexeme` — точечное запоминание слов | error trace, one hook, fading support, delayed production |
| broad topic vocabulary weakness | `vocab` — запоминание слов | topic vocabulary in portions, both directions, live phrase |
| tones or pronunciation | `tones` — тоновый дрилл | class + sign + syllable facts → verified tone |
| grammar or constructions | `grammar` — трансформации | rebuild, correct, extend and assemble one construction |
| spelling, reading or clusters | `spelling` — восстановление написания | transcription → script, trap pairs, gaps and corrections |
| register, address or politeness | `register` — уместность | interlocutor and situation determine the form |
| terminology or misunderstood wording | `reference` — справка | short explanation and one comprehension check |

If no mode fits, `general` assembles a mixed block from
`thai-tasks/references/exercise-catalog.md` and the tracker category should be sharpened.

→ Read **references/drill-modes.md** whenever building the drill.

→ Read **references/lexeme-memory.md** whenever mode is `lexeme`.

## Two-round rule

A repeated error gets a second round immediately, rebuilt rather than repeated.

For thematic mistakes:

- present the pattern inductively instead of repeating the same explanation;
- use a counterexample when a false rule is present;
- make operations smaller and supports stronger;
- use fresh tasks.

For `lexeme` mistakes:

- replace the hook if it did not reconstruct the spelling;
- isolate the exact unstable fragment;
- step back from whole-word production to chunks, then fade support again;
- keep the final check delayed and productive.

If the second round also fails, stop for the day. `attempt --result fail` on a second same-day
round marks the pattern `critical` and schedules it for tomorrow. More immediate repetition
creates familiarity, not durable recall.

Two clean rounds in succession resolve the pattern; its history remains in the tracker.

## Closing a topic

`thai-tasks` assembles the closing test. This workflow checks it, reports it and records the
result through `close`.

- Show the forecast-versus-result mismatch in the report.
- A correct answer marked uncertain receives quality 3 for that item, not for the whole
  topic.
- Confirm every `close` flag from the actual sheet: `--production`, `--no-hints` and
  `--calibrated`.

A resolved exact-word pattern does not by itself close or reopen a whole topic; topic gates
still use the topic's own core and closing test.

## Tracker

Run from the project root:

```bash
T=".codex/skills/thai-tasks/scripts/tracker.py"

# thematic vocabulary gap
python3 $T mistake progress.json "аайу_возраст" --category "Словарный запас" \
    --topic 2.1 --your "ฉันเอา…ปี" --correct "ฉันอายุ…ปี" \
    --context "Гл.2 срез, зад.11"

# exact learned word that repeatedly fails
python3 $T record progress.json "พฤศจิกายน" 1 --type word --topic 3.3 --item-only
python3 $T mistake progress.json "พฤศจิกายน_воспроизведение" \
    --category "Орфография" --topic 3.3 --mode lexeme \
    --your "พฤษดีกายน" --correct "พฤศจิกายน" \
    --context "срез, задание 5в"

python3 $T drill-plan progress.json
python3 $T drill-plan progress.json --topic 3.4
python3 $T drill-plan progress.json --due
python3 $T mistakes progress.json --category Тоны --limit 5
python3 $T mistake-mode progress.json "พฤศจิกายน_воспроизведение" lexeme \
    --reason "слово искажено в двух разнесённых письменных работах"

python3 $T attempt progress.json "аайу_возраст" --result ok
python3 $T attempt progress.json "аайу_возраст" --result fail \
    --context "круг 2, снова เอา"

python3 $T close progress.json 3.4 --result ok --accuracy 0.9 \
    --production --no-hints --calibrated
```

`drill-plan` returns topic, modes, learner-facing mode titles, task volume, critical status,
round information and pattern examples. It includes `vocab_pool` only for broad `vocab`
work. A `lexeme` group is built only from its listed mistake examples.

Inside a drill, run `record` for every word or rule exercised and `attempt` for every
pattern. Use `--item-only` on lexeme-memory results so a weak word does not shake the whole
topic. Pattern fields remain `topic`, `mode`, `rounds`, `drill_ok`, `last_drill` and `status`
(`active`, `critical`, `resolved`).

## Do not

- Do not produce remediation before the report and tracker update.
- Do not turn an exact-word memory lapse into a lesson on the whole topic.
- Do not use `lexeme` when several errors reveal one transferable rule.
- Do not count copying, immediate repetition or recognition as successful word recall.
- Do not ask for calibration after revealing the verdict.
- Do not reproach an admitted guess.
- Do not argue verbally with a misconception; use a counterexample.
- Do not use free composition in a live drill.
- Do not grade tones from memory.
- Do not expose tracker internals such as `frequency`, `mastery`, EF or mode names on the
  learner's sheet.
- Do not soften the report to protect a topic status.
- Do not run more than two rounds in one day.
- Do not copy examples from the course file's practice section.

## Checklist

1. Calibration was asked before the verdict or explicitly skipped by the learner.
2. The full report follows `report-format.md`, shows literal answers and supplies the full
   correct answer for every 🟡 and ❌.
3. Every tone verdict was verified.
4. Every assessed element was recorded; every error has category, topic and literal example.
5. Each error was routed as thematic, `lexeme`, misconception or reference problem from
   evidence rather than from its report category alone.
6. An exact-word gap received `--mode lexeme` and `record ... --item-only`, did not reopen
   the topic and did not pull in the whole topic vocabulary.
7. Written remediation exists as one real dated practice HTML for the report, with
   thematic and compact lexeme modules kept distinct and answers hidden.
8. Paths, names, control-named practice directories and links follow `../assessment-artifacts.md`; no
   optional link targets a future file.
9. Live work, when requested, used the correct reference and inherited the source format.
10. A misconception used a counterexample; a lexeme cycle used fading support and delayed
   production.
11. `attempt ok` used the completion criterion for its route; a failed second round stopped
    for the day.
12. The closing summary states what is resolved and what is scheduled to return.
13. Any topic-closing test was recorded with flags verified from the sheet itself.
