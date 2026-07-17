import os
from io import BytesIO

from markitdown import MarkItDown, StreamInfo
from pydantic import Field

SUPPORTED_FILE_TYPES = ("pdf", "docx")


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Filesystem path to a PDF or DOCX document to convert"
    ),
) -> str:
    """Read a document from disk and convert its contents to markdown.

    Opens the file at the given path, reads its raw bytes, infers the file
    type from the path's extension, and converts the document to
    markdown-formatted text. Only PDF and DOCX documents are supported.

    When to use:
    - When you have a PDF or DOCX file on the local filesystem and need its
      contents as markdown text.
    - When a tool or model should read a document by path rather than by
      receiving its raw bytes.

    When not to use:
    - For unsupported formats (anything other than PDF or DOCX).
    - When you already hold the document's bytes in memory; use
      binary_document_to_markdown instead.

    Examples:
    >>> document_path_to_markdown("docs/report.pdf")
    '# Report\\n\\n...'
    >>> document_path_to_markdown("docs/notes.docx")
    '# Notes\\n\\n...'
    """
    _, extension = os.path.splitext(file_path)
    file_type = extension.lstrip(".").lower()

    if file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(
            f"Unsupported file type '{file_type}'. "
            f"Supported types are: {', '.join(SUPPORTED_FILE_TYPES)}."
        )

    with open(file_path, "rb") as f:
        binary_data = f.read()

    return binary_document_to_markdown(binary_data, file_type)
