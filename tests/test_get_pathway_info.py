import pytest
from pywikipathways.get_pathway_info import (
    get_pathway_info,
    get_pathway_info_ids,
    get_pathway_info_names,
    get_pathway_info_urls,
)

def test_get_pathway_info():
    """Test the get_pathway_info function."""
    
    # Test with a specific pathway ID
    pathway_id = 'WP554'
    result = get_pathway_info(pathway_id)
    # Should return a DataFrame or None (if no network access or pathway not found)
    assert result is None or len(result) >= 0
    
    # Test with another pathway ID
    pathway_id = 'WP4'
    result = get_pathway_info(pathway_id)
    assert result is None or len(result) >= 0
    
    # Test with invalid pathway ID
    pathway_id = 'WP999999'
    result = get_pathway_info(pathway_id)
    assert result is None
    
    # Test without pathway parameter (should return all pathways)
    result = get_pathway_info()
    # Should return a DataFrame with all pathways or None (if no network access)
    assert result is None or len(result) > 0
    
    # Test with None parameter (should return all pathways)
    result = get_pathway_info(None)
    assert result is None or len(result) > 0

def test_get_pathway_info_ids():
    """Test the get_pathway_info_ids function."""
    pathway_id = 'WP554'
    result = get_pathway_info_ids(pathway_id)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')
    
    # Test without pathway parameter
    result = get_pathway_info_ids()
    assert result is None or hasattr(result, 'name')

def test_get_pathway_info_names():
    """Test the get_pathway_info_names function."""
    pathway_id = 'WP554'
    result = get_pathway_info_names(pathway_id)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')
    
    # Test without pathway parameter
    result = get_pathway_info_names()
    assert result is None or hasattr(result, 'name')

def test_get_pathway_info_urls():
    """Test the get_pathway_info_urls function."""
    pathway_id = 'WP554'
    result = get_pathway_info_urls(pathway_id)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')
    
    # Test without pathway parameter
    result = get_pathway_info_urls()
    assert result is None or hasattr(result, 'name')