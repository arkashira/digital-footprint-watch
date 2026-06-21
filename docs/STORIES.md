# STORIES.md – digital-footprint-watch

## Overview
**Product:** *digital-footprint‑watch* – a personal digital‑footprint management tool that automates search and monitoring across multiple platforms (social media, forums, code repositories, news sites, etc.).  
**Goal:** Enable users to discover, review, and act on any public data that references them, reducing reputational risk and improving personal brand control.

---

## Epics & Backlog

| Epic | Description | MVP Priority |
|------|-------------|--------------|
| **E1 – Account & Platform Integration** | Connect user accounts and configure which public platforms to monitor. | 1 |
| **E2 – Automated Footprint Discovery** | Crawl, index, and surface public mentions of the user across selected platforms. | 1 |
| **E3 – Alerting & Notification** | Notify users of new mentions with configurable channels and severity. | 2 |
| **E4 – Insight & Sentiment Dashboard** | Visualise trends, sentiment, and exposure over time. | 3 |
| **E5 – Action & Remediation** | Provide quick actions (request removal, comment, archive) directly from the UI. | 4 |
| **E6 – Privacy & Data Governance** | Ensure GDPR‑compliant data handling, user consent, and data‑export. | 5 |
| **E7 – Enterprise & Team Sharing** (future) | Allow shared monitoring for teams or brands. | 6 |

---

## User Stories

### Epic E1 – Account & Platform Integration
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E1‑01** | **As a new user, I want to sign‑up with email or OAuth, so that I can start using the service securely.** | 1. Sign‑up page offers email/password and Google/GitHub OAuth.<br>2. Email verification link is sent and must be confirmed before first login.<br>3. Password must meet minimum complexity (8 chars, upper, lower, digit). |
| **E1‑02** | **As a user, I want to link my social‑media accounts (Twitter, Instagram, LinkedIn) and code profiles (GitHub, GitLab), so that the system can monitor those sources.** | 1. “Add Platform” wizard lists supported platforms.<br>2. OAuth flow stores a read‑only token securely (encrypted at rest).<br>3. User can view linked accounts and revoke any connection. |
| **E1‑03** | **As a user, I want to select which public platforms to monitor, so that I only receive relevant data.** | 1. Checkbox list of all supported platforms (including “Custom RSS/Website”).<br>2. At least one platform must be selected to enable monitoring.<br>3. Selections are persisted to the user profile. |
| **E1‑04** | **As a user, I want to set a “monitoring frequency” (daily, hourly, real‑time), so that I control how often new data is fetched.** | 1. Dropdown with three options.<br>2. Frequency is stored per‑user and respected by the background crawler.<br>3. Changing the setting updates the next scheduled run without service restart. |

### Epic E2 – Automated Footprint Discovery
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E2‑01** | **As a system, I need to crawl public APIs and web pages for mentions of the user’s identifiers (username, email hash, domain), so that we can build a searchable index.** | 1. Crawl jobs are queued per‑user based on selected platforms and frequency.<br>2. Each job stores raw result (URL, timestamp, snippet) in the `mentions` table.<br>3. Duplicate detection (same URL & snippet) prevents redundant entries. |
| **E2‑02** | **As a user, I want to see a list of recent mentions with source, date, and snippet, so that I can quickly assess relevance.** | 1. Paginated table view (20 rows per page).<br>2. Columns: Platform, Source URL (clickable), Date, Snippet, Sentiment (auto‑computed).<br>3. “Mark as read/unread” toggle persists per‑mention. |
| **E2‑03** | **As a system, I need to run language detection and basic sentiment analysis on each snippet, so that users can filter by tone.** | 1. Use a lightweight model (e.g., VADER) to assign sentiment score – Positive, Neutral, Negative.<br>2. Sentiment stored alongside the mention record.<br>3. API endpoint `/mentions?sentiment=negative` returns filtered results. |

### Epic E3 – Alerting & Notification
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E3‑01** | **As a user, I want to configure alert thresholds (e.g., any negative mention, >5 mentions per day), so that I’m only notified when it matters.** | 1. UI to set “Notify on any negative sentiment” (boolean).<br>2. UI to set “Daily mention count > X” (numeric).<br>3. Settings saved and applied to the alert engine. |
| **E3‑02** | **As a user, I want to receive alerts via email and/or push notification, so that I can act promptly.** | 1. Checkbox for Email, Push (Web‑Push).<br>2. Test button sends a sample alert.<br>3. Real alerts contain: Platform, URL, snippet, and direct link to the dashboard. |
| **E3‑03** | **As a system, I need to batch‑process alerts at the end of each monitoring cycle, so that we don’t overload the notification service.** | 1. All new mentions for a user are evaluated against their thresholds.<br>2. If any condition matches, a single aggregated notification is sent (list of up‑to‑5 items).<br>3. Notification logs are persisted for audit. |

