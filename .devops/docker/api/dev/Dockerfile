FROM python:3.12-slim

WORKDIR /image-manager

RUN apt-get update \
    && apt-get install -y libpq-dev gcc curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./apps/image_api/pyproject.toml ./apps/image_api/uv.lock ./

RUN uv venv \
    && uv sync --frozen

COPY ./apps/image_api/src ./src

ENV PYTHONPATH=src

# Run the application.
CMD [".venv/bin/fastapi", "run", "./src/main.py", "--port", "8000", "--host", "0.0.0.0"]

