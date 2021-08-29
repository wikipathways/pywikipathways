import re
import sys
import requests
import pandas

from .list_organisms import *

def download_pathway_archive(date='current', organism=None, format='gpml', destpath='./'):
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
