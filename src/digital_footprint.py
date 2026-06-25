import logging
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List, Protocol, runtime_checkable
from abc import ABC, abstractmethod
import threading


@dataclass
class SearchResult:
    url: str
    snippet: str
    timestamp: datetime


@runtime_checkable
class SearchClient(Protocol):
    @abstractmethod
    def search(self, query: str) -> List[SearchResult]:
        """Return a list of SearchResult for the given query."""


class ResultStore:
    """In-memory store that deduplicates results by URL."""

    def __init__(self) -> None:
        self._results: List[SearchResult] = []

    def add_results(self, results: List[SearchResult]) -> None:
        existing_urls = {r.url for r in self._results}
        for res in results:
            if res.url not in existing_urls:
                self._results.append(res)
                existing_urls.add(res.url)

    def get_all(self) -> List[SearchResult]:
        return list(self._results)


class Crawler:
    """Crawl public mentions of an email address using provided search clients."""

    def __init__(
        self,
        email: str,
        clients: List[SearchClient],
        store: ResultStore,
        logger: logging.Logger | None = None,
    ) -> None:
        self.email = email
        self.clients = clients
        self.store = store
        self.logger = logger or logging.getLogger(__name__)

    def run_once(self) -> None:
        """Execute a single crawl cycle."""
        for client in self.clients:
            attempts = 0
            while attempts < 3:
                try:
                    results = client.search(self.email)
                    # Attach current timestamp to each result
                    now = datetime.utcnow()
                    for r in results:
                        r.timestamp = now
                    self.store.add_results(results)
                    break  # success, move to next client
                except Exception as exc:
                    attempts += 1
                    self.logger.warning(
                        f"Client {client.__class__.__name__} failed on attempt {attempts}: {exc}"
                    )
                    if attempts >= 3:
                        self.logger.error(
                            f"Client {client.__class__.__name__} failed after 3 attempts."
                        )
                    else:
                        time.sleep(0.1)  # small backoff


class Scheduler:
    """Runs a crawler at a fixed interval."""

    def __init__(self, crawler: Crawler, interval_seconds: int = 86400) -> None:
        self.crawler = crawler
        self.interval = interval_seconds
        self._timer: threading.Timer | None = None
        self._stopped = threading.Event()

    def _run(self) -> None:
        if not self._stopped.is_set():
            self.crawler.run_once()
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()

    def start(self) -> None:
        if self._timer is None:
            self._stopped.clear()
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()

    def stop(self) -> None:
        self._stopped.set()
        if self._timer:
            self._timer.cancel()
            self._timer = None
