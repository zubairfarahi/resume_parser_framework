# Code Review Command

Carefully perform a comprehensive code review of $ARGUMENTS.

## Review Standards

Reference the following for code quality standards:

1. **Project Guidelines**: [`CLAUDE.md`](../../CLAUDE.md)
   - SOLID principles compliance
   - Code quality standards
   - Testing requirements
   - Security considerations

2. **External Best Practices**:
   - [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
   - [Full-Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)

3. **Example Code** (match design/style/conventions):
   - `app/core/parsers/base.py` - Abstract base classes and interfaces
   - `app/core/extractors/base.py` - Field extractor patterns
   - `app/utils/validators.py` - Input validation and security
   - `app/config/logging_config.py` - Logging and error handling
   - `tests/unit/test_extractors.py` - Test structure and patterns

## Review Process

### 1. Understanding Phase
- Read relevant sections from `CLAUDE.md`
- Review example code files to understand patterns
- Understand the context of $ARGUMENTS in the codebase

### 2. SOLID Principles Check
Verify adherence to SOLID principles:
- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Derived classes are substitutable
- **I**nterface Segregation: Focused, minimal interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

### 3. Comprehensive Analysis
Analyze $ARGUMENTS covering:

#### Code Structure & Organization
- File organization matches project structure
- Imports are clean and organized (isort compliant)
- Separation of concerns is clear
- Module/class/function responsibilities are well-defined

#### Design Patterns
- Appropriate use of Abstract Base Classes (ABC)
- Factory pattern for object creation (if applicable)
- Strategy pattern for configurable behaviors
- Proper use of dependency injection

#### Code Quality
- **Type Hints**: All functions have proper type annotations
- **Docstrings**: Google-style docstrings on all public APIs
- **Naming**: Clear, self-explanatory names (PEP 8 compliant)
- **Complexity**: Functions are focused and not overly complex
- **DRY**: No unnecessary code duplication

#### Security
- No hardcoded secrets or API keys
- Input validation and sanitization
- File size and type validation (for file parsers)
- Path traversal prevention
- Timeout protection for long-running operations
- SQL injection prevention (if database operations)
- XSS prevention (if web-facing)

#### Performance
- No obvious performance bottlenecks
- Efficient algorithms and data structures
- Proper use of generators for large datasets
- Appropriate caching strategies
- Timeout handling for external APIs
- Memory-efficient file handling

#### Error Handling
- Custom exceptions for domain-specific errors
- Proper exception hierarchy
- Graceful error handling with informative messages
- Logging of errors with appropriate context
- No bare `except` clauses

#### Testing
- Unit tests exist for new code
- Test coverage meets thresholds (e80%)
- Edge cases are covered
- Fixtures are used appropriately
- Mocks are used for external dependencies
- Tests follow AAA pattern (Arrange, Act, Assert)

## Output Requirements

Save review as `ai-code-reviews/{filename}.review.md` for each file reviewed.

### Review Template

```markdown
# Code Review: {filename}

**Reviewer**: AI Assistant
**Date**: {current_date}
**Overall Rating**: Excellent | Good | Needs Improvement | Poor
**Refactoring Effort**: Low | Medium | High

## Summary

Brief overview of the code's purpose and quality.

## SOLID Principles Compliance

- [ ] **Single Responsibility**: Description
- [ ] **Open/Closed**: Description
- [ ] **Liskov Substitution**: Description
- [ ] **Interface Segregation**: Description
- [ ] **Dependency Inversion**: Description

## Detailed Analysis

### Strengths
- List of what the code does well
- Specific examples with line references

### Issues Found

#### Critical Issues (Must Fix)
- **Line {X}**: Description and suggestion
- **Line {Y}**: Description and suggestion

#### Major Issues (Should Fix)
- **Line {X}**: Description and suggestion
- **Line {Y}**: Description and suggestion

#### Minor Issues (Nice to Have)
- **Line {X}**: Description and suggestion
- **Line {Y}**: Description and suggestion

### Code Quality Metrics

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Type Hints | X% | 100% | /L |
| Docstrings | X% | 100% | /L |
| Test Coverage | X% | e80% | /L |
| Linting | Pass/Fail | Pass | /L |
| Complexity | X | <10 | /L |

### Security Analysis
- Input validation: /L/N/A
- Output sanitization: /L/N/A
- Authentication/Authorization: /L/N/A
- Secrets management: /L/N/A
- File upload safety: /L/N/A

### Performance Analysis
- Algorithm efficiency: /L/N/A
- Memory usage: /L/N/A
- Timeout handling: /L/N/A
- Caching strategy: /L/N/A

## Recommendations

### Immediate Actions
1. Specific action item with priority
2. Specific action item with priority

### Future Improvements
1. Suggested enhancement
2. Suggested enhancement

## Refactoring Suggestions

```python
# Before (problematic code)
def bad_example():
    pass

# After (improved code)
def good_example():
    """Improved implementation."""
    pass
```

## Conclusion

Final assessment and next steps.
```

## Review Checklist

Use this checklist for every review:

### Code Quality
- [ ] Follows SOLID principles
- [ ] Passes Black formatting (`black --check`)
- [ ] Passes isort (`isort --check`)
- [ ] Passes Ruff linting (`ruff check`)
- [ ] Passes MyPy type checking (`mypy`)
- [ ] Follows PEP 8 naming conventions
- [ ] No code smells or anti-patterns

### Documentation
- [ ] All functions have type hints
- [ ] All public APIs have Google-style docstrings
- [ ] Complex logic has explanatory comments
- [ ] Module-level docstring present
- [ ] Example usage provided (if applicable)

### Design
- [ ] Appropriate use of ABC for interfaces
- [ ] Proper separation of concerns
- [ ] Dependencies are injected, not hardcoded
- [ ] Configuration is externalized
- [ ] Extensibility considered

### Security
- [ ] No hardcoded secrets or API keys
- [ ] Input validation implemented
- [ ] Output sanitization applied
- [ ] File operations are safe
- [ ] SQL queries are parameterized (if applicable)
- [ ] Timeout protection in place

### Performance
- [ ] No obvious performance bottlenecks
- [ ] Appropriate data structures used
- [ ] Generators used for large datasets
- [ ] Caching implemented where beneficial
- [ ] Database queries optimized (if applicable)

### Error Handling
- [ ] Custom exceptions defined
- [ ] Errors logged with context
- [ ] Graceful degradation implemented
- [ ] No bare `except` clauses
- [ ] Error messages are informative

### Testing
- [ ] Unit tests exist
- [ ] Test coverage e 80%
- [ ] Edge cases covered
- [ ] Fixtures used appropriately
- [ ] Mocks used for external dependencies
- [ ] Integration tests exist (if applicable)

## Example Review Commands

```bash
# Review a specific file
/code-review app/core/parsers/pdf_parser.py

# Review multiple files
/code-review app/core/extractors/*.py

# Review entire module
/code-review app/core/
```

## Quality Standards Reference

Align code with these standards from `CLAUDE.md`:

### Code Behaviour (Outstanding = 4)
-  Code runs/compiles without errors
-  Considers all edge cases
-  Thorough error handling with informative logs
-  Comprehensive input validation

### Solution Design (Outstanding = 4)
-  All logical concepts properly implemented
-  Full separation of concerns
-  Extensibility and scalability considered
-  Code organized by best practices

### Code Testing (Outstanding = 4)
-  Unit tests exist and pass
-  Tests cover all happy paths and edge cases
-  90%+ code coverage target
-  Integration tests included

### Readability (Outstanding = 4)
-  Self-explanatory code with clear naming
-  Comments clarifying complex logic
-  Comprehensive documentation
-  Code follows Python best practices

## Notes

- Focus on constructive feedback with specific examples
- Provide code snippets for suggested improvements
- Prioritize issues: Critical > Major > Minor
- Consider the broader architecture and design patterns
- Reference specific lines for all issues
- Be thorough but pragmatic in recommendations
