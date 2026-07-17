# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`app` is a Python package (Ch. 9 of the Anthropic API course) that implements document-related tools — format conversion and processing — and exposes them through an **MCP (Model Context Protocol) server** so AI assistants can call them. This is a *starter* project: tool logic lives in `tools/`, but the MCP server entrypoint (`main.py`) is built out during the chapter and does not exist yet.

## Commands

```bash
# Setup: create venv, activate, install editable
uv venv && source .venv/bin/activate && uv pip install -e .

uv run main.py            # start the MCP server (once main.py exists)
uv run pytest             # run all tests
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf  # single test
```

## Environment note

The venv runs **Python 3.14** intentionally. `uv.lock` was bumped past its course-default pins (`onnxruntime`, `pydantic`/`pydantic-core`, `typing-extensions`, `typing-inspection`) because the originals had no cp314 wheels and fell back to source builds requiring `rustc ≥1.75`. Keep this in mind before regenerating the lock — a plain re-resolve to older versions will break `uv run` on 3.14. Harmless `SyntaxWarning: 'return' in a 'finally' block` messages from `pluggy`/`anyio` under 3.14 are expected.

## Architecture

- **`tools/`** — each module holds plain, framework-agnostic Python functions (e.g. `document.py`, `math.py`). Functions have no MCP dependency, which is what makes them directly unit-testable in `tests/`.
- **Document conversion** (`tools/document.py`) — `binary_document_to_markdown` wraps `markitdown.MarkItDown`, feeding it a `BytesIO` stream plus a `StreamInfo(extension=...)`. Callers pass raw bytes + a file-type extension string ("pdf", "docx"); the tool returns markdown text. Supported formats depend on the `markitdown[docx,pdf]` extras in `pyproject.toml`.
- **MCP wiring** — the server (in `main.py`) registers each function as a tool with `mcp.tool()(my_function)`. Tools stay decoupled from the server: define/test the function in `tools/`, then register it. `mcp[cli]` is pinned to `1.8.0`.
- **`tests/`** — pytest, imports tools directly (`from tools.document import ...`). Real fixtures live in `tests/fixtures/` (`mcp_docs.pdf`, `mcp_docs.docx`); tests exercise actual conversion rather than mocking.

## Conventions

- Always give function arguments (and return values) appropriate type annotations. For MCP tool functions, pair the type with a pydantic `Field(description=...)`.

## Defining MCP tools

Tools are defined as functions and registered with `mcp.tool()(my_function)`. The tool's **docstring and parameter descriptions are what the model sees**, so treat them as the interface, not incidental comments. Follow the `tools/math.py` `add` function as the reference template.

Every tool description should:
- Begin with a one-line summary.
- Provide a detailed explanation of functionality.
- Explain **when to use (and when not to use)** the tool.
- Include usage examples with expected input/output.

Describe each parameter with pydantic's `Field`:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of what this does.

    When to use:
    - ...

    Examples:
    >>> my_tool("x", 1)
    ...
    """
    # implementation
```
