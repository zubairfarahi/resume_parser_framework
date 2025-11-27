"""Integration tests for the complete framework."""

from pathlib import Path

import pytest

from app.core.extractors import EmailExtractor, NameExtractor, SkillsExtractor
from app.core.framework import ResumeParserFramework
from app.core.models.resume_data import ResumeData


class TestResumeParserFramework:
    """Integration tests for end-to-end resume parsing."""

    @pytest.fixture
    def framework_with_regex_only(self) -> ResumeParserFramework:
        """Create framework with only regex-based extractors (no LLM)."""
        extractors = {
            "name": NameExtractor(),
            "email": EmailExtractor(),
        }
        return ResumeParserFramework(extractors)

    def test_framework_initialization(self, framework_with_regex_only: ResumeParserFramework) -> None:
        """Test framework initializes correctly."""
        assert framework_with_regex_only is not None
        assert framework_with_regex_only.resume_extractor is not None
        assert len(framework_with_regex_only.extractors) == 2

    def test_register_custom_parser(self, framework_with_regex_only: ResumeParserFramework) -> None:
        """Test registering custom parser."""
        from app.core.parsers import PDFParser

        framework_with_regex_only.register_parser(".txt", PDFParser)
        assert ".txt" in framework_with_regex_only._parsers

    def test_parse_resume_returns_resume_data(
        self, framework_with_regex_only: ResumeParserFramework, sample_pdf_path: Path
    ) -> None:
        """Test that parsing returns ResumeData instance."""
        try:
            result = framework_with_regex_only.parse_resume(str(sample_pdf_path))
            assert isinstance(result, ResumeData)
        except ImportError:
            pytest.skip("pypdf not installed")

    def test_parse_nonexistent_file_raises_error(
        self, framework_with_regex_only: ResumeParserFramework
    ) -> None:
        """Test that parsing nonexistent file raises error."""
        with pytest.raises(Exception):  # ValidationError or ParsingError
            framework_with_regex_only.parse_resume("/nonexistent/file.pdf")

    def test_parse_unsupported_format_raises_error(
        self, framework_with_regex_only: ResumeParserFramework, temp_directory: Path
    ) -> None:
        """Test that unsupported file format raises error."""
        # Create a file with unsupported extension
        unsupported_file = temp_directory / "resume.txt"
        unsupported_file.write_text("Some resume text")

        with pytest.raises(Exception):  # ParsingError
            framework_with_regex_only.parse_resume(str(unsupported_file))


class TestEndToEndWorkflow:
    """End-to-end workflow tests."""

    def test_complete_resume_extraction_flow(self, sample_resume_text: str) -> None:
        """Test complete flow from text to ResumeData."""
        from app.core.resume_extractor import ResumeExtractor

        # Create extractors (regex only, no LLM)
        extractors = {
            "name": NameExtractor(),
            "email": EmailExtractor(),
        }

        # Create extractor
        extractor = ResumeExtractor(extractors)

        # Extract data
        result = extractor.extract(sample_resume_text)

        # Verify results
        assert isinstance(result, ResumeData)
        assert result.name is not None  # Should extract from sample text
        assert result.email is not None  # Should extract from sample text

    def test_extraction_handles_missing_fields_gracefully(self) -> None:
        """Test that extraction handles missing fields without crashing."""
        from app.core.resume_extractor import ResumeExtractor

        extractors = {
            "name": NameExtractor(),
            "email": EmailExtractor(),
        }

        extractor = ResumeExtractor(extractors)

        # Text with no name or email
        text = "Just some random text without any extractable information"

        result = extractor.extract(text)

        assert isinstance(result, ResumeData)
        # Fields should be None if not found, not raise errors
        assert result.name is None or isinstance(result.name, str)
        assert result.email is None or isinstance(result.email, str)
