import pytest
from pywikipathways.get_ontology_terms import (
    get_ontology_terms,
    get_pathways_by_ontology_term,
    get_pathways_by_parent_ontology_term,
)

def test_get_ontology_terms():
    # get by WPID
    terms = get_ontology_terms('WP554')
    assert len(terms) > 0

def test_get_pathways_by_ontology_term():
    # find by ontology term
    pathways = get_pathways_by_ontology_term('PW:0000002')
    assert len(pathways) > 0

def test_get_pathways_by_parent_ontology_term():
    # find by parent ontology term
    pathways = get_pathways_by_parent_ontology_term('signaling pathway')
    assert len(pathways) > 0
    