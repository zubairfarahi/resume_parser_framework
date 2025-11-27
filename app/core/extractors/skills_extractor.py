"""Skills extractor using LLM (Google Gemini or OpenAI).

This module provides a concrete implementation of FieldExtractor for extracting skills
using Large Language Models.
"""

import json
import os
from typing import Any, List, Optional

from app.config.logging_config import get_logger
from app.core.extractors.base import FieldExtractor
from app.exceptions.exceptions import ExtractionError

logger = get_logger(__name__)


class SkillsExtractor(FieldExtractor):
    """Extract skills from resume text using LLM.

    This extractor uses Google Gemini or OpenAI to extract skills from resume text.
    Requires API key configuration via environment variables.

    SOLID Principles:
    - Single Responsibility: Only extracts skills
    - Liskov Substitution: Can replace FieldExtractor
    - Dependency Inversion: Depends on FieldExtractor abstraction

    Strategy: LLM-based (ML/AI) extraction

    Environment Variables:
        GEMINI_API_KEY: Google Gemini API key (preferred)
        OPENAI_API_KEY: OpenAI API key (fallback)
    """

    def __init__(self, config: Optional[dict] = None) -> None:
        """Initialize the skills extractor.

        Args:
            config: Optional configuration dictionary with keys:
                - provider: 'gemini' or 'openai' (default: 'gemini')
                - model: Model name (default: 'gemini-pro' or 'gpt-3.5-turbo')
                - temperature: Temperature for generation (default: 0.0)
                - max_tokens: Maximum tokens for response (default: 500)
        """
        super().__init__(config)

        self.provider = self.config.get("provider", "gemini")
        self.temperature = self.config.get("temperature", 0.0)
        self.max_tokens = self.config.get("max_tokens", 500)

        # Initialize LLM client
        self._initialize_llm()

    def _initialize_llm(self) -> None:
        """Initialize LLM client based on provider."""
        if self.provider == "gemini":
            self._initialize_gemini()
        elif self.provider == "openai":
            self._initialize_openai()
        else:
            raise ValueError(
                f"Unsupported LLM provider: {self.provider}. Use 'gemini' or 'openai'"
            )

    def _initialize_gemini(self) -> None:
        """Initialize Google Gemini client."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment")
            raise ExtractionError(
                "GEMINI_API_KEY environment variable not set",
                field_name="skills",
                details={"provider": "gemini"},
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            self.model_name = self.config.get("model", "gemini-pro")
            self.model = genai.GenerativeModel(self.model_name)
            logger.info("Gemini client initialized", model=self.model_name)

        except ImportError:
            logger.error("google-generativeai package not installed")
            raise ExtractionError(
                "google-generativeai package not installed. Install with: pip install google-generativeai",
                field_name="skills",
            )

    def _initialize_openai(self) -> None:
        """Initialize OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment")
            raise ExtractionError(
                "OPENAI_API_KEY environment variable not set",
                field_name="skills",
                details={"provider": "openai"},
            )

        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=api_key)
            self.model_name = self.config.get("model", "gpt-3.5-turbo")
            logger.info("OpenAI client initialized", model=self.model_name)

        except ImportError:
            logger.error("openai package not installed")
            raise ExtractionError(
                "openai package not installed. Install with: pip install openai",
                field_name="skills",
            )

    def extract(self, text: str) -> Any:
        """Extract skills from resume text using LLM.

        Args:
            text: Raw resume text

        Returns:
            List of extracted skills

        Raises:
            ValueError: If text is invalid
            ExtractionError: If LLM extraction fails
        """
        # Validate input
        validation_error = self.validate_input(text)
        if validation_error:
            logger.warning("Skills extraction validation failed", error=validation_error)
            raise ValueError(validation_error)

        logger.debug(
            "Starting skills extraction",
            text_length=len(text),
            provider=self.provider,
        )

        # Create prompt for LLM
        prompt = self._create_prompt(text)

        # Extract skills using LLM
        try:
            if self.provider == "gemini":
                skills = self._extract_with_gemini(prompt)
            else:
                skills = self._extract_with_openai(prompt)

            logger.info(
                "Skills extracted successfully",
                skills_count=len(skills),
                provider=self.provider,
            )

            return skills

        except Exception as e:
            logger.error(
                "Skills extraction failed",
                provider=self.provider,
                error=str(e),
                exc_info=True,
            )
            raise ExtractionError(
                f"Failed to extract skills using {self.provider}: {str(e)}",
                field_name="skills",
                details={"provider": self.provider, "error_type": type(e).__name__},
            )

    def _create_prompt(self, text: str) -> str:
        """Create prompt for LLM.

        Args:
            text: Resume text

        Returns:
            Formatted prompt string
        """
        # Truncate text if too long (keep first 2000 chars)
        truncated_text = text[:2000] if len(text) > 2000 else text

        prompt = f"""You are an expert technical recruiter with 10+ years of experience identifying professional skills from resumes.

Analyze the following resume text and extract ALL relevant professional skills.

Focus on:
- Technical skills (programming languages, frameworks, tools, technologies)
- Soft skills (communication, leadership, teamwork)
- Domain expertise (machine learning, data analysis, cloud computing, etc.)
- Certifications and qualifications
- Methodologies (Agile, Scrum, DevOps, etc.)

IMPORTANT: Return ONLY a valid JSON array of strings, with no additional text, explanations, or formatting.

Example output format:
["Python", "Machine Learning", "Docker", "Leadership", "Agile"]

Resume text:
{truncated_text}

JSON array of skills:"""

        return prompt

    def _extract_with_gemini(self, prompt: str) -> List[str]:
        """Extract skills using Google Gemini.

        Args:
            prompt: Formatted prompt

        Returns:
            List of skills

        Raises:
            ExtractionError: If extraction fails
        """
        try:
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                },
            )

            # Parse response
            response_text = response.text.strip()
            logger.debug("Gemini response received", response_length=len(response_text))

            # Extract JSON array from response
            skills = self._parse_skills_response(response_text)

            return skills

        except Exception as e:
            logger.error("Gemini extraction failed", error=str(e))
            raise

    def _extract_with_openai(self, prompt: str) -> List[str]:
        """Extract skills using OpenAI.

        Args:
            prompt: Formatted prompt

        Returns:
            List of skills

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

            # Extract JSON array from response
            skills = self._parse_skills_response(response_text)

            return skills

        except Exception as e:
            logger.error("OpenAI extraction failed", error=str(e))
            raise

    def _parse_skills_response(self, response_text: str) -> List[str]:
        """Parse skills from LLM response.

        Args:
            response_text: Raw response from LLM

        Returns:
            List of skills

        Raises:
            ExtractionError: If parsing fails
        """
        try:
            # Try to find JSON array in response
            # Sometimes LLMs add extra text before/after the JSON
            start_idx = response_text.find("[")
            end_idx = response_text.rfind("]") + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]

            # Parse JSON
            skills = json.loads(json_str)

            if not isinstance(skills, list):
                raise ValueError("Response is not a JSON array")

            # Filter and clean skills
            cleaned_skills = []
            for skill in skills:
                if isinstance(skill, str) and skill.strip():
                    cleaned_skills.append(skill.strip())

            return cleaned_skills

        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON response", error=str(e), response=response_text)
            raise ExtractionError(
                "LLM returned invalid JSON format",
                field_name="skills",
                details={"response": response_text[:200]},
            )

    def get_field_name(self) -> str:
        """Get the field name this extractor handles.

        Returns:
            'skills'
        """
        return "skills"
