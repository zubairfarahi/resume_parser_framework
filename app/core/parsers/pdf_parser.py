"""PDF parser implementation using pypdf library.

This module provides a concrete implementation of FileParser for PDF files.
"""

import signal
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from pypdf import PdfReader

from app.config.logging_config import get_logger, log_performance
from app.core.parsers.base import FileParser
from app.exceptions.exceptions import ParsingError, TimeoutError

logger = get_logger(__name__)


class PDFParser(FileParser):
    """PDF file parser implementation.

    Uses pypdf library to extract text from PDF files with timeout protection.

    SOLID Principles:
    - Single Responsibility: Only handles PDF parsing
    - Liskov Substitution: Can replace FileParser without breaking code
    - Dependency Inversion: Depends on FileParser abstraction

    Example:
        >>> parser = PDFParser(timeout=30)
        >>> text = parser.parse(Path("resume.pdf"))
    """

    @contextmanager
    def _timeout_handler(self, seconds: int) -> Generator[None, None, None]:
        """Context manager for timeout protection.

        Args:
            seconds: Timeout in seconds

        Raises:
            TimeoutError: If operation exceeds timeout

        Yields:
            None
        """

        def timeout_signal_handler(signum: int, frame: object) -> None:
            raise TimeoutError(
                f"PDF parsing exceeded {seconds}s timeout",
                timeout_seconds=seconds,
                operation="pdf_parsing",
            )

        # Set alarm signal
        old_handler = signal.signal(signal.SIGALRM, timeout_signal_handler)
        signal.alarm(seconds)

        try:
            yield
        finally:
            # Reset alarm
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

    @log_performance("pdf_parsing")
    def parse(self, file_path: Path) -> str:
        """Parse PDF file and extract text content.

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text content as string

        Raises:
            FileNotFoundError: If file doesn't exist
            ParsingError: If PDF parsing fails
            TimeoutError: If parsing exceeds timeout
        """
        # Validate file first
        validation_error = self.validate_file(file_path)
        if validation_error:
            logger.error("PDF validation failed", file_path=str(file_path), error=validation_error)
            raise ParsingError(validation_error, file_path=str(file_path))

        logger.info("Starting PDF parsing", file_path=str(file_path))

        try:
            with self._timeout_handler(self.timeout):
                # Read PDF file
                reader = PdfReader(str(file_path))

                # Extract text from all pages
                text_parts = []
                for page_num, page in enumerate(reader.pages, start=1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    except Exception as e:
                        logger.warning(
                            "Failed to extract text from page",
                            page_num=page_num,
                            file_path=str(file_path),
                            error=str(e),
                        )

                # Combine all text
                full_text = "\n\n".join(text_parts)

                if not full_text.strip():
                    logger.warning("No text extracted from PDF", file_path=str(file_path))
                    raise ParsingError(
                        "No text content found in PDF",
                        file_path=str(file_path),
                    )

                logger.info(
                    "PDF parsing successful",
                    file_path=str(file_path),
                    pages=len(reader.pages),
                    text_length=len(full_text),
                )

                return full_text

        except TimeoutError:
            logger.error("PDF parsing timeout", file_path=str(file_path), timeout=self.timeout)
            raise

        except Exception as e:
            logger.error(
                "PDF parsing failed",
                file_path=str(file_path),
                error=str(e),
                exc_info=True,
            )
            raise ParsingError(
                f"Failed to parse PDF: {str(e)}",
                file_path=str(file_path),
                details={"error_type": type(e).__name__},
            )

    def supports_format(self, file_path: Path) -> bool:
        """Check if this parser supports PDF format.

        Args:
            file_path: Path to file

        Returns:
            True if file has .pdf extension
        """
        return file_path.suffix.lower() == ".pdf"
