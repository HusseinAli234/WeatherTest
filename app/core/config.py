from pydantic_settings import BaseSettings
from typing import Optional
import os
class Settings(BaseSettings):
    PROJECT_NAME: str = "WeatherTest"
    VERSION: str = "1"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = "weather"
    ALGORITHM: str = "HS256"
    OPENWEATHER_URL: str = "https://api.openweathermap.org/data/2.5/weather "
    OPENWEATHER_API_KEY: str = "43d4fa8c9a3bfa2cbb7db51809f5d9fe"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@mydb")
    # @property
    # def DATABASE_URL(self) -> str:
    #     return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    # @property
    # def DATABASE_URL_SYNC(self):
    #     return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
