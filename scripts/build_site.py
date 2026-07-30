#!/usr/bin/env python3
"""Сборка HTML-сайта курса из markdown-файлов тем.

Читает `Thai A2/` и `Thai B1/`, кладёт результат в `site/`:

    site/index.html          — уровни (A2, B1) и справочники
    site/<level>/index.html  — главы уровня со списком тем
    site/<level>/<tema>.html — сама тема

Только стандартная библиотека. Запуск: python3 scripts/build_site.py
"""

from __future__ import annotations

import html
import re
import shutil
import unicodedata
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"


# ── Модель курса ──────────────────────────────────────────────────────


class Topic(NamedTuple):
    source: Path
    slug: str
    number: str  # «1.2» — из заголовка или имени файла
    title: str  # «Согласные»
    summary: str  # первая цитата-цель темы, если есть


class Chapter(NamedTuple):
    number: str
    title: str
    topics: List[Topic]
    extras: List[Tuple[str, str]]  # (подпись, относительная ссылка) — контрольные


class Level(NamedTuple):
    slug: str  # «a2»
    name: str  # «A2»
    caption: str
    source_dir: Path
    plan: Optional[Path]
    chapters: List[Chapter]


LEVEL_CAPTIONS = {
    "A2": "Алфавит, тоны, базовое общение и бытовые темы",
    "B1": "Фонетика связной речи и словообразование",
}


# ── Markdown → HTML ───────────────────────────────────────────────────

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def inline(text: str) -> str:
    """Жирный, курсив, код и ссылки внутри строки."""
    out = html.escape(text, quote=False)
    out = _INLINE_CODE.sub(lambda m: "<code>%s</code>" % m.group(1), out)
    out = _BOLD.sub(lambda m: "<strong>%s</strong>" % m.group(1), out)
    out = _ITALIC.sub(lambda m: "<em>%s</em>" % m.group(1), out)
    out = _LINK.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), out)
    return out


def slugify(text: str) -> str:
    """Идентификатор для якоря: латиница и цифры, остальное — дефис."""
    # NFC, а не NFKD: разложение ломает кириллические й/ё и тайские знаки.
    plain = unicodedata.normalize("NFC", text)
    keep = [c if (c.isalnum() or c in "-_.") else "-" for c in plain.lower()]
    return re.sub(r"-+", "-", "".join(keep)).strip("-") or "x"


class Section(NamedTuple):
    anchor: str
    title: str


def render_markdown(lines: List[str]) -> Tuple[str, List[Section]]:
    """Возвращает HTML тела и оглавление по заголовкам второго уровня."""
    out: List[str] = []
    toc: List[Section] = []
    seen: Dict[str, int] = {}
    i = 0
    n = len(lines)

    def anchor_for(title: str) -> str:
        base = slugify(title)
        seen[base] = seen.get(base, 0) + 1
        return base if seen[base] == 1 else "%s-%d" % (base, seen[base])

    while i < n:
        raw = lines[i].rstrip("\n")
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        # Код без подсветки — блоки с тайскими примерами
        if stripped.startswith("```"):
            i += 1
            block: List[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                block.append(lines[i].rstrip("\n"))
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(block), quote=False))
            continue

        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
            out.append("<hr>")
            i += 1
            continue

        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            if level == 1:  # заголовок темы уже стоит в шапке страницы
                i += 1
                continue
            anchor = anchor_for(title)
            if level == 2:
                toc.append(Section(anchor, title))
            out.append(
                '<h%d id="%s">%s<a class="anchor" href="#%s" aria-hidden="true">#</a></h%d>'
                % (level, anchor, inline(title), anchor, level)
            )
            i += 1
            continue

        # Таблица
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = split_row(stripped)
            i += 2
            body: List[List[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                body.append(split_row(lines[i].strip()))
                i += 1
            out.append(render_table(header, body))
            continue

        # Цитата
        if stripped.startswith(">"):
            quote: List[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            body_html = "<br>".join(inline(x) for x in quote if x)
            out.append("<blockquote>%s</blockquote>" % body_html)
            continue

        # Список
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", raw):
            block_lines: List[str] = []
            while i < n and (
                re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]) or lines[i].strip() == ""
            ):
                if lines[i].strip() == "":
                    # пустая строка внутри списка обрывает его, если дальше не пункт
                    if i + 1 < n and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i + 1]):
                        i += 1
                        continue
                    break
                block_lines.append(lines[i].rstrip("\n"))
                i += 1
            out.append(render_list(block_lines))
            continue

        # Абзац
        para: List[str] = []
        while i < n and lines[i].strip() and not is_block_start(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))

    return "\n".join(out), toc


