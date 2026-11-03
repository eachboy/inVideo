# Backend (FastAPI, модульный монолит)

Спецификация: `docs/project/architecture.md` (3.3 БД, 3.4 слои, 3.5 API) и `logic_of_operation.md` (процессы). Правила по типам файлов (БД, API, сервисы, пайплайн, тесты, auth) лежат в `.claude/rules/` и подгружаются сами.

## Команды (из каталога `backend/`)

- `uv sync` — зависимости
- `uv run pytest` — все тесты; `uv run pytest -m "not slow"` — без медленных (FFmpeg, e2e)
- `uv run ruff check .` и `uv run ruff format --check .` — линт и формат
- `uv run mypy app` — типы (strict)
- `uv run alembic revision --autogenerate -m "..."` — только черновик миграции, затем прочитать и поправить руками
- `uv run alembic upgrade head` / `uv run alembic downgrade -1`
- `uv run uvicorn app.main:app --reload` — обычно через `make up`
- `uv run celery -A app.workers.celery_app worker -Q video -c 1 -l info` — воркер видео

## Структура

- `app/main.py` — фабрика приложения, middleware, обработчики ошибок; `app/api_router.py` — сборка роутеров под `/api/v1`.
- `app/core/` — config (pydantic-settings), database, models_base, redis, storage (два S3-клиента), security, errors, logging, pagination, rate_limit, metrics.
- `app/modules/<name>/` — router, schemas, service, repository, models, dependencies, exceptions (+ policies, tasks, status по необходимости).
- `app/workers/` — `celery_app.py`, `beat_schedule.py`, синхронная сессия БД `db.py`. Сами задачи живут в модулях.
- `scripts/` — `seed_data.py` (в т.ч. 100 тыс. видео-записей для EXPLAIN), `create_admin.py`.
- `tests/` — `unit/` (чистые функции), `integration/` (репозитории и сервисы), `api/` (HTTPX), `workers/` (FFmpeg). Фикстуры видео генерируются FFmpeg, бинарников в Git нет.

## Слои

- **Router**: принять и провалидировать запрос, получить зависимости, вызвать один метод сервиса, вернуть схему. Без SQL и бизнес-правил.
- **Service**: правила, политики доступа, транзакции, оркестрация репозиториев и адаптеров. Бросает доменные исключения, не знает про HTTP.
- **Repository**: запросы с говорящими именами. Не коммитит, не проверяет права. У каждого модуля свой, без универсального базового класса.
- **Адаптеры** (storage, cache, queue, telegram): тонкие обёртки; в тестах подменяются.
- Чистые функции без ввода-вывода (переходы статусов, лесенка качеств, оценка рекомендаций, правила дедупликации) вынесены отдельно и покрыты unit-тестами; ими пользуются и API, и воркеры.

## Сессии БД

- API: async engine, asyncpg, сессия на запрос с откатом при исключении, `expire_on_commit=False`.
- Воркеры: синхронный engine, psycopg, короткие сессии на этап.
- Суммарный размер пулов API и воркеров меньше лимита соединений PostgreSQL. Для роли приложения — `statement_timeout` и таймаут простоя в транзакции.

## Формат API

- Ошибка: HTTP-код, машиночитаемый код (`EMAIL_TAKEN`), сообщение, `request_id`. Ошибки Pydantic приводятся к тому же формату.
- Список: `items` и `next_cursor` (пустой, если страниц больше нет); `limit` по умолчанию 20, максимум 50.
- Время в ISO 8601 UTC, идентификаторы — строки.

## Celery

Очереди: `video` (воркер с concurrency 1), `default`, `notifications`. JSON-сериализация, в задачу передаётся только идентификатор. Подтверждение после выполнения, prefetch 1. Подробности — в `.claude/rules/video-pipeline.md`.

## Логи

structlog в JSON; обязательные поля: `event`, `request_id`, `user_id`; в пайплайне — `video_id`, `job_id`, этап. `request_id` передаётся в Celery через заголовки задачи. Пароли, токены, подписи и заголовок Authorization маскируются.
