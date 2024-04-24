from pydantic import EmailStr, SecretStr, Field
from pydantic_settings import BaseSettings


class SMTPSettings(BaseSettings):
    """SMTP-specific configuration settings."""

    smtp_server: str = Field(..., env="SMTP_SERVER")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_user: EmailStr = Field(..., env="SMTP_USER")
    smtp_password: str = Field(..., env="SMTP_PASSWORD")
    smtp_use_ssl: bool = Field(True, env="SMTP_USE_SSL")


class GoogleServiceSettings(BaseSettings):
    """Google API service configuration settings.
    OAuth Authorization
    """
    google_credentials_path: str = Field(..., env="GOOGLE_CREDENTIALS_PATH")



class AppConfig(BaseSettings):
    """Application configuration settings, including all sub-configurations."""

    smtp_settings: SMTPSettings = Field(default_factory=SMTPSettings)
    google_settings: GoogleServiceSettings = Field(
        default_factory=GoogleServiceSettings
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def load_config() -> AppConfig:
    """Load and return the application configuration."""
    return AppConfig()


# This allows the settings to be loaded when the module is imported
settings = load_config()
