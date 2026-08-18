"""Core configuration and security settings."""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "ANSOP"
    app_version: str = "0.1.0"
    app_env: str = os.getenv("APP_ENV", "development")
    app_debug: bool = os.getenv("APP_DEBUG", "false").lower() == "true"
    app_log_level: str = os.getenv("APP_LOG_LEVEL", "INFO")

    # Server
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    backend_workers: int = int(os.getenv("BACKEND_WORKERS", "4"))

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://ansop_user:ansop_password_change_me@localhost:5432/ansop_db",
    )
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    database_pool_timeout: int = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
    database_echo: bool = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    # JWT Authentication
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_secret_key: str = os.getenv(
        "JWT_SECRET_KEY",
        "your-super-secret-jwt-key-change-me-in-production",
    )
    jwt_expiration_minutes: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))
    jwt_refresh_expiration_days: int = int(os.getenv("JWT_REFRESH_EXPIRATION_DAYS", "7"))

    # Password requirements
    password_min_length: int = int(os.getenv("PASSWORD_MIN_LENGTH", "12"))
    password_require_uppercase: bool = (
        os.getenv("PASSWORD_REQUIRE_UPPERCASE", "true").lower() == "true"
    )
    password_require_lowercase: bool = (
        os.getenv("PASSWORD_REQUIRE_LOWERCASE", "true").lower() == "true"
    )
    password_require_numbers: bool = (
        os.getenv("PASSWORD_REQUIRE_NUMBERS", "true").lower() == "true"
    )
    password_require_special: bool = (
        os.getenv("PASSWORD_REQUIRE_SPECIAL", "true").lower() == "true"
    )

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Lab Configuration
    lab_mode: bool = os.getenv("LAB_MODE", "true").lower() == "true"
    dry_run: bool = os.getenv("DRY_RUN", "true").lower() == "true"
    allow_private_targets: bool = (
        os.getenv("ALLOW_PRIVATE_TARGETS", "true").lower() == "true"
    )
    block_external_targets: bool = (
        os.getenv("BLOCK_EXTERNAL_TARGETS", "true").lower() == "true"
    )

    # API Documentation
    enable_api_docs: bool = os.getenv("ENABLE_API_DOCS", "true").lower() == "true"
    api_docs_url: str = os.getenv("API_DOCS_URL", "/docs")
    redoc_url: str = os.getenv("REDOC_URL", "/redoc")

    # Security Headers
    enable_security_headers: bool = (
        os.getenv("ENABLE_SECURITY_HEADERS", "true").lower() == "true"
    )
    hsts_max_age: int = int(os.getenv("HSTS_MAX_AGE", "31536000"))
    x_frame_options: str = os.getenv("X_FRAME_OPTIONS", "DENY")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = False

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
