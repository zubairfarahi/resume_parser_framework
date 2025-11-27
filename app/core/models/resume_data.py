"""Resume data model for structured storage of parsed information.

This module defines the ResumeData Pydantic model that serves as the
standard output format for all resume parsing operations.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class WorkExperience(BaseModel):
    """Work experience entry."""

    company: Optional[str] = None
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)


class Education(BaseModel):
    """Education entry."""

    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None


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

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

    skills: List[str] = Field(default_factory=list, description="Technical and soft skills")
    experience: List[WorkExperience] = Field(
        default_factory=list, description="Work experience history"
    )
    education: List[Education] = Field(default_factory=list, description="Educational background")
    certifications: List[str] = Field(
        default_factory=list, description="Professional certifications"
    )
    languages: List[str] = Field(default_factory=list, description="Spoken/written languages")

    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website_url: Optional[str] = None

    parsed_at: datetime = Field(default_factory=datetime.now, description="Parsing timestamp")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
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
    def validate_skills(cls, v: List[str]) -> List[str]:
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

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
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
