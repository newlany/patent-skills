#!/usr/bin/env python3
"""
PatentsView API Helper Script

This script provides convenient functions for searching patents using the
PatentsView Search API. It handles authentication, request construction,
pagination, and error handling.

Usage:
    export PATENTSVIEW_API_KEY="your_api_key_here"
    python patent_search.py
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class PatentsViewAPI:
    """Client for the PatentsView Search API."""

    BASE_URL = "https://search.patentsview.org/api/v1/patent/"
    RATE_LIMIT = 45  # requests per minute

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the API client.

        Args:
            api_key: PatentsView API key. If not provided, reads from
                    PATENTSVIEW_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("PATENTSVIEW_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set PATENTSVIEW_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.last_request_time = 0
        self.request_count = 0
        self.request_times = []

    def _rate_limit(self):
        """Implement rate limiting (45 requests per minute)."""
        current_time = time.time()

        # Remove requests older than 60 seconds
        self.request_times = [t for t in self.request_times if current_time - t < 60]

        # If we've hit the rate limit, wait
        if len(self.request_times) >= self.RATE_LIMIT:
            wait_time = 60 - (current_time - self.request_times[0])
            if wait_time > 0:
                print(f"Rate limit reached. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                # Clear old requests after waiting
                self.request_times = []

        self.request_times.append(current_time)

    def search(
        self,
        query: dict[str, Any],
        fields: Optional[list[str]] = None,
        sort: Optional[list[dict[str, str]]] = None,
        options: Optional[dict[str, Any]] = None,
        method: str = "POST",
    ) -> dict[str, Any]:
        """
        Execute a patent search query.

        Args:
            query: Query dictionary with search criteria
            fields: List of fields to return
            sort: Sort specifications
            options: Additional options (size, after, etc.)
            method: HTTP method (GET or POST)

        Returns:
            API response as dictionary
        """
        self._rate_limit()

        # Build request payload
        payload = {"q": query}
        if fields:
            payload["f"] = fields
        if sort:
            payload["s"] = sort
        if options:
            payload["o"] = options

        # Make request
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}

        try:
            if method == "POST":
                req = Request(
                    self.BASE_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST",
                )
            else:  # GET
                url = f"{self.BASE_URL}?{urlencode({'q': json.dumps(query)})}"
                req = Request(url, headers=headers)

            with urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result

        except HTTPError as e:
            error_body = e.read().decode("utf-8")
            error_msg = f"HTTP {e.code}: {e.reason}"
            if e.headers.get("X-Status-Reason"):
                error_msg += f" - {e.headers['X-Status-Reason']}"
            error_msg += f"\n{error_body}"
            raise Exception(error_msg)

        except URLError as e:
            raise Exception(f"Network error: {e.reason}")

    def search_by_title(
        self,
        keywords: str,
        limit: int = 100,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Search patents by title keywords.

        Args:
            keywords: Keywords to search in title
            limit: Maximum number of results
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            API response
        """
        query = {"_text_any": {"patent_title": keywords}}

        if start_date or end_date:
            conditions = [query]
            if start_date:
                conditions.append({"_gte": {"patent_date": start_date}})
            if end_date:
                conditions.append({"_lte": {"patent_date": end_date}})
            query = {"_and": conditions}

        fields = [
            "patent_id",
            "patent_title",
            "patent_date",
            "inventors.inventor_name_last",
            "assignees.assignee_organization",
        ]

        sort = [{"patent_date": "desc"}]
        options = {"size": limit}

        return self.search(query, fields, sort, options)

    def search_by_inventor(
        self, last_name: str, first_name: Optional[str] = None, limit: int = 100
    ) -> dict[str, Any]:
        """
        Search patents by inventor name.

        Args:
            last_name: Inventor last name
            first_name: Inventor first name (optional)
            limit: Maximum number of results

        Returns:
            API response
        """
        conditions = [{"inventors.inventor_name_last": last_name}]
        if first_name:
            conditions.append({"inventors.inventor_name_first": first_name})

        query = {"_and": conditions} if len(conditions) > 1 else conditions[0]

        fields = [
            "patent_id",
            "patent_title",
            "patent_date",
            "inventors.inventor_name_first",
            "inventors.inventor_name_last",
        ]

        sort = [{"patent_date": "desc"}]
        options = {"size": limit}

        return self.search(query, fields, sort, options)

    def search_by_assignee(
        self, assignee: str, limit: int = 100, start_date: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Search patents by assignee (company/organization).

        Args:
            assignee: Assignee name or partial name
            limit: Maximum number of results
            start_date: Optional start date filter (YYYY-MM-DD)

        Returns:
            API response
        """
        conditions = [{"assignees.assignee_organization": {"_contains": assignee}}]
        if start_date:
            conditions.append({"_gte": {"patent_date": start_date}})

        query = {"_and": conditions} if len(conditions) > 1 else conditions[0]

        fields = ["patent_id", "patent_title", "patent_date", "assignees.assignee_organization"]

        sort = [{"patent_date": "desc"}]
        options = {"size": limit}

        return self.search(query, fields, sort, options)

    def search_prior_art(
        self, keywords: str, before_date: str, limit: int = 100, search_abstract: bool = True
    ) -> dict[str, Any]:
        """
        Search for prior art before a specific date.

        Args:
            keywords: Keywords to search
            before_date: Search patents before this date (YYYY-MM-DD)
            limit: Maximum number of results
            search_abstract: If True, search in both title and abstract

        Returns:
            API response
        """
        if search_abstract:
            text_query = {
                "_or": [
                    {"_text_any": {"patent_title": keywords}},
                    {"_text_any": {"patent_abstract": keywords}},
                ]
            }
        else:
            text_query = {"_text_any": {"patent_title": keywords}}

        query = {
            "_and": [text_query, {"_lt": {"patent_date": before_date}}, {"patent_type": "utility"}]
        }

        fields = [
            "patent_id",
            "patent_title",
            "patent_abstract",
            "patent_date",
            "inventors.inventor_name_last",
            "assignees.assignee_organization",
            "cpc_current.cpc_group_id",
        ]

        sort = [{"patent_date": "desc"}]
        options = {"size": limit}

        return self.search(query, fields, sort, options)

    def get_all_pages(
        self,
        query: dict[str, Any],
        fields: Optional[list[str]] = None,
        sort: Optional[list[dict[str, str]]] = None,
        max_results: int = 1000,
    ) -> list[dict[str, Any]]:
        """
        Retrieve all pages of results up to max_results.

        Args:
            query: Query dictionary
            fields: Fields to return
            sort: Sort specifications
            max_results: Maximum total results to retrieve

        Returns:
            List of all patent records
        """
        all_patents = []
        page_size = min(100, max_results)
        options = {"size": page_size}

        while len(all_patents) < max_results:
            response = self.search(query, fields, sort, options)

            if response.get("error"):
                raise Exception(f"API error: {response}")

            patents = response.get("patents", [])
            if not patents:
                break

            all_patents.extend(patents)

            # Check if there are more results
            if len(patents) < page_size or len(all_patents) >= response.get("total_hits", 0):
                break

            # Set up pagination cursor
            if sort:
                last_patent = patents[-1]
                cursor = []
                for sort_spec in sort:
                    field = list(sort_spec.keys())[0]
                    # Handle nested fields
                    field_parts = field.split(".")
                    value = last_patent
                    for part in field_parts:
                        value = value.get(part) if isinstance(value, dict) else value
                    cursor.append(value)
                options["after"] = cursor
            else:
                # Default sort by patent_id
                options["after"] = [patents[-1]["patent_id"]]

        return all_patents[:max_results]


def format_patent(patent: dict[str, Any]) -> str:
    """Format a patent record for display."""
    lines = []
    lines.append(f"Patent ID: US{patent.get('patent_id', 'N/A')}")
    lines.append(f"Title: {patent.get('patent_title', 'N/A')}")
    lines.append(f"Date: {patent.get('patent_date', 'N/A')}")

    inventors = patent.get("inventors", [])
    if inventors:
        inventor_names = [
            f"{inv.get('inventor_name_first', '')} {inv.get('inventor_name_last', '')}"
            for inv in inventors[:3]
        ]
        lines.append(f"Inventors: {', '.join(inventor_names)}")
        if len(inventors) > 3:
            lines.append(f"  (and {len(inventors) - 3} more)")

    assignees = patent.get("assignees", [])
    if assignees:
        assignee_names = [
            a.get("assignee_organization", "") for a in assignees if a.get("assignee_organization")
        ]
        if assignee_names:
            lines.append(f"Assignees: {', '.join(assignee_names[:2])}")

    abstract = patent.get("patent_abstract", "")
    if abstract:
        lines.append(f"Abstract: {abstract[:200]}...")

    lines.append(f"URL: https://patents.google.com/patent/US{patent.get('patent_id', '')}")
    lines.append("")

    return "\n".join(lines)


def _dump_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def _doctor_status() -> dict[str, Any]:
    has_api_key = bool(os.environ.get("PATENTSVIEW_API_KEY"))
    return {
        "ready": has_api_key,
        "patentsview_api_key_present": has_api_key,
        "setup_url": (
            "https://patentsview-support.atlassian.net/servicedesk/customer/portal/1/group/1/create/18"
        ),
        "error": None if has_api_key else "PATENTSVIEW_API_KEY is not set.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search the PatentsView API.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Check whether PATENTSVIEW_API_KEY is configured.")

    title_parser = subparsers.add_parser("title", help="Search by title keywords.")
    title_parser.add_argument("keywords")
    title_parser.add_argument("--limit", type=int, default=10)
    title_parser.add_argument("--start-date")
    title_parser.add_argument("--end-date")

    assignee_parser = subparsers.add_parser("assignee", help="Search by assignee name.")
    assignee_parser.add_argument("name")
    assignee_parser.add_argument("--limit", type=int, default=10)
    assignee_parser.add_argument("--start-date")

    inventor_parser = subparsers.add_parser("inventor", help="Search by inventor name.")
    inventor_parser.add_argument("last_name")
    inventor_parser.add_argument("--first-name")
    inventor_parser.add_argument("--limit", type=int, default=10)

    prior_art_parser = subparsers.add_parser("prior-art", help="Search for prior art before a date.")
    prior_art_parser.add_argument("keywords")
    prior_art_parser.add_argument("before_date", help="YYYY-MM-DD")
    prior_art_parser.add_argument("--limit", type=int, default=10)
    prior_art_parser.add_argument(
        "--title-only",
        action="store_true",
        help="Only search titles instead of title + abstract.",
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "doctor":
        _dump_json(_doctor_status())
        return 0

    try:
        api = PatentsViewAPI()
    except ValueError as exc:
        _dump_json({"error": str(exc), "doctor_hint": "Run: python3 patent_search.py doctor"})
        return 1

    try:
        if args.command == "title":
            payload = api.search_by_title(
                args.keywords,
                limit=args.limit,
                start_date=args.start_date,
                end_date=args.end_date,
            )
        elif args.command == "assignee":
            payload = api.search_by_assignee(
                args.name,
                limit=args.limit,
                start_date=args.start_date,
            )
        elif args.command == "inventor":
            payload = api.search_by_inventor(
                args.last_name,
                first_name=args.first_name,
                limit=args.limit,
            )
        else:
            payload = api.search_prior_art(
                args.keywords,
                args.before_date,
                limit=args.limit,
                search_abstract=not args.title_only,
            )
    except Exception as exc:
        _dump_json({"error": str(exc)})
        return 1

    _dump_json(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
