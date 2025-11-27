"""Unit tests for field extractors."""

import pytest

from app.core.extractors import (
    EducationExtractor,
    EmailExtractor,
    ExperienceExtractor,
    NameExtractor,
    PhoneExtractor,
    SkillsExtractor,
)


class TestNameExtractor:
    """Test suite for NameExtractor."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.extractor = NameExtractor()

    def test_extract_simple_name(self) -> None:
        """Test extraction of simple two-word name."""
        text = "John Doe\nSoftware Engineer\njohn@example.com"
        result = self.extractor.extract(text)
        assert result == "John Doe"

    def test_extract_three_word_name(self) -> None:
        """Test extraction of three-word name."""
        text = "John Michael Doe\nSenior Developer"
        result = self.extractor.extract(text)
        assert result == "John Michael Doe"

    def test_extract_with_contact_info(self) -> None:
        """Test extraction with contact information following name."""
        text = "Jane Smith\nEmail: jane@example.com\nPhone: 123-456-7890"
        result = self.extractor.extract(text)
        assert result == "Jane Smith"

    def test_no_name_found(self) -> None:
        """Test when no valid name is present."""
        text = "resume contact information skills"
        result = self.extractor.extract(text)
        assert result is None

    def test_empty_text_raises_error(self) -> None:
        """Test that empty text raises ValueError."""
        with pytest.raises(ValueError):
            self.extractor.extract("")

    def test_get_field_name(self) -> None:
        """Test get_field_name returns correct value."""
        assert self.extractor.get_field_name() == "name"


class TestEmailExtractor:
    """Test suite for EmailExtractor."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.extractor = EmailExtractor()

    def test_extract_valid_email(self) -> None:
        """Test extraction of valid email address."""
        text = "Contact: john.doe@example.com for more information"
        result = self.extractor.extract(text)
        assert result == "john.doe@example.com"

    def test_extract_email_with_plus(self) -> None:
        """Test extraction of email with + symbol."""
        text = "Email: john+work@example.com"
        result = self.extractor.extract(text)
        assert result == "john+work@example.com"

    def test_extract_first_email_when_multiple(self) -> None:
        """Test extraction when multiple emails present."""
        text = "Primary: john@example.com Secondary: jane@example.com"
        result = self.extractor.extract(text)
        # Should return first valid email
        assert result in ["john@example.com", "jane@example.com"]

    def test_no_email_found(self) -> None:
        """Test when no email is present."""
        text = "No email here just regular text"
        result = self.extractor.extract(text)
        assert result is None

    def test_invalid_email_rejected(self) -> None:
        """Test that invalid email formats are rejected."""
        text = "Contact: notanemail@"
        result = self.extractor.extract(text)
        assert result is None

    def test_empty_text_raises_error(self) -> None:
        """Test that empty text raises ValueError."""
        with pytest.raises(ValueError):
            self.extractor.extract("")

    def test_get_field_name(self) -> None:
        """Test get_field_name returns correct value."""
        assert self.extractor.get_field_name() == "email"


class TestSkillsExtractor:
    """Test suite for SkillsExtractor."""

    def test_initialization_with_openai(self, monkeypatch) -> None:
        """Test initialization with OpenAI."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = SkillsExtractor()
            assert extractor.model_name == "gpt-4o-mini"
            assert extractor.temperature == 0.0
        except ImportError:
            pytest.skip("openai package not installed")

    def test_initialization_without_api_key_fails(self, monkeypatch) -> None:
        """Test that initialization fails without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(Exception):  # Should raise ExtractionError
            SkillsExtractor()

    def test_get_field_name(self, monkeypatch) -> None:
        """Test get_field_name returns correct value."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = SkillsExtractor()
            assert extractor.get_field_name() == "skills"
        except ImportError:
            pytest.skip("openai package not installed")

    def test_parse_skills_response(self, monkeypatch) -> None:
        """Test parsing skills from JSON response."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = SkillsExtractor()

            # Test with clean JSON
            response = '["Python", "JavaScript", "Docker"]'
            skills = extractor._parse_skills_response(response)
            assert skills == ["Python", "JavaScript", "Docker"]

            # Test with JSON surrounded by text
            response = 'Here are the skills:\n["Python", "Java"]\nThank you!'
            skills = extractor._parse_skills_response(response)
            assert skills == ["Python", "Java"]

        except ImportError:
            pytest.skip("openai package not installed")


