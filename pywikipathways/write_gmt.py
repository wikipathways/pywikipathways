def write_gmt(df, outfile):
    """Write a data frame to GMT format."""
    ncols = len(df.columns)
    if ncols < 2:
        raise ValueError("The input data frame must include at least two columns.")

    data = df.copy()

    if ncols == 2:
        id_col = data.columns[0]
        gene_col = data.columns[1]
        data["desc"] = data[id_col]
        data = data[[id_col, "desc", gene_col]]
    elif ncols > 3:
        id_cols = list(data.columns[: ncols - 2])
        print(
            "Concatenating the following columns to use as Identifiers: "
            + ", ".join(id_cols)
        )
        data["_identifier"] = data[id_cols].astype(str).agg("%".join, axis=1)
        desc_col = data.columns[ncols - 2]
        gene_col = data.columns[ncols - 1]
        data = data[["_identifier", desc_col, gene_col]]

    id_col = data.columns[0]
    desc_col = data.columns[1]
    gene_col = data.columns[2]

    unique_ids = data[id_col].drop_duplicates().tolist()
    lines = []
    for identifier in unique_ids:
        subset = data[data[id_col] == identifier]
        desc = subset.iloc[0][desc_col]
        genes = subset[gene_col].astype(str).tolist()
        lines.append("\t".join([str(identifier), str(desc), *genes]))

    with open(outfile, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
        handle.write("\n")
