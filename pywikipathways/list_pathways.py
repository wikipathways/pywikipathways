import requests
import pandas

def list_pathways(organism=""):
    """List Pathways

    Retrieve list of pathways per species, including WPID, name,
    species, URL and latest revision number.

    Args:
        organism (str): A particular species.

    Returns:
        pandas.DataFrame or None: A dataframe of pathway information, or None if
            no pathways are available for the given organism or on error.

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
    try:
        response = requests.get('https://www.wikipathways.org/json/listPathways.json')
        response.raise_for_status()
        data = response.json()

        if 'organisms' not in data:
            print("API response missing expected organisms data structure")
            return None

        pathways = []
        for organism_entry in data['organisms']:
            # Each organism entry contains a list of pathway dictionaries
            pathways.extend(organism_entry.get('pathways', []))

        if len(pathways) == 0:
            print("No results")
            return None

        df = pandas.DataFrame(pathways).reset_index(drop=True)

        if organism:
            filtered_df = df[df['species'] == organism]
            if len(filtered_df) == 0:
                print(f"No results for organism: {organism}")
                return None
            return filtered_df.reset_index(drop=True)

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

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
    if res is None:
        return None
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
    if res is None:
        return None
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
    if res is None:
        return None
    return res['url']
