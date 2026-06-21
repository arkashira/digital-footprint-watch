# Requirements.md – digital-footprint-watch

## 1. Overview
**digital-footprint-watch** is a personal digital‑footprint management tool that continuously searches, aggregates, and monitors a user’s publicly available data across multiple online platforms (social networks, forums, code repositories, news sites, etc.).  
The system notifies the user of new exposures, outdated personal information, and potential privacy risks, and provides actionable remediation steps.

The requirements below are derived from the repository context, existing Axentx infrastructure, and validated market need for automated personal data monitoring.

---

## 2. Functional Requirements

| ID | Description |
|----|-------------|
| **FR‑1** | **User Account Management** – Users must be able to register, log in, reset password, and delete their account. Authentication shall use OAuth 2.0 (Google, Apple, Microsoft) and optional email/password fallback. |
| **FR‑2** | **Profile Configuration** – After login, users can add, edit, or remove “digital identities” (e.g., usernames, email addresses, phone numbers) and select which platforms to monitor (e.g., Twitter, Reddit, GitHub, LinkedIn, public search engines). |
| **FR‑3** | **Search Engine Integration** – The system shall query each selected platform’s public API (or scrape public pages when no API exists) for occurrences of the user’s identifiers. Queries must be performed at configurable intervals (default: once per 24 h). |
| **FR‑4** | **Result Aggregation & De‑duplication** – All matches returned from different platforms must be normalized, de‑duplicated, and stored with metadata (source, timestamp, URL, snippet). |
| **FR‑5** | **Risk Scoring** – Each aggregated result shall be scored (0‑100) based on sensitivity (e.g., personal email vs. public tweet) and exposure recency. The scoring algorithm must be configurable via a JSON rule set. |
| **FR‑6** | **User Dashboard** – A responsive web UI must display: <br>• Summary risk score <br>• Timeline of new findings <br>• Filters by platform, date, score <br>• Ability to mark items as “resolved” or “ignore”. |
| **FR‑7** | **Notification System** – Users receive real‑time alerts (email & push) when a new finding exceeds a configurable risk threshold (default ≥ 70). Notification content includes a short description and a direct link to the source. |
| **FR‑8** | **Remediation Guidance** – For each high‑risk finding, the system suggests concrete actions (e.g., “request removal from site X”, “update privacy settings”). Guidance data is stored in a curated knowledge base. |
| **FR‑9** | **Export / Data Portability** – Users can export their entire footprint history (JSON or CSV) and import it into another instance of the product. |
| **FR‑10** | **Audit Log** – All user‑initiated actions (login, config changes, dismissals) and system‑generated events (search runs, detections) must be logged with tamper‑evident timestamps for compliance. |
| **FR‑11** | **Admin Console** – Internal admins can view system health, manage platform API credentials, and manually trigger a full re‑crawl for a specific user. |
| **FR‑12** | **Privacy‑by‑Design Data Handling** – All user‑provided identifiers are stored encrypted at rest; raw search results are retained only for the retention period selected by the user (default 90 days). |

---

## 3. Non‑Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | • Initial full‑scan of up to 20 identifiers across 10 platforms must complete ≤ 30 minutes. <br>• Incremental scans (only new data) must complete ≤ 5 minutes. |
| **NFR‑2** | **Scalability** | System must support ≥ 10 000 concurrent users with average 2 identifiers each, scaling horizontally via container orchestration (K8s). |
| **NFR‑3** | **Reliability** | • 99.9 % uptime SLA for the public API and dashboard. <br>• Automatic retry with exponential back‑off for failed platform queries (max 3 attempts). |
| **NFR‑4** | **Security** | • All traffic encrypted TLS 1.3+. <br>• Secrets (API keys, DB passwords) stored in Vault‑compatible secret manager. <br>• Regular (monthly) penetration testing and OWASP Top 10 compliance. |
| **NFR‑5** | **Data Privacy** | • GDPR‑compliant data deletion on user request within 24 h. <br>• No data is sold or shared with third parties. |
| **NFR‑6** | **Observability** | • Structured logs (JSON) shipped to centralized logging (e.g., Loki). <br>• Metrics exposed via Prometheus (search latency, error rates, queue depth). <br>• Alerting on SLA breaches via Alertmanager. |
| **NFR‑7** | **Maintainability** | • Codebase follows Axentx C‑Framework conventions. <br>• Unit test coverage ≥ 80 % for core modules; integration tests for each platform connector. |
| **NFR‑8** | **Internationalization** | UI must support English and be easily extensible to additional locales via i18n JSON files. |
| **NFR‑9** | **Accessibility** | Dashboard must meet WCAG 2.1 AA criteria (keyboard navigation, ARIA labels, contrast). |
| **NFR‑10** | **Compliance** | Must support export of audit logs in standard formats (JSON‑L, CSV) for legal requests. |

---

## 4. Constraints

1. **Platform API Limits** – Must respect rate limits of each external platform; implement adaptive throttling per API key.
2. **Legal Scraping** – For platforms without public APIs, scraping must obey `robots.txt` and terms of service; fallback to manual user‑provided URLs only.
3. **Data Residency** – All user data must reside in EU‑region cloud storage for GDPR‑covered users.
4. **Technology Stack** – Must use Axentx‑approved components: <br>• Backend: Python 3.11 + FastAPI <br>• Async task queue: Celery 5 with Redis broker <br>• Database: PostgreSQL 15 (encrypted at rest) <br>• Frontend: React 18 + TypeScript <br>• Containerization: Docker + Kubernetes (v1.28).  
5. **Third‑Party Dependencies** – Only libraries with permissive licenses (MIT, Apache‑2.0, BSD) may be used to avoid licensing conflicts with existing datasets.

---

## 5. Assumptions

| ID | Assumption |
|----|------------|
| **A‑1** | Users possess at least one publicly searchable identifier (e.g., email, username). |
| **A‑2** | External platforms provide either a public API or allow limited unauthenticated scraping. |
| **A‑3** | The risk‑scoring rule set will be iteratively refined based on early user feedback; initial version uses a static JSON file. |
| **A‑4** | Users will opt‑in to receive email/push notifications; opt‑out is respected per GDPR. |
| **A‑5** | The underlying Axentx knowledge base (pgvector) will be leveraged for similarity matching of newly discovered snippets to known sensitive patterns. |
| **A‑6** | The product will launch in English first; localization will be added after product‑market fit is validated. |
| **A‑7** | The system will operate under the assumption that the user’s device (browser) is up‑to‑date and supports modern web standards. |

---

## 6. Acceptance Criteria (High‑Level)

1. A new user can register, configure identifiers, and receive the first scan results within 30 minutes.
2. The dashboard correctly displays aggregated findings, risk scores, and allows marking items as resolved.
3. Notifications are sent only when the risk score exceeds the user‑defined threshold.
4. All personal identifiers are encrypted at rest; audit logs show access events with tamper‑evident timestamps.
5. System maintains ≥ 99.9 % uptime over a 30‑day monitoring window in staging.
6. Security review passes OWASP Top 10 checklist; no critical findings remain open.

--- 

*Document version: 1.0 – 2026‑06‑21*
