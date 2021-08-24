import pandas

def find_pathways_by_text(query):
    res = wikipathways_get('findPathwaysByText', {'query': query, 'format': 'json'})
    tmp = pandas.DataFrame(res['result'])
    score = tmp['score'].apply(lambda x: x['0'])
    tmp['score'] = score
    return tmp.drop(['fields'], axis=1).drop_duplicates(ignore_index=True)
