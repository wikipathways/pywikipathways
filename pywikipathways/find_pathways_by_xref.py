from .utilities import *

def find_pathways_by_xref(identifier, system_code):
    res = wikipathways_get('findPathwaysByXref', {'ids': identifier, 'codes': system_code, 'format': 'json'})
    tmp = pandas.DataFrame(res['result'])
    score = tmp['score'].apply(lambda x: x['0'])
    # score = tmp['score'].apply(lambda x: list(x.values())[0])
    tmp['score'] = score
    return tmp.drop(['fields'], axis=1).drop_duplicates(ignore_index=True)

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
            e.g., En (Ensembl), L (Entrez), Ch (HMDB), etc. See column two of
            https://github.com/bridgedb/datasources/blob/main/datasources.tsv.

    Returns:
        pandas.Series: A series of WPIDs.

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
            e.g., En (Ensembl), L (Entrez), Ch (HMDB), etc. See column two of
            https://github.com/bridgedb/datasources/blob/main/datasources.tsv.

    Returns:
        pandas.Series: A series of names.

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
            e.g., En (Ensembl), L (Entrez), Ch (HMDB), etc. See column two of
            https://github.com/bridgedb/datasources/blob/main/datasources.tsv.

    Returns:
        pandas.Series: A series of URLs.

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
    return res['url']
