# Resume Parser Framework

A production-ready, AI-powered Python framework for parsing resumes from PDF and Word documents. Built with SOLID principles, OpenAI integration, and designed for extensibility.

## 🚀 Features

- **📄 Multiple File Formats**: Full support for PDF and Word (.docx) documents
- **🤖 AI-Powered Extraction**: OpenAI GPT-4o-mini for intelligent field extraction
- **🧩 Pluggable Architecture**: Easy to add new parsers and extractors
- **🏗️ SOLID Design Principles**: Clean, maintainable, and extensible codebase
- **✅ Type-Safe**: Full type hints and Pydantic v2 validation
- **🔒 Security-First**: File validation, size limits, MIME type checking
- **🧪 Comprehensive Testing**: 80%+ test coverage with pytest
- **📊 Structured Logging**: JSON logging with structlog
- **🐳 Docker Support**: Production-ready containerization
- **⚡ CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **🎯 FastAPI REST API**: Modern, async API for resume parsing

## 📦 What It Extracts

The framework extracts comprehensive information from resumes:

- ✅ **Name** - Full name of the candidate
- ✅ **Email** - Email address with validation
- ✅ **Phone** - Phone number in various formats (using OpenAI)
- ✅ **Skills** - Technical and soft skills (using OpenAI)
- ✅ **Education** - Complete education history (using OpenAI)
- ✅ **Work Experience** - Detailed work history (using OpenAI)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/zubairfarahi/resume_parser_framework.git
cd resume_parser_framework

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Configuration

Create a `.env` file with your OpenAI API key:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Model configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.0
```

### Running the API

```bash
# Start the FastAPI server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- 🌐 API: http://localhost:8000
- 📚 Interactive Docs: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc

### Using the API

#### Upload and Parse a Resume

```bash
# Using curl
curl -X POST "http://localhost:8000/parse-resume" \
     -F "file=@/path/to/resume.pdf"

# Example response
{
  "success": true,
  "data": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1 (555) 123-4567",
    "skills": ["Python", "FastAPI", "Machine Learning", "Docker"],
    "education": [
      {
        "institution": "University of California",
        "degree": "Bachelor of Science",
        "field_of_study": "Computer Science",
        "graduation_date": "2020"
      }
    ],
    "experience": [
      {
        "company": "Tech Corp",
        "title": "Software Engineer",
        "start_date": "Jan 2020",
        "end_date": "Present",
        "description": "Developed web applications"
      }
    ]
  },
  "filename": "resume.pdf"
}
```

### Python SDK Usage

```python
from app.core.extractors import (
    EducationExtractor,
    EmailExtractor,
    ExperienceExtractor,
    NameExtractor,
    PhoneExtractor,
    SkillsExtractor,
)
from app.core.framework import ResumeParserFramework

# Initialize extractors
extractors = {
    "name": NameExtractor(),
    "email": EmailExtractor(),
    "phone": PhoneExtractor(),
    "skills": SkillsExtractor(),
    "education": EducationExtractor(),
    "experience": ExperienceExtractor(),
}

# Create framework and parse
framework = ResumeParserFramework(extractors)
resume_data = framework.parse_resume("path/to/resume.pdf")

# Access extracted data
print(f"Name: {resume_data.name}")
print(f"Email: {resume_data.email}")
print(f"Phone: {resume_data.phone}")
print(f"Skills: {', '.join(resume_data.skills)}")
print(f"Education: {len(resume_data.education)} entries")
print(f"Experience: {len(resume_data.experience)} entries")
```

## 🏗️ Architecture

### Project Structure

