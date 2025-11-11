---
name: google-billing-monitor
description: Monitor Google Cloud billing costs via BigQuery Export. Use when user asks to check spending, query costs (today/yesterday/week/month/hour), track Gemini API usage, or wants billing reports. Auto-invokes when user mentions checking costs, spending, or billing data.
---

# Google Billing Monitor

## Overview

Monitor Google Cloud and Gemini API costs by querying billing data exported to BigQuery. Enables real-time cost tracking, service-level breakdowns, and historical spending analysis.

**Limitations:** Billing data has latency (typically hours). Not suitable for real-time token counting - use this for post-usage cost analysis only.

## When to Use This Skill

Invoke this skill when the user asks to:
- Check spending (today, yesterday, week, month, hour)
- Query Gemini API costs
- Track Google Cloud billing
- Get billing reports or cost breakdowns
- Monitor service-level expenses
- Analyze historical spending patterns

## Prerequisites

Before using this skill, ensure BigQuery Export is configured:

### 1. Enable BigQuery Export (One-Time Setup)

**Required by user:**

1. Go to [Cloud Billing Export](https://console.cloud.google.com/billing/export)
2. Select billing account
3. Click "EDIT SETTINGS" under "BigQuery export"
4. Choose or create a BigQuery dataset (e.g., `billing_export`)
5. Enable "Detailed usage cost"
6. Click "Save"

**Dataset location:** Note the dataset name (e.g., `billing_export`) - needed for queries.

**Data freshness:** Billing data updates "throughout the day" with latency of several hours. Do not expect real-time data.

### 2. Grant BigQuery Permissions

Ensure the service account has access:

```bash
# Service account email (already configured):
# calude-code@claude-code-477312.iam.gserviceaccount.com

# Grant BigQuery Data Viewer role to the dataset
# (User must do this via Cloud Console or gcloud CLI)
```

**Via Cloud Console:**
1. Go to [BigQuery](https://console.cloud.google.com/bigquery)
2. Select the billing dataset (e.g., `billing_export`)
3. Click "SHARE" → "Permissions"
4. Add `calude-code@claude-code-477312.iam.gserviceaccount.com`
5. Grant role: "BigQuery Data Viewer"

**Via gcloud CLI:**
```bash
gcloud projects add-iam-policy-binding claude-code-477312 \
    --member="serviceAccount:calude-code@claude-code-477312.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"
```

## Quick Start

### Query Today's Costs

```bash
python3 scripts/query_costs.py
```

### Query Specific Period

```bash
python3 scripts/query_costs.py --period yesterday
python3 scripts/query_costs.py --period week
python3 scripts/query_costs.py --period month
python3 scripts/query_costs.py --period hour  # Last 60 minutes
```

### Filter by Service

```bash
# Gemini API only
python3 scripts/query_costs.py --service "Generative Language API"

# BigQuery costs
python3 scripts/query_costs.py --service "BigQuery"

# Combine with period
python3 scripts/query_costs.py --period week --service "Generative Language API"
```

### Custom Dataset Name

If the BigQuery dataset is not named `billing_export`:

```bash
python3 scripts/query_costs.py --dataset my_custom_dataset_name
```

## Core Capabilities

### 1. Period-Based Queries

Query costs for different time periods:

| Period | Description | Use Case |
|--------|-------------|----------|
| `today` | Current day (00:00 to now) | Daily cost tracking |
| `yesterday` | Previous day | Yesterday's spending |
| `week` | Last 7 days | Weekly trends |
| `month` | Current calendar month | Monthly budget tracking |
| `hour` | Last 60 minutes | Recent activity (note: data delay) |

**Example:**
```bash
python3 scripts/query_costs.py --period month
```

### 2. Service-Level Breakdown

Filter costs by Google Cloud service:

**Common services:**
- `Generative Language API` - Gemini API (Flash, Pro, Embedding)
- `BigQuery` - BigQuery queries and storage
- `Cloud Storage` - GCS buckets
- `Compute Engine` - VM instances
- `Cloud Functions` - Serverless functions

**Example:**
```bash
# Check only Gemini API costs
python3 scripts/query_costs.py --service "Generative Language API"
```

### 3. Cost Analysis Output

The script returns:

```
================================================================================
GOOGLE CLOUD BILLING SUMMARY
================================================================================

Service: Generative Language API
  Cost: USD 0.1234
  Records: 47
  Period: 2025-01-08 00:00:00 UTC to 2025-01-08 23:59:59 UTC
--------------------------------------------------------------------------------
Service: BigQuery
  Cost: USD 0.0056
  Records: 12
  Period: 2025-01-08 00:00:00 UTC to 2025-01-08 23:59:59 UTC
--------------------------------------------------------------------------------

TOTAL COST: USD 0.1290

================================================================================
```

**Fields explained:**
- **Service:** Google Cloud service name
- **Cost:** Total cost in currency (usually USD)
- **Records:** Number of billing records (individual line items)
- **Period:** Time range of usage data

### 4. Pricing Reference

For interpreting costs, consult `references/gemini_pricing.md`:

**Key Gemini API prices:**
- Gemini 1.5 Flash: $0.075/1M input tokens, $0.30/1M output tokens (≤128K)
- Gemini 1.5 Pro: $1.25/1M input tokens, $5.00/1M output tokens (≤128K)
- Gemini 2.0 Flash: Free (experimental)

**Load pricing reference when needed:**
```bash
# Read for detailed pricing breakdown
cat references/gemini_pricing.md
```

## Common Use Cases

### Use Case 1: Daily Cost Tracking

**User request:** "How much did I spend on Gemini API today?"

**Workflow:**
```bash
python3 scripts/query_costs.py --service "Generative Language API"
```

**Expected output:** Cost breakdown for Gemini API usage today.

**Note:** Data may be delayed by several hours. Morning queries may show $0.00.

### Use Case 2: Weekly Budget Check

**User request:** "What are my total Google Cloud costs this week?"

**Workflow:**
```bash
python3 scripts/query_costs.py --period week
```

**Expected output:** All services costs summed for last 7 days.

### Use Case 3: Hourly Monitoring

**User request:** "How much did I spend in the last hour?"

**Workflow:**
```bash
python3 scripts/query_costs.py --period hour
```

**Expected output:** Recent costs (note: likely $0.00 due to data delay).

**Important:** Billing data is NOT real-time. Hourly queries are approximate and may show stale data.

### Use Case 4: Service Comparison

**User request:** "Compare BigQuery vs Gemini API costs this month"

**Workflow:**
```bash
# Query all services for the month
python3 scripts/query_costs.py --period month
```

**Expected output:** Breakdown showing each service's costs side-by-side.

## Troubleshooting

### Error: "Table not found"

**Cause:** BigQuery Export not configured or dataset name incorrect.

**Fix:**
1. Verify BigQuery Export enabled (see Prerequisites)
2. Check dataset name: `--dataset <correct_name>`
3. Wait 24 hours after enabling export for first data

### Error: "Access Denied"

**Cause:** Service account lacks BigQuery permissions.

**Fix:**
1. Grant "BigQuery Data Viewer" role to service account
2. See Prerequisites → Grant BigQuery Permissions

### No Data Returned

**Cause:** No costs in selected period OR data delay.

**Fix:**
1. Try a longer period: `--period week`
2. Wait several hours for data to appear
3. Verify billing is enabled on the project

### Service Name Not Found

**Cause:** Service filter name incorrect.

**Fix:**
1. Run without `--service` to see all service names
2. Use exact name from output (case-sensitive)
3. Common names: "Generative Language API", "BigQuery", "Cloud Storage"

## Limitations

1. **Data Delay:** Billing data has latency of several hours. Not suitable for real-time tracking.

2. **No Token Counting:** Cannot count tokens before requests. Use `GenerativeModel.count_tokens()` for pre-request estimation.

3. **Dataset Required:** User must configure BigQuery Export (one-time setup).

4. **Permissions:** Service account needs BigQuery access (user must grant).

5. **Granularity:** Hourly queries are approximate due to data delay. Best for daily/weekly/monthly analysis.

6. **Free Tier Tracking:** BigQuery Export works for both free and paid tiers, but free tier usage may not show costs (shows $0.00).

## Resources

### scripts/query_costs.py

Main script for querying BigQuery billing data. Supports multiple time periods, service filtering, and custom datasets.

**Usage:** See Quick Start section above.

### references/gemini_pricing.md

Comprehensive pricing reference for Google Gemini API models including:
- Gemini 1.5 Flash pricing
- Gemini 1.5 Pro pricing
- Gemini 1.0 Pro pricing
- Text Embedding pricing
- Context caching costs
- Rate limits (free vs paid tier)
- Cost calculation examples

**When to load:** When user needs to interpret costs or calculate expected spending.

## Auto-Correction System

This skill includes an automatic error correction system that learns from mistakes and prevents them from happening again.

### How It Works

When a script or command in this skill fails:

1. **Detect the error** - The system identifies what went wrong
2. **Fix automatically** - Updates the skill's code/instructions
3. **Log the learning** - Records the fix in LEARNINGS.md
4. **Prevent recurrence** - Same error won't happen again

### Using Auto-Correction

**Scripts available:**

```bash
# Fix a problem in this skill's SKILL.md
python3 scripts/update_skill.py <old_text> <new_text>

# Log what was learned
python3 scripts/log_learning.py <error_description> <fix_description> [line]
```

**Example workflow when error occurs:**

```bash
# 1. Fix the error in SKILL.md
python3 scripts/update_skill.py \
    "python3 query_costs.py --prompt today" \
    "python3 query_costs.py --period today"

# 2. Log the learning
python3 scripts/log_learning.py \
    "Flag --prompt should be --period" \
    "Updated command to use --period flag" \
    "SKILL.md:97"
```

### LEARNINGS.md

All fixes are automatically recorded in `LEARNINGS.md`:

```markdown
### 2025-01-08 - Flag --prompt should be --period

**Problema:** Command used wrong flag name
**Correção:** Updated to use --period flag
**Linha afetada:** SKILL.md:97
**Status:** ✅ Corrigido
```

This creates a history of improvements and ensures mistakes don't repeat.
