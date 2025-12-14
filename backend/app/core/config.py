from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Sweet Shop Management"

    # JWT
    JWT_SECRET_KEY: str = Field(
        default="super-secret-key-change-this",
        validation_alias="SECRET_KEY",  # backward compatibility
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        validation_alias="ALGORITHM",  # backward compatibility
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # 🔑 prevents this error forever
    )


settings = Settings()

