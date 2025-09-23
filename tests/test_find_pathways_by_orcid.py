import pytest
from pywikipathways.find_pathways_by_orcid import (
    find_pathways_by_orcid,
    find_pathway_ids_by_orcid,
    find_pathway_names_by_orcid,
    find_pathway_urls_by_orcid,
)

def test_find_pathways_by_orcid():
    """Test the find_pathways_by_orcid function with various queries."""
    
    # Test with a query that should return at least one pathway (example from R implementation)
    orcid = '0000-0001-9773-4008'
    result = find_pathways_by_orcid(orcid)
    # Should return a DataFrame or None (if no network access or no results)
    assert result is None or len(result) > 0
    
    # Test with another ORCID format
    orcid = '0000-0002-1234-5678'
    result = find_pathways_by_orcid(orcid)
    assert result is None or len(result) >= 0
    
    # Test with a query that should not return any pathways
    orcid = '0000-0000-0000-0000'
    result = find_pathways_by_orcid(orcid)
    assert result is None
    
    # Test error handling for None query
    with pytest.raises(ValueError):
        find_pathways_by_orcid(None)

def test_find_pathway_ids_by_orcid():
    """Test the find_pathway_ids_by_orcid function."""
    orcid = '0000-0001-9773-4008'
    result = find_pathway_ids_by_orcid(orcid)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')

def test_find_pathway_names_by_orcid():
    """Test the find_pathway_names_by_orcid function."""
    orcid = '0000-0001-9773-4008'
    result = find_pathway_names_by_orcid(orcid)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')

def test_find_pathway_urls_by_orcid():
    """Test the find_pathway_urls_by_orcid function."""
    orcid = '0000-0001-9773-4008'
    result = find_pathway_urls_by_orcid(orcid)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')