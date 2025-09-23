import requests
import pandas


def get_counts():
    """Get Counts for WikiPathways Stats
    
    Retrieve information about various total counts at WikiPathways.
    
    Returns:
        pandas.DataFrame: A dataframe of counts including pathways, authors, 
                         organisms, and other WikiPathways statistics.
                         Returns None if no results or on error.
    
    Examples:
        >>> get_counts()
    """
    try:
        # Fetch the static JSON file containing counts data
        response = requests.get('https://www.wikipathways.org/json/getCounts.json')
        response.raise_for_status()
        data = response.json()
        
        # Convert to DataFrame - the JSON response should contain count statistics
        df = pandas.DataFrame([data])
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None