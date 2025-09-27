import pytest
from pywikipathways.get_pathway import *

def test_get_pathway():
    "get WP554"
    gpml = get_pathway("WP554")
    assert len(gpml) > 0

    "get WP4 (again)"
    gpml = get_pathway(pathway="WP554")
    assert len(gpml) > 0

    "get a specific revision of WP554"
    gpml = get_pathway(pathway="WP554", revision=83654)
    assert len(gpml) > 0
