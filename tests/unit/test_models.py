"""Unit tests for data models."""

import pytest
from pydantic import ValidationError

from app.core.models.resume_data import Education, ResumeData, WorkExperience


class TestResumeData:
    """Test suite for ResumeData model."""

    def test_create_minimal_resume_data(self) -> None:
        """Test creating ResumeData with minimal fields."""
        resume = ResumeData()

        assert resume.name is None
        assert resume.email is None
        assert resume.skills == []
        assert resume.experience == []
        assert resume.education == []

    def test_create_complete_resume_data(self, sample_resume_data: ResumeData) -> None:
        """Test creating ResumeData with all fields."""
        assert sample_resume_data.name == "John Doe"
        assert sample_resume_data.email == "john.doe@example.com"
        assert len(sample_resume_data.skills) == 5
        assert len(sample_resume_data.experience) == 2
        assert len(sample_resume_data.education) == 1

    def test_email_validation(self) -> None:
        """Test email validation."""
        # Valid email
        resume = ResumeData(email="test@example.com")
        assert resume.email == "test@example.com"

        # Invalid email should raise validation error
        with pytest.raises(ValidationError):
            ResumeData(email="invalid-email")

    def test_phone_validation(self) -> None:
        """Test phone number validation and cleaning."""
        # Valid phone with formatting
        resume = ResumeData(phone="+1-555-123-4567")
        assert resume.phone == "+15551234567"

        # Phone too short
        resume = ResumeData(phone="123")
        assert resume.phone is None

    def test_skills_deduplication(self) -> None:
        """Test that duplicate skills are removed."""
        resume = ResumeData(
            skills=["Python", "python", "PYTHON", "Java", "Python"]
        )

        # Should have only 2 unique skills (Python and Java)
        assert len(resume.skills) == 2
        assert "Python" in resume.skills
        assert "Java" in resume.skills

    def test_to_dict(self, sample_resume_data: ResumeData) -> None:
        """Test conversion to dictionary."""
        data_dict = sample_resume_data.to_dict()

        assert isinstance(data_dict, dict)
        assert data_dict["name"] == "John Doe"
        assert data_dict["email"] == "john.doe@example.com"

    def test_to_json(self, sample_resume_data: ResumeData) -> None:
        """Test conversion to JSON string."""
        json_str = sample_resume_data.to_json()

        assert isinstance(json_str, str)
        assert "John Doe" in json_str
        assert "john.doe@example.com" in json_str


class TestWorkExperience:
    """Test suite for WorkExperience model."""

    def test_create_work_experience(self) -> None:
        """Test creating WorkExperience instance."""
        experience = WorkExperience(
            company="Tech Corp",
            title="Software Engineer",
            start_date="2020-01",
            end_date="2023-12",
            description="Backend development",
            responsibilities=["Developed APIs", "Code reviews"],
        )

        assert experience.company == "Tech Corp"
        assert experience.title == "Software Engineer"
        assert len(experience.responsibilities) == 2


class TestEducation:
    """Test suite for Education model."""

    def test_create_education(self) -> None:
        """Test creating Education instance."""
        education = Education(
            institution="University of California",
            degree="Bachelor of Science",
            field_of_study="Computer Science",
            graduation_date="2018",
            gpa="3.8",
        )

        assert education.institution == "University of California"
        assert education.degree == "Bachelor of Science"
        assert education.gpa == "3.8"
