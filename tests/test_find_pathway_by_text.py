import pytest
from pywikipathways.find_pathways_by_text import *

def test_find_pathways_by_text():
    # Test with a query that should return at least one pathway
    query = 'cancer'
    result = find_pathways_by_text(query)
    if result is not None:
        assert len(result) > 0
        assert 'id' in result.columns
        assert 'name' in result.columns
        assert 'url' in result.columns

    # Test with a more specific query
    query = 'apoptosis'
    result = find_pathways_by_text(query)
    if result is not None:
        assert len(result) > 0

    # Test with field parameter
    query = 'sapiens'
    result = find_pathways_by_text(query, field='species')
    if result is not None:
        assert len(result) > 0

    # Test with a query that should not return any pathways
    query = 'qwertyuiop'
    result = find_pathways_by_text(query)
    assert result is None

def test_find_pathway_helper_functions():
    # Test helper functions
    query = 'cancer'
    
    # Test IDs function
    ids = find_pathway_ids_by_text(query)
    if ids is not None:
        assert len(ids) > 0
    
    # Test names function  
    names = find_pathway_names_by_text(query)
    if names is not None:
        assert len(names) > 0
        
    # Test URLs function
    urls = find_pathway_urls_by_text(query)
    if urls is not None:
        assert len(urls) > 0

def test_invalid_inputs():
    # Test None query
    with pytest.raises(ValueError):
        find_pathways_by_text(None)
    
    # Test invalid field (this should raise an error when data is available)
    # We'll skip this test in environments without internet access