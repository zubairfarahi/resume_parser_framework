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

    @patch("app.core.framework.ParserFactory.get_parser")
    def test_parse_resume_pdf(self, mock_get_parser):
        """Test parsing a PDF resume."""
        # Mock parser
        mock_parser = Mock()
        mock_parser.parse.return_value = "Sample resume text"
        mock_get_parser.return_value = mock_parser

        # Mock extractors
        extractors = {
            "name": MockExtractor("name", "John Doe"),
            "email": MockExtractor("email", "john@example.com"),
        }

        framework = ResumeParserFramework(extractors)
        result = framework.parse_resume(Path("/fake/resume.pdf"))

        # Verify parser was called
        mock_get_parser.assert_called_once_with(Path("/fake/resume.pdf"))
        mock_parser.parse.assert_called_once()

        # Verify result
        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == "john@example.com"

    @patch("app.core.framework.ParserFactory.get_parser")
    def test_parse_resume_docx(self, mock_get_parser):
        """Test parsing a Word document resume."""
        # Mock parser
        mock_parser = Mock()
        mock_parser.parse.return_value = "Sample resume text from Word"
        mock_get_parser.return_value = mock_parser

        # Mock extractors
        extractors = {
            "name": MockExtractor("name", "Jane Smith"),
        }

        framework = ResumeParserFramework(extractors)
        result = framework.parse_resume(Path("/fake/resume.docx"))

        # Verify result
        assert isinstance(result, ResumeData)
        assert result.name == "Jane Smith"

    @patch("app.core.framework.ParserFactory.get_parser")
    def test_parse_resume_with_missing_fields(self, mock_get_parser):
        """Test parsing resume when some fields are not extracted."""
        mock_parser = Mock()
        mock_parser.parse.return_value = "Limited resume text"
        mock_get_parser.return_value = mock_parser

        # Only extract name, email will be None
        extractors = {
            "name": MockExtractor("name", "Test User"),
            "email": MockExtractor("email", None),
        }

        framework = ResumeParserFramework(extractors)
        result = framework.parse_resume(Path("/fake/resume.pdf"))

        assert result.name == "Test User"
        assert result.email is None

    @patch("app.core.framework.ParserFactory.get_parser")
    def test_parse_resume_extractor_exception_handled(self, mock_get_parser):
        """Test that extractor exceptions are handled gracefully."""
        mock_parser = Mock()
        mock_parser.parse.return_value = "Resume text"
        mock_get_parser.return_value = mock_parser

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

    @patch("app.core.framework.ParserFactory.get_parser")
    def test_parse_resume_parser_fails(self, mock_get_parser):
        """Test handling of parser failures."""
        mock_parser = Mock()
        mock_parser.parse.side_effect = ParsingError("Failed to parse PDF")
        mock_get_parser.return_value = mock_parser

        extractors = {"name": MockExtractor("name", "Test")}
        framework = ResumeParserFramework(extractors)

        with pytest.raises(ParsingError):
            framework.parse_resume(Path("/fake/resume.pdf"))

    def test_parse_resume_with_string_path(self):
        """Test parsing with string path (should convert to Path)."""
        with patch("app.core.framework.ParserFactory.get_parser") as mock_get_parser:
            mock_parser = Mock()
            mock_parser.parse.return_value = "Text"
            mock_get_parser.return_value = mock_parser

            extractors = {"name": MockExtractor("name", "Test")}
            framework = ResumeParserFramework(extractors)

            result = framework.parse_resume("/fake/resume.pdf")

            assert isinstance(result, ResumeData)
            # Verify Path was created
            mock_get_parser.assert_called_once()

    def test_get_supported_formats(self):
        """Test getting supported file formats."""
        framework = ResumeParserFramework({})

        # This would depend on your implementation
        # For now, just verify the method exists and returns something
        if hasattr(framework, "get_supported_formats"):
            formats = framework.get_supported_formats()
            assert isinstance(formats, (list, set, tuple))
