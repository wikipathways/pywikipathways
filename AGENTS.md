# pywikipathways Agent Guide

Use this file as the first stop when changing code or docs. Default triage order: keep regressions and API compatibility first, then small improvements, then new endpoints.

## Mission and Scope
- Provide Python interfaces for WikiPathways operations; parity with rWikiPathways is the long-term goal (function names adapt to snake_case).
- Core package lives in `pywikipathways/`; each module wraps either a static JSON endpoint or a live webservice call.
- This repo is user-facing (published on PyPI) and powers scientific workflows; prioritise backwards compatibility and clear error handling.

## Code Structure and Conventions
- `pywikipathways/utilities.py` holds shared HTTP helpers (`wikipathways_get`, `build_url`). Reuse and extend these rather than duplicating request code.
- Individual feature modules (for example `find_pathways_by_literature.py`, `get_pathway_info.py`, `get_counts.py`) follow a consistent pattern: validate inputs, request JSON (static files under `https://www.wikipathways.org/json/` when available), normalise into `pandas.DataFrame` or `Series`, return `None` when nothing is found, and print a diagnostic on exceptions. Match this behaviour in new wrappers.
- Docstrings stay descriptive and include example calls; mimic the concise numpy-style tone used today.
- Maintain snake_case function names and keep argument names aligned with the R originals whenever possible.
- Data shapes: pathway lists are typically `DataFrame` rows with pathway identifiers, names, species, and URLs; single lookups often return `Series` keyed by field name. Preserve column/index naming when adding wrappers.

## Error Handling Checklist
- Validate inputs early; prefer informative `ValueError` only when caller mistakes are clear.
- On network or parsing issues return `None` and print a short diagnostic so downstream code can detect outages.
- Access JSON defensively (use `.get` with defaults) because static mirrors can drift.
- Avoid raising raw exceptions from third-party libraries; translate into the patterns above.

## New Endpoint Recipe
- Inspect the remote JSON first (manual `requests` call) to confirm shape and required params.
- Build URLs with `build_url` and fetch with `wikipathways_get`; keep new helper logic in `utilities.py` if it will be shared.
- Normalise to `pandas` objects with stable column/index names; avoid hard-coding counts.
- Add a concise docstring example, a focused pytest (happy path, schema not counts), and a brief docs note in `README.md` or `docs/`.

## Network and Tests
- Tests live in `tests/` and use `pytest`. Run from the repo root. They rely on live WikiPathways endpoints; avoid hammering the service (space out runs, prefer targeted `pytest tests/<module> -k happy` during iteration).
- If network is unavailable (CI or local), mark affected tests `xfail` or skip with a clear reason instead of removing them.
- Manual smoke checks are encouraged for new endpoints before wiring them into `pandas`.

## Development Workflow
- Use a virtual environment and install locally with `pip install -e .` to iterate quickly.
- `uv` works out of the box with `pyproject.toml`; `uv pip install -e .` and `uv run pytest` mirror the pip workflow.
- Respect the repo’s minimum Python version (see `pyproject.toml`) and keep dependencies lightweight—prefer standard library or existing deps (`requests`, `pandas`, `lxml`).
- When touching generation scripts or notebooks (see `docs/pywikipathways_Overview.ipynb`), keep output size modest and consider moving long examples into docs instead of inline tests.
- For new functionality, update `README.md` and Read the Docs sources under `docs/` so users discover additions.
- Friendly API behaviour matters: deprecate gently and note behavioural changes in `LITERATURE_API_UPDATE.md` or a similar short note.

## Release and Tooling
- Packaging metadata lives in `pyproject.toml`; bump the version there when releasing. Build with `python -m build` and publish with `twine` after verifying `README.md` renders.
- Licensing is MIT (`LICENSE`).
- Prefer existing formatting/lint settings in the repo; if unsure, mirror current style and keep changes minimal.

## Common Pitfalls
- Static JSON mirrors can drift; handle missing keys defensively and emit user-friendly messages instead of raising raw exceptions.
- Downstream consumers expect `None` on network failures—mirror this behaviour so callers can detect outages.
- Avoid large downloads or storing generated data in the repo; rely on runtime fetching.
