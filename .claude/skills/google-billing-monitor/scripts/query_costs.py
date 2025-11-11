#!/usr/bin/env python3
"""
Query Google Cloud billing costs via BigQuery.

Usage:
    python3 query_costs.py                      # Today's costs
    python3 query_costs.py --period today       # Today's costs
    python3 query_costs.py --period yesterday   # Yesterday's costs
    python3 query_costs.py --period week        # Last 7 days
    python3 query_costs.py --period month       # Current month
    python3 query_costs.py --period hour        # Last hour (approximate)
    python3 query_costs.py --service "Generative Language API"  # Filter by service
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuration
CREDENTIALS_PATH = os.path.expanduser("~/Desktop/ClaudeCode-Workspace/config/google_service_account.json")
PROJECT_ID = "claude-code-477312"

def get_bigquery_client():
    """Initialize BigQuery client with service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/bigquery.readonly"]
    )
    return bigquery.Client(credentials=credentials, project=PROJECT_ID)

def build_query(period="today", service=None, dataset_name=None):
    """
    Build BigQuery SQL query based on period and filters.

    Args:
        period: today, yesterday, week, month, hour
        service: Filter by service description (e.g., "Generative Language API")
        dataset_name: BigQuery dataset name (auto-detected if None)

    Returns:
        SQL query string
    """

    # Define time filters
    time_filters = {
        "today": "DATE(usage_start_time) = CURRENT_DATE()",
        "yesterday": "DATE(usage_start_time) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)",
        "week": "DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)",
        "month": "EXTRACT(MONTH FROM usage_start_time) = EXTRACT(MONTH FROM CURRENT_DATE()) AND EXTRACT(YEAR FROM usage_start_time) = EXTRACT(YEAR FROM CURRENT_DATE())",
        "hour": "usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)"
    }

    time_condition = time_filters.get(period, time_filters["today"])

    # Build service filter
    service_condition = ""
    if service:
        service_condition = f"AND service.description = '{service}'"

    # Note: User needs to replace this with their actual dataset
    if dataset_name is None:
        dataset_name = "billing_export"  # Default, must be configured

    query = f"""
    SELECT
        service.description AS service_name,
        SUM(cost) AS total_cost,
        currency AS currency,
        COUNT(*) AS num_records,
        MIN(usage_start_time) AS earliest_usage,
        MAX(usage_end_time) AS latest_usage
    FROM
        `{PROJECT_ID}.{dataset_name}.gcp_billing_export_v1_*`
    WHERE
        {time_condition}
        {service_condition}
    GROUP BY
        service_name, currency
    ORDER BY
        total_cost DESC
    """

    return query

def format_results(results):
    """Format BigQuery results for display."""
    if not results:
        return "No billing data found for this period."

    output = []
    output.append("\n" + "="*80)
    output.append("GOOGLE CLOUD BILLING SUMMARY")
    output.append("="*80 + "\n")

    total = 0
    for row in results:
        service = row.service_name or "Unknown Service"
        cost = row.total_cost or 0
        currency = row.currency or "USD"
        records = row.num_records
        earliest = row.earliest_usage
        latest = row.latest_usage

        total += cost

        output.append(f"Service: {service}")
        output.append(f"  Cost: {currency} {cost:.4f}")
        output.append(f"  Records: {records}")
        output.append(f"  Period: {earliest} to {latest}")
        output.append("-" * 80)

    output.append(f"\nTOTAL COST: {currency} {total:.4f}\n")
    output.append("="*80)

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Query Google Cloud billing costs")
    parser.add_argument(
        "--period",
        choices=["today", "yesterday", "week", "month", "hour"],
        default="today",
        help="Time period to query (default: today)"
    )
    parser.add_argument(
        "--service",
        help="Filter by service name (e.g., 'Generative Language API')"
    )
    parser.add_argument(
        "--dataset",
        help="BigQuery dataset name (default: billing_export)"
    )

    args = parser.parse_args()

    # Check credentials exist
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"❌ Error: Credentials not found at {CREDENTIALS_PATH}")
        print("Please configure Google Service Account credentials.")
        sys.exit(1)

    try:
        # Initialize BigQuery client
        client = get_bigquery_client()

        # Build and execute query
        query = build_query(args.period, args.service, args.dataset)

        print(f"\n🔍 Querying billing data for period: {args.period}")
        if args.service:
            print(f"   Filtering by service: {args.service}")
        print("\n⏳ Executing query...\n")

        results = client.query(query).result()

        # Format and display results
        output = format_results(results)
        print(output)

    except Exception as e:
        print(f"\n❌ Error querying billing data: {e}")
        print("\nCommon issues:")
        print("1. BigQuery Export not configured - see SKILL.md for setup")
        print("2. Service account lacks BigQuery permissions")
        print("3. Dataset name incorrect - use --dataset flag")
        print("4. Billing data delay (can take hours to appear)")
        sys.exit(1)

if __name__ == "__main__":
    main()
