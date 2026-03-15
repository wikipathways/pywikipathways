import pandas as pd

from .read_gmt import _read_gmt_records


def read_pathway_gmt(file):
    """Read a WikiPathways GMT file as pathway-gene associations."""
    rows = _read_gmt_records(file)
    records = []
    for parts in rows:
        pathway = parts[0]
        for gene in parts[2:]:
            records.append({"pathway": str(pathway), "gene": str(gene)})

    frame = pd.DataFrame(records, columns=["pathway", "gene"])
    if frame.empty:
        return pd.DataFrame(columns=["name", "version", "wpid", "org", "gene"])

    split = frame["pathway"].str.split("%", n=3, expand=True)
    split = split.reindex(columns=[0, 1, 2, 3])
    split.columns = ["name", "version", "wpid", "org"]
    return pd.concat([split, frame[["gene"]]], axis=1)
