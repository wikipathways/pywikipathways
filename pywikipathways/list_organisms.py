import requests

def list_organisms():
    """List Organisms.

    Retrieve the list of organisms supported by WikiPathways

    Returns:
        list or None: A list of organisms, or None if there was an error

    Example:
        >>> list_organisms()
    """
    try:
        res = requests.get("https://www.wikipathways.org/json/listOrganisms.json")
        res.raise_for_status()
        return res.json()['organisms']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None
