# Node/TypeScript MCP Server Implementation Guide

## Overview

This guide covers creating MCP servers using Node.js/TypeScript and the MCP TypeScript SDK. TypeScript servers are ideal for Node ecosystem integrations and when type safety is critical.

## Prerequisites

- Node.js 18 or higher
- TypeScript 5.0+
- MCP TypeScript SDK: `npm install @modelcontextprotocol/sdk`
- Zod for input validation

## Project Structure

```
my-mcp-server/
├── src/
│   ├── index.ts       # Main server file
│   ├── tools.ts       # Tool implementations
│   ├── api.ts         # API client
│   └── types.ts       # Type definitions
├── dist/              # Compiled JavaScript (generated)
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

## Project Setup

### package.json

```json
{
  "name": "mcp-service-name",
  "version": "1.0.0",
  "description": "MCP server for [Service Name]",
  "type": "module",
  "bin": {
    "mcp-service-name": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.22.0",
    "node-fetch": "^3.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Basic Server Template

### src/index.ts

```typescript
#!/usr/bin/env node

/**
 * MCP server for [Service Name]
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// Constants
const CHARACTER_LIMIT = 25000;
const API_BASE_URL = "https://api.example.com";

// Environment variables
const API_KEY = process.env.SERVICE_API_KEY;
if (!API_KEY) {
  throw new Error("SERVICE_API_KEY environment variable required");
}

// Types
interface ApiResponse<T> {
  data?: T;
  error?: string;
}

interface SearchResult {
  id: string;
  title: string;
  description: string;
  url: string;
  status: string;
}

// Input Schemas
const SearchItemsSchema = z.object({
  query: z.string().describe("Search query. Examples: 'python tutorials', 'api docs'"),
  limit: z.number().int().min(1).max(100).default(50)
    .describe("Number of results to return (1-100)"),
  format: z.enum(["json", "markdown"]).default("markdown")
    .describe("Response format: 'json' or 'markdown'"),
}).strict();

const CreateItemSchema = z.object({
  title: z.string().min(1).max(200)
    .describe("Item title (1-200 characters)"),
  description: z.string().optional().default("")
    .describe("Item description (optional)"),
  tags: z.array(z.string()).max(10).default([])
    .describe("List of tags (max 10)"),
}).strict();

// API Client
class ApiClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(baseUrl: string, apiKey: string) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}/${endpoint}`, {
        ...options,
        headers: {
          "Authorization": `Bearer ${this.apiKey}`,
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      if (!response.ok) {
        if (response.status === 429) {
          const retryAfter = response.headers.get("Retry-After") || "60";
          return { error: `Rate limit exceeded. Retry in ${retryAfter}s` };
        } else if (response.status === 404) {
          return { error: "Resource not found. Verify ID and try again." };
        } else if (response.status === 401) {
          return { error: "Authentication failed. Check API_KEY." };
        } else {
          return { error: `API error: ${response.status}` };
        }
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return { error: `Request failed: ${error}` };
    }
  }

  async get<T>(endpoint: string, params?: Record<string, string>): Promise<ApiResponse<T>> {
    const url = params
      ? `${endpoint}?${new URLSearchParams(params)}`
      : endpoint;
    return this.request<T>(url);
  }

  async post<T>(endpoint: string, body: unknown): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }
}

// Initialize API client
const apiClient = new ApiClient(API_BASE_URL, API_KEY);

// Response Formatters
function formatMarkdown(items: SearchResult[]): string {
  const lines: string[] = [];

  for (const item of items) {
    lines.push(`## ${item.title}`);
    lines.push(`- **ID:** ${item.id}`);
    lines.push(`- **Status:** ${item.status}`);
    lines.push(`- **URL:** ${item.url}`);
    lines.push("");
  }

  return lines.join("\n");
}

function formatJson(data: unknown): string {
  return JSON.stringify(data, null, 2);
}

function truncateResponse(response: string, limit: number = CHARACTER_LIMIT): string {
  if (response.length <= limit) {
    return response;
  }

  return (
    response.substring(0, limit) +
    "\n\n[Response truncated. Use filters to narrow results.]"
  );
}

// Tool Implementations
async function searchItems(args: z.infer<typeof SearchItemsSchema>): Promise<string> {
  const { query, limit, format } = args;

  // Make API request
  const result = await apiClient.get<{ items: SearchResult[] }>("search", {
    q: query,
    limit: limit.toString(),
  });

  // Handle errors
  if (result.error) {
    return result.error;
  }

  const items = result.data?.items || [];

  // Format response
  let response: string;
  if (format === "json") {
    response = formatJson(items);
  } else {
    response = formatMarkdown(items);
  }

  // Truncate if needed
  return truncateResponse(response);
}

async function createItem(args: z.infer<typeof CreateItemSchema>): Promise<string> {
  const { title, description, tags } = args;

  // Validate
  if (!title.trim()) {
    return "Error: Title cannot be empty";
  }

  if (tags.length > 10) {
    return "Error: Maximum 10 tags allowed";
  }

  // Make API request
  const result = await apiClient.post<{ id: string; url: string }>("items", {
    title,
    description,
    tags,
  });

  // Handle errors
  if (result.error) {
    return result.error;
  }

  // Success response
  const { id, url } = result.data!;
  return `✓ Item created successfully\n\nID: ${id}\nURL: ${url}`;
}

// Initialize MCP Server
const server = new Server(
  {
    name: "service-name",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Register Tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_items",
        description:
          "Search for items using the service API.\n\n" +
          "Searches the service for items matching the query. Supports full-text " +
          "search across titles, descriptions, and tags.\n\n" +
          "Examples:\n" +
          "  - search_items({query: 'python tutorials', limit: 10})\n" +
          "  - search_items({query: 'api docs', format: 'json'})\n\n" +
          "Errors:\n" +
          "  - Invalid query: Returns error with suggestions\n" +
          "  - Rate limit: Returns retry time\n" +
          "  - Network error: Returns clear error message",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query. Examples: 'python tutorials', 'api docs'",
            },
            limit: {
              type: "number",
              description: "Number of results to return (1-100)",
              minimum: 1,
              maximum: 100,
              default: 50,
            },
            format: {
              type: "string",
              enum: ["json", "markdown"],
              description: "Response format: 'json' or 'markdown'",
              default: "markdown",
            },
          },
          required: ["query"],
        },
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true,
      },
      {
        name: "create_item",
        description:
          "Create a new item in the service.\n\n" +
          "Creates a new item with the specified properties. Returns the created " +
          "item's ID and URL.\n\n" +
          "Examples:\n" +
          "  - create_item({title: 'My Item', description: 'Description here'})\n" +
          "  - create_item({title: 'Tagged Item', tags: ['important', 'review']})\n\n" +
          "Errors:\n" +
          "  - Invalid title: Returns error with requirements\n" +
          "  - Too many tags: Returns error with limit\n" +
          "  - API error: Returns clear error message",
        inputSchema: {
          type: "object",
          properties: {
            title: {
              type: "string",
              description: "Item title (1-200 characters)",
              minLength: 1,
              maxLength: 200,
            },
            description: {
              type: "string",
              description: "Item description (optional)",
              default: "",
            },
            tags: {
              type: "array",
              items: { type: "string" },
              description: "List of tags (max 10)",
              maxItems: 10,
              default: [],
            },
          },
          required: ["title"],
        },
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: true,
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args } = request.params;

    switch (name) {
      case "search_items": {
        const validated = SearchItemsSchema.parse(args);
        const result = await searchItems(validated);
        return {
          content: [{ type: "text", text: result }],
        };
      }

      case "create_item": {
        const validated = CreateItemSchema.parse(args);
        const result = await createItem(validated);
        return {
          content: [{ type: "text", text: result }],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new Error(
        `Invalid arguments: ${error.errors.map((e) => `${e.path.join(".")}: ${e.message}`).join(", ")}`
      );
    }
    throw error;
  }
});

