from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Personal Trainer"

    # Database
    DATABASE_URL: str = "sqlite:///./ai_trainer.db"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS. In production set ALLOWED_HOSTS to your frontend origin(s).
    # ALLOWED_ORIGIN_REGEX lets Vercel preview deployments through.
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    ALLOWED_ORIGIN_REGEX: str = r"https://.*\.vercel\.app"

    # Shared-secret gate. Empty = open (local dev). Set in production.
    ACCESS_PASSWORD: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Azure OpenAI Settings -- fill these in your .env file
    OPENAI_API_KEY: str = ""           # Azure OpenAI API key
    AZURE_OPENAI_ENDPOINT: str = ""    # e.g. https://my-resource.openai.azure.com/
    AZURE_API_VERSION: str = "2024-06-01"
    CHAT_MODEL: str = "gpt-4o-mini"    # Azure deployment name for the chat model

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
