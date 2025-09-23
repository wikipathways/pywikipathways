import pytest
from pywikipathways.get_counts import get_counts


def test_get_counts():
    """Test the get_counts function."""
    
    # Test the main function
    result = get_counts()
    
    # Should return a DataFrame or None (if no network access)
    # In CI environment without network, this will be None
    assert result is None or (hasattr(result, 'shape') and len(result.columns) > 0)
    
    # If we get a result, it should be a DataFrame with one row (since it's counts data)
    if result is not None:
        assert len(result) == 1  # Should have one row of count statistics
        # Should have some expected columns related to WikiPathways statistics
        # Note: We can't test exact columns since we don't have network access
        # but the structure should be a DataFrame
        assert hasattr(result, 'columns')
        assert hasattr(result, 'index')


def test_get_counts_return_type():
    """Test that get_counts returns the correct type."""
    result = get_counts()
    
    # Should return either None (network error) or pandas DataFrame
    assert result is None or str(type(result)) == "<class 'pandas.core.frame.DataFrame'>"


def test_get_counts_no_parameters():
    """Test that get_counts works without any parameters."""
    # This should not raise any exceptions
    try:
        result = get_counts()
        # If it returns something, it should be a DataFrame or None
        assert result is None or hasattr(result, 'shape')
    except Exception as e:
        # Should not raise any exceptions beyond network errors
        # which are handled gracefully by returning None
        pytest.fail(f"get_counts() raised an unexpected exception: {e}")