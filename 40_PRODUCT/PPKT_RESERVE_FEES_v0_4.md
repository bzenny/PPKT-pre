# PPKT Economics v0.4 — Reserve, Issuance, Redemption and Sustainability
**21 November 2026 | Working design; NOT a legal promise, issuer license, live reserve or authorization to mint**

**User-approved baseline:** PPKT is the name. PHP-referenced, full eligible reserve coverage, elastic supply tied to settled funding, no unbacked PPKT allocation, no PCCO peg stabilization, one eventual official chain. **Testnet fixed for current development: Polygon Amoy (80002)**, with redesign/migration permitted before launch. Mainnet not selected.

## 1. Economic perimeter / separated accounts
1. **PPKT backing**: safeguarded eligible asset portfolio held for identified holders, accounted at issuer liability level. No lending, rehypothecation, operating expenses, yield guarantees, KDef, speculative token backing or investor withdrawals.
2. **Issuer equity / risk capital**: separately sourced capital to absorb loss, legal compliance, cyber/operational exposure and solvency shocks. Not included in required backing unless actually contributed into an eligible reserve with rights documented.
3. **OperatingCo working capital**: fees that are earned, unrestricted company investment and funding; pays payroll, outsourced partners, support, fraud prevention and infrastructure.
4. **PCCO rewards budget**: restricted program allocation from genuine unrestricted cash and/or grants; **no dependence on PPKT reserve balances, liquidity, fees belonging to redemption holders, or token appreciation**.
5. **KDef**: independently approved unrestricted development allocation; no PPKT backing assets.

**Do not confuse**: issuer reserve ≠ exchange liquidity pool ≠ corporate treasury ≠ capital adequacy ≠ deposit insurance. A foreign parent's treasury account does not itself ring-fence PPKT assets or create PH retail redemption rights.

## 2. Reserve requirements: initial proposed policy
- Hard coverage objective: **eligible, unencumbered and legally accessible R >= all outstanding redemption obligations L**, using actual issuer-level legally enforceable claims, after relevant mark-to-market haircuts and accrued fees/encumbrances. Applicable laws or partner covenants may require MORE or different assets.
- Initially use **100% PHP-denominated, available cash** with properly documented legal segregation and independently reviewed solvency/credit status; permit treasury instruments only in a later approved reserve-policy amendment. Do not promise same-day access from a nominal bank balance.
- Prefer **2 or more qualified, independently reviewed counterparties** for any substantive authorized live issuance; proposed default **no single counterparty above 60%** of reserve nominal value, subject to real account availability, law and an approved escalation/exception. Two banks at 50/50 are a diversification target, not an assumption of credit safety.
- Model **30% redemption requests in one day**, **50% rapid redemption**, **60% of one bank unavailable**, frozen banking access, AML hold, fraud, payment holiday, custody dispute and a failed bridge/RPC despite healthy reserves. These are stress inputs, not probability predictions. A reserve is not sufficiently liquid merely because its nominal book value exceeds liabilities.
- Publish supply/issuer liabilities daily after authorized launch and commission independent reserve/liability assurance **at least monthly as a proposed goal**, with a frequency and scope matched to actual regulator/issuer approval. Independent reconciliation is DAILY during issuance/redeemable operations; alerts must stop minting on loss of source truth or coverage.
- Legal counsel must verify **holder beneficial rights, issuer insolvency outcome, priority, claims process, permitted assets, client-money restrictions, bank/custodian enforceability, redemption eligibility and location/cross-border risks**. A reserve bank letter or smart contract balance is not sufficient.
- PPKT is peso-referenced: this does not hedge Philippine inflation or imply secondary-market price never deviates from ₱1.

### Accounting obligation invariant
Let C be circulating redeemable PPKT including units held under a pending redemption but **still counted in total redeemable supply**. Let U be authorized burned or otherwise legally extinguished units for which PHP payout remains UNSETTLED and is **not already included in C**. Other payable claims O (if any) must be separately counted.
`L = C + U + O` at face PHP conversion (without double-counting). `R_eligible >= L`.
Mint authority must also meet *incremental* settled funding conditions and risk/limits: unused reserve headroom alone is NOT permission to mint.
The off-chain authoritative issuer liability ledger and on-chain total supply must be reconciled, accounting for held issuer inventory and other legitimate supply adjustments. Negative residuals, missing provider evidence or unresolved events block issuance.

**Example:** 1,000,000 valid tokens and ₱1,000,000 backing. Redeem/burn 200,000 tokens while PHP payout is pending => C=800,000, U=200,000, L=₱1,000,000 and backing must remain >=₱1,000,000. After settling ₱100,000 of that pending payout, U=100,000, L=₱900,000 and reserve may legitimately decrease to ₱900,000. Never erase U on burn alone.

## 3. Issuance controls
1. Licensed/responsible issuer receives legally eligible PHP funds and obtains **settled final bank evidence** with unique funding ID. Pending deposit, intercompany promise, off-chain oracle, exchange quotation and PCCO market value are NOT backing.
2. Independent reserve/treasury reviewer checks beneficiary, reserve title, available value, concentration, transfer terms, sanction/compliance checks and risk capacity.
3. Unique immutable mint proposal with amount, link to settled funding, issuer approvals and signed authorization. **Four-eyes minimum; preferably threshold-controlled signing** under a separate internal policy; prohibit unilateral arbitrary mint.
4. On Polygon Amoy ONLY, simulator may exercise equivalent mock supply logic with zero-value fake assets. No actual PPKT production mint before F0. Idempotent submission/retry and separate chain receipt/finality policy required.
5. Issuer reconciles on-chain supply, reserve bank statements and accounting obligations. Negative gap -> automatic mint stop + human incident escalation.

