# Resume Parser Framework

A production-ready, pluggable Python framework for parsing resumes from PDF and Word documents with configurable field extractors. Built with SOLID principles and designed for extensibility.

## Features

- **Multiple File Formats**: PDF and Word (.docx) support
- **Pluggable Architecture**: Easy to add new parsers and extractors
- **SOLID Design**: Clean, maintainable, and extensible codebase
- **Type-Safe**: Full type hints and Pydantic validation
- **Security-First**: File validation, size limits, MIME type checking
- **Comprehensive Testing**: 80%+ test coverage with pytest
- **Structured Logging**: JSON logging with structlog
- **Production-Ready**: Configuration management, error handling, performance monitoring

## Quick Start

### Installation

#### Option 1: Using Make (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-parser-framework.git
cd resume-parser-framework

# Complete setup (installs dependencies, creates directories, copies .env)
make setup

# Or install dependencies only
make install-dev
```

#### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-parser-framework.git
cd resume-parser-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (for testing and linting)
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env
```

#### Option 3: Using Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-parser-framework.git
cd resume-parser-framework

# Start with Docker Compose (development)
docker-compose -f docker/docker-compose.yml up -d

# Or use Make
make docker-up

# View logs
make docker-logs
```

### Basic Usage

```python
from pathlib import Path
from app.core.models.resume_data import ResumeData

# Example will be added as parsers are implemented
# For now, you can work with the ResumeData model directly

resume = ResumeData(
    name="John Doe",
    email="john.doe@example.com",
    phone="+1-555-123-4567",
    skills=["Python", "FastAPI", "Docker"],
)

print(resume.to_json())
```

### Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then update the values in `.env`:

```bash
# Application Settings
RESUME_PARSER_DEBUG=false
RESUME_PARSER_ENVIRONMENT=production

# File Processing
RESUME_PARSER_MAX_FILE_SIZE=10485760  # 10MB
RESUME_PARSER_PARSING_TIMEOUT=30

# Logging
RESUME_PARSER_LOG_LEVEL=INFO
RESUME_PARSER_LOG_FORMAT=json

# API Settings (if using FastAPI)
RESUME_PARSER_API_HOST=0.0.0.0
RESUME_PARSER_API_PORT=8000
```

See [.env.example](.env.example) for all available configuration options.

## Architecture

### Project Structure

```
resume_parser_framework/
├── app/
│   ├── core/
│   │   ├── parsers/          # File parsers (PDF, Word)
│   │   │   ├── base.py       # Abstract FileParser
│   │   │   ├── pdf_parser.py # PDF implementation (TODO)
│   │   │   └── word_parser.py # Word implementation (TODO)
│   │   ├── extractors/       # Field extractors
│   │   │   ├── base.py       # Abstract FieldExtractor
│   │   │   └── ...           # Concrete extractors (TODO)
│   │   ├── models/
│   │   │   └── resume_data.py # Pydantic data models
│   │   └── framework.py      # Main orchestrator (TODO)
│   ├── config/
│   │   ├── settings.py       # Pydantic Settings
│   │   └── logging_config.py # Structlog configuration
│   ├── utils/
│   │   └── validators.py     # File validation
│   └── exceptions/
│       └── exceptions.py     # Custom exceptions
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── docs/                    # Documentation
├── examples/                # Usage examples
├── pyproject.toml          # Project configuration
└── README.md
```

### SOLID Principles

This framework strictly adheres to SOLID principles:

1. **Single Responsibility Principle (SRP)**
   - Each class has one reason to change
   - Parsers only parse, extractors only extract

2. **Open/Closed Principle (OCP)**
   - Abstract base classes allow extension without modification
   - Add new file formats by implementing `FileParser`
   - Add new fields by implementing `FieldExtractor`

3. **Liskov Substitution Principle (LSP)**
   - All parser implementations are substitutable for `FileParser`
   - All extractor implementations are substitutable for `FieldExtractor`

4. **Interface Segregation Principle (ISP)**
   - Minimal interfaces with only necessary methods
   - Clients don't depend on methods they don't use

5. **Dependency Inversion Principle (DIP)**
   - Depend on abstractions (ABC) not concretions
   - Configuration injected through settings

## Development

### Makefile Commands

The project includes a comprehensive Makefile with common development tasks:

```bash
# Show all available commands
make help

# Setup development environment
make setup

# Run tests
make test                  # All tests
make test-unit            # Unit tests only
make test-integration     # Integration tests only
make coverage             # Tests with coverage report

