# TECH_SPEC.md  

**Project:** digital-footprint-watch  
**Owner:** Axentx – Personal Digital Footprint Management Team  
**Status:** Specification (ready for implementation)  
**Last Updated:** 2026‑06‑21  

---  

## 1. Overview  

digital-footprint-watch (DFW) is a SaaS tool that continuously discovers, indexes, and monitors a user’s personal data across public and semi‑public online platforms (search engines, social networks, data‑broker sites, forums, code repositories, etc.).  

* **Goal:** Give individuals a single dashboard to view, filter, and act on their digital footprint, with automated alerts when new references appear or when existing references change risk level.  
* **Scope:**  
  * Automated crawling & API ingestion for ~30 high‑impact platforms (Google, Bing, DuckDuckGo, Twitter/X, Reddit, LinkedIn, GitHub, Pastebin, etc.).  
  * Normalisation & enrichment pipeline (entity extraction, sentiment, risk scoring).  
  * Secure, privacy‑first storage of discovered artefacts.  
  * Real‑time alerting via email, SMS, or push notification.  
  * User‑facing web UI + RESTful API for integration.  

---  

## 2. Architecture Overview  

```
+-------------------+      +-------------------+      +-------------------+
|   Front‑End (SPA) | <--->|   API Gateway     | <--->|   Auth Service    |
+-------------------+      +-------------------+      +-------------------+
                                 |
                                 v
                         +-------------------+
                         |   Orchestrator    |  (Celery Beat / Airflow)
                         +-------------------+
                                 |
        +------------------------+------------------------+
        |                        |                        |
        v                        v                        v
+----------------+      +----------------+      +----------------+
|   Crawlers     |      |   Enrichers    |      |   Alert Engine |
| (vLLM‑based)   |      | (SGLang)       |      | (Rule‑based)   |
+----------------+      +----------------+      +----------------+
        |                        |                        |
        v                        v                        v
+---------------------------------------------------------------+
|                     Central Data Store (PostgreSQL)          |
+---------------------------------------------------------------+
        |
        v
+-------------------+      +-------------------+
|   Object Store    |<---->|   Search Index    |
| (MinIO / S3)      |      | (ElasticSearch)   |
+-------------------+      +-------------------+
```

* **Front‑End:** React + Vite SPA, served via CDN.  
* **API Gateway:** FastAPI (Python) – single entry point, request validation, rate‑limiting.  
* **Auth Service:** OAuth2 / OpenID Connect (Keycloak) – supports social login (Google, Apple) and email/password.  
* **Orchestrator:** Airflow (Docker‑Compose) schedules periodic crawls per user‑defined watchlist.  
* **Crawlers:**  
  * **Web search** – headless Chromium (Playwright) + custom parsers.  
  * **Platform APIs** – native SDKs (Twitter API v2, Reddit API, GitHub GraphQL, etc.).  
  * **LLM‑enhanced extraction** – vLLM inference engine (GPU‑accelerated) to summarise long pages.  
* **Enrichers:** Structured generation pipelines built with SGLang to extract entities (names, emails, usernames), sentiment, and compute a **Risk Score** (0‑100).  
* **Alert Engine:** Rules engine (Durable Rules) evaluates new/changed artefacts against user thresholds and triggers notifications via Twilio (SMS), SendGrid (email), or Firebase Cloud Messaging (push).  
* **Data Store:** PostgreSQL 15 (primary relational store).  
* **Object Store:** MinIO (S3‑compatible) for raw HTML, PDFs, screenshots.  
* **Search Index:** Elasticsearch 8.x for full‑text search and faceted filtering in UI.  

---  

## 3. Components & Responsibilities  

