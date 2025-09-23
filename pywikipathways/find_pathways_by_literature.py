from .utilities import *

def find_pathways_by_literature(query):
    """Find Pathways By Literature
    
    Retrieve pathways containing the query citation from a static JSON endpoint.
    
    Args:
        query (str): The character string to search for, e.g., a PMID, title 
                    keyword, journal abbreviation, year, or author name.
    
    Returns:
        pandas.DataFrame: A dataframe of pathway attributes including the matching
                         citations, or None if no results.
    """
    if query is None:
        raise ValueError("Must provide a query, e.g., '15134803' or 'Schwartz GL'")
    
    try:
        # Fetch the static JSON file containing all pathway literature data
        response = requests.get('https://www.wikipathways.org/json/findPathwaysByLiterature.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None
            
        pathway_info = data['pathwayInfo']
        
        # Filter pathways that contain the query in any literature-related field
        query_lower = query.lower()
        filtered_pathways = []
        
        for pathway in pathway_info:
            # Check if query matches any literature-related fields
            match_found = False
            
            # Check all fields that might contain literature information
            # Based on R implementation, we check from 'refs' to 'citations' columns
            for key, value in pathway.items():
                if value is not None:
                    # Convert value to string and check for match
                    value_str = str(value).lower()
                    if query_lower in value_str:
                        match_found = True
                        break
            
            if match_found:
                filtered_pathways.append(pathway)
        
        if len(filtered_pathways) == 0:
            print("No results")
            return None
            
        # Convert to DataFrame and return
        return pandas.DataFrame(filtered_pathways)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def find_pathway_ids_by_literature(query):
    """Find Pathway IDs By Literature
    
    Retrieve list of pathway IDs containing the query citation.
    
    Args:
        query (str): The character string to search for, e.g., a PMID, title 
                    keyword or author name.
    
    Returns:
        pandas.Series or None: A series of pathway IDs, or None if no results.
    """
    res = find_pathways_by_literature(query)
    if res is None:
        return None
    return res['id']

def find_pathway_names_by_literature(query):
    """Find Pathway Names By Literature
    
    Retrieve list of pathway names containing the query citation.
    
    Args:
        query (str): The character string to search for, e.g., a PMID, title 
                    keyword or author name.
    
    Returns:
        pandas.Series or None: A series of pathway names, or None if no results.
    """
    res = find_pathways_by_literature(query)
    if res is None:
        return None
    return res['name']

def find_pathway_urls_by_literature(query):
    """Find Pathway URLs By Literature
    
    Retrieve list of pathway URLs containing the query citation.
    
    Args:
        query (str): The character string to search for, e.g., a PMID, title 
                    keyword or author name.
    
    Returns:
        pandas.Series or None: A series of pathway URLs, or None if no results.
    """
    res = find_pathways_by_literature(query)
    if res is None:
        return None
    return res['url']
