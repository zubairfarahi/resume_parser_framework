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
I need you to analyze the following resume text and extract ALL relevant professional skills EXPLICITLY mentioned in the resume.

ONLY extract skills that are clearly listed or mentioned. Do NOT infer or add generic skills.

Focus on identifying:
- Programming languages (Python, JavaScript, C++, Java, etc.)
- Frameworks and libraries (FastAPI, Django, React, PyTorch, TensorFlow, etc.)
- Tools and technologies (Docker, Git, AWS, Azure, Kubernetes, etc.)
- Databases (PostgreSQL, MySQL, MongoDB, Redis, etc.)
- Machine learning / AI technologies (LLMs, RAG, computer vision, NLP, etc.)
- Cloud platforms and services (AWS, Azure, GCP and their services)
- DevOps and CI/CD tools (GitHub Actions, Jenkins, GitLab CI, etc.)
- Certifications mentioned

IMPORTANT:
- Your response must be a single, valid, raw JSON array of strings
- Do NOT add any comments, introductory text, or markdown formatting
- Only include skills EXPLICITLY mentioned in the resume text
- Do NOT add generic soft skills unless explicitly listed

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


# Phone extraction instruction
PHONE_EXTRACTION_INSTRUCTION = """
I need you to identify the phone number of the candidate from the following resume text.

Look for formats like: +1 (123) 456-7890, +1-123-456-7890, (123) 456-7890, 123-456-7890, etc.

IMPORTANT: Your response must be a single, valid, raw JSON object with the phone field.
Do not add any comments, introductory text, or markdown formatting.
If no phone number is found, return {{"phone": null}}

JSON format:
{{"phone": "+1 (123) 456-7890"}}

Resume text:
{resume_text}

Please place your answer here (JSON object only):
"""


# Education extraction instruction
EDUCATION_EXTRACTION_INSTRUCTION = """
I need you to extract ALL education entries from the following resume text.

For each education entry, extract:
- institution: University/College name
- degree: Degree type (BSc, MSc, PhD, etc.)
- field: Field of study
- start_year: Start year
- end_year: End year (or "Present" if ongoing)

IMPORTANT:
- Your response must be a single, valid, raw JSON array of objects
- Do not add any comments, introductory text, or markdown formatting
- Extract ALL education entries, not just the most recent
- If no education is found, return []

JSON format:
[
  {{
    "institution": "University Name",
    "degree": "BSc",
    "field": "Computer Science",
    "start_year": "2016",
    "end_year": "2020"
  }}
]

Resume text:
{resume_text}

Please place your answer here (JSON array only):
"""


# Experience extraction instruction
EXPERIENCE_EXTRACTION_INSTRUCTION = """
I need you to extract ALL work experience entries from the following resume text.

For each experience entry, extract:
- company: Company name
- position: Job title/position
- location: City, Country
- start_date: Start date (e.g., "May 2025", "Nov 2023")
- end_date: End date (or "Present" if current)
- description: Brief summary of responsibilities (1-2 sentences max)

IMPORTANT:
- Your response must be a single, valid, raw JSON array of objects
- Do not add any comments, introductory text, or markdown formatting
- Extract ALL experience entries in reverse chronological order
- Keep descriptions brief and factual
- If no experience is found, return []

JSON format:
[
  {{
    "company": "Company Name",
    "position": "Job Title",
    "location": "City, Country",
    "start_date": "Jan 2023",
    "end_date": "Present",
    "description": "Brief description of role and responsibilities"
  }}
]

Resume text:
{resume_text}

Please place your answer here (JSON array only):
"""


def generate_phone_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for phone extraction.

    Args:
        resume_text: Raw text from resume

    Returns:
        Formatted prompt for OpenAI
    """
    # Use first 1000 chars where phone is likely to be
    truncated_text = resume_text[:1000] if len(resume_text) > 1000 else resume_text

    prompt = f"""{ROLE_RESUME_EXPERT}

{PHONE_EXTRACTION_INSTRUCTION.format(resume_text=truncated_text)}"""

    return prompt


def generate_education_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for education extraction.

    Args:
        resume_text: Raw text from resume

    Returns:
        Formatted prompt for OpenAI
    """
    prompt = f"""{ROLE_RESUME_EXPERT}

{EDUCATION_EXTRACTION_INSTRUCTION.format(resume_text=resume_text)}"""

    return prompt


def generate_experience_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for experience extraction.

    Args:
        resume_text: Raw text from resume

    Returns:
        Formatted prompt for OpenAI
    """
    prompt = f"""{ROLE_RESUME_EXPERT}

{EXPERIENCE_EXTRACTION_INSTRUCTION.format(resume_text=resume_text)}"""

    return prompt