| Component | Language / Runtime | Key Libraries | Responsibilities |
|-----------|-------------------|----------------|------------------|
| **Front‑End** | TypeScript (React) | React‑Query, MUI, Redux Toolkit | Dashboard, watchlist CRUD, alert preferences, result browsing |
| **API Gateway** | Python 3.11 | FastAPI, Pydantic, Uvicorn, Redis (cache) | Auth validation, request routing, pagination, throttling |
| **Auth Service** | Java (Keycloak) | – | User identity, MFA, token issuance |
| **Orchestrator** | Python | Apache Airflow, Celery, Redis broker | Schedule crawls, monitor task health, retry logic |
| **Crawler Workers** | Python | Playwright, httpx, vLLM, beautifulsoup4 | Fetch raw content, store raw artefacts, produce metadata |
| **Enricher Workers** | Python | SGLang, spaCy, transformers (sentence‑transformers) | Entity extraction, sentiment, risk scoring |
| **Alert Engine** | Python | durable‑rules, Twilio SDK, SendGrid SDK, firebase‑admin | Evaluate rules, dispatch notifications |
| **PostgreSQL** | – | pgvector (for embedding storage) | Structured data, user profiles, artefact metadata |
| **MinIO** | – | – | Blob storage for raw files |
| **Elasticsearch** | – | – | Full‑text indexing, faceted search |
| **Monitoring** | – | Prometheus, Grafana, Loki | Metrics, logs, alerts on system health |

---  

## 4. Data Model  

### 4.1 Core Tables (PostgreSQL)

| Table | Primary Key | Important Columns | Description |
|-------|--------------|-------------------|-------------|
| `users` | `id` (UUID) | `email`, `hashed_pw`, `created_at`, `last_login` | Account data |
| `watchlists` | `id` (UUID) | `user_id`, `name`, `platforms[]`, `query`, `frequency` | User‑defined monitoring set |
| `artefacts` | `id` (UUID) | `watchlist_id`, `platform`, `url`, `title`, `snippet`, `discovered_at`, `last_seen_at`, `risk_score`, `status` | Individual discovered item |
| `artefact_embeddings` | `artefact_id` (FK) | `embedding` (vector) | For similarity search |
| `alerts` | `id` (UUID) | `user_id`, `artefact_id`, `type`, `sent_at`, `channel` | Notification history |
| `platform_credentials` | `id` (UUID) | `user_id`, `platform`, `encrypted_token`, `expires_at` | OAuth tokens for API access |

### 4.2 Object Store Layout  

```
/raw/{user_id}/{watchlist_id}/{artefact_id}/
    - page.html
    - screenshot.png
    - pdf.pdf (if applicable)
```

### 4.3 Search Index Mapping (Elasticsearch)

```json
{
  "mappings": {
    "properties": {
      "artefact_id": {"type": "keyword"},
      "user_id": {"type": "keyword"},
      "platform": {"type": "keyword"},
      "title": {"type": "text"},
      "content": {"type": "text"},
      "risk_score": {"type": "float"},
      "discovered_at": {"type": "date"},
      "embedding": {"type": "dense_vector", "dims": 384}
    }
  }
}
```

---  

## 5. Key APIs / Interfaces  

All endpoints are versioned under `/api/v1/`. Authentication via Bearer JWT.

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| `POST` | `/auth/login` | Issue JWT | `{email, password}` | `{access_token, refresh_token}` |
| `POST` | `/auth/refresh` | Refresh token | `{refresh_token}` | `{access_token}` |
| `GET` | `/watchlists` | List user watchlists | – | `[{id, name, platforms, query, frequency}]` |
| `POST` | `/watchlists` | Create watchlist | `{name, platforms[], query, frequency}` | `{id}` |
| `PUT` | `/watchlists/{id}` | Update watchlist | same as create | `200 OK` |
| `DELETE` | `/watchlists/{id}` | Delete watchlist | – | `204 No Content` |
| `GET` | `/artefacts` | Search artefacts (supports pagination, filters) | Query params: `platform`, `risk_min`, `risk_max`, `q` (full‑text) | `{hits, total, page}` |
| `GET` | `/artefacts/{id}` | Get artefact details | – | `{metadata, raw_url}` |
| `GET` | `/alerts` | List recent alerts | – | `[{id, artefact_id, type, sent_at, channel}]` |
| `POST` | `/alerts/test` | Send test notification (user‑selected channel) | `{channel, target}` | `202 Accepted` |

