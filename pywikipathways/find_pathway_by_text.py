from .utilities import *

def find_pathways_by_text(query):
    res = wikipathways_get('findPathwaysByText', {'query': query, 'format': 'json'})
    tmp = pandas.DataFrame(res['result'])
    score = tmp['score'].apply(lambda x: x['0'])
    tmp['score'] = score
    return tmp.drop(['fields'], axis=1).drop_duplicates(ignore_index=True)

def find_pathway_ids_by_text(query):
    res = find_pathways_by_text(query)
    return res['id']

def find_pathway_names_by_text(query):
    res = find_pathways_by_text(query)
    return res['name']

def find_pathway_urls_by_text(query):
    res = find_pathways_by_text(query)
    return res['url']
