# Drill modes

Load this file when you are assembling the drill block (step 6 of the `thai-mistakes`
pipeline). Seven modes. The mode follows from the mistake's category (`drill-plan` returns
the `mode` field), the volume from the 3+1 formula with a ceiling of 10. Inside a mode,
tasks go from simple to hard and always include рус→тай production.

Russian in this file is of two kinds and neither is an oversight: **data** — category and
mode-title strings that `tracker.py` matches on — and **anything the learner reads**.
Leave both alone.

**Common to every mode:**

- Free writing of a dialogue / text / story is **never** given, in any mode.
- Every task passes the unambiguity checklist from
  `thai-tasks/references/output-format.md`: one action verb, an explicit statement of what
  to send and in what form, a format sample, and a correct answer for every sub-item.
- **Plain, concrete wording.** No metalanguage (แม่/«мать», มาตรา, คำเป็น/คำตาย, IPA), no
  term the course has not taught; the question asks about an observable fact («на какой звук
  заканчивается», «какой значок над буквой»), and the options are real sounds, not codes.
  In a drill this matters doubly: the learner has already missed on this topic, and an
  opaque question adds a second difficulty on top of the linguistic one.
- Examples are fresh — not copied from the «Практические упражнения» section of the course
  file, but on the same topic's vocabulary and rules.
- Two or more objects in a task (words, letters, situations) mean the same number of nested
  lettered sub-items (а, б, в), so «3б» can be referred to. A comma-separated run-on does
  not count, even for short objects.
- Transcription in Cyrillic, tone mark over the vowel.
- After the round — `record` per element and `attempt` per pattern.

---

## How the drill sheet is built

These four rules cut across all modes. They come from what is measured to work on foreign
vocabulary — retrieval beats rereading, a keyword hook on top of retrieval beats retrieval
alone, interleaved topics beat blocked ones, and spaced returns beat one long sitting.
They shape the *sheet*, not the choice of mode.

**1. A hook before the drill, and only once.**

Each vocabulary block opens with a **крючок** — a card that gives the learner something to
hang the words on, then never repeats. A hook is worth giving only if it is **systemic**:
one structure that unlocks the whole set, not a pile of private associations.

Thai hands these out generously, and they are already in the course files:

| Set | Hook |
|---|---|
| Days of the week | Sanskrit planet names, the same logic as Monday ← Moon-day |
| Months | zodiac sign + ending, and the ending gives the month's length |
| Frequency markers | one scale from «всегда» to «никогда», not seven separate words |
| Periods of the day | one timeline by the clock |
| Morning verbs | the chain of actions in the order they happen |

Everything after the hook is retrieval. A second explanatory table mid-block undoes the
block: the learner reads instead of recalling.

**2. Three passes over a word, separated by other words.**

The three passes of the `vocab` mode (recognition → cloze → production) must not sit next
to each other for the same word. Between two encounters with one word there must be others
— the sheet's own ordering does the spacing. Adjacent passes turn into copying from one's
own previous line, and the effort that builds the memory never happens.

**3. A mixed block at the end.**

Inside a single-topic block the correct rule is given away by the block itself, which reads
as mastery and is not. Close the sheet with a block where **topics are deliberately
shuffled**: each item first requires working out *which* rule applies. Build it out of the
exact places where the learner lost points — it is the only block that shows the real state
of things.

Skip it in a live session (mode A): there the whole exchange is already interleaved by the
dialogue.

**4. For a self-guided sheet: hidden keys and a return schedule.**

When the drill goes out as a sheet the learner works through alone (worksheet, HTML page),
two things get added that a live session does not need:

- **The key is closed until she has answered.** In HTML that is a `<details>` toggle per
  task; on paper, the key goes on a separate page. State the rule on the sheet in Russian
  and say plainly why: reading the correct answer is not what works, the effort of recall
  is. «Не знаю» written down and then checked counts as a pass; peeking does not.
- **A schedule of returns on the sheet**, with blanks for dates: same day → +1 → +3 → +7 →
  +14, narrowing each time to what failed and to the mixed block. This is the learner-facing
  face of the same spacing the tracker runs in SM-2 — it does not replace `record`.

---

## `vocab` — запоминание слов

**When:** a wrong word choice, a forgotten word, a similar word substituted, a blank («не
знаю»). There is no rule at stake here — there is a hole in the topic's vocabulary.

**The point:** the **whole topic vocabulary** gets drilled, not the one word that failed.
Take `vocab_pool` from `drill-plan` (sorted by mastery, weakest first). A portion is
**5–7 words** per pass; a larger topic goes in portions, with a short «взято / осталось»
note between them.

**Open with the hook** (see «How the drill sheet is built», rule 1). For a set that has no
systemic hook, skip it rather than inventing associations one at a time — an arbitrary
mnemonic per word is one more thing to remember.

**Three passes over each portion:**

1. **Recognition тай→рус** — a list of Thai words, answered with the meaning.
2. **Production рус→тай** — the same meanings back, answered in Thai script (with or
   without transcription, per difficulty level).
3. **The word in a live phrase** — a short context phrase with a gap to fill; situations
   from real life (market, café, daily routine), not abstractions.

