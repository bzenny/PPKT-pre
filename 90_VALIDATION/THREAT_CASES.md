# Minimum adversarial scenarios to instrument in future app tests

- Credential theft, malicious insider, delegated access escalation.
- Duplicate request, replayed or out-of-order provider event, rollback after external finality.
- Unknown callback, stale quote, dropped settlement, payout rejected after token burn.
- Ledger double-posting, missing evidence, reserve deficit, account takeover.
- User council wallet splitting, vote capture, unverified identity and conflicts.
- KDef 4/7 unauthorized path, compromised signers, misleading fund reports.
- Public exposure of KYC or personal data; abuse of customer support recovery.
- Missing/expired partner permission, marketing without disclosures or inaccurate issuance claim.

Each applicable scenario needs an owner, independent reviewer, fixture and signed result before the associated module can be released.
