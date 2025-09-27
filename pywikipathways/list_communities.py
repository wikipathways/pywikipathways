import requests
import pandas

def list_communities():
    """List Communities
    
    Retrieve the list of communities hosted by WikiPathways.
    
    Returns:
        pandas.DataFrame or None: A dataframe of community information, or None 
            if no communities are available or on error.
    
    Examples:
        >>> list_communities()
           community-tag    display-name            home-page           description
        0            AOP   AOP-Wiki Community  https://aopwiki.org/  The AOP-Wiki serves ...
        1     COVID-19  COVID-19 Community                    NaN  Community portal for...
    """
    try:
        response = requests.get('https://www.wikipathways.org/json/listCommunities.json')
        response.raise_for_status()
        data = response.json()
        
        if 'communities' not in data:
            print("API response missing expected communities data structure")
            return None
            
        communities = data['communities']
        
        if len(communities) == 0:
            print("No results")
            return None
        
        # Extract community-level information (first 5 columns in R implementation)
        community_info = []
        for community in communities:
            community_data = {
                'display-name': community.get('display-name'),
                'title': community.get('title'),
                'short-description': community.get('short-description'),
                'community-tag': community.get('community-tag'),
                'editors': community.get('editors')
            }
            community_info.append(community_data)
        
        df = pandas.DataFrame(community_info).reset_index(drop=True)
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None


def get_pathways_by_community(community_tag=None):
    """Get Pathways By Community
    
    Retrieve pathways per community.
    
    Args:
        community_tag (str): Abbreviated name of community.
    
    Returns:
        pandas.DataFrame or None: A dataframe of pathway information for the 
            specified community, or None if the community is not found or on error.
    
    Examples:
        >>> get_pathways_by_community("AOP")
              id                                                url           name species  revision
        0   WP999  https://www.wikipathways.org/index.php/Pathway... Example pathway    Homo sapiens    123456
    """
    if community_tag is None:
        print("Must provide a community_tag, e.g., AOP")
        return None
    
    try:
        response = requests.get('https://www.wikipathways.org/json/listCommunities.json')
        response.raise_for_status()
        data = response.json()
        
        if 'communities' not in data:
            print("API response missing expected communities data structure")
            return None
            
        communities = data['communities']
        
        # Find the specified community
        target_community = None
        for community in communities:
            if community.get('community-tag') == community_tag:
                target_community = community
                break
                
        if target_community is None:
            print(f"Must provide a valid community_tag, e.g., AOP. Available tags: {[c.get('community-tag') for c in communities]}")
            return None
            
        # Extract pathway information
        pathways = target_community.get('pathways', [])
        
        if len(pathways) == 0:
            print(f"No pathways found for community: {community_tag}")
            return None
            
        df = pandas.DataFrame(pathways).reset_index(drop=True)
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None


def get_pathway_ids_by_community(community_tag=None):
    """Get Pathway IDs By Community
    
    Retrieve the list of pathway IDs per community.
    
    Args:
        community_tag (str): Abbreviated name of community.
    
    Returns:
        pandas.Series or None: A series of pathway IDs, or None if the 
            community is not found or on error.
    
    Examples:
        >>> get_pathway_ids_by_community("AOP")
        0     WP999
        1    WP1000
        Name: id, dtype: object
    """
    res = get_pathways_by_community(community_tag)
    if res is None:
        return None
    return res['id'] if 'id' in res.columns else None


def get_pathway_names_by_community(community_tag=None):
    """Get Pathway Names By Community
    
    Retrieve the list of pathway names per community.
    
    Args:
        community_tag (str): Abbreviated name of community.
    
    Returns:
        pandas.Series or None: A series of pathway names, or None if the 
            community is not found or on error.
    
    Examples:
        >>> get_pathway_names_by_community("AOP")
        0     Example pathway 1
        1     Example pathway 2
        Name: name, dtype: object
    """
    res = get_pathways_by_community(community_tag)
    if res is None:
        return None
    return res['name'] if 'name' in res.columns else None


def get_pathway_urls_by_community(community_tag=None):
    """Get Pathway URLs By Community
    
    Retrieve the list of pathway URLs per community.
    
    Args:
        community_tag (str): Abbreviated name of community.
    
    Returns:
        pandas.Series or None: A series of pathway URLs, or None if the 
            community is not found or on error.
    
    Examples:
        >>> get_pathway_urls_by_community("AOP")
        0     https://www.wikipathways.org/index.php/Pathway...
        1     https://www.wikipathways.org/index.php/Pathway...
        Name: url, dtype: object
    """
    res = get_pathways_by_community(community_tag)
    if res is None:
        return None
    return res['url'] if 'url' in res.columns else None