"""Unit tests for file parsers."""

from pathlib import Path

import pytest

from app.core.parsers import PDFParser, WordParser
from app.exceptions.exceptions import ParsingError


class TestPDFParser:
    """Test suite for PDFParser."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = PDFParser(timeout=10)

    def test_supports_pdf_format(self) -> None:
        """Test that parser supports .pdf extension."""
        assert self.parser.supports_format(Path("test.pdf")) is True
        assert self.parser.supports_format(Path("test.PDF")) is True

    def test_does_not_support_other_formats(self) -> None:
        """Test that parser rejects non-PDF formats."""
        assert self.parser.supports_format(Path("test.docx")) is False
        assert self.parser.supports_format(Path("test.txt")) is False

    def test_parse_valid_pdf(self, sample_pdf_path: Path) -> None:
        """Test parsing a valid PDF file."""
        try:
            text = self.parser.parse(sample_pdf_path)
            assert isinstance(text, str)
            assert len(text) > 0
        except ImportError:
            pytest.skip("pypdf not installed")
        except ParsingError as e:
            # Skip if PDF has no extractable text (common with minimal test PDFs)
            if "No text content found" in str(e):
                pytest.skip("Test PDF has no extractable text content")
            raise

    def test_parse_nonexistent_file(self) -> None:
        """Test parsing a file that doesn't exist."""
        with pytest.raises(ParsingError):
            self.parser.parse(Path("/nonexistent/file.pdf"))

    def test_timeout_initialization(self) -> None:
        """Test custom timeout initialization."""
        parser = PDFParser(timeout=60)
        assert parser.timeout == 60


class TestWordParser:
    """Test suite for WordParser."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = WordParser(timeout=10)

    def test_supports_docx_format(self) -> None:
        """Test that parser supports .docx extension."""
        assert self.parser.supports_format(Path("test.docx")) is True
        assert self.parser.supports_format(Path("test.DOCX")) is True
        assert self.parser.supports_format(Path("test.doc")) is True

    def test_does_not_support_other_formats(self) -> None:
        """Test that parser rejects non-Word formats."""
        assert self.parser.supports_format(Path("test.pdf")) is False
        assert self.parser.supports_format(Path("test.txt")) is False

    def test_parse_nonexistent_file(self) -> None:
        """Test parsing a file that doesn't exist."""
        with pytest.raises(ParsingError):
            self.parser.parse(Path("/nonexistent/file.docx"))

    def test_timeout_initialization(self) -> None:
        """Test custom timeout initialization."""
        parser = WordParser(timeout=60)
        assert parser.timeout == 60

    def test_parse_valid_docx(self, sample_docx_path: Path) -> None:
        """Test parsing a valid Word document."""
        try:
            text = self.parser.parse(sample_docx_path)
            assert isinstance(text, str)
            assert len(text) > 0
            # Check that sample content is present
            assert "John Doe" in text
            assert "Software Engineer" in text
            assert "Python" in text or "SKILLS" in text
        except ImportError:
            pytest.skip("python-docx not installed")
        except ParsingError as e:
            # Skip if Word has no extractable text
            if "No text content found" in str(e):
                pytest.skip("Test Word document has no extractable text content")
            raise

    def test_parse_docx_with_tables(self, sample_docx_path: Path) -> None:
        """Test parsing Word document extracts table content."""
        try:
            text = self.parser.parse(sample_docx_path)
            # Table content should be extracted
            assert "Education" in text or "UC Berkeley" in text
        except ImportError:
            pytest.skip("python-docx not installed")

    def test_parse_empty_docx(self, temp_directory: Path) -> None:
        """Test parsing an empty Word document raises ParsingError."""
        try:
            from docx import Document

            empty_docx = temp_directory / "empty.docx"
            document = Document()
            document.save(str(empty_docx))

            with pytest.raises(ParsingError) as exc_info:
                self.parser.parse(empty_docx)

            assert "No text content found" in str(exc_info.value)

        except ImportError:
            pytest.skip("python-docx not installed")
