import pandas as pd

from pywikipathways.read_gmt import read_gmt, read_gmtnames
from pywikipathways.read_pathway_gmt import read_pathway_gmt
from pywikipathways.write_gmt import write_gmt


def test_read_gmt_and_names(tmp_path):
    gmt_file = tmp_path / "simple.gmt"
    gmt_file.write_text(
        "TERM_A\tTerm A Desc\t100\t200\nTERM_B\tTerm B Desc\t300\n",
        encoding="utf-8",
    )

    term_gene = read_gmt(str(gmt_file))
    assert list(term_gene.columns) == ["term", "gene"]
    assert len(term_gene) == 3
    assert term_gene.iloc[0].to_dict() == {"term": "TERM_A", "gene": "100"}

    term_name = read_gmtnames(str(gmt_file))
    assert list(term_name.columns) == ["term", "name"]
    assert term_name.iloc[1].to_dict() == {"term": "TERM_B", "name": "Term B Desc"}


def test_read_pathway_gmt(tmp_path):
    gmt_file = tmp_path / "pathway.gmt"
    gmt_file.write_text(
        "Pathway One%20240101%WP1%Homo sapiens\tDesc\t111\t222\n",
        encoding="utf-8",
    )

    frame = read_pathway_gmt(str(gmt_file))
    assert list(frame.columns) == ["name", "version", "wpid", "org", "gene"]
    assert frame.iloc[0].to_dict() == {
        "name": "Pathway One",
        "version": "20240101",
        "wpid": "WP1",
        "org": "Homo sapiens",
        "gene": "111",
    }


def test_write_gmt_round_trip(tmp_path):
    source = pd.DataFrame(
        {
            "id": ["WP1000", "WP1000", "WP1001"],
            "description": ["cancer", "cancer", "diabetes"],
            "gene": ["574413", "2167", "5781"],
        }
    )
    out_file = tmp_path / "written.gmt"

    write_gmt(source, str(out_file))
    loaded = read_gmt(str(out_file))
    assert len(loaded) == 3
    assert set(loaded["term"]) == {"WP1000", "WP1001"}
