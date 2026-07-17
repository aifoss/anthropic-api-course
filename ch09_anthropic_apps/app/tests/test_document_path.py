import os
from pathlib import Path

import pytest

from tools.document import document_path_to_markdown


class TestDocumentPathToMarkdown:
    # Reuse the shared fixtures used by the binary-conversion tests.
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_document_path_to_markdown_with_pdf(self) -> None:
        """Convert a PDF referenced by path to markdown."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        # Typical markdown formatting; exact content depends on the fixture.
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_with_docx(self) -> None:
        """Convert a DOCX referenced by path to markdown."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_nonexistent_file(self) -> None:
        """A path that does not exist should raise FileNotFoundError."""
        missing = os.path.join(self.FIXTURES_DIR, "does_not_exist.pdf")

        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(missing)

    def test_document_path_to_markdown_invalid_file_type(self, tmp_path: Path) -> None:
        """An unsupported extension should be rejected with a ValueError.

        markitdown will happily convert some non-PDF/DOCX inputs, so the tool
        itself must validate the extension against the supported set rather
        than relying on the converter to fail.
        """
        bad_file = tmp_path / "sample.txt"
        bad_file.write_text("just some plain text, not a pdf or docx")

        with pytest.raises(ValueError):
            document_path_to_markdown(str(bad_file))

    def test_document_path_to_markdown_empty_document(self, tmp_path: Path) -> None:
        """An empty file with a supported extension cannot be converted."""
        empty_file = tmp_path / "empty.pdf"
        empty_file.write_bytes(b"")

        with pytest.raises(Exception):
            document_path_to_markdown(str(empty_file))
