up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f bot

test:
	docker compose run --rm bot uv run pytest

lint:
	docker compose run --rm bot uv run ruff check .

fmt:
	docker compose run --rm bot uv run ruff format .
