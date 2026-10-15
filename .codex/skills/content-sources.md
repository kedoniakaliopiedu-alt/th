# Content source contract

This is the shared evidence contract for authoring or substantially revising Thai course
material. Follow it when writing a lesson; `thai-tasks` uses it while
building the lesson's exercises and controls. It does not replace the source boundaries in
`RESOURCES.md`: thai-language.com remains the only authority for tones, and a written
control remains restricted to what the course files already teach.

## Match the source to the claim

Do not use one convenient website as evidence for every kind of claim. A source supports
only the role for which it is suitable:

| Claim or authoring need | Preferred evidence | What it does not prove alone |
|---|---|---|
| spelling, senses, part of speech, usage label | Kaikki/Wiktextract or Thai Wiktionary; thai-language.com when required by `RESOURCES.md` | naturalness of a complete new sentence |
| standard grammar and word order | UD Thai-TUD or Thai-PUD; LST20/ORCHID when their access terms permit | everyday conversational register |
| long-form rule explanation or competing analysis | a modern reference grammar or a topic-specific thesis; historical Noss/FSI only as secondary evidence | current register, learner level, or machine-readable Thai |
| exercise mechanic and progression | FSI drills or another lawful pedagogical source | permission to copy its Thai, transcription, answer, or historical register |
| dataset discovery and annotation design | ACL, TNC, UD, OPUS, WangchanBERTa or PyThaiNLP papers | a learner-facing rule or natural example |
| short neutral example or translation prompt | Tatoeba Thai, checked manually; selected OPUS parallel corpora | dictionary meaning, tone, or universal acceptability |
| bilingual translation exercise | Tatoeba sentence links or a licence-checked OPUS subcorpus | that every alignment is human or pedagogically suitable |
| cloze or word-order exercise | Tatoeba, Thai Wikipedia, UD Thai or LST20 | the learner's level; filter vocabulary before use |
| reading comprehension | Thai Wikipedia, Thai QA or ThaiSum | conversational usage |
| formal or encyclopedic context | Thai Wikipedia, ThaiSum, GlobalVoices | ordinary conversation |
| conversational or social-media register | Wisesight, Pantip, Dek-D, or a suitable dialogue corpus | standard spelling or formal acceptability |
| dialogue-like context | Pantip or Dek-D; OpenSubtitles only after checking the subcorpus rights | a clean sentence boundary or neutral register |
| sentiment and opinion | Wisesight or Wongnai | general language frequency outside their domains |
| technical and interface language | Blognone, GNOME, KDE or Ubuntu corpora | household or general conversational usage |
| frequency or broad collocation | a sufficiently large, named corpus such as Wikipedia, CulturaX, OSCAR or CC100 | correctness by itself |

The catalogue supplied by the user is a discovery guide, not an authority. Verify that the
named dataset and URL still exist, read its current description and licence, and prefer the
official project page or repository. For example, the current public UD treebanks are
Thai-TUD and Thai-PUD; do not preserve a stale catalogue name merely because it was listed.

## Minimum source profile for a course topic

For a new or substantially revised topic, use evidence from every applicable row below:

1. **Lexicon:** one structured dictionary source for new meanings and register labels.
2. **Grammar:** one annotated corpus or specialist grammar source for each central
   construction.
3. **Examples:** one sentence corpus for short neutral contexts; inspect the sentence
   itself because community corpora can contain mistakes.
4. **Register:** one register-matched source whenever the lesson teaches colloquial,
   formal, social-media, youth, technical or dialogue language.

This is role coverage, not a quota of links. A topic with no register distinction may need
three source families; a topic about colloquial particles needs a fourth. Two pages from
the same site are still one source family and do not provide independent evidence.

Record an internal evidence ledger before drafting:

```text
claim: พี่ and น้อง can be terms of address
lexicon: Kaikki/Wiktionary — senses and conversational label
grammar/example: Tatoeba — manually checked short uses
register: conversational
decision: teach as a contextual option, not a universal replacement for คุณ
```

