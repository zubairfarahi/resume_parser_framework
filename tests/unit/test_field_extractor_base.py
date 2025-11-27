"""Tests for the FieldExtractor base class."""


from app.core.extractors.base import FieldExtractor


class DummyExtractor(FieldExtractor):
    """Concrete extractor used for base class testing."""

    def extract(self, text: str) -> str:
        return text

    def get_field_name(self) -> str:
        return "dummy"


def test_validate_input_empty_string() -> None:
    """Empty input should return validation error."""
    extractor = DummyExtractor()
    assert extractor.validate_input("") == "Input text is empty or contains only whitespace"


def test_validate_input_too_short() -> None:
    """Very short input should trigger validation error."""
    extractor = DummyExtractor()
    assert extractor.validate_input("short") == (
        "Input text is too short to extract meaningful information"
    )


def test_validate_input_valid_text() -> None:
    """Valid input should pass validation."""
    extractor = DummyExtractor()
    assert extractor.validate_input("This is a valid resume text snippet.") is None
