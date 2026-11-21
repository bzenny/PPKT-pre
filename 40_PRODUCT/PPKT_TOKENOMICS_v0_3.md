# PPKT Tokenomics v0.3 — Working Economic Architecture

**Named project / intended token:** PPKT (public brand: PH Probinsyano Token)  
**Date:** 21 November 2026 | **Status:** WORKING DESIGN DECISION / UNRATIFIED — NOT AN OFFER, ISSUANCE OR REDEMPTION PROMISE
**Priority:** Define monetary obligations and user benefit before official chain and before building a production contract.

## Decision in one sentence
**PPKT is designed as a fully reserved, PHP-referenced payment token with dynamically funded supply, issued and redeemed only by an appropriately authorized liable party.** PCCO and KDef remain financially separate. Production issuance requires legal, operational and independent risk approvals.

## Structural options reviewed
| Option | Model | Pros | Principal concern | Disposition |
|---|---|---|---|---|
| A | Fiat-reserved, obligation-linked PPKT | Defensible PHP face value and simple explanation, on/off ramp potential, transparent books | Real issuer, backing, custody, partner and licensing burden | **Preferred economic end-state** |
| B | Crypto overcollateralized PPKT | On-chain transparency and programmability | Liquidation, PHP asset mismatch, reserve volatility, oracle risk, complexity | Not preferred for family payments |
| C | Algorithmic / two-coin stabilization | Capital efficient in optimistic conditions | Depeg/death-spiral exposure; PCCO insufficiently stable backing | **Reject** |
| D | Unbacked utility/reward token named PPKT | Fast to launch, inexpensive to issue | Cannot honestly promise one-PHP purchasing value or safe transfer | Reject as primary PPKT |
| E | PPKT software account + licensed partner balance, no own minted asset | Fastest lawful research and learning; lower first capital need | Partner dependence, token not initially issued | **Preferred P0–P1 implementation path** |

A is the **product tokenomic target**. E is the **initial execution vehicle**, not a rebranding of PPKT.

## PPKT parameters — proposed baseline
| Field | Architecture |
|---|---|
| Name | **PPKT** — final name; PH Probinsyano Token in full |
| Purpose | PHP-value transfer, family support, payments, merchant/authorized partner settlement |
| Reference / target | **1 PPKT = 1 PHP in an enforceable eligible redemption channel if legally issued**; market trading price may deviate |
| Initial real supply | **0**; PPKT has not been issued |
| Token supply curve | **Elastic, reserve-funded**, not a pre-minted finite quantity; size limited by approved backing, exposure, counterparties and permissions |
| Founder / community allocation of PPKT | **0 unbacked or discounted tokens**; no free reserve claims |
| Algorithmic stabilizer | None; no price-triggered issuance, reflexive swaps, or PCCO stabilization |
| Reserve floor | **At least 100% eligible, segregated reserve value relative to all outstanding redeemable claims**, or more if applicable law/partner contract requires; no reuse for KDef, operating expenses, trading, lending or investor return |
| Reserve composition | PHP-denominated liquid eligible assets with enforceable custody, diversified counterparties and independently documented haircut/liquidity risk; final eligible list determined by issuer regulator |
| Company capital | Separately funded operating runway and regulatory capital; any additional 5–10% loss-absorbing policy buffer is a **scenario**, not money drawn from customer reserves and not yet a mandatory figure |
| Issuance | Only after verifiable *settled* backing, authorizations and unique mint authorization; exact claims, supply and reserve events linked |
| Redemption | Burner may retire units after valid surrender, but until settled fiat delivery the unpaid redemption is a separate outstanding customer payable; do not reduce required coverage merely because tokens burned |
| Rewards/yield | None inherent in PPKT; holders do not automatically share issuer profit or reserve yield |
| Fees | Transparent service-based fees separate from token face value; publish all-in cost and separate issuer redemption terms; no price-based supply fee |
| Control rights | Operational mint/pause/recovery authorities separated, auditable and subject to explicit legal restrictions and emergency review |
| On-chain precision | **Candidate 6 decimals** for EVM/Solana interoperability; do not finalize without dust, settlement, wallet, bridge and redemption proof tests; P0 ledger uses integer centavos |
| Cross-chain | Single official issuance chain initially; **no bridges, duplicated native supply or multi-chain liquidity** before independent bridge and rights assessment |
| Disclosure | External reserve and liability attestations, chain supply, outstanding burned-but-unpaid obligations, counterparty exposure, liquidity, redemptions, controls, fee terms, and incidents |