```
resume_parser_framework/
├── app/
│   ├── core/
│   │   ├── parsers/              # File parsers (PDF, Word)
│   │   │   ├── base.py           # Abstract FileParser
│   │   │   ├── pdf_parser.py     # PDF implementation ✅
│   │   │   └── word_parser.py    # Word implementation ✅
│   │   ├── extractors/           # Field extractors
│   │   │   ├── base.py           # Abstract FieldExtractor
│   │   │   ├── name_extractor.py         # Name extraction ✅
│   │   │   ├── email_extractor.py        # Email extraction ✅
│   │   │   ├── phone_extractor.py        # Phone extraction ✅ (OpenAI)
│   │   │   ├── skills_extractor.py       # Skills extraction ✅ (OpenAI)
│   │   │   ├── education_extractor.py    # Education extraction ✅ (OpenAI)
│   │   │   └── experience_extractor.py   # Experience extraction ✅ (OpenAI)
│   │   ├── models/
│   │   │   └── resume_data.py    # Pydantic data models ✅
│   │   ├── framework.py          # Main orchestrator ✅
│   │   └── resume_extractor.py   # Field extraction coordinator ✅
│   ├── config/
│   │   ├── settings.py           # Pydantic Settings
│   │   └── logging_config.py     # Structlog configuration
│   ├── prompts/                  # LLM prompts for extractors
│   │   └── resume_extraction_prompts.py
│   ├── utils/
│   │   └── validators.py         # File validation
│   └── exceptions/
│       └── exceptions.py         # Custom exceptions
├── tests/
│   ├── unit/                     # Unit tests (54 tests)
│   ├── integration/              # Integration tests
│   └── conftest.py              # Pytest fixtures
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD ✅
├── Dockerfile                   # Production Docker image ✅
├── main.py                      # FastAPI application ✅
├── Makefile                     # Development commands ✅
└── README.md                    # This file
```

### SOLID Principles

This framework strictly adheres to SOLID principles:

1. **Single Responsibility Principle (SRP)**
   - Each class has one reason to change
   - Parsers only parse files, extractors only extract fields

2. **Open/Closed Principle (OCP)**
   - Abstract base classes allow extension without modification
   - Add new file formats by implementing `FileParser`
   - Add new fields by implementing `FieldExtractor`

3. **Liskov Substitution Principle (LSP)**
   - All parser implementations are substitutable for `FileParser`
   - All extractor implementations are substitutable for `FieldExtractor`

4. **Interface Segregation Principle (ISP)**
   - Minimal interfaces with only necessary methods
   - Separate interfaces for parsing and extraction

5. **Dependency Inversion Principle (DIP)**
   - Framework depends on abstractions (ABC), not concretions
   - Configuration injected through environment variables

## 🧪 Development

### Makefile Commands

```bash
# Show all available commands
make help

# Installation
make install           # Install production dependencies
make install-dev       # Install dev dependencies

# Testing
make test              # Run all tests
make test-unit         # Run unit tests only
make test-cov          # Run tests with coverage

# Code Quality
make format            # Format code with Black and isort
make lint              # Lint with Ruff and MyPy
make clean             # Clean temporary files

# Running
make run               # Start FastAPI server

# Docker
make docker-build      # Build Docker image
make docker-run        # Run Docker container
```

### Running Tests

```bash
# Using Make (recommended)
make test
make test-cov

# Direct pytest
pytest tests/unit -v
pytest --cov=app --cov-report=html
```

### Code Quality Standards

The project enforces strict code quality:

```bash
# Format code
make format

# Run all linters
make lint

# Individual tools
black app tests examples
isort app tests examples
ruff check app tests examples
mypy app --ignore-missing-imports
```

## 🐳 Docker

### Production Deployment

```bash
# Build image
docker build -t resume-parser:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  --name resume-parser \
  resume-parser:latest

# Check health
curl http://localhost:8000/health
```

### Docker Compose