def is_block_start(line: str) -> bool:
    s = line.strip()
    return (
        s.startswith(("#", ">", "|", "```"))
        or bool(re.match(r"^\s*([-*+]|\d+[.)])\s+", line))
        or bool(re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s))
    )


def split_row(row: str) -> List[str]:
    cells = row.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def render_table(header: List[str], body: List[List[str]]) -> str:
    head = "".join("<th>%s</th>" % inline(c) for c in header)
    rows: List[str] = []
    for r in body:
        cells = "".join("<td>%s</td>" % inline(c) for c in r)
        rows.append("<tr>%s</tr>" % cells)
    return (
        '<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
        % (head, "".join(rows))
    )


def render_list(block: List[str]) -> str:
    """Список с одним уровнем вложенности."""
    items: List[str] = []
    ordered = bool(re.match(r"^\s*\d+[.)]\s+", block[0]))
    nested: List[str] = []

    def flush_nested() -> None:
        if not nested or not items:
            return
        items[-1] = items[-1] + render_list(nested)
        nested.clear()

    for line in block:
        indent = len(line) - len(line.lstrip(" "))
        text = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", line)
        if indent >= 2 and items:
            nested.append(line.lstrip(" "))
            continue
        flush_nested()
        items.append(inline(text))
    flush_nested()

    tag = "ol" if ordered else "ul"
    return "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % it for it in items), tag)


# ── Разбор структуры курса ────────────────────────────────────────────

_TITLE_RE = re.compile(r"^#\s*(?:Глава\s*(\d+)\s*·\s*)?Тема\s*([\d.]+)\s*[—-]\s*(.+)$")


def read_topic(path: Path) -> Topic:
    lines = path.read_text(encoding="utf-8").splitlines()
    number = ""
    title = path.stem
    for line in lines[:5]:
        m = _TITLE_RE.match(line.strip())
        if m:
            number = m.group(2)
            title = m.group(3).strip()
            break
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if not number:
        m = re.search(r"tema(\d+)", path.stem)
        number = m.group(1) if m else ""
    summary = ""
    for line in lines[:12]:
        if line.strip().startswith(">"):
            summary = re.sub(r"^Цель темы:\s*", "", line.strip().lstrip(">").strip())
            summary = summary[:1].upper() + summary[1:]
            break
    return Topic(path, slugify(path.stem), number, title, summary)


def read_level(name: str, slug: str) -> Level:
    src = ROOT / ("Thai " + name)
    plan = next(iter(sorted(src.glob("*_plan.md"))), None)
    names = chapter_names(plan)
    chapters: List[Chapter] = []
    for chapter_dir in sorted(src.glob("Chapter *"), key=chapter_key):
        num = chapter_dir.name.split()[-1]
        topics = [read_topic(p) for p in sorted(chapter_dir.glob("*.md"))]
        if not topics:
            continue
        extras: List[Tuple[str, str]] = []
        for extra in sorted(chapter_dir.glob("*.html")):
            label = extract_title(extra) or extra.stem
            rel = "../../%s/%s/%s" % (src.name, chapter_dir.name, extra.name)
            extras.append((label, rel))
        chapters.append(Chapter(num, names.get(num, ""), topics, extras))
    return Level(slug, name, LEVEL_CAPTIONS.get(name, ""), src, plan, chapters)


