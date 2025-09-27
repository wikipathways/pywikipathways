"""Tests for the get_xref_list wrapper."""

import pytest

from pywikipathways.get_xref_list import get_xref_list


def test_get_xref_list_contains_known_uniprot():
    """WP2338 should include a known UniProt identifier."""
    try:
        xrefs = get_xref_list("WP2338", "S")
    except RuntimeError:
        pytest.skip("WikiPathways endpoint unavailable.")

    assert isinstance(xrefs, list)
    assert "Q15633" in xrefs


def test_get_xref_list_keyword_arguments():
    """Keyword invocation should match positional behaviour."""
    try:
        xrefs = get_xref_list(pathway="WP2338", system_code="S")
    except RuntimeError:
        pytest.skip("WikiPathways endpoint unavailable.")

    assert "Q15633" in xrefs