The final topic footer lists source roles in Russian so later revisions remain auditable:

```html
<footer class="topic-sources">
  <p><strong>Источники проверки материала</strong></p>
  <ul>
    <li><a href="…">Kaikki / Wiktionary</a> — значения и пометы регистра</li>
    <li><a href="…">UD Thai-TUD</a> — порядок слов и конструкции</li>
    <li><a href="…">Tatoeba Thai</a> — короткие нейтральные контексты</li>
  </ul>
</footer>
```

Do not expose the ledger, corpus counts, licence analysis or research process in the lesson.
The footer is provenance, not a bibliography dump: include only sources actually consulted
for that topic and state their role.

## Long-form grammars, courses and theses

Long-form sources support an analysis; they do not replace the role-based minimum above.
Use a reference grammar when a short corpus pattern needs an explanation, and use a thesis
only when its actual subject matches the construction being taught. Record the edition,
page, access status and rights with the claim so another revision can reproduce the decision.

Noss and the FSI Thai Basic Course are historical secondary sources. They can supply a
competing grammatical analysis, a drill mechanic or a progression, but every current Thai
claim must be checked against a modern lexicon, annotated corpus and register-matched
examples. Their checked scans are not machine-readable Thai: FSI Vol. 1–2 are image-only,
and the checked Noss copy exposes noisy English OCR but no Thai Unicode. Never bulk-import
that OCR or silently repair it. Keep the page image and verify every Thai sign manually.

External romanization never enters course material. Rebuild any required Cyrillic
transcription through `thai-phonetics`, because Noss and FSI use systems that do not encode
the project's choices. A historical example is rewritten as a fresh level-appropriate
example after modern verification; it is not copied into practice or a control.

Repository availability is not a reuse licence. An in-copyright thesis may inform an
internal paraphrase with a page citation, but its text is not added to a redistributable
corpus. Papers about corpora and NLP are discovery sources: use them to choose data or
understand annotations, never as the sole evidence for a Thai rule or sentence. The tested
book inventory and extraction results are recorded in
`../research/thai-open-books-audit-2026-10-15.md`.

## From corpus evidence to learner material

1. Confirm the word and intended sense in the lexicon.
2. Retrieve multiple examples from a corpus suited to the intended register.
3. Reject examples with doubtful spelling, machine-alignment artefacts, unknown grammar,
   unnecessary vocabulary or a different sense of the word.
4. Infer the reusable pattern from the remaining evidence. A corpus hit shows attestation;
   it does not by itself prove a rule or the only possible order.
5. Write a fresh A2/B1-level example in the same register. Do not copy a corpus sentence
   into an exercise merely because it is authentic.
6. Check the fresh example against the taught vocabulary and construction, then solve every
   exercise and control item internally.

Separate registers explicitly. Preserve at least the conceptual fields `source`,
`source_url`, `register`, `orthography` and `licence` in research notes or the evidence
ledger. Do not present noisy social-media spelling as neutral standard Thai, and do not
rewrite a genuine conversational form into an academic form merely because it is informal.

## Rights and quotation

Use open datasets according to their current licence and attribution rules. Publicly
readable text is not automatically reusable: Pantip and similar sites may support pattern
analysis, but their posts are not copied into course files. For mixed-rights OPUS corpora,
inspect the selected subcorpus before use. Prefer freshly written examples grounded in
attested patterns; quote only when the exact text is pedagogically necessary, short, and
lawfully reusable.

## Controls

External corpora validate the lesson during authoring. They do not expand an assessment's
scope. A control may test only vocabulary and constructions already taught in the named
course files. When a source review changes a meaning, register boundary or central rule,
revise the material first and then rebuild the affected dated control under
`assessment-artifacts.md`. A source-footer or link-only change does not require a new
control.
