import pytest
from pywikipathways.list_pathways import list_pathways

def test_list_pathways():
    # pathways are found
    pathways = list_pathways()
    assert len(pathways) > 0

    # Anopheles gambiae pathways are found
    pathways = list_pathways(organism="Anopheles gambiae")
    assert len(pathways) > 0
