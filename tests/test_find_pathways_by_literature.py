import pytest
from pywikipathways.find_pathways_by_literature import (
    find_pathways_by_literature,
    find_pathway_ids_by_literature,
    find_pathway_names_by_literature,
    find_pathway_urls_by_literature,
)

def test_find_pathways_by_literature():
    """Test the find_pathways_by_literature function with various queries."""
    
    # find by keyword
    pathways = find_pathways_by_literature("cancer")
    assert len(pathways) > 0
    
    # find by pmid (again)
    pathways = find_pathways_by_literature(query="10423528")
    assert len(pathways) > 0

    # find by author
    pathways = find_pathways_by_literature(query="smith")
    assert len(pathways) > 0