Interleave the three passes rather than running them back to back on the same word — rule 2
above.

**Criterion for «taken»:** a word counts as taken after **two correct answers in a row in
different directions** (recognition + production). Words not taken come back once more at
the end of the pass and, if missed again, go to the tracker at low quality
(`record <слово> 1`).

**Extra types when there are several portions:** sorting words into meaning groups, finding
the odd one out in a row, matching an antonym/pair from the same topic, matching word ↔
situation.

---

## `tones` — тоновый дрилл

**When:** a wrong tone, a wrong tone in transcription, falling/mid confusion and the like.

**Mandatory:** every tone, in the answer and in the key, is verified against
http://thai-language.com/dict/search. Never from memory.

**Task types:**

- **The chain «класс → знак → тип слога → тон»** over 6–10 words of the topic: per word,
  answer as «класс согласной — тоновый знак — открытый/закрытый — тон».
- **Transcription with tone** of a list of the topic's words.
- **Minimal pairs**: two words differing only in tone (e.g. ขาว / ข่าว) — give the tone and
  meaning of each.
- **Find in the list**: «выпиши слова с нисходящим тоном».
- **The reverse task**: given a tone and a meaning — pick the correct spelling of two.
- **Positional reading** (when the mistake is on finals): «как читается จ / ท / ธ в начале
  слога и в финали» — with examples from the topic.

---

## `grammar` — трансформации

**When:** word order, a particle, a construction, a classifier, a time marker, a question
form.

**Principle:** one construction from **4–5 different angles**, not five identical
substitutions.

**Task types:**

- **Rebuild the phrase**: given a correct phrase — turn it into a question / a negation /
  past / the polite form.
- **Find and fix**: a phrase carrying the same type of mistake the learner made — find it,
  fix it, explain in one line.
- **Extend by model**: a sample plus three unfinished phrases.
- **Choice of two** with a justification (the main support on a second round).
- **Assembly рус→тай**: a short phrase whole in Thai, the construction obligatory.
- **Assemble from blocks**: words given scrambled — put them in the right order.

At least one task must be productive рус→тай, but **a phrase, not a text**.

**When the mistake is a broken word order, the hook is a counterexample, not a rule.**
Take the learner's own version and run it through a case where it visibly collapses — her
`หนังสือนี้เล่ม` against «три книги», where the same slot is taken by the number. A rule
stated over a wrong rule does not land; see `misconceptions.md`.

---

## `spelling` — восстановление написания

**When:** a wrong consonant/vowel, a lost mark, a wrong consonant class, a false cluster
(จริง, สร้าง), joined/split writing.

**Task types:**

- **Write from transcription**: Cyrillic transcription + meaning given — write it in Thai
  script.
- **Trap pair**: two similar spellings (กู / คู, ลิ / ลี) — pick the right one and say how
  they differ in sound/tone.
- **Find the mistake**: the word is misspelled — find it, fix it, name what was swapped.
- **Fill the gap**: a word with a hole (`?ับ`) — restore the mark/vowel/consonant.
  Candidates by mask can be checked with `thai-handwriting/scripts/lookup.py`.
- **Syllable breakdown**: split the word into initial — vowel — final, name the class of
  the initial and the resulting tone.
- **False clusters**: a list of words where ร is silent or the cluster is not read
  literally — read them and write the transcription.

---

## `register` — регистр и уместность

**When:** a wrong form of address (คุณ instead of ป้า), the wrong gendered particle, too
bookish or too familiar, the wrong level of politeness.

This is not a «rule mistake» but a miss on the addressee. So every task is built from the
**situation and the interlocutor**.

**Task types:**

- **Who you are talking to**: 4–5 situations (an elderly market vendor, a peer colleague, a
  child, an official, a friend) — pick the address form and the particle.
- **Rewrite politer / plainer / more colloquial**: a neutral phrase, shift the register.
- **Fix the inappropriate**: a grammatically correct phrase in the wrong register — what is
  off and how to say it.
- **Situation → line**: one concrete line (not a dialogue!) for a given situation.
- **Tell the pair apart**: two phrases, same meaning, different register — say where each
  fits.

The «естественность» lens from `thai-tasks/references/checking.md` belongs here too: show
how a native speaker would put it, on its own line — that does not lower the mark.

---

## `reference` — справка без дрилла

**When:** the mistake is not linguistic but one of understanding the wording: an unfamiliar
teaching term (แม่ as «группа по конечному звуку»), a misread instruction.

A task block is **not assembled**. Instead:

1. A short explanation of the term — 2–3 lines, with an example from what is already
   covered.
2. **One** comprehension check question.
3. The term goes into the tracker as an element (`record ... --type rule`), so it surfaces
   in the spiral.

If the term is still not understood after the check question, then assemble a drill in the
mode the material itself belongs to (usually `spelling` or `tones`).

---

## `general` — смешанный

The category fitted no mode. Assemble a block from the types in
`thai-tasks/references/exercise-catalog.md` on the topic of the mistake, keeping the common
rules (volume by formula, production obligatory, no free composition). While you are at it,
sharpen the mistake's category in the tracker — `mistake --category` with a more precise
name — so the mode resolves itself next time.
