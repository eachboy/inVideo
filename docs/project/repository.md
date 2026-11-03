# Часть IV. Структура репозитория

Один репозиторий (монорепозиторий) с backend, frontend, инфраструктурой, e2e-тестами и документацией. Для одного разработчика это проще всего: одна история изменений, один CI, атомарные изменения API и фронтенда в одном коммите.

Воркеры **не** выделены в отдельный проект: они используют те же модели, конфигурацию и сервисы, что и API. Отдельная директория `workers` с копией кода привела бы к дублированию. Поэтому код задач живёт в модулях backend, а в `backend/app/workers` — только точка входа Celery и расписание. Образ один, но собирается в двух вариантах: API (без FFmpeg) и воркер (с FFmpeg).

## Дерево директорий

```text
invideo/
├── README.md
├── Makefile
├── .env.example
├── .gitignore
├── .editorconfig
├── .pre-commit-config.yaml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── app/
│   │   ├── main.py
│   │   ├── api_router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── models_base.py
│   │   │   ├── redis.py
│   │   │   ├── storage.py
│   │   │   ├── security.py
│   │   │   ├── errors.py
│   │   │   ├── logging.py
│   │   │   ├── pagination.py
│   │   │   ├── rate_limit.py
│   │   │   └── metrics.py
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── models.py
│   │   │   │   ├── dependencies.py
│   │   │   │   └── exceptions.py
│   │   │   ├── users/
│   │   │   ├── channels/
│   │   │   ├── subscriptions/
│   │   │   ├── uploads/
│   │   │   ├── videos/
│   │   │   │   ├── ...
│   │   │   │   ├── policies.py
│   │   │   │   └── status.py
│   │   │   ├── processing/
│   │   │   │   ├── tasks.py
│   │   │   │   ├── pipeline.py
│   │   │   │   ├── probe.py
│   │   │   │   ├── transcode.py
│   │   │   │   ├── ladder.py
│   │   │   │   ├── thumbnails.py
│   │   │   │   └── sweepers.py
│   │   │   ├── views/
│   │   │   ├── reactions/
│   │   │   ├── comments/
│   │   │   ├── playlists/
│   │   │   ├── history/
│   │   │   ├── search/
│   │   │   ├── recommendations/
│   │   │   │   ├── ...
│   │   │   │   ├── candidates.py
│   │   │   │   └── scoring.py
│   │   │   ├── studio/
│   │   │   ├── notifications/
│   │   │   │   ├── ...
│   │   │   │   └── telegram.py
│   │   │   └── admin/
│   │   └── workers/
│   │       ├── celery_app.py
│   │       ├── beat_schedule.py
│   │       └── db.py
│   ├── scripts/
│   │   ├── seed_data.py
│   │   └── create_admin.py
│   └── tests/
│       ├── conftest.py
│       ├── factories.py
│       ├── fixtures/
│       │   └── media/
│       ├── unit/
│       ├── integration/
│       ├── api/
│       └── workers/
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── index.html
│   ├── Dockerfile
│   ├── public/
│   └── src/
│       ├── main.tsx
│       ├── app/
│       │   ├── router.tsx
│       │   └── providers.tsx
│       ├── api/
│       │   ├── client.ts
│       │   └── schema.gen.ts
│       ├── features/
│       │   ├── auth/
│       │   ├── player/
│       │   ├── upload/
│       │   ├── videos/
│       │   ├── comments/
│       │   ├── channels/
│       │   ├── playlists/
│       │   ├── search/
│       │   ├── history/
│       │   ├── notifications/
│       │   └── studio/
│       ├── pages/
│       ├── components/
│       │   ├── ui/
│       │   └── layout/
│       ├── stores/
│       ├── lib/
│       ├── styles/
│       └── test/
├── e2e/
│   ├── playwright.config.ts
│   ├── fixtures/
│   └── tests/
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx/
│   │   ├── nginx.conf
│   │   ├── conf.d/
│   │   └── snippets/
│   ├── postgres/
│   │   └── init/
│   ├── storage/
│   │   └── init-buckets.sh
│   ├── monitoring/
│   │   ├── prometheus/
│   │   │   ├── prometheus.yml
│   │   │   └── alerts.yml
│   │   └── grafana/
│   │       ├── provisioning/
│   │       └── dashboards/
│   └── scripts/
│       ├── deploy.sh
│       ├── backup.sh
│       └── restore.sh
└── docs/
    ├── architecture.md
    ├── runbook.md
    ├── adr/
    └── diagrams/
```

## Назначение директорий

### Корень

| Путь | Назначение |
| --- | --- |
| README.md | Витрина проекта: что это, скриншоты, архитектурная схема, стек, как запустить одной командой, ссылки на документацию. Первое, что откроет работодатель |
| Makefile | Короткие команды: поднять окружение, остановить, миграции, тесты, линтеры, генерация типов API, сид данных |
| .env.example | Все переменные окружения с безопасными значениями-заглушками и комментариями. Настоящий .env в Git не попадает |
| .pre-commit-config.yaml | Ruff, mypy, проверка форматирования фронтенда, поиск случайно закоммиченных секретов |
| .github/workflows | ci.yml — линтеры, тесты, сборка образов на каждый push и pull request; deploy.yml — деплой на VPS из main |

