"""Resume extraction prompts for OpenAI LLM.

This module contains structured prompts for extracting information from resumes,
following the pattern from building-data-extractor.
"""

# Role definition for the LLM
ROLE_RESUME_EXPERT = """
You are an expert technical recruiter with 10+ years of experience analyzing resumes
and identifying professional skills, qualifications, and competencies.
"""

# Skills extraction instruction
SKILLS_EXTRACTION_INSTRUCTION = """
I need you to analyze the following resume text and extract ALL relevant professional skills.

Focus on identifying:
- Technical skills (programming languages, frameworks, tools, technologies)
- Soft skills (communication, leadership, teamwork, problem-solving)
- Domain expertise (machine learning, data analysis, cloud computing, web development, etc.)
- Certifications and qualifications
- Methodologies (Agile, Scrum, DevOps, CI/CD, etc.)

IMPORTANT: Your response must be a single, valid, raw JSON array of strings.
Do not add any comments, introductory text, or markdown formatting.

JSON format:
["skill1", "skill2", "skill3", ...]

Resume text:
{resume_text}

Please place your answer here (JSON array only):
"""

# Name extraction instruction (LLM-based fallback)
NAME_EXTRACTION_INSTRUCTION = """
I need you to identify the full name of the candidate from the following resume text.

The name is typically found at the top of the resume, before contact information.

IMPORTANT: Your response must be a single, valid, raw JSON object with the name field.
Do not add any comments, introductory text, or markdown formatting.

JSON format:
{{"name": "Full Name"}}

Resume text:
{resume_text}

Please place your answer here (JSON object only):
"""

# Email extraction instruction (LLM-based fallback)
EMAIL_EXTRACTION_INSTRUCTION = """
I need you to identify the email address of the candidate from the following resume text.

IMPORTANT: Your response must be a single, valid, raw JSON object with the email field.
Do not add any comments, introductory text, or markdown formatting.

JSON format:
{{"email": "email@example.com"}}

Resume text:
{resume_text}

Please place your answer here (JSON object only):
"""


def generate_skills_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for skills extraction.

    Args:
        resume_text: Raw text from resume

    Returns:
        Formatted prompt for OpenAI
    """
    # Truncate text if too long (keep first 3000 chars)
    truncated_text = resume_text[:3000] if len(resume_text) > 3000 else resume_text

    prompt = f"""{ROLE_RESUME_EXPERT}

{SKILLS_EXTRACTION_INSTRUCTION.format(resume_text=truncated_text)}"""

    return prompt


def generate_name_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for name extraction (LLM fallback).

    Args:
        resume_text: Raw text from resume

    Returns:
        Formatted prompt for OpenAI
    """
    # Use first 500 chars where name is likely to be
    truncated_text = resume_text[:500] if len(resume_text) > 500 else resume_text

    prompt = f"""{ROLE_RESUME_EXPERT}

{NAME_EXTRACTION_INSTRUCTION.format(resume_text=truncated_text)}"""

    return prompt


def generate_email_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for email extraction (LLM fallback).

    Args:
        resume_text: Raw text from resume

    Returns:
        Formatted prompt for OpenAI
    """
    # Use first 1000 chars where email is likely to be
    truncated_text = resume_text[:1000] if len(resume_text) > 1000 else resume_text

    prompt = f"""{ROLE_RESUME_EXPERT}

{EMAIL_EXTRACTION_INSTRUCTION.format(resume_text=truncated_text)}"""

    return prompt
