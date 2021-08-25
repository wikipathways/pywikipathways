from .utilities import *

def find_pathways_by_literature(query):
    res = wikipathways_get('findPathwaysByLiterature', {'query': query, 'format': 'json'})
    dictlist = []
    for i in list(res['result'].values()):
        d = {}
        d['score'] = i['score']['0']
        d['id'] = i['id']
        d['name'] = i['name']
        d['url'] = i['url']
        d['species'] = i['species']
        d['revision'] = i['revision']
        if i['fields'].get('graphId'):
            d['graphId'] = i['fields'].get('graphId')['values']
        if i['fields'].get('literature.pubmed'):
            d['literature.pubmed'] = i['fields'].get('literature.pubmed')['values']
        if i['fields'].get('literature.title'):
            d['literature.title'] = i['fields'].get('literature.title')['values']
        dictlist.append(d)
    return pandas.DataFrame(dictlist).sort_values(by=['score'])

def find_pathway_ids_by_literature(query):
    res = find_pathways_by_literature(query)
    return res['id']

def find_pathway_names_by_literature(query):
    res = find_pathways_by_literature(query)
    return res['name']

def find_pathway_urls_by_literature(query):
    res = find_pathways_by_literature(query)
    return res['url']
