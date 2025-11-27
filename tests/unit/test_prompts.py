"""Tests for prompt generation utilities."""

from app.prompts import resume_extraction_prompts as prompts


def test_generate_skills_prompt_truncates_long_text() -> None:
    """Skills prompt should include role text and truncate after 3000 chars."""
    text = "A" * 3000 + "EXTRA_SKILLS_SECTION"
    prompt = prompts.generate_skills_extraction_prompt(text)

    assert prompts.ROLE_RESUME_EXPERT.strip() in prompt
    assert "A" * 3000 in prompt
    assert "EXTRA_SKILLS_SECTION" not in prompt
    assert "JSON array of strings" in prompt


def test_generate_name_prompt_limits_context() -> None:
    """Name prompt should only include first 500 characters."""
    text = "B" * 500 + "NAME_TAIL"
    prompt = prompts.generate_name_extraction_prompt(text)

    assert "B" * 500 in prompt
    assert "NAME_TAIL" not in prompt
    assert '{"name": "Full Name"}' in prompt


def test_generate_email_prompt_limits_context() -> None:
    """Email prompt should limit to 1000 characters."""
    text = "Contact info " * 200
    prompt = prompts.generate_email_extraction_prompt(text)

    assert text[:1000] in prompt
    assert text[1000:] not in prompt
    assert '{"email": "email@example.com"}' in prompt


def test_generate_phone_prompt_limits_context() -> None:
    """Phone prompt should limit to 1000 characters."""
    text = "Phone info " * 200
    prompt = prompts.generate_phone_extraction_prompt(text)

    assert text[:1000] in prompt
    assert text[1000:] not in prompt
    assert '{"phone": "+1 (123) 456-7890"}' in prompt


def test_generate_education_prompt_includes_full_text() -> None:
    """Education prompt should include full resume text."""
    text = "Education details " * 200
    prompt = prompts.generate_education_extraction_prompt(text)

    assert text in prompt
    assert '"institution": "University Name"' in prompt


def test_generate_experience_prompt_includes_full_text() -> None:
    """Experience prompt should include full resume text."""
    text = "Experience details " * 200
    prompt = prompts.generate_experience_extraction_prompt(text)

    assert text in prompt
    assert '"company": "Company Name"' in prompt
