from .utilities import *

def find_pathways_by_text(query, field=None):
    """Find Pathways By Text
    
    Retrieve pathways matching the query text from a static JSON endpoint.
    
    Args:
        query (str): A character string to search for, e.g., "cancer". Case insensitive.
        field (str, optional): Optional character string to restrict search to a single
                             field, e.g., id, name, description, species, revision, authors,
                             datanodes, annotations, or citedIn.
    
    Returns:
        pandas.DataFrame: A dataframe of pathway attributes including the matching
                         attributes, or None if no results.
    
    Details:
        Searches id, name, description, species, revision date, authors,
        datanode labels, ontology annotations, and citedIn (e.g., PMCIDs).
    
    Examples:
        >>> find_pathways_by_text('cancer')
        >>> find_pathways_by_text('cancer', 'name')
    """
    if query is None:
        raise ValueError("Must provide a query, e.g., 'cancer'")
    
    try:
        # Fetch the static JSON file containing all pathway text data
        response = requests.get('https://www.wikipathways.org/json/findPathwaysByText.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None
            
        pathway_info = data['pathwayInfo']
        
        # Convert to DataFrame first to get consistent structure
        df = pandas.DataFrame(pathway_info)
        
        if len(df) == 0:
            print("No pathways available in dataset")
            return None
        
        # Check if field parameter is valid
        if field is not None and field not in df.columns:
            available_fields = ', '.join(df.columns)
            raise ValueError(f"Must provide a supported field, e.g., name. Available fields: {available_fields}")
        
        # Filter pathways that contain the query
        query_lower = query.lower()
        
        if field is None:
            # Search across all fields - get boolean mask for each row
            mask = df.astype(str).apply(
                lambda row: any(query_lower in str(val).lower() for val in row), 
                axis=1
            )
        else:
            # Search only in the specified field
            mask = df[field].astype(str).str.lower().str.contains(query_lower, na=False)
        
        # Filter the dataframe
        filtered_df = df[mask].copy()
        
        if len(filtered_df) == 0:
            print("No results")
            return None
            
        # Reset index and return
        return filtered_df.reset_index(drop=True)
        
    except ValueError:
        # Re-raise ValueError (for invalid inputs)
        raise
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def find_pathway_ids_by_text(query, field=None):
    """Find Pathway WPIDs By Text 
    
    Retrieve list of pathway WPIDs containing the query text.
    
    Args:
        query (str): A character string to search for, e.g., "cancer"
        field (str, optional): Optional character string to restrict search to a single
                             field, e.g., name, description, id, species, revision, authors,
                             datanodes, annotations, or citedIn.
    
    Returns:
        pandas.Series or None: A series of WPIDs, or None if no results.
    
    Examples:
        >>> find_pathway_ids_by_text('cancer')
    """
    res = find_pathways_by_text(query, field)
    if res is None:
        return None
    return res['id']

def find_pathway_names_by_text(query, field=None):
    """Find Pathway Names By Text 
    
    Retrieve list of pathway names containing the query text.
    
    Args:
        query (str): A character string to search for, e.g., "cancer"
        field (str, optional): Optional character string to restrict search to a single
                             field, e.g., name, description, id, species, revision, authors,
                             datanodes, annotations, or citedIn.
    
    Returns:
        pandas.Series or None: A series of pathway names, or None if no results.
    
    Examples:
        >>> find_pathway_names_by_text('cancer')
    """
    res = find_pathways_by_text(query, field)
    if res is None:
        return None
    return res['name']

def find_pathway_urls_by_text(query, field=None):
    """Find Pathway URLs By Text 
    
    Retrieve list of pathway URLs containing the query text.
    
    Args:
        query (str): A character string to search for, e.g., "cancer"
        field (str, optional): Optional character string to restrict search to a single
                             field, e.g., name, description, id, species, revision, authors,
                             datanodes, annotations, or citedIn.
    
    Returns:
        pandas.Series or None: A series of URLs, or None if no results.
    
    Examples:
        >>> find_pathway_urls_by_text('cancer')
    """
    res = find_pathways_by_text(query, field)
    if res is None:
        return None
    return res['url']
