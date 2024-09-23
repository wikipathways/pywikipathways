import requests

def list_organisms():
    """List Organisms.

    Retrieve the list of organisms supported by WikiPathways

    Returns:
        list: A list of organisms

    Example:
        >>> list_organisms()
    """
    res = requests.get("https://www.wikipathways.org/json/listOrganisms.json")
    res.raise_for_status()
    return res.json()['organisms']
