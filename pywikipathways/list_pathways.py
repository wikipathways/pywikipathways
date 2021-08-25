from .utilities import *

def list_pathways(organism=""):
    res = wikipathways_get('listpathways', {'organism':  organism, 'format': 'json'})
    if 'pathways' in res.keys():
        return pandas.DataFrame(res['pathways'])
    else:
        print("No results")

def list_pathway_ids(organism=""):
    res = list_pathways(organism)
    return res['id']

def list_pathway_names(organism=""):
    res = list_pathways(organism)
    return res['name']

def list_pathway_urls(organism=""):
    res = list_pathways(organism)
    return res['url']