def chapter_key(path: Path) -> int:
    m = re.search(r"(\d+)", path.name)
    return int(m.group(1)) if m else 0


_CHAPTER_RE = re.compile(r"^#{2,4}\s*\W*\s*Глава\s*(\d+)\s*[.—–-]\s*(.+?)\s*$")


def chapter_names(plan: Optional[Path]) -> Dict[str, str]:
    """Названия глав берём из плана уровня — своего файла у главы нет."""
    if plan is None:
        return {}
    found: Dict[str, str] = {}
    for line in plan.read_text(encoding="utf-8").splitlines():
        m = _CHAPTER_RE.match(line.strip())
        if m:
            found.setdefault(m.group(1), m.group(2))
    return found


def extract_title(path: Path) -> str:
    m = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8"), re.S)
    return html.unescape(m.group(1).strip()) if m else ""


# ── Шаблоны страниц ───────────────────────────────────────────────────


def page(title: str, css_depth: int, body: str, cls: str = "") -> str:
    css = "../" * css_depth + "assets/style.css"
    return """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css}">
</head>
<body class="{cls}">
{body}
<script>
  (function () {{
    var key = "thai-theme";
    var root = document.documentElement;
    var saved = localStorage.getItem(key);
    if (saved) root.setAttribute("data-theme", saved);
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {{
      var dark = root.getAttribute("data-theme") === "dark"
        || (!root.getAttribute("data-theme")
            && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem(key, next);
    }});
  }})();
</script>
</body>
</html>
""".format(title=html.escape(title), css=css, cls=cls, body=body)


def toggle() -> str:
    return '<button class="theme-toggle" type="button" title="Светлая / тёмная тема">◐</button>'


def plural(n: int, one: str, few: str, many: str) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "%d %s" % (n, one)
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "%d %s" % (n, few)
    return "%d %s" % (n, many)


def build_index(levels: List[Level], helpers: List[Topic]) -> str:
    cards: List[str] = []
    for lv in levels:
        topics_total = sum(len(c.topics) for c in lv.chapters)
        cards.append(
            """<a class="level-card" href="{slug}/index.html">
  <span class="level-badge">{name}</span>
  <span class="level-caption">{caption}</span>
  <span class="level-meta">{ch} · {tp}</span>
</a>""".format(
                slug=lv.slug,
                name=html.escape(lv.name),
                caption=html.escape(lv.caption),
                ch=plural(len(lv.chapters), "глава", "главы", "глав"),
                tp=plural(topics_total, "тема", "темы", "тем"),
            )
        )

    helper_items = "".join(
        '<li><a href="helpers/%s.html">%s</a></li>' % (t.slug, html.escape(t.title))
        for t in helpers
    )
    helpers_block = (
        '<section class="block"><h2>Справочники</h2><ul class="plain">%s</ul></section>' % helper_items
        if helpers
        else ""
    )

    body = """<div class="wrap home">
  <header class="head">
    <div class="eyebrow">Курс тайского языка</div>
    <h1>Тайский<span class="sub">материалы курса по уровням</span></h1>
    {toggle}
  </header>
  <section class="levels">{cards}</section>
  {helpers}
</div>""".format(toggle=toggle(), cards="".join(cards), helpers=helpers_block)
    return page("Тайский — курс", 0, body, "home-page")


