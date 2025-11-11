# Grok Imagine API Documentation

## Overview

Grok Imagine is xAI's multimodal image and video generation model that converts text or images into short visual outputs with coherent motion and synchronized audio.

**Model Type:** Image To Video, Text To Video, Text To Image, Upscale
**Pricing:** 4 credits ($0.02) per generation — get 6 images each time

## Authentication

All APIs require authentication via Bearer Token.

```
Authorization: Bearer YOUR_API_KEY
```

**Security Notes:**
- 🔒 Keep your API Key secure
- 🚫 Do not share it with others
- ⚡ Reset immediately if compromised

## API Endpoints

### Create Task

**Endpoint:** `POST /api/v1/jobs/createTask`

Create a new generation task.

**Request Body Structure:**
```json
{
  "model": "string",
  "callBackUrl": "string (optional)",
  "input": {
    "prompt": "string (required, max 5000 chars)",
    "aspect_ratio": "string (optional: 2:3, 3:2, 1:1)"
  }
}
```

**Parameters:**

- `model` (required): The model name to use for generation
  - Example: `"grok-imagine/text-to-image"`

- `callBackUrl` (optional): Callback URL for task completion notifications
  - If provided, system sends POST requests when task completes
  - If not provided, no callback notifications sent
  - Example: `"https://your-domain.com/api/callback"`

- `input.prompt` (required): Text description of image to generate
  - Max length: 5000 characters
  - Example: `"Cinematic portrait of a woman sitting by a vinyl record player, retro living room background, soft ambient lighting, warm earthy tones, nostalgic 1970s wardrobe, reflective mood, gentle film grain texture, shallow depth of field, vintage editorial photography style."`

- `input.aspect_ratio` (optional): Width-to-height ratio
  - Options: `"2:3"`, `"3:2"`, `"1:1"`
  - Default: `"1:1"`

**Response Example:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "task_12345678"
  }
}
```

**Response Fields:**
- `code`: Status code (200 = success, others = failure)
- `message`: Response message (error description when failed)
- `data.taskId`: Task ID for querying task status

### Query Task

**Endpoint:** `POST /api/v1/jobs/queryTask`

Query the status of a created task.

**Request Body:**
```json
{
  "taskId": "task_12345678"
}
```

**Response States:**
- `pending`: Task is queued
- `processing`: Task is being processed
- `success`: Task completed successfully
- `fail`: Task failed

**Success Response Example:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "task_12345678",
    "state": "success",
    "resultJson": "{\"resultUrls\":[\"https://example.com/image1.jpg\",\"https://example.com/image2.jpg\"]}",
    "consumeCredits": 4,
    "costTime": 8,
    "createTime": 1755599634000,
    "completeTime": 1755599644000
  }
}
```

**Failure Response Example:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "task_12345678",
    "state": "fail",
    "failCode": "500",
    "failMsg": "Internal server error",
    "consumeCredits": 0
  }
}
```

## Callback Notifications

When `callBackUrl` is provided during task creation, the system sends POST requests to the specified URL upon task completion.

**Success Callback Example:**
```json
{
  "code": 200,
  "data": {
    "completeTime": 1755599644000,
    "consumeCredits": 100,
    "costTime": 8,
    "createTime": 1755599634000,
    "model": "grok-imagine/text-to-image",
    "param": "{\"callBackUrl\":\"https://your-domain.com/api/callback\",\"model\":\"grok-imagine/text-to-image\",\"input\":{\"prompt\":\"...\",\"aspect_ratio\":\"3:2\"}}",
    "remainedCredits": 2510330,
    "resultJson": "{\"resultUrls\":[\"https://example.com/generated-image.jpg\"]}",
    "state": "success",
    "taskId": "e989621f54392584b05867f87b160672",
    "updateTime": 1755599644000
  },
  "msg": "Playground task completed successfully."
}
```

**Failure Callback Example:**
```json
{
  "code": 501,
  "data": {
    "completeTime": 1755597081000,
    "consumeCredits": 0,
    "costTime": 0,
    "createTime": 1755596341000,
    "failCode": "500",
    "failMsg": "Internal server error",
    "model": "grok-imagine/text-to-image",
    "param": "{\"callBackUrl\":\"https://your-domain.com/api/callback\",\"model\":\"grok-imagine/text-to-image\",\"input\":{\"prompt\":\"...\",\"aspect_ratio\":\"3:2\"}}",
    "remainedCredits": 2510430,
    "state": "fail",
    "taskId": "bd3a37c523149e4adf45a3ddb5faf1a8",
    "updateTime": 1755597097000
  },
  "msg": "Playground task failed."
}
```

**Important Notes:**
- The callback content structure is identical to the Query Task API response
- The `param` field contains the complete Create Task request parameters, not just the input section
- If `callBackUrl` is not provided, no callback notifications will be sent

## Rate Limits & Best Practices

1. **Polling Interval:** Wait at least 5 seconds between query attempts
2. **Timeout:** Tasks typically complete within 30-60 seconds
3. **Batch Processing:** Use parallel task creation for multiple images
4. **Cost:** Each generation costs 4 credits ($0.02) and returns 6 images
5. **Prompt Quality:** More detailed prompts produce better results

## Error Handling

Common error scenarios:
- Invalid API key: Check authentication header
- Rate limit exceeded: Implement exponential backoff
- Task timeout: Increase max polling attempts
- Generation failure: Check prompt validity and API status

## Example Workflow

```
1. Create Task
   ↓
2. Receive task_id
   ↓
3. Poll Query Task (every 5s)
   ↓
4. Task state = "success"
   ↓
5. Parse resultJson for image URLs
   ↓
6. Download images
```
