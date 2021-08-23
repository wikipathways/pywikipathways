import pandas

def list_pathways(organism=""):
    res = wikipathways_get('listpathways', {'organism' = organism, 'format': 'json'})
    if 'pathways' in res.keys():
        return(pandas.DataFrame(res['pathways']))
    else:
        print("No results")
