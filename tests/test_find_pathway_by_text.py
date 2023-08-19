#from find_pathway_by_text import find_pathways_by_text
import pytest
from pywikipathways.find_pathway_by_text import *

def test_find_pathways_by_text():
    # Test with a query that should return at least one pathway
    query = 'cancer'
    result = find_pathways_by_text(query)
    assert len(result) > 0

    # Test with a query that should not return any pathways
    query = 'qwertyuiop'
    result = find_pathways_by_text(query)
    assert result is None