# M1.1 — First synthetic family transfer: implementation contract

**Phase:** P0 only · **Issuer:** none · **No live funds** · **Status:** SPECIFICATION / NOT IMPLEMENTED · **Date:** 20 November 2026

## Goal and acceptance scenario
A synthetic sender in a provincial Philippine household authorizes transfer of **₱1,000.00** to a synthetic urban relative. Quote shows **₱15.00 total illustrative fee**. The sender's test liability decreases **₱1,015.00**; recipient's test liability increases **₱1,000.00**; an illustrative provider fee payable increases **₱12.00**; and an illustrative platform revenue account increases **₱3.00**. Every number is fake, fixed for an example only and **must not be advertised as a real commercial rate**.

The simulator demonstrates authorization, a held balance, one logical provider instruction, pending/unknown outcomes, confirmed simulation, separate reconciliation and a receipt. No tokens, real peso reserves, external payment initiation or KYC/PII are involved.

## Fixed units and ledger postings
- Currency `PHP`; `minor_unit=centavo`; amounts stored as signed **integer centavos**, never floating point.
- Fixed seeded account identities: `DEMO_SENDER_AVAILABLE`, `DEMO_SENDER_HELD`, `DEMO_RECIPIENT_AVAILABLE`, `DEMO_PROVIDER_FEE_PAYABLE`, `DEMO_PLATFORM_REVENUE`, `DEMO_ASSET`.
- Seed: Dr `DEMO_ASSET` 200000; Cr `DEMO_SENDER_AVAILABLE` 200000.
- Authorization hold: Dr `DEMO_SENDER_AVAILABLE` 101500; Cr `DEMO_SENDER_HELD` 101500.
- Successful settlement: Dr `DEMO_SENDER_HELD` 101500; Cr `DEMO_RECIPIENT_AVAILABLE` 100000; Cr `DEMO_PROVIDER_FEE_PAYABLE` 1200; Cr `DEMO_PLATFORM_REVENUE` 300.
- Failure before settlement: Dr `DEMO_SENDER_HELD` 101500; Cr `DEMO_SENDER_AVAILABLE` 101500, attached to an explicit compensating batch.
- **Invariants:** per-posting batch sum Dr = sum Cr, entries append-only, no negative spendable synthetic sender funds, no duplicate hold/settle/refund, same simulation reference on linked events.
- Fee breakdown is a **test fixture**, not a promise to use the same revenue split in a later commercial product.

## State machine
`DRAFT -> QUOTED -> AUTHORIZED -> SUBMITTED -> PENDING -> SIM_SETTLED -> RECONCILED`.
Error/recovery branches: `QUOTE_EXPIRED`, `REJECTED`, `PENDING_UNKNOWN` (do not resubmit), `EXCEPTION`, `FAILED_RELEASED` (compensating hold release), `RECONCILIATION_EXCEPTION` (not complete). `SIM_SETTLED` is not equivalent to independent reconciliation or cash received in the real world.

## Endpoints (Cloudflare staging *only*)
- `POST /v1/sandbox/quotes`: validate synthetic actor, recipient, amount and currency; returns gross, net, fee breakdown, expiry and quote ID.
- `POST /v1/sandbox/transfers`: requires `Idempotency-Key`, quote ID, simulation authorization and user identity. Atomically create request, reserved hold batch and durable outbox instruction; replay returns same transfer ID and no new hold.
- `GET /v1/sandbox/transfers/{id}`: role-restricted state, timestamps, provider simulation reference, reconciliation state and receipt if completed.
- `POST /v1/sandbox/provider-events` **internal adapter only**: signed synthetic fixture event with event ID, match on exact transfer ID; reject or quarantine unrecognized/out-of-order events.
- `POST /v1/sandbox/reconciliation/run` **internal scheduled actor only**: deterministic comparison of transfer, ledger posting and simulated provider facts. Independent of settlement callback.
- `GET /v1/sandbox/evidence/{id}` **reviewer role**: redacted audit trail and batch invariants.

All mutation endpoints must validate authentication, actor resource access, authorization scope, payload/fee and quote expiry server-side. Backend service secrets only; no direct client writes to financial tables.

## Supabase data model and access constraints
Use a private PostgreSQL schema `sandbox_finance` **not exposed through Data API** and separate from any future production ledger. Versioned migrations define:
`demo_personas`, `demo_quotes`, `demo_accounts`, `demo_posting_batches`, `demo_journal_entries`, `demo_transfers`, `demo_outbox`, `demo_provider_events`, `demo_reconciliation_runs`, `demo_audit_events`.

- Every financial posting is atomic; journal entry immutability enforced in DB, not UI only. Invariant check at commit; immutable event IDs and unique `(actor_id, idempotency_key)`.
- Nonnegative amounts and valid account categories, fixed currency, unique synthetic provider references, status transition guard and reconciliation provenance.
- All tables have RLS enabled even in private schema; no public Data API grants. Access via scoped server component only, with role checks and least privilege.
- All fixtures are fake, e.g. `PERSONA_PROVINCE_001`, `PERSONA_CITY_002`, no phone numbers, ID docs, accounts or real secrets.
- Keep financial book authoritative for accounting facts, simulated provider for mock settlement evidence; don't silently rewrite either.

## AI Studio deliverable
Mobile-first 3-screen prototype (quote, confirmation/pending, receipt/error) following Symbol 05 palette. Demonstrate readable totals, fake-money banner, accessible state and recovery. Export committed UI spec and screenshot-based human review evidence. No Google AI Studio production credentials or customer data.

## Cloudflare deliverable
Private staging Worker API; environment scoped secrets; rate limits, least-privilege backend authorization, request IDs, structured redacted logs, health probe and recovery playbook. Public site must not expose financial test endpoints without access controls.

## Simulator deliverable
Deterministic provider adapter implementing exactly one logical submission per transfer and scenarios: `SUCCESS`, `TIMEOUT_UNKNOWN`, `DUPLICATE_CALLBACK`, `REJECTION`, `OUT_OF_ORDER_EVENT`, `LATE_SUCCESS`, `SERVICE_UNAVAILABLE`. No provider sandbox keys or external requests in default tests.

## Automated test contract
T01 exact quote fee and expiry; T02 double-entry seed/hold/settle balances; T03 duplicate transfer API idempotency; T04 duplicate callback deduplication; T05 unknown timeout stays pending without resubmission; T06 expired quote cannot authorize; T07 insufficient funds fails without hold; T08 malicious actor cannot see another persona; T09 provider failure posts linked release exactly once; T10 late/out-of-order event safely quarantined; T11 independently reconciled status only when all records agree; T12 mismatch raises exception; T13 journal immutable; T14 restore backup and re-run ledger/reconciliation invariants; T15 no real funds, keys or PII in build; T16 UI shows pending vs reconciled and prominent simulation label.

## Exit / evidence
- Clean GitHub PR with 2 reviewers for financial-path changes where collaborators permit (otherwise document independent external review without claiming branch protection).
- Schema migration and rollback/recovery plan; deterministic fixtures; unit, integration and failure tests.
- UI test screenshot checklist; Cloudflare API simulation trace and Supabase staging reconciliation output.
- One end-to-end sample report from quote through independent reconciliation and a failure/timeout report.
- PPKT VERIFY returns `M1.1_TECHNICAL_READY` only after all technical evidence, while G0–G7 and F0 remain blocked.
- **Explicit exclusions:** public launch, wallet funding, real remittance, actual bank data, unlicensed payment operations, investments, mainnet contracts, PCCO rewards or fiat redemption.
