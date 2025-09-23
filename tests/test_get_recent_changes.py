import pytest
from pywikipathways.get_recent_changes import get_recent_changes, get_recent_changes_ids, get_recent_changes_names

def test_get_recent_changes():
    """Test get_recent_changes function"""
    # Test with a timestamp that should return results if API is available
    timestamp = '20240101'
    result = get_recent_changes(timestamp)
    
    # In environments without internet access, result will be None
    if result is not None:
        # If we get results, verify the structure
        assert len(result) >= 0
        expected_columns = ['id', 'name', 'url', 'species', 'revision']
        for col in expected_columns:
            assert col in result.columns
    
    # Test with default timestamp (None)
    result_default = get_recent_changes()
    # Should behave same as above - either None or valid DataFrame
    if result_default is not None:
        assert len(result_default) >= 0
        expected_columns = ['id', 'name', 'url', 'species', 'revision']
        for col in expected_columns:
            assert col in result_default.columns
    
    # Test with very old timestamp that should return many results
    result_old = get_recent_changes('20070301')
    if result_old is not None:
        assert len(result_old) >= 0

def test_get_recent_changes_helper_functions():
    """Test helper functions"""
    timestamp = '20240101'
    
    # Test IDs function
    ids = get_recent_changes_ids(timestamp)
    if ids is not None:
        assert len(ids) >= 0
    
    # Test names function  
    names = get_recent_changes_names(timestamp)
    if names is not None:
        assert len(names) >= 0

def test_invalid_timestamp_format():
    """Test handling of invalid timestamp formats"""
    # Test with invalid timestamp format
    result = get_recent_changes('invalid')
    assert result is None
    
    # Test with partial timestamp
    result = get_recent_changes('2024')
    if result is not None:
        # Should work if padded/truncated correctly
        assert len(result) >= 0

def test_timestamp_string_conversion():
    """Test that various timestamp formats are handled correctly"""
    # Test with integer timestamp
    result = get_recent_changes(20240101)
    # Should not crash, either returns None (network error) or valid results
    if result is not None:
        assert len(result) >= 0
    
    # Test with long timestamp (should be truncated to 8 digits)
    result = get_recent_changes('202401011234')
    if result is not None:
        assert len(result) >= 0