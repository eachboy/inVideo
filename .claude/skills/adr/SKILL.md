---
name: adr
description: Write an Architecture Decision Record in docs/adr/ for a significant technical decision.
disable-model-invocation: true
argument-hint: "[decision title]"
---

Оформи решение «$ARGUMENTS» как ADR.

1. Посмотри `docs/adr/`: определи следующий номер (`NNNN-kebab-title.md`) и не дублируй существующие решения. Если каталога нет — создай.
2. Узнай у меня контекст, если он неясен из разговора; не выдумывай причины.
3. Шаблон (на английском):
   - **Status** (Proposed / Accepted / Superseded by NNNN)
   - **Date**
   - **Context** — проблема и ограничения
   - **Options considered** — 2–3 варианта с плюсами и минусами
   - **Decision** — что выбрано
   - **Consequences** — что стало проще, что сложнее, что придётся пересмотреть
4. Если решение меняет `docs/project/`, напомни мне об этом и предложи правку; сам файлы документации не меняй.
5. Объём — не больше одной страницы.
