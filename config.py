"""
Configuration for AI Interview Orchestrator.

Loads settings from environment variables (or a .env file in dev). All values
have sensible local defaults but should be overridden in production.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


# --- Service discovery ---
# In docker-compose, services are reachable as `redis` / `postgres` on the
# default bridge network. In local dev, default to localhost.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "ai_interview_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# --- Worker / Celery ---
WORKER_CONCURRENCY = int(os.getenv("WORKER_CONCURRENCY", "4"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# --- API / Security ---
# Token required by worker agents to call /register-worker and /worker/heartbeat.
API_TOKEN = os.getenv("API_TOKEN", "dev-token-change-me")
# Comma-separated origin list for CORS. Use "*" to allow all (dev only).
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGIGNS", "*")

# --- Optional feature flags ---
ENABLE_CELERY_BROKER = _bool("ENABLE_CELERY_BROKER", True)

# --- Derived ---
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
