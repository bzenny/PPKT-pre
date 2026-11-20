# MasterSys CORE / ICM architecture charter

**Decision:** folders → HTML → Markdown → JSON → YAML. Not an autonomous corporate AI system. Start with one repository, one modular service boundary, explicit manifests and auditable decisions. `CORE` must remain understandable to a second maintainer without installing a fleet of agents.

- **Floors:** Floor 1 public, Floor 2 operational, Floor 3 oversight, Basement synthetic development; not trust levels.
- **Rooms:** product/authority modules described in `module-registry.json`; bounded interfaces and declarations for money, data, approvals and failures.
- **Authority:** actual corporate/legal instruments > signed human charter > design proposal > software. Independent evidence has its own provenance.
- **Key split:** provider sandbox credentials / Supabase service keys / blockchain testnet signers stay in separate managed secret stores; never Git.
- **Data split:** browser/UI cannot write financial ledgers directly; API uses transactional functions and idempotency controls, with RLS where tables are exposed.
- **Upgrade trigger:** move beyond CORE only when a measured ownership, security, modularity, resilience or scale problem is documented with cost comparison; record an ADR.

See `50_BUILD/ARCHITECTURE.md` for target integrations and `30_CHARTER/PPKT_Building_Charter_v0_2.md` for the human-facing authority design.
