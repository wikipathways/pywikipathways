import requests
from .utilities import *

def find_pathways_by_xref(identifier, system_code):
    """Find Pathways By Xref
    
    Retrieve pathways containing the query Xref by identifier and system code
    from a static JSON endpoint.
    
    Args:
        identifier (str): The official ID specified by a data source or system
        system_code (str): The BridgeDb code associated with the data source or system,
            e.g., En (Ensembl), L (NCBI gene), H (HGNC), U (UniProt), Wd (Wikidata), 
            Ce (ChEBI), Ik (InChI). See column two of
            https://github.com/bridgedb/datasources/blob/main/datasources.tsv.
    
    Returns:
        pandas.DataFrame: A dataframe of pathway attributes including the matching
                         identifiers, or None if no results.
    """
    if identifier is None:
        raise ValueError("Must provide an identifier to query, e.g., ENSG00000100031")
    if system_code is None:
        raise ValueError("Must provide a systemCode, e.g., En")
    
    # Map system codes to field names (based on R implementation)
    code_list = {
        "En": "ensembl",
        "L": "ncbigene", 
        "H": "hgnc",
        "U": "uniprot",
        "Wd": "wikidata",
        "Ce": "chebi",
        "Ik": "inchikey"
    }
    
    if system_code not in code_list:
        raise ValueError(f"Must provide a supported systemCode, e.g., En. Supported codes: {', '.join(code_list.keys())}")
    
    try:
        # Fetch the static JSON file containing all pathway xref data
        response = requests.get('https://www.wikipathways.org/json/findPathwaysByXref.json')
        response.raise_for_status()
        data = response.json()
        
        if 'pathwayInfo' not in data:
            print("API response missing expected pathwayInfo data structure")
            return None
            
        pathway_info = data['pathwayInfo']
        
        field_name = code_list[system_code]
        identifier_lower = identifier.lower()
        
        # Filter pathways that contain the identifier in the appropriate field
        filtered_pathways = []
        for pathway in pathway_info:
            field_value = pathway.get(field_name)
            if field_value is not None:
                field_value_str = str(field_value).lower()
                if identifier_lower in field_value_str:
                    filtered_pathways.append(pathway)
        
        if len(filtered_pathways) == 0:
            print("No results")
            return None
            
        # Convert to DataFrame and return
        return pandas.DataFrame(filtered_pathways).drop_duplicates(ignore_index=True)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def find_pathway_ids_by_xref(identifier, system_code):
    """Find Pathway WPIDs By Xref
    
    Retrieve list of pathway WPIDs containing the query Xref by
    identifier and system code.
    
    Note:
        there will be multiple listings of the same pathway if the
        Xref is present mutiple times.
        
    Args:
        identifier (str): The official ID specified by a data source or system
        system_code (str): The BridgeDb code associated with the data source or system,
            e.g., En (Ensembl), L (NCBI gene), H (HGNC), U (UniProt), Wd (Wikidata), 
            Ce (ChEBI), Ik (InChI). See column two of
            https://github.com/bridgedb/datasources/blob/main/datasources.tsv.

    Returns:
        pandas.Series or None: A series of WPIDs, or None if no results.

    Examples:
        >>> find_pathway_ids_by_xref('ENSG00000232810','En')
        0     WP2813
        1     WP4341
        2     WP4673
        3     WP1584
        4     WP2571
               ...  
        82    WP5055
        83    WP5093
        84    WP5115
        85    WP5094
        86    WP5098
        Name: id, Length: 87, dtype: object
    """
    res = find_pathways_by_xref(identifier, system_code)
    if res is None:
        return None
    return res['id']

def find_pathway_names_by_xref(identifier, system_code):
    """Find Pathway Names By Xref
    
    Retrieve list of pathway names containing the query Xref by
    identifier and system code.
    
    Note:
        there will be multiple listings of the same pathway if the
        Xref is present mutiple times.
        
    Args:
        identifier (str): The official ID specified by a data source or system
        system_code (str): The BridgeDb code associated with the data source or system,
            e.g., En (Ensembl), L (NCBI gene), H (HGNC), U (UniProt), Wd (Wikidata), 
            Ce (ChEBI), Ik (InChI). See column two of
            https://github.com/bridgedb/datasources/blob/main/datasources.tsv.

    Returns:
        pandas.Series or None: A series of names, or None if no results.

    Examples:
        >>> find_pathway_names_by_xref('ENSG00000232810','En')
        0     Mammary gland development pathway - Embryonic ...
        1       Non-genomic actions of 1,25 dihydroxyvitamin D3
        2                                      Male infertility
        3                             Type II diabetes mellitus
        4                     Polycystic kidney disease pathway
                                    ...                        
        82                                   Burn wound healing
        83                   Opioid receptor pathway annotation
        84          Network map of SARS-CoV-2 signaling pathway
        85                              Orexin receptor pathway
        86                         T-cell activation SARS-CoV-2
        Name: name, Length: 87, dtype: object
    """
    res = find_pathways_by_xref(identifier, system_code)
    if res is None:
        return None
    return res['name']

def find_pathway_urls_by_xref(identifier, system_code):
    """Find Pathway URLs By Xref
    
    Retrieve list of pathway URLs containing the query Xref by
    identifier and system code.
    
    Note:
        there will be multiple listings of the same pathway if the
        Xref is present mutiple times.
        
    Args:
        identifier (str): The official ID specified by a data source or system
        system_code (str): The BridgeDb code associated with the data source or system,
            e.g., En (Ensembl), L (NCBI gene), H (HGNC), U (UniProt), Wd (Wikidata), 
            Ce (ChEBI), Ik (InChI). See column two of
            https://github.com/bridgedb/datasources/blob/main/datasources.tsv.

    Returns:
        pandas.Series or None: A series of URLs, or None if no results.

    Examples:
        >>> find_pathway_urls_by_xref('ENSG00000232810','En')
        0     https://www.wikipathways.org/index.php/Pathway...
        1     https://www.wikipathways.org/index.php/Pathway...
        2     https://www.wikipathways.org/index.php/Pathway...
        3     https://www.wikipathways.org/index.php/Pathway...
        4     https://www.wikipathways.org/index.php/Pathway...
                                    ...                        
        82    https://www.wikipathways.org/index.php/Pathway...
        83    https://www.wikipathways.org/index.php/Pathway...
        84    https://www.wikipathways.org/index.php/Pathway...
        85    https://www.wikipathways.org/index.php/Pathway...
        86    https://www.wikipathways.org/index.php/Pathway...
        Name: url, Length: 87, dtype: object
    """
    res = find_pathways_by_xref(identifier, system_code)
    if res is None:
        return None
    return res['url']
