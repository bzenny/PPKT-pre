# Interface contract catalog (v0.2 proposed)

**Common request** (not an API to real money): `request_id`, `idempotency_key`, `actor`, `module`, `policy_version`, `amount_minor`, `currency`, `recipient_reference`, `consent_reference`, `created_at`, `evidence_id`.

**Status response:** `provider_reference`, `state` (`requested|validated|authorized|submitted|pending_unknown|confirmed|reconciled|exception`), `fees_minor`, `provider_timestamp`, `settlement_evidence_ref`, `reconciliation_evidence_ref`.

**Financial invariants:** amounts are integer minor units; for each posted journal transaction sum(debits)=sum(credits); no hard-delete of posted journals; original obligation remains outstanding until independently evidenced settlement; no double-charge on repeated inputs; no admin overrides without immutable history.

**Security/data:** no private keys, bearer tokens, raw identity documents, email addresses or sensitive IDs in open events or public blockchain. All external connectors map to a versioned adapter manifest and have simulated failure tests.
