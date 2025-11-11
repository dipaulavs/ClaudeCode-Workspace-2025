# Google Gemini API Pricing Reference

## Overview

This document contains the official pricing for Google Gemini API models as of January 2025.

**Source:** https://ai.google.dev/gemini-api/docs/pricing

## Gemini 2.0 Flash (Experimental)

**Free during experimental period**

### Input Pricing
- Text: Free
- Image: Free
- Audio: Free
- Video: Free

### Output Pricing
- Text: Free
- Audio: Free

### Context Caching
- Storage: Free
- Input (cached): Free

**Rate Limits:**
- 10 requests per minute (RPM)
- 4 million tokens per minute (TPM)

---

## Gemini 1.5 Flash

### Prompts ≤ 128K tokens

| Input Type | Price per 1M tokens |
|------------|---------------------|
| Text input | $0.075 |
| Image input | $0.075 |
| Audio input | $0.075 |
| Video input | $0.075 |

| Output Type | Price per 1M tokens |
|-------------|---------------------|
| Text output | $0.30 |

### Prompts > 128K tokens

| Input Type | Price per 1M tokens |
|------------|---------------------|
| Text input | $0.15 |
| Image input | $0.15 |
| Audio input | $0.15 |
| Video input | $0.15 |

| Output Type | Price per 1M tokens |
|-------------|---------------------|
| Text output | $0.60 |

### Context Caching

| Operation | Price per 1M tokens |
|-----------|---------------------|
| Storage | $1.00 per million tokens per hour |
| Input (cached) | $0.01875 (≤128K) / $0.0375 (>128K) |

**Rate Limits (Free tier):**
- 15 RPM
- 1 million TPM
- 1,500 requests per day (RPD)

**Rate Limits (Paid tier):**
- 2,000 RPM
- 4 million TPM

---

## Gemini 1.5 Pro

### Prompts ≤ 128K tokens

| Input Type | Price per 1M tokens |
|------------|---------------------|
| Text input | $1.25 |
| Image input | $1.25 |
| Audio input | $1.25 |
| Video input | $1.25 |

| Output Type | Price per 1M tokens |
|-------------|---------------------|
| Text output | $5.00 |

### Prompts > 128K tokens

| Input Type | Price per 1M tokens |
|------------|---------------------|
| Text input | $2.50 |
| Image input | $2.50 |
| Audio input | $2.50 |
| Video input | $2.50 |

| Output Type | Price per 1M tokens |
|-------------|---------------------|
| Text output | $10.00 |

### Context Caching

| Operation | Price per 1M tokens |
|-----------|---------------------|
| Storage | $4.50 per million tokens per hour |
| Input (cached) | $0.3125 (≤128K) / $0.625 (>128K) |

**Rate Limits (Free tier):**
- 2 RPM
- 32,000 TPM
- 50 RPD

**Rate Limits (Paid tier):**
- 1,000 RPM
- 4 million TPM

---

## Gemini 1.0 Pro

| Input Type | Price per 1M tokens |
|------------|---------------------|
| Text input | $0.50 |
| Image input | $0.50 |

| Output Type | Price per 1M tokens |
|-------------|---------------------|
| Text output | $1.50 |

**Rate Limits (Free tier):**
- 15 RPM
- 1 million TPM
- 1,500 RPD

**Rate Limits (Paid tier):**
- 360 RPM
- 4 million TPM

---

## Text Embedding

| Model | Price per 1M tokens |
|-------|---------------------|
| text-embedding-004 | $0.00001 (first 128 tokens) |
|                    | $0.00012 (after 128 tokens) |

**Rate Limits (Free tier):**
- 1,500 RPM

**Rate Limits (Paid tier):**
- 1,500 RPM

---

## Important Notes

1. **Billing Unit:** Costs are calculated per 1,000 characters (approximately 1 token = 4 characters for English text)

2. **Free Tier:** Available in all supported regions through Google AI Studio. No credit card required.

3. **Paid Tier:** Requires Cloud Billing account for higher rate limits and production use.

4. **Failed Requests:** Requests that fail with 4xx or 5xx errors are NOT charged, but still count toward quota.

5. **Context Caching:** Charged separately for storage (per hour) and input (per use). Can reduce costs for repeated long contexts.

6. **Tuned Models:** Pricing same as base model + additional tuning costs (see documentation).

7. **Rate Limit Notes:**
   - RPM = Requests Per Minute
   - TPM = Tokens Per Minute
   - RPD = Requests Per Day

---

## Cost Calculation Examples

### Example 1: Gemini 1.5 Flash (128K context)

**Request:**
- Input: 50,000 tokens (text)
- Output: 5,000 tokens (text)

**Cost:**
- Input: (50,000 / 1,000,000) × $0.075 = $0.00375
- Output: (5,000 / 1,000,000) × $0.30 = $0.00150
- **Total: $0.00525**

### Example 2: Gemini 1.5 Pro (200K context)

**Request:**
- Input: 200,000 tokens (text)
- Output: 10,000 tokens (text)

**Cost:**
- Input: (200,000 / 1,000,000) × $2.50 = $0.50
- Output: (10,000 / 1,000,000) × $10.00 = $0.10
- **Total: $0.60**

### Example 3: Context Caching

**Scenario:** 500K token document cached for 2 hours, used 10 times

**Cost:**
- Storage: (500,000 / 1,000,000) × $1.00 × 2 hours = $1.00
- Input (10 uses): (500,000 / 1,000,000) × $0.0375 × 10 = $0.1875
- **Total: $1.1875**

**vs. without caching:**
- Input (10 uses): (500,000 / 1,000,000) × $0.15 × 10 = $0.75
- **Savings: No savings in this case** (caching costs more for short sessions)

**When caching saves money:** Long sessions (>8 hours) or many uses (>50)

---

## Service Name in BigQuery

When querying billing data, filter by:

```sql
service.description = 'Generative Language API'
```

This covers all Gemini API usage (Flash, Pro, Embedding, etc.)

---

**Last Updated:** 2025-01-08