### Monetary invariant
Define eligible reserve assets **R** and all relevant legally enforceable redemption claims **L**, counting circulating units plus any burned-but-unpaid fiat redemptions **without double count**:
- Hard objective: `R >= L`; internal and regulatory haircuts/coverage rules take precedence.
- New issuance is permitted **only** for verified incremental eligible reserve value and only within approved exposure limits.
- A pending deposit, speculative PCCO market value, future fundraising pledge or treasury projection **never** authorizes minting.
- A burn by itself does **not** extinguish a redemption payable.

### Flow: issue, move, redeem, reconcile
1. Deposit/partner settlement confirmed and checked for sanctions/risk where required.
2. Independent funding and issuer authority confirmed; one immutable issuance request is recorded.
3. Mint **only** matching backed units; reconcile contract supply + issuer obligations to bank/custodian evidence.
4. Users transfer; separate provider, chain and platform fees disclosed before action.
5. Redemption is registered against legitimate holder rights. Burn or lock under approved lifecycle; fiat payable remains until actual cash/payout confirmation.
6. Reconcile bank/custodian, financial journal, on-chain supply, unpaid obligations and exceptions. Show true evidence, never a fictitious 100% claim.

### What this corrects from the legacy whitepaper
- **Legacy 150% collateral** using PHP + 50% PCCO → **do not count PCCO as PPKT required backing**.
- **Algorithmic mint/burn linked to oracle deviations** → **mint only against settled eligible backing; burn on verified redemption lifecycle**.
- **Use 25% of PPKT pool for lending** → **no lending, operating use or investment from customer reserves**.
- **Fixed PPKT supply or founder allocation** → **none**; financed supply only.
- **PCCO 100 million released over five years** → archived design hypothesis, **not adopted**; separate future decision.
- **Solana primary / Polygon backup multichain** → reassess both as peers; **single official chain first**.

## PCCO — preserve the identity, separate the promises
PCCO (historical Pico/Piso association) is **not** a subdivision of PHP or PPKT, not required to transact, not the PPKT stabilizer and not issued today. First prototype as **budgeted, nontransferable community participation credits / memberships** with transparent award and cancellation rules, backed by program funding where redemption creates a payable. If later sold, transferred, staked or marketed for gains, PCCO needs its own rights, security/regulatory assessment, maximum/vesting schedule and funding plan. Do not promise a supply of 100 million merely because it appears in the legacy document.

## KDef — independent impact stewardship
KDef grants and expenses come exclusively from allocated company profits, grants or separately sourced unrestricted capital. Transfer to KDef requires proper corporate approval and independent fund governance. PPKT holder reserves are never a funding source.

## Partner and corporate considerations
ParentCo may be in Singapore or an appropriate Dubai regime, and PH software/service delivery remains the preferred cost base. **The token issuer, cash reserve custodian, PH customer liability and local redemption partner need not be ParentCo**, and their legal/financial rights must be unambiguously documented.

MAS September 2026 SCS perimeter is SGD/G10, not a ready-made Philippine-peso authorization. Dubai VARA FRVA issuance requires license and asset-level approval and VARA's own restrictions include no local UAE goods/services payments with those tokens. A foreign parent is not a waiver of PH laws. Legal classification, money services and issuance approvals remain open.

## Formal decision status
**Fixed now:** PPKT naming; user payment role; no unbacked PPKT allocations; no PCCO-backed peg; distinct KDef.  
**Working economic choice:** PHP-referenced fully reserved dynamic supply; one chain after testnet evaluation; P0 no-issued-token accounts.  
**Open for human approval:** actual issuer, holder redemption party and times, asset eligibility/custody, 6 vs 2 token decimals, capital buffers, jurisdiction, fees, chain, audit and compliance terms.

## Research references (21 November 2026)

- Coins.ph PHPC whitepaper (1:1 PHP peg, issuer, reserve and Polygon/Ronin): https://www.coins.ph/en-ph/phpc-whitepaper
- BSP Memorandum M-2026-023 token-listing six-pillar due diligence: https://www.bsp.gov.ph/Regulations/Issuances/2026/M-2026-023.pdf
- MAS consultation (September 2026 SGD/G10 MAS-SCS perimeter): https://www.mas.gov.sg/news/media-releases/2026/mas-consults-on-legislative-amendments-to-implement-stablecoin-regulatory-framework
- Dubai VARA FRVA rules (approval, backing, redemptions): https://rulebooks.vara.ae/rulebook/annex-1-fiat-referenced-virtual-assets-issuance-rules
- OpenZeppelin Contracts v5 ERC20 and AccessControl: https://docs.openzeppelin.com/contracts/5.x/api/token/erc20
- Solana Token Extensions: https://solana.com/docs/tokens/extensions
- Polygon Chain payments scaling (first-party claims; benchmark independently): https://polygon.technology/blog/polygon-chain-now-supports-5000-payments-per-second-hitting-the-speed-of-a-card-network-at-a-fraction-of-the-cost

