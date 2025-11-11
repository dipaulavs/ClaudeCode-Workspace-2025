# Python MCP Server Implementation Guide

## Overview

This guide covers creating MCP servers using Python and the MCP Python SDK. Python servers are ideal for data processing, API integrations, and when you need Python's extensive library ecosystem.

## Prerequisites

- Python 3.10 or higher
- MCP Python SDK: `pip install mcp`
- Pydantic v2 for input validation

## Project Structure

### Simple Server (Single File)
```
my-mcp-server/
├── server.py          # Main server file
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

### Complex Server (Multi-Module)
```
my-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py      # Main server
│   ├── tools.py       # Tool implementations
│   ├── api.py         # API client
│   └── models.py      # Pydantic models
├── requirements.txt
└── README.md
```

## Basic Server Template

```python
#!/usr/bin/env python3
"""MCP server for [Service Name]."""

import asyncio
import os
from typing import Literal

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field, HttpUrl

# Constants
CHARACTER_LIMIT = 25000
API_BASE_URL = "https://api.example.com"

# Initialize MCP server
mcp = Server("service-name")

# API client setup
API_KEY = os.getenv("SERVICE_API_KEY")
if not API_KEY:
    raise ValueError("SERVICE_API_KEY environment variable required")


# Input Models
class SearchInput(BaseModel):
    """Input for search_items tool."""

    model_config = {"extra": "forbid"}

    query: str = Field(
        description="Search query. Examples: 'python tutorials', 'api docs'"
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Number of results to return (1-100)"
    )
    format: Literal["json", "markdown"] = Field(
        default="markdown",
        description="Response format: 'json' or 'markdown'"
    )