### Internal Service Calls  

* **Crawler → Orchestrator** – `POST /internal/crawl_complete` (JSON payload with artefact IDs).  
* **Enricher → Alert Engine** – `POST /internal/enrichment_done` (artefact ID, risk score, embeddings).  

All internal calls use mutual TLS and a shared service API key stored in Vault.

---  

## 6. Technology Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | Python 3.11 (backend), TypeScript (frontend) | Mature ecosystem, strong LLM libraries, fast dev cycles |
| **LLM Inference** | vLLM (GPU‑accelerated, supports quantised models) | Low latency summarisation & extraction |
| **Structured Generation** | SGLang | Enables deterministic entity extraction with controllable prompts |
| **Orchestration** | Apache Airflow (Docker) | Visual DAGs, easy schedule changes per user |
| **Task Queue** | Celery + Redis | Proven pattern for async workers |
| **Database** | PostgreSQL 15 + pgvector | Relational integrity + vector similarity |
| **Blob Storage** | MinIO (S3‑compatible) | On‑premise, cost‑effective, easy to replace with cloud S3 |
| **Search** | Elasticsearch 8.x | Scalable full‑text + vector search |
| **Auth** | Keycloak (OpenID Connect) | Enterprise‑grade, MFA, social login |
| **Containerisation** | Docker Compose (dev) → Helm charts (k8s prod) | Consistent environments |
| **Observability** | Prometheus + Grafana + Loki | Metrics, dashboards, log aggregation |
| **CI/CD** | GitHub Actions + ArgoCD (k8s) | Automated testing, canary deployments |
| **Security** | Vault for secrets, OWASP secure headers, GDPR‑compliant data deletion API | Privacy‑first product |

---  

## 7. Dependencies  

| Dependency | Version | License |
|------------|---------|---------|
| fastapi | 0.112.0 | MIT |
| uvicorn | 0.30.0 | BSD |
| sqlalchemy | 2.0.30 | MIT |
| asyncpg | 0.29.0 | PostgreSQL |
| playwright | 1.45.0 | MIT |
| vllm | 0.4.2 | Apache‑2.0 |
| sglang | 0.2.1 | Apache‑2.0 |
| elasticsearch-py | 8.13.0 | Apache‑2.0 |
| minio | 7.2.5 | Apache‑2.0 |
| keycloak-admin | 23.0.0 | Apache‑2.0 |
| durable‑rules | 2.0.0 | MIT |
| twilio | 9.2.2 | MIT |
| sendgrid | 6.11.0 | MIT |
| firebase-admin | 6.5.0 | Apache‑2.0 |
| prometheus‑client | 0.20.0 | Apache‑2.0 |
| grafana‑sdk | 1.0.0 | MIT |

---  

## 8. Deployment Architecture  

### 8.1 Production Environment (Kubernetes)  

```
Namespace: dfw-prod
 ├─ ingress-nginx (TLS termination)
 ├─ keycloak (stateful, external DB)
 ├─ api-gateway (FastAPI) – 3 replicas, HPA (CPU >70%)
 ├─ auth-service (Keycloak) – 2 replicas
 ├─ orchestrator (Airflow web + scheduler) – 1 replica each
 ├─ worker‑crawler (Celery) – 5 replicas (GPU node pool)
 ├─ worker‑enricher (Celery) – 5 replicas (GPU node pool)
 ├─ alert‑engine (Celery) – 2 replicas
 ├─ postgres‑primary (statefulset) – 2 replicas + Patroni
 ├─ minio (distributed) – 4 pods
 ├─ elasticsearch (statefulset) – 3 master + 2 data nodes
 ├─ redis (cache) – 2 replicas
 └─ prometheus + grafana (monitoring)
```

* **GPU Nodes** – NVIDIA A100 (or compatible) for vLLM & SGLang inference.  
* **Autoscaling** – Airflow DAGs trigger scaling of crawler/enricher workers based on queue depth.  
* **CI/CD Flow:**  
  1. PR merged → GitHub Actions run unit/integration tests.  
  2. Docker images built & pushed to internal registry.  
  3. ArgoCD syncs Helm releases to `dfw-prod`.  
  4. Canary rollout (5 % traffic) with automated health checks before full promotion.  

