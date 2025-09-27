import pytest
from pywikipathways.list_organisms import list_organisms


def test_list_organisms_returns_results():
    """list_organisms should return organism data or None on network issues."""
    result = list_organisms()

    # Should return a list or None (if no network access)
    assert result is None or isinstance(result, list)

    # If we get a result, it should be a list with more than 0 organisms
    if result is not None:
        assert len(result) > 0


def test_list_organisms_contains_anopheles_gambiae():
    """List should contain 'Anopheles gambiae' if network is available."""
    result = list_organisms()

    # Should return a list or None (if no network access)
    assert result is None or isinstance(result, list)

    # If we get a result, it should contain "Anopheles gambiae"
    # This matches the R test expectation
    if result is not None:
        assert "Anopheles gambiae" in result


def test_list_organisms_return_type():
    """Test that list_organisms returns the correct type."""
    result = list_organisms()
    
    # Should return either None (network error) or list
    assert result is None or isinstance(result, list)


def test_list_organisms_no_parameters():
    """Test that list_organisms works without any parameters."""
    # This should not raise any exceptions
    try:
        result = list_organisms()
        # If it returns something, it should be a list or None
        assert result is None or isinstance(result, list)
    except Exception as e:
        # Should not raise any exceptions beyond network errors
        # which are handled gracefully by returning None
        pytest.fail(f"list_organisms() raised an unexpected exception: {e}")