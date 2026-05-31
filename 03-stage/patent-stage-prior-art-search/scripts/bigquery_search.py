#!/usr/bin/env python3
"""
Codex-compatible BigQuery patent search helper.

This version is self-contained so the skill can run without the original
repository's `mcp_server` package. It supports:

- dependency and credential checks via `doctor`
- keyword search across Google Patents public BigQuery data
- CPC classification search
- publication lookup by patent number
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from google_patents_fetch import extract_google_patent_record, save_google_patent_record


def _add_local_site_packages() -> None:
    """Allow the script to use a skill-local virtualenv when present."""
    script_dir = Path(__file__).resolve().parent
    for root in (script_dir, script_dir.parent):
        venv_lib = root / ".venv" / "lib"
        if not venv_lib.exists():
            continue
        for python_dir in sorted(venv_lib.glob("python*/site-packages")):
            sys.path.insert(0, str(python_dir))
            return


_add_local_site_packages()

try:
    from google.cloud import bigquery
except ImportError as exc:  # pragma: no cover - environment dependent
    bigquery = None
    BIGQUERY_IMPORT_ERROR = exc
else:
    BIGQUERY_IMPORT_ERROR = None


SKILL_ROOT = Path(__file__).resolve().parent.parent
INSTALL_HINT = (
    f"cd {SKILL_ROOT} && "
    "python3 -m venv .venv && "
    ".venv/bin/pip install -r scripts/requirements.txt"
)


def _default_adc_path() -> Path:
    """Return the standard application-default credentials path."""
    return Path.home() / ".config" / "gcloud" / "application_default_credentials.json"


def _dump_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def _normalized_publication_number(value: str) -> str:
    return "".join(ch for ch in value.upper() if ch.isalnum())


def _google_patents_fallback(
    patent_number: str,
    *,
    fallback_reason: str,
    save_dir: str | None = None,
) -> dict[str, Any]:
    payload = extract_google_patent_record(patent_number)
    record = payload["record"]
    html_text = payload["html"]
    record["fallback_reason"] = fallback_reason
    if save_dir:
        record["saved_files"] = save_google_patent_record(
            patent_number,
            record,
            html_text,
            save_dir,
        )
    return record


class BigQueryPatentSearch:
    """Minimal BigQuery-backed patent search client."""

    FULL_TABLE_ID = "patents-public-data.patents.publications"

    def __init__(self, project_id: str | None = None):
        if bigquery is None:
            raise ImportError(
                "google-cloud-bigquery is not installed. "
                f"Run from this skill directory: {INSTALL_HINT}"
            ) from BIGQUERY_IMPORT_ERROR

        self.billing_project = self._detect_billing_project(project_id)
        if not self.billing_project:
            raise ValueError(
                "No Google Cloud billing project found. Set GOOGLE_CLOUD_PROJECT or "
                "use a credentials JSON file whose project/quota project is enabled for BigQuery."
            )

        self.client = bigquery.Client(project=self.billing_project)

    @staticmethod
    def _detect_billing_project(project_id: str | None) -> str | None:
        if project_id:
            return project_id

        env_project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if env_project:
            return env_project

        for candidate in (
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            str(_default_adc_path()),
        ):
            if not candidate:
                continue
            path = Path(candidate).expanduser()
            if not path.exists():
                continue
            try:
                data = json.loads(path.read_text())
            except Exception:
                continue
            for field in ("quota_project_id", "project_id"):
                if data.get(field):
                    return data[field]

        return None

    @staticmethod
    def _format_date(value: Any) -> str | None:
        if value in (None, ""):
            return None
        text = str(value)
        if len(text) == 8 and text.isdigit():
            return f"{text[:4]}-{text[4:6]}-{text[6:]}"
        return text

    def search_by_keywords(
        self,
        query: str,
        *,
        limit: int = 20,
        country: str = "US",
        start_year: int | None = None,
        end_year: int | None = None,
        search_fields: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        if search_fields is None:
            search_fields = ["abstract", "title", "claims"]

        conditions = ["country_code = @country"]
        text_conditions = []
        if "abstract" in search_fields:
            text_conditions.append("LOWER(abstract_localized[SAFE_OFFSET(0)].text) LIKE @query")
        if "title" in search_fields:
            text_conditions.append("LOWER(title_localized[SAFE_OFFSET(0)].text) LIKE @query")
        if "claims" in search_fields and country.upper() == "US":
            text_conditions.append("LOWER(claims_localized[SAFE_OFFSET(0)].text) LIKE @query")
        if text_conditions:
            conditions.append(f"({' OR '.join(text_conditions)})")
        if start_year:
            conditions.append("CAST(filing_date AS INT64) >= @start_date")
        if end_year:
            conditions.append("CAST(filing_date AS INT64) <= @end_date")

        sql = f"""
        SELECT
          publication_number,
          application_number,
          title_localized[SAFE_OFFSET(0)].text AS title,
          abstract_localized[SAFE_OFFSET(0)].text AS abstract,
          CAST(filing_date AS STRING) AS filing_date,
          CAST(grant_date AS STRING) AS grant_date,
          CAST(publication_date AS STRING) AS publication_date,
          family_id,
          country_code
        FROM `{self.FULL_TABLE_ID}`
        WHERE {' AND '.join(conditions)}
        ORDER BY publication_date DESC
        LIMIT @limit
        """

        params = [
            bigquery.ScalarQueryParameter("country", "STRING", country.upper()),
            bigquery.ScalarQueryParameter("query", "STRING", f"%{query.lower()}%"),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter(
                "start_date", "INT64", int(f"{start_year}0101") if start_year else None
            ),
            bigquery.ScalarQueryParameter(
                "end_date", "INT64", int(f"{end_year}1231") if end_year else None
            ),
        ]

        results = self.client.query(
            sql, job_config=bigquery.QueryJobConfig(query_parameters=params)
        ).result(timeout=30)

        patents: list[dict[str, Any]] = []
        for row in results:
            patents.append(
                {
                    "patent_number": row.publication_number,
                    "application_number": row.application_number,
                    "title": row.title or "",
                    "abstract": row.abstract or "",
                    "filing_date": self._format_date(row.filing_date),
                    "grant_date": self._format_date(row.grant_date),
                    "publication_date": self._format_date(row.publication_date),
                    "country": row.country_code,
                    "family_id": row.family_id,
                }
            )
        return patents

    def get_patent_details(self, patent_number: str) -> dict[str, Any] | None:
        normalized = _normalized_publication_number(patent_number)
        sql = f"""
        SELECT
          publication_number,
          application_number,
          title_localized[SAFE_OFFSET(0)].text AS title,
          abstract_localized[SAFE_OFFSET(0)].text AS abstract,
          claims_localized[SAFE_OFFSET(0)].text AS claims,
          description_localized[SAFE_OFFSET(0)].text AS description,
          CAST(filing_date AS STRING) AS filing_date,
          CAST(grant_date AS STRING) AS grant_date,
          CAST(publication_date AS STRING) AS publication_date,
          family_id,
          country_code,
          cpc,
          ipc
        FROM `{self.FULL_TABLE_ID}`
        WHERE publication_number = @patent_number
           OR REPLACE(publication_number, "-", "") = @normalized_patent_number
        LIMIT 1
        """

        params = [
            bigquery.ScalarQueryParameter("patent_number", "STRING", patent_number.upper()),
            bigquery.ScalarQueryParameter("normalized_patent_number", "STRING", normalized),
        ]

        results = self.client.query(
            sql, job_config=bigquery.QueryJobConfig(query_parameters=params)
        ).result(timeout=30)

        for row in results:
            return {
                "patent_number": row.publication_number,
                "application_number": row.application_number,
                "title": row.title or "",
                "abstract": row.abstract or "",
                "claims": row.claims or "",
                "description": row.description or "",
                "filing_date": self._format_date(row.filing_date),
                "grant_date": self._format_date(row.grant_date),
                "publication_date": self._format_date(row.publication_date),
                "country": row.country_code,
                "family_id": row.family_id,
                "cpc_codes": [item.code for item in row.cpc or [] if getattr(item, "code", None)],
                "ipc_codes": [item.code for item in row.ipc or [] if getattr(item, "code", None)],
            }
        return None

    def search_by_cpc(
        self, cpc_code: str, *, limit: int = 20, country: str = "US"
    ) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
          publication_number,
          application_number,
          title_localized[SAFE_OFFSET(0)].text AS title,
          abstract_localized[SAFE_OFFSET(0)].text AS abstract,
          CAST(filing_date AS STRING) AS filing_date,
          CAST(publication_date AS STRING) AS publication_date,
          country_code
        FROM `{self.FULL_TABLE_ID}`, UNNEST(cpc) AS cpc_entry
        WHERE country_code = @country
          AND STARTS_WITH(cpc_entry.code, @cpc_code)
        ORDER BY publication_date DESC
        LIMIT @limit
        """

        params = [
            bigquery.ScalarQueryParameter("country", "STRING", country.upper()),
            bigquery.ScalarQueryParameter("cpc_code", "STRING", cpc_code.upper()),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
        ]

        results = self.client.query(
            sql, job_config=bigquery.QueryJobConfig(query_parameters=params)
        ).result(timeout=30)

        patents: list[dict[str, Any]] = []
        for row in results:
            patents.append(
                {
                    "patent_number": row.publication_number,
                    "application_number": row.application_number,
                    "title": row.title or "",
                    "abstract": row.abstract or "",
                    "filing_date": self._format_date(row.filing_date),
                    "publication_date": self._format_date(row.publication_date),
                    "country": row.country_code,
                }
            )
        return patents


