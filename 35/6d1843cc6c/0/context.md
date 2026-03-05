# Session Context

**Session ID:** 246551e4-6bd8-431f-9dcb-478dd7e592c6

**Commit Message:** Update this repository to support testing with the uv command.

## Prompt

update this repository to support testing with the uv command.

## Summary

All 54 tests pass (2 skipped due to an unavailable endpoint). Here's a summary of all changes:

### uv support
- **`pyproject.toml`**: Changed `[tool.uv] dev-dependencies` to `[dependency-groups] dev` (current uv format). Tests now run with `uv run pytest`.

### Missing functions ported from rwikipathways

**`pathways.py`** — Added 3 functions:
- `list_pathway_ids()`, `list_pathway_names()`, `list_pathway_urls()`

**`search.py`** — Added 12 functions + fixed parameter naming:
- `find_pathway_ids_by_text()`, `find_pathway_names_by_text()`, `find_pathway_urls_by_text()`
- `find_pathway_ids_by_xref()`, `find_pathway_names_by_xref()`, `find_pathway_urls_by_xref()`
- `find_pathway_ids_by_literature()`, `find_pathway_names_by_literature()`, `find_pathway_urls_by_literature()`
- `find_pathway_ids_by_orcid()`, `find_pathway_names_by_orcid()`, `find_pathway_urls_by_orcid()`
- Fixed `find_pathways_by_orcid`: renamed `orcid` param to `query` (matching R)

**`annotations.py`** — Added 4 functions, replaced 3 deprecated ones:
- Added: `get_ontology_term_names()`, `get_ontology_term_ids()`, `get_pathway_ids_by_ontology_term()`, `get_pathway_ids_by_parent_ontology_term()`, `get_curation_status()`
- Removed deprecated: `get_curation_tags()`, `get_every_curation_tag()`, `get_pathways_by_curation_tag()` (used old webservice API)

**`communities.py`** — Added 3 functions:
- `get_pathway_ids_by_community()`, `get_pathway_names_by_community()`, `get_pathway_urls_by_community()`

**`stats.py`** — Added 2 functions:
- `get_recent_changes_ids()`, `get_recent_changes_names()`

**`gmt.py`** — New module with 4 functions:
- `read_gmt()`, `read_gmt_names()`, `read_pathway_gmt()`, `write_gmt()`

### Inconsistencies fixed
- **`pathways.py`**: `download_pathway_archive()` now raises `ValueError` instead of calling `sys.exit()`
- **`utilities.py`**: Deleted (only served deprecated functions)
- **`__init__.py`**: Updated to export the new `gmt` module

## Key Actions

- - **Glob**: pyproject.toml
- - **Glob**: setup.{py,cfg}
- - **Read**: /home/kozo2/repos/pywikipathways/pyproject.toml
- - **Edit**: /home/kozo2/repos/pywikipathways/pyproject.toml
- - **Bash**: Sync uv dependencies
- - **Bash**: Run GMT tests via uv
- - **Bash**: Run full test suite via uv
