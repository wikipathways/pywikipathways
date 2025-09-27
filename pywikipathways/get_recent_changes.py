"""Python translation of the `getRecentChanges` utilities from R/getRecentChanges.R."""

from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, List
import pandas as pd
import requests

_INFO_URL = "https://www.wikipathways.org/json/getPathwayInfo.json"
_DROP_FIELDS = {"authors", "description", "citedIn"}

def _normalize_timestamp(timestamp: str | int | None) -> _dt.date:
    """Return the cutoff date derived from the provided timestamp."""
    if timestamp is None:
        timestamp = 20070301
    text = str(timestamp)[:8]
    if len(text) != 8:
        raise ValueError("Timestamp must contain at least 8 digits (YYYYMMDD).")
    try:
        return _dt.datetime.strptime(text, "%Y%m%d").date()
    except ValueError as exc:
        raise ValueError("Timestamp must be in YYYYMMDD format.") from exc


def _parse_revision_date(raw: str | None) -> _dt.date | None:
    """Convert revision text to a date if possible."""
    if not raw:
        return None
    raw = raw.strip()
    if not raw:
        return None

    iso_candidate = raw[:10]
    try:
        return _dt.date.fromisoformat(iso_candidate)
    except ValueError:
        pass

    basic_candidate = raw[:8]
    try:
        return _dt.datetime.strptime(basic_candidate, "%Y%m%d").date()
    except ValueError:
        return None


def _fetch_recent_changes_json() -> Dict[str, Any]:
    """Fetch the recent changes JSON payload."""
    try:
        response = requests.get(_INFO_URL, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Failed to retrieve JSON data ({exc.response.status_code})."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError("Failed to retrieve JSON data (network error).") from exc


def get_recent_changes(timestamp: str | int | None = None) -> pd.DataFrame:
    """Return recently changed pathways filtered by timestamp.

    Parameters
    ----------
    timestamp : str | int | None, optional
        8-digit cutoff (YYYYMMDD). Pathways with revision dates after this value
        are returned. Defaults to ``20070301`` when omitted.

    Returns
    -------
    pandas.DataFrame
        Table of pathway records excluding ``authors``, ``description``, and
        ``citedIn`` fields.
    """

    cutoff = _normalize_timestamp(timestamp)
    payload = _fetch_recent_changes_json()
    entries = payload.get("pathwayInfo", [])

    template_columns: List[str] | None = None
    records: List[Dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        revision_date = _parse_revision_date(entry.get("revision"))
        if revision_date is None or revision_date <= cutoff:
            continue
        filtered = {k: v for k, v in entry.items() if k not in _DROP_FIELDS}
        if template_columns is None:
            template_columns = list(filtered.keys())
        records.append(filtered)

    if template_columns is None:
        template_columns = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            for key in entry.keys():
                if key in _DROP_FIELDS or key in template_columns:
                    continue
                template_columns.append(key)

    frame = pd.DataFrame.from_records(records, columns=template_columns)
    return frame


def get_recent_changes_ids(timestamp: str | int | None = None) -> List[Any]:
    """Return pathway IDs for recent changes after the given timestamp."""
    frame = get_recent_changes(timestamp)
    return frame.get("id", pd.Series(dtype=object)).tolist()


def get_recent_changes_names(timestamp: str | int | None = None) -> List[Any]:
    """Return pathway names for recent changes after the given timestamp."""
    frame = get_recent_changes(timestamp)
    return frame.get("name", pd.Series(dtype=object)).tolist()


__all__ = [
    "get_recent_changes",
    "get_recent_changes_ids",
    "get_recent_changes_names",
]
