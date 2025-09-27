import requests
import pandas as pd

# ----------------------------------------------------------------------
# Get Ontology Terms by Pathway
def get_ontology_terms(pathway=None):
    url = "https://www.wikipathways.org/json/getOntologyTermsByPathway.json"
    res = requests.get(url).json()
    pathways_data = res['pathways']
    res_df = pd.DataFrame(pathways_data)
    if 'terms' in res_df.columns:
        # Explode lists to separate rows first, then normalize
        res_df_exploded = res_df.explode('terms')
        terms_normalized = pd.json_normalize(res_df_exploded['terms'])
        terms_normalized.columns = ['terms_' + col for col in terms_normalized.columns]    
        # Combine back
        res_df = pd.concat([res_df_exploded.drop('terms', axis=1).reset_index(drop=True), 
                            terms_normalized.reset_index(drop=True)], axis=1)
    
    if pathway is not None:
        res_df = res_df[res_df["id"] == pathway]

    return res_df.reset_index(drop=True)

# ----------------------------------------------------------------------
# Get Ontology Term Names by Pathway
def get_ontology_term_names(pathway=None):
    df = get_ontology_terms(pathway)
    return df["name"].dropna().unique().tolist()

# ----------------------------------------------------------------------
# Get Ontology Term IDs by Pathway
def get_ontology_term_ids(pathway=None):
    df = get_ontology_terms(pathway)
    return df["id"].dropna().unique().tolist()

# ----------------------------------------------------------------------
# Get Pathways by Ontology Term
def get_pathways_by_ontology_term(term=None):
    url = "https://www.wikipathways.org/json/getPathwaysByOntologyTerm.json"
    res = requests.get(url).json()
    pathways_data = res['terms']
    res_df = pd.DataFrame(pathways_data)
    if 'pathways' in res_df.columns:
        # Explode lists to separate rows first, then normalize
        res_df_exploded = res_df.explode('pathways')
        pathways_normalized = pd.json_normalize(res_df_exploded['pathways'])
        pathways_normalized.columns = ['pathways_' + col for col in pathways_normalized.columns]    
        # Combine back
        res_df = pd.concat([res_df_exploded.drop('pathways', axis=1).reset_index(drop=True), 
                            pathways_normalized.reset_index(drop=True)], axis=1)    
    
    if term is not None:
        res_df = res_df[res_df["id"] == term]
    
    return res_df.reset_index(drop=True)

# ----------------------------------------------------------------------
# Get Pathway WPIDs by Ontology Term
def get_pathway_ids_by_ontology_term(term=None):
    df = get_pathways_by_ontology_term(term)
    return df["pathways_id"].dropna().unique().tolist()

# ----------------------------------------------------------------------
# Get Pathways by Parent Ontology Term
def get_pathways_by_parent_ontology_term(term=None):
    url = "https://www.wikipathways.org/json/getOntologyTermsByPathway.json"
    res = requests.get(url).json()
    pathways_data = res['pathways']
    res_df = pd.DataFrame(pathways_data)
    if 'terms' in res_df.columns:
        # Explode lists to separate rows first, then normalize
        res_df_exploded = res_df.explode('terms')
        terms_normalized = pd.json_normalize(res_df_exploded['terms'])
        terms_normalized.columns = ['terms_' + col for col in terms_normalized.columns]    
        # Combine back
        res_df = pd.concat([res_df_exploded.drop('terms', axis=1).reset_index(drop=True), 
                            terms_normalized.reset_index(drop=True)], axis=1)
    
    if term is not None:
        res_df = res_df[res_df["terms_parent"] == term]

    return res_df.reset_index(drop=True)

# ----------------------------------------------------------------------
# Get Pathway WPIDs by Parent Ontology Term
def get_pathway_ids_by_parent_ontology_term(term=None):
    df = get_pathways_by_parent_ontology_term(term)
    return df["id"].dropna().unique().tolist()
