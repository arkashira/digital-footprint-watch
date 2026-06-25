import datetime
import logging
import pytest
from digital_footprint import (
    Crawler,
    ResultStore,
    SearchResult,
    SearchClient,
)


class MockClient(SearchClient):
    """Mock client that returns preset results."""

    def __init__(self, results: list[SearchResult]) -> None:
        self._results = results

    def search(self, query: str) -> list[SearchResult]:
        return list(self._results)


class FlakyClient(SearchClient):
    """Client that fails a set number of times before succeeding."""

    def __init__(self, fail_times: int, results: list[SearchResult]) -> None:
        self.fail_times = fail_times
        self.attempts = 0
        self._results = results

    def search(self, query: str) -> list[SearchResult]:
        if self.attempts < self.fail_times:
            self.attempts += 1
            raise RuntimeError("Simulated failure")
        return list(self._results)


class AlwaysFailClient(SearchClient):
    """Client that always fails."""

    def search(self, query: str) -> list[SearchResult]:
        raise RuntimeError("Always fails")


@pytest.fixture
def store() -> ResultStore:
    return ResultStore()


def test_happy_path(store):
    client_a = MockClient(
        [
            SearchResult(url="http://example.com/a", snippet="A", timestamp=datetime.datetime.utcnow()),
            SearchResult(url="http://example.com/b", snippet="B", timestamp=datetime.datetime.utcnow()),
        ]
    )
    client_b = MockClient(
        [
            SearchResult(url="http://example.com/b", snippet="B duplicate", timestamp=datetime.datetime.utcnow()),
            SearchResult(url="http://example.com/c", snippet="C", timestamp=datetime.datetime.utcnow()),
        ]
    )
    crawler = Crawler("dev@example.com", [client_a, client_b], store)
    crawler.run_once()
    results = store.get_all()
    assert len(results) == 3
    urls = {r.url for r in results}
    assert urls == {"http://example.com/a", "http://example.com/b", "http://example.com/c"}
    # Ensure timestamps are set to now (within a reasonable delta)
    now = datetime.datetime.utcnow()
    for r in results:
        assert abs((now - r.timestamp).total_seconds()) < 5


def test_retry_logic(store, caplog):
    caplog.set_level(logging.WARNING)
    client = FlakyClient(
        fail_times=2,
        results=[
            SearchResult(url="http://example.com/d", snippet="D", timestamp=datetime.datetime.utcnow()),
        ],
    )
    crawler = Crawler("dev@example.com", [client], store)
    crawler.run_once()
    results = store.get_all()
    assert len(results) == 1
    assert results[0].url == "http://example.com/d"
    # Two warnings should have been logged
    warnings = [rec for rec in caplog.records if rec.levelno == logging.WARNING]
    assert len(warnings) == 2
    assert "attempt 1" in warnings[0].message
    assert "attempt 2" in warnings[1].message


def test_failure_after_three_attempts(store, caplog):
    caplog.set_level(logging.ERROR)
    client = AlwaysFailClient()
    crawler = Crawler("dev@example.com", [client], store)
    crawler.run_once()
    results = store.get_all()
    assert len(results) == 0
    errors = [rec for rec in caplog.records if rec.levelno == logging.ERROR]
    assert len(errors) == 1
    assert "failed after 3 attempts" in errors[0].message
