import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

# Load .env manually first (optional but safe)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", ".env")
load_dotenv(env_path)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Library API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database connection
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost:3306/library_db"

    # JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    REFRESH_SECRET_KEY: str = Field(..., env="REFRESH_SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    KAFKA_NETWORK: str = Field(..., env="KAFKA_NETWORK")
    TOPIC_NAME: str = Field(..., env="TOPIC_NAME")

    # ✅ Proper v2 config syntax
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# create singleton
settings = Settings()
