# Собрать схему (СХ)

Loaded when a diagram carries more signal than prose: skill relationships, the flow of a
lesson, how data moves through `progress.json`, the state of a mistake being worked off.

All labels in Russian. Mermaid renders in the repository's Markdown viewers, so the diagram
goes straight into the document.

## When a diagram is actually better

Reach for one when the subject has **more than three moving parts and the relationships
matter more than the details**. Do not diagram a linear procedure — a numbered list is
clearer and diffs better. `.codex/skills/MAP.md` currently draws the skill graph as an
ASCII tree; a Mermaid version is an improvement only if the graph has stopped being a tree.

## Choosing the type

| Subject | Type |
|---|---|
| which skill calls which, who owns what | `flowchart LR` |
| the course of a lesson: task → answer → check → drill | `flowchart TD` |
| a hand-off between skills over time (tasks → mistakes → tracker) | `sequenceDiagram` |
| the life of a mistake: новая → в отработке → снята → рецидив → critical | `stateDiagram-v2` |
| chapter and topic hierarchy | `flowchart TD` or a Markdown list — prefer the list unless there is cross-linking |

## Rules

- **Nodes are nouns, edges are verbs.** `thai-tasks -->|передаёт ход| thai-mistakes`, not an
  unlabelled arrow. An unlabelled edge in a skill graph is exactly the ambiguity the diagram
  was supposed to remove — the README already makes this point about
  `tasks → mistakes` being a hand-off, not a subordination.
- **One diagram, one question.** If it needs a legend, it is two diagrams.
- **Quote labels containing spaces, punctuation or Cyrillic**: `A["Работа над ошибками"]`.
  Avoid parentheses inside unquoted labels — they break the parser.
- **Node ids stay ASCII**, labels are Russian: `mistakes["thai-mistakes — работа над
  ошибками"]`. Cyrillic ids work in some renderers and not others.
- **Cap it around a dozen nodes.** Beyond that, split by subsystem.
- **No styling** unless it carries meaning. If colour marks something, say what in a caption.

## Verify before delivering

Mermaid fails silently in some viewers — a broken diagram renders as nothing, and nobody
notices for months. Before handing it over:

- reread the syntax for unquoted parentheses, stray `|`, and edges referencing undeclared
  nodes;
- confirm every node in the diagram exists in reality — a skill that was renamed, a script
  that moved;
- state plainly that you could not render it yourself, and ask her to confirm it displays.

## Output

A fenced ```mermaid block, plus one or two sentences in Russian saying what the diagram
shows and what it deliberately leaves out. If it is going into an existing document, say
which section it replaces — a diagram added next to the prose it duplicates leaves two
sources to keep in sync.
