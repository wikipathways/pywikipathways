import pytest
from pywikipathways.get_pathway_info import get_pathway_info

def test_get_pathway_info():
    """Test the get_pathway_info function."""    
    # get WP554
    info = get_pathway_info("WP554")
    assert info['id'][0] == 'WP554'
    
    # get WP554 (again)
    info = get_pathway_info(pathway="WP554")
    assert info['id'][0] == 'WP554'
    