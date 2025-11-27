"""Resume data model for structured storage of parsed information.

This module defines the ResumeData Pydantic model that serves as the
standard output format for all resume parsing operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class WorkExperience(BaseModel):
    """Work experience entry."""

    company: str | None = None
    title: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None
    responsibilities: list[str] = Field(default_factory=list)


class Education(BaseModel):
    """Education entry."""

    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    graduation_date: str | None = None
    gpa: str | None = None


class ResumeData(BaseModel):
    """Structured resume data model.

    This model represents the complete parsed resume data with validation.
    All fields are optional to handle incomplete or partially extracted data.

    SOLID Principles:
    - Single Responsibility: Only handles data structure and validation
    - Open/Closed: Can be extended with additional fields without modification
    - Liskov Substitution: Can be used anywhere a BaseModel is expected
    - Interface Segregation: Clean interface with no unnecessary fields
    - Dependency Inversion: Uses Pydantic abstractions for validation

    Attributes:
        name: Full name of the candidate
        email: Email address (validated format)
        phone: Phone number
        location: Geographic location
        summary: Professional summary or objective
        skills: List of technical and soft skills
        experience: List of work experience entries
        education: List of education entries
        certifications: List of professional certifications
        languages: List of spoken/written languages
        linkedin_url: LinkedIn profile URL
        github_url: GitHub profile URL
        website_url: Personal website URL
        parsed_at: Timestamp when resume was parsed
    """

    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    summary: str | None = None

    skills: list[str] = Field(default_factory=list, description="Technical and soft skills")
    experience: list[WorkExperience] = Field(
        default_factory=list, description="Work experience history"
    )
    education: list[Education] = Field(default_factory=list, description="Educational background")
    certifications: list[str] = Field(
        default_factory=list, description="Professional certifications"
    )
    languages: list[str] = Field(default_factory=list, description="Spoken/written languages")

    linkedin_url: str | None = None
    github_url: str | None = None
    website_url: str | None = None

    parsed_at: datetime = Field(default_factory=datetime.now, description="Parsing timestamp")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Validate and clean phone number.

        Args:
            v: Phone number string

        Returns:
            Cleaned phone number or None
        """
        if v is None:
            return None

        # Remove common separators and whitespace
        cleaned = "".join(c for c in v if c.isdigit() or c == "+")

        # Basic validation: should have at least 10 digits
        digits = "".join(c for c in cleaned if c.isdigit())
        if len(digits) < 10:
            return None

        return cleaned

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, v: list[str]) -> list[str]:
        """Validate and clean skills list.

        Args:
            v: List of skills

        Returns:
            Cleaned and deduplicated skills list
        """
        # Remove empty strings and duplicates (case-insensitive)
        cleaned = [skill.strip() for skill in v if skill and skill.strip()]

        # Remove duplicates while preserving order (case-insensitive)
        seen = set()
        unique_skills = []
        for skill in cleaned:
            skill_lower = skill.lower()
            if skill_lower not in seen:
                seen.add(skill_lower)
                unique_skills.append(skill)

        return unique_skills

    def to_dict(self) -> dict:
        """Convert model to dictionary.

        Returns:
            Dictionary representation of the resume data
        """
        return self.model_dump()

    def to_json(self) -> str:
        """Convert model to JSON string.

        Returns:
            JSON string representation of the resume data
        """
        return self.model_dump_json(indent=2)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "location": "San Francisco, CA",
                "summary": "Experienced software engineer with 5+ years in Python development",
                "skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "AWS"],
                "experience": [
                    {
                        "company": "Tech Corp",
                        "title": "Senior Software Engineer",
                        "start_date": "2020-01",
                        "end_date": "Present",
                        "description": "Backend development team lead",
                        "responsibilities": [
                            "Led team of 5 engineers",
                            "Designed and implemented microservices architecture",
                        ],
                    }
                ],
                "education": [
                    {
                        "institution": "University of California",
                        "degree": "Bachelor of Science",
                        "field_of_study": "Computer Science",
                        "graduation_date": "2018",
                        "gpa": "3.8",
                    }
                ],
                "certifications": ["AWS Certified Solutions Architect"],
                "languages": ["English (Native)", "Spanish (Intermediate)"],
                "linkedin_url": "https://linkedin.com/in/johndoe",
                "github_url": "https://github.com/johndoe",
            }
        }
    )