### Epic E4 – Insight & Sentiment Dashboard
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E4‑01** | **As a user, I want a time‑series chart of total mentions per week, so that I can see trends.** | 1. Chart displays last 12 weeks by default, with zoom option.<br>2. Hover shows exact count per week.<br>3. Data source is the aggregated `mentions` table. |
| **E4‑02** | **As a user, I want a sentiment breakdown (pie or bar) for the selected period, so that I understand overall tone.** | 1. Shows percentages of Positive / Neutral / Negative.<br>2. Clicking a segment filters the mention list accordingly. |
| **E4‑03** | **As a user, I want to export my mention data (CSV/JSON), so that I can perform offline analysis.** | 1. Export button respects current filters (date range, platform, sentiment).<br>2. Generated file includes: Platform, URL, Date, Snippet, Sentiment, Read‑status. |

### Epic E5 – Action & Remediation
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E5‑01** | **As a user, I want a one‑click “Request Removal” button for supported platforms, so that I can start takedown processes quickly.** | 1. Button appears only for platforms that expose a DMCA/takedown API (e.g., GitHub).<br>2. Clicking opens a pre‑filled request modal; user confirms and submits.<br>3. Request status (Pending/Completed/Failed) is stored and displayed. |
| **E5‑02** | **As a user, I want to add a private note to any mention, so that I can record context or next steps.** | 1. Inline “Add note” field per mention.<br>2. Notes are encrypted at rest and only visible to the owner.<br>3. Notes appear in the mention detail view. |
| **E5‑03** | **As a user, I want to archive a mention (hide from active view), so that I can keep my dashboard clean while preserving the record.** | 1. Archive action moves the mention to an “Archived” tab.<br>2. Archived items are searchable but not included in default dashboards/alerts. |

### Epic E6 – Privacy & Data Governance
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E6‑01** | **As a user, I want to delete my entire account and all collected data, so that I can exercise my right to be forgotten.** | 1. “Delete Account” button triggers a confirmation flow.<br>2. Upon confirmation, all user‑related rows (profile, mentions, notes, alerts) are permanently removed.<br>3. Email confirmation is required before deletion proceeds. |
| **E6‑02** | **As a system, I need to store all personal data encrypted at rest and limit access to service accounts, so that we comply with GDPR.** | 1. Encryption keys are managed via AWS KMS (or equivalent).<br>2. Access logs record every read/write to personal tables.<br>3. Regular audit script verifies no plaintext data exists. |
| **E6‑03** | **As a user, I want to download a GDPR‑compliant data export (all personal data in machine‑readable format), so that I can keep a copy for my records.** | 1. Export includes profile, linked platforms, mentions, notes, and alert settings.<br>2. Generated ZIP is encrypted with a user‑provided password.<br>3. Export link expires after 24 h. |

### Epic E7 – Enterprise & Team Sharing (Future)
| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E7‑01** | **As a team admin, I want to invite members to a shared monitoring workspace, so that we can collectively manage a brand’s footprint.** | 1. Invite flow sends email with a one‑time token.<br>2. Admin can assign roles (Viewer, Editor, Admin). |
| **E7‑02** | **As a team member, I want to see aggregated mentions for the whole organization, with filters per sub‑brand, so that I can focus on my area.** | 1. Dashboard supports multi‑tenant view with brand tags.<br>2. Permissions enforce visibility based on role. |

---

## Prioritisation for MVP (Release 1.0)

1. **E1‑01, E1‑02, E1‑03, E1‑04** – Core onboarding & platform selection.  
2. **E2‑01, E2‑02** – Basic crawling and mention list.  
3. **E3‑01, E3‑02** – Simple alert thresholds and email notifications.  
4. **E4‑01, E4‑02** – Minimal insight dashboard (trend + sentiment).  
5. **E5‑02, E5‑03** – Note & archive actions (remediation optional for MVP).  
6. **E6‑01, E6‑02, E6‑03** – GDPR compliance foundations.  

*Future releases* will extend to advanced remediation (E5‑01), richer platform support, and enterprise sharing (E7).

--- 

*End of STORIES.md*