## 4. Redemption controls
1. Identify legally entitled holder and applicable issuer terms; specify authorized redemption channel, threshold, fees, limits, timing and complaint rights BEFORE launch.
2. Lock/surrender token under approved rules, and record redemption obligation; burning before payment NEVER eliminates issuer payable.
3. Initiate one idempotent PHP payout. Timeout = **unknown/pending**, not automatic retry.
4. Only verified final fiat settlement closes payable and releases the correct reserve amount; returned payout or exception stays outstanding and is escalated.
5. Record reversal/chargeback pathways and bank holidays in actual terms. Disclose gross face value separate from clearly itemized wallet/network/on-off-ramp fees. A fee can reduce net pesos received even if gross issuer redemption is 1:1; do not advertise fees as a hidden change to token peg.

## 5. Fee architecture and financial sustainability
**Three services, three actual cost structures**:
- Wallet-to-wallet PPKT movement: marginal Polygon transaction/sponsorship, anti-fraud, support and signer infrastructure; do NOT assume a bank-payout fee on every on-chain transfer.
- Fiat cash-in/out/remittance: bank/payment rails, KYC/compliance, fraud risk, reconciliation, cash handling and after-sales; itemized partner fees may dominate.
- Merchant acquisition/payments and paid institutional API services: independently negotiated and lawful service revenues. Do not rely on reserve yield, investment speculation or selling PPKT as the operating model.

**Illustrative fee formula for a one-hop fiat payout, NOT a recommended customer tariff**: charged user fee = ₱5 + 1% of transfer; provider variable cost = ₱5 + 0.35% of transfer; additional network/support/fraud processing = ₱2 per transfer. All figures unverified hypotheses; overhead varies by stage. This matches the previous synthetic ₱15 fee at ₱1,000, but tests whether that fixture could cover costs. See `60_EVIDENCE/ppkt-fee-scenarios.json` for explicit calculations.

`unit_contribution = user_fee - provider_cost - network_support_risk`  
`monthly_operating_surplus = transactions * unit_contribution - stage_fixed_monthly_overhead`  
`break_even_transactions = ceil(fixed_overhead / unit_contribution)` if unit contribution >0; otherwise business is not viable at that price.

### Major finding
A ₱1,000 payout at ₱15 fee with these assumptions yields only ₱4.50 contribution, BEFORE fixed cost, tax, capital cost and further regulated burdens. In the previous M1.1 illustrative split, provider receives ₱12; platform receives only ₱3 gross **before its own expenses**. For a ₱100 micro-transfer, ₱6 is a 6% customer burden and hypothetical unit contribution is NEGATIVE. A universal flat/percent tariff is not compatible with financial inclusion at every payment size.

**Required pricing experiments**: compare zero/low wallet transfers, separately priced on/off ramps, micropayment batching/merchant acceptance, family transfer subscription, licensed partner wholesale volume rates and institutional merchant/B2B revenue. Compare actual competing BSP-supervised fees; do not claim an advantage from an invented cost basket. No user should be forced to acquire PCCO to earn a fee waiver or complete basic transfers.

### Operating-capital gate
Start only with verified independent runway, capital and risk-funding arrangements adequate for legal/regulatory and partner commitments (budget horizon determined after cost quotes). Customer PPKT reserves are never runway. Commercial sustainability requires signed provider quotes, real conversion mix, fraud & support data, bank liquidity arrangements and measured willingness to pay. Growth scenarios alone are not proof of profit.

## 6. Proposed financial launch constraints
- Zero issuance in P0/P1 until C0/F0 and real backing verified.
- Before first real issue: approved issuer and qualified custody, actual terms, allowed assets, independent counsel and a paid-for reserve/liquidity assurance program, versioned contracts, security audit, risk capital and partner exit plan.
- Initial circulation cap **based on approved liquidity/custodian operational capacity, not a preprinted speculative token allocation**; proposed step-ups only after stress/rights evidence. No arbitrary promise of 100 million units.
- Issuance halt if uncovered liability, unverified bank statement, custody access restriction, unresolved mint key compromise, fraud escalation, sanction block or accounting mismatch.
- Testnet under D1 only. Polygon testnet is CONFIRMED; mainnet chain not yet ratified, and migration/redesign remains available before official release.

## 7. Decision register
**User-selected:** model, name, Polygon testnet and right to reconsider before official launch.  
**Proposed numeric policies:** 2+ custodians/60% concentration, 30% and 50% redemption stress, monthly external assurance, liquidity and fees.  
**Not approved / missing:** real legal issuer, exact reserve title, T+0/T+1 redemption SLA, bank contracts and quotes, actual pricing, capital/cost budget, mainnet token address and launch authorization.

**References:** BSP M-2026-023 https://www.bsp.gov.ph/Regulations/Issuances/2026/M-2026-023.pdf ; Coins.ph PHPC https://www.coins.ph/en-ph/phpc-whitepaper ; Circle transparency https://www.circle.com/transparency ; BSP fees https://www.bsp.gov.ph/Pages/PAYMENTS%20AND%20SETTLEMENTS/National%20Retail%20Payment%20System/Fees-on-Electronic-Payments.aspx .