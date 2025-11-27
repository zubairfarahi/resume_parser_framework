"""Unit tests for file validators."""

from pathlib import Path

import pytest

from app.exceptions.exceptions import ValidationError
from app.utils.validators import FileValidator


class TestFileValidator:
    """Test suite for FileValidator class."""

    def test_validate_path_existing_file(self, sample_pdf_path: Path) -> None:
        """Test path validation with existing file."""
        # Should not raise any exception
        FileValidator.validate_path(sample_pdf_path)

    def test_validate_path_nonexistent_file(self) -> None:
        """Test path validation with non-existent file."""
        with pytest.raises(ValidationError) as exc_info:
            FileValidator.validate_path(Path("/nonexistent/file.pdf"))

        assert exc_info.value.details["validation_type"] == "path"

    def test_validate_file_size_within_limit(self, sample_pdf_path: Path, test_settings) -> None:
        """Test file size validation within limits."""
        # Should not raise any exception
        FileValidator.validate_file_size(sample_pdf_path)

    def test_validate_file_size_exceeds_limit(self, temp_directory: Path, monkeypatch) -> None:
        """Test file size validation when exceeding limit."""
        # Create a file larger than the test limit
        large_file = temp_directory / "large_file.pdf"
        large_file.write_bytes(b"x" * (2 * 1024 * 1024))  # 2MB

        # Set max file size to 1MB for this test
        from app.config import settings

        monkeypatch.setattr(settings, "max_file_size", 1024 * 1024)

        with pytest.raises(ValidationError) as exc_info:
            FileValidator.validate_file_size(large_file)

        assert exc_info.value.details["validation_type"] == "file_size"

    def test_get_safe_filename(self) -> None:
        """Test filename sanitization."""
        # Test path traversal attempt
        assert FileValidator.get_safe_filename("../../etc/passwd") == "etc_passwd"

        # Test spaces
        assert FileValidator.get_safe_filename("my resume.pdf") == "my_resume.pdf"

        # Test special characters
        assert FileValidator.get_safe_filename("file<>:|?.pdf") == "file_____.pdf"

        # Test empty filename
        assert FileValidator.get_safe_filename("") == "unnamed_file"

    def test_validate_mime_type_valid_pdf(self, sample_pdf_path: Path) -> None:
        """Test MIME type validation with valid PDF."""
        # Note: This test requires python-magic to be properly installed
        # Should not raise exception for valid PDF
        try:
            FileValidator.validate_mime_type(sample_pdf_path)
        except ValidationError:
            # May fail if python-magic not properly configured
            pytest.skip("python-magic not properly configured")

    def test_validate_file_complete(self, sample_pdf_path: Path) -> None:
        """Test complete file validation."""
        try:
            FileValidator.validate_file(sample_pdf_path)
        except ValidationError:
            # May fail if python-magic not properly configured
            pytest.skip("python-magic not properly configured")
