"""File and input validation utilities.

This module provides security-focused validation for file uploads and inputs.
Prevents common vulnerabilities like path traversal, file size attacks, and
invalid file types.
"""

import mimetypes
from pathlib import Path
from typing import Optional

import magic

from app.config.settings import settings
from app.exceptions.exceptions import ValidationError


class FileValidator:
    """Validates uploaded files for security and correctness.

    This class provides static methods for validating files before processing.
    Implements security best practices to prevent common file upload vulnerabilities.

    SOLID Principles:
    - Single Responsibility: Only handles file validation
    - Open/Closed: Can be extended with new validation methods
    - Dependency Inversion: Uses settings abstraction for configuration

    Security Checks:
    - File size limits to prevent DoS attacks
    - MIME type validation to prevent malicious files
    - Path traversal prevention
    - File existence and readability checks
    """

    @staticmethod
    def validate_file_size(file_path: Path) -> None:
        """Validate that file size is within limits.

        Args:
            file_path: Path to the file to validate

        Raises:
            ValidationError: If file size exceeds maximum allowed size
        """
        file_size = file_path.stat().st_size

        if file_size > settings.max_file_size:
            max_size_mb = settings.max_file_size / (1024 * 1024)
            actual_size_mb = file_size / (1024 * 1024)
            raise ValidationError(
                f"File size ({actual_size_mb:.2f}MB) exceeds maximum "
                f"allowed size ({max_size_mb:.2f}MB)",
                validation_type="file_size",
                details={
                    "file_path": str(file_path),
                    "file_size_bytes": file_size,
                    "max_size_bytes": settings.max_file_size,
                },
            )

    @staticmethod
    def validate_mime_type(file_path: Path) -> None:
        """Validate that file MIME type is allowed.

        Uses python-magic for accurate MIME type detection based on file content,
        not just file extension (which can be spoofed).

        Args:
            file_path: Path to the file to validate

        Raises:
            ValidationError: If MIME type is not in allowed list
        """
        # Use python-magic to detect MIME type from file content
        try:
            mime_type = magic.from_file(str(file_path), mime=True)
        except Exception as e:
            raise ValidationError(
                f"Failed to detect file MIME type: {str(e)}",
                validation_type="mime_type",
                details={"file_path": str(file_path)},
            )

        if mime_type not in settings.allowed_mime_types:
            raise ValidationError(
                f"File type '{mime_type}' is not allowed. "
                f"Allowed types: {', '.join(settings.allowed_mime_types)}",
                validation_type="mime_type",
                details={
                    "file_path": str(file_path),
                    "detected_mime_type": mime_type,
                    "allowed_mime_types": settings.allowed_mime_types,
                },
            )

    @staticmethod
    def validate_path(file_path: Path) -> None:
        """Validate that file path is safe and accessible.

        Prevents path traversal attacks and ensures file exists and is readable.

        Args:
            file_path: Path to the file to validate

        Raises:
            ValidationError: If path is invalid, file doesn't exist, or isn't readable
        """
        # Ensure path is absolute to prevent path traversal
        try:
            file_path = file_path.resolve(strict=True)
        except (FileNotFoundError, RuntimeError) as e:
            raise ValidationError(
                f"Invalid file path: {str(e)}",
                validation_type="path",
                details={"file_path": str(file_path)},
            )

        # Check if file exists
        if not file_path.exists():
            raise ValidationError(
                f"File not found: {file_path}",
                validation_type="path",
                details={"file_path": str(file_path)},
            )

        # Check if path points to a file (not a directory)
        if not file_path.is_file():
            raise ValidationError(
                f"Path is not a file: {file_path}",
                validation_type="path",
                details={"file_path": str(file_path)},
            )

        # Check if file is readable
        try:
            with open(file_path, "rb") as f:
                f.read(1)  # Try to read one byte
        except PermissionError:
            raise ValidationError(
                f"File is not readable: {file_path}",
                validation_type="path",
                details={"file_path": str(file_path)},
            )
        except Exception as e:
            raise ValidationError(
                f"Error reading file: {str(e)}",
                validation_type="path",
                details={"file_path": str(file_path)},
            )

    @staticmethod
    def validate_file(file_path: Path) -> None:
        """Perform complete file validation.

        Runs all validation checks: path, size, and MIME type.

        Args:
            file_path: Path to the file to validate

        Raises:
            ValidationError: If any validation check fails

        Example:
            >>> try:
            >>>     FileValidator.validate_file(Path("resume.pdf"))
            >>> except ValidationError as e:
            >>>     print(f"Validation failed: {e}")
        """
        FileValidator.validate_path(file_path)
        FileValidator.validate_file_size(file_path)
        FileValidator.validate_mime_type(file_path)

    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal and other attacks.

        Removes path separators and dangerous characters from filename.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename safe for file system operations

        Example:
            >>> FileValidator.get_safe_filename("../../etc/passwd")
            'etc_passwd'
            >>> FileValidator.get_safe_filename("my resume.pdf")
            'my_resume.pdf'
        """
        # Remove path separators
        safe_name = filename.replace("/", "_").replace("\\", "_")

        # Remove other potentially dangerous characters
        safe_name = "".join(
            c if c.isalnum() or c in "._- " else "_" for c in safe_name
        )

        # Replace spaces with underscores
        safe_name = safe_name.replace(" ", "_")

        # Remove leading/trailing underscores and dots
        safe_name = safe_name.strip("._")

        # Ensure filename is not empty
        if not safe_name:
            safe_name = "unnamed_file"

        return safe_name
