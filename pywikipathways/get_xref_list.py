"""Python translation of the `getXrefList` function from R/getXrefList.R."""

from __future__ import annotations

import csv
import io
import re
import urllib.error
import urllib.request
from typing import Iterable, List


_CODE_MAP = {
    "En": "Ensembl",
    "L": "NCBI gene",
    "H": "HGNC",
    "S": "UniProt",
    "Wd": "Wikidata",
    "Ce": "ChEBI",
    "Ik": "InChI",
    "Cpc": "PubChem",
    "Cs": "ChemSpider",
    "Ch": "HMDB",
    "Ck": "KEGG",
    "Lm": "LipidMaps",
}

_BASE_URL = (
    "https://www.wikipathways.org/wikipathways-assets/pathways/{pathway}/"
    "{pathway}-datanodes.tsv"
)


def _unique_preserve_order(values: Iterable[str]) -> List[str]:
    """Return unique values while preserving first-seen order."""
    seen = {}
    return [seen.setdefault(v, v) for v in values if v not in seen]


def get_xref_list(pathway: str | None = None,
                  system_code: str | None = None,
                  compact: bool = False) -> List[str]:
    """Return Xref identifiers for the given pathway and system code.

    Parameters
    ----------
    pathway : str
        WikiPathways identifier (for example ``"WP554"``).
    system_code : str
        BridgeDb system code (for example ``"L"`` for NCBI gene).
    compact : bool, optional
        When ``True`` the returned identifiers keep their datasource prefix.
        When ``False`` (default) the prefix is stripped (e.g. ``"ncbigene:1215"``
        becomes ``"1215"``).

    Returns
    -------
    list of str
        Unique identifiers matching the requested system.

    Raises
    ------
    ValueError
        If required arguments are missing or unsupported.
    RuntimeError
        If the remote TSV cannot be retrieved or lacks the requested column.
    """

    if not pathway:
        raise ValueError("Must provide a pathway identifier, e.g. 'WP554'.")
    if not system_code:
        raise ValueError("Must provide a system code, e.g. 'L'.")
    if system_code not in _CODE_MAP:
        raise ValueError("Unsupported system code; see BridgeDb datasources.")

    url = _BASE_URL.format(pathway=pathway)

    try:
        with urllib.request.urlopen(url) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Failed to retrieve TSV data ({exc.code}).") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError("Failed to retrieve TSV data (network error).") from exc

    column = _CODE_MAP[system_code]
    reader = csv.DictReader(io.StringIO(raw), delimiter="\t")
    if not reader.fieldnames or column not in reader.fieldnames:
        raise RuntimeError(
            f"Column '{column}' is not present in the downloaded TSV file."
        )

    values: List[str] = []
    for row in reader:
        raw_value = row.get(column)
        if not raw_value:
            continue
        for item in raw_value.split(";"):
            item = item.strip()
            if item:
                values.append(item)

    unique_values = _unique_preserve_order(values)

    if not compact:
        unique_values = [re.sub(r".*:", "", value) for value in unique_values]

    return unique_values
