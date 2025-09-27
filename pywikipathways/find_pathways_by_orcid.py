import requests

def find_pathways_by_orcid(orcid):
    """Find Pathways By ORCID
    
    Retrieve pathways containing the query ORCID from a static JSON endpoint.
    
    Args:
        orcid (str): The ORCID identifier to search for, e.g., '0000-0001-9773-4008'.
    
    Returns:
        pandas.DataFrame: A dataframe of pathway attributes including the matching
                         ORCIDs, or None if no results.
    """
    if orcid is None:
        raise ValueError("Must provide an ORCID, e.g., '0000-0001-9773-4008'")
    
    try:
        # Fetch the static JSON file containing all pathway ORCID data
        response = requests.get('https://www.wikipathways.org/json/findPathwaysByOrcid.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None
            
        pathway_info = data['pathwayInfo']
        
        # Filter pathways that contain the query ORCID in the orcids field
        orcid_lower = orcid.lower()
        filtered_pathways = []
        
        for pathway in pathway_info:
            # Check if ORCID matches in the orcids field
            orcids_value = pathway.get('orcids')
            if orcids_value is not None:
                orcids_str = str(orcids_value).lower()
                if orcid_lower in orcids_str:
                    filtered_pathways.append(pathway)
        
        if len(filtered_pathways) == 0:
            print(f"No pathways found for ORCID: {orcid}")
            return None
            
        # Convert to DataFrame and return
        return pandas.DataFrame(filtered_pathways).drop_duplicates(ignore_index=True)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def find_pathway_ids_by_orcid(orcid):
    """Find Pathway IDs By ORCID
    
    Retrieve list of pathway IDs containing the query ORCID.
    
    Args:
        orcid (str): The ORCID identifier to search for, e.g., '0000-0001-9773-4008'.
    
    Returns:
        pandas.Series or None: A series of pathway IDs, or None if no results.
    """
    res = find_pathways_by_orcid(orcid)
    if res is None:
        return None
    return res['id']

def find_pathway_names_by_orcid(orcid):
    """Find Pathway Names By ORCID
    
    Retrieve list of pathway names containing the query ORCID.
    
    Args:
        orcid (str): The ORCID identifier to search for, e.g., '0000-0001-9773-4008'.
    
    Returns:
        pandas.Series or None: A series of pathway names, or None if no results.
    """
    res = find_pathways_by_orcid(orcid)
    if res is None:
        return None
    return res['name']

def find_pathway_urls_by_orcid(orcid):
    """Find Pathway URLs By ORCID
    
    Retrieve list of pathway URLs containing the query ORCID.
    
    Args:
        orcid (str): The ORCID identifier to search for, e.g., '0000-0001-9773-4008'.
    
    Returns:
        pandas.Series or None: A series of pathway URLs, or None if no results.
    """
    res = find_pathways_by_orcid(orcid)
    if res is None:
        return None
    return res['url']