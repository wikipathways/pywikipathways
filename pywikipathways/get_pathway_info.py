import requests
import pandas

def get_pathway_info(pathway=None):
    """Get Pathway Info
    
    Retrieve information for a specific pathway or all pathways.
    
    Args:
        pathway (str, optional): WikiPathways identifier (WPID) for the pathway, 
                               e.g. WP554. If None, then all pathways are returned.
    
    Returns:
        pandas.DataFrame: A dataframe of pathway WPID, URL, name, species, revision,
                         authors, description, and other pathway information.
                         Returns None if no results or on error.
    
    Examples:
        >>> get_pathway_info('WP554')
        >>> get_pathway_info()  # Returns all pathways
    """
    try:
        # Fetch the static JSON file containing all pathway info data
        response = requests.get('https://www.wikipathways.org/json/getPathwayInfo.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None
            
        pathway_info = data['pathwayInfo']
        
        # Convert to DataFrame 
        df = pandas.DataFrame(pathway_info)
        
        # Filter by specific pathway if provided
        if pathway is not None:
            filtered_df = df[df['id'] == pathway]
            if len(filtered_df) == 0:
                print(f"No pathway found with ID: {pathway}")
                return None
            return filtered_df.reset_index(drop=True)
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def get_pathway_info_ids(pathway=None):
    """Get Pathway Info IDs
    
    Retrieve list of pathway IDs for a specific pathway or all pathways.
    
    Args:
        pathway (str, optional): WikiPathways identifier (WPID) for the pathway, 
                               e.g. WP554. If None, then all pathway IDs are returned.
    
    Returns:
        pandas.Series or None: A series of pathway IDs, or None if no results.
    """
    res = get_pathway_info(pathway)
    if res is None:
        return None
    return res['id']

def get_pathway_info_names(pathway=None):
    """Get Pathway Info Names
    
    Retrieve list of pathway names for a specific pathway or all pathways.
    
    Args:
        pathway (str, optional): WikiPathways identifier (WPID) for the pathway, 
                               e.g. WP554. If None, then all pathway names are returned.
    
    Returns:
        pandas.Series or None: A series of pathway names, or None if no results.
    """
    res = get_pathway_info(pathway)
    if res is None:
        return None
    return res['name']

def get_pathway_info_urls(pathway=None):
    """Get Pathway Info URLs
    
    Retrieve list of pathway URLs for a specific pathway or all pathways.
    
    Args:
        pathway (str, optional): WikiPathways identifier (WPID) for the pathway, 
                               e.g. WP554. If None, then all pathway URLs are returned.
    
    Returns:
        pandas.Series or None: A series of pathway URLs, or None if no results.
    """
    res = get_pathway_info(pathway)
    if res is None:
        return None
    return res['url']
