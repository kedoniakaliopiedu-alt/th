# Exact-word memory remediation

Read this file when the learner systematically writes the same word incorrectly, cannot
produce it without a model, or explicitly says it does not stick. This route works on the
exact lexeme and does not expand it into a lesson on the whole topic.

Instructions are English. Learner-facing prompts and the literal stored answer remain
Russian and Thai.

## Select this route

Set `--mode lexeme` only when recurring evidence shows that the exact learned word, rather
than a transferable rule, is unstable. Evidence can include:

- the same learned word is distorted in two separated later attempts or assessed works;
- productive tasks repeatedly contain `?`, «не знаю» or a blank for a previously taught
  word after unclear wording and answer format have been ruled out;
- recognition succeeds but Russian/context → exact Thai spelling fails;
- the learner says the word systematically cannot be retained.

One slip followed by confident production remains `spelling`. Several words failing through
one transferable rule remain thematic. For example, repeated `คะ / ค่ะ` choices call for a
particle lesson rather than one memory card per phrase.

Keep the report category (`Словарный запас` or `Орфография`) but store the separate route:

```bash
python3 $T mistake progress.json "พฤศจิกายน_воспроизведение" \
    --category "Орфография" --topic 3.3 --mode lexeme \
    --your "พฤษดีกายน" --correct "พฤศจิกายน" \
    --context "срез, задание 5c"
```

The route neither reopens nor blocks the broader topic by itself. Record the weak item through
`record ... --item-only`. Use `mistake-mode` to reclassify an existing pattern without
inventing another occurrence; supply the evidence in `--reason`. Reclassification does not
retroactively restore a topic state: use thematic evidence and the normal topic commands if
the broader rule itself later proves unstable.

## Identify the unstable link

Compare the literal attempt with the verified word and choose the main difficulty:

1. meaning does not retrieve the word;
2. the overall shape remains, but one internal fragment breaks;
3. two letters or fragments are confused;
4. the word is recognised but not produced.

Do not teach a rule when no transferable rule exists. Add word history, consonant class or
terminology only when it directly reconstructs the spelling.

## Memory actions

Use these actions in a compact sequence suited to the word. They are supports, not a fixed
difficulty ladder.

### Literal error trace

Show the actual stored answer beside the verified form and mark only the first relevant
difference:

```text
Твой вариант: พฤษดีกายน
Верно:       พฤศจิกายน
Первое расхождение: [выделенный фрагмент]
```

This makes the choice visible. Preserve the learner's literal historical form.

### One reconstructive hook

Choose one reliable path back to the Thai form: syllable-sized chunks, a direct contrast
between the confused fragments, a short image tied to both meaning and visible spelling, or
a personal sentence where the word naturally belongs. Do not invent etymology or attach a
mnemonic to every character.

### Fading support and handwriting

Show the correct form before memory production. Then close it and combine useful actions:

- assemble a few chunks;
- fill only the unstable fragment;
- handwrite the whole word from Russian meaning or a short situation;
- use it in a new bounded phrase.

After a failed attempt, show the whole answer, compare the relevant fragment, hide it and
reproduce it. Distribute short writing across the file rather than one copying block.

### Separated returns

Place other meaningful work between attempts and change the context on return. Use the
project tracker to decide future dates adaptively. Do not impose a fixed `1–3–7–14` calendar,
a universal attempt count or a universal mastery threshold. Recognition may accompany the
cycle but never replaces productive spelling.

## Compact self-study HTML

After a written control, create one compact memory practice for the fresh lexeme gaps. Its
placement and links follow `../../assessment-artifacts.md`. It contains:

1. target words with literal historical variants;
2. one useful hook per word;
3. reconstruction or unstable-fragment work;
4. hidden Russian/context → Thai handwriting;
5. later mixed returns after other material;
6. prepared self-check answers for every exercise.

Keep each answer in `<details>`. Inside, show the complete answer first and then a brief
explanation only if needed. The target form must not remain visible above an active recall
task. The file does not grade the learner, infer new errors or automatically create further
practice. Formal conclusions come only from a later control.

Do not add a whole-topic lecture, neighbouring vocabulary, required listening, speaking,
voice-input checks or oral repetition. If thematic gaps occurred in the same control, the
practice file may contain both compact lexeme modules and thematic modules while keeping
their scopes visibly distinct.

Minimal one-word pattern:

```html
<section class="module" aria-labelledby="month-memory">
  <h2 id="month-memory">Точечное запоминание месяца</h2>
  <p>В срезе: <span lang="th">พฤษดีกายน</span>.</p>
  <details open>
    <summary>Образец: изучи, затем закрой</summary>
    <p lang="th">พฤศจิกายน</p>
    <p>Опора: พฤศจิ + กายน.</p>
  </details>
  <div class="task">
    <p>Закрой образец и восстанови: <span lang="th">พฤ__กายน</span>.</p>
    <details><summary>Показать ответ</summary><p lang="th">พฤศจิกายน</p></details>
  </div>
  <div class="task"><p>Выполни другое задание темы.</p></div>
  <div class="task">
    <p>Напиши от руки по-тайски: «ноябрь».</p>
    <details><summary>Показать ответ</summary><p lang="th">พฤศจิกายน</p></details>
  </div>
  <p>Следующую дату возврата возьми из трекера и смени контекст.</p>
</section>
```

## Formal result

Creating or opening the practice file is not a successful attempt. On a later assessed
response, use `record ... --item-only` for the word and `attempt` for the pattern under the
existing two-round rules. Choosing, copying or assembling from fully supplied parts is not
enough evidence of independent recall.

The tracker, not this reference, decides the next interval. Reopen the broader topic only
when separate evidence shows failure of a transferable rule or several core items.
