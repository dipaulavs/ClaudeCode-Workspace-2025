# KB Generator - Troubleshooting

## Error 1: "Oversized sections detected"

**Symptom:** Phase 1 or Phase 2 creates SUBDIVISION_REQUEST.md

**Cause:** One or more sections exceed 5000 token limit

**Solution:**
1. Read SUBDIVISION_REQUEST.md for details
2. Extract oversized section content
3. Identify logical subdivisions
4. Update structure.json with `children` array
5. Re-run phase with updated structure

**Example:**
```json
{
  "id": "section_002",
  "title": "API Reference",
  "start_line": 200,
  "end_line": 800,
  "children": [
    {
      "id": "section_002_001",
      "title": "Authentication",
      "start_line": 200,
      "end_line": 350
    },
    {
      "id": "section_002_002",
      "title": "Endpoints",
      "start_line": 350,
      "end_line": 800
    }
  ]
}
```

## Error 2: "Line range overlap detected"

**Symptom:** Validation fails with overlap error

**Cause:** Two sections have overlapping line numbers

**Solution:**
1. Review structure.json for overlapping ranges
2. Adjust `end_line` and `start_line` to eliminate overlap
3. Ensure no gaps between sequential sections

**Example fix:**
```json
// Before (overlap)
{"start_line": 100, "end_line": 250}
{"start_line": 200, "end_line": 350}

// After (no overlap)
{"start_line": 100, "end_line": 200}
{"start_line": 200, "end_line": 350}
```

## Error 3: "Cannot extract PDF content"

**Symptom:** Script fails to read PDF

**Cause:** PDF is image-based or encrypted

**Solution:**
1. Convert PDF to text using OCR if needed
2. Use Markdown or TXT format instead
3. Check PDF permissions (no encryption)

## Error 4: "structure.json invalid"

**Symptom:** Phase 2 fails to parse structure

**Cause:** Malformed JSON syntax

**Solution:**
1. Validate JSON using `python3 -m json.tool structure.json`
2. Fix syntax errors (missing commas, brackets, quotes)
3. Ensure all required fields present (`id`, `title`, `start_line`, `end_line`)
