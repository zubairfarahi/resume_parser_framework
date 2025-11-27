"""Custom exception classes for the resume parser framework.

This module defines a hierarchy of exceptions for different error scenarios.
All exceptions inherit from ResumeParserException for easy catching.
"""

from typing import Any


class ResumeParserException(Exception):
    """Base exception for all resume parser errors.

    This is the base class for all custom exceptions in the framework.
    Catching this exception will catch all framework-specific errors.

    Attributes:
        message: Human-readable error message
        details: Optional dictionary with additional error context
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation of the exception.

        Returns:
            Formatted error message with details if available
        """
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class ParsingError(ResumeParserException):
    """Exception raised when file parsing fails.

    This exception is raised when a file parser encounters an error
    while trying to extract text from a file.

    Examples:
        - Corrupted PDF file
        - Unsupported Word document version
        - Invalid file format
    """

    def __init__(
        self,
        message: str,
        file_path: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the parsing error.

        Args:
            message: Human-readable error message
            file_path: Path to the file that failed to parse
            details: Optional dictionary with additional error context
        """
        details = details or {}
        if file_path:
            details["file_path"] = file_path
        super().__init__(message, details)


class ExtractionError(ResumeParserException):
    """Exception raised when field extraction fails.

    This exception is raised when a field extractor encounters an error
    while trying to extract specific information from resume text.

    Examples:
        - LLM API failure
        - Regex pattern mismatch
        - Invalid extraction configuration
    """

    def __init__(
        self,
        message: str,
        field_name: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the extraction error.

        Args:
            message: Human-readable error message
            field_name: Name of the field that failed to extract
            details: Optional dictionary with additional error context
        """
        details = details or {}
        if field_name:
            details["field_name"] = field_name
        super().__init__(message, details)


class ValidationError(ResumeParserException):
    """Exception raised when validation fails.

    This exception is raised when input validation fails, such as:
    - Invalid file size
    - Unsupported MIME type
    - Invalid configuration
    - Schema validation failure
    """

    def __init__(
        self,
        message: str,
        validation_type: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the validation error.

        Args:
            message: Human-readable error message
            validation_type: Type of validation that failed (e.g., "file_size", "mime_type")
            details: Optional dictionary with additional error context
        """
        details = details or {}
        if validation_type:
            details["validation_type"] = validation_type
        super().__init__(message, details)


class TimeoutError(ResumeParserException):
    """Exception raised when an operation exceeds its timeout limit.

    This exception is raised when a parsing or extraction operation
    takes longer than the configured timeout period.

    Examples:
        - Large PDF file parsing timeout
        - LLM API request timeout
        - External service timeout
    """

    def __init__(
        self,
        message: str,
        timeout_seconds: int | None = None,
        operation: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the timeout error.

        Args:
            message: Human-readable error message
            timeout_seconds: The timeout limit that was exceeded
            operation: Name of the operation that timed out
            details: Optional dictionary with additional error context
        """
        details = details or {}
        if timeout_seconds:
            details["timeout_seconds"] = timeout_seconds
        if operation:
            details["operation"] = operation
        super().__init__(message, details)
