from pydantic_settings import BaseSettings
from enum import Enum

class Environment(str ,Enum):
    dev = "dev"
    prod = "prod"

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///:memory:"
    ENV: Environment = Environment.dev

settings = Settings()