def check_bigquery_available() -> dict[str, Any]:
    credentials_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    adc_path = _default_adc_path()
    project = BigQueryPatentSearch._detect_billing_project(None)
    status = {
        "dependency_installed": bigquery is not None,
        "google_application_credentials": credentials_env,
        "adc_file_present": adc_path.exists(),
        "adc_path": str(adc_path),
        "billing_project": project,
        "ready": False,
    }

    if bigquery is None:
        status["error"] = (
            "Missing dependency: google-cloud-bigquery. "
            f"Run from this skill directory: {INSTALL_HINT}"
        )
        return status

    if not project:
        status["error"] = (
            "No billing project detected. Set GOOGLE_CLOUD_PROJECT, or point "
            "GOOGLE_APPLICATION_CREDENTIALS at a JSON credential with project information."
        )
        return status

    try:
        searcher = BigQueryPatentSearch(project)
        table = searcher.client.get_table(searcher.FULL_TABLE_ID)
    except Exception as exc:
        status["error"] = str(exc)
        return status

    status["ready"] = True
    status["table_rows"] = table.num_rows
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search Google Patents public data via BigQuery.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Check dependencies, credentials, and billing project.")

    search_parser = subparsers.add_parser("search", help="Keyword search.")
    search_parser.add_argument("query", help="Keyword query, best with 2-3 terms.")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--country", default="US")
    search_parser.add_argument("--start-year", type=int)
    search_parser.add_argument("--end-year", type=int)
    search_parser.add_argument(
        "--fields",
        nargs="+",
        default=["abstract", "title", "claims"],
        choices=["abstract", "title", "claims"],
        help="Fields to search.",
    )

    get_parser = subparsers.add_parser("get", help="Fetch one publication.")
    get_parser.add_argument("patent_number", help="Publication number, hyphenated or plain.")
    get_parser.add_argument(
        "--fallback",
        default="google-patents",
        choices=["google-patents", "none"],
        help="Fallback source when BigQuery full-text retrieval fails.",
    )
    get_parser.add_argument(
        "--save-dir",
        help="Optional directory for fallback HTML/JSON/Markdown files.",
    )

    cpc_parser = subparsers.add_parser("cpc", help="Search by CPC prefix.")
    cpc_parser.add_argument("cpc_code", help="Example: G10L17 or G06F21.")
    cpc_parser.add_argument("--limit", type=int, default=10)
    cpc_parser.add_argument("--country", default="US")

    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "doctor":
        _dump_json(check_bigquery_available())
        return 0

    try:
        searcher = BigQueryPatentSearch()
    except Exception as exc:
        if args.command == "get" and getattr(args, "fallback", None) == "google-patents":
            try:
                payload = _google_patents_fallback(
                    args.patent_number,
                    fallback_reason=f"BigQuery unavailable: {exc}",
                    save_dir=args.save_dir,
                )
                _dump_json(payload)
                return 0
            except Exception as fallback_exc:
                _dump_json(
                    {
                        "error": str(exc),
                        "fallback_error": str(fallback_exc),
                        "doctor_hint": "Run: python3 bigquery_search.py doctor",
                    }
                )
                return 1
        _dump_json({"error": str(exc), "doctor_hint": "Run: python3 bigquery_search.py doctor"})
        return 1

    try:
        if args.command == "search":
            payload = searcher.search_by_keywords(
                args.query,
                limit=args.limit,
                country=args.country,
                start_year=args.start_year,
                end_year=args.end_year,
                search_fields=args.fields,
            )
        elif args.command == "get":
            payload = searcher.get_patent_details(args.patent_number)
            if payload is None and args.fallback == "google-patents":
                payload = _google_patents_fallback(
                    args.patent_number,
                    fallback_reason="BigQuery returned no matching publication.",
                    save_dir=args.save_dir,
                )
        else:
            payload = searcher.search_by_cpc(args.cpc_code, limit=args.limit, country=args.country)
    except Exception as exc:
        if args.command == "get" and args.fallback == "google-patents":
            try:
                payload = _google_patents_fallback(
                    args.patent_number,
                    fallback_reason=f"BigQuery failed: {exc}",
                    save_dir=args.save_dir,
                )
                _dump_json(payload)
                return 0
            except Exception as fallback_exc:
                _dump_json(
                    {
                        "error": str(exc),
                        "fallback_error": str(fallback_exc),
                    }
                )
                return 1
        _dump_json({"error": str(exc)})
        return 1

    _dump_json(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
