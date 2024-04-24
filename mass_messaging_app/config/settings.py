# Example of how to load settings from a .env file or environment variables
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_config: AppConfig

    class Config:
        env_file = ".env"
