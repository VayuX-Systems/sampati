# SPDX-License-Identifier: Apache-2.0
"""Configuration for Sampati API."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    env: str = Field(default="dev", alias="SAMPATI_ENV")
    base_url: str | None = Field(default=None, alias="SAMPATI_BASE_URL")

    # Database
    database_url: str = Field(default="", alias="SAMPATI_DATABASE_URL")

    # Redis
    redis_url: str = Field(default="", alias="SAMPATI_REDIS_URL")

    # Storage (S3-compatible)
    storage_url: str | None = Field(default=None, alias="SAMPATI_STORAGE_URL")
    storage_bucket: str | None = Field(default=None, alias="SAMPATI_STORAGE_BUCKET")

    # Key management
    key_mode: str = Field(default="local", alias="SAMPATI_KEY_MODE")

    # OIDC
    oidc_issuer: str | None = Field(default=None, alias="SAMPATI_OIDC_ISSUER")
    oidc_client_id: str | None = Field(default=None, alias="SAMPATI_OIDC_CLIENT_ID")
    oidc_client_secret: str | None = Field(default=None, alias="SAMPATI_OIDC_CLIENT_SECRET")

    # Email
    smtp_url: str | None = Field(default=None, alias="SAMPATI_SMTP_URL")

    # Localization
    default_locale: str = Field(default="en-IN", alias="SAMPATI_DEFAULT_LOCALE")
    timezone: str = Field(default="Asia/Kolkata", alias="SAMPATI_TIMEZONE")

    # Plugin sandbox
    plugin_sandbox: str = Field(default="container", alias="SAMPATI_PLUGIN_SANDBOX")

    # AI
    ai_enabled: bool = Field(default=False, alias="SAMPATI_AI_ENABLED")
    ai_base_url: str | None = Field(default=None, alias="SAMPATI_AI_BASE_URL")

    # Logging
    log_level: str = Field(default="info", alias="SAMPATI_LOG_LEVEL")

    # Security
    secret_key: str = Field(default="", alias="SAMPATI_SECRET_KEY")
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Validate required settings in production
        if self.env == "prod":
            if not self.secret_key:
                raise ValueError("SAMPATI_SECRET_KEY is required in production")
            if not self.database_url:
                raise ValueError("SAMPATI_DATABASE_URL is required in production")
            if not self.redis_url:
                raise ValueError("SAMPATI_REDIS_URL is required in production")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
