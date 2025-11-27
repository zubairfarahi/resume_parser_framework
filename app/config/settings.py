"""Application settings using Pydantic Settings.

This module provides type-safe configuration management using environment variables.
All settings can be overridden via environment variables.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support.

    All settings can be configured via environment variables with the
    RESUME_PARSER_ prefix. For example, MAX_FILE_SIZE can be set via
    RESUME_PARSER_MAX_FILE_SIZE environment variable.

    SOLID Principles:
    - Single Responsibility: Only handles configuration, not business logic
    - Open/Closed: New settings can be added without modifying existing code
    - Dependency Inversion: Other components depend on this abstraction
    """

    model_config = SettingsConfigDict(
        env_prefix="RESUME_PARSER_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Settings
    app_name: str = Field(
        default="Resume Parser Framework",
        description="Application name",
    )
    app_version: str = Field(
        default="0.1.0",
        description="Application version",
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )
    environment: str = Field(
        default="development",
        description="Environment (development, staging, production)",
    )

    # File Processing Settings
    max_file_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        description="Maximum file size in bytes",
    )
    allowed_mime_types: list[str] = Field(
        default=[
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ],
        description="Allowed MIME types for file uploads",
    )
    parsing_timeout: int = Field(
        default=30,
        description="Timeout for file parsing operations in seconds",
    )
    extraction_timeout: int = Field(
        default=30,
        description="Timeout for field extraction operations in seconds",
    )

    # Logging Settings
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    log_format: str = Field(
        default="json",
        description="Log format (json, console)",
    )
    log_file: str = Field(
        default="logs/resume_parser.log",
        description="Log file path",
    )

    # API Settings (if building REST API)
    api_host: str = Field(
        default="0.0.0.0",
        description="API server host",
    )
    api_port: int = Field(
        default=8000,
        description="API server port",
    )
    api_key_enabled: bool = Field(
        default=False,
        description="Enable API key authentication",
    )
    api_key: str = Field(
        default="",
        description="API key for authentication (set via environment variable)",
    )

    # Directory Settings
    temp_dir: Path = Field(
        default=Path("tmp"),
        description="Temporary directory for file processing",
    )
    upload_dir: Path = Field(
        default=Path("uploads"),
        description="Directory for uploaded files",
    )
    log_dir: Path = Field(
        default=Path("logs"),
        description="Directory for log files",
    )

    def create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [self.temp_dir, self.upload_dir, self.log_dir]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()
