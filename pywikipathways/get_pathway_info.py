import requests
import pandas as pd

def get_pathway_info(pathway=None):
    """
    Retrieve information for a specific pathway (or all pathways) from WikiPathways.

    Parameters
    ----------
    pathway : str, optional
        WikiPathways identifier (WPID) for the pathway to download, e.g. 'WP554'.
        If None, then all pathways are returned.

    Returns
    -------
    pd.DataFrame
        DataFrame containing pathway info: WPID, URL, name, species, revision,
        authors, description, citedIn.
    """
    url = "https://www.wikipathways.org/json/getPathwayInfo.json"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()

    # Extract pathwayInfo list and normalize into dataframe
    df = pd.json_normalize(data["pathwayInfo"])

    # Filter if pathway is given
    if pathway is not None:
        df = df[df["id"] == pathway]

    return df.reset_index(drop=True)
