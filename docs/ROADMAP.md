# Roadmap for **digital-footprint-watch**
*Personal digital footprint management tool that automates search and monitoring across multiple platforms.*

---  

## Vision
Empower individuals to understand, control, and reduce their online exposure by providing a unified, automated, privacy‑first monitoring service for social media, forums, code repositories, and public data sources.

---

## MVP (Must‑Have for Launch) – **Release 0.1**

| Milestone | Description | Acceptance Criteria | Owner |
|-----------|-------------|---------------------|-------|
| **Core Data Connectors** | Build reliable scrapers/APIs for the top 5 platforms (Twitter/X, LinkedIn, GitHub, Reddit, Google Search). | • Data fetched within 5 min of request.<br>• Rate‑limit handling & back‑off implemented.<br>• GDPR‑compliant consent flow. | Backend |
| **Search & Index Engine** | Store fetched items in a searchable vector store (using **vLLM** for fast similarity search). | • Index updates within 2 min of new data.<br>• Query latency < 500 ms for 10 k results.<br>• Basic fuzzy & boolean operators. | Architecture / Backend |
| **User Dashboard (Web UI)** | Simple React SPA showing “Recent Findings”, “Risk Score”, and “Export” button. | • Auth via email + magic‑link.<br>• Responsive layout (mobile‑first).<br>• Export results as CSV/JSON. | Front‑end |
| **Risk Scoring Engine** | Heuristic model that scores each finding (exposure, sensitivity, recency). | • Scores 1‑10 displayed next to each item.<br>• Configurable weighting in admin UI. | Data Science |
| **Alerting (Email)** | Daily digest of new high‑risk items (score ≥ 7). | • Delivered ≤ 30 min after scan.<br>• Unsubscribe link compliant with CAN‑SPAM. | DevOps |
| **Compliance & Security Baseline** | End‑to‑end encryption at rest & in transit, GDPR data‑deletion endpoint. | • All PII encrypted with AES‑256.<br>• Data‑deletion request processed within 24 h. | Security |
| **Observability** | Basic metrics (scrape success, latency, error rates) + alerting. | • Grafana dashboards + PagerDuty alerts for > 5 % error rate. | DevOps |

**MVP‑Critical Items**: Core Data Connectors, Search & Index Engine, User Dashboard, Risk Scoring, Compliance baseline.  
Alerting & Observability are required for production stability but can be minimal.

---

## Phase 1 – **Version 1.0** (Quarter 2 2026)

**Theme:** *Depth & Personalization*

| Feature | Description | MVP Impact | Owner |
|---------|-------------|------------|-------|
| **Expanded Platform Support** | Add Instagram, TikTok, Facebook, StackOverflow, and public data‑broker sites. | Increases coverage to > 90 % of personal identifiers. | Backend |
| **Customizable Watchlists** | Users tag keywords, usernames, or domains to monitor. | Improves relevance of results. | Front‑end |
| **Advanced Risk Model (ML)** | Train a lightweight classifier on the **instr‑resp** dataset to predict “privacy impact”. | Replaces heuristic scoring, higher precision. | Data Science |
| **Real‑time Push Notifications** | Web‑push & SMS (Twilio) for critical findings (score ≥ 9). | Faster user reaction. | DevOps |
| **Bulk Export & API** | Public REST endpoint for programmatic access to a user’s findings. | Enables integration with 3rd‑party privacy tools. | Backend |
| **User Settings & Data Retention Policies** | Choose retention period (30 d, 90 d, indefinite) and auto‑purge. | Aligns with privacy regulations. | Front‑end |
| **Beta Analytics Dashboard** | Trend graphs (exposure over time, platform breakdown). | Gives users actionable insights. | Front‑end |

**Success Metrics**  
- 5 k active users by end of Q2.  
- 80 % of users create at least one watchlist.  
- Reduction in high‑risk findings > 30 % after ML scoring rollout.

---

## Phase 2 – **Version 2.0** (Quarter 4 2026)

**Theme:** *Automation & Enterprise Enablement*

