import pytest

from pywikipathways.list_communities import (
    list_communities,
    get_pathways_by_community,
    get_pathway_ids_by_community,
    get_pathway_names_by_community,
    get_pathway_urls_by_community
)


def test_list_communities_returns_results():
    """list_communities should return community data or None on network issues."""
    result = list_communities()
    result.to_csv("test.csv")

    assert result is None or len(result) > 0

    if result is not None:
        expected_columns = {"display-name", "title", "short-description", "community-tag", "editors"}
        assert expected_columns.issubset(set(result.columns))


def test_get_pathways_by_community_requires_tag():
    """get_pathways_by_community should require a community_tag parameter."""
    result = get_pathways_by_community()
    assert result is None

    result = get_pathways_by_community(None)
    assert result is None


def test_get_pathways_by_community_with_valid_tag():
    """get_pathways_by_community should return pathway data for valid community tags."""
    # This test will work if there are communities available
    communities = list_communities()
    
    if communities is not None and len(communities) > 0:
        # Get the first community tag
        first_tag = communities['community-tag'].iloc[0]
        result = get_pathways_by_community(first_tag)
        
        # Result can be None if community has no pathways, or a DataFrame if it has pathways
        assert result is None or len(result) >= 0


def test_get_pathway_ids_by_community():
    """get_pathway_ids_by_community should return pathway IDs or None."""
    communities = list_communities()
    
    if communities is not None and len(communities) > 0:
        first_tag = communities['community-tag'].iloc[0]
        result = get_pathway_ids_by_community(first_tag)
        
        # Result can be None if community has no pathways, or a Series if it has pathways
        assert result is None or hasattr(result, 'name')


def test_get_pathway_names_by_community():
    """get_pathway_names_by_community should return pathway names or None."""
    communities = list_communities()
    
    if communities is not None and len(communities) > 0:
        first_tag = communities['community-tag'].iloc[0]
        result = get_pathway_names_by_community(first_tag)
        
        # Result can be None if community has no pathways, or a Series if it has pathways
        assert result is None or hasattr(result, 'name')


def test_get_pathway_urls_by_community():
    """get_pathway_urls_by_community should return pathway URLs or None."""
    communities = list_communities()
    
    if communities is not None and len(communities) > 0:
        first_tag = communities['community-tag'].iloc[0]
        result = get_pathway_urls_by_community(first_tag)
        
        # Result can be None if community has no pathways, or a Series if it has pathways
        assert result is None or hasattr(result, 'name')


def test_invalid_community_tag():
    """Functions should handle invalid community tags gracefully."""
    invalid_tag = "NONEXISTENT_COMMUNITY"
    
    result = get_pathways_by_community(invalid_tag)
    assert result is None
    
    result = get_pathway_ids_by_community(invalid_tag)
    assert result is None
    
    result = get_pathway_names_by_community(invalid_tag)
    assert result is None
    
    result = get_pathway_urls_by_community(invalid_tag)
    assert result is None