```bash
# Using Make
make docker-build
make docker-run

# Or directly
docker-compose up -d
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions pipeline:

- ✅ **Linting**: Black, isort, Ruff, MyPy
- ✅ **Testing**: pytest with coverage reporting
- ✅ **Building**: Docker image build and push
- ✅ **Deployment**: Automatic deployment on main branch

### Pipeline Stages

1. **Lint** - Code quality checks
2. **Test** - Unit and integration tests (80% coverage required)
3. **Build** - Docker image creation (only on main/release branches)

## 🔒 Security

### File Upload Security

- ✅ **Size Limits**: 10MB maximum (configurable)
- ✅ **MIME Type Validation**: Only PDF and DOCX allowed
- ✅ **Path Traversal Prevention**: Filename sanitization
- ✅ **Timeout Protection**: 30-second parsing timeout
- ✅ **Input Validation**: Pydantic validation on all data

### Best Practices

- ✅ No hardcoded secrets (environment variables only)
- ✅ Input validation on all user-provided data
- ✅ Secure file handling with proper cleanup
- ✅ Structured logging for security audit trails

## ⚡ Performance

### Benchmarks

- PDF parsing: ~5 seconds
- Word parsing: ~3 seconds
- AI extraction (per field): ~2-3 seconds
- Total end-to-end: ~15-20 seconds per resume

### Optimization Features

- ✅ Timeout limits prevent runaway operations
- ✅ Efficient file handling with context managers
- ✅ Performance monitoring via structured logs
- ✅ Async API with FastAPI for concurrent requests

## 📊 Technology Stack

- **Framework**: FastAPI
- **Parsing**: pypdf, python-docx
- **AI/ML**: OpenAI GPT-4o-mini
- **Validation**: Pydantic v2
- **Logging**: Structlog
- **Testing**: pytest, pytest-cov
- **Code Quality**: Black, isort, Ruff, MyPy
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## 🗺️ Roadmap

### ✅ Phase 1: Core Framework (Completed)
- [x] Project structure and configuration
- [x] Base abstract classes (FileParser, FieldExtractor)
- [x] Pydantic data models
- [x] File validation and security
- [x] Test infrastructure

### ✅ Phase 2: Parsers (Completed)
- [x] PDF parser implementation
- [x] Word parser implementation
- [x] Parser factory pattern
- [x] Parser tests

### ✅ Phase 3: Extractors (Completed)
- [x] Name extractor (regex-based)
- [x] Email extractor (regex-based)
- [x] Phone extractor (OpenAI-powered)
- [x] Skills extractor (OpenAI-powered)
- [x] Education extractor (OpenAI-powered)
- [x] Experience extractor (OpenAI-powered)

### ✅ Phase 4: Integration (Completed)
- [x] Framework orchestrator
- [x] FastAPI REST API
- [x] End-to-end tests
- [x] Performance optimization

### ✅ Phase 5: DevOps (Completed)
- [x] Docker containerization
- [x] GitHub Actions CI/CD
- [x] Makefile automation
- [x] Comprehensive documentation

### 🚧 Future Enhancements
- [ ] Support for more file formats (HTML, RTF)
- [ ] Batch processing API
- [ ] Web UI for resume upload
- [ ] Database storage for parsed resumes
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Custom field extractors

## 📝 Git Workflow

This project follows a clean Git workflow:

```
main (production)
  ↑
  └── release (pre-production)
        ↑
        └── feature/* (development)
```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add new feature
fix: bug fix
docs: documentation changes
test: add or update tests
refactor: code refactoring
perf: performance improvements
chore: maintenance tasks
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Write tests for new functionality
4. Ensure all tests pass: `make test`
5. Ensure code quality: `make lint`
6. Commit your changes: `git commit -m 'feat: add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 👤 Author

**Zubair Farahi**

- GitHub: [@zubairfarahi](https://github.com/zubairfarahi)

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI-powered by [OpenAI](https://openai.com/)
- Inspired by modern software engineering best practices

## 📞 Support

For questions or issues:
- 📧 Open an issue on [GitHub](https://github.com/zubairfarahi/resume_parser_framework/issues)
- 📚 Check the [API documentation](http://localhost:8000/docs)

---

**⭐ If you find this project useful, please consider giving it a star!**
