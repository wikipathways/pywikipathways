from .utilities import *

def list_pathways(organism=""):
    """List Pathways
    
    Retrieve list of pathways per species, including WPID, name,
    species, URL and latest revision number.
    
    Args:
        organism (str): A particular species.
    
    Returns:
        dataframe: A dataframe of pathway information.
        
    Examples:
        >>> list_pathways('Mus musculus')
    
    """
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
