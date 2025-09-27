# Copilot Instructions for pywikipathways

## Repository Overview

**pywikipathways** is a Python client package providing programmatic access to the WikiPathways API. It's a Python port of the R Bioconductor package rWikiPathways, maintaining unified function names and arguments (with camelCase/snake_case differences). The repository contains ~600 lines of Python code across 22 files.

### Key Repository Information
- **Language**: Python 3.9+ (supports 3.9, 3.10, 3.11, 3.12)
- **Package Type**: API client library for bioinformatics
- **Build System**: Modern Python packaging with `pyproject.toml` and hatchling backend
- **Dependencies**: requests, pandas, lxml
- **API Target**: WikiPathways web service (`webservice.wikipathways.org`)
- **Documentation**: Sphinx with Jupyter notebooks (nbsphinx extension)
- **License**: MIT

## Build and Development Instructions

### Prerequisites
Always ensure you have Python 3.9+ and pip installed before starting any development work.

### Installation and Setup

**Development Installation (REQUIRED first step):**
```bash
# Install the package dependencies manually (due to network timeouts with hatchling):
pip install requests pandas lxml pytest

# Set PYTHONPATH for development:
export PYTHONPATH=/path/to/pywikipathways:$PYTHONPATH

# Test the installation:
python -c "import pywikipathways; print('Import successful, version:', pywikipathways.__version__)"
```

**Important**: Due to network connectivity issues in CI environments, the standard `pip install ./` often fails with timeout errors when installing hatchling build dependencies. Always install dependencies manually first.

### Testing

**Run all tests:**
```bash
# Set PYTHONPATH and run pytest:
PYTHONPATH=/path/to/pywikipathways:$PYTHONPATH pytest tests/ -v
```

**Note on test failures**: Tests require network access to WikiPathways API endpoints (`webservice.wikipathways.org`, `www.wikipathways.org`). In environments without internet access, tests will fail with connection errors - this is expected and not a code issue.

**Test structure**: Tests use pytest and are located in `tests/` directory. Each test file corresponds to a main module (e.g., `test_get_pathway.py` tests `get_pathway.py`). All tests will fail with connection errors in environments without internet access - this is expected behavior, not a code issue.

### Build Process

**Package building** (may fail due to network issues):
```bash
# Install build tools:
pip install build

# Build wheel (may timeout due to hatchling dependency installation):
python -m build --wheel --skip-dependency-check
```

**Workaround for build issues**: If build fails due to network timeouts, development and testing can still proceed using PYTHONPATH method above.

### Documentation

**Documentation building**:
```bash
# Install documentation dependencies:
pip install sphinx nbsphinx

# Build documentation (requires pandoc for notebook conversion):
cd docs/
PYTHONPATH=/path/to/pywikipathways:$PYTHONPATH sphinx-build -b html . _build/html
```

**Documentation dependencies**: Requires pandoc for Jupyter notebook conversion. If pandoc is missing, documentation build will fail.

**Documentation structure**: 
- Sphinx configuration: `docs/conf.py`
- Main documentation: `docs/index.rst`
- Jupyter notebook tutorials in `docs/` directory

## Project Architecture and Layout

### Core Package Structure (`pywikipathways/`)
- `__init__.py` - Main package imports (47 public functions)
- `utilities.py` - Core HTTP client (`wikipathways_get()`, `build_url()`)
- `_version.py` - Version definition (currently 0.1.0)

### Main API Modules
Each module corresponds to a WikiPathways API endpoint:
- `download_pathway_archive.py` - Download pathway archives
- `find_pathway_by_text.py` - Text-based pathway search
- `find_pathways_by_literature.py` - Literature-based search
- `find_pathways_by_xref.py` - Cross-reference based search
- `get_pathway.py` - Get pathway data by ID
- `get_pathway_info.py` - Get pathway metadata
- `get_pathway_history.py` - Get pathway version history
- `list_organisms.py` - List supported organisms
- `list_pathways.py` - List all pathways

### Configuration Files
- `pyproject.toml` - Modern Python package configuration (hatchling backend)
- `.github/workflows/python-package.yml` - CI pipeline testing Python 3.9-3.12
- `.readthedocs.yaml` - Read the Docs configuration
- `docs/requirements.txt` - Documentation dependencies (pywikipathways, bridgedbpy, nbsphinx)

### Tests (`tests/`)
- `test_download_pathway_archive.py`
- `test_find_pathway_by_text.py` 
- `test_find_pathways_by_xref.py`
- `test_get_pathway.py`

All tests follow the pattern: import module, call function with test data, assert results.

## Continuous Integration

**GitHub Actions Workflow** (`.github/workflows/python-package.yml`):
- Runs on: Ubuntu latest
- Python versions: 3.9, 3.10, 3.11, 3.12
- Steps: checkout → setup Python → install dependencies → install package → run pytest
- Triggers: On all pushes

## Common Issues and Workarounds

### Network Connectivity Issues
**Problem**: Pip timeouts when installing hatchling or build dependencies
**Solution**: Install dependencies manually: `pip install requests pandas lxml pytest`

**Problem**: Tests fail with connection errors
**Solution**: This is expected in environments without internet access. Tests require WikiPathways API connectivity.

### Package Installation Issues  
**Problem**: `pip install ./` fails with hatchling build errors
**Solution**: Use PYTHONPATH method for development work

### Documentation Build Issues
**Problem**: "Pandoc wasn't found" error
**Solution**: Install pandoc system package or skip documentation building for code changes

## Development Guidelines

### Making Changes
1. Always test imports first: `python -c "import pywikipathways"`
2. Run relevant tests after changes: `PYTHONPATH=. pytest tests/test_[module].py -v`
3. The package is a thin wrapper around HTTP requests - most functions follow the pattern:
   ```python
   def some_function(param):
       res = wikipathways_get('apiEndpoint', {'param': param, 'format': 'json'})
       return process_response(res)
   ```

### API Pattern
All functions use `utilities.wikipathways_get()` which:
- Makes HTTP GET requests to `https://webservice.wikipathways.org`
- Handles JSON/text responses
- Returns None on errors (with error printing)

### Dependencies
- **requests**: HTTP client for API calls
- **pandas**: Data manipulation for API responses
- **lxml**: XML parsing for pathway data

## File System Layout

```
/
├── .github/workflows/python-package.yml  # CI configuration
├── .readthedocs.yaml                     # Documentation hosting config
├── pyproject.toml                        # Package configuration
├── README.md                             # Main documentation
├── LICENSE                               # MIT license
├── pywikipathways/                       # Main package
│   ├── __init__.py                       # Package imports
│   ├── utilities.py                      # HTTP client core
│   ├── _version.py                       # Version info
│   └── [15 API modules]                  # Individual API functions
├── tests/                                # Test suite
│   └── [4 test files]                    # pytest-based tests
└── docs/                                 # Documentation
    ├── conf.py                           # Sphinx configuration
    ├── index.rst                         # Main docs
    ├── requirements.txt                  # Doc dependencies
    └── [3 Jupyter notebooks]             # Tutorial notebooks
```

## Trust These Instructions

These instructions have been validated through comprehensive repository exploration. Only search for additional information if:
1. The instructions are incomplete for your specific task
2. You encounter errors not covered in the "Common Issues" section
3. You need to understand code patterns not documented here

The development workflow using PYTHONPATH is the most reliable method for this repository.