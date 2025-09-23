import pytest
from pywikipathways.find_pathways_by_text import *

def test_find_pathways_by_text():
    # find by keyword
    pathways = find_pathways_by_text("cancer")
    assert len(pathways) > 0

    # find by datanode label (again)
    pathways = find_pathways_by_text(query="5-FU")
    assert len(pathways) > 0

    # find by multiple keywords
    pathways = find_pathways_by_text(query=["cancer", "5-FU"])
    assert len(pathways) > 0