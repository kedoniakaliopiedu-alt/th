# Standalone thematic HTML modules

Use this workflow by default after a written control, worksheet, or review with errors. The checked report remains the evidence; the remediation is delivered immediately as files and does not wait for the learner to answer in chat.

## Core rule

An error identifies a root topic. It does not define the boundary of the lesson. Group related errors by the smallest useful root topic, then build one standalone module per topic. The original answer appears only in the opening block **Почему эта тема появилась**:

- the learner's literal answer;
- the full correct answer;
- the root topic revealed by the error.

After that block, teach the topic as if the triggering error did not exist. A module fails quality review if it would not work as an independent lesson.

## Research before writing

For every substantial module:

1. read the relevant chapter files;
2. verify meanings and constructions in reliable dictionaries and educational references;
3. compare several independent sources for a complex distinction;
4. check that every Thai example is natural;
5. separate chapter essentials from useful extensions.

The chapter is the starting point, not the ceiling. Do not add academic detail that does not help practical use. Do not grade tones without `thai-verify`.

## Required lesson structure

Use the sections that apply, in this order:

1. **Почему эта тема появилась**.
2. **Что это такое**: a simple idea, then a precise explanation.
3. **Главное значение**.
4. **Формула**: a visible `A + B + C` pattern and the role of every part.
5. **Базовые примеры**: Thai, Russian translation, and a short analysis; highlight the target form.
6. **Как это работает в разных ситуациях**: statements, questions, negation, answers, or other genuinely relevant variants.
7. **Когда используется** with examples.
8. **Когда не используется** with a natural replacement.
9. **⚠️ Не путай**: a comparison table followed by a prose explanation and contrastive examples.
10. **Порядок слов**, including a correct pattern and a typical Russian-transfer error when relevant.
11. **Разговорный тайский**: textbook, neutral, colloquial, and formal variants only where the distinction matters. Mark what the learner should actively use and what is recognition-only.
12. **⚠️ Типичные ошибки**: several errors from learners in general, not just the triggering answer.
13. **Исключения и ограничения**, split into **Обязательно запомнить** and **Полезно знать**.

For broad topics label material as **🟢 Основа**, **🟡 Расширение**, and **🔵 Дополнительно**.

## Practice and built-in checking

Practice covers the whole lesson: meaning, position, contrasts, Russian-to-Thai production, correction, choice by meaning, a new spoken context, a suitable answer, and independent construction. It is not limited by `drill-plan`'s interactive task count.

Every task must contain a closed disclosure answer, implemented in HTML with `<details>` and a visible `<summary>Показать ответ</summary>`. Inside use:

- **✅ Ответ** or **Один естественный вариант**;
- **Почему**;
- **Что проверить в своём ответе**;
- **Также возможно** when several natural answers exist.

Do not imply that only one phrase is correct. Free production is allowed here because the learner self-checks against criteria and natural examples; provide a bounded situation and explicit checklist.

End with **🧠 После изучения этой темы я должна уметь**, listing observable skills, followed by a mixed final check that tests those exact skills.

## Artifact rules

- Create actual `.html` files next to the source chapter or review; never paste raw HTML into chat.
- For several topics create an `index.html` linking all modules.
- Use the project's dark visual style, readable Thai type, responsive layout, print styles, and keyboard-accessible native controls.
- Keep answers hidden initially without requiring a server.
- Include a short sources section with chapter files and external links used for research.
- Open every file in a browser and inspect desktop and narrow layouts before delivery.

Generating these files does not count as a successful drill attempt and must not close a tracker pattern. Record `attempt` only after the learner demonstrates the skill in an assessed session.

## Interactive exception

If the learner explicitly asks to work live in chat, use the interactive drill workflow in `drill-modes.md`: diagnosis, explanation, new tasks, feedback, and `attempt`. Do not mix that workflow with the self-study HTML format.
