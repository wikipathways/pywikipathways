def get_curation_tags(pathway):
    res = wikipathways_get('getCurationTags', {'pwId': pathway, 'format': 'json'})
    return pandas.DataFrame(res['tags'])

def get_curation_tag_names(pathway):
    res = get_curation_tags(pathway)
    return res['name']

def get_every_curation_tag(tag):
    res = wikipathways_get('getCurationTagsByName', {'tagName': tag, 'format': 'json'})
    return pandas.DataFrame(res['tags'])
