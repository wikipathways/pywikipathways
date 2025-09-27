"""Python translation of the `getPathway` function from R/getPathway.R."""

from __future__ import annotations
from typing import Any
import requests
from lxml import etree as ET

_BASE_URL = (
    "https://www.wikipathways.org/wikipathways-assets/pathways/{pathway}/"
    "{pathway}.gpml"
)


def get_pathway(pathway: str | None, revision: Any = 0) -> str:
    """Return the GPML content for the requested WikiPathways identifier.

    Parameters
    ----------
    pathway : str
        WikiPathways identifier (for example ``"WP554"``).
    revision : Any, optional
        Accepted for API compatibility but ignored because only the latest
        revision is exposed by the service.

    Returns
    -------
    str
        GPML document encoded as UTF-8 text.

    Raises
    ------
    ValueError
        If ``pathway`` is missing.
    RuntimeError
        If the remote GPML cannot be retrieved or parsed.
    """

    if not pathway:
        raise ValueError("Must provide a pathway identifier, e.g. 'WP554'.")

    url = _BASE_URL.format(pathway=pathway)
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response else "unknown"
        raise RuntimeError(
            f"Failed to retrieve GPML ({status_code})."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError("Failed to retrieve GPML (network error).") from exc

    xml_bytes = response.content
    try:
        root = ET.fromstring(xml_bytes)
    except ET.XMLSyntaxError as exc:
        raise RuntimeError("Failed to parse GPML response.") from exc

    xml_string = ET.tostring(
        root, encoding="utf-8", xml_declaration=True
    ).decode("utf-8").rstrip("\n")
    return xml_string


__all__ = ["get_pathway"]
