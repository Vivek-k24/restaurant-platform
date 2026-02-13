import logging
import os
from contextlib import asynccontextmanager

import psycopg
import structlog
from fastapi import FastAPI


def configure_logging() -> structlog.stdlib.BoundLogger:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
    return structlog.get_logger("api")


logger = configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_url = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/restaurant"
    )
    logger.info("database_connection_check_started", database_url=database_url)
    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    logger.info("database_connection_check_succeeded")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    logger.info("healthcheck_requested")
    return {"status": "ok"}
