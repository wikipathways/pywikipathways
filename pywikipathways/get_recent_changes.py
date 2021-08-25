from .utilities import *

def get_recent_changes(timestamp):
    res = wikipathways_get('getRecentChanges', {'timestamp': timestamp, 'format': 'json'})
    if 'pathways' in res.keys():
        return pandas.DataFrame(res['pathways'])
    else:
        print("No results")

def get_recent_changes_ids(timestamp):
    res = get_recent_changes(timestamp)
    return res['id']

def get_recent_changes_names(timestamp):
    res = get_recent_changes(timestamp)
    return res['name']
