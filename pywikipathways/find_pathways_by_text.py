from .utilities import *


def find_pathways_by_text(query, field=None):
    """Find Pathways By Text

    Retrieve pathways matching the query text from the static JSON endpoint.

    Args:
        query (str): A character string to search for, e.g., "cancer". Case insensitive.
        field (str, optional): Restrict search to a single field, e.g., id, name,
            description, species, revision, authors, datanodes, annotations, or citedIn.

    Returns:
        pandas.DataFrame or None: A dataframe of pathway attributes including the
            matching attributes, or None if no results are found or on error.

    Details:
        Searches id, name, description, species, revision date, authors,
        datanode labels, ontology annotations, and citedIn (e.g., PMCIDs).

    Examples:
        >>> find_pathways_by_text('cancer')
        >>> find_pathways_by_text('cancer', 'name')
    """
    if query is None:
        raise ValueError("Must provide a query, e.g., 'ACE2'")

    if isinstance(query, (list, tuple, set)):
        query_terms = [str(term).lower() for term in query]
    else:
        query_terms = [str(query).lower()]

    try:
        response = requests.get('https://www.wikipathways.org/json/findPathwaysByText.json')
        response.raise_for_status()
        data = response.json()

        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None

        df = pandas.DataFrame(data['pathwayInfo']).reset_index(drop=True)
        if df.empty:
            print("No pathways available in dataset")
            return None

        if field is not None and field not in df.columns:
            raise ValueError("Must provide a supported field, e.g., 'name'")

        if field is None and {'id', 'citedIn'}.issubset(df.columns):
            start_idx = df.columns.get_loc('id')
            end_idx = df.columns.get_loc('citedIn') + 1
            search_columns = df.columns[start_idx:end_idx]
        elif field is None:
            search_columns = df.columns
        else:
            search_columns = [field]

        search_frame = df[search_columns].fillna('').astype(str)

        match_mask = pandas.Series(False, index=df.index)
        if field is None:
            lower_frame = search_frame.map(lambda value: value.lower())
            row_strings = lower_frame.apply(lambda row: ' '.join(row), axis=1)
            for term in query_terms:
                match_mask |= row_strings.str.contains(term, na=False, regex=False)
        else:
            column_series = search_frame[field].str.lower()
            for term in query_terms:
                match_mask |= column_series.str.contains(term, na=False, regex=False)

        filtered_df = df[match_mask]
        if filtered_df.empty:
            print("No results")
            return None

        return filtered_df.reset_index(drop=True)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except ValueError:
        raise
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
