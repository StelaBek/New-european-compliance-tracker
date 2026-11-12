# European Product Compliance Intelligence — new architecture (prototype)

**Goal:** evidence-first European product compliance monitoring. **This is not yet a complete national legal database ingestion service.** The design explicitly measures missing coverage, rather than stating that a successful homepage fetch means a country's law is covered.

## What runs today

- Separate Streamlit dashboard, source-health matrix and document candidate list.
- Direct official metadata ingestion for selected EU, UK, Germany, Norway and Sweden endpoints; success must be checked through live logs. These are *partial* sources, not national legal archives.
- Exact official document links accepted only when the link is on the registered publisher domain.
- Country registry for EU and European jurisdictions, exposing missing connections.
- Product category tagging (heuristic only) for furniture, toys, textiles, materials, machinery, electronics, packaging and other ecommerce sectors.
- Scheduled GitHub Actions scan with a committed JSON snapshot (public source metadata only). No Google News.
- Source status and findings separated from legal amendment verification. No automatic claim of legal approval.

## What is NOT delivered yet

- Complete official legal database ingestion for all European jurisdictions.
- Guaranteed detection of every new law and every amendment, including backfills, promulgation, consolidated-text versioning and multilingual texts.
- Legally verified compliance decisions without expert review. This cannot be guaranteed by an automatic summarizer.
- Full legal-text parsing for PDFs and document/version diffing.

## Setup

1. Create a **new** GitHub repository and upload **the contents** of this folder, including hidden `.github/workflows/scan.yml`.
2. Deploy via https://share.streamlit.io using `app.py` on `main`.
3. In GitHub, check Settings → Actions → General → Workflow permissions: allow read/write if needed.
4. Run Actions → **Scan official legislation sources** → **Run workflow** (branch `main`).
5. Inspect **Country coverage** and workflow logs. A successful GitHub job means the script ran, not that every source succeeded.
6. Locally: `pip install -r requirements.txt && python scan.py && streamlit run app.py`.
7. Tests: `pytest -q`.

## Development roadmap to the requested coverage

1. **Source inventory:** Contract per jurisdiction: legal gazette URLs, regulator sources, access/license, update cadence, publication index, API credentials and permissions.
2. **Connector implementation:** Proper APIs, bulk datasets, RSS/Atom, paginated official site endpoints and permitted scraping, with language-specific support.
3. **Complete backfill + reconciliation:** Monthly official published-count comparisons; verify both source coverage and date-range completeness; revision-aware deduplication and historical regression tests.
4. **Law change engine:** Version snapshots, article-level changes, repeal and amendment relations, effective dates, exemptions and transposition rules.
5. **Product applicability:** SKU/category/material/market mapping with grounded obligations, excerpts and exact legal citations. AI can assist but not certify legal interpretation.
6. **QA and expert approval:** Precision/recall against an independently curated legislative dataset; legal reviewer sign-off; audit logs; change alerts; retention/privacy controls.
7. **Operations:** Replace Git-tracked JSON with managed database + queue/job scheduler for higher volume, retries, audit trail, alert history and role-based access.

## Important operational notes

- The supplied source endpoints may change, rate-limit, or return a feed inconsistent with expectations. Failed scans show errors.
- Some jurisdictions may require accounts, paid access or negotiated data licenses.
- Avoid storing confidential SKU or supplier information in a public GitHub repository.
- The dashboard does not make decisions to block SKUs, certify products or replace legal counsel.
