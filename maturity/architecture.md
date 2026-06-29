# Software Architecture Assessment (Advisory Lens)

> A diagnostic lens for judging whether a software project — especially a **web app** — is *architecturally sound* to become and sustain a Digital Public Good. **This is advisory, not a 10th indicator.** DPG eligibility is defined by the [9 indicators](./indicators.md) and the [tier model](./tier-model.md); the architecture review does **not** change the tier. It explains *why* certain indicators are strong or fragile and surfaces risks (e.g. cloud lock-in, no offline support) that the binary indicators miss.
>
> Read by the `dpg-assess` skill. Each dimension is scored **strong / adequate / weak / n/a** with evidence. Automated signals come from `scripts/audit/run_audit.py` → `checks.architecture`; the skill combines them with reading the repo.

## How architecture relates to the indicators

Architecture quality clusters under five indicators: **4** (platform independence), **5** (documentation), **6** (data extraction), **8** (standards & best practices), **9A** (data privacy & security). A dimension scored `weak` is a flag to re-examine the related indicator's evidence — but it never overrides the indicator's own status.

## The 12 dimensions

### 1. Modularity & separation of concerns — *(4, 5, 8)*
**Good:** loosely-coupled modules with clear layer boundaries (presentation / business / data); shared logic factored out; no circular deps. **Signals:** clear directory separation (`api/`, `services/`, `web/`, `data/`); ADRs; absence of duplicated business logic.

### 2. API-first & interoperability — *(4, 5, 8)*
**Good:** functionality exposed via documented, versioned APIs with machine-readable specs (OpenAPI/AsyncAPI/JSON Schema); stable, backwards-compatible contracts; open protocols. **Signals:** `openapi*.yaml`/`swagger*`, `/api/v1/` versioning, generated API docs.

### 3. Platform independence / cloud-agnosticism — *(4)*
**Good:** runs on any cloud or on-prem; containerized; infra-as-code; no hard dependency on proprietary cloud services, or such deps abstracted behind adapters with documented open alternatives; config externalized (12-factor). **Signals:** `Dockerfile`, `docker-compose`, `helm/`, `k8s/`, `*.tf`; counts of `azure`/`aws`/`gcp` SDK refs in manifests; `.env.example`. **Weak =** pervasive single-cloud SDK usage with no abstraction (a direct indicator-4 risk).

### 4. Scalability & performance — *(8)*
**Good:** stateless services / externalized sessions; async processing (queues/workers); documented caching; horizontal scaling. **Signals:** message-queue libs, cache (Redis), load-test scripts, stateless deployment.

### 5. Offline & low-connectivity resilience — *(8; inclusion)*
**Good:** client caching (IndexedDB/local storage), request queueing + idempotent sync, retry/backoff, small payloads; offline UX. **Signals:** service workers (`sw.js`, `workbox*`), web app manifest, sync/retry code. **Especially important** for field tools in low-connectivity / global-South contexts.

### 6. Localization & accessibility — *(7, 8, 9)*
**Good:** externalized i18n strings, locale-aware formatting, RTL support; WCAG 2.1 AA (semantic HTML, keyboard nav, alt text, contrast, ARIA). **Signals:** i18n libs/locale files (`locales/`, `en.json`/`fr.json`, `*.po`); axe/Lighthouse configs. Accessibility is a legal requirement in many jurisdictions and a do-no-harm concern.

### 7. Security architecture — *(7, 8, 9A)*
**Good:** OIDC/OAuth2 auth (not custom), declarative RBAC, MFA for sensitive ops; **no secrets in git** (verified by gitleaks/trufflehog); external secrets store; encryption in transit & at rest; pinned deps + SBOM + dependency/SAST scanning; OpenSSF Scorecard passing. **Signals:** OIDC/Keycloak config, RBAC tests, `gitleaks` clean, SBOM files, SAST workflow, Scorecard score.

### 8. Data portability & open formats — *(6, 4, 7)*
**Good:** non-PII data exportable/importable in non-proprietary formats (CSV/JSON/XML, or domain standards like GeoJSON/FHIR); documented schema; round-trips losslessly; GDPR Art. 20 addressed. **Signals:** `/export`/`/download` endpoints, documented data dictionary, no bulk export locked to proprietary formats.

### 9. Testing & CI/CD — *(8, 5, 9A)*
**Good:** test pyramid (unit > integration > E2E), deterministic tests, tracked coverage; CI runs tests + lint + SAST + dependency scan on every commit; mandatory review; tagged, signed releases. **Signals:** test dirs/files, `.github/workflows/*`, coverage config, branch protection, release tags.

### 10. Observability — *(8, 5, 9)*
**Good:** structured logs (JSON, correlation IDs), correct log levels, metrics (latency/error/throughput), dashboards + alerting, distributed tracing. **Signals:** structured-logging libs (serilog/winston/pino), OpenTelemetry, Prometheus/Grafana configs.

### 11. Documentation — *(5, 8)*
**Good:** README (incl. getting-started + structure), `ARCHITECTURE.md`/ADRs, API docs, deployment & ops runbooks, data dictionaries. **Signals:** `ARCHITECTURE.md`, `docs/adr*`, per-component READMEs, diagrams, deployment docs.

### 12. Maintainability & community — *(3, 5, 8)*
**Good:** clear ownership/governance (CODEOWNERS, GOVERNANCE.md), responsive triage, semantic versioning + changelog, issue/PR templates, marked deprecations. **Signals:** `CODEOWNERS`, `GOVERNANCE.md`, `CHANGELOG*`, release cadence, templates.

## Scoring

Per dimension: `strong` (clear, multiple signals + good practice), `adequate` (present but partial/undocumented), `weak` (largely absent or anti-patterns), `n/a` (doesn't apply — justify). Summarize **strengths**, **risks** (weak dimensions that endanger a DPG indicator), and a short **recommendations** list. Do not let architecture change the DPG tier — instead, in the gap report note e.g. *"Indicator 4 is partial; architecturally the cloud lock-in (dimension 3 = weak) is the root cause."*

## Sources

| Source | URL |
|---|---|
| DPG Standard | https://www.digitalpublicgoods.net/standard |
| GovStack architecture specs | https://specs.govstack.global/architecture |
| GovStack interoperability | https://specs.govstack.global/architecture/4-interoperability-architecture |
| Principles for Digital Development | https://digitalprinciples.org/ |
| WCAG 2.1 | https://www.w3.org/TR/WCAG21/ |
| 12-Factor App | https://12factor.net/ |
| OpenSSF Scorecard checks | https://github.com/ossf/scorecard/blob/main/docs/checks.md |
| OpenAPI Specification | https://swagger.io/specification/ |
| GDPR right to data portability (Art. 20) | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-data-portability/ |
| Enhanced Privacy Framework (DPGA) | https://www.digitalpublicgoods.net/dpg-privacy-report |
| Practical Test Pyramid (Fowler) | https://martinfowler.com/articles/practical-test-pyramid.html |
| OpenTelemetry | https://opentelemetry.io/docs/ |
| DPG Charter (DIAL) | https://dial.global/work/charter-for-digital-public-goods/ |
| UNDP — DPI & the SDGs | https://www.undp.org/digital/digital-public-infrastructure |

> Some URLs were collected via automated research; verify before citing externally. The DPGA / GovStack / Principles / WCAG / OpenSSF / 12-factor / OpenAPI links are authoritative.
