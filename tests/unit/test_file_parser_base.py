"""Tests for the FileParser base class."""

from pathlib import Path

from app.core.parsers.base import FileParser


class DummyParser(FileParser):
    """Concrete parser used to exercise shared validation logic."""

    def parse(self, file_path: Path) -> str:
        return file_path.read_text()

    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix == ".txt"


def test_validate_file_missing(tmp_path) -> None:
    """Missing files should report appropriate error."""
    parser = DummyParser()
    missing = tmp_path / "missing.txt"
    assert parser.validate_file(missing) == f"File not found: {missing}"


def test_validate_file_not_regular_file(tmp_path) -> None:
    """Directories should not pass validation."""
    parser = DummyParser()
    assert parser.validate_file(tmp_path) == f"Path is not a file: {tmp_path}"


def test_validate_file_unsupported_format(tmp_path) -> None:
    """Unsupported suffixes should return an error message."""
    parser = DummyParser()
    target = tmp_path / "resume.pdf"
    target.write_text("data")
    assert parser.validate_file(target) == "Unsupported file format: .pdf"


def test_validate_file_success(tmp_path) -> None:
    """Supported files should pass validation."""
    parser = DummyParser()
    target = tmp_path / "resume.txt"
    target.write_text("data")
    assert parser.validate_file(target) is None
