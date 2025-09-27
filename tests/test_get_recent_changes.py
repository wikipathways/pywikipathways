import pytest
from pywikipathways.get_recent_changes import get_recent_changes, get_recent_changes_ids, get_recent_changes_names

def test_get_by_date():
    info = get_recent_changes('20180201000000')
    # Should not crash, either returns None (network error) or valid results
    assert len(info) > 0
