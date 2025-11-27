"""Education extractor using OpenAI LLM.

This module provides a concrete implementation of FieldExtractor for extracting education
using OpenAI's Language Models.
"""

import json
import os
from typing import Any

from openai import OpenAI

from app.config.logging_config import get_logger
from app.core.extractors.base import FieldExtractor
from app.core.models.resume_data import Education
from app.exceptions.exceptions import ExtractionError
from app.prompts.resume_extraction_prompts import generate_education_extraction_prompt

logger = get_logger(__name__)


class EducationExtractor(FieldExtractor):
    """Extract education from resume text using OpenAI LLM.

    This extractor uses OpenAI to extract education entries from resume text.
    Requires OPENAI_API_KEY environment variable.

    SOLID Principles:
    - Single Responsibility: Only extracts education
    - Liskov Substitution: Can replace FieldExtractor
    - Dependency Inversion: Depends on FieldExtractor abstraction

    Strategy: LLM-based (ML/AI) extraction using OpenAI

    Environment Variables:
        OPENAI_API_KEY: OpenAI API key (required)
        OPENAI_MODEL: Model name (optional, default: gpt-4o-mini)
        OPENAI_TEMPERATURE: Temperature for generation (optional, default: 0.0)
    """

    def __init__(self, config: dict | None = None) -> None:
        """Initialize the education extractor.

        Args:
            config: Optional configuration dictionary with keys:
                - model: Model name (default: from env or 'gpt-4o-mini')
                - temperature: Temperature for generation (default: from env or 0.0)
                - max_tokens: Maximum tokens for response (default: 1000)
        """
        super().__init__(config)

        # Get configuration from env or config
        self.model_name = self.config.get("model") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(
            self.config.get("temperature") or os.getenv("OPENAI_TEMPERATURE", "0.0")
        )
        self.max_tokens = self.config.get("max_tokens", 1000)

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
                field_name="education",
            )

        try:
            self.client = OpenAI(api_key=api_key)
            logger.info(
                "OpenAI client initialized for education extraction",
                model=self.model_name,
                temperature=self.temperature,
            )

        except Exception as e:
            logger.error("Failed to initialize OpenAI client", error=str(e))
            raise ExtractionError(
                f"Failed to initialize OpenAI client: {str(e)}",
                field_name="education",
            )

    def extract(self, text: str) -> Any:
        """Extract education from resume text using OpenAI.

        Args:
            text: Raw resume text

        Returns:
            List of Education objects

        Raises:
            ValueError: If text is invalid
            ExtractionError: If LLM extraction fails
        """
        # Validate input
        validation_error = self.validate_input(text)
        if validation_error:
            logger.warning("Education extraction validation failed", error=validation_error)
            raise ValueError(validation_error)

        logger.debug(
            "Starting education extraction with OpenAI",
            text_length=len(text),
            model=self.model_name,
        )

        # Generate prompt using structured prompts
        prompt = generate_education_extraction_prompt(text)

        # Extract education using OpenAI
        try:
            education = self._extract_with_openai(prompt)

            logger.info(
                "Education extracted successfully",
                education_count=len(education),
                model=self.model_name,
            )

            return education

        except Exception as e:
            logger.error(
                "Education extraction failed",
                model=self.model_name,
                error=str(e),
                exc_info=True,
            )
            raise ExtractionError(
                f"Failed to extract education using OpenAI: {str(e)}",
                field_name="education",
                details={"model": self.model_name, "error_type": type(e).__name__},
            )

    def _extract_with_openai(self, prompt: str) -> list[Education]:
        """Extract education using OpenAI.

        Args:
            prompt: Formatted prompt

        Returns:
            List of Education objects

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

            # Extract education from JSON response
            education = self._parse_education_response(response_text)

            return education

        except Exception as e:
            logger.error("OpenAI API call failed", error=str(e))
            raise

    def _parse_education_response(self, response_text: str) -> list[Education]:
        """Parse education from OpenAI response.

        Args:
            response_text: Raw response from OpenAI

        Returns:
            List of Education objects

        Raises:
            ExtractionError: If parsing fails
        """
        try:
            # Try to find JSON array in response
            start_idx = response_text.find("[")
            end_idx = response_text.rfind("]") + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]

            # Parse JSON
            data = json.loads(json_str)

            if not isinstance(data, list):
                raise ValueError("Response is not a JSON array")

            # Convert to Education objects
            education_list = []
            for entry in data:
                if not isinstance(entry, dict):
                    continue

                # Map prompt fields to Education model fields
                # Prompt uses: institution, degree, field, start_year, end_year
                # Model uses: institution, degree, field_of_study, graduation_date, gpa
                education_entry = Education(
                    institution=entry.get("institution"),
                    degree=entry.get("degree"),
                    field_of_study=entry.get("field") or entry.get("field_of_study"),
                    graduation_date=entry.get("end_year")
                    or entry.get("graduation_date"),  # Use end_year as graduation_date
                    gpa=entry.get("gpa"),  # Optional, might not be in prompt
                )

                education_list.append(education_entry)

            return education_list

        except json.JSONDecodeError as e:
            logger.error(
                "Failed to parse JSON response", error=str(e), response=response_text[:200]
            )
            raise ExtractionError(
                "OpenAI returned invalid JSON format",
                field_name="education",
                details={"response": response_text[:200]},
            )
        except Exception as e:
            logger.error("Failed to create Education objects", error=str(e))
            raise ExtractionError(
                f"Failed to parse education data: {str(e)}",
                field_name="education",
                details={"error_type": type(e).__name__},
            )

    def get_field_name(self) -> str:
        """Get the field name this extractor handles.

        Returns:
            'education'
        """
        return "education"
