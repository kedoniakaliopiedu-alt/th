# Composing the session — stance and technique batch

Loaded once the topic and goal are known, to set the **stance** and the **technique batch** in
one step. The composer page does both, so it is the default path; chat is the fallback.

## The composer page (primary)

The generated page lives at `{S}/assets/brain-selector.html`. If the catalog changed (the CSV
or `extra-techniques.json` was edited), regenerate it first:

```bash
S=.claude/skills/skill-brainstorm
python3 $S/scripts/brain.py --extra $S/assets/extra-techniques.json \
  html --out $S/assets/brain-selector.html
```

Try to open it (`open`), then say, in one message: *«Должна открыться в браузере — собери
сессию, нажми **Скопировать промпт** и вставь результат сюда. Если не открылась — открой
`<путь>` руками или скажи "давай в чате".»* You cannot see their browser, so **never claim the
page opened.**

Read the pasted block:

| Line in the paste | Meaning |
|---|---|
| `Режим ведения: <...>` | the stance for the whole run |
| `Техники:` + numbered list | run them as given; each one's full description is in the paste, so no `list`/`show` needed |
| `(случайный выбор)` on an item | the technique was drawn at random — run it the same way |
| `придумай N новых техник на ходу` | invent N brand-new techniques on the fly. Announce the order, log each one's name + description, and at wrap-up offer to save a keeper into `{S}/assets/extra-techniques.json` |
| `придумай 1 новую технику в духе категории «X»` | invent, but honor that category's spirit |
| `выбери сам ещё N техник под мою цель` | pick N that fit the goal; confirm exact names with a scoped `list --category`. Never pull the library whole into context |

## Or in chat

If they can't open the page or would rather not, pick the stance here, then the batch. **3–4
techniques is the sweet spot.** Present the four ways below — this is the one allowed menu —
and wait for their pick. Present them in Russian.

- **Выберу я (default)** — from the goal and the `categories` map, name a batch of 3–4. Confirm
  exact names with a targeted `list --category` on only the categories you're drawing from;
  never enumerate the library to choose.
- **Посмотрю сам** — send them to the composer page after all; they tick techniques and paste
  the result back, which carries each one's full name, category and description.
- **По категориям** — the user names one or more categories; `random --category` draws the
  batch from them. No listing needed.
- **Придумай новые** — invent at least 3 techniques, announce the order before the first, touch
  no script. Log each one's name + description so you can offer to save a keeper into
  `assets/extra-techniques.json` at wrap-up.

The library is large — never pull it whole into context. The only way in is the helper, always
passing `--extra` so the project's own «методика» techniques are first-class:

```bash
S=.claude/skills/skill-brainstorm
B="python3 $S/scripts/brain.py --extra $S/assets/extra-techniques.json"

$B categories                      # names + counts; the cheap survey map
$B list --category методика        # index (name + gist) for those categories
$B random --category deep -n 4     # draw a batch blind, listing nothing
$B show "Инверсия ошибки"          # one technique's full method — call only as it runs
$B html --out <path>               # write the composer page to a file
```

Bare `list` is refused by the script, and `html` writes to a file rather than stdout: reaching
the whole library at once must always be a deliberate choice.

### Which categories fit this project

The catalog ships 13 general categories plus **`методика`** — 14 techniques written for this
repository (designing exercises and skill mechanics). Rules of thumb:

| The session is about | Reach for |
|---|---|
| a new exercise format, fixing a recurring mistake | `методика` first, then `constraint` |
| a skill's instruction being misread or too vague | `методика` (Аудит одной строки, Провал скилла, Триггерный стресс-тест) |
| structuring a topic or chapter | `structured`, `deep` |
| the session feels stale, everything sounds the same | `wild`, `absurdist`, `theatrical` |
| a decision about direction, not a format | `deep`, `introspective_delight` |

Mixing one `методика` technique with one wild one is usually stronger than four sober ones: the
project-specific technique grounds the batch, the wild one breaks the obvious answer.

## Running the batch

Whichever path set it, once the stance is known: create the memlog (`init`, with
`--field mode=`) and **load that stance's frame** for the rest of the run — Facilitator →
`mode-facilitator.md`, Creative Partner → `mode-partner.md`, Ideate for me →
`mode-autonomous.md`. Tell the user the memlog path: state is on disk now, so the session
survives an interruption.

(In **Ideate for me** you pick and run techniques yourself — see `mode-autonomous.md`.)

Run each technique until it stops producing — log each idea, and log the switch itself as a
`technique` entry when you move on — then announce the new lens and let the change of technique
do the domain-shifting. When the batch is spent, offer three paths: another batch, **converge**
(`converge.md`), or wrap up (`finalize.md`).
