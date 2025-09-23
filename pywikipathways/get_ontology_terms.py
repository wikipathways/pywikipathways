import requests
import pandas

def get_ontology_terms(pathway=None):
    """Get Ontology Terms by Pathway
    
    Retrieve information about ontology terms for a specific pathway.
    
    Args:
        pathway (str, optional): WikiPathways identifier (WPID) for the pathway, e.g. WP554. 
                                If None, then ontology term information for all pathways is returned.
    
    Returns:
        pandas.DataFrame: A dataframe of pathway id and term information, or None if error occurs.
        
    Example:
        >>> get_ontology_terms('WP554')
        >>> get_ontology_terms()  # Get all pathways
    """
    try:
        # Fetch the static JSON file containing all pathway ontology data
        response = requests.get('https://www.wikipathways.org/json/getOntologyTermsByPathway.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathways' not in data:
            print("API response missing expected pathways data structure")
            return None
            
        pathways = data['pathways']
        
        # Flatten the nested structure - each pathway can have multiple terms
        flattened_rows = []
        for pathway_info in pathways:
            pathway_id = pathway_info.get('id')
            pathway_name = pathway_info.get('name')
            pathway_species = pathway_info.get('species')
            pathway_revision = pathway_info.get('revision')
            pathway_url = pathway_info.get('url')
            
            terms = pathway_info.get('terms', [])
            if terms:
                for term in terms:
                    flattened_row = {
                        'id': pathway_id,
                        'name': pathway_name,
                        'species': pathway_species,
                        'revision': pathway_revision,
                        'url': pathway_url,
                        'terms_id': term.get('id'),
                        'terms_name': term.get('name'),
                        'terms_parent': term.get('parent')
                    }
                    flattened_rows.append(flattened_row)
            else:
                # Include pathways with no terms
                flattened_row = {
                    'id': pathway_id,
                    'name': pathway_name,
                    'species': pathway_species,
                    'revision': pathway_revision,
                    'url': pathway_url,
                    'terms_id': None,
                    'terms_name': None,
                    'terms_parent': None
                }
                flattened_rows.append(flattened_row)
        
        if not flattened_rows:
            print("No pathway data found")
            return None
            
        # Create DataFrame
        df = pandas.DataFrame(flattened_rows)
        
        # Filter by pathway if specified
        if pathway is not None:
            df = df[df['id'] == pathway]
            if df.empty:
                print(f"No ontology terms found for pathway '{pathway}'")
                return None
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def get_ontology_term_names(pathway=None):
    """Get Ontology Term Names by Pathway
    
    Retrieve names of ontology terms for a specific pathway.
    
    Args:
        pathway (str, optional): WikiPathways identifier (WPID) for the pathway, e.g. WP554
    
    Returns:
        pandas.Series: A series of unique term names, or None if error occurs.
        
    Example:
        >>> get_ontology_term_names('WP554')
    """
    res = get_ontology_terms(pathway)
    if res is None:
        return None
    # Filter out None values and return unique names
    names = res['terms_name'].dropna().unique()
    return pandas.Series(names) if len(names) > 0 else None

def get_ontology_term_ids(pathway=None):
    """Get Ontology Term IDs by Pathway
    
    Retrieve identifiers of ontology terms for a specific pathway.
    
    Args:
        pathway (str, optional): WikiPathways identifier (WPID) for the pathway, e.g. WP554
    
    Returns:
        pandas.Series: A series of unique term identifiers, or None if error occurs.
        
    Example:
        >>> get_ontology_term_ids('WP554')
    """
    res = get_ontology_terms(pathway)
    if res is None:
        return None
    # Filter out None values and return unique IDs
    ids = res['terms_id'].dropna().unique()
    return pandas.Series(ids) if len(ids) > 0 else None

def get_pathways_by_ontology_term(term):
    """Get Pathways by Ontology Term
    
    Retrieve pathway information for every pathway with a given ontology term.
    
    Args:
        term (str): Official ID of ontology term, e.g., "PW:0000045"
    
    Returns:
        pandas.DataFrame: A dataframe of pathway information, or None if error occurs.
        
    Example:
        >>> get_pathways_by_ontology_term('PW:0000045')
    """
    try:
        # Fetch the static JSON file containing pathways by ontology term data
        response = requests.get('https://www.wikipathways.org/json/getPathwaysByOntologyTerm.json')
        response.raise_for_status()
        data = response.json()
        
        if 'terms' not in data:
            print("API response missing expected terms data structure")
            return None
            
        terms_data = data['terms']
        
        # Find the term that matches our query
        target_term_data = None
        for term_info in terms_data:
            if term_info.get('id') == term:
                target_term_data = term_info
                break
        
        if target_term_data is None:
            print(f"No pathways found for ontology term '{term}'")
            return None
            
        pathways = target_term_data.get('pathways', [])
        if not pathways:
            print(f"No pathways found for ontology term '{term}'")
            return None
        
        # Flatten the nested structure
        flattened_rows = []
        term_id = target_term_data.get('id')
        term_name = target_term_data.get('name')
        term_parent = target_term_data.get('parent')
        
        for pathway in pathways:
            flattened_row = {
                'id': term_id,
                'name': term_name,
                'parent': term_parent,
                'pathways_id': pathway.get('id'),
                'pathways_name': pathway.get('name'),
                'pathways_species': pathway.get('species'),
                'pathways_revision': pathway.get('revision'),
                'pathways_url': pathway.get('url')
            }
            flattened_rows.append(flattened_row)
        
        return pandas.DataFrame(flattened_rows)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def get_pathway_ids_by_ontology_term(term):
    """Get Pathway WPIDs by Ontology Term
    
    Retrieve pathway WPIDs for every pathway with a given ontology term.
    
    Args:
        term (str): Official ID of ontology term, e.g., "PW:0000045"
    
    Returns:
        pandas.Series: A series of unique pathway WPIDs, or None if error occurs.
        
    Example:
        >>> get_pathway_ids_by_ontology_term('PW:0000045')
    """
    res = get_pathways_by_ontology_term(term)
    if res is None:
        return None
    # Return unique pathway IDs
    ids = res['pathways_id'].unique()
    return pandas.Series(ids) if len(ids) > 0 else None

def get_pathways_by_parent_ontology_term(term):
    """Get Pathways by Parent Ontology Term
    
    Retrieve pathway information for every pathway with a child term of given ontology term.
    
    Args:
        term (str): Official name of ontology term, e.g., "signaling pathway"
    
    Returns:
        pandas.DataFrame: A dataframe of pathway information, or None if error occurs.
        
    Example:
        >>> get_pathways_by_parent_ontology_term('signaling pathway')
    """
    try:
        # Use the same endpoint as get_ontology_terms and filter by parent term
        response = requests.get('https://www.wikipathways.org/json/getOntologyTermsByPathway.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathways' not in data:
            print("API response missing expected pathways data structure")
            return None
            
        pathways = data['pathways']
        
        # Filter pathways that have terms with the specified parent
        filtered_rows = []
        for pathway_info in pathways:
            pathway_id = pathway_info.get('id')
            pathway_name = pathway_info.get('name')
            pathway_species = pathway_info.get('species')
            pathway_revision = pathway_info.get('revision')
            pathway_url = pathway_info.get('url')
            
            terms = pathway_info.get('terms', [])
            for term_info in terms:
                if term_info.get('parent') == term:
                    filtered_row = {
                        'id': pathway_id,
                        'name': pathway_name,
                        'species': pathway_species,
                        'revision': pathway_revision,
                        'url': pathway_url,
                        'terms_id': term_info.get('id'),
                        'terms_name': term_info.get('name'),
                        'terms_parent': term_info.get('parent')
                    }
                    filtered_rows.append(filtered_row)
        
        if not filtered_rows:
            print(f"No pathways found with parent ontology term '{term}'")
            return None
            
        return pandas.DataFrame(filtered_rows)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def get_pathway_ids_by_parent_ontology_term(term):
    """Get Pathway WPIDs by Parent Ontology Term
    
    Retrieve pathway WPIDs for every pathway with a child term of given ontology term.
    
    Args:
        term (str): Official name of ontology term, e.g., "signaling pathway"
    
    Returns:
        pandas.Series: A series of unique pathway WPIDs, or None if error occurs.
        
    Example:
        >>> get_pathway_ids_by_parent_ontology_term('signaling pathway')
    """
    res = get_pathways_by_parent_ontology_term(term)
    if res is None:
        return None
    # Return unique pathway IDs
    ids = res['id'].unique()
    return pandas.Series(ids) if len(ids) > 0 else None