### 8.2 Development / Staging  

* Docker‑Compose stack mirroring production services (Postgres, MinIO, Elasticsearch, Redis).  
* Hot‑reload for FastAPI (`uvicorn --reload`).  
* Mock platform APIs (via WireMock) to avoid rate‑limit issues.  

---  

## 9. Security & Privacy  

1. **Data Minimisation** – Store only URLs, snippets (≤ 500 chars), and extracted entities. Raw pages are encrypted at rest (AES‑256) in MinIO.  
2. **User Consent** – Onboarding flow requires explicit consent to crawl public data on behalf of the user.  
3. **GDPR / CCPA** – `DELETE /users/{id}` triggers:  
   * Immediate removal of all artefacts, embeddings, and raw blobs.  
   * Asynchronous purge from Elasticsearch snapshots.  
4. **Transport Security** – All external and internal traffic over TLS 1.3.  
5. **Secret Management** – API keys, OAuth tokens stored in HashiCorp Vault; workers retrieve via short‑lived tokens.  
6. **Rate Limiting** – Per‑user API quota (configurable) to prevent abuse of third‑party platforms.  

---  

## 10. Observability  

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| `crawler_success_total` | Prometheus (worker) | < 95 % success over 5 min → alert |
| `enricher_latency_seconds` | Prometheus | > 2 s avg → scale workers |
| `alert_delivery_failure` | Loki logs | > 5 % failures → investigate |
| `db_connection_errors` | pg_exporter | > 0 → immediate |
| `cpu_utilization_gpu` | node exporter | > 85 % → add GPU node |

Dashboards:  
* **System Health** – CPU, memory, GPU utilisation, queue depth.  
* **User Activity** – New artefacts per day, risk score distribution.  
* **Alert Funnel** – Sent vs. delivered vs. opened.  

---  

## 11. Testing Strategy  

| Test Type | Scope | Tools |
|-----------|-------|-------|
| Unit | Individual functions (parsers, risk scoring) | pytest, hypothesis |
| Integration | API endpoints + DB migrations | testcontainers, httpx |
| End‑to‑End | Full crawl → enrichment → alert flow | Playwright (for UI), Locust (load) |
| Performance | vLLM inference latency, Elasticsearch query latency | wrk, custom benchmark scripts |
| Security | OWASP ZAP scan, secret leakage checks | zap, truffleHog |
| Regression | Snapshot of UI components | Storybook, jest |

Coverage target: **≥ 85 %** for backend, **≥ 80 %** for frontend.

---  

## 12. Roadmap (Post‑Launch)  

| Milestone | Timeline | Deliverable |
|-----------|----------|-------------|
| MVP Release | 2026‑09‑01 | Core crawling, dashboard, email alerts |
| Mobile Push Support | 2026‑11‑15 | FCM integration, native iOS/Android wrappers |
| Enterprise Admin Console | 2027‑02‑01 | Multi‑tenant, role‑based access, audit logs |
| AI‑Driven Risk Recommendations | 2027‑05‑01 | Suggest remediation actions (e.g., DMCA takedown) |
| Marketplace for 3rd‑Party Plugins | 2027‑08‑01 | SDK, sandboxed plugin execution |

---  

## 13. Glossary  

* **Artefact** – A discovered piece of content (web page, post, file) that references the user.  
* **Risk Score** – Numeric indicator (0‑100) derived from sentiment, exposure level, and platform sensitivity.  
* **Watchlist** – User‑defined set of queries/platforms to monitor.  
* **vLLM** – High‑throughput LLM inference engine used for summarisation and extraction.  
* **SGLang** – Structured generation language enabling deterministic LLM outputs.  

---  

*Prepared by:*  
Senior Product/Engineering Lead – digital-footprint-watch  
Axentx – Autonomous AI‑Workforce  

---
