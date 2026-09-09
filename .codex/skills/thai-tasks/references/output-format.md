# Sheet layout and task wording

Read this file whenever you assemble a worksheet, a test or any sheet the user sees whole.
Two blocks: **how the sheet is laid out** and **how a single item is worded**. The worksheet
template and the order of blocks are in `scope-and-modes.md`.

Instructions here are English; everything quoted as an example is Russian, because that is
what lands on the learner's page. Do not "fix" the Russian parts.

## Sheet formatting

The sheet must read easily. Presentation rules:

- **Block headings are lettered.** «Блок A» / «Блок B» / «Блок C» in order; a descriptive
  name only in parentheses and only if you want one: «Блок B (Сборка)». No methodological
  commentary on the sheet itself.
- **Numbering restarts inside every block.** Every block begins at item 1 — there is no
  running numbering across the sheet. Because «1» therefore occurs in every block, a
  reference must always carry the block letter. Reference format —
  `Блок {Буква}.Задание {N}`, or `Блок {Буква}.Задание {N}.Пункт {Буква}` when the item has
  sub-points. Examples: `Блок B.Задание 2`, `Блок A.Задание 4.Пункт Б`. Use that format both
  in the task and when reviewing answers.
- **Count the objects: two or more means that many lettered sub-points.** This is the rule
  broken most often, so apply it mechanically rather than by feel. Take the item and count
  what the user has to work on separately — words, letters, syllables, phrases, situations.
  Two or more → each one is its own nested point lettered а, б, в, … There are **no
  exceptions for short objects**: a row of four single letters is still four sub-points, and
  a set does not stop being a set because it fits on one line. Never separate cases with
  commas, dots or dashes inside the instruction line. The instruction stays on the numbered
  line; the material moves down.

  > Плохо: «2. Раздели на среднеклассовые и непарные низкоклассовые: อ, ว, ฎ, ย, ป, ง».
  >
  > Хорошо:
  >
  > 2. Раздели буквы на две группы — среднеклассовые и непарные низкоклассовые:
  >    - а) **อ**
  >    - б) **ว**
  >    - в) **ฎ**

  The point is not neatness. She answers by reference — «Блок A.Задание 4.Пункт Б» — and a
  flat line has nothing to refer to, so both her answer and the review lose their anchors.
- **Lists are real markdown lists, not a flat line.** Items — a numbered list; material
  inside an item — nested points. A blank line before any list (CommonMark), otherwise it
  will not render. Example of a fully laid-out item:

  > 4. Какое обращение подойдёт?
  >    - а) к пожилой продавщице → ?
  >    - б) к министру → ?
  >    - в) к официанту моложе тебя → ?
- **Present vocabulary cleanly:** `**тайское**` (bold, large) · *transcription in italics* —
  translation. One word per line, or as a list. **Do not use the consonant-class colouring
  from thai-display** (in chat it turns into junk coloured "beads" with a legend and looks
  bad). Apply thai-display only when the user **explicitly asks** for a consonant-class
  breakdown.
- **Do not output methodological plumbing** (spiral percentages, mastery, source links) on a
  learning sheet — that is internal. The sheet is pure tasks.
