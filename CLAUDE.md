# Resume Parser Framework - Development Guidelines

## CRITICAL: SOLID Design Principles

**IMPORTANT!!!** Whenever you write code, it MUST follow the SOLID design principles.
Never write code that violates these principles. If you do, you will be asked to refactor it.

### The SOLID Principles

1. **Single Responsibility Principle (SRP)**
   - Each class should have one, and only one, reason to change
   - Separate file parsing from data extraction from orchestration
   - Example: `PDFParser` only handles PDF reading, not extraction logic

2. **Open/Closed Principle (OCP)**
   - Classes should be open for extension but closed for modification
   - Use abstract base classes and interfaces
   - Example: Add new file formats without modifying existing parsers

3. **Liskov Substitution Principle (LSP)**
   - Derived classes must be substitutable for their base classes
   - All `FileParser` implementations must work interchangeably
   - Example: `PDFParser` and `WordParser` can replace `FileParser` without breaking code

4. **Interface Segregation Principle (ISP)**
   - Clients should not depend on interfaces they don't use
   - Create focused interfaces rather than one large interface
   - Example: Separate `FileParser` from `FieldExtractor` interfaces

5. **Dependency Inversion Principle (DIP)**
   - Depend on abstractions, not concretions
   - High-level modules should not depend on low-level modules
   - Example: `ResumeParserFramework` depends on `FileParser` interface, not `PDFParser` directly

---

## Project Structure

Follow this production-level directory structure:

```text
resume_parser_framework/
├── .github/                          # GitHub Actions workflows
│   └── workflows/
│       ├── ci-feature.yml           # CI for feature branches
│       ├── ci-release.yml           # CI for release branch
│       └── ci-main.yml              # CI/CD for main branch
├── app/                             # Main application code
│   ├── __init__.py
│   ├── core/                        # Core business logic
│   │   ├── __init__.py
│   │   ├── parsers/                 # File parsers (PDF, Word, etc.)
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Abstract FileParser
│   │   │   ├── pdf_parser.py       # PDFParser implementation
│   │   │   └── word_parser.py      # WordParser implementation
│   │   ├── extractors/              # Field extractors
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Abstract FieldExtractor
│   │   │   ├── name_extractor.py
│   │   │   ├── email_extractor.py
│   │   │   └── skills_extractor.py
│   │   ├── models/                  # Data models
│   │   │   ├── __init__.py
│   │   │   └── resume_data.py      # ResumeData data class
│   │   ├── resume_extractor.py      # ResumeExtractor coordinator
│   │   └── framework.py             # ResumeParserFramework orchestrator
│   ├── config/                      # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py             # Application settings
│   │   └── logging_config.py       # Logging configuration
│   ├── prompts/                     # LLM/AI prompts (if using ML/LLM)
│   │   ├── __init__.py
│   │   ├── name_extraction.py
│   │   ├── email_extraction.py
│   │   └── skills_extraction.py
│   ├── utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py           # Input validation
│   │   └── helpers.py              # Helper functions
│   └── exceptions/                  # Custom exceptions
│       ├── __init__.py
│       ├── parser_exceptions.py
│       └── extractor_exceptions.py
├── tests/                           # Test files
│   ├── __init__.py
│   ├── unit/                        # Unit tests
│   │   ├── __init__.py
│   │   ├── test_parsers.py
│   │   ├── test_extractors.py
│   │   └── test_framework.py
│   ├── integration/                 # Integration tests
│   │   ├── __init__.py
│   │   └── test_end_to_end.py
│   ├── fixtures/                    # Test data
│   │   ├── sample_resume.pdf
│   │   └── sample_resume.docx
│   └── conftest.py                  # Pytest configuration
├── examples/                        # Usage examples
│   ├── __init__.py
│   ├── parse_pdf_resume.py
│   └── parse_word_resume.py
├── docs/                            # Documentation
│   ├── architecture.md
│   ├── api_reference.md
│   └── usage_guide.md
├── .env.example                     # Example environment variables
├── .gitignore
├── pyproject.toml                   # Project configuration
├── requirements.txt                 # Python dependencies
├── requirements-dev.txt             # Development dependencies
├── README.md                        # Project README
├── CLAUDE.md                        # This file
└── LICENSE
```

---

## Code Quality Standards

### 1. Linting and Formatting

Use the following tools (configured in `pyproject.toml`):

