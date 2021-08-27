from .utilities import *

def list_pathways(organism=""):
    """List Pathways
    
    Retrieve list of pathways per species, including WPID, name,
    species, URL and latest revision number.
    
    Args:
        organism (str): A particular species.
    
    Returns:
        pandas.DataFrame: A dataframe of pathway information.
        
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
        pandas.Series: A series of WPIDs.
        
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
    """List Pathway Names
    
    Retrieve list of pathway names per species.
    Basically returns a subset of list_pathways result.
    
    Args:
        organism (str): A particular species.
    
    Returns:
        pandas.Series: A series of names.
        
    Examples:
        >>> list_pathway_names('Mus musculus')
        0                            Statin pathway
        1                    IL-9 signaling pathway
        2                  Cholesterol biosynthesis
        3      Selenium metabolism / selenoproteins
        4                TGF-beta signaling pathway
                               ...                 
        230                   Tryptophan metabolism
        231                          Focal adhesion
        232                   Nucleotide metabolism
        233            Toll-like receptor signaling
        234                  IL-4 signaling pathway
        Name: name, Length: 235, dtype: object
    """
    res = list_pathways(organism)
    return res['name']

def list_pathway_urls(organism=""):
    """List Pathway URLs
    
    Retrieve list of pathway URLs per species.
    Basically returns a subset of list_pathways result.
    
    Args:
        organism (str): A particular species.
    
    Returns:
        pandas.Series: A series of URLs.
        
    Examples:
        >>> list_pathway_urls('Mus musculus')
        0      https://www.wikipathways.org/index.php/Pathway...
        1      https://www.wikipathways.org/index.php/Pathway...
        2      https://www.wikipathways.org/index.php/Pathway...
        3      https://www.wikipathways.org/index.php/Pathway...
        4      https://www.wikipathways.org/index.php/Pathway...
                                     ...                        
        230    https://www.wikipathways.org/index.php/Pathway...
        231    https://www.wikipathways.org/index.php/Pathway...
        232    https://www.wikipathways.org/index.php/Pathway...
        233    https://www.wikipathways.org/index.php/Pathway...
        234    https://www.wikipathways.org/index.php/Pathway...
        Name: url, Length: 235, dtype: object
    """
    res = list_pathways(organism)
    return res['url']
