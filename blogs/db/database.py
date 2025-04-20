# database.py
from databases import Database

from blogs.configs.settings import settings

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

database: Database = Database(
    DATABASE_URL,
    user=f"{settings.DB_USER}",
    password=f"{settings.DB_PASSWORD}",
    min_size=settings.DB_MIN_CONNECTIONS,
    max_size=settings.DB_MAX_CONNECTIONS
)
