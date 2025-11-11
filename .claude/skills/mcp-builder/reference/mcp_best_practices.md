# MCP Best Practices

## Server and Tool Naming Conventions

### Server Naming
- Use lowercase with hyphens (kebab-case)
- Be descriptive and specific: `github-api` not `gh`
- Avoid redundant "mcp" prefix: `slack` not `mcp-slack`

### Tool Naming
- Use snake_case for tool names
- Start with verb: `create_issue`, `get_user`, `list_repos`
- Group related tools with consistent prefixes
- Follow natural task subdivisions, not just API structure

## Response Format Guidelines

### JSON vs Markdown

**Use JSON when:**
- Data needs to be machine-readable
- Agent may need to extract specific fields programmatically
- Response contains structured data (arrays, nested objects)

**Use Markdown when:**
- Content is primarily for human reading
- Response includes formatted text (code blocks, lists, tables)
- Visual formatting adds clarity

**Best Practice:** Support both formats with a format parameter:
```python
format: Literal["json", "markdown"] = "markdown"
```

### Response Design Principles

**Optimize for Limited Context:**
- Return high-signal information, not exhaustive data dumps
- Provide "concise" vs "detailed" response options
- Default to human-readable identifiers (names over IDs)
- Consider agent's context budget as scarce resource

**Make Responses Actionable:**
- Include relevant next steps or related operations
- Suggest filters or parameters to narrow results
- Guide agents toward successful workflows

## Pagination Best Practices

### When to Paginate
- Any operation that could return large result sets
- List/search operations
- Historical data queries

### Pagination Parameters
```python
limit: int = 50  # Results per page (default 50, max 100)
offset: int = 0  # Starting position
```

### Pagination Response Format
Always include metadata to guide agents:
```python
{
    "items": [...],
    "total": 450,
    "limit": 50,
    "offset": 0,
    "has_more": true
}
```

## Character Limits and Truncation

### Why Character Limits Matter
- Agents have limited context windows
- Large responses waste tokens on low-value data
- Truncated responses can still be highly useful

### Standard Limits
- **Default limit:** 25,000 characters per response
- **Large responses:** Implement automatic truncation with clear indication
- **Very large datasets:** Require pagination

### Truncation Strategy
```python
CHARACTER_LIMIT = 25000

if len(response) > CHARACTER_LIMIT:
    response = response[:CHARACTER_LIMIT] + "\n\n[Response truncated. Use filters to narrow results.]"
```

## Tool Development Guidelines

### Build for Workflows, Not Just API Endpoints

**DON'T:** Simply wrap individual API endpoints
```python
@mcp.tool()
def check_availability(date: str): ...

@mcp.tool()
def create_event(date: str, title: str): ...
```

**DO:** Consolidate into workflow-oriented tools
```python
@mcp.tool()
def schedule_event(date: str, title: str, check_conflicts: bool = True):
    """Schedule event, optionally checking availability first"""
    if check_conflicts:
        # Check availability
        ...
    # Create event
    ...
```

### Design Actionable Error Messages

**Bad error message:**
```
"Invalid date format"
```

**Good error message:**
```
"Invalid date format. Expected YYYY-MM-DD (e.g., '2024-03-15'). Received: '03/15/2024'"
```

**Great error message:**
```
"Invalid date format. Expected YYYY-MM-DD (e.g., '2024-03-15'). Received: '03/15/2024'.
Try using format='flexible' to auto-parse common date formats."
```

### Input Validation

**Always validate inputs with clear constraints:**
```python
from pydantic import BaseModel, Field

class CreateIssueInput(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Issue title")
    body: str = Field(description="Issue description")
    labels: list[str] = Field(default_factory=list, max_length=10)
```

### Tool Annotations

Use MCP tool hints to help agents understand tool behavior:

```python
@mcp.tool(
    readOnlyHint=True,      # Tool only reads data
    destructiveHint=False,  # Tool doesn't delete/modify critical data
    idempotentHint=True,    # Repeated calls have same effect
    openWorldHint=True      # Interacts with external systems
)
```

## Security and Error Handling

### Authentication
- Store credentials securely (environment variables)
- Support multiple auth methods when applicable
- Provide clear auth error messages

### Rate Limiting
- Implement exponential backoff
- Respect API rate limits
- Return clear rate limit errors

### Error Handling Pattern
```python
try:
    response = await api_call()
    return response
except RateLimitError as e:
    return f"Rate limit exceeded. Try again in {e.retry_after} seconds."
except AuthError:
    return "Authentication failed. Check your API credentials."
except NotFoundError:
    return "Resource not found. Verify the ID and try again."
except Exception as e:
    return f"Unexpected error: {str(e)}"
```

## Documentation Standards

### Tool Docstrings

Every tool must have comprehensive documentation:

```python
@mcp.tool()
async def search_issues(
    query: str = Field(description="Search query using GitHub search syntax"),
    state: Literal["open", "closed", "all"] = Field(default="open"),
    limit: int = Field(default=50, ge=1, le=100)
) -> str:
    """
    Search for issues across repositories.

    Searches GitHub issues using the query syntax. Supports filters like
    'is:open', 'author:username', 'label:bug', etc.

    Examples:
        - "is:open label:bug" - Open bugs
        - "is:closed author:octocat" - Closed issues by octocat
        - "created:>2024-01-01" - Issues created after Jan 1, 2024

    Returns:
        Markdown-formatted list of matching issues with title, state,
        author, and URL. Limited to specified number of results.

    Errors:
        - Invalid query syntax: Returns error with syntax guide
        - Rate limit: Returns retry time
    """
```

### Parameter Descriptions

Be specific and include examples:

```python
date: str = Field(
    description="Event date in YYYY-MM-DD format (e.g., '2024-03-15')"
)

tags: list[str] = Field(
    default_factory=list,
    description="Tags to filter by. Examples: ['bug', 'urgent'], ['feature']"
)
```

## Testing Best Practices

### Manual Testing
- Test with realistic queries
- Verify error messages are helpful
- Check response formatting
- Confirm pagination works correctly

### Integration Testing
- Test against real API when possible
- Mock external calls for unit tests
- Test authentication flows
- Verify rate limiting behavior

## Performance Optimization

### Minimize API Calls
- Batch requests when possible
- Cache frequently accessed data
- Use ETags for conditional requests

### Async Operations
- Use `async/await` for all I/O
- Run independent operations concurrently
- Stream large responses when possible

### Response Optimization
- Only return necessary fields
- Implement field selection parameters
- Compress large text responses
