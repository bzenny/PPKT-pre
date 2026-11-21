# PPKT Polygon Amoy Sandbox — No Financial Value

**Development artifact; not a real token issuance.** Token uses `tPPKT`, a "NO VALUE" name and hard-coded chain gating (`80002` Polygon Amoy and `31337` local Hardhat). This prototype is NOT intended for mainnet and does not implement lawful reserve custody.

## Run offline/local tests (network needed once to install npm dependencies and solc)
```bash
cd token-sandbox
npm install --no-audit --no-fund
npm test
cd ..
python -m unittest discover -s token-sandbox/python_tests -v
```

Do **not** deploy to Amoy until D1 test-environment, signatory/key security, budget and independent reviewer approvals are recorded. There is intentionally **no deployment script** and no RPC private key in this repository.

## Key design facts
- `attestFakeFunding` does NOT attest real reserves or verify banking data. Its event is for a nonvaluable simulator only.
- Two different authorized actors approve and execute minting; this is not a substitute for legal reserve verification.
- `lockForSimulatedRedemption` escrows tokens; `burnPendingSimulatedPayout` reduces on-chain supply but **leaves fiat liability outstanding off-chain**.
- `recordSimulatedFiatSettlement` only records mock test evidence. Production settlement cannot rely on this event.
- Pausing is an emergency control; actual user rights and responsible signing must be legally established.
- No upgrades, bridge, staking, yield, PCCO trading or real-money integration.
- Do not interpret this as audited, production safe, or legally authorized.

Dependencies are version-pinned in package.json; lockfile/reproducible dependency audit and independent Solidity/security review are prerequisites to further deployment.

## Chain
Polygon Amoy: chain ID `80002`. The user authorized it as the **testnet** and reserved the ability to redesign/migrate before official launch. No mainnet selected.
