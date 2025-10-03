FROM python:3.13-slim

RUN pip install --no-cache-dir poetry

ENV PATH="/root/.local/bin:${PATH}"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-dev --no-interaction --no-ansi


COPY . .

RUN python manage.py collectstatic --noinput


EXPOSE 8000
