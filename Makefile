COMPOSE = docker compose -f infrastructure/docker-compose.yml --env-file .env

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f --tail 100

shell:
	$(COMPOSE) exec api sh

lint:
	cd backend && uv run ruff check . && uv run ruff format --check .

test:
	cd backend && uv run pytest

clean:
	$(COMPOSE) down -v

.PHONY: up down restart ps logs shell lint test clean
