---
name: stage-done
description: Verify that a stage meets its completion criteria from realization.md and update docs/STATUS.md.
disable-model-invocation: true
argument-hint: "[stage number 1-13]"
---

Проверь завершение этапа $ARGUMENTS.

1. Прочитай критерии завершения и тесты этапа в `docs/project/realization.md`.
2. Для каждого критерия найди доказательство: запусти тесты, линтер, mypy, `make`-цели, сборку; проверь миграции (`upgrade head` и `downgrade -1`), `.env.example`, README. Ничего не считай выполненным без запуска.
3. Сверь код с чек-листом ревью из `docs/project/quality.md` и инвариантами из корневого `CLAUDE.md`.
4. Выведи таблицу: критерий | статус (выполнено / нет / частично) | доказательство.
5. Если всё выполнено — предложи обновить `docs/STATUS.md` (отметить этап, дату, что сделано, что отложено, известные долги) и коммит. Если нет — перечисли недостающее, ничего не отмечай.
6. Напомни, что на собеседовании стоит уметь объяснить в этом этапе (3–5 тем), и предложи `/interview` по ним.
