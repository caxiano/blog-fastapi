import databases
import sqlalchemy as sa

from src.config import settings


database_args = {}
if settings.environment == "production" and settings.database_url.startswith("postgresql"):
    database_args["ssl"] = True

database = databases.Database(settings.database_url, **database_args)
metadata = sa.MetaData()

if settings.environment == "production":
    engine = sa.create_engine(settings.database_url)
else:
    engine = sa.create_engine(settings.database_url, connect_args={"check_same_thread": False})