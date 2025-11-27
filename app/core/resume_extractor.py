"""Resume extraction coordinator.

This module coordinates field extraction from resume text using multiple extractors.
"""

from typing import Dict

from app.config.logging_config import get_logger, log_performance
from app.core.extractors.base import FieldExtractor
from app.core.models.resume_data import ResumeData

logger = get_logger(__name__)


class ResumeExtractor:
    """Coordinates field extraction from resume text.

    This class orchestrates multiple field extractors to extract structured
    information from raw resume text.

    SOLID Principles:
    - Single Responsibility: Only coordinates extraction, doesn't parse files
    - Open/Closed: Can add new extractors without modifying this class
    - Dependency Inversion: Depends on FieldExtractor abstraction
    - Interface Segregation: Clean interface with single extract method

    Example:
        >>> from app.core.extractors import NameExtractor, EmailExtractor, SkillsExtractor
        >>> extractors = {
        ...     "name": NameExtractor(),
        ...     "email": EmailExtractor(),
        ...     "skills": SkillsExtractor()
        ... }
        >>> extractor = ResumeExtractor(extractors)
        >>> resume_data = extractor.extract(text)
    """

    def __init__(self, extractors: Dict[str, FieldExtractor]) -> None:
        """Initialize with field extractors.

        Args:
            extractors: Dictionary mapping field names to extractors
                       Example: {"name": NameExtractor(), "email": EmailExtractor()}
        """
        self.extractors = extractors
        logger.info(
            "ResumeExtractor initialized",
            extractor_count=len(extractors),
            fields=list(extractors.keys()),
        )

    @log_performance("field_extraction")
    def extract(self, text: str) -> ResumeData:
        """Extract all fields from resume text.

        Runs each configured extractor and collects the results into a
        ResumeData instance.

        Args:
            text: Raw text from resume

        Returns:
            ResumeData instance with extracted fields

        Example:
            >>> text = "John Doe\\njohn@example.com\\nSkills: Python, Java"
            >>> resume_data = extractor.extract(text)
            >>> print(resume_data.name)  # "John Doe"
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for extraction")
            return ResumeData()

        logger.info("Starting field extraction", text_length=len(text))

        extracted_fields = {}

        # Run each extractor
        for field_name, extractor in self.extractors.items():
            try:
                logger.debug(f"Extracting field: {field_name}")
                value = extractor.extract(text)

                # Post-process the value
                value = extractor.post_process(value)

                extracted_fields[field_name] = value

                logger.debug(
                    f"Field extracted: {field_name}",
                    field=field_name,
                    has_value=value is not None,
                )

            except Exception as e:
                logger.error(
                    f"Failed to extract {field_name}",
                    field=field_name,
                    error=str(e),
                    exc_info=True,
                )
                # Set to None if extraction fails
                extracted_fields[field_name] = None

        # Create ResumeData instance
        resume_data = ResumeData(**extracted_fields)

        logger.info(
            "Field extraction completed",
            fields_extracted=sum(1 for v in extracted_fields.values() if v is not None),
            total_fields=len(extracted_fields),
        )

        return resume_data