```toml
[tool.black]
line-length = 100
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 100

[tool.ruff]
select = ["E", "F", "B", "I"]
ignore = ["E501"]
line-length = 100
target-version = "py39"

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py
```

### 2. Type Hints

- **REQUIRED**: Use type hints for all function signatures
- Use `typing` module for complex types
- Example:

  ```python
  from typing import Dict, List, Optional
  from pathlib import Path

  def parse_resume(file_path: Path) -> Dict[str, Any]:
      """Parse resume and return structured data."""
      pass
  ```

### 3. Docstrings

- **REQUIRED**: All classes and public methods must have docstrings
- Use Google-style docstrings
- Example:

  ```python
  def extract_email(text: str) -> Optional[str]:
      """Extract email address from text using regex.

      Args:
          text: Raw text content from resume

      Returns:
          Email address if found, None otherwise

      Raises:
          ValueError: If text is empty or None
      """
      pass
  ```

### 4. Code Comments

- Comment **why**, not **what**
- Only comment complex logic or non-obvious technical decisions
- Keep comments up-to-date with code changes

---

## Testing Requirements

### Testing Dependencies

Required packages (add to `requirements-dev.txt`):

- `pytest` - Testing framework
- `pytest-cov` - Code coverage plugin for pytest
- `pytest-mock` - Mocking/fixtures support
- `coverage` - Coverage reporting

Install with:

```bash
pip install -r requirements-dev.txt
```

### Test Coverage Goals

- **Minimum**: 80% code coverage
- **Target**: 90%+ code coverage
- **Outstanding**: 95%+ with all edge cases

### Test Structure

```python
# tests/unit/test_extractors.py
import pytest
from app.core.extractors.email_extractor import EmailExtractor

class TestEmailExtractor:
    """Test suite for EmailExtractor."""

    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = EmailExtractor()

    def test_extract_valid_email(self):
        """Test extraction of valid email address."""
        text = "Contact: john.doe@example.com"
        result = self.extractor.extract(text)
        assert result == "john.doe@example.com"

    def test_extract_no_email(self):
        """Test extraction when no email present."""
        text = "No email here"
        result = self.extractor.extract(text)
        assert result is None

    def test_extract_multiple_emails(self):
        """Test extraction with multiple emails (should return first)."""
        text = "Contact: john@example.com or jane@example.com"
        result = self.extractor.extract(text)
        assert result == "john@example.com"

    @pytest.mark.parametrize("invalid_text", [
        "",
        None,
        "   ",
    ])
    def test_extract_invalid_input(self, invalid_text):
        """Test extraction with invalid input."""
        with pytest.raises(ValueError):
            self.extractor.extract(invalid_text)
```

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/test_extractors.py -v

