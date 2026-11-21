"""Independent arithmetic verifier for FAKE issuer balances; never a real reserve attestation.
Integer arithmetic: 6-token decimals = 10_000 micro-units per PHP centavo.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

MICRO_UNITS_PER_CENTAVO = 10_000

class ReserveException(ValueError): pass

@dataclass(frozen=True)
class BankSnapshot:
    alias: str
    eligible_php_centavos: int
    inaccessible_php_centavos: int = 0
    simulated_evidence_id: str = ""

    def validate(self) -> None:
        if not self.alias or not self.simulated_evidence_id:
            raise ReserveException("bank evidence missing")
        if min(self.eligible_php_centavos, self.inaccessible_php_centavos) < 0:
            raise ReserveException("negative bank amount")
        if self.inaccessible_php_centavos > self.eligible_php_centavos:
            raise ReserveException("inaccessible more than eligible")

@dataclass(frozen=True)
class IssuerSnapshot:
    circulating_token_micro_units: int
    burned_but_unpaid_php_centavos: int
    other_redeemable_php_centavos: int = 0

    def liability_centavos(self) -> int:
        if min(self.circulating_token_micro_units, self.burned_but_unpaid_php_centavos,
               self.other_redeemable_php_centavos) < 0:
            raise ReserveException("negative issuer liabilities")
        # CEIL micro-units to the closest PHP centavo: conservative around token dust.
        circulating_cents = (self.circulating_token_micro_units + MICRO_UNITS_PER_CENTAVO - 1) // MICRO_UNITS_PER_CENTAVO
        return circulating_cents + self.burned_but_unpaid_php_centavos + self.other_redeemable_php_centavos

@dataclass(frozen=True)
class ReserveVerdict:
    liability_centavos: int
    eligible_centavos: int
    liquid_centavos: int
    reserve_gap_centavos: int
    redemption_stress_gap_centavos: int
    fully_backed: bool
    liquid_under_stress: bool
    minting_should_halt: bool

def verify_reserve(
    banks: Sequence[BankSnapshot],
    issuer: IssuerSnapshot,
    stress_redemption_bps: int = 5000,
    concentration_limit_bps: int = 6000
) -> ReserveVerdict:
    if not 0 <= stress_redemption_bps <= 10000: raise ReserveException("bad stress basis points")
    if not 0 < concentration_limit_bps <= 10000: raise ReserveException("bad concentration limit")
    if not banks: raise ReserveException("bank evidence empty")
    aliases=set()
    for b in banks:
        b.validate()
        if b.alias in aliases: raise ReserveException("duplicate bank identity")
        aliases.add(b.alias)
    eligible = sum(x.eligible_php_centavos for x in banks)
    liquid = eligible - sum(x.inaccessible_php_centavos for x in banks)
    liability = issuer.liability_centavos()
    required_now=(liability*stress_redemption_bps+9999)//10000
    # Concentration controls are a proposed policy and can fail closed for minting.
    concentration_breach = eligible > 0 and any(x.eligible_php_centavos*10000 > eligible*concentration_limit_bps for x in banks)
    covered = eligible >= liability
    enough_liquid = liquid >= required_now
    return ReserveVerdict(
        liability, eligible, liquid,
        max(0, liability-eligible), max(0, required_now-liquid),
        covered, enough_liquid,
        not covered or not enough_liquid or concentration_breach
    )

def approve_simulated_incremental_mint(
    reserve_before_centavos: int, liability_before_centavos: int,
    settled_incremental_funding_centavos: int, requested_micro_units: int
) -> bool:
    if min(reserve_before_centavos, liability_before_centavos,
           settled_incremental_funding_centavos, requested_micro_units) < 0:
        return False
    if settled_incremental_funding_centavos == 0 or requested_micro_units == 0:
        return False
    minted_cents=(requested_micro_units+MICRO_UNITS_PER_CENTAVO-1)//MICRO_UNITS_PER_CENTAVO
    if minted_cents>settled_incremental_funding_centavos: return False
    return reserve_before_centavos+settled_incremental_funding_centavos >= liability_before_centavos+minted_cents
