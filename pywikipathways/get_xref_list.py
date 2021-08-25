from .utilities import *

def get_xref_list(pathway, system_code):
    res = wikipathways_get('getXrefList', {'pwId': pathway, 'code': system_code, 'format': 'json'})
    return res['xrefs']
