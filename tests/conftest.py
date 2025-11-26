"""Shared pytest fixtures for all tests.

This module provides reusable fixtures for testing the resume parser framework.
"""

from pathlib import Path
from typing import Generator

import pytest

from app.config.settings import Settings
from app.core.models.resume_data import Education, ResumeData, WorkExperience


@pytest.fixture
def temp_directory(tmp_path: Path) -> Generator[Path, None, None]:
    """Provide a temporary directory for test files.

    Args:
        tmp_path: Pytest's temporary path fixture

    Yields:
        Path to temporary directory
    """
    test_dir = tmp_path / "test_files"
    test_dir.mkdir(exist_ok=True)
    yield test_dir


@pytest.fixture
def sample_resume_data() -> ResumeData:
    """Provide sample resume data for testing.

    Returns:
        ResumeData instance with sample data
    """
    return ResumeData(
        name="John Doe",
        email="john.doe@example.com",
        phone="+1-555-123-4567",
        location="San Francisco, CA",
        summary="Experienced software engineer with 5+ years in Python development",
        skills=["Python", "FastAPI", "Docker", "PostgreSQL", "AWS"],
        experience=[
            WorkExperience(
                company="Tech Corp",
                title="Senior Software Engineer",
                start_date="2020-01",
                end_date="Present",
                description="Backend development team lead",
                responsibilities=[
                    "Led team of 5 engineers",
                    "Designed and implemented microservices architecture",
                ],
            ),
            WorkExperience(
                company="Startup Inc",
                title="Software Engineer",
                start_date="2018-06",
                end_date="2019-12",
                description="Full-stack development",
                responsibilities=["Built REST APIs", "Developed React frontend"],
            ),
        ],
        education=[
            Education(
                institution="University of California",
                degree="Bachelor of Science",
                field_of_study="Computer Science",
                graduation_date="2018",
                gpa="3.8",
            )
        ],
        certifications=["AWS Certified Solutions Architect"],
        languages=["English (Native)", "Spanish (Intermediate)"],
        linkedin_url="https://linkedin.com/in/johndoe",
        github_url="https://github.com/johndoe",
    )


@pytest.fixture
def sample_resume_text() -> str:
    """Provide sample resume text for testing extractors.

    Returns:
        Sample resume text as string
    """
    return """
    John Doe
    Software Engineer
    Email: john.doe@example.com
    Phone: +1-555-123-4567
    Location: San Francisco, CA

    SUMMARY
    Experienced software engineer with 5+ years in Python development.
    Specialized in backend systems and API design.

    SKILLS
    - Python, FastAPI, Django
    - Docker, Kubernetes
    - PostgreSQL, Redis
    - AWS, Azure

    EXPERIENCE

    Tech Corp - San Francisco, CA
    Senior Software Engineer, January 2020 - Present
    - Led team of 5 engineers
    - Designed and implemented microservices architecture
    - Improved system performance by 40%

    Startup Inc - San Francisco, CA
    Software Engineer, June 2018 - December 2019
    - Built REST APIs using FastAPI
    - Developed React frontend applications

    EDUCATION

    University of California, Berkeley
    Bachelor of Science in Computer Science, 2018
    GPA: 3.8/4.0

    CERTIFICATIONS
    - AWS Certified Solutions Architect
    - Python Professional Certificate

    LANGUAGES
    - English (Native)
    - Spanish (Intermediate)
    """


@pytest.fixture
def test_settings() -> Settings:
    """Provide test settings configuration.

    Returns:
        Settings instance for testing
    """
    return Settings(
        debug=True,
        environment="testing",
        max_file_size=1024 * 1024,  # 1MB for testing
        log_level="DEBUG",
    )


@pytest.fixture
def sample_pdf_path(temp_directory: Path) -> Path:
    """Create a sample PDF file for testing.

    Args:
        temp_directory: Temporary directory fixture

    Returns:
        Path to sample PDF file
    """
    # Create a minimal PDF file (just a placeholder for testing)
    pdf_path = temp_directory / "sample_resume.pdf"

    # Minimal valid PDF content
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Sample Resume) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000214 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
308
%%EOF
"""

    pdf_path.write_bytes(pdf_content)
    return pdf_path


@pytest.fixture(autouse=True)
def setup_test_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up test environment for all tests.

    Args:
        tmp_path: Pytest's temporary path fixture
        monkeypatch: Pytest's monkeypatch fixture
    """
    # Override settings for testing
    monkeypatch.setenv("RESUME_PARSER_ENVIRONMENT", "testing")
    monkeypatch.setenv("RESUME_PARSER_DEBUG", "true")
    monkeypatch.setenv("RESUME_PARSER_LOG_LEVEL", "DEBUG")
