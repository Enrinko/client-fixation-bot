FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS base
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

FROM base AS dev
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
CMD ["uv", "run", "--no-sync", "python", "-m", "bot.main"]

FROM base AS prod
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY bot/ ./bot/
RUN groupadd -r app && useradd -r -g app app \
    && mkdir -p /data && chown app:app /data
USER app
CMD ["uv", "run", "--no-sync", "python", "-m", "bot.main"]
