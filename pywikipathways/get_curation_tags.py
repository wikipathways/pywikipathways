from .utilities import *

def get_curation_tags(pathway):
    res = wikipathways_get('getCurationTags', {'pwId': pathway, 'format': 'json'})
    return pandas.DataFrame(res['tags'])

def get_curation_tag_names(pathway):
    res = get_curation_tags(pathway)
    return res['name']

def get_every_curation_tag(tag):
    res = wikipathways_get('getCurationTagsByName', {'tagName': tag, 'format': 'json'})
    return pandas.DataFrame(res['tags'])

def get_pathways_by_curation_tag(tag):
    res = wikipathways_get('getCurationTagsByName', {'tagName': tag, 'format': 'json'})
    return pandas.DataFrame([i['pathway'] for i in res['tags']])

def get_pathway_ids_by_curation_tag(tag):
    res = get_pathways_by_curation_tag(tag)
    return res['id']
