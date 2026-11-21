# PPKT Treasury, Safeguarding and Redemption Playbook v0.1

**Status: proposed policy — not an attestation, incorporation, custody agreement, official bank commitment, regulatory approval or live payment instruction.**

## Separation of rights / ledgers
1. Protected customer reserve portfolio — issuer's legally documented segregation, enforceable customer rights and account contracts (verify by counsel).
2. Issuer equity / loss absorbing capital — funded by shareholders separately from tokenholder redemptions.
3. OperatingCo working capital — legitimate fees/financing. No borrowing from protected reserves.
4. PCCO grant/benefit pool — appropriations from realized eligible surplus and restricted grants only; program can make no unfunded voucher promises.
5. KDef — independent development stewardship funded without touching reserves.

For any eventual Singapore or Dubai ParentCo, contractually specify which legal entity owes holder PHP redemptions; where custody is; who holds title; how bankruptcy, bank insolvency, jurisdiction and PH customer protection operate. Overseas incorporation **alone** does not protect balances.

## Proposed reserve parameters (not yet ratified)
- Baseline 100% *eligible and accessible* backing of liabilities (including burned-but-unpaid redemptions) as legally defined; hold no PCCO, crypto, unsecured future capital pledge or speculative investment as eligible reserves.
- Start with cash; no investment of reserves in interest/yield programs without separately reviewed legal and risk policy.
- Two or more independent qualified counterparties as a goal; modeled bank limit **60%** maximum of eligible reserves per bank, with preapproved contingency and disclosed exceptions when a second provider is unavailable.
- Daily independent reconciliation against original signed bank/issuer statements plus onchain supply and full liability ledger.
- Annual external audit and **proposed monthly reserve/liability assurance**; scope, standards and frequency to be resolved with issuer/regulator.
- **Proposed** issuer-only capital/stress buffer of at least 5% of projected eligible liabilities as a budgeting scenario, NOT a statutory threshold or substitute for 100% backing.
- Cash access buckets: immediately payable operating liquidity, secondary safeguarded same-day funds and contingency with legally evidenced access. Each controlled by issuer policies.
- Monitoring: early warning at unusually high redemption velocity, any stale reconciliation/statement, liquidity deficit, concentration breaches, unexpected pending payout, missing signer, custody freeze or reserve haircut. Pause mint immediately; decide transfer/redemption effects with counsel and consumer fairness safeguards.

## Redemption state machine
`REQUESTED -> ELIGIBILITY_VERIFIED -> TOKEN_LOCKED -> BURNED_FIAT_PAYABLE -> FIAT_PAYOUT_SUBMITTED -> FIAT_CONFIRMED -> RECONCILED/CLOSED`.

`PAYOUT_UNKNOWN` remains a payable and must not create duplicate bank instructions. `REJECTED` before burn can refund escrow through controlled operation; after burn requires explicit payable-resolution/reissue policy with legal sign-off, no silent token recreation.

Never release the issuer's liability just because an on-chain burn succeeded; cash must demonstrably reach the lawful recipient under actual terms.

## Emergency procedures
**One bank inaccessible**: halt new minting if reserve/settlement proof or concentration breached, stop sending new redemptions to that bank, route only to a contractually authorized alternative; retain tokenholder claims. Provide public incident status compatible with confidentiality and consumer law.

**50% rapid redemption + 60% reserve inaccessible**: under ₱10M nominal liabilities and backing, only ₱4M accessible against ₱5M demand (₱1M liquidity gap); activate properly prefunded independent liquidity or binding alternative, not a draw on KDef/operating revenue/PCCO.

**Key compromise**: pause under bounded governance, lock mint permissions, rotate credential holders, independently account for supply, preserve incident evidence, notify regulator/partners/users as contractually required, test reactivation.

**Unknown bank payout**: query exact original provider reference; do not blind-retry or pay a second time.

**Out-of-balance / missing evidence**: freeze mint authorization; protect valid redemptions and customer information; open incident and reconcile independently.

## Control ownership / evidence
| Control | Day-to-day owner | Independent check | Required evidence |
|---|---|---|---|
| Bank/custodian eligibility | Treasury owner | Independent risk/legal | contracts, bank statements, audit, eligibility |
| Mint release | Issuer authorized operator | Separate attester + reviewer | settled funding ID, reserve gap, onchain receipt |
| Redemption closure | Settlement operator | Accounting/reconciliation reviewer | bank payout final confirmation |
| Cash movement | Two authorized signers | Finance oversight | approvals, bank ref, audit logs |
| Reserve disclosure | Finance oversight | External assurance provider | scope, certificate, source statements |
| PCCO benefit budget | Community program owner | Finance verifier | approved surplus/grant source, catalog obligation |
| Emergency pause | Designated incident manager | Independent time-bounded review | event timeline and recovery test |

No actual individual is assigned by this proposal. Require named mandates, conflict handling and legal counsel review for production.

## Critical external evidence gates
- Licensed liable issuer and legally enforceable redemption terms.
- Bank/custodian insolvency segregation and verified balance rights.
- Actual payout channels, liquidity commitments, rates, settlement timetable and regional service constraints.
- PH market access, relevant MAS/VARA obligations if used, privacy/AML/sanctions terms and disclosures.
- Independent third-party assurance and source data.
- Actual founding capital, operating runway and risk buffer — distinct from backing.

**Development may model these controls using fake data; D1 governs sandbox deployment. C0/F0 remain blocked.**
