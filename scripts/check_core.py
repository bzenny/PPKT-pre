#!/usr/bin/env python3
"""Dependency-free PPKT CORE structural validator; not a legal compliance assessment."""
from __future__ import annotations
import json
from pathlib import Path, PurePosixPath
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['manifest.json','MASTER.html','CONTEXT.md','00_PRIME/PRIME.html',
 '10_ARCHITECTURE/rules.json','10_ARCHITECTURE/registry.json',
 '20_BRAND/brand-standard.html','20_BRAND/brand-guide.md','20_BRAND/design-tokens.json',
 '30_CHARTER/PPKT_Building_Charter_v0_2.md','30_CHARTER/PPKT_Building_Charter_v0_2_3_RC1.md','30_CHARTER/authority-matrix.json',
 '95_RECORDS/approvals.json','95_RECORDS/decisions.json','70_DELIVERY/release-gates.json',
 '60_EVIDENCE/competitors.json','60_EVIDENCE/benchmarks.json','90_VALIDATION/VERIFIER.md']

def valid_relative(root, value):
    if not isinstance(value,str) or not value or '\\' in value or '://' in value: return False
    p=PurePosixPath(value)
    return not p.is_absolute() and '..' not in p.parts and (root/value).is_file()

def validate(root=ROOT):
    issues=[]
    for f in REQUIRED:
        if not valid_relative(root,f): issues.append('Missing or unsafe path '+f)
    data={}
    for f in root.rglob('*.json'):
        try: data[f.relative_to(root).as_posix()]=json.loads(f.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError) as exc: issues.append('Invalid JSON '+str(f)+' '+str(exc))
    doc=lambda p:data.get(p,{})
    m=doc('manifest.json')
    if m.get('project')!='PH Probinsyano Token' or m.get('identifier')!='PPKT':issues.append('Wrong brand or identifier')
    if m.get('status')!='unratified' or m.get('is_issued_token') is not False or m.get('has_live_customer_funds') is not False: issues.append('Sandbox baseline falsely asserts live status')
    if m.get('canonical_charter')!='30_CHARTER/PPKT_Building_Charter_v0_2_3_RC1.md' or not valid_relative(root,m.get('canonical_charter')):issues.append('Canonical charter mismatch')
    if m.get('icm_profile')!='MasterSys CORE':issues.append('ICM profile drift')
    if m.get('corporate_domicile')!='UNDECIDED' or m.get('financing_status')!='uncommitted': issues.append('International jurisdiction or financing incorrectly treated as finalized')
    if not (root/'30_CHARTER/JURISDICTION_DILIGENCE.md').is_file(): issues.append('Missing cross-border jurisdiction diligence')
    cross=(root/m.get('canonical_charter','missing')).read_text(encoding='utf-8') if valid_relative(root,m.get('canonical_charter')) else ''
    if 'Article 17' not in cross or 'offshore parent' not in cross.lower(): issues.append('International parent safeguards not embedded in charter')
    model=doc('30_CHARTER/operating-location-model.json')
    if model.get('approved') is not False or model.get('preferred_delivery_location') != 'Philippines': issues.append('PH delivery location unverified or misrepresented')
    if model.get('cost_model',{}).get('numeric_percentage_public') is not False or model.get('cost_model',{}).get('source_validation') != 'pending': issues.append('Unverified quantified costs promoted as audited public claims')
    if 'cost' not in cross.lower() or 'counterparty' not in cross.lower(): issues.append('Cross-border cost and counterparty controls not reflected in charter')
    if doc('30_CHARTER/authority-matrix.json').get('fundraise_authorized') is not False: issues.append('Financing incorrectly pre-authorized')
    rules=doc('10_ARCHITECTURE/rules.json')
    if rules.get('ordered_context')!=['FOLDERS','HTML','Markdown','JSON','YAML']:issues.append('CORE priority drift')
    if rules.get('complexity')!='CORE':issues.append('Unapproved complexity promotion')
    if 'applicable_law_and_executed_contracts' not in rules.get('authority_priority',[]):issues.append('Law/executed contracts precedence missing')
    brand=doc('20_BRAND/design-tokens.json').get('brand',{})
    if brand.get('identifier')!='PPKT' or '05' not in brand.get('selectedSymbol',''):issues.append('Symbol 05 brand drift')
    for e in doc('10_ARCHITECTURE/registry.json').get('entries',[]):
        if not valid_relative(root,e.get('path')): issues.append('Registry entry invalid: '+str(e.get('path')))
    approvals=doc('95_RECORDS/approvals.json')
    if approvals.get('ratified') is True and not approvals.get('corporate_approvals'):issues.append('Ratifcation lacks corporate evidence')
    if approvals.get('ratified') is False and approvals.get('effective_on'):issues.append('Unratified has effective date')
    decisions=doc('95_RECORDS/decisions.json').get('decisions',[])
    ids=[d.get('id') for d in decisions]
    if len(ids)<10 or len(ids)!=len(set(ids)):issues.append('Incomplete or duplicate decision IDs')
    if not any(d.get('topic')=='PCCO' and 'no issued' in str(d.get('choice','')) for d in decisions):issues.append('PCCO no-issuance boundary missing')
    auth={e.get('action'):e for e in doc('30_CHARTER/authority-matrix.json').get('rules',[])}
    if 'KDef_committee_at_least_5_of_7' not in auth.get('kdef_disbursement',{}).get('approves',[]):issues.append('KDef 5/7 threshold missing')
    emerg=auth.get('emergency_pause',{})
    if emerg.get('reviews_in_hours')!=24 or emerg.get('expires_or_renews_in_hours')!=72:issues.append('24/72h emergency rule mismatch')
    if auth.get('protected_amendment',{}).get('notice_days')!=30:issues.append('30d protected notice missing')
    gates=doc('70_DELIVERY/release-gates.json').get('gates',[])
    if [g.get('id') for g in gates]!=[f'G{i}' for i in range(8)]:issues.append('Release gate IDs are not G0–G7')
    if any(g.get('status') not in ('unknown','blocked','failed','pass') for g in gates):issues.append('Invalid gate status')
    if any(g.get('status')=='pass' and (not g.get('evidence') or not g.get('approved_by')) for g in gates):issues.append('Un-evidenced gate asserted pass')
    return issues

if __name__=='__main__':
    problems=validate()
    print('CORE structural check: '+('PASS' if not problems else 'FAIL'))
    for x in problems:print(' - '+x)
    raise SystemExit(1 if problems else 0)
