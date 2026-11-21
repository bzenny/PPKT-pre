> **NAME CONFIRMED (21 November 2026):** The project and intended token are named **PPKT** (PH Probinsyano Token). The name is finalized; actual token issuance, symbol registration/listing, chain selection, and corporate/legal authorization remain separate decisions. Read [Tokenomics v0.3](40_PRODUCT/PPKT_TOKENOMICS_v0_3.md), [Reserve/Fee v0.4](40_PRODUCT/PPKT_RESERVE_FEES_v0_4.md) and [PCCO v0.2](40_PRODUCT/PCCO_COMMUNITY_ECONOMICS_v0_2.md) and [Chain Decision](50_BUILD/ADR-0002_CHAIN_SHORTLIST.md) before introducing chain-specific code.

> **NOVEMBER 20, 2026 UPDATE:** PPKT-pre is the incubator. Parent-company domicile is **not selected**; Singapore and Dubai are jurisdictions for evaluation. No partner financing, corporate formation, licence, token issuance or user-fund operations are confirmed.

# PH Probinsyano Token / PPKT — PPKT-pre Foundation

**State: PRE-RATIFICATION / SIMULATION ONLY** · 20 November 2026  
**Purpose:** Corporate, product, governance, brand, evidence and validation baseline before application development.

> **No issued PPKT/PCCO token, licensed activity, signed partner, registered OperatingCo, funded KDef, verified reserves or publicly launched product is claimed.** This project is not an investment solicitation, an offer of financial instruments, or proof of authorization. All sample values are synthetic.

## One-minute orientation

1. Open [`MASTER.html`](MASTER.html) — visual navigation and current authority state.
2. Read [`00_PRIME/PRIME.html`](00_PRIME/PRIME.html) and [`CONTEXT.md`](CONTEXT.md) — who/what controls decisions.
3. Review [`30_CHARTER/PPKT_Building_Charter_v0_2.md`](30_CHARTER/PPKT_Building_Charter_v0_2.md) — proposed charter and schedules; **not ratified**.
4. Review [`95_RECORDS/decisions.json`](95_RECORDS/decisions.json) — recorded draft choices and required human approvals.
5. Review [`20_BRAND/brand-standard.html`](20_BRAND/brand-standard.html) and [`20_BRAND/design-tokens.json`](20_BRAND/design-tokens.json) — selected Symbol 05 identity, production vector work pending.
6. Review [`40_PRODUCT/PRD.md`](40_PRODUCT/PRD.md) and [`50_BUILD/ARCHITECTURE.md`](50_BUILD/ARCHITECTURE.md).
7. Run tests; separately assess release-readiness. Passing CI is *not* permission to launch.

## Automated checks

Requires **Python 3.11+**; no third-party Python dependencies.

```bash
python -m unittest discover -s tests -v
python scripts/check_core.py
python scripts/release_readiness.py --report /tmp/ppkt-readiness.json
# The last command prints BLOCKED until real evidence exists; use --enforce only in release workflow.
```

## MasterSys CORE / ICM practice

**FOLDERS → HTML → Markdown → JSON → YAML.** Files convey scope, canonical documents convey human context, and machine records support checking. The chain is **not** a substitute for lawful human approval. `CORE` first; graduate to `STRUCTURED` and `INTELLIGENT` only when verified technical need justifies it. The repo holds one modular application boundary, not multiple microservices or autonomous agents.

## Repository map

- `00_PRIME` — human authority boundary, adoption prerequisites.
- `10_ARCHITECTURE` — folder/rule registry, fund/role and module contracts.
- `20_BRAND` — selected brand guide and reference art; concept art is *not* production vector.
- `30_CHARTER` — proposed v0.2 charter, authority matrix, corporate/product/governance drafts.
- `40_PRODUCT` — first user journey, customer rights, failure cases.
- `50_BUILD` — future Cloudflare/Supabase/AI Studio architecture; no live credentials or migrations.
- `60_EVIDENCE` — competitor hypotheses and measurement definitions.
- `70_DELIVERY` — GitHub-to-prelaunch staged roadmap and gate evidence records.
- `90_VALIDATION` — validator playbook, brand gate and threat scenario list.
- `95_RECORDS` — decisions, approval ledger and history.
- `scripts`, `tests`, `.github` — structural CI, evidence-only release gating and workflow templates.

## Important distinction

**GitHub CI green** means this documentation/scaffold remains internally consistent and its tests run; **G0–G7 blocked** means no approved commercial pre-launch. Do not configure financial production services from this draft alone. Legal counsel must confirm which financial licenses/authorities and disclosures apply to each actor and transaction.

## GitHub onboarding

**Public pre-release repository:** https://github.com/bzenny/PPKT-pre. Drafts must be proposed on branches and reviewed before any merge. The eventual official core release will have a separate adoption, release and repository decision. The private financial negotiation memo is not part of the public repository. **Do not upload `.env`, secrets, customer records or unreviewed financial claims.**

> **Jurisdiction / cost note:** Cost and jurisdiction: PH delivery is the preferred operating baseline, while Singapore/Dubai parent options remain under diligence. No unverified percentage is a public financial-performance claim.

## Current review and milestone (20 November 2026)
Charter **v0.2.3-RC1 is UNRATIFIED**; see `30_CHARTER/ARTICLE_REVIEW_v0_2_2.md` and `30_CHARTER/RATIFICATION_PACKET.md`. Development-only human D1 approval is distinct from any corporate/financial permission. Milestone 1.1 is a **design specification**, not an implemented service. See `40_PRODUCT/MILESTONE_1_1.md`. The complete synthetic module and external staging deployment have not yet been built.

## Brand review PDF
A visually reviewed, size-optimized 13-page Brand Standards PDF is committed as [`PPKT_Brand_Standards_v1_0_web.pdf`](PPKT_Brand_Standards_v1_0_web.pdf). The original lossless PDF is retained in the downloadable complete source package; the PDF is brand documentation, not financial authorization.


**Decision 21 November 2026:** Polygon Amoy (80002) is the chosen **testnet** only; switch or redesign before official launch if testing identifies issues. Neither Polygon mainnet nor any other mainnet has been adopted.
