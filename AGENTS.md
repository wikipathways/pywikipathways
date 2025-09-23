# pywikipathways Agent Guide

## Mission and Scope
- Provide Python interfaces for WikiPathways operations; parity with rWikiPathways is the long-term goal (function names adapt to snake_case).
- Core package lives in `pywikipathways/`; each module wraps either a static JSON endpoint or a live webservice call.
- This repo is user-facing (published on PyPI) and powers scientific workflows; prioritise backwards compatibility and clear error handling.

## Code Structure and Conventions
- `pywikipathways/utilities.py` holds shared HTTP helpers (`wikipathways_get`, `build_url`). Reuse and extend these rather than duplicating request code.
- Individual feature modules (for example `find_pathways_by_literature.py`, `get_pathway_info.py`, `get_counts.py`) follow a consistent pattern: validate inputs, request JSON (static files under `https://www.wikipathways.org/json/` when available), normalise into `pandas.DataFrame` or `Series`, return `None` when nothing is found, and print a diagnostic on exceptions. Match this behaviour in new wrappers.
- Keep docstrings descriptive and include example calls. Existing docs favour concise numpy-style prose; mimic tone and structure.
- Maintain snake_case function names and keep argument names aligned with the R originals whenever possible.

## Tests and Verification
- Test suite is in `tests/` and uses `pytest`. Run `pytest` from the repo root; tests rely on live WikiPathways endpoints, so expect network access and avoid overusing them in rapid succession.
- When adding or changing API wrappers, create focused tests that exercise the happy path while protecting against brittle network assumptions (e.g., assert schema fields, not hard-coded counts).
- Manual smoke checks are encouraged for new endpoints: confirm the remote JSON shape with `requests` before wiring it into `pandas`.

## Development Workflow
- Use a virtual environment and install the project locally with `pip install -e .` to iterate quickly.
- Respect the repo’s minimum Python version (see `pyproject.toml`) and keep dependencies lightweight—prefer standard library or existing deps (`requests`, `pandas`, `lxml`).
- When touching generation scripts or notebooks (see `docs/pywikipathways_Overview.ipynb`), keep output size modest and consider moving long examples into docs instead of inline tests.
- For new functionality, update `README.md` and Read the Docs sources under `docs/` so users discover additions.

## Common Pitfalls
- Static JSON mirrors can drift; handle missing keys defensively and emit user-friendly messages instead of raising raw exceptions.
- Downstream consumers expect `None` on network failures—mirror this behaviour so callers can detect outages.
- Avoid large downloads or storing generated data in the repo; rely on runtime fetching.

## Useful References
- Packaging metadata lives in `pyproject.toml`; bump versions there when releasing.
- Licensing is MIT (`LICENSE`).
- See `LITERATURE_API_UPDATE.md` for a recent example of documenting behavioural changes.