def build_level(level: Level) -> str:
    blocks: List[str] = []
    for ch in level.chapters:
        items: List[str] = []
        for t in ch.topics:
            items.append(
                """<li><a class="topic" href="{slug}.html">
  <span class="topic-num">{num}</span>
  <span class="topic-body"><span class="topic-title">{title}</span>{sum}</span>
</a></li>""".format(
                    slug=t.slug,
                    num=html.escape(t.number),
                    title=html.escape(t.title),
                    sum='<span class="topic-sum">%s</span>' % inline(t.summary) if t.summary else "",
                )
            )
        for label, href in ch.extras:
            items.append(
                '<li><a class="topic extra" href="%s"><span class="topic-num">К</span>'
                '<span class="topic-body"><span class="topic-title">%s</span></span></a></li>'
                % (href, html.escape(label))
            )
        blocks.append(
            """<section class="chapter">
  <h2><span class="chapter-num">Глава {num}</span>{title}</h2>
  <ul class="topics">{items}</ul>
</section>""".format(
                num=html.escape(ch.number),
                title='<span class="chapter-title">%s</span>' % html.escape(ch.title) if ch.title else "",
                items="".join(items),
            )
        )

    plan_link = (
        '<a class="crumb-extra" href="plan.html">План уровня</a>' if level.plan else ""
    )
    body = """<div class="wrap">
  <nav class="crumbs"><a href="../index.html">← Уровни</a>{plan}</nav>
  <header class="head">
    <div class="eyebrow">Уровень {name}</div>
    <h1>{name}<span class="sub">{caption}</span></h1>
    {toggle}
  </header>
  {blocks}
</div>""".format(
        plan=plan_link,
        name=html.escape(level.name),
        caption=html.escape(level.caption),
        toggle=toggle(),
        blocks="".join(blocks),
    )
    return page("Тайский %s" % level.name, 1, body)


def build_topic(
    level: Level, chapter: Chapter, topic: Topic, prev: Optional[Topic], nxt: Optional[Topic]
) -> str:
    lines = topic.source.read_text(encoding="utf-8").splitlines()
    content, toc = render_markdown(lines)

    toc_html = ""
    if len(toc) > 1:
        items = "".join('<li><a href="#%s">%s</a></li>' % (s.anchor, html.escape(s.title)) for s in toc)
        toc_html = '<nav class="toc"><div class="toc-label">На странице</div><ul>%s</ul></nav>' % items

    nav: List[str] = []
    if prev:
        nav.append('<a class="prev" href="%s.html">← %s</a>' % (prev.slug, html.escape(prev.title)))
    if nxt:
        nav.append('<a class="next" href="%s.html">%s →</a>' % (nxt.slug, html.escape(nxt.title)))

    body = """<div class="wrap topic-page">
  <nav class="crumbs">
    <a href="../index.html">Уровни</a>
    <a href="index.html">{level}</a>
    <span>Глава {ch}</span>
  </nav>
  <header class="head">
    <div class="eyebrow">Тема {num}</div>
    <h1>{title}</h1>
    {toggle}
  </header>
  {toc}
  <article class="prose">{content}</article>
  <nav class="pager">{nav}</nav>
</div>""".format(
        level=html.escape(level.name),
        ch=html.escape(chapter.number),
        num=html.escape(topic.number),
        title=html.escape(topic.title),
        toggle=toggle(),
        toc=toc_html,
        content=content,
        nav="".join(nav),
    )
    return page("%s — %s" % (topic.number, topic.title), 1, body)


def build_doc(path: Path, title: str, back: str, back_label: str, depth: int) -> str:
    content, toc = render_markdown(path.read_text(encoding="utf-8").splitlines())
    toc_html = ""
    if len(toc) > 1:
        items = "".join('<li><a href="#%s">%s</a></li>' % (s.anchor, html.escape(s.title)) for s in toc)
        toc_html = '<nav class="toc"><div class="toc-label">На странице</div><ul>%s</ul></nav>' % items
    body = """<div class="wrap topic-page">
  <nav class="crumbs"><a href="{back}">← {back_label}</a></nav>
  <header class="head">
    <h1>{title}</h1>
    {toggle}
  </header>
  {toc}
  <article class="prose">{content}</article>
</div>""".format(
        back=back,
        back_label=html.escape(back_label),
        title=html.escape(title),
        toggle=toggle(),
        toc=toc_html,
        content=content,
    )
    return page(title, depth, body)