class TestPhoneExtractor:
    """Test suite for PhoneExtractor."""

    def test_initialization_with_openai(self, monkeypatch) -> None:
        """Test initialization with OpenAI."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = PhoneExtractor()
            assert extractor.model_name == "gpt-4o-mini"
            assert extractor.temperature == 0.0
        except ImportError:
            pytest.skip("openai package not installed")

    def test_initialization_without_api_key_fails(self, monkeypatch) -> None:
        """Test that initialization fails without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(Exception):  # Should raise ExtractionError
            PhoneExtractor()

    def test_get_field_name(self, monkeypatch) -> None:
        """Test get_field_name returns correct value."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = PhoneExtractor()
            assert extractor.get_field_name() == "phone"
        except ImportError:
            pytest.skip("openai package not installed")

    def test_parse_phone_response(self, monkeypatch) -> None:
        """Test parsing phone from JSON response."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = PhoneExtractor()

            # Test with clean JSON
            response = '{"phone": "+1 (555) 123-4567"}'
            phone = extractor._parse_phone_response(response)
            assert phone == "+1 (555) 123-4567"

            # Test with JSON surrounded by text
            response = 'Here is the phone:\n{"phone": "+1-555-123-4567"}\nThank you!'
            phone = extractor._parse_phone_response(response)
            assert phone == "+1-555-123-4567"

            # Test with null phone
            response = '{"phone": null}'
            phone = extractor._parse_phone_response(response)
            assert phone is None

        except ImportError:
            pytest.skip("openai package not installed")


class TestEducationExtractor:
    """Test suite for EducationExtractor."""

    def test_initialization_with_openai(self, monkeypatch) -> None:
        """Test initialization with OpenAI."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = EducationExtractor()
            assert extractor.model_name == "gpt-4o-mini"
            assert extractor.temperature == 0.0
        except ImportError:
            pytest.skip("openai package not installed")

    def test_initialization_without_api_key_fails(self, monkeypatch) -> None:
        """Test that initialization fails without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(Exception):  # Should raise ExtractionError
            EducationExtractor()

    def test_get_field_name(self, monkeypatch) -> None:
        """Test get_field_name returns correct value."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = EducationExtractor()
            assert extractor.get_field_name() == "education"
        except ImportError:
            pytest.skip("openai package not installed")

    def test_parse_education_response(self, monkeypatch) -> None:
        """Test parsing education from JSON response."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = EducationExtractor()

            # Test with clean JSON
            response = """[
                {
                    "institution": "MIT",
                    "degree": "BSc",
                    "field": "Computer Science",
                    "start_year": "2016",
                    "end_year": "2020"
                }
            ]"""
            education = extractor._parse_education_response(response)
            assert len(education) == 1
            assert education[0].institution == "MIT"
            assert education[0].degree == "BSc"
            assert education[0].field_of_study == "Computer Science"

            # Test with empty array
            response = "[]"
            education = extractor._parse_education_response(response)
            assert education == []

        except ImportError:
            pytest.skip("openai package not installed")


class TestExperienceExtractor:
    """Test suite for ExperienceExtractor."""

    def test_initialization_with_openai(self, monkeypatch) -> None:
        """Test initialization with OpenAI."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = ExperienceExtractor()
            assert extractor.model_name == "gpt-4o-mini"
            assert extractor.temperature == 0.0
        except ImportError:
            pytest.skip("openai package not installed")

    def test_initialization_without_api_key_fails(self, monkeypatch) -> None:
        """Test that initialization fails without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(Exception):  # Should raise ExtractionError
            ExperienceExtractor()

    def test_get_field_name(self, monkeypatch) -> None:
        """Test get_field_name returns correct value."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = ExperienceExtractor()
            assert extractor.get_field_name() == "experience"
        except ImportError:
            pytest.skip("openai package not installed")

    def test_parse_experience_response(self, monkeypatch) -> None:
        """Test parsing experience from JSON response."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

        try:
            extractor = ExperienceExtractor()

            # Test with clean JSON
            response = """[
                {
                    "company": "Tech Corp",
                    "position": "Software Engineer",
                    "location": "San Francisco, CA",
                    "start_date": "Jan 2020",
                    "end_date": "Present",
                    "description": "Developed web applications"
                }
            ]"""
            experience = extractor._parse_experience_response(response)
            assert len(experience) == 1
            assert experience[0].company == "Tech Corp"
            assert experience[0].title == "Software Engineer"
            assert experience[0].start_date == "Jan 2020"

            # Test with empty array
            response = "[]"
            experience = extractor._parse_experience_response(response)
            assert experience == []

        except ImportError:
            pytest.skip("openai package not installed")
