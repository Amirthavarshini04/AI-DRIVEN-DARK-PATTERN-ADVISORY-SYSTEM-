import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Dark Pattern & Compliance Advisory System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./dark_patterns.db"
    CORS_ORIGINS: list = ["*"]
    
    # Optional LLM adapter config
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