// Start Server
async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
```

## Zod Schema Best Practices

### Comprehensive Validation

```typescript
import { z } from "zod";

// String with constraints
const TitleSchema = z.string()
  .min(1, "Title cannot be empty")
  .max(200, "Title too long (max 200 chars)")
  .describe("Item title");

// Number with range
const LimitSchema = z.number()
  .int("Must be an integer")
  .min(1, "Minimum 1")
  .max(100, "Maximum 100")
  .default(50)
  .describe("Number of results");

// Enum
const FormatSchema = z.enum(["json", "markdown"])
  .default("markdown")
  .describe("Response format");

// URL validation
const UrlSchema = z.string()
  .url("Must be valid URL")
  .describe("HTTP/HTTPS URL");

// Array with constraints
const TagsSchema = z.array(z.string())
  .max(10, "Maximum 10 tags")
  .default([])
  .describe("List of tags");

// Optional field
const DescriptionSchema = z.string()
  .optional()
  .default("")
  .describe("Optional description");

// Date validation
const DateSchema = z.string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "Must be YYYY-MM-DD format")
  .describe("Date in YYYY-MM-DD format");

// Strict object (no extra fields)
const StrictSchema = z.object({
  field: z.string(),
}).strict();
```

## Type Safety

### Explicit Types

```typescript
// Return types
async function fetchData(endpoint: string): Promise<ApiResponse<SearchResult[]>> {
  // ...
}

