from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")
    database_url: str = "sqlite:///../blog.db"
    environment: str = "production"


settings = Settings()