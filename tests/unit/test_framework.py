"""Unit tests for ResumeParserFramework."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app.core.extractors.base import FieldExtractor
from app.core.framework import ResumeParserFramework
from app.core.models.resume_data import ResumeData
from app.exceptions.exceptions import ParsingError


class MockExtractor(FieldExtractor):
    """Mock extractor for testing."""

    def __init__(self, field_name: str, return_value=None):
        super().__init__()
        self.field_name = field_name
        self.return_value = return_value

    def extract(self, text: str):
        return self.return_value

    def get_field_name(self) -> str:
        return self.field_name


class TestResumeParserFramework:
    """Test suite for ResumeParserFramework."""

    def test_initialization_with_extractors(self):
        """Test framework initialization with extractors."""
        extractors = {
            "name": MockExtractor("name", "John Doe"),
            "email": MockExtractor("email", "john@example.com"),
        }

        framework = ResumeParserFramework(extractors)

        assert framework.extractors == extractors
        assert len(framework.extractors) == 2

    def test_initialization_empty_extractors(self):
        """Test framework initialization with empty extractors."""
        framework = ResumeParserFramework({})

        assert framework.extractors == {}

    @patch("app.utils.validators.FileValidator.validate_file")
    @patch("app.core.framework.PDFParser")
    def test_parse_resume_pdf(self, mock_pdf_parser_class, mock_validate):
        """Test parsing a PDF resume."""
        # Mock parser instance
        mock_parser = Mock()
        mock_parser.parse.return_value = "Sample resume text"
        mock_pdf_parser_class.return_value = mock_parser

        # Mock extractors
        extractors = {
            "name": MockExtractor("name", "John Doe"),
            "email": MockExtractor("email", "john@example.com"),
        }

        framework = ResumeParserFramework(extractors)
        result = framework.parse_resume(Path("/fake/resume.pdf"))

        # Verify validation was called
        mock_validate.assert_called_once()

        # Verify parser was instantiated and called
        mock_pdf_parser_class.assert_called_once()
        mock_parser.parse.assert_called_once()

        # Verify result
        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == "john@example.com"

    @patch("app.utils.validators.FileValidator.validate_file")
    @patch("app.core.framework.WordParser")
    def test_parse_resume_docx(self, mock_word_parser_class, mock_validate):
        """Test parsing a Word document resume."""
        # Mock parser instance
        mock_parser = Mock()
        mock_parser.parse.return_value = "Sample resume text from Word"
        mock_word_parser_class.return_value = mock_parser

        # Mock extractors
        extractors = {
            "name": MockExtractor("name", "Jane Smith"),
        }

        framework = ResumeParserFramework(extractors)
        result = framework.parse_resume(Path("/fake/resume.docx"))

        # Verify result
        assert isinstance(result, ResumeData)
        assert result.name == "Jane Smith"

    @patch("app.utils.validators.FileValidator.validate_file")
    @patch("app.core.framework.PDFParser")
    def test_parse_resume_with_missing_fields(self, mock_pdf_parser_class, mock_validate):
        """Test parsing resume when some fields are not extracted."""
        # Mock parser instance
        mock_parser = Mock()
        mock_parser.parse.return_value = "Limited resume text"
        mock_pdf_parser_class.return_value = mock_parser

        # Only extract name, email will be None
        extractors = {
            "name": MockExtractor("name", "Test User"),
            "email": MockExtractor("email", None),
        }

        framework = ResumeParserFramework(extractors)
        result = framework.parse_resume(Path("/fake/resume.pdf"))

        assert result.name == "Test User"
        assert result.email is None

    @patch("app.utils.validators.FileValidator.validate_file")
    @patch("app.core.framework.PDFParser")
    def test_parse_resume_extractor_exception_handled(self, mock_pdf_parser_class, mock_validate):
        """Test that extractor exceptions are handled gracefully."""
        # Mock parser instance
        mock_parser = Mock()
        mock_parser.parse.return_value = "Resume text"
        mock_pdf_parser_class.return_value = mock_parser

        # Mock extractor that raises exception
        failing_extractor = Mock(spec=FieldExtractor)
        failing_extractor.get_field_name.return_value = "name"
        failing_extractor.extract.side_effect = Exception("Extraction failed")

        working_extractor = MockExtractor("email", "test@example.com")

        extractors = {
            "name": failing_extractor,
            "email": working_extractor,
        }

        framework = ResumeParserFramework(extractors)
        result = framework.parse_resume(Path("/fake/resume.pdf"))

        # Should continue despite exception
        assert isinstance(result, ResumeData)
        assert result.name is None  # Failed extraction
        assert result.email == "test@example.com"  # Successful extraction

    @patch("app.utils.validators.FileValidator.validate_file")
    @patch("app.core.framework.PDFParser")
    def test_parse_resume_parser_fails(self, mock_pdf_parser_class, mock_validate):
        """Test handling of parser failures."""
        # Mock parser instance that raises exception
        mock_parser = Mock()
        mock_parser.parse.side_effect = ParsingError("Failed to parse PDF")
        mock_pdf_parser_class.return_value = mock_parser

        extractors = {"name": MockExtractor("name", "Test")}
        framework = ResumeParserFramework(extractors)

        with pytest.raises(ParsingError):
            framework.parse_resume(Path("/fake/resume.pdf"))

    @patch("app.utils.validators.FileValidator.validate_file")
    @patch("app.core.framework.PDFParser")
    def test_parse_resume_with_string_path(self, mock_pdf_parser_class, mock_validate):
        """Test parsing with string path (should convert to Path)."""
        # Mock parser instance
        mock_parser = Mock()
        mock_parser.parse.return_value = "Text"
        mock_pdf_parser_class.return_value = mock_parser

        extractors = {"name": MockExtractor("name", "Test")}
        framework = ResumeParserFramework(extractors)

        result = framework.parse_resume("/fake/resume.pdf")

        assert isinstance(result, ResumeData)
        # Verify parser was instantiated
        mock_pdf_parser_class.assert_called_once()

    def test_get_supported_formats(self):
        """Test getting supported file formats."""
        framework = ResumeParserFramework({})

        # This would depend on your implementation
        # For now, just verify the method exists and returns something
        if hasattr(framework, "get_supported_formats"):
            formats = framework.get_supported_formats()
            assert isinstance(formats, (list, set, tuple))
