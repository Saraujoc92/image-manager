FROM python:3.12-slim

WORKDIR /image-manager

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./pyproject.toml .
COPY ./uv.lock .

COPY src/ .

RUN uv sync --frozen --no-cache

ENV PYTHONPATH=.

# Run the application.
CMD ["/image-manager/.venv/bin/fastapi", "run", "/image-manager/main.py", "--port", "8000", "--host", "0.0.0.0"]