### backend

| Путь | Назначение |
| --- | --- |
| pyproject.toml, uv.lock | Зависимости и настройки инструментов (Ruff, mypy, pytest, coverage) |
| Dockerfile | Многоэтапная сборка с двумя целями: api и worker (в воркер добавляется FFmpeg). Непривилегированный пользователь |
| alembic/ | Окружение миграций и сами миграции в versions/ |
| app/main.py | Фабрика приложения: middleware, обработчики ошибок, подключение роутеров, события старта и остановки |
| app/api\_router.py | Сборка роутеров всех модулей под префиксом /api/v1 |
| app/core/ | Общая инфраструктура, не относящаяся к конкретной предметной области: настройки, подключение к БД, базовый класс моделей, клиенты Redis и S3, JWT и хеширование, исключения, логирование, пагинация, rate limiting, метрики |
| app/modules/ | Предметные модули (см. 3.4). Набор файлов одинаков: router, schemas, service, repository, models, плюс специфичные файлы (policies, status, tasks) |
| app/modules/processing/ | Весь пайплайн обработки видео: задачи Celery, шаги пайплайна, запуск FFprobe и FFmpeg, расчёт лесенки, превью, подметальщики зависших задач |
| app/workers/ | Точка входа Celery: настройка приложения и очередей, маршрутизация задач, расписание Beat, синхронная сессия БД для воркеров |
| scripts/ | Генерация тестовых данных (пользователи, каналы, тысячи видео-заглушек для проверки поиска) и создание администратора |
| tests/ | Все Python-тесты: unit (чистые функции без БД), integration (репозитории и сервисы с настоящей БД), api (endpoint-ы через HTTPX), workers (пайплайн на маленьких тестовых видео). fixtures/media — короткие тестовые ролики на несколько секунд и заведомо битые файлы |

### frontend

| Путь | Назначение |
| --- | --- |
| src/app/ | Маршрутизация и провайдеры (TanStack Query, тема) |
| src/api/ | HTTP-клиент с автоматическим обновлением access-токена и сгенерированные из OpenAPI типы |
| src/features/ | Код по функциональным областям: компоненты, хуки запросов, логика. Например, upload — многочастная загрузка с прогрессом и докачкой; player — обёртка над hls.js, сохранение позиции, событие просмотра |
| src/pages/ | Страницы-маршруты, которые собирают фичи: главная, просмотр, канал, поиск, история, Studio |
| src/components/ | Переиспользуемые UI-компоненты (кнопки, поля, модальные окна, карточка видео) и раскладка (шапка, боковое меню) |
| src/stores/ | Небольшое клиентское состояние (Zustand): токен в памяти, текущий пользователь, настройки плеера |
| src/lib/, src/styles/ | Утилиты (форматирование длительности, чисел, дат) и стили, токены дизайна |
| src/test/ | Настройка тестов и обработчики MSW для моков API |
| Dockerfile | Сборка статики; готовые файлы копируются в образ Nginx |

### e2e

Playwright-сценарии на полностью поднятом окружении: регистрация, создание канала, загрузка тестового ролика, ожидание READY, воспроизведение, комментарий, поиск. Отдельно от backend и frontend, потому что проверяет их вместе.

### infrastructure

| Путь | Назначение |
| --- | --- |
| docker-compose.yml | Локальная разработка: все сервисы, тома, порты наружу для отладки, монтирование кода с автоперезагрузкой |
| docker-compose.prod.yml | Продакшен: готовые образы из реестра, без лишних портов, лимиты CPU и памяти, политики перезапуска, проверки здоровья |
| nginx/ | Главный конфиг и конфиги сайтов: статика, /api, /hls с кешем и secure\_link, поддомен загрузок, HTTPS, заголовки безопасности, rate limiting |
| postgres/init/ | Скрипт первого запуска: расширение pg\_trgm, пользователь приложения с минимальными правами |
| storage/init-buckets.sh | Создание бакетов, политики доступа, CORS для загрузки, правило удаления незавершённых multipart-загрузок |
| monitoring/ | Конфигурация Prometheus (цели, правила алертов) и Grafana (источники данных и дашборды как код) |
| scripts/ | Деплой, резервное копирование и восстановление |

### docs

| Путь | Назначение |
| --- | --- |
| architecture.md | Этот документ или его сокращённая версия |
| adr/ | Architecture Decision Records — короткие записи «контекст, решение, последствия» для каждого важного выбора: модульный монолит, прямая загрузка в хранилище, HLS вместо DASH, Celery, FTS в PostgreSQL. Отличный материал для собеседования |
| runbook.md | Эксплуатация: как задеплоить, откатить, восстановить из бэкапа, перезапустить зависшую обработку |
| diagrams/ | Исходники Mermaid-диаграмм |