# ── Сборка ────────────────────────────────────────────────────────────


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)

    levels = [read_level("A2", "a2"), read_level("B1", "b1")]
    helpers = [read_topic(p) for p in sorted((ROOT / "Helpers").glob("*.md"))]

    write(OUT / "assets" / "style.css", STYLE)
    write(OUT / "index.html", build_index(levels, helpers))

    pages = 0
    for level in levels:
        write(OUT / level.slug / "index.html", build_level(level))
        pages += 1
        flat = [(ch, t) for ch in level.chapters for t in ch.topics]
        for idx, (chapter, topic) in enumerate(flat):
            prev = flat[idx - 1][1] if idx > 0 else None
            nxt = flat[idx + 1][1] if idx + 1 < len(flat) else None
            write(
                OUT / level.slug / (topic.slug + ".html"),
                build_topic(level, chapter, topic, prev, nxt),
            )
            pages += 1
        if level.plan:
            write(
                OUT / level.slug / "plan.html",
                build_doc(level.plan, "План уровня %s" % level.name, "index.html", level.name, 1),
            )
            pages += 1

    for helper in helpers:
        write(
            OUT / "helpers" / (helper.slug + ".html"),
            build_doc(helper.source, helper.title, "../index.html", "Главная", 1),
        )
        pages += 1

    print("site: %d страниц" % (pages + 1))