# Helper Functions
async def make_api_request(endpoint: str, params: dict = None) -> dict:
    """Make API request with error handling."""
    import httpx

    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE_URL}/{endpoint}",
                headers=headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After", "60")
                return {"error": f"Rate limit exceeded. Retry in {retry_after}s"}
            elif e.response.status_code == 404:
                return {"error": "Resource not found. Verify ID and try again."}
            else:
                return {"error": f"API error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}


def format_response_markdown(data: list[dict]) -> str:
    """Format data as Markdown."""
    lines = []
    for item in data:
        lines.append(f"## {item['title']}")
        lines.append(f"- **ID:** {item['id']}")
        lines.append(f"- **Status:** {item['status']}")
        lines.append(f"- **URL:** {item['url']}")
        lines.append("")
    return "\n".join(lines)


def format_response_json(data: list[dict]) -> str:
    """Format data as JSON."""
    import json
    return json.dumps(data, indent=2)


def truncate_response(response: str, limit: int = CHARACTER_LIMIT) -> str:
    """Truncate response if too long."""
    if len(response) <= limit:
        return response

    return (
        response[:limit] +
        "\n\n[Response truncated. Use filters to narrow results.]"
    )


# Tools
@mcp.tool(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=True
)
async def search_items(
    query: str = Field(description="Search query"),
    limit: int = Field(default=50, ge=1, le=100),
    format: Literal["json", "markdown"] = "markdown"
) -> str:
    """
    Search for items using the service API.

    Searches the service for items matching the query. Supports full-text
    search across titles, descriptions, and tags.

    Args:
        query: Search query string
        limit: Number of results (1-100, default 50)
        format: Response format ('json' or 'markdown')

    Returns:
        Formatted search results in specified format.

    Examples:
        - search_items("python tutorials", limit=10)
        - search_items("api docs", format="json")

    Errors:
        - Invalid query: Returns error with suggestions
        - Rate limit: Returns retry time
        - Network error: Returns clear error message
    """
    # Validate inputs (automatic via Pydantic)
    inputs = SearchInput(query=query, limit=limit, format=format)

    # Make API request
    result = await make_api_request("search", {
        "q": inputs.query,
        "limit": inputs.limit
    })

    # Handle errors
    if "error" in result:
        return result["error"]

    # Format response
    items = result.get("items", [])

    if inputs.format == "json":
        response = format_response_json(items)
    else:
        response = format_response_markdown(items)

    # Truncate if needed
    return truncate_response(response)


@mcp.tool(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=True
)
async def create_item(
    title: str = Field(min_length=1, max_length=200),
    description: str = Field(default=""),
    tags: list[str] = Field(default_factory=list, max_length=10)
) -> str:
    """
    Create a new item in the service.

    Creates a new item with the specified properties. Returns the created
    item's ID and URL.

    Args:
        title: Item title (1-200 characters)
        description: Item description (optional)
        tags: List of tags (max 10)

    Returns:
        Success message with item ID and URL, or error message.

    Examples:
        - create_item("My Item", "Description here")
        - create_item("Tagged Item", tags=["important", "review"])

    Errors:
        - Invalid title: Returns error with requirements
        - Too many tags: Returns error with limit
        - API error: Returns clear error message
    """
    # Validate
    if not title.strip():
        return "Error: Title cannot be empty"

    if len(tags) > 10:
        return "Error: Maximum 10 tags allowed"

    # Make API request
    result = await make_api_request("items", {
        "title": title,
        "description": description,
        "tags": tags
    })

    # Handle errors
    if "error" in result:
        return result["error"]

    # Success response
    item_id = result.get("id")
    item_url = result.get("url")

    return f"✓ Item created successfully\n\nID: {item_id}\nURL: {item_url}"


# Server Entry Point
async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

## Pydantic Models Best Practices

### Model Configuration

Always use Pydantic v2 with strict configuration:

```python
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    """Input model for a tool."""

    model_config = {"extra": "forbid"}  # Reject unexpected fields

    field_name: str = Field(
        description="Clear description with examples",
        min_length=1,
        max_length=100
    )
```

### Common Validation Patterns

```python
# String with length constraints
name: str = Field(min_length=1, max_length=200)

# Integer with range
limit: int = Field(ge=1, le=100, default=50)

# Enum with literal types
status: Literal["open", "closed", "all"] = "open"

# URL validation
url: HttpUrl = Field(description="Valid HTTP/HTTPS URL")

# List with max length
tags: list[str] = Field(default_factory=list, max_length=10)

# Optional field
description: str | None = Field(default=None)

# Field with regex pattern
code: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
```

## Type Hints

Use comprehensive type hints throughout:

```python
from typing import Literal, Any
from collections.abc import Sequence

# Function signatures
async def fetch_data(
    endpoint: str,
    params: dict[str, Any] | None = None
) -> dict[str, Any]:
    ...

# Return types
def format_items(items: Sequence[dict]) -> str:
    ...

# Async functions
async def process_batch(ids: list[str]) -> list[dict[str, Any]]:
    ...
```

## Error Handling

### Comprehensive Error Handling Pattern

```python
async def safe_api_call(endpoint: str) -> dict | str:
    """Make API call with comprehensive error handling."""
    import httpx

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/{endpoint}")
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException:
        return "Request timed out. The service may be slow. Try again."

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "Authentication failed. Check API_KEY environment variable."
        elif e.response.status_code == 403:
            return "Access forbidden. Verify your permissions."
        elif e.response.status_code == 404:
            return "Resource not found. Verify the ID and try again."
        elif e.response.status_code == 429:
            retry = e.response.headers.get("Retry-After", "60")
            return f"Rate limit exceeded. Retry in {retry} seconds."
        else:
            return f"API error {e.response.status_code}: {e.response.text}"

    except httpx.NetworkError:
        return "Network error. Check your connection and try again."

    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

## Async/Await Patterns

### Concurrent Operations

```python
import asyncio

async def fetch_multiple_items(ids: list[str]) -> list[dict]:
    """Fetch multiple items concurrently."""
    tasks = [make_api_request(f"items/{id}") for id in ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out errors
    return [r for r in results if isinstance(r, dict) and "error" not in r]
```

### Timeout Handling

```python
async def fetch_with_timeout(endpoint: str, timeout: float = 30.0) -> dict:
    """Fetch with timeout."""
    try:
        return await asyncio.wait_for(
            make_api_request(endpoint),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return {"error": f"Request timed out after {timeout}s"}
```

## Quality Checklist

Use this checklist before finalizing your Python MCP server:

### Code Quality
- [ ] All functions have type hints
- [ ] Pydantic models use `model_config = {"extra": "forbid"}`
- [ ] No code duplication between tools
- [ ] Shared logic extracted into helper functions
- [ ] All I/O operations use async/await

### Documentation
- [ ] Every tool has comprehensive docstring
- [ ] Docstrings include Args, Returns, Examples, Errors
- [ ] Field descriptions include examples
- [ ] README explains setup and usage

### Error Handling
- [ ] All external calls wrapped in try/except
- [ ] Error messages are clear and actionable
- [ ] Rate limiting handled gracefully
- [ ] Authentication errors provide guidance

### Input Validation
- [ ] Pydantic models for all tool inputs
- [ ] String fields have min/max length
- [ ] Numeric fields have ranges (ge/le)
- [ ] Lists have max_length constraints
- [ ] Enums use Literal types

### Response Formatting
- [ ] Support both JSON and Markdown formats
- [ ] Responses truncated if > 25,000 characters
- [ ] Pagination implemented for list operations
- [ ] Human-readable identifiers (names over IDs)

### Tool Annotations
- [ ] readOnlyHint set correctly
- [ ] destructiveHint set correctly
- [ ] idempotentHint set correctly
- [ ] openWorldHint set correctly

### Testing
- [ ] Server runs without errors: `python server.py` (in tmux or with timeout)
- [ ] Imports are correct
- [ ] API_KEY environment variable handled
- [ ] Tested with realistic queries

## Common Patterns

### Pagination Helper

```python
def paginate_results(
    all_items: list[dict],
    limit: int = 50,
    offset: int = 0
) -> dict:
    """Paginate results."""
    total = len(all_items)
    items = all_items[offset:offset + limit]

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + limit < total
    }
```

### Response Formatter

```python
def format_response(
    data: Any,
    format: Literal["json", "markdown"]
) -> str:
    """Format response based on requested format."""
    if format == "json":
        import json
        return json.dumps(data, indent=2)
    else:
        # Convert to markdown
        return convert_to_markdown(data)
```

## Dependencies

Typical `requirements.txt`:

```
mcp>=1.0.0
pydantic>=2.0.0
httpx>=0.25.0
python-dotenv>=1.0.0  # For .env file support
```
