"""Nontransferable PCCO earned participation demonstration, not a currency or issued asset.
Never import PPKT financial balances or reserve accounts into this ledger.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Dict, Set

class ParticipationError(ValueError): pass

@dataclass(frozen=True)
class ProgramEvent:
    sequence: int
    kind: str
    reference: str
    member: str
    units: int
    cents: int
    digest: str

class ParticipationLedger:
    ALLOWED_ACTIONS = frozenset({"financial_literacy", "community_service", "merchant_education", "verified_peer_support"})
    ALLOWED_FUNDING = frozenset({"approved_unrestricted_surplus", "restricted_grant"})

    def __init__(self) -> None:
        self.credits: Dict[str, int] = {}
        self._seen: Set[str] = set()
        self._committed_cents = 0
        self._allocated_cents = 0
        self._events: list[ProgramEvent] = []
        self._last_hash = "GENESIS"

    @property
    def budget_cents(self) -> int: return self._allocated_cents

    @property
    def uncommitted_cents(self) -> int: return self._allocated_cents - self._committed_cents

    @property
    def events(self) -> tuple[ProgramEvent, ...]: return tuple(self._events)

    def _check_unique(self, ref: str) -> None:
        if not ref or ref in self._seen: raise ParticipationError("missing or repeated event reference")

    def _record(self, kind: str, ref: str, member: str, units: int, cents: int) -> None:
        payload = json.dumps([self._last_hash, kind, ref, member, units, cents, len(self._events) + 1], separators=(",", ":"))
        digest = sha256(payload.encode()).hexdigest()
        self._events.append(ProgramEvent(len(self._events) + 1, kind, ref, member, units, cents, digest))
        self._last_hash = digest
        self._seen.add(ref)

    def fund_budget(self, event_ref: str, source: str, cents: int) -> None:
        self._check_unique(event_ref)
        if source not in self.ALLOWED_FUNDING: raise ParticipationError("PPKT reserve and debt sources prohibited")
        if not isinstance(cents, int) or cents <= 0: raise ParticipationError("invalid budget")
        # In real operations independent approval of funding source must happen elsewhere.
        self._allocated_cents += cents
        self._record("budget:" + source, event_ref, "", 0, cents)

    def award_verified_action(self, event_ref: str, member: str, action: str, units: int, evidence: str) -> None:
        self._check_unique(event_ref)
        if not member or not evidence: raise ParticipationError("missing member/evidence")
        if action not in self.ALLOWED_ACTIONS: raise ParticipationError("not a verified program action")
        if not isinstance(units, int) or not (1 <= units <= 10): raise ParticipationError("per-event cap 10")
        self.credits[member] = self.credits.get(member, 0) + units
        self._record("award:" + action, event_ref, member, units, 0)

    def reserve_budgeted_benefit(self, event_ref: str, member: str, units: int, max_fulfillment_cost_cents: int) -> None:
        self._check_unique(event_ref)
        if not isinstance(units, int) or units <= 0: raise ParticipationError("invalid units")
        if not isinstance(max_fulfillment_cost_cents, int) or max_fulfillment_cost_cents <= 0:
            raise ParticipationError("invalid cost")
        if self.credits.get(member, 0) < units: raise ParticipationError("insufficient earned participation")
        if self.uncommitted_cents < max_fulfillment_cost_cents: raise ParticipationError("no prefunded benefit budget")
        self.credits[member] -= units
        self._committed_cents += max_fulfillment_cost_cents
        self._record("benefit_reserved", event_ref, member, -units, max_fulfillment_cost_cents)

    def verify_event_chain(self) -> bool:
        last = "GENESIS"
        for i, ev in enumerate(self._events, 1):
            payload = json.dumps([last, ev.kind, ev.reference, ev.member, ev.units, ev.cents, i], separators=(",", ":"))
            expected = sha256(payload.encode()).hexdigest()
            if ev.sequence != i or ev.digest != expected: return False
            last = expected
        return True
