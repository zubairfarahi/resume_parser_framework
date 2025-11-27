"""Phone extractor using OpenAI LLM.

This module provides a concrete implementation of FieldExtractor for extracting phone numbers
using OpenAI's Language Models.
"""

import json
import os
from typing import Any, Optional

from openai import OpenAI

from app.config.logging_config import get_logger
from app.core.extractors.base import FieldExtractor
from app.exceptions.exceptions import ExtractionError
from app.prompts.resume_extraction_prompts import generate_phone_extraction_prompt

logger = get_logger(__name__)


class PhoneExtractor(FieldExtractor):
    """Extract phone number from resume text using OpenAI LLM.

    This extractor uses OpenAI to extract phone number from resume text.
    Requires OPENAI_API_KEY environment variable.

    SOLID Principles:
    - Single Responsibility: Only extracts phone numbers
    - Liskov Substitution: Can replace FieldExtractor
    - Dependency Inversion: Depends on FieldExtractor abstraction

    Strategy: LLM-based (ML/AI) extraction using OpenAI

    Environment Variables:
        OPENAI_API_KEY: OpenAI API key (required)
        OPENAI_MODEL: Model name (optional, default: gpt-4o-mini)
        OPENAI_TEMPERATURE: Temperature for generation (optional, default: 0.0)
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        """Initialize the phone extractor.

        Args:
            config: Optional configuration dictionary with keys:
                - model: Model name (default: from env or 'gpt-4o-mini')
                - temperature: Temperature for generation (default: from env or 0.0)
                - max_tokens: Maximum tokens for response (default: 200)
        """
        super().__init__(config)

        # Get configuration from env or config
        self.model_name = self.config.get("model") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(
            self.config.get("temperature") or os.getenv("OPENAI_TEMPERATURE", "0.0")
        )
        self.max_tokens = self.config.get("max_tokens", 200)

        # Initialize OpenAI client
        self._initialize_openai()

    def _initialize_openai(self) -> None:
        """Initialize OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment")
            raise ExtractionError(
                "OPENAI_API_KEY environment variable not set. "
                "Please set it in your .env file or environment.",
                field_name="phone",
            )

        try:
            self.client = OpenAI(api_key=api_key)
            logger.info(
                "OpenAI client initialized for phone extraction",
                model=self.model_name,
                temperature=self.temperature,
            )

        except Exception as e:
            logger.error("Failed to initialize OpenAI client", error=str(e))
            raise ExtractionError(
                f"Failed to initialize OpenAI client: {str(e)}",
                field_name="phone",
            )

    def extract(self, text: str) -> Any:
        """Extract phone number from resume text using OpenAI.

        Args:
            text: Raw resume text

        Returns:
            Extracted phone number as string, or None if not found

        Raises:
            ValueError: If text is invalid
            ExtractionError: If LLM extraction fails
        """
        # Validate input
        validation_error = self.validate_input(text)
        if validation_error:
            logger.warning("Phone extraction validation failed", error=validation_error)
            raise ValueError(validation_error)

        logger.debug(
            "Starting phone extraction with OpenAI",
            text_length=len(text),
            model=self.model_name,
        )

        # Generate prompt using structured prompts
        prompt = generate_phone_extraction_prompt(text)

        # Extract phone using OpenAI
        try:
            phone = self._extract_with_openai(prompt)

            logger.info(
                "Phone extracted successfully",
                phone=phone,
                model=self.model_name,
            )

            return phone

        except Exception as e:
            logger.error(
                "Phone extraction failed",
                model=self.model_name,
                error=str(e),
                exc_info=True,
            )
            raise ExtractionError(
                f"Failed to extract phone using OpenAI: {str(e)}",
                field_name="phone",
                details={"model": self.model_name, "error_type": type(e).__name__},
            )

    def _extract_with_openai(self, prompt: str) -> Optional[str]:
        """Extract phone using OpenAI.

        Args:
            prompt: Formatted prompt

        Returns:
            Phone number string or None

        Raises:
            ExtractionError: If extraction fails
        """
        try:
            # Create chat completion
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # Parse response
            response_text = response.choices[0].message.content.strip()
            logger.debug("OpenAI response received", response_length=len(response_text))

            # Extract phone from JSON response
            phone = self._parse_phone_response(response_text)

            return phone

        except Exception as e:
            logger.error("OpenAI API call failed", error=str(e))
            raise

    def _parse_phone_response(self, response_text: str) -> Optional[str]:
        """Parse phone from OpenAI response.

        Args:
            response_text: Raw response from OpenAI

        Returns:
            Phone number or None

        Raises:
            ExtractionError: If parsing fails
        """
        try:
            # Try to find JSON object in response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")

            json_str = response_text[start_idx:end_idx]

            # Parse JSON
            data = json.loads(json_str)

            if not isinstance(data, dict):
                raise ValueError("Response is not a JSON object")

            # Extract phone field
            phone = data.get("phone")

            # Return None if phone is null or empty
            if not phone or not isinstance(phone, str):
                return None

            return phone.strip()

        except json.JSONDecodeError as e:
            logger.error(
                "Failed to parse JSON response", error=str(e), response=response_text[:200]
            )
            raise ExtractionError(
                "OpenAI returned invalid JSON format",
                field_name="phone",
                details={"response": response_text[:200]},
            )

    def get_field_name(self) -> str:
        """Get the field name this extractor handles.

        Returns:
            'phone'
        """
        return "phone"
