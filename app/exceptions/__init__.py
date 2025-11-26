"""Custom exceptions for the resume parser framework."""

from app.exceptions.exceptions import (
    ExtractionError,
    ParsingError,
    ResumeParserException,
    TimeoutError,
    ValidationError,
)

__all__ = [
    "ResumeParserException",
    "ParsingError",
    "ExtractionError",
    "ValidationError",
    "TimeoutError",
]
