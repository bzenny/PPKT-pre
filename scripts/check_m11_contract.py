#!/usr/bin/env python3
"""Fail-closed design contract validation, NOT a working transfer implementation."""
import json, pathlib
r=pathlib.Path(__file__).resolve().parents[1]
load=lambda p:json.loads((r/p).read_text())
fx=load('40_PRODUCT/fixtures/m11_family_transfer.json')
a=load('50_BUILD/M11_OPENAPI.json')
g=load('70_DELIVERY/development-approval-gates.json')
q=fx['quote']
assert q['principal_minor'] + q['total_fee_minor'] == q['total_sender_debit_minor']
assert q['provider_fee_minor'] + q['platform_fee_minor'] == q['total_fee_minor']
assert fx['starting_sender_available_minor']-q['total_sender_debit_minor']==fx['expected']['sender_available_after_hold_minor']
assert q['total_sender_debit_minor']==q['principal_minor']+q['provider_fee_minor']+q['platform_fee_minor']
assert len(a['paths'])==6
assert g['status']=='PENDING_D1_HUMAN_APPROVAL' and all(x['status']!='approved' for x in g['gates'])
assert not fx['actual_financial_activity']
print('M1.1 DESIGN CONTRACT: VALID (no implementation, no transfer performed, D1 remains blocked)')
