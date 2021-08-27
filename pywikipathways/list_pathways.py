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
            id	url	name	species	revision
        0	WP1	https://www.wikipathways.org/index.php/Pathway...	Statin pathway	Mus musculus	117947
        1	WP10	https://www.wikipathways.org/index.php/Pathway...	IL-9 signaling pathway	Mus musculus	117067
        2	WP103	https://www.wikipathways.org/index.php/Pathway...	Cholesterol biosynthesis	Mus musculus	116834
        3	WP108	https://www.wikipathways.org/index.php/Pathway...	Selenium metabolism / selenoproteins	Mus musculus	117940
        4	WP113	https://www.wikipathways.org/index.php/Pathway...	TGF-beta signaling pathway	Mus musculus	116497
        ...	...	...	...	...	...
        230	WP79	https://www.wikipathways.org/index.php/Pathway...	Tryptophan metabolism	Mus musculus	104913
        231	WP85	https://www.wikipathways.org/index.php/Pathway...	Focal adhesion	Mus musculus	116710
        232	WP87	https://www.wikipathways.org/index.php/Pathway...	Nucleotide metabolism	Mus musculus	116529
        233	WP88	https://www.wikipathways.org/index.php/Pathway...	Toll-like receptor signaling	Mus musculus	116521
        234	WP93	https://www.wikipathways.org/index.php/Pathway...	IL-4 signaling pathway	Mus musculus	117991
        235 rows × 5 columns
    """
    res = wikipathways_get('listpathways', {'organism':  organism, 'format': 'json'})
    if 'pathways' in res.keys():
        return pandas.DataFrame(res['pathways'])
    else:
        print("No results")

def list_pathway_ids(organism=""):
    """List Pathway WPIDs
    
    Retrieve list of pathway WPIDs per species.
    Basically returns a subset of list_pathways result.
    
    Args:
        organism (str): A particular species.
    
    Returns:
        dataframe: A dataframe of pathway information.
        
    Examples:
        >>> list_pathway_ids('Mus musculus')
        0        WP1
        1       WP10
        2      WP103
        3      WP108
        4      WP113
               ...  
        230     WP79
        231     WP85
        232     WP87
        233     WP88
        234     WP93
        Name: id, Length: 235, dtype: object
    """
    res = list_pathways(organism)
    return res['id']

def list_pathway_names(organism=""):
    res = list_pathways(organism)
    return res['name']

def list_pathway_urls(organism=""):
    res = list_pathways(organism)
    return res['url']
