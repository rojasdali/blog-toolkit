"""Safe loader for Google Search Console striking-distance keyword telemetry."""

import json
import logging
import os
from datetime import datetime, timedelta

from blog_toolkit.engine.types import StrikingKeyword

logger = logging.getLogger(__name__)


def _get_gsc_credentials():
    """Resolves credentials from service account JSON or environment."""
    try:
        from google.oauth2 import service_account
    except ImportError:
        return None

    raw = os.getenv("GSC_SERVICE_ACCOUNT_JSON")
    if raw and raw.strip().startswith("{"):
        try:
            scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
            return service_account.Credentials.from_service_account_info(
                json.loads(raw), scopes=scopes
            )
        except Exception as e:
            logger.debug("Failed parsing GSC_SERVICE_ACCOUNT_JSON: %s", e)

    file_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if file_path and os.path.exists(file_path):
        try:
            scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
            return service_account.Credentials.from_service_account_file(
                file_path, scopes=scopes
            )
        except Exception as e:
            logger.debug("Failed loading credentials file: %s", e)
    return None


def fetch_live_striking_keywords(
    site_url: str | None = None,
    days: int = 30,
) -> list[StrikingKeyword]:
    """Queries live striking-distance keywords (pos 8.0-25.0) from GSC."""
    creds = _get_gsc_credentials()
    if not creds:
        return []

    try:
        from googleapiclient.discovery import build

        url = site_url or os.getenv("GSC_SITE_URL", "sc-domain:el-laundry.com")
        now = datetime.now()
        end_date = (now - timedelta(days=2)).strftime("%Y-%m-%d")
        start_date = (now - timedelta(days=days)).strftime("%Y-%m-%d")

        service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
        req = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["query"],
            "rowLimit": 150,
        }
        res = service.searchanalytics().query(siteUrl=url, body=req).execute()

        keywords: list[StrikingKeyword] = []
        for r in res.get("rows", []):
            pos = float(r.get("position", 0.0))
            impr = int(r.get("impressions", 0))
            clicks = int(r.get("clicks", 0))
            q = str(r["keys"][0]).strip()
            if 8.0 <= pos <= 25.0 and impr >= 3:
                keywords.append(StrikingKeyword(query=q, position=pos, impressions=impr, clicks=clicks))
        return keywords
    except Exception as e:
        logger.warning("Could not fetch GSC striking keywords: %s", e)
        return []
