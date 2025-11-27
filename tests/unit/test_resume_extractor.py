"""Unit tests for ResumeExtractor."""

from unittest.mock import Mock

from app.core.extractors.base import FieldExtractor
from app.core.models.resume_data import ResumeData
from app.core.resume_extractor import ResumeExtractor


class MockExtractor(FieldExtractor):
    """Mock extractor for testing."""

    def __init__(self, field_name: str, return_value=None):
        super().__init__()
        self.field_name = field_name
        self.return_value = return_value
        self.called = False

    def extract(self, text: str):
        self.called = True
        return self.return_value

    def get_field_name(self) -> str:
        return self.field_name


class TestResumeExtractor:
    """Test suite for ResumeExtractor."""

    def test_initialization_with_extractors(self):
        """Test extractor initialization."""
        extractors = {
            "name": MockExtractor("name", "John Doe"),
            "email": MockExtractor("email", "john@example.com"),
        }

        extractor = ResumeExtractor(extractors)

        assert extractor.extractors == extractors
        assert len(extractor.extractors) == 2

    def test_extract_all_fields(self):
        """Test extracting all fields from text."""
        extractors = {
            "name": MockExtractor("name", "John Doe"),
            "email": MockExtractor("email", "john@example.com"),
            "skills": MockExtractor("skills", ["Python", "JavaScript"]),
        }

        extractor = ResumeExtractor(extractors)
        text = "Sample resume text"
        result = extractor.extract(text)

        # Verify all extractors were called
        assert extractors["name"].called
        assert extractors["email"].called
        assert extractors["skills"].called

        # Verify result is ResumeData
        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == "john@example.com"
        assert result.skills == ["Python", "JavaScript"]

    def test_extract_with_none_values(self):
        """Test extraction when some fields return None."""
        extractors = {
            "name": MockExtractor("name", "Jane Smith"),
            "email": MockExtractor("email", None),  # Not found
            "phone": MockExtractor("phone", None),  # Not found
        }

        extractor = ResumeExtractor(extractors)
        result = extractor.extract("Resume text")

        assert result.name == "Jane Smith"
        assert result.email is None
        assert result.phone is None

    def test_extract_with_empty_text(self):
        """Test extraction with empty text."""
        extractors = {
            "name": MockExtractor("name", None),
        }

        extractor = ResumeExtractor(extractors)

        # Should handle empty text gracefully
        result = extractor.extract("")

        assert isinstance(result, ResumeData)
        assert result.name is None

    def test_extract_handles_extractor_exceptions(self):
        """Test that extractor exceptions are handled."""
        failing_extractor = Mock(spec=FieldExtractor)
        failing_extractor.get_field_name.return_value = "name"
        failing_extractor.extract.side_effect = Exception("Extraction failed")

        working_extractor = MockExtractor("email", "test@example.com")

        extractors = {
            "name": failing_extractor,
            "email": working_extractor,
        }

        extractor = ResumeExtractor(extractors)
        result = extractor.extract("Resume text")

        # Should handle exception and continue
        assert isinstance(result, ResumeData)
        assert result.name is None  # Failed
        assert result.email == "test@example.com"  # Succeeded

    def test_extract_with_no_extractors(self):
        """Test extraction with no extractors."""
        extractor = ResumeExtractor({})
        result = extractor.extract("Some text")

        assert isinstance(result, ResumeData)
        # All fields should be None/empty
        assert result.name is None
        assert result.email is None

    def test_extract_with_complex_data_types(self):
        """Test extraction with complex data types (lists, dicts)."""
        extractors = {
            "name": MockExtractor("name", "John Doe"),
            "skills": MockExtractor("skills", ["Python", "Java", "Docker"]),
            "education": MockExtractor("education", []),  # Empty list
            "experience": MockExtractor("experience", []),  # Empty list
        }

        extractor = ResumeExtractor(extractors)
        result = extractor.extract("Resume text with skills")

        assert result.name == "John Doe"
        assert len(result.skills) == 3
        assert "Python" in result.skills
        assert result.education == []
        assert result.experience == []

    def test_extractor_order_independence(self):
        """Test that extraction works regardless of extractor order."""
        # Define extractors in different order
        extractors_order1 = {
            "email": MockExtractor("email", "test@example.com"),
            "name": MockExtractor("name", "Test User"),
        }

        extractors_order2 = {
            "name": MockExtractor("name", "Test User"),
            "email": MockExtractor("email", "test@example.com"),
        }

        extractor1 = ResumeExtractor(extractors_order1)
        extractor2 = ResumeExtractor(extractors_order2)

        result1 = extractor1.extract("Text")
        result2 = extractor2.extract("Text")

        # Results should be the same regardless of order
        assert result1.name == result2.name
        assert result1.email == result2.email

    def test_extract_validates_result(self):
        """Test that extracted data is validated by Pydantic."""
        extractors = {
            "name": MockExtractor("name", "Valid Name"),
            "email": MockExtractor("email", "valid@example.com"),
        }

        extractor = ResumeExtractor(extractors)
        result = extractor.extract("Resume text")

        # Pydantic should validate the data
        assert isinstance(result, ResumeData)
        assert result.name == "Valid Name"
        assert result.email == "valid@example.com"
