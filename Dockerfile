FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:slim

WORKDIR /app/

ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY ./scripts /app/scripts/

COPY ./pyproject.toml ./uv.lock /app/

COPY ./src /app/src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD ["fastapi", "run", "--workers", "4", "src/app/main.py"]
