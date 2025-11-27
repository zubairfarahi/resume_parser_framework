"""Name extractor using regex and heuristics.

This module provides a concrete implementation of FieldExtractor for extracting names.
"""

import re
from typing import Any, Optional

from app.config.logging_config import get_logger
from app.core.extractors.base import FieldExtractor

logger = get_logger(__name__)


class NameExtractor(FieldExtractor):
    """Extract name from resume text using regex and heuristics.

    This extractor uses pattern matching to identify names typically found
    at the beginning of resumes.

    SOLID Principles:
    - Single Responsibility: Only extracts names
    - Liskov Substitution: Can replace FieldExtractor
    - Dependency Inversion: Depends on FieldExtractor abstraction

    Strategy: Regex-based with multiple patterns and heuristics
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        """Initialize the name extractor.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)

        # Name patterns (prioritized)
        self.patterns = [
            # Pattern 1: Name followed by contact info
            r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*(?:\n|Email|Phone|Tel|\d)",
            # Pattern 2: Name at start of document (2-4 words, each capitalized)
            r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s*\n",
            # Pattern 3: Simple capitalized name (2-3 words)
            r"^([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b",
        ]

    def extract(self, text: str) -> Any:
        """Extract name from resume text.

        Args:
            text: Raw resume text

        Returns:
            Extracted name as string, or None if not found

        Raises:
            ValueError: If text is invalid
        """
        # Validate input
        validation_error = self.validate_input(text)
        if validation_error:
            logger.warning("Name extraction validation failed", error=validation_error)
            raise ValueError(validation_error)

        logger.debug("Starting name extraction", text_length=len(text))

        # Clean text: get first few lines where name is likely to be
        lines = text.strip().split("\n")
        search_text = "\n".join(lines[:10])  # Search in first 10 lines

        # Try each pattern
        for i, pattern in enumerate(self.patterns, start=1):
            match = re.search(pattern, search_text, re.MULTILINE)
            if match:
                name = match.group(1).strip()

                # Validate extracted name
                if self._is_valid_name(name):
                    logger.info(
                        "Name extracted successfully",
                        name=name,
                        pattern_index=i,
                    )
                    return name

        # Fallback: Try to find any capitalized words at the start
        words = search_text.split()
        capitalized_words = []
        for word in words[:5]:  # Check first 5 words
            if word and word[0].isupper() and word.isalpha():
                capitalized_words.append(word)
                if len(capitalized_words) == 2:  # Assume 2-word name
                    name = " ".join(capitalized_words)
                    if self._is_valid_name(name):
                        logger.info("Name extracted via fallback", name=name)
                        return name
                    break

        logger.warning("No name found in text")
        return None

    def _is_valid_name(self, name: str) -> bool:
        """Validate if extracted string looks like a real name.

        Args:
            name: Potential name string

        Returns:
            True if valid name, False otherwise
        """
        if not name or len(name) < 3:
            return False

        # Check if it contains common resume keywords (likely not a name)
        invalid_keywords = [
            "resume",
            "curriculum",
            "vitae",
            "profile",
            "summary",
            "objective",
            "experience",
            "education",
            "skills",
            "contact",
        ]

        name_lower = name.lower()
        for keyword in invalid_keywords:
            if keyword in name_lower:
                return False

        # Name should have 2-4 words
        words = name.split()
        if len(words) < 2 or len(words) > 4:
            return False

        # Each word should start with capital letter
        for word in words:
            if not word[0].isupper():
                return False

        return True

    def get_field_name(self) -> str:
        """Get the field name this extractor handles.

        Returns:
            'name'
        """
        return "name"
