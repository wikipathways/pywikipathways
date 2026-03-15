import requests
import pandas as pd


def _normalize_exploded_column(df, column_name, prefix):
    exploded_df = df.explode(column_name).reset_index(drop=True)
    normalized = pd.json_normalize(
        exploded_df[column_name].apply(lambda value: value if isinstance(value, dict) else {})
    )
    if not normalized.empty:
        normalized.columns = [f"{prefix}_{col}" for col in normalized.columns]
    return pd.concat([exploded_df.drop(column_name, axis=1), normalized], axis=1)

# ----------------------------------------------------------------------
# Get Ontology Terms by Pathway
def get_ontology_terms(pathway=None):
    url = "https://www.wikipathways.org/json/getOntologyTermsByPathway.json"
    res = requests.get(url).json()
    pathways_data = res['pathways']
    res_df = pd.DataFrame(pathways_data)
    if 'terms' in res_df.columns:
        res_df = _normalize_exploded_column(res_df, 'terms', 'terms')
    
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
        res_df = _normalize_exploded_column(res_df, 'pathways', 'pathways')
    
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
        res_df = _normalize_exploded_column(res_df, 'terms', 'terms')
    
    if term is not None:
        res_df = res_df[res_df["terms_parent"] == term]

    return res_df.reset_index(drop=True)

# ----------------------------------------------------------------------
# Get Pathway WPIDs by Parent Ontology Term
def get_pathway_ids_by_parent_ontology_term(term=None):
    df = get_pathways_by_parent_ontology_term(term)
    return df["id"].dropna().unique().tolist()
