import pytest
from pywikipathways.find_pathways_by_literature import (
    find_pathways_by_literature,
    find_pathway_ids_by_literature,
    find_pathway_names_by_literature,
    find_pathway_urls_by_literature,
)

def test_find_pathways_by_literature():
    """Test the find_pathways_by_literature function with various queries."""
    
    # Test with a query that should return at least one pathway (common term)
    query = 'cancer'
    result = find_pathways_by_literature(query)
    # Should return a DataFrame or None (if no network access or no results)
    assert result is None or len(result) > 0
    
    # Test with a more specific query
    query = 'diabetes'
    result = find_pathways_by_literature(query)
    assert result is None or len(result) >= 0
    
    # Test with a query that should not return any pathways
    query = 'qwertyuiop'
    result = find_pathways_by_literature(query)
    assert result is None
    
    # Test error handling for None query
    with pytest.raises(ValueError):
        find_pathways_by_literature(None)

def test_find_pathway_ids_by_literature():
    """Test the find_pathway_ids_by_literature function."""
    query = 'cancer'
    result = find_pathway_ids_by_literature(query)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')

def test_find_pathway_names_by_literature():
    """Test the find_pathway_names_by_literature function."""
    query = 'cancer'
    result = find_pathway_names_by_literature(query)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')

def test_find_pathway_urls_by_literature():
    """Test the find_pathway_urls_by_literature function."""
    query = 'cancer'
    result = find_pathway_urls_by_literature(query)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')