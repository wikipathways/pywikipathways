from .utilities import *
from datetime import datetime

def get_recent_changes(timestamp=None):
    """Get Recent Changes
    
    Retrieve recently changed pathways at WikiPathways from a static JSON endpoint.
    
    Args:
        timestamp (str): (8 digits, YYYYMMDD) Limit by time, only pathways changed 
                        after the given date, e.g., '20180201' for changes since 
                        Feb 1st, 2018. If None, defaults to '20070301'.
    
    Returns:
        pandas.DataFrame: A dataframe of recently changed pathways, including id, name,
                         url, species and revision, or None if no results.
    """
    if timestamp is None:
        timestamp = '20070301'
    
    # Ensure timestamp is string and limit to 8 digits
    timestamp = str(timestamp)[:8]
    
    try:
        # Fetch the static JSON file containing all pathway info data
        response = requests.get('https://www.wikipathways.org/json/getPathwayInfo.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None
            
        pathway_info = data['pathwayInfo']
        
        # Filter pathways that have revision dates after the given timestamp
        filtered_pathways = []
        
        try:
            # Convert timestamp to datetime for comparison
            timestamp_date = datetime.strptime(timestamp, '%Y%m%d')
            
            for pathway in pathway_info:
                revision = pathway.get('revision')
                if revision is not None:
                    try:
                        # Convert revision date to datetime for comparison
                        revision_date = datetime.strptime(str(revision)[:8], '%Y%m%d')
                        if revision_date > timestamp_date:
                            # Remove unwanted fields like in R implementation
                            filtered_pathway = {k: v for k, v in pathway.items() 
                                              if k not in ['authors', 'description', 'citedIn']}
                            filtered_pathways.append(filtered_pathway)
                    except (ValueError, TypeError):
                        # Skip pathways with invalid revision dates
                        continue
                        
        except ValueError:
            print(f"Invalid timestamp format: {timestamp}. Expected YYYYMMDD format.")
            return None
        
        if len(filtered_pathways) == 0:
            print(f"No pathways found changed after {timestamp}")
            return None
            
        # Convert to DataFrame and return
        return pandas.DataFrame(filtered_pathways)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def get_recent_changes_ids(timestamp):
    """Get WPIDs of Recent Changes
    
    Retrieve WPIDs of recently changed pathways at WikiPathways.
    
    Args:
        timestamp (str): (8 digits, YYYYMMDD) Limit by time, only pathways changed 
                        after the given date, e.g., '20180201' for changes since 
                        Feb 1st, 2018.
    
    Returns:
        pandas.Series or None: A series of pathway IDs, or None if no results.
    """
    res = get_recent_changes(timestamp)
    if res is None:
        return None
    return res['id']

def get_recent_changes_names(timestamp):
    """Get Pathway Names of Recent Changes
    
    Retrieve names of recently changed pathways at WikiPathways.
    
    Args:
        timestamp (str): (8 digits, YYYYMMDD) Limit by time, only pathways changed 
                        after the given date, e.g., '20180201' for changes since 
                        Feb 1st, 2018.
    
    Returns:
        pandas.Series or None: A series of pathway names, or None if no results.
        Note: pathway deletions will be listed as blank names.
    """
    res = get_recent_changes(timestamp)
    if res is None:
        return None
    return res['name']