# Code quality
make format               # Format with Black and isort
make lint                 # Lint with Ruff
make type-check          # Type check with MyPy
make quality             # Run all quality checks
make ci                  # Simulate CI pipeline locally

# Cleaning
make clean               # Remove generated files and caches

# Security
make security-check      # Check for vulnerabilities
```

### Running Tests

```bash
# Using Make (recommended)
make test
make coverage
make test-unit

# Direct pytest commands
pytest
pytest --cov=app --cov-report=html
pytest tests/unit/test_models.py -v
pytest -k "test_validate" -v
```

### Code Quality

```bash
# Using Make (recommended)
make quality              # Run all quality checks
make format              # Format code
make lint                # Run linter
make type-check          # Type checking

# Direct commands
black .
isort .
ruff check .
mypy app/
```

### Git Workflow

This project follows a three-tier branching strategy:

```
main (production)
  ↑
  └── release (pre-production)
        ↑
        └── feature/* (development)
```

**Creating a new feature:**

```bash
# Checkout from release
git checkout release
git pull origin release

# Create feature branch
git checkout -b feature/my-new-feature

# Make changes, commit frequently
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-new-feature

# Create pull request to release branch
```

**Commit Message Convention:**

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

## Docker Usage

### Development with Docker

```bash
# Build development image
make docker-build-dev

# Start containers
make docker-up

# View logs
make docker-logs

# Access container shell
make docker-shell

# Run tests in container
make docker-test

# Stop containers
make docker-down

# Clean up Docker resources
make docker-clean
```

### Production with Docker

```bash
# Build production image
make docker-build

# Run with production compose file
docker-compose -f docker/docker-compose.prod.yml up -d

# View logs
docker-compose -f docker/docker-compose.prod.yml logs -f
```

### Docker Architecture

- **Dockerfile**: Multi-stage production build for minimal image size
- **Dockerfile.dev**: Development build with hot reload and dev tools
- **docker-compose.yml**: Development environment with volume mounts
- **docker-compose.prod.yml**: Production environment with resource limits

## Testing Requirements

- **Feature branches**: ≥ 80% coverage
- **Release branch**: ≥ 85% coverage
- **Main branch**: ≥ 90% coverage

## Security

### File Upload Security

- **Size Limits**: 10MB maximum (configurable)
- **MIME Type Validation**: Only PDF and DOCX allowed
- **Path Traversal Prevention**: Filename sanitization
- **Timeout Protection**: 30-second parsing timeout

### Best Practices

- No hardcoded secrets (use environment variables)
- Input validation on all user-provided data
- Secure file handling with proper error handling
- Structured logging for security audit trails

## Performance

### Benchmarks (Target)

- PDF parsing: < 5 seconds
- Word parsing: < 3 seconds
- Field extraction: < 2 seconds per field
- End-to-end: < 15 seconds

### Optimization

- Timeout limits prevent runaway operations
- Lazy loading of heavy dependencies
- Efficient file handling with context managers
- Performance monitoring via structured logs

## Documentation

- [Developer Documentation](docs/dev/) - Technical implementation details
- [User Documentation](docs/user/) - Usage guides and examples
- [CLAUDE.md](CLAUDE.md) - Comprehensive development guidelines
- [API Documentation](docs/dev/api-reference.md) - API reference (TODO)

## Contributing

1. Read [CLAUDE.md](CLAUDE.md) for development guidelines
2. Create a feature branch from `release`
3. Write tests for new functionality
4. Ensure all quality checks pass
5. Submit pull request to `release` branch

## License

[Add your license here]

## Roadmap

### Phase 1: Core Framework (Current)
- [x] Project structure
- [x] Base abstract classes
- [x] Data models
- [x] Configuration and logging
- [x] File validation
- [x] Test infrastructure

### Phase 2: Parsers (Next)
- [ ] PDF parser implementation
- [ ] Word parser implementation
- [ ] Parser factory
- [ ] Parser tests

### Phase 3: Extractors
- [ ] Name extractor
- [ ] Email extractor
- [ ] Phone extractor
- [ ] Skills extractor
- [ ] Experience extractor
- [ ] Education extractor

### Phase 4: Integration
- [ ] Framework orchestrator
- [ ] End-to-end tests
- [ ] Example applications
- [ ] Performance optimization

### Phase 5: API (Optional)
- [ ] FastAPI REST endpoints
- [ ] API documentation
- [ ] Rate limiting
- [ ] Authentication

## Contact

For questions or feedback, please open an issue on GitHub.
