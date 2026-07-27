# Step 4: present and act

## RULES

- Speak Russian to the user. The report file is written in Russian.
- `решение` findings are resolved **before** `правка` findings are handled.
- Nothing is modified until the user picks an option.

## INSTRUCTIONS

### 1. Clean review shortcut

If zero findings survived triage, say so and skip to section 5.

### 2. Write the report

Write `{report}` = `.claude/reviews/ревью-{target}-{ГГГГ-ММ-ДД}.md` (create
`.claude/reviews/` if missing). If a file with that name exists, append a new
`## Прогон <время>` section rather than overwriting it.

```markdown
# Ревью: {target} — {дата}

**Что ревьюили:** <файлы / диапазон> · **Режим:** <с замыслом | без замысла>
**Слои:** <перечень запущенных> · **Не отработали:** <или «—»>
**Итог:** <D> решений · <P> правок · <W> отложено · <R> отсеяно как шум

## Требуют решения

- [ ] **<Заголовок>** — <описание> · `<файл>:<строка>` · важность: <высокая|средняя|низкая>
      Варианты: <а> / <б>

## Правки

- [ ] **<Заголовок>** · `<файл>:<строка>` · важность: <...>
      <в чём дефект и каким должен быть верный вариант>

## Отложено

- [x] **<Заголовок>** · `<файл>:<строка>` — существовало до этих изменений
```

Order matters: `решение`, then `правка`, then `отложить` — most-blocking first.

Also append each `отложить` finding to `{deferred}` = `.claude/reviews/отложено.md`, under
a heading `## Из ревью: {target} ({дата})`, one bullet each. This is the standing list of
known-but-parked problems; a later review that rediscovers one should recognize it here and
not re-file it.

### 3. Present the summary

> **Ревью готово.** <D> требуют решения, <P> правок, <W> отложено, <R> отсеяно как шум.
> Отчёт: `{report}`

Then list the `high` findings inline — she should not have to open a file to learn that
something is seriously wrong.

### 4. Resolve, then fix

**First, `решение` findings.** Present each with its detail and the real options. She
decides; the fix is genuinely ambiguous without her. Walk through them one at a time, or
batch clearly related ones. Each resolved finding becomes a `правка`, an `отложить`, or is
dismissed.

If she defers one, ask for a one-line reason and append it to both `{report}` and
`{deferred}` — a parked item without a reason gets re-litigated every review.

**HALT** after presenting the options. Wait for her answer; do not proceed.

**Then, `правка` findings.** HALT and ask:

> **Что делаем с правками (<P>)?**
> 1. **Применить все** — чиню всё сразу, без подтверждения по каждой. Отложенное и то, что
>    требовало решения, не трогаю.
> 2. **Оставить как список задач** — они уже записаны в `{report}`
> 3. **Пройти по каждой** — показываю детали, решаешь по одной

**HALT** — wait for the number. Do not proceed until she picks.

- **Применить все** — apply every `правка`, touching nothing in the other buckets. Then
  present a summary of what changed and check the items off in `{report}`.
- **Оставить как список** — done, they are already in the report.
- **Пройти по каждой** — show each finding with full context and the proposed fix, then
  re-offer the options above. **HALT** again for the choice.

**A rule specific to this repository:** when a fix changes a `SKILL.md` frontmatter
`description`, it changes *when the skill fires*. Never apply that silently as part of
«применить все» — surface it separately and confirm, even if the wording fix itself looked
unambiguous.

### 5. Close out

Update `{report}`: check off what was fixed, leave the rest. Then:

> **Ревью завершено.**
> Исправлено: <N> · Осталось задачами: <M> · Отложено: <W> · Отсеяно: <R>
> Отчёт: `{report}`

### 6. Clean up what is spent

The report is a working document, not an archive: it earns its place while findings are
still open. When every finding has been fixed or dismissed and `{deferred}` holds nothing,
it stops being a resource — the reasoning that mattered belongs in the commit message by
then, not in a file nobody opens.

So when the last finding closes, **offer to remove what is spent**, and say what dies:

> Все находки закрыты, парковка пуста. Отчёт `{report}` больше ни на что не влияет —
> удалить? Если он закоммичен, вернётся из истории: `git show <sha>:<путь>`.

Rules for that offer:

- **Offer, never delete on your own.**
- **Only when nothing is open.** A report with unchecked boxes is the task list — leave it.
- **`{deferred}` outlives the report** whenever it still holds parked findings: it is the
  standing list a later review checks so it does not re-file them. Delete it only when it
  is empty.
- **Say what is recoverable** — committed files come back from git, uncommitted ones do not.

### 7. Next steps

Offer, in Russian:

1. **Переписать что-то целиком** — a finding that turned out to be a structural problem
   goes to `skill-writer`, not to a patch;
2. **Поштурмить решение** — an ambiguous `решение` finding that nobody knows how to answer
   goes to `skill-brainstorm`;
3. **Перезапустить ревью** — after fixes, to confirm nothing new broke;
4. **Готово.**

**HALT** and wait for her choice.
