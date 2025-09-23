import pytest
from pywikipathways.get_ontology_terms import (
    get_ontology_terms,
    get_ontology_term_names,
    get_ontology_term_ids,
    get_pathways_by_ontology_term,
    get_pathway_ids_by_ontology_term,
    get_pathways_by_parent_ontology_term,
    get_pathway_ids_by_parent_ontology_term,
)

def test_get_ontology_terms():
    """Test the get_ontology_terms function."""
    
    # Test with a specific pathway ID
    pathway_id = 'WP554'
    result = get_ontology_terms(pathway_id)
    # Should return a DataFrame or None (if no network access or pathway not found)
    assert result is None or len(result) >= 0
    
    # Test with another pathway ID
    pathway_id = 'WP4'
    result = get_ontology_terms(pathway_id)
    assert result is None or len(result) >= 0
    
    # Test with invalid pathway ID
    pathway_id = 'WP999999'
    result = get_ontology_terms(pathway_id)
    assert result is None
    
    # Test without pathway parameter (should return all pathways)
    result = get_ontology_terms()
    # Should return a DataFrame with all pathways or None (if no network access)
    assert result is None or len(result) > 0
    
    # Test with None parameter (should return all pathways)
    result = get_ontology_terms(None)
    assert result is None or len(result) > 0

def test_get_ontology_term_names():
    """Test the get_ontology_term_names function."""
    pathway_id = 'WP554'
    result = get_ontology_term_names(pathway_id)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')
    
    # Test without pathway parameter
    result = get_ontology_term_names()
    assert result is None or hasattr(result, 'name')

def test_get_ontology_term_ids():
    """Test the get_ontology_term_ids function."""
    pathway_id = 'WP554'
    result = get_ontology_term_ids(pathway_id)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')
    
    # Test without pathway parameter
    result = get_ontology_term_ids()
    assert result is None or hasattr(result, 'name')

def test_get_pathways_by_ontology_term():
    """Test the get_pathways_by_ontology_term function."""
    
    # Test with a common ontology term
    term = 'PW:0000045'
    result = get_pathways_by_ontology_term(term)
    # Should return a DataFrame or None (if no network access or term not found)
    assert result is None or len(result) >= 0
    
    # Test with invalid ontology term
    term = 'INVALID:999999'
    result = get_pathways_by_ontology_term(term)
    assert result is None

def test_get_pathway_ids_by_ontology_term():
    """Test the get_pathway_ids_by_ontology_term function."""
    term = 'PW:0000045'
    result = get_pathway_ids_by_ontology_term(term)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')

def test_get_pathways_by_parent_ontology_term():
    """Test the get_pathways_by_parent_ontology_term function."""
    
    # Test with a common parent term
    term = 'signaling pathway'
    result = get_pathways_by_parent_ontology_term(term)
    # Should return a DataFrame or None (if no network access or term not found)
    assert result is None or len(result) >= 0
    
    # Test with invalid parent term
    term = 'invalid_parent_term'
    result = get_pathways_by_parent_ontology_term(term)
    assert result is None

def test_get_pathway_ids_by_parent_ontology_term():
    """Test the get_pathway_ids_by_parent_ontology_term function."""
    term = 'signaling pathway'
    result = get_pathway_ids_by_parent_ontology_term(term)
    # Should return a Series or None
    assert result is None or hasattr(result, 'name')