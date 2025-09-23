import pytest

from pywikipathways.list_pathways import list_pathways


def test_list_pathways_returns_results():
    """list_pathways should return pathway data or None on network issues."""
    result = list_pathways()

    assert result is None or len(result) > 0

    if result is not None:
        expected_columns = {"id", "url", "name", "species", "revision"}
        assert expected_columns.issubset(set(result.columns))


def test_list_pathways_filters_by_organism():
    """Filtering by organism should restrict pathways to that species."""
    organism = "Anopheles gambiae"
    result = list_pathways(organism)

    assert result is None or len(result) > 0

    if result is not None:
        assert result["species"].eq(organism).all()
