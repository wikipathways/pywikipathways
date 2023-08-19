import pytest
from pywikipathways.find_pathways_by_xref import *

def test_find_pathways_by_xref():
    # find by Xref
    pathways = find_pathways_by_xref('ENSG00000232810','En')
    assert len(pathways) > 0

    # find by Xref (again)
    pathways = find_pathways_by_xref(identifier="ENSG00000232810", system_code="En")
    assert len(pathways) > 0