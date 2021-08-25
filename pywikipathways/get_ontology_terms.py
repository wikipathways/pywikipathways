from .utilities import *

def get_ontology_terms(pathway):
    res = wikipathways_get('getOntologyTermsByPathway', {'pwId': 'WP554', 'format': 'json'})
    return pandas.DataFrame(res['terms'])

def get_ontology_term_names(pathway):
    res = get_ontology_terms(pathway)
    return res['name']

def get_ontology_term_ids(pathway):
    res = get_ontology_terms(pathway)
    return res['id']

def get_pathways_by_ontology_term(term):
    res = wikipathways_get('getPathwaysByOntologyTerm', {'term': term, 'format': 'json'})
    return pandas.DataFrame(res['pathways'])

def get_pathway_ids_by_ontology_term(term):
    res = get_pathways_by_ontology_term(term)
    return res['id']

def get_pathways_by_parent_ontology_term(term):
    res = wikipathways_get('getPathwaysByParentOntologyTerm', {'term': term, 'format': 'json'})
    return pandas.DataFrame(res['pathways'])

def get_pathway_ids_by_parent_ontology_term(term):
    res = get_pathways_by_parent_ontology_term(term)
    return res['id']
