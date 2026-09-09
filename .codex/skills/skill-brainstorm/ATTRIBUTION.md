# Attribution

Адаптировано из [BMAD Method](https://github.com/bmad-code-org/bmad-method),
скилл `src/core-skills/bmad-brainstorming`. Лицензия MIT.

## Что взято как есть

| Файл | Источник в BMAD |
|---|---|
| `scripts/memlog.py` | `src/scripts/memlog.py` — снят заголовок `# /// script` (запускается через `python3`, не через `uv`) |
| `scripts/brain.py` | `src/core-skills/bmad-brainstorming/scripts/brain.py` — добавлен `from __future__ import annotations` (Python 3.8+ вместо 3.10+); страница композера переведена на русский; добавлена таблица `CATEGORY_LABELS`; категория «методика» добавлена в надгруппы |
| `assets/brain-methods.csv` | без изменений — 108 техник |
| `assets/brain-icons.json` | без изменений |

## Что написано для этого проекта

- `SKILL.md` и все файлы `references/` — переписаны под мета-задачу: штурм по механикам
  скиллов и методике заданий, а не по продуктовым фичам. Убрана инфраструктура BMAD
  (`_bmad/config.toml`, `customize.toml`, `resolve_customization.py`, запуск через `uv`),
  вместо неё — прямые пути внутри репозитория.
- `assets/extra-techniques.json` — 14 техник категории «методика», написанных под этот
  проект. Подмешиваются в каталог через `--extra`, поэтому равноправны везде: в списках,
  в случайных выборках и на странице композера.
- Журнал сессии переведён с BMAD-поля `status: complete` на запись
  `(event) сессия завершена` — так требует актуальный контракт `memlog.py`.

## Лицензия оригинала

```
MIT License

Copyright (c) 2025 BMad Code, LLC

This project incorporates contributions from the open source community.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

BMad™, BMad Method™ и BMad Core™ — товарные знаки BMad Code, LLC. Скиллы этого
репозитория названы `skill-*` и знаков не используют.
