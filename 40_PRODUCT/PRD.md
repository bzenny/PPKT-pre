# Product requirements: synthetic family transfer (MVP 0)

**Status:** design hypothesis, no real funds. **User:** a person in a Philippine province wishing to transfer value to family in a city. **Need:** understandable fees, clear recipient result and recoverable exceptions without speculative ownership.

**Must-have demonstrator:** (1) clear sender/recipient identity and permissions, (2) whole fee and pay-out amount quote in PHP simulation, (3) explicit confirmation, (4) stable idempotency ID, (5) ledger reservation/obligation and balanced journal, (6) pending/unknown simulator, (7) provider result and independent reconciliation, (8) receipt or exception/support case, (9) accessible mobile and low-bandwidth journey. English and Filipino copy should be validated with users, not auto-declared accessible.

**Out of scope:** live transfer, KYC of real people, storing identifiable documents in test fixtures, active bank connections, minted PPKT, PCCO sale/staking/interest, KDef treasury operations, DEX/bridge, deposit-taking or lending.

**Acceptance examples:** exactly one logical payout for repeated client requests; callbacks duplicate-safe and reordered; provider timeout remains UNKNOWN with no automatic second transfer; user-facing state mirrors recorded truth; reconciliation closes only when original obligation and external settlement agree; restore+replay preserves amounts and unfulfilled liabilities; fraud/abuse and complaint workflow observable.

**Success measurements (research hypotheses):** task completion, errors per journey, total proposed transfer cost, time until recipient can use funds, complaint turnaround, user comprehension and support burden. Compare against licensed/non-crypto alternatives using comparable conditions and timestamps; no market superiority is currently established.
