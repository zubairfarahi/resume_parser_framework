"""Resume parser framework orchestrator.

This module provides the main entry point for the resume parsing framework.
"""

from pathlib import Path
from typing import Dict

from app.config.logging_config import get_logger, log_performance
from app.core.extractors.base import FieldExtractor
from app.core.models.resume_data import ResumeData
from app.core.parsers.base import FileParser
from app.core.parsers.pdf_parser import PDFParser
from app.core.parsers.word_parser import WordParser
from app.core.resume_extractor import ResumeExtractor
from app.exceptions.exceptions import ParsingError
from app.utils.validators import FileValidator

logger = get_logger(__name__)


class ResumeParserFramework:
    """Main framework orchestrator for resume parsing.

    This class combines file parsing and field extraction to provide a
    complete resume parsing solution.

    SOLID Principles:
    - Single Responsibility: Only orchestrates parsing workflow
    - Open/Closed: Extensible via parser and extractor registration
    - Liskov Substitution: All parsers/extractors are interchangeable
    - Dependency Inversion: Depends on abstractions (FileParser, FieldExtractor)

    Example:
        >>> from app.core.extractors import NameExtractor, EmailExtractor, SkillsExtractor
        >>> from app.core.framework import ResumeParserFramework
        >>>
        >>> # Create extractors
        >>> extractors = {
        ...     "name": NameExtractor(),
        ...     "email": EmailExtractor(),
        ...     "skills": SkillsExtractor()
        ... }
        >>>
        >>> # Create framework
        >>> framework = ResumeParserFramework(extractors)
        >>>
        >>> # Parse resume
        >>> resume_data = framework.parse_resume("path/to/resume.pdf")
        >>> print(resume_data.name, resume_data.email)
    """

    def __init__(
        self,
        extractors: Dict[str, FieldExtractor],
        parser: FileParser = None,
    ) -> None:
        """Initialize the framework.

        Args:
            extractors: Dictionary of field extractors
            parser: Optional file parser (if None, auto-detect based on file extension)
        """
        self.extractors = extractors
        self.resume_extractor = ResumeExtractor(extractors)
        self.parser = parser

        # Register default parsers
        self._parsers: Dict[str, type[FileParser]] = {
            ".pdf": PDFParser,
            ".docx": WordParser,
            ".doc": WordParser,
        }

        logger.info(
            "ResumeParserFramework initialized",
            extractor_count=len(extractors),
            has_custom_parser=parser is not None,
        )

    def register_parser(self, extension: str, parser_class: type[FileParser]) -> None:
        """Register a custom parser for a file extension.

        Args:
            extension: File extension (e.g., '.txt', '.html')
            parser_class: Parser class to handle this extension

        Example:
            >>> framework.register_parser('.txt', TextParser)
        """
        self._parsers[extension.lower()] = parser_class
        logger.info(
            "Parser registered",
            extension=extension,
            parser_class=parser_class.__name__,
        )

    @log_performance("resume_parsing")
    def parse_resume(self, file_path: str) -> ResumeData:
        """Parse resume file and extract structured data.

        This is the main entry point of the framework. It:
        1. Validates the file
        2. Selects appropriate parser based on file extension
        3. Parses the file to extract text
        4. Extracts fields using configured extractors
        5. Returns structured ResumeData

        Args:
            file_path: Path to resume file (PDF or Word document)

        Returns:
            ResumeData instance with extracted information

        Raises:
            ParsingError: If file parsing fails
            ExtractionError: If field extraction fails
            ValidationError: If file validation fails

        Example:
            >>> resume_data = framework.parse_resume("resume.pdf")
            >>> print(resume_data.to_json())
        """
        # Convert to Path object
        path = Path(file_path)

        logger.info(
            "Starting resume parsing",
            file_path=str(path),
            file_extension=path.suffix,
        )

        # Step 1: Validate file
        logger.debug("Validating file")
        FileValidator.validate_file(path)

        # Step 2: Get appropriate parser
        parser = self._get_parser(path)
        logger.debug(
            "Parser selected",
            parser_class=parser.__class__.__name__,
        )

        # Step 3: Parse file to extract text
        logger.debug("Parsing file")
        text = parser.parse(path)

        logger.info(
            "File parsed successfully",
            file_path=str(path),
            text_length=len(text),
        )

        # Step 4: Extract fields
        logger.debug("Extracting fields")
        resume_data = self.resume_extractor.extract(text)

        logger.info(
            "Resume parsing completed",
            file_path=str(path),
            name=resume_data.name,
            email=resume_data.email,
            skills_count=len(resume_data.skills) if resume_data.skills else 0,
        )

        return resume_data

    def _get_parser(self, file_path: Path) -> FileParser:
        """Get appropriate parser for file.

        Args:
            file_path: Path to file

        Returns:
            Parser instance

        Raises:
            ParsingError: If no parser available for file extension
        """
        # If custom parser provided, use it
        if self.parser:
            return self.parser

        # Get parser based on file extension
        extension = file_path.suffix.lower()

        if extension not in self._parsers:
            raise ParsingError(
                f"No parser available for {extension} files. "
                f"Supported formats: {', '.join(self._parsers.keys())}",
                file_path=str(file_path),
                details={"extension": extension},
            )

        # Create parser instance
        parser_class = self._parsers[extension]
        return parser_class()
