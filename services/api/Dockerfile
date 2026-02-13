FROM python:3.11-slim

WORKDIR /app

# Copy metadata first (better caching)
COPY pyproject.toml ./

# Copy source BEFORE installing project (because setuptools needs app/)
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

# tests are not needed for runtime, but ok if you want them in image:
COPY tests ./tests

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir ".[dev]"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
