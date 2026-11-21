# ADR-0002 — Official Chain Shortlist and Proof-of-Fit

**Status:** POLYGON AMOY TESTNET SELECTED BY PROJECT SPONSOR; **mainnet chain not selected**. 21 November 2026.
**Project decision:** use **Polygon PoS Amoy testnet (chain ID 80002)** for first simulated token contract and lifecycle. Retain a documented option to redesign or migrate before official launch if cost, security, recovery, partner, performance or stability tests fail. Solana and Base are comparison/exit candidates, not mandatory parallel implementations. No mainnet deploy, bridging, presale or real token issue.

## Why chain selection follows token obligations
One PPKT should target a valid 1 PHP issuer redemption claim on an authorized path. That requires legal rights, reserve confirmation, custody, operational recovery and a transparent financial ledger regardless of the blockchain. The network records token supply and movements but does not prove bank solvency or fiat payout.

## Qualitative comparison (hypotheses, verify with recorded trials)
| Dimension | Polygon PoS | Solana | Base | Algorand |
|---|---|---|---|---|
| Stack | EVM ERC-20 with established audit tooling | SPL / Token-2022 extensions | EVM ERC-20 L2 | Native ASA / Smart ASA |
| First PH relevance | Existing PHPC publicly supports Polygon; **no PPKT partner agreement implied** | Strong high-volume transfer/fee design; exact PH partner must be demonstrated | Strong EVM/paymaster/app-account ecosystem; specific PH partner unproven | Deterministic finality and low base fees; narrower initially evidenced PH distribution |
| Fees | Low by payment standards but gas varies; measure p50/p95/p99 | Very low base cost; priority fees and rent/account setup count | Low but variable; L2 inclusion vs L1 finality and withdrawal timing differ | Fixed base fee in normal conditions; opt-in and ecosystem constraints |
| Compliance tools | ERC-20 role-based mint, pause, allowlists as specified | Token-2022 freeze, hooks, transfer restrictions (beware wallet compatibility) | ERC-20 access control and account abstraction | ASA freeze/clawback; design for recovery and holder rights |
| Issuance and reserve evidence | Custom issuer integration needed | Custom issuer integration needed | Custom issuer integration needed | Custom issuer integration needed |
| Key risk to test | RPC and settlement, gas spikes, role compromise, partner economics | Wallet support for extensions, gas sponsoring, rent, account recovery | Sequencer/L2 finality, outages and L1 withdrawals | Wallet adoption and partner endpoints |
| Disposition | **Test first** | **Test on same acceptance suite** | Evaluate if partner/UX favors Base | Retain as later option |

### Benchmark workloads: no invented throughput promises
Using **scenario assumptions**, not forecasts, see `60_EVIDENCE/ppkt-capacity-scenarios.json`. For 100,000 monthly active users doing 8 transfers/month, ~800,000 transfers/month require just ~0.31 transfers/sec averaged over 30 days; at an assumed 20x traffic concentration ~6.17 transfers/sec. Backend/on-chain events may multiply by mint, burn and reconciliation strategy. Build throughput claims from actual observed traces.

### Testnet bakeoff, same contract-equivalent behavior on each
1. Choose user experience: custodial partner-led versus self-custodial with recovery; document PH off-ramp and costs.
2. Test 100, 1,000 and 10,000 synthetic transfers, with bursts, at least three separate observation periods and failures.
3. Record fee per transfer incl gas sponsorship, account creation, RPC, signing, custody and infrastructure; measure p50/p95/p99, not marketing base fee.
4. Record time to accepted, final, and issuer-reconciled (these are different).
5. Validate unauthorized mint denied, burn with unpaid fiat liability, suspended authority, lost signer, RPC timeout, chain reorganizations/finality policy and recovery.
6. Confirm at least one lawful, demonstrable PHP fiat partner path, plus a reasonable exit/replacement plan; a PHPC-on-Polygon fact does not grant PPKT access.
7. Obtain counsel/issuer review of chain control (freeze/cancel/blacklist), customer rights, privacy, sanction controls, token decimals and on-chain compliance.
8. Only then ratify network ID, mainnet token address, ownership of mint roles, risk budget and audit requirements.

### Decision rule (proposed)
Candidate qualifies only if (a) a lawful credible issuer/partner path exists, (b) p95 all-in fees are competitive for the **₱500–₱1,000** intended user journey, (c) holder rights and recovery can be faithfully implemented, (d) security controls and audit tooling are satisfactory, and (e) financial reconciliations and network-exit obligations are unambiguous. If no candidate passes, keep PPKT service off-chain until it does.

**Baseline choice for engineering:** EVM adapter and ERC-20 test contracts on **Polygon Amoy (chain ID 80002)**. **Do not call Polygon PPKT's official chain yet.** Build an equivalent Solana test for real fee/recovery comparison. **No primary-plus-bridge plan in v0.3.**

## Research references (21 November 2026)

- Coins.ph PHPC whitepaper (1:1 PHP peg, issuer, reserve and Polygon/Ronin): https://www.coins.ph/en-ph/phpc-whitepaper
- BSP Memorandum M-2026-023 token-listing six-pillar due diligence: https://www.bsp.gov.ph/Regulations/Issuances/2026/M-2026-023.pdf
- MAS consultation (September 2026 SGD/G10 MAS-SCS perimeter): https://www.mas.gov.sg/news/media-releases/2026/mas-consults-on-legislative-amendments-to-implement-stablecoin-regulatory-framework
- Dubai VARA FRVA rules (approval, backing, redemptions): https://rulebooks.vara.ae/rulebook/annex-1-fiat-referenced-virtual-assets-issuance-rules
- OpenZeppelin Contracts v5 ERC20 and AccessControl: https://docs.openzeppelin.com/contracts/5.x/api/token/erc20
- Solana Token Extensions: https://solana.com/docs/tokens/extensions
- Polygon Chain payments scaling (first-party claims; benchmark independently): https://polygon.technology/blog/polygon-chain-now-supports-5000-payments-per-second-hitting-the-speed-of-a-card-network-at-a-fraction-of-the-cost



## Explicit confirmation (21 November 2026)
Polygon Amoy is the **chosen testnet**. The official mainnet chain is not yet chosen and has a nonbinding redesign/exit route. Do not equate testnet mint events with real PPKT issuance or real reserves. Production keys, funds, official chain and contracts stay gated by C0/F0.
