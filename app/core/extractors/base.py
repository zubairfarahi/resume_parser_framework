"""Abstract base class for field extractors.

This module defines the FieldExtractor ABC that all concrete extractors must implement.
Follows the Open/Closed Principle - new extractors can be added without modifying existing code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FieldExtractor(ABC):
    """Abstract base class for extracting specific fields from resume text.

    This class defines the interface that all field extractors must implement.
    Each extractor is responsible for extracting a specific type of information
    from raw resume text.

    SOLID Principles:
    - Single Responsibility: Only handles extraction of one specific field type
    - Open/Closed: New field types can be added without modifying this class
    - Liskov Substitution: All subclasses can be used interchangeably
    - Interface Segregation: Minimal interface with only necessary methods
    - Dependency Inversion: Depends on abstractions not concretions
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize the field extractor.

        Args:
            config: Optional configuration dictionary for the extractor
        """
        self.config = config or {}

    @abstractmethod
    def extract(self, text: str) -> Any:
        """Extract specific field information from resume text.

        Args:
            text: Raw resume text to extract information from

        Returns:
            Extracted field value (type depends on the specific extractor)

        Raises:
            ValueError: If the text is invalid or extraction fails
        """
        pass

    @abstractmethod
    def get_field_name(self) -> str:
        """Get the name of the field this extractor handles.

        Returns:
            The field name (e.g., 'email', 'name', 'skills')
        """
        pass

    def validate_input(self, text: str) -> str | None:
        """Validate that the input text is suitable for extraction.

        Args:
            text: Raw resume text to validate

        Returns:
            Error message if validation fails, None if validation passes
        """
        if not text or not text.strip():
            return "Input text is empty or contains only whitespace"

        if len(text.strip()) < 10:
            return "Input text is too short to extract meaningful information"

        return None

    def post_process(self, value: Any) -> Any:
        """Post-process the extracted value.

        This method can be overridden by subclasses to perform
        additional processing on the extracted value.

        Args:
            value: The raw extracted value

        Returns:
            The post-processed value
        """
        return value