// Function parameters
function formatItems(items: SearchResult[]): string {
  // ...
}

// Avoid 'any' - use proper types
interface Config {
  apiKey: string;
  baseUrl: string;
  timeout?: number;
}

function configure(config: Config): void {
  // ...
}
```

### Type Guards

```typescript
function isError(response: ApiResponse<unknown>): response is { error: string } {
  return "error" in response && typeof response.error === "string";
}

// Usage
const result = await apiClient.get("endpoint");
if (isError(result)) {
  return result.error;
}
// TypeScript knows result.data exists here
```

## Error Handling

### Comprehensive Pattern

```typescript
async function safeApiCall<T>(endpoint: string): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
      headers: { "Authorization": `Bearer ${API_KEY}` },
    });

    if (!response.ok) {
      switch (response.status) {
        case 401:
          return { error: "Authentication failed. Check API_KEY." };
        case 403:
          return { error: "Access forbidden. Verify permissions." };
        case 404:
          return { error: "Resource not found. Verify ID and try again." };
        case 429: {
          const retry = response.headers.get("Retry-After") || "60";
          return { error: `Rate limit exceeded. Retry in ${retry}s` };
        }
        default:
          return { error: `API error: ${response.status}` };
      }
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    if (error instanceof TypeError && error.message.includes("fetch")) {
      return { error: "Network error. Check connection and try again." };
    }
    return { error: `Unexpected error: ${error}` };
  }
}
```

## Quality Checklist

Use this checklist before finalizing your TypeScript MCP server:

### TypeScript Configuration
- [ ] `strict: true` in tsconfig.json
- [ ] No `any` types used
- [ ] All functions have explicit return types
- [ ] `npm run build` completes without errors

### Code Quality
- [ ] Zod schemas use `.strict()` for objects
- [ ] No code duplication between tools
- [ ] Shared logic extracted into functions/classes
- [ ] All async operations properly awaited

### Documentation
- [ ] Every tool has comprehensive description
- [ ] Tool descriptions include examples and error cases
- [ ] Schema fields have clear descriptions
- [ ] README explains setup and usage

### Error Handling
- [ ] All fetch calls wrapped in try/catch
- [ ] Error messages are clear and actionable
- [ ] Rate limiting handled gracefully
- [ ] Zod validation errors properly formatted

### Input Validation
- [ ] Zod schemas for all tool inputs
- [ ] String fields have min/max length
- [ ] Numeric fields have min/max values
- [ ] Arrays have maxItems constraints
- [ ] Enums use z.enum()

### Response Formatting
- [ ] Support both JSON and Markdown formats
- [ ] Responses truncated if > 25,000 characters
- [ ] Pagination implemented for list operations
- [ ] Human-readable identifiers used

### Tool Annotations
- [ ] readOnlyHint set correctly
- [ ] destructiveHint set correctly
- [ ] idempotentHint set correctly
- [ ] openWorldHint set correctly

### Testing
- [ ] `npm run build` succeeds
- [ ] dist/index.js created
- [ ] Server runs without errors (in tmux or with timeout)
- [ ] Environment variables handled correctly

## Common Patterns

### Pagination

```typescript
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

function paginateResults<T>(
  allItems: T[],
  limit: number = 50,
  offset: number = 0
): PaginatedResponse<T> {
  const total = allItems.length;
  const items = allItems.slice(offset, offset + limit);

  return {
    items,
    total,
    limit,
    offset,
    has_more: offset + limit < total,
  };
}
```

### Concurrent Requests

```typescript
async function fetchMultiple(ids: string[]): Promise<SearchResult[]> {
  const promises = ids.map((id) => apiClient.get<SearchResult>(`items/${id}`));
  const results = await Promise.allSettled(promises);

  return results
    .filter((r): r is PromiseFulfilledResult<ApiResponse<SearchResult>> =>
      r.status === "fulfilled" && !r.value.error
    )
    .map((r) => r.value.data!);
}
```

## Build and Run

```bash
# Install dependencies
npm install

# Build
npm run build

# Run server (for testing in tmux)
npm start

# Or run with timeout
timeout 5s npm start
```
