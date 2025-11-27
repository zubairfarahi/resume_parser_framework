"""Email extractor using regex patterns.

This module provides a concrete implementation of FieldExtractor for extracting emails.
"""

from __future__ import annotations

import re
from typing import Any

from app.config.logging_config import get_logger
from app.core.extractors.base import FieldExtractor

logger = get_logger(__name__)


class EmailExtractor(FieldExtractor):
    """Extract email from resume text using regex.

    This extractor uses RFC 5322 compliant regex pattern to find email addresses.

    SOLID Principles:
    - Single Responsibility: Only extracts email addresses
    - Liskov Substitution: Can replace FieldExtractor
    - Dependency Inversion: Depends on FieldExtractor abstraction

    Strategy: Regex-based pattern matching
    """

    def __init__(self, config: dict | None = None) -> None:
        """Initialize the email extractor.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)

        # RFC 5322 compliant email pattern (simplified)
        self.email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    def extract(self, text: str) -> Any:
        """Extract email from resume text.

        Args:
            text: Raw resume text

        Returns:
            Extracted email as string, or None if not found

        Raises:
            ValueError: If text is invalid
        """
        # Validate input
        validation_error = self.validate_input(text)
        if validation_error:
            logger.warning("Email extraction validation failed", error=validation_error)
            raise ValueError(validation_error)

        logger.debug("Starting email extraction", text_length=len(text))

        # Find all email matches
        matches = self.email_pattern.findall(text)

        if not matches:
            logger.warning("No email found in text")
            return None

        # Take the first valid email
        for email in matches:
            # Additional validation
            if self._is_valid_email(email):
                logger.info("Email extracted successfully", email=email)
                return email.lower()  # Return lowercase

        logger.warning("No valid email found in text")
        return None

    def _is_valid_email(self, email: str) -> bool:
        """Additional validation for email address.

        Args:
            email: Potential email address

        Returns:
            True if valid, False otherwise
        """
        # Check length
        if len(email) < 6 or len(email) > 254:
            return False

        # Must have exactly one @
        if email.count("@") != 1:
            return False

        return True

    def get_field_name(self) -> str:
        """Get the field name this extractor handles.

        Returns:
            'email'
        """
        return "email"
