import re
import sys
import requests
import pandas

from .list_organisms import *

def download_pathway_archive(date='current', organism=None, format='gpml', destpath='./'):
    """Download Pathway Archive

    Access the monthly archives of pathway content from WikiPathways.

    If you do not specify an organism, then an archive file will not be downloaded.
    Instead, the archive will be opened in a tab in your default browser.

    Args:
        date (str, optional): The timestamp for a monthly release (e.g., 20171010) 
            or "current" (default) for the latest release.
        organism (str, optional): A particular species. See `listOrganisms`.
        format (str, optional): Either "gpml" (default), "gmt", or "svg".
        destpath (str, optional): Destination path for the file to be downloaded to. 
            Default is the current working directory.

    Returns:
        str: Filename of the downloaded file or an opened tab in the default browser.

    Examples:
        >>> download_pathway_archive()  # open in browser
        >>> download_pathway_archive(format="gmt")  # open in browser
        >>> download_pathway_archive(date="20230710", format="svg")  # open in browser
        >>> download_pathway_archive(date="20230710", organism="Mus musculus", format="svg")  # download file
        >>> download_pathway_archive(organism="Mus musculus")  # download file
    """
    # get validated format
    if not format in ['gpml', 'gmt', 'svg']:
        sys.exit(format + " is not in ['gpml', 'gmt', 'svg']. Please specify one of these.")
    
    # validate date
    if date != 'current':
        if not re.match("^\\d{8}$", date):
            sys.exit('The date must be 8 digits (YYYYMMDD) or "current"')
    
    # validate organism
    orgs = list_organisms()
    if organism:
        if not organism in orgs:
            sys.exit('The organism must match the list of supported organisms, see list_organisms()')
    
    # download specific file, or...
    if organism:
        if date == 'current':
            curr_files = pandas.read_html("https://wikipathways-data.wmcloud.org/current/" + format)[0]['Filename']
            filename = curr_files[curr_files.str.contains(organism.replace(" ", "_"))]
            filename = list(filename)[0]
            if not True in curr_files.str.contains(organism.replace(" ", "_")):
                sys.exit('Could not find a file matching your specifications. Try browsing http://data.wikipathways.org.')
        else:
            if requests.get("https://wikipathways-data.wmcloud.org/" + date).ok:
                ext = ".zip"
                if format == 'gmt':
                    ext = ".gmt"
                filename = "-".join(['wikipathways', date, format, organism.replace(" ", "_")]) + ext
        url = "/".join(['http://data.wikipathways.org', date, format, filename])
        r = requests.get(url)
        file = open(filename, "wb")
        file.write(r.content)
        file.close()
        return filename
    else:
        url = "/".join(['http://data.wikipathways.org', date, format])
        print("organism argument is not specified. Open " + url + " with your web browser and specify the organism.")
