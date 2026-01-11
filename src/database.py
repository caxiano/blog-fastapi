import databases
import sqlalchemy as sa

from src.config import settings


final_db_url = settings.database_url
database_args = {}

if settings.environment == "production" and settings.database_url.startswith("postgresql"):
    database_args["ssl"] = True
    if settings.database_url.startswith("postgresql://"):
        final_db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)


database = databases.Database(final_db_url, **database_args)
metadata = sa.MetaData()

if settings.environment == "production":
    engine = sa.create_engine(final_db_url)
else:
    # Use the original URL for sqlite, which doesn't need the scheme replacement
    engine = sa.create_engine(settings.database_url, connect_args={"check_same_thread": False})