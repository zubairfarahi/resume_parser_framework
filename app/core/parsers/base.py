"""Abstract base class for file parsers.

This module defines the FileParser ABC that all concrete parsers must implement.
Follows the Open/Closed Principle - open for extension, closed for modification.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class FileParser(ABC):
    """Abstract base class for parsing different file formats.

    This class defines the interface that all file parsers must implement.
    Each parser is responsible for extracting raw text from a specific file format.

    SOLID Principles:
    - Single Responsibility: Only handles file parsing, not extraction logic
    - Open/Closed: New file formats can be added without modifying this class
    - Liskov Substitution: All subclasses can be used interchangeably
    - Interface Segregation: Minimal interface with only necessary methods
    - Dependency Inversion: Depends on abstractions (Path) not concretions
    """

    def __init__(self, timeout: int = 30) -> None:
        """Initialize the file parser.

        Args:
            timeout: Maximum time in seconds allowed for parsing (default: 30)
        """
        self.timeout = timeout

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """Parse a file and extract raw text content.

        Args:
            file_path: Path to the file to parse

        Returns:
            Extracted text content as a string

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file format is invalid or unsupported
            TimeoutError: If parsing exceeds the timeout limit
        """
        pass

    @abstractmethod
    def supports_format(self, file_path: Path) -> bool:
        """Check if this parser supports the given file format.

        Args:
            file_path: Path to the file to check

        Returns:
            True if this parser can handle the file format, False otherwise
        """
        pass

    def validate_file(self, file_path: Path) -> Optional[str]:
        """Validate that the file exists and is accessible.

        Args:
            file_path: Path to the file to validate

        Returns:
            Error message if validation fails, None if validation passes
        """
        if not file_path.exists():
            return f"File not found: {file_path}"

        if not file_path.is_file():
            return f"Path is not a file: {file_path}"

        if not self.supports_format(file_path):
            return f"Unsupported file format: {file_path.suffix}"

        return None
