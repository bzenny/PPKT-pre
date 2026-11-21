# Technical blueprint | deliberately **not an implementation**

**Current layer:** repository charter/brand evidence and checker. No database project, Cloudflare Worker, Google AI Studio prototype, wallet, token contracts or secrets are deployed by this package.

```text
GitHub CORE (versioned controls + CI)
       │
       ├── Google AI Studio: UI prototype using synthetic data only
       ├── Cloudflare: future public site, API front door, rate limiting, analytics
       └── Supabase: future auth, isolated financial ledger, RLS, evidence, outbox
                        │
                        ├── simulation provider adapter (first)
                        └── legal-approved partner adapter (later)
                               └── optional chain testnet adapter (only if justified)
```

**Boundary contracts:**
- Browser/UI is untrusted. It requests quotes/actions, but does not insert or amend financial journal rows.
- Cloudflare API validates identity, scope, amounts, input schemas, rate limits and idempotency. Keep privileged keys server-side, never in browser or in repository.
- Supabase Postgres is the operational source for journal/obligations, with transactions, append-only accounting events, role enforcement, RLS when exposed, unique request IDs and durable outbox/attempt log. A database field called `reserved` is not legal asset segregation.
- Providers expose finality, reversal, fees, errors and status query. A timeout is unknown, **not a failed transfer**; never automatically resend with a new ID.
- Blockchain, if justified later, establishes chain events only; not legal rights, fiat settlement, identity, or reserve backing by itself.
- Role boundaries should exist independent of frameworks and vendors so providers/networks can be replaced. Prefer a modular monolith initially.

**Future build gates:** write `schema.sql` only after G0 corporate/financial rights mapped and approved; no live SQL migrations or credentials in this foundation. For any exposed Supabase tables, enable and test RLS and grants, owner-scoped policies, SECURITY INVOKER where appropriate, and protect signing keys outside ordinary app roles. Use GitHub Actions checks, protected environment secrets and independently reviewed promotion.

**AI Studio role:** ideation/wireframes and copy/user tests only. Prototype UX with synthetic values; no financial authorization, not a source for regulatory statements or authoritative balances.
