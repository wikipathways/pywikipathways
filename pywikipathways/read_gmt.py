import pandas as pd


def _read_gmt_records(file):
    rows = []
    with open(file, encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            rows.append(parts)
    return rows


def read_gmt(file):
    """Read a generic GMT file as term-gene associations."""
    rows = _read_gmt_records(file)
    records = []
    for parts in rows:
        term = parts[0]
        for gene in parts[2:]:
            records.append({"term": str(term), "gene": str(gene)})
    return pd.DataFrame(records, columns=["term", "gene"])


def read_gmtnames(file):
    """Read a generic GMT file as term-name associations."""
    rows = _read_gmt_records(file)
    records = [{"term": str(parts[0]), "name": str(parts[1])} for parts in rows]
    return pd.DataFrame(records, columns=["term", "name"])
