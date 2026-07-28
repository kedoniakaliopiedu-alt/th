# Choosing techniques in chat

Loaded only when the user won't use the composer page (no browser, or they declined). Here
you pick the batch in conversation. **3–4 is the sweet spot.** Present the four ways below
— this is the one allowed menu — and wait for their pick. Present them in Russian.

- **Выберу я (default)** — from the goal and the `categories` map, name a batch of 3–4.
  Confirm exact names with a targeted `list --category` on only the categories you're
  drawing from; never enumerate the library to choose.
- **Посмотрю сам** — send them to the composer page after all (`## Running a session` in
  `SKILL.md`); they tick techniques and paste the result back, which carries each one's
  full name, category and description.
- **По категориям** — the user names one or more categories; `random --category` draws the
  batch from them. No listing needed.
- **Придумай новые** — invent at least 3 techniques, announce the order before the first,
  touch no script. Log each one's name + description so you can offer to save a keeper into
  `assets/extra-techniques.json` at wrap-up.

The library is large — never pull it whole into context. The only way in is the helper,
always passing `--extra` so the project's own «методика» techniques are first-class:

```bash
S=.claude/skills/skill-brainstorm
B="python3 $S/scripts/brain.py --extra $S/assets/extra-techniques.json"

$B categories                      # names + counts; the cheap survey map
$B list --category методика        # index (name + gist) for those categories
$B random --category deep -n 4     # draw a batch blind, listing nothing
$B show "Инверсия ошибки"          # one technique's full method — call only as it runs
$B html --out <path>               # write the composer page to a file
```

Bare `list` is refused by the script, and `html` writes to a file rather than stdout:
reaching the whole library at once must always be a deliberate choice.

## Which categories fit this project

The catalog ships 13 general categories plus **`методика`** — 14 techniques written for
this repository (designing exercises and skill mechanics). Rules of thumb:

| The session is about | Reach for |
|---|---|
| a new exercise format, fixing a recurring mistake | `методика` first, then `constraint` |
| a skill's instruction being misread or too vague | `методика` (Аудит одной строки, Провал скилла, Триггерный стресс-тест) |
| structuring a topic or chapter | `structured`, `deep` |
| the session feels stale, everything sounds the same | `wild`, `absurdist`, `theatrical` |
| a decision about direction, not a format | `deep`, `introspective_delight` |

Mixing one `методика` technique with one wild one is usually stronger than four sober ones:
the project-specific technique grounds the batch, the wild one breaks the obvious answer.
