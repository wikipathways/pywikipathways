# Updated find_pathways_by_literature Usage Examples

The `find_pathways_by_literature` function has been updated to work with the new JSON API. Here are usage examples:

## Basic Usage

```python
from pywikipathways.find_pathways_by_literature import find_pathways_by_literature

# Search for pathways related to cancer
results = find_pathways_by_literature('cancer')
if results is not None:
    print(f"Found {len(results)} pathways related to cancer")
    print(results.head())
else:
    print("No pathways found or network error")

# Search by PMID
results = find_pathways_by_literature('15134803')

# Search by author name  
results = find_pathways_by_literature('Schwartz GL')

# Search by journal
results = find_pathways_by_literature('Eur J Pharmacol')
```

## Using Helper Functions

```python
from pywikipathways.find_pathways_by_literature import (
    find_pathway_ids_by_literature,
    find_pathway_names_by_literature, 
    find_pathway_urls_by_literature
)

# Get just the pathway IDs
pathway_ids = find_pathway_ids_by_literature('diabetes')
if pathway_ids is not None:
    print("Pathway IDs:", list(pathway_ids))

# Get just the pathway names
pathway_names = find_pathway_names_by_literature('diabetes')
if pathway_names is not None:
    print("Pathway names:", list(pathway_names))

# Get just the pathway URLs
pathway_urls = find_pathway_urls_by_literature('diabetes')
if pathway_urls is not None:
    print("Pathway URLs:", list(pathway_urls))
```

## Migration from Old API

**Old implementation (deprecated):**
- Used web service API with server-side filtering
- Returned complex nested JSON structure with score objects

**New implementation:**
- Uses static JSON file with all pathway literature data
- Implements client-side filtering for better flexibility
- Returns cleaner DataFrame structure
- Better error handling and graceful degradation

The function signature and basic usage remain the same for backward compatibility.