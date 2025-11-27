"""File parsers for different document formats."""

from app.core.parsers.base import FileParser
from app.core.parsers.pdf_parser import PDFParser
from app.core.parsers.word_parser import WordParser

__all__ = ["FileParser", "PDFParser", "WordParser"]