STYLE = """
:root {
  --paper: #f4f5f7;
  --card: #fbfbfc;
  --ink: #151c26;
  --ink-soft: #4d5866;
  --ink-faint: #8b95a3;
  --rule: #d7dce4;
  --rule-soft: #e6eaf0;
  --accent: #26497d;
  --accent-soft: #e6ecf6;
  --gold: #8a6420;
  --gold-soft: #f3ecdd;
  --shadow: 0 1px 0 rgba(21, 28, 38, .04), 0 12px 32px -20px rgba(21, 28, 38, .35);

  --serif: "Charter", "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}

@media (prefers-color-scheme: dark) {
  :root {
    --paper: #0e131a;
    --card: #151b24;
    --ink: #e7ebf1;
    --ink-soft: #a9b3c1;
    --ink-faint: #6f7a89;
    --rule: #2a323d;
    --rule-soft: #212933;
    --accent: #8fb0e4;
    --accent-soft: #1b2635;
    --gold: #d5ac66;
    --gold-soft: #262015;
    --shadow: 0 12px 32px -22px #000;
  }
}

:root[data-theme="dark"] {
  --paper: #0e131a;
  --card: #151b24;
  --ink: #e7ebf1;
  --ink-soft: #a9b3c1;
  --ink-faint: #6f7a89;
  --rule: #2a323d;
  --rule-soft: #212933;
  --accent: #8fb0e4;
  --accent-soft: #1b2635;
  --gold: #d5ac66;
  --gold-soft: #262015;
  --shadow: 0 12px 32px -22px #000;
}

:root[data-theme="light"] {
  --paper: #f4f5f7;
  --card: #fbfbfc;
  --ink: #151c26;
  --ink-soft: #4d5866;
  --ink-faint: #8b95a3;
  --rule: #d7dce4;
  --rule-soft: #e6eaf0;
  --accent: #26497d;
  --accent-soft: #e6ecf6;
  --gold: #8a6420;
  --gold-soft: #f3ecdd;
  --shadow: 0 1px 0 rgba(21, 28, 38, .04), 0 12px 32px -20px rgba(21, 28, 38, .35);
}

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--sans);
  font-size: 17px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

a { color: var(--accent); }

.wrap {
  max-width: 48rem;
  margin: 0 auto;
  padding: clamp(1.25rem, 4vw, 3rem) clamp(1rem, 4vw, 2rem) 5rem;
}

/* ── Шапка ─────────────────────────────────────────── */

.head {
  position: relative;
  padding-bottom: 1.5rem;
  margin-bottom: 2.25rem;
  border-bottom: 2px solid var(--ink);
}

.eyebrow {
  font-family: var(--mono);
  font-size: .72rem;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--gold);
  display: flex;
  align-items: center;
  gap: .55rem;
  margin-bottom: .9rem;
}

.eyebrow::before {
  content: "";
  width: .5rem;
  height: .5rem;
  border: 1.5px solid currentColor;
  border-radius: 50%;
}

.head h1 {
  font-family: var(--serif);
  font-size: clamp(1.9rem, 5.5vw, 2.9rem);
  line-height: 1.08;
  font-weight: 600;
  letter-spacing: -.015em;
  text-wrap: balance;
  margin: 0;
}

.head h1 .sub {
  display: block;
  font-family: var(--sans);
  font-size: .34em;
  font-weight: 400;
  letter-spacing: .01em;
  line-height: 1.4;
  color: var(--ink-soft);
  margin-top: .8rem;
}

.theme-toggle {
  position: absolute;
  top: 0;
  right: 0;
  width: 2.2rem;
  height: 2.2rem;
  border: 1px solid var(--rule);
  border-radius: 50%;
  background: var(--card);
  color: var(--ink-soft);
  font-size: 1rem;
  cursor: pointer;
}

.theme-toggle:hover { color: var(--ink); border-color: var(--ink-faint); }

/* ── Навигация ─────────────────────────────────────── */

.crumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: .5rem;
  font-family: var(--mono);
  font-size: .74rem;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 1.75rem;
}

.crumbs a { color: var(--ink-soft); text-decoration: none; }
.crumbs a:hover { color: var(--accent); }
.crumbs > * + *::before { content: "/"; margin-right: .5rem; color: var(--rule); }
.crumbs .crumb-extra { margin-left: auto; color: var(--accent); }
.crumbs .crumb-extra::before { content: none; }

.pager {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 3.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--rule);
  font-size: .9rem;
}

.pager a { text-decoration: none; color: var(--ink-soft); }
.pager a:hover { color: var(--accent); }
.pager .next { margin-left: auto; text-align: right; }

/* ── Главная: уровни ───────────────────────────────── */

.levels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: 1rem;
}

.level-card {
  display: flex;
  flex-direction: column;
  gap: .4rem;
  padding: 1.6rem 1.5rem;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: .5rem;
  box-shadow: var(--shadow);
  text-decoration: none;
  color: inherit;
  transition: border-color .15s, transform .15s;
}

.level-card:hover { border-color: var(--accent); transform: translateY(-2px); }

.level-badge {
  font-family: var(--serif);
  font-size: 2.4rem;
  font-weight: 600;
  line-height: 1;
  color: var(--accent);
}

.level-caption { color: var(--ink-soft); }

.level-meta {
  font-family: var(--mono);
  font-size: .72rem;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--ink-faint);
}

.block { margin-top: 3rem; }

.block h2 {
  font-family: var(--mono);
  font-size: .74rem;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--ink-faint);
  border-bottom: 1px solid var(--rule);
  padding-bottom: .5rem;
}

ul.plain { list-style: none; padding: 0; margin: 0; }
ul.plain li { padding: .35rem 0; }

/* ── Уровень: главы и темы ─────────────────────────── */

.chapter { margin-bottom: 2.75rem; }

.chapter h2 {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: .75rem;
  margin: 0 0 .75rem;
  font-size: 1.2rem;
  font-weight: 600;
  border-bottom: 1px solid var(--rule);
  padding-bottom: .5rem;
}

.chapter-num {
  font-family: var(--mono);
  font-size: .74rem;
  font-weight: 600;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--gold);
}

.chapter-title { font-family: var(--serif); letter-spacing: -.01em; }

.topics { list-style: none; margin: 0; padding: 0; }

.topic {
  display: flex;
  gap: 1rem;
  align-items: baseline;
  padding: .85rem 1rem;
  border: 1px solid transparent;
  border-radius: .4rem;
  text-decoration: none;
  color: inherit;
}

.topic:hover { background: var(--card); border-color: var(--rule); }

.topic-num {
  flex: none;
  min-width: 2.6rem;
  font-family: var(--mono);
  font-size: .85rem;
  color: var(--ink-faint);
  font-variant-numeric: tabular-nums;
}

.topic-body { display: flex; flex-direction: column; gap: .2rem; }
.topic-title { font-weight: 500; }

.topic-sum {
  font-size: .88rem;
  color: var(--ink-soft);
  line-height: 1.45;
}

.topic.extra .topic-num { color: var(--gold); }
.topic.extra .topic-title { color: var(--accent); }

/* ── Оглавление темы ───────────────────────────────── */

.toc {
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: .4rem;
  padding: 1rem 1.25rem;
  margin-bottom: 2.5rem;
}

.toc-label {
  font-family: var(--mono);
  font-size: .68rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: .5rem;
}

.toc ul { list-style: none; margin: 0; padding: 0; }
.toc li { padding: .18rem 0; }
.toc a { text-decoration: none; }
.toc a:hover { text-decoration: underline; }

/* ── Текст темы ────────────────────────────────────── */

.prose h2 {
  font-family: var(--serif);
  font-size: 1.65rem;
  font-weight: 600;
  letter-spacing: -.01em;
  margin: 3rem 0 1rem;
  padding-bottom: .4rem;
  border-bottom: 1px solid var(--rule);
}

.prose h3 {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 2.2rem 0 .75rem;
  color: var(--accent);
}

.prose h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 1.6rem 0 .5rem;
  color: var(--ink-soft);
}

.prose .anchor {
  margin-left: .4rem;
  font-size: .7em;
  color: var(--rule);
  text-decoration: none;
  opacity: 0;
}

.prose h2:hover .anchor,
.prose h3:hover .anchor,
.prose h4:hover .anchor { opacity: 1; }

.prose p { margin: 0 0 1rem; }
.prose ul, .prose ol { margin: 0 0 1.15rem; padding-left: 1.4rem; }
.prose li { margin: .3rem 0; }
.prose li > ul, .prose li > ol { margin: .3rem 0 .3rem; }

.prose hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 2.5rem 0;
}

.prose blockquote {
  margin: 0 0 1.25rem;
  padding: .85rem 1.15rem;
  background: var(--accent-soft);
  border-left: 3px solid var(--accent);
  border-radius: 0 .3rem .3rem 0;
  color: var(--ink-soft);
}

.prose code {
  font-family: var(--mono);
  font-size: .88em;
  background: var(--rule-soft);
  border-radius: .25rem;
  padding: .1em .35em;
}

.prose pre {
  overflow-x: auto;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: .4rem;
  padding: 1rem 1.15rem;
  margin: 0 0 1.4rem;
  line-height: 1.7;
}

.prose pre code {
  background: none;
  padding: 0;
  font-size: .92rem;
  white-space: pre;
}

.table-wrap {
  overflow-x: auto;
  margin: 0 0 1.5rem;
  border: 1px solid var(--rule);
  border-radius: .4rem;
}

.prose table {
  border-collapse: collapse;
  width: 100%;
  font-size: .95rem;
}

.prose th, .prose td {
  text-align: left;
  padding: .55rem .8rem;
  border-bottom: 1px solid var(--rule-soft);
  border-right: 1px solid var(--rule-soft);
  vertical-align: top;
}

.prose th:last-child, .prose td:last-child { border-right: 0; }

.prose thead th {
  background: var(--card);
  font-family: var(--mono);
  font-size: .7rem;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--ink-faint);
  border-bottom: 1px solid var(--rule);
  border-right-color: var(--rule);
  white-space: nowrap;
}

.prose tbody tr:last-child td { border-bottom: 0; }
.prose tbody tr:hover { background: var(--card); }
"""


if __name__ == "__main__":
    main()
