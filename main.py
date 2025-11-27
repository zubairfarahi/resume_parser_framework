"""FastAPI application for resume parsing.

This module provides a REST API endpoint for uploading and parsing resumes.
"""

import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.logging_config import get_logger, setup_logging
from app.core.extractors import (
    EducationExtractor,
    EmailExtractor,
    ExperienceExtractor,
    NameExtractor,
    PhoneExtractor,
    SkillsExtractor,
)
from app.core.framework import ResumeParserFramework
from app.exceptions.exceptions import ParsingError, ValidationError

# Load environment variables from .env file
load_dotenv()

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Resume Parser API",
    description="Upload and parse resumes (PDF/Word) to extract structured information",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize framework with extractors
extractors = {
    "name": NameExtractor(),
    "email": EmailExtractor(),
    "phone": PhoneExtractor(),  # Uses OpenAI (configure via .env)
    "skills": SkillsExtractor(),  # Uses OpenAI (configure via .env)
    "education": EducationExtractor(),  # Uses OpenAI (configure via .env)
    "experience": ExperienceExtractor(),  # Uses OpenAI (configure via .env)
}
framework = ResumeParserFramework(extractors)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information.

    Returns:
        API information and available endpoints
    """
    return {
        "message": "Resume Parser API",
        "version": "1.0.0",
        "endpoints": {
            "parse": "POST /parse-resume - Upload and parse a resume",
            "health": "GET /health - Health check endpoint",
            "docs": "GET /docs - Interactive API documentation",
        },
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status message indicating API is running
    """
    return {"status": "healthy", "service": "resume-parser-api"}


@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)) -> JSONResponse:
    """Parse an uploaded resume file and extract structured information.

    This endpoint accepts PDF or Word (.docx) resume files and extracts:
    - Name
    - Email
    - Phone (using OpenAI LLM)
    - Skills (using OpenAI LLM)
    - Education (using OpenAI LLM)
    - Experience (using OpenAI LLM)

    Args:
        file: Uploaded resume file (PDF or Word)

    Returns:
        JSONResponse with extracted resume data

    Raises:
        HTTPException: If file validation fails or parsing errors occur

    Example:
        ```bash
        curl -X POST "http://localhost:8000/parse-resume" \\
             -F "file=@/path/to/resume.pdf"
        ```

        Response:
        ```json
        {
            "success": true,
            "data": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1 (555) 123-4567",
                "skills": ["Python", "FastAPI", "Machine Learning"],
                "education": [...],
                "experience": [...]
            },
            "filename": "resume.pdf"
        }
        ```
    """
    logger.info("Received resume upload request", filename=file.filename)

    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        logger.warning(
            "Invalid file extension",
            filename=file.filename,
            extension=file_ext,
            allowed=list(ALLOWED_EXTENSIONS),
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid file format",
                "message": f"Only {', '.join(ALLOWED_EXTENSIONS)} files are supported",
                "received": file_ext,
            },
        )

    # Validate file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        logger.warning(
            "File too large",
            filename=file.filename,
            size_mb=file_size / (1024 * 1024),
            max_mb=MAX_FILE_SIZE / (1024 * 1024),
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error": "File too large",
                "message": f"Maximum file size is {MAX_FILE_SIZE / (1024 * 1024)}MB",
                "received_mb": round(file_size / (1024 * 1024), 2),
            },
        )

    # Save uploaded file to temporary location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        logger.debug(
            "Saved uploaded file to temporary location",
            temp_path=tmp_file_path,
            size_bytes=len(content),
        )

        # Parse the resume
        logger.info("Starting resume parsing", filename=file.filename)
        resume_data = framework.parse_resume(tmp_file_path)

        # Convert to dict for JSON response
        # Use model_dump() to convert Pydantic models to dicts (including nested Education/WorkExperience)
        resume_dict = resume_data.model_dump()

        result = {
            "success": True,
            "data": {
                "name": resume_dict["name"],
                "email": resume_dict["email"],
                "phone": resume_dict["phone"],
                "skills": resume_dict["skills"],
                "education": resume_dict["education"],  # Now properly serialized
                "experience": resume_dict["experience"],  # Now properly serialized
            },
            "filename": file.filename,
        }

        logger.info(
            "Resume parsed successfully",
            filename=file.filename,
            extracted_fields={
                "name": resume_data.name is not None,
                "email": resume_data.email is not None,
                "skills_count": len(resume_data.skills) if resume_data.skills else 0,
            },
        )

        return JSONResponse(content=result, status_code=200)

    except ValidationError as e:
        logger.error(
            "Validation error during parsing",
            filename=file.filename,
            error=str(e),
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Validation error",
                "message": str(e),
                "filename": file.filename,
            },
        )

    except ParsingError as e:
        logger.error(
            "Parsing error",
            filename=file.filename,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Parsing error",
                "message": str(e),
                "filename": file.filename,
            },
        )

    except Exception as e:
        logger.error(
            "Unexpected error during resume parsing",
            filename=file.filename,
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred while parsing the resume",
                "filename": file.filename,
            },
        )

    finally:
        # Clean up temporary file
        try:
            Path(tmp_file_path).unlink()
            logger.debug("Cleaned up temporary file", temp_path=tmp_file_path)
        except Exception as e:
            logger.warning(
                "Failed to clean up temporary file",
                temp_path=tmp_file_path,
                error=str(e),
            )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Resume Parser API server")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info",
    )