# Run with markers
pytest -m "not slow"
```

---

## Git Branching Strategy

### Branch Structure

```text
main (production)
  ↑
  └── release (pre-production)
        ↑
        └── feature/* (development)
```

### Branch Descriptions

1. **`main`** - Production branch
   - Only accepts merges from `release`
   - All code must be tested and reviewed
   - Auto-deploys to production (if CI/CD configured)
   - Protected: No direct commits

2. **`release`** - Pre-production/staging branch
   - Accepts merges from `feature/*` branches
   - Used for final testing before production
   - Auto-deploys to staging environment
   - Protected: Requires PR approval

3. **`feature/*`** - Development branches
   - Branch naming: `feature/descriptive-name`
   - Examples:
     - `feature/pdf-parser`
     - `feature/email-extractor`
     - `feature/llm-skills-extraction`
   - Create from `release` branch
   - Merge back to `release` via Pull Request

## Development Workflow

1. Before making any changes, create and checkout a feature branch named `feature-[brief-description]`
2. Write comprehensive tests for all new functionality
3. Compile code and run all tests before committing
4. Write detailed commit messages explaining the changes and rationale
5. Commit all changes to the feature branch

### Git Workflow Details

1. **Starting new feature:**

   ```bash
   git checkout release
   git pull origin release
   git checkout -b feature/your-feature-name
   ```

2. **Working on feature:**

   ```bash
   git add .
   git commit -m "feat: add PDF parser implementation"
   git push origin feature/your-feature-name
   ```

3. **Merging to release:**
   - Create Pull Request from `feature/*` to `release`
   - Ensure all tests pass
   - Request code review
   - Merge after approval

4. **Releasing to production:**
   - Create Pull Request from `release` to `main`
   - Run full test suite
   - Get final approval
   - Merge to `main`

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```text
feat(parser): add Word document parser implementation

Implements WordParser class that extends FileParser abstract class.
Uses python-docx library to extract text from .docx files.

Closes #123

---

fix(extractor): handle email extraction edge case

Fixed bug where emails with + symbol were not extracted correctly.

---

test(skills): add comprehensive test suite for skills extractor

- Add tests for common skills extraction
- Add tests for edge cases (empty text, special characters)
- Achieve 95% code coverage for skills extractor module
```

---

## CI/CD Pipeline

### GitHub Actions Workflows

**Feature Branch CI** (`.github/workflows/ci-feature.yml`):

```yaml
name: Feature Branch CI

on:
  push:
    branches:
      - 'feature/**'
  pull_request:
    branches:
      - release

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run linters
        run: |
          black --check app tests
          isort --check app tests
          ruff check app tests
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Check coverage
        run: |
          coverage report --fail-under=80
```

**Release Branch CI** (`.github/workflows/ci-release.yml`):

- Same as feature CI + integration tests
- Higher coverage threshold (85%)

**Main Branch CI/CD** (`.github/workflows/ci-main.yml`):

- Full test suite
- Coverage threshold: 90%
- Auto-deploy to production (if configured)

---

## Security Considerations

### File Parsing Security

**CRITICAL**: File parsing can be a security risk. Always validate and sanitize inputs.

1. **File Size Limits**
   - Enforce maximum file size (e.g., 10MB)
   - Prevent DoS attacks from extremely large files
   - Example in settings: `MAX_FILE_SIZE_MB = 10`

2. **File Type Validation**
   - Verify file extensions match content (magic bytes)
   - Only allow whitelisted file types (`.pdf`, `.docx`)
   - Reject executable files or suspicious content

3. **Path Traversal Prevention**
   - Never use user-provided filenames directly
   - Sanitize all file paths
   - Use `pathlib.Path` with validation

4. **Malicious File Protection**
   - Set timeouts for parsing operations
   - Sandbox file parsing if possible
   - Catch and handle parser exceptions gracefully
   - Never execute macros or scripts from documents

5. **Input Sanitization**
   - Validate extracted data before processing
   - Sanitize strings to prevent injection attacks
   - Escape special characters in outputs

6. **API Key Security**
   - Never hardcode API keys in code
   - Use environment variables (`.env` file)
   - Never commit `.env` to version control
   - Rotate API keys regularly

### Example Security Implementation

```python
# app/utils/validators.py
from pathlib import Path
from typing import Optional
import magic  # python-magic library

class FileValidator:
    """Validates uploaded files for security."""

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }

    @classmethod
    def validate_file(cls, file_path: Path) -> Optional[str]:
        """Validate file for security concerns.

        Args:
            file_path: Path to file to validate

        Returns:
            None if valid, error message if invalid
        """
        # Check file size
        if file_path.stat().st_size > cls.MAX_FILE_SIZE:
            return f"File too large. Maximum size: {cls.MAX_FILE_SIZE} bytes"

        # Check MIME type
        mime = magic.from_file(str(file_path), mime=True)
        if mime not in cls.ALLOWED_MIME_TYPES:
            return f"Invalid file type: {mime}"

        return None
```

---

## Quality Gates

All code must pass these quality gates before merging:

### Automated Quality Checks

1. **Linting** (must pass)
   - Black formatting: `black --check app tests`
   - Import sorting: `isort --check app tests`
   - Ruff linting: `ruff check app tests`

2. **Type Checking** (must pass)
   - MyPy static type checking: `mypy app`
   - No type errors allowed

3. **Test Coverage** (minimum thresholds)
   - **Feature branches**: ≥ 80% coverage
   - **Release branch**: ≥ 85% coverage
   - **Main branch**: ≥ 90% coverage

4. **Unit Tests** (must all pass)
   - All existing tests must pass
   - New code must have corresponding tests
   - Edge cases must be covered

5. **Integration Tests** (must pass for release/main)
   - End-to-end parsing tests
   - Multi-format compatibility tests

### Manual Quality Checks

1. **Code Review** (required)
   - At least one approval from team member
   - All comments resolved
   - No requested changes pending

2. **Documentation** (required)
   - All new functions have docstrings
   - README updated if API changes
   - CHANGELOG updated

### Pre-commit Checklist

Run before committing:

```bash
# Format code
black app tests
isort app tests

# Run linters
ruff check app tests

# Type checking
mypy app

# Run tests with coverage
pytest --cov=app --cov-report=term --cov-fail-under=80

# Check for security vulnerabilities
pip-audit
```

---

## Performance Considerations

### Parsing Performance

1. **Timeout Limits**
   - Set maximum parsing time per file (e.g., 30 seconds)
   - Prevent hanging on malformed files
   - Example: `PARSING_TIMEOUT_SECONDS = 30`

2. **File Size Optimization**
   - Stream large files instead of loading entirely into memory
   - Use generators where possible
   - Implement pagination for bulk processing

3. **LLM API Considerations**
   - Implement retry logic with exponential backoff
   - Set reasonable timeout values
   - Cache results when appropriate
   - Monitor API rate limits

4. **Performance Benchmarks**
   - PDF parsing: < 5 seconds for typical resume (1-3 pages)
   - Word parsing: < 3 seconds for typical resume
   - Field extraction: < 2 seconds per field
   - Total end-to-end: < 15 seconds per resume

### Example Performance Implementation

```python
# app/core/parsers/pdf_parser.py
import signal
from contextlib import contextmanager
from pathlib import Path
from app.exceptions.parser_exceptions import ParsingTimeoutError

class PDFParser(FileParser):
    """PDF parser with timeout protection."""

    TIMEOUT_SECONDS = 30

    @contextmanager
    def _timeout(self, seconds: int):
        """Context manager for timeout."""
        def timeout_handler(signum, frame):
            raise ParsingTimeoutError(f"Parsing exceeded {seconds}s timeout")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)

    def parse(self, file_path: Path) -> str:
        """Parse PDF with timeout protection."""
        with self._timeout(self.TIMEOUT_SECONDS):
            # Parsing logic here
            pass
```

### Performance Monitoring

Add timing decorators to track performance:

```python
import time
import functools
from app.config.logging_config import logger

def monitor_performance(func):
    """Decorator to monitor function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time

        logger.info(
            f"Performance: {func.__name__}",
            duration_seconds=duration,
            function=func.__name__
        )

        if duration > 10:  # Warn if takes longer than 10s
            logger.warning(
                f"Slow operation: {func.__name__} took {duration:.2f}s"
            )

        return result
    return wrapper
```

---

## Error Handling and Logging

### Custom Exceptions

Create domain-specific exceptions:

```python
# app/exceptions/parser_exceptions.py
class ParserException(Exception):
    """Base exception for parser errors."""
    pass

class UnsupportedFileFormatError(ParserException):
    """Raised when file format is not supported."""
    pass

class FileParsingError(ParserException):
    """Raised when file cannot be parsed."""
    pass

# app/exceptions/extractor_exceptions.py
class ExtractorException(Exception):
    """Base exception for extractor errors."""
    pass

class FieldExtractionError(ExtractorException):
    """Raised when field extraction fails."""
    pass
```

### Logging Configuration

Use structured logging with custom logger:

```python
# app/config/logging_config.py
import logging
import sys
from typing import Any, Dict

class StructuredLogger:
    """Structured logger with context support."""

    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.context: Dict[str, Any] = {}

    def with_context(self, **kwargs) -> 'StructuredLogger':
        """Add context to logger."""
        self.context.update(kwargs)
        return self

    def info(self, message: str, **kwargs):
        """Log info message with context."""
        self.logger.info(f"{message} | Context: {self.context | kwargs}")

    def error(self, message: str, **kwargs):
        """Log error message with context."""
        self.logger.error(f"{message} | Context: {self.context | kwargs}")

# Usage
logger = StructuredLogger("resume_parser")
logger.with_context(file_path="resume.pdf", user_id="12345").info(
    "Starting resume parsing"
)
```

---

## Prompt Engineering (for LLM/ML Extractors)

When implementing ML or LLM-based extractors, follow these guidelines:

### Prompt Structure

```python
# app/prompts/skills_extraction.py

ROLE_SKILLS_EXPERT = """
You are an expert technical recruiter with 10+ years of experience
identifying technical and professional skills from resumes.
"""

SKILLS_EXTRACTION_INSTRUCTION = """
Analyze the provided resume text and extract all relevant professional skills.

Focus on:
- Technical skills (programming languages, frameworks, tools)
- Soft skills (communication, leadership, teamwork)
- Domain expertise (machine learning, data analysis, etc.)
- Certifications and qualifications

Return ONLY a valid JSON array of strings, no additional text or formatting.

Example output:
["Python", "Machine Learning", "Docker", "Leadership", "Agile"]

Resume text:
{resume_text}

Your response (JSON array only):
"""

def get_skills_extraction_prompt(resume_text: str) -> str:
    """Generate prompt for skills extraction.

    Args:
        resume_text: Raw text extracted from resume

    Returns:
        Formatted prompt for LLM
    """
    return f"{ROLE_SKILLS_EXPERT}\n\n{SKILLS_EXTRACTION_INSTRUCTION.format(resume_text=resume_text)}"
```

### Prompt Best Practices

1. **Define clear roles** - Set expertise context
2. **Provide explicit instructions** - Be specific about output format
3. **Include examples** - Show expected output format
4. **Handle edge cases** - Account for missing or malformed data
5. **Validate output** - Always validate LLM responses
6. **Use templates** - Keep prompts maintainable and versioned

---

## Configuration Management

### Environment Variables

Store sensitive data in environment variables:

```python
# .env.example
# LLM API Configuration
OPENAI_API_KEY=your-api-key-here
GEMINI_API_KEY=your-api-key-here
MODEL_NAME=gpt-4

# Application Settings
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf,docx

# Feature Flags
USE_LLM_EXTRACTOR=true
USE_REGEX_FALLBACK=true
```

```python
# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings."""

    # LLM Configuration
    openai_api_key: str = ""
    gemini_api_key: str = ""
    model_name: str = "gpt-4"

    # Application Settings
    log_level: str = "INFO"
    max_file_size_mb: int = 10
    allowed_file_types: List[str] = ["pdf", "docx"]

    # Feature Flags
    use_llm_extractor: bool = True
    use_regex_fallback: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## Object-Oriented Design Patterns

### Abstract Base Classes

Always use ABC for interfaces:

```python
# app/core/parsers/base.py
from abc import ABC, abstractmethod
from pathlib import Path

class FileParser(ABC):
    """Abstract base class for file parsers."""

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """Parse file and extract raw text.

        Args:
            file_path: Path to file to parse

        Returns:
            Raw text content from file

        Raises:
            FileParsingError: If file cannot be parsed
        """
        pass

    @abstractmethod
    def supports_format(self, file_path: Path) -> bool:
        """Check if parser supports file format.

        Args:
            file_path: Path to file to check

        Returns:
            True if format is supported, False otherwise
        """
        pass
```

### Strategy Pattern

Use for configurable extraction strategies:

```python
# app/core/extractors/base.py
from abc import ABC, abstractmethod
from typing import Any, Optional

class FieldExtractor(ABC):
    """Abstract base class for field extractors."""

    @abstractmethod
    def extract(self, text: str) -> Optional[Any]:
        """Extract field value from text.

        Args:
            text: Raw text to extract from

        Returns:
            Extracted value or None if not found

        Raises:
            FieldExtractionError: If extraction fails
        """
        pass
```

### Factory Pattern

Use for creating parsers/extractors:

```python
# app/core/parsers/factory.py
from pathlib import Path
from typing import Dict, Type
from app.core.parsers.base import FileParser
from app.core.parsers.pdf_parser import PDFParser
from app.core.parsers.word_parser import WordParser
from app.exceptions.parser_exceptions import UnsupportedFileFormatError

class ParserFactory:
    """Factory for creating file parsers."""

    _parsers: Dict[str, Type[FileParser]] = {
        ".pdf": PDFParser,
        ".docx": WordParser,
    }

    @classmethod
    def get_parser(cls, file_path: Path) -> FileParser:
        """Get appropriate parser for file.

        Args:
            file_path: Path to file

        Returns:
            Parser instance for file format

        Raises:
            UnsupportedFileFormatError: If no parser for format
        """
        suffix = file_path.suffix.lower()
        parser_class = cls._parsers.get(suffix)

        if parser_class is None:
            raise UnsupportedFileFormatError(
                f"No parser available for {suffix} files"
            )

        return parser_class()

    @classmethod
    def register_parser(cls, extension: str, parser_class: Type[FileParser]):
        """Register new parser for file extension.

        Args:
            extension: File extension (e.g., '.txt')
            parser_class: Parser class to register
        """
        cls._parsers[extension.lower()] = parser_class
```

### Coordinator Pattern

Use for orchestrating multiple components:

```python
# app/core/resume_extractor.py
from typing import Dict
from app.core.extractors.base import FieldExtractor
from app.core.models.resume_data import ResumeData

class ResumeExtractor:
    """Coordinates field extraction from resume text."""

    def __init__(self, extractors: Dict[str, FieldExtractor]):
        """Initialize with field extractors.

        Args:
            extractors: Dictionary mapping field names to extractors
        """
        self.extractors = extractors

    def extract(self, text: str) -> ResumeData:
        """Extract all fields from resume text.

        Args:
            text: Raw text from resume

        Returns:
            ResumeData instance with extracted fields
        """
        extracted_fields = {}

        for field_name, extractor in self.extractors.items():
            try:
                value = extractor.extract(text)
                extracted_fields[field_name] = value
            except Exception as e:
                logger.error(f"Failed to extract {field_name}: {e}")
                extracted_fields[field_name] = None

        return ResumeData(**extracted_fields)
```

---

## Documentation Standards

### README.md Structure

```markdown
# Resume Parser Framework

Brief description of the project.

## Features

- PDF and Word document parsing
- Field-specific extraction strategies (regex, NER, LLM)
- Pluggable architecture for easy extension
- Comprehensive test coverage

## Installation

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Quick Start

\`\`\`python
from pathlib import Path
from app.core.framework import ResumeParserFramework
# ... example usage
\`\`\`

## Configuration

Details about environment variables and configuration.

## Development

How to set up development environment, run tests, etc.

## Architecture

Link to architecture documentation.

## Contributing

Branching strategy and contribution guidelines.

## License

MIT License
```

### Code Documentation

- **Every module** must have a module-level docstring
- **Every class** must document its purpose and usage
- **Every public method** must have complete docstring
- Include examples in docstrings where helpful

---

## Evaluation Criteria Alignment

Based on the provided rubric, ensure:

### Code Behaviour (Outstanding = 4)

- ✅ Code runs/compiles without errors
- ✅ Considers all edge cases
- ✅ Thorough error handling with informative logs
- ✅ Comprehensive input validation

### Solution Design (Outstanding = 4)

- ✅ All logical concepts properly implemented
- ✅ Full separation of concerns (parsers, extractors, models, framework)
- ✅ Extensibility and scalability considered
- ✅ Code organized by best practices (see Project Structure)

### Code Testing (Outstanding = 4)

- ✅ Unit tests exist and pass
- ✅ Tests cover all happy paths and edge cases
- ✅ 90%+ code coverage target
- ✅ Integration tests included

### Readability (Outstanding = 4)

- ✅ Self-explanatory code with clear naming
- ✅ Comments clarifying complex logic
- ✅ Comprehensive README with setup instructions
- ✅ Code follows Python best practices (PEP 8, type hints)

---

## Quick Reference Checklist

Before submitting code, verify:

### Code Quality

- [ ] Follows SOLID principles
- [ ] Passes all linters (black, isort, ruff)
- [ ] Type hints on all functions
- [ ] Docstrings on all classes and public methods
- [ ] MyPy type checking passes
- [ ] No code smells or anti-patterns

### Testing

- [ ] Test coverage ≥ 80% (feature), ≥ 85% (release), ≥ 90% (main)
- [ ] All unit tests passing
- [ ] Integration tests passing (for release/main)
- [ ] Edge cases covered

### Security

- [ ] No hardcoded secrets (use .env)
- [ ] File size limits enforced
- [ ] File type validation implemented
- [ ] Input sanitization applied
- [ ] Timeouts configured for parsing operations
- [ ] Security vulnerabilities checked (`pip-audit`)

### Performance

- [ ] Parsing operations complete within benchmarks
- [ ] No memory leaks
- [ ] Performance monitoring in place
- [ ] Appropriate caching implemented (if applicable)

### Documentation

- [ ] README.md is up-to-date
- [ ] All new APIs documented
- [ ] CHANGELOG updated
- [ ] Usage examples provided

### Git Workflow

- [ ] Feature branch from `release`
- [ ] Commit messages follow convention
- [ ] Pull request created with description
- [ ] Code review completed and approved
- [ ] CI pipeline passes
- [ ] All comments resolved

---

## Resources

- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [PEP 8 Style Guide](https://pep8.org/)

---

**Last Updated**: 2025-11-26
**Maintained By**: Development Team
