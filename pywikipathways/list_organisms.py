from .utilities import *

def list_organisms():
    res = wikipathways_get('listOrganisms', {'format': 'json'})
    return res['organisms']
