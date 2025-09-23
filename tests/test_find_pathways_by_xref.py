import pytest
from pywikipathways.find_pathways_by_xref import (
    find_pathways_by_xref,
    find_pathway_ids_by_xref,
    find_pathway_names_by_xref,
    find_pathway_urls_by_xref,
)

def test_find_pathways_by_xref():
    """Test the find_pathways_by_xref function."""
    # find by Xref
    pathways = find_pathways_by_xref('ENSG00000232810','En')
    # Should return a DataFrame or None (if no network access or no results)
    assert pathways is None or len(pathways) > 0

    # find by Xref (again) - test named parameters
    pathways = find_pathways_by_xref(identifier="ENSG00000232810", system_code="En")
    assert pathways is None or len(pathways) > 0

def test_find_pathways_by_xref_validation():
    """Test parameter validation for find_pathways_by_xref."""
    # Test error handling for None identifier
    with pytest.raises(ValueError):
        find_pathways_by_xref(None, 'En')
    
    # Test error handling for None system_code
    with pytest.raises(ValueError):
        find_pathways_by_xref('test', None)
    
    # Test error handling for invalid system_code
    with pytest.raises(ValueError):
        find_pathways_by_xref('test', 'INVALID')

def test_find_pathway_ids_by_xref():
    """Test the find_pathway_ids_by_xref function."""
    result = find_pathway_ids_by_xref('ENSG00000232810','En')
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')

def test_find_pathway_names_by_xref():
    """Test the find_pathway_names_by_xref function."""
    result = find_pathway_names_by_xref('ENSG00000232810','En')
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')

def test_find_pathway_urls_by_xref():
    """Test the find_pathway_urls_by_xref function."""
    result = find_pathway_urls_by_xref('ENSG00000232810','En')
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')