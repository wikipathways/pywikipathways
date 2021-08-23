import pandas

def get_ontology_terms(pathway):
    res = wikipathways_get('getOntologyTermsByPathway', {'pwId': 'WP554', 'format': 'json'})
    return pandas.DataFrame(res['terms'])

def get_ontology_term_names(pathway):
    res = get_ontology_terms(pathway)
    return res['name']

def get_ontology_term_ids(pathway):
    res = get_ontology_terms(pathway)
    return res['id']
