import pandas

def find_pathways_by_xref(identifier, systemCode):
    res = wikipathways_get('findPathwaysByXref', {'ids': identifier, 'codes': systemCode, 'format': 'json'})
    tmp = pandas.DataFrame(res['result'])
    # score = tmp['score'].apply(lambda x: x['0'])
    score = tmp['score'].apply(lambda x: list(x.values())[0])
    tmp['score'] = score
    return tmp.drop(['fields'], axis=1).drop_duplicates(ignore_index=True)
