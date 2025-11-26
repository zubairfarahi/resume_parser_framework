"""Logging configuration using structlog.

This module sets up structured logging with JSON output for production
and human-friendly console output for development.
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.types import EventDict, Processor

from app.config.settings import settings


def add_app_context(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add application context to log entries.

    Args:
        logger: The logger instance
        method_name: The logging method name
        event_dict: The event dictionary

    Returns:
        Enhanced event dictionary with app context
    """
    event_dict["app"] = settings.app_name
    event_dict["version"] = settings.app_version
    event_dict["environment"] = settings.environment
    return event_dict


def setup_logging() -> None:
    """Configure structured logging for the application.

    Sets up structlog with appropriate processors based on the environment:
    - Development: Human-readable console output with colors
    - Production: JSON output for log aggregation systems

    SOLID Principles:
    - Single Responsibility: Only handles logging configuration
    - Dependency Inversion: Uses settings abstraction for configuration
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Determine processors based on environment
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        add_app_context,
    ]

    # Add environment-specific processors
    if settings.log_format == "json":
        # JSON output for production
        processors.append(structlog.processors.JSONRenderer())
    else:
        # Pretty console output for development
        processors.extend(
            [
                structlog.dev.ConsoleRenderer(
                    colors=True,
                    exception_formatter=structlog.dev.plain_traceback,
                )
            ]
        )

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a configured logger instance.

    Args:
        name: Name of the logger (typically __name__)

    Returns:
        Configured structlog logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing resume", file_name="resume.pdf", size_kb=245)
    """
    return structlog.get_logger(name)


# Performance monitoring decorator
def log_performance(operation: str) -> Any:
    """Decorator to log operation performance.

    Args:
        operation: Name of the operation being monitored

    Returns:
        Decorator function

    Example:
        >>> @log_performance("pdf_parsing")
        >>> def parse_pdf(file_path: Path) -> str:
        >>>     # parsing logic
        >>>     pass
    """
    import functools
    import time

    def decorator(func: Any) -> Any:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = get_logger(func.__module__)
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                logger.info(
                    f"{operation} completed",
                    operation=operation,
                    function=func.__name__,
                    duration_seconds=round(duration, 3),
                )

                # Warn if operation is slow
                if duration > 10:
                    logger.warning(
                        f"{operation} slow",
                        operation=operation,
                        function=func.__name__,
                        duration_seconds=round(duration, 3),
                    )

                return result

            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"{operation} failed",
                    operation=operation,
                    function=func.__name__,
                    duration_seconds=round(duration, 3),
                    error=str(e),
                    exc_info=True,
                )
                raise

        return wrapper

    return decorator
