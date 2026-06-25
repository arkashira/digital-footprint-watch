# digital-footprint-watch

A minimal Python project that crawls public mentions of a developer's verified email address
using Bing and Google Custom Search APIs. The crawler runs every 24 hours, de‑duplicates
results, stores them with source URL, snippet, and timestamp, and retries failed
requests up to three times.

## Features

- **Scheduled crawling** – runs automatically every 24 hours.
- **Multi‑source search** – queries both Bing and Google Custom Search APIs.
- **Deduplication** – stores each unique URL only once.
- **Retry logic** – retries failed API calls up to three times.
- **In‑memory storage** – results are kept in a simple list (replaceable with a DB).

## Installation