- Thai text inside a task — large and legible (bold), transcription — italic.
- **Transcription is strictly Cyrillic, no Latin and no Latin look-alikes.** The tone mark
  (` ˆ ´ ˇ) sits **over the vowel** of the syllable, not over the consonant. A frequent
  error is the mark sliding onto the final consonant with a Latin character substituted.
  Correct: **ตื่น** → *ты̀н* (mark over ы). Wrong: *тыǹ* (Latin ǹ, mark on н). If you are
  unsure of the tone or the spelling, verify it (thai-phonetics + thai-language.com) — do
  not invent. See skill **thai-phonetics**.

Once answers arrive, review them by the checking rules from `thai-learning` (hint →
explanation → the rule in one sentence; a test has no hints).

## Wording the task itself (so it is unambiguous)

A vague wording kills the practice. Run every item through this checklist before issuing it.

1. **One action verb.** Прочитай / переведи / напиши по-тайски / собери / ответь / определи /
   преобразуй. Do not merge two actions into one item («прочитай и заодно придумай ещё три
   слова» is two tasks).
2. **It says explicitly WHAT to send and IN WHAT FORM.** Thai script? Cyrillic
   transcription? A translation? All of it? Do not make her guess the answer format.
3. **A sample format is shown** when it is not obvious. For example: «Ответ в виде: тайское
   слово — транскрипция — перевод».
4. **It is clear what counts as a complete answer.** For productive items state the volume
   and the required elements: «Собери диалог из 3 реплик, в каждой — частица вежливости».
5. **One focus.** The item tests one thing (for atomic items) or one connected set (for
   composite ones). More foci than that — split into sub-points.
6. **No metalanguage in the question.** Never make her *name a category by its linguistic
   name*. Details and the ban list — the section below.
7. **Plain, concrete words throughout.** Not only the ban list: the whole wording is
   everyday Russian a person with no linguistic training reads once and acts on. Ask about
   what can be seen or heard — «на какой звук заканчивается», «какая буква написана
   первой», «над какой буквой стоит значок» — rather than about a category, a rule name, or
   a property. No terms she has not been taught in this course, no abstractions
   («охарактеризуй», «определи природу», «проанализируй структуру»), no chains of
   subordinate clauses. If a term is genuinely needed, replace it with its plain-language
   description; if that makes the item unwieldy, the item is aimed at the wrong thing.
8. **Every sub-point actually has a correct answer.** Before issuing, answer each item
   yourself. The typical failure is a list assembled by theme rather than by validity — e.g.
   asking for the final sound of ฝ, which never occurs as a final at all, so the sub-point
   has no answer. If a sub-point has none, replace it, do not ship it.

Плохо: «Поработай с едой и тонами».
Хорошо: «Напиши по-тайски "я хочу рис" (ฉันอยากกินข้าว). Затем определи тон слова ข้าว
и объясни одним предложением, почему он такой. Ответ: тайская фраза + тон + причина».

Unfamiliar words or constructions inside a task get the ⚑ marker by the rule from
`thai-learning` — that is a reference note, not a hint, and it does not relax the checking.

### Plain language, no metalanguage

The user does not know the linguistic names of categories, and the wording itself is what
blocks her: «определи „мать“ (แม่กก / กด / กบ …)» leaves her unsure what a «мать» is, what
the codes in brackets are, and what she is being asked to do. Do not ask for the name, and
do not try to teach the name inside the task either — that turns one item into a lecture.

**The test before issuing an item:** read it as someone who knows Thai words but no grammar
terminology. Is it obvious what to do and what to send back? If the answer is «obvious once
you know what X means» — rewrite it. A person stuck on the *wording* learns nothing about
Thai; that turn is spent entirely on decoding the question, and the item's difficulty stops
measuring what it was supposed to measure.

Three habits that keep wording plain:

- **Ask about the visible or the audible**, not about a property: «какой значок стоит над
  словом», «на какой звук оно заканчивается», «какая буква первая» — not «определи тип»,
  «охарактеризуй», «в чём особенность».
- **Offer real options rather than codes**: `-к, -т, -п` and not `แม่กก / แม่กด / แม่กบ`;
  «высокий / низкий / средний» spelled out and not letters or numbers of the class.
- **One short sentence for the instruction, one for the format.** A long compound sentence
  with «при этом», «учитывая, что», «в случае если» is a rewrite signal, not a precision
  gain.

Ask about the **observable fact** — what sound is heard at the end of the word, which mark
is written, where the tone mark sits — in plain language, and offer ready answer options
made of real sounds rather than codes.

Terms that must not appear in a task's wording: **แม่ / «мать»** (finals group), **มาตรา**,
**สระ / วรรณยุกต์** as terms, **อักษรกลาง/สูง/ต่ำ** in Thai (Russian «средний / высокий /
низкий класс» is fine — that one she has learned), **แม่ก กา**, **คำเป็น / คำตาย** (say
«открытый / закрытый слог» instead), IPA notation.

Плохо: «Определи „мать“ (แม่กก / กด / กบ / กง / กน / กม / เกย / เกอว): а) รัก …».
Хорошо: «На какой звук заканчивается каждое слово? Выбери из: -к, -т, -п, -нг, -н, -м,
-й, -в. а) **รัก** *рак* → ? б) **บิน** *бин* → ?».

One caveat on that «Хорошо» example: give the transcription only when the item is not about
reading. Where the task is precisely to work out the final sound from the script, the
transcription hands over the answer — drop it there.
