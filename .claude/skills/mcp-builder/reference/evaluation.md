# MCP Server Evaluation Guide

## Overview

Evaluations test whether LLMs can effectively use your MCP server to answer realistic, complex questions. A good evaluation proves that your server enables real-world task completion.

## Purpose

Evaluations serve multiple purposes:

1. **Validate Server Quality**: Confirm tools work together to solve complex tasks
2. **Test Tool Design**: Verify tools are discoverable and usable
3. **Measure Effectiveness**: Quantify how well LLMs can use your server
4. **Guide Improvements**: Identify gaps in tool coverage or documentation

## Evaluation Creation Process

### Step 1: Tool Inspection

To create effective evaluations, first understand what tools are available and their capabilities.

**Load your server's tool list:**
- Read the server code or documentation
- Note available tools and their parameters
- Understand what each tool can do

**Example tool inventory:**
```
Available Tools:
- search_issues(query, state, limit) - Search GitHub issues
- get_issue(issue_number) - Get specific issue details
- list_comments(issue_number) - Get comments on an issue
- get_user(username) - Get user information
- list_repositories(org) - List organization repositories
```

### Step 2: Content Exploration

Before writing questions, explore what data is actually available through READ-ONLY operations.

**Exploration workflow:**
1. Use search/list tools to discover available content
2. Note interesting patterns, names, IDs, relationships
3. Identify data that could form the basis of questions
4. Verify data is stable (won't change over time)

**Example exploration:**
```
# Explore GitHub issues
search_issues("is:open label:bug") → Find bug reports
search_issues("author:octocat") → Find user's issues
get_issue(123) → See issue structure and details
list_comments(123) → See comment patterns
```

**What to look for:**
- Unique identifiers that can be referenced
- Relationships between entities
- Specific values that are verifiable
- Patterns that require multi-step exploration

### Step 3: Question Generation

Create 10 complex, realistic questions based on your exploration.

#### Question Requirements

Each question MUST be:

**1. Independent**
- Not dependent on other questions
- Can be answered in isolation
- Doesn't require previous question context

**2. Read-only**
- Only uses non-destructive operations
- No creating, updating, or deleting
- Safe to run multiple times

**3. Complex**
- Requires multiple tool calls (3-10+)
- Involves exploration and discovery
- Can't be answered by a single tool call
- Tests tool orchestration

**4. Realistic**
- Based on real use cases
- Something a human would actually want to know
- Reflects practical value of the server

**5. Verifiable**
- Has a single, clear, specific answer
- Answer can be verified by string comparison
- Not subjective or ambiguous
- Answer is stable over time

**6. Stable**
- Answer won't change over time
- Based on historical or fixed data
- Not dependent on current state (e.g., "today's date")

#### Question Patterns

**Good question patterns:**

**Deep Exploration:**
```
"In discussions about the spotted wild cat model, engineers debated
what ASL (AI Safety Level) designation it needed. What number (X in ASL-X)
was being determined?"
```
*Why it's good: Requires searching → filtering → reading multiple comments → extracting specific value*

**Cross-Reference:**
```
"Which repository has the most issues labeled 'performance' that were
closed in 2023 by users whose username starts with 'eng-'?"
```
*Why it's good: Requires listing repos → searching issues → filtering by criteria → counting*

**Multi-Step Reasoning:**
```
"Find the issue with the longest discussion thread (most comments) that
mentions both 'kubernetes' and 'memory leak'. What was the final resolution?"
```
*Why it's good: Requires searching → getting comments → comparing lengths → reading resolution*

**Bad question patterns:**

❌ **Too Simple:**
```
"How many open issues are there?"
```
*Why it's bad: Single tool call, not realistic, changes over time*

❌ **Ambiguous Answer:**
```
"What's the most important feature request?"
```
*Why it's bad: Subjective, can't be verified by string comparison*

❌ **Unstable:**
```
"What issue was created most recently?"
```
*Why it's bad: Answer changes as new issues are created*

❌ **Requires Modification:**
```
"Create a new issue and tell me its number"
```
*Why it's bad: Not read-only, changes state*

#### Tips for Great Questions

1. **Start with exploration**: Use the tools yourself to discover interesting data
2. **Look for buried information**: Questions that require digging through multiple layers
3. **Use specific identifiers**: Reference specific names, IDs, or values found during exploration
4. **Test multiple tools**: Questions should require using different tools together
5. **Verify answers**: Manually solve each question to confirm the answer

### Step 4: Answer Verification

For each question, solve it yourself using the tools to verify:

1. **The question is answerable**: Tools provide the necessary information
2. **The answer is specific**: Not vague or subjective
3. **The answer is stable**: Won't change over time
4. **The process is realistic**: Represents real workflow

**Verification checklist:**
- [ ] I can answer the question using only available tools
- [ ] The answer is a specific value I can verify
- [ ] The answer won't change if I run this tomorrow
- [ ] The question reflects a realistic use case
- [ ] The question requires 3+ tool calls to answer
- [ ] Multiple people would arrive at the same answer

## Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>

  <qa_pair>
    <question>In the performance optimization thread for the container orchestration system, engineers identified a memory leak pattern. What was the exact regex pattern they used to detect the leak in log files?</question>
    <answer>^\[ERROR\].*memory allocation failed.*0x[0-9a-f]{8}$</answer>
  </qa_pair>

  <!-- 8 more qa_pairs... -->
</evaluation>
```

### XML Format Rules

- Root element: `<evaluation>`
- Each Q&A pair in `<qa_pair>` tags
- Question in `<question>` tags
- Answer in `<answer>` tags
- Exactly 10 qa_pair elements
- No other elements or attributes

### Answer Format Guidelines

**Keep answers concise and specific:**

✅ Good answers:
- `3` (number)
- `ASL-3` (specific code)
- `John Smith` (name)
- `2024-03-15` (date)
- `memory-leak-fix` (identifier)

❌ Bad answers:
- `The answer is 3` (extra words)
- `It was determined to be ASL-3` (verbose)
- `The engineer's name was John Smith` (redundant)

## Example Evaluation

Here's a complete example for a GitHub MCP server:

```xml
<evaluation>
  <qa_pair>
    <question>Find the issue discussing the "nanobanana" model launch. In the thread, engineers debated what ASL safety level it required. What number (the X in ASL-X) was being determined?</question>
    <answer>3</answer>
  </qa_pair>

  <qa_pair>
    <question>Which repository owned by the 'anthropics' organization has the most issues labeled 'documentation' that were closed in 2024?</question>
    <answer>claude-code</answer>
  </qa_pair>

  <qa_pair>
    <question>Find the issue with the most comments that mentions both 'kubernetes' and 'prometheus'. What was the issue number?</question>
    <answer>1247</answer>
  </qa_pair>

  <qa_pair>
    <question>In issues labeled 'bug' and 'critical', find the one where the user 'eng-alice' proposed a fix involving a specific regex pattern. What was that exact regex pattern?</question>
    <answer>^\\[ERROR\\].*timeout.*\\d{3}ms$</answer>
  </qa_pair>

  <qa_pair>
    <question>Find discussions about the "fast-inference" feature. What was the exact name of the configuration parameter that controlled batch size?</question>
    <answer>inference_batch_size</answer>
  </qa_pair>

  <qa_pair>
    <question>Which issue authored by 'devops-team' and labeled 'infrastructure' has the label that was added most recently among all infrastructure issues?</question>
    <answer>892</answer>
  </qa_pair>

  <qa_pair>
    <question>In the issue discussing the migration from PostgreSQL to DuckDB, what was the exact version number of DuckDB that was finally chosen?</question>
    <answer>0.9.2</answer>
  </qa_pair>

  <qa_pair>
    <question>Find the issue where engineers discussed adding support for a new embedding model. What was the exact model identifier they decided to use?</question>
    <answer>text-embedding-3-large</answer>
  </qa_pair>

  <qa_pair>
    <question>In issues labeled 'security', find the one discussing API rate limiting. What was the exact rate limit (requests per minute) that was implemented?</question>
    <answer>100</answer>
  </qa_pair>

  <qa_pair>
    <question>Which user who commented on issues labeled 'performance' has the username that appears most frequently across all performance-related discussions?</question>
    <answer>perf-engineer-bob</answer>
  </qa_pair>
</evaluation>
```

## Running Evaluations

### Using the Connections Script

The `scripts/connections.py` script helps test your MCP server by running evaluations.

**Basic usage:**
```bash
# Run evaluation
python scripts/connections.py evaluate \
  --server-command "python server.py" \
  --eval-file evaluation.xml \
  --output results.json
```

**What it does:**
1. Starts your MCP server
2. Connects an LLM to the server
3. Asks each question from the evaluation
4. Compares LLM answers to expected answers
5. Reports success rate and details

**Output format:**
```json
{
  "total_questions": 10,
  "correct": 8,
  "incorrect": 2,
  "accuracy": 0.8,
  "details": [
    {
      "question": "...",
      "expected": "3",
      "actual": "3",
      "correct": true
    },
    {
      "question": "...",
      "expected": "claude-code",
      "actual": "anthropic-sdk",
      "correct": false
    }
  ]
}
```

### Interpreting Results

**Good results:**
- 80%+ accuracy: Server is working well
- Failed questions reveal tool gaps or documentation issues
- Use failures to improve server

**Poor results (<50% accuracy):**
- Tools may be missing key functionality
- Error messages may be unclear
- Documentation may be insufficient
- Questions may be too hard (verify manually)

## Iteration Based on Results

When evaluations reveal problems:

1. **Analyze failures**: Why did the LLM get it wrong?
2. **Identify root cause**:
   - Missing tool functionality?
   - Unclear tool descriptions?
   - Poor error messages?
   - Confusing response formats?

3. **Make improvements**:
   - Add missing tools
   - Improve documentation
   - Better error messages
   - Clearer response formatting

4. **Re-run evaluations**: Verify improvements work

## Best Practices

### DO:
- ✅ Create questions based on real exploration
- ✅ Verify all answers manually first
- ✅ Make questions realistic and practical
- ✅ Test multiple tools working together
- ✅ Use specific, verifiable answers
- ✅ Base questions on stable data

### DON'T:
- ❌ Write questions without exploring first
- ❌ Use subjective or ambiguous answers
- ❌ Create questions requiring state changes
- ❌ Make questions too simple (single tool call)
- ❌ Use answers that change over time
- ❌ Copy questions without understanding them

## Summary

Good evaluations:
1. Are based on deep content exploration
2. Test realistic, complex workflows
3. Require multiple tool calls
4. Have specific, stable, verifiable answers
5. Reflect real-world use cases
6. Help improve server quality

Use evaluations to validate your server works effectively and guide improvements.
