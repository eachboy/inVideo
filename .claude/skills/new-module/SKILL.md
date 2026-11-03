---
name: new-module
description: Scaffold a new backend module (router, schemas, service, repository, models, dependencies, exceptions) with a test skeleton.
disable-model-invocation: true
argument-hint: "[module name, e.g. comments]"
---

Создай каркас backend-модуля `$ARGUMENTS`.

1. Сверься с `docs/project/repository.md` (структура модулей) и `architecture.md` 3.4: какие файлы нужны именно этому модулю.
2. Создай `backend/app/modules/$ARGUMENTS/` с файлами `__init__.py`, `router.py`, `schemas.py`, `service.py`, `repository.py`, `models.py`, `dependencies.py`, `exceptions.py` (`policies.py`, `tasks.py` и т. д. — только если модуль их требует по документации).
3. Каркас минимальный: классы и сигнатуры с докстрингами, без выдуманной логики. Никаких универсальных базовых классов.
4. Подключи роутер в `app/api_router.py`. Модели добавь в импорт `alembic/env.py`.
5. Создай `backend/tests/api/test_$ARGUMENTS.py` и `tests/integration/test_${ARGUMENTS}_repository.py` с одним падающим по делу тестом-заглушкой, помеченным `xfail` с причиной.
6. Не создавай миграцию автоматически: предложи команду и покажи, что должно в ней оказаться.
7. Запусти `ruff` и `mypy`, покажи результат и кратко объясни, как слои этого модуля связаны.
