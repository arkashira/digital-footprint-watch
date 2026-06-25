import datetime
import pytest
from digital_footprint import ResultStore, SearchResult


def test_deduplication():
    store = ResultStore()
    now = datetime.datetime.utcnow()
    results = [
        SearchResult(url="http://example.com/a", snippet="A", timestamp=now),
        SearchResult(url="http://example.com/b", snippet="B", timestamp=now),
        SearchResult(url="http://example.com/a", snippet="A duplicate", timestamp=now),
    ]
    store.add_results(results)
    stored = store.get_all()
    assert len(stored) == 2
    urls = {r.url for r in stored}
    assert urls == {"http://example.com/a", "http://example.com/b"}


def test_empty_add():
    store = ResultStore()
    store.add_results([])
    assert store.get_all() == []
