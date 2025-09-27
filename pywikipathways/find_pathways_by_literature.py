import requests
import pandas

def find_pathways_by_literature(query):
    """Find Pathways By Literature

    Retrieve pathways containing the query citation from the static JSON
    endpoint used by WikiPathways.

    Args:
        query (str): The character string to search for, e.g., a PMID, title
            keyword, journal abbreviation, year, or author name.

    Returns:
        pandas.DataFrame or None: A dataframe of pathway attributes including the
            matching citations, or None if no results are found or on error.
    """
    if query is None:
        raise ValueError("Must provide a query, e.g., '15134803' or 'Schwartz GL'")

    query_lower = str(query).lower()

    try:
        response = requests.get('https://www.wikipathways.org/json/findPathwaysByLiterature.json')
        response.raise_for_status()
        data = response.json()

        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None

        df = pandas.DataFrame(data['pathwayInfo']).reset_index(drop=True)
        if df.empty:
            print("No results")
            return None

        search_columns = [col for col in ['refs', 'citations'] if col in df.columns]
        if not search_columns:
            print("API response missing literature fields to search")
            return None

        match_mask = pandas.Series(False, index=df.index)
        for col in search_columns:
            column_values = df[col].fillna('')
            column_strings = column_values.astype(str).str.lower()
            match_mask |= column_strings.str.contains(query_lower, na=False, regex=False)

        filtered_df = df[match_mask]
        if filtered_df.empty:
            print(f"No pathways found matching query: {query}")
            return None

        return filtered_df.reset_index(drop=True)

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