| Feature | Description | Owner |
|---------|-------------|-------|
| **Automated Remediation Suggestions** | Generate “take‑down” request templates, privacy‑setting guides, or code‑snippet removal steps. | Product |
| **Browser Extension** | Inline badge on visited pages indicating presence of user data. | Front‑end |
| **Team & Family Plans** | Shared watchlists, role‑based permissions, centralized billing. | PM / Backend |
| **Enterprise SSO & SCIM** | Azure AD, Okta integration for corporate deployments. | Security |
| **Marketplace Integration** | Plug‑in SDK for third‑party data sources (e.g., data‑broker APIs). | Architecture |
| **Compliance Reporting** | GDPR/CCPA audit reports downloadable per user. | Security |
| **AI‑Powered Summaries** | Use **SGLang** to produce natural‑language summaries of daily digests. | Data Science |

**Success Metrics**  
- $10 k MRR from team/family subscriptions.  
- 20 % of enterprise trial users convert to paid.  
- 90 % of remediation suggestions result in successful data removal (tracked via follow‑up scans).

---

## Phase 3 – **Version 3.0** (2027 H1)

**Theme:** *Proactive Protection & Ecosystem*

| Feature | Description | Owner |
|---------|-------------|-------|
| **Predictive Exposure Forecasting** | Time‑series model forecasting future exposure based on trends. | Data Science |
| **Zero‑Trust Personal Vault** | Encrypted local vault for storing sensitive documents, synced with monitoring engine. | Security |
| **Community‑Driven Threat Intel** | Crowdsourced indicator sharing (hashes, URLs) with reputation scoring. | Product |
| **Voice‑Assistant Integration** | Alexa/Google‑Assistant skill to query “What new data is out there about me?”. | Front‑end |
| **Regulatory Change Alerts** | Notify users when new laws affect their data rights. | PM |
| **Open‑Source SDK** | Allow developers to embed footprint monitoring into their apps. | Architecture |

**Success Metrics**  
- 30 % of users adopt the Personal Vault.  
- Forecast accuracy > 80 % (MAE).  
- SDK adopted by ≥ 10 external projects.

---

## Release Cadence & Governance

| Cycle | Duration | Deliverables | Review Gate |
|-------|----------|--------------|-------------|
| **Sprint** | 2 weeks | Feature branch, unit tests, CI pass | Engineering Lead |
| **Beta Sprint** | 4 weeks | End‑to‑end QA, internal beta sign‑up | QA Lead |
| **Release Candidate** | 1 week | Documentation, security audit | Reviewer (hard‑gate) |
| **Production Deploy** | Continuous (canary) | Monitoring dashboards active | Ops Lead |

All releases must pass:

1. **Security Review** – static analysis, dependency scanning, GDPR compliance check.  
2. **Performance SLA** – search latency ≤ 500 ms, scrape success ≥ 95 %.  
3. **User Acceptance** – ≥ 80 % of beta participants rate the feature “useful”.  

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Platform API rate limits / policy changes | Service disruption | Build adaptive back‑off, maintain fallback scrapers, monitor API deprecation notices. |
| Data privacy lawsuits | Legal/brand damage | Strict consent flow, data‑deletion SLA, regular legal audit. |
| ML model bias / false positives | User distrust | Human‑in‑the‑loop review for high‑risk scores, continuous model retraining with validated feedback. |
| Scaling of vector store | Latency blow‑up | Partition index by user, use vLLM’s sharding, auto‑scale on demand. |
| Competition releasing similar free tools | Market share loss | Focus on automation & remediation, enterprise features, and strong privacy guarantees. |

---

## Appendix

- **Primary Tech Stack**: React + Vite, FastAPI, PostgreSQL, vLLM (vector store), SGLang (structured generation), Docker + Kubernetes (EKS), Terraform (IaC).  
- **Datasets Utilized**: `auto`, `instr-resp`, `messages`, `query-resp` for training the risk classifier and summarization models.  
- **Related Repos**: `arkashira/surrogate-1-harvest` (data pipeline utilities), `vllm-project/vllm` (inference engine).  

---  

*Prepared by the Senior Product/Engineering Lead – Axentx*
