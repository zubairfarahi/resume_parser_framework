"""Prompts for LLM-based extraction."""

from app.prompts.resume_extraction_prompts import (
    generate_education_extraction_prompt,
    generate_email_extraction_prompt,
    generate_experience_extraction_prompt,
    generate_name_extraction_prompt,
    generate_phone_extraction_prompt,
    generate_skills_extraction_prompt,
)

__all__ = [
    "generate_skills_extraction_prompt",
    "generate_name_extraction_prompt",
    "generate_email_extraction_prompt",
    "generate_phone_extraction_prompt",
    "generate_education_extraction_prompt",
    "generate_experience_extraction_prompt",
]
