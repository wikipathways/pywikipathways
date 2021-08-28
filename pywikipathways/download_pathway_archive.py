import re
import sys

from .list_organisms import *

def download_pathway_archive(date='current', organism=None, format='gpml', destpath='./'):
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
    #if organism:
        
