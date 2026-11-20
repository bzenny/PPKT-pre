#!/usr/bin/env python3
"""Evidence-based, fail-closed prelaunch gate; does not grant any legal permissions."""
import argparse, datetime as dt, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def recent(d, today, max_days=180):
    try:v=dt.date.fromisoformat(d or '')
    except (TypeError,ValueError):return False
    return 0<=(today-v).days<=max_days

def review(gates, approvals, competitors, benchmarks, today=None):
    today=today or dt.date.today()
    blocks=[]
    if approvals.get('ratified') is not True or not approvals.get('effective_on'):blocks.append('Charter not ratified with effective date')
    if not approvals.get('corporate_approvals') or not approvals.get('legal_opinions'):blocks.append('Signed corporate and legal evidence missing')
    if not approvals.get('source_evidence'):blocks.append('Independent approval source evidence missing')
    entries=gates.get('gates',[])
    if [g.get('id') for g in entries]!=[f'G{i}' for i in range(8)]:blocks.append('Invalid or missing G0–G7 gates')
    for g in entries:
        id=g.get('id','?')
        if g.get('status')!='pass':blocks.append(f'{id}: {g.get("status","missing")}');continue
        if not g.get('evidence') or not g.get('approved_by') or not g.get('independent_attestation'):blocks.append(f'{id}: missing evidence/reviewer/independence')
        if not recent(g.get('reviewed_at'),today):blocks.append(f'{id}: stale/future/missing review')
    alternatives=competitors.get('records',[])
    if len(alternatives)<3 or not any(a.get('type')=='non-crypto' for a in alternatives):blocks.append('At least three alternatives including non-crypto baseline required')
    if any(a.get('verification') not in ('observed','measured') or not a.get('source_url') for a in alternatives):blocks.append('Comparable source observations missing')
    required={m.get('id') for m in benchmarks.get('metrics',[]) if m.get('required')}
    if not required:blocks.append('Required comparison metrics absent')
    for alt in alternatives:
        seen={m.get('metric') for m in benchmarks.get('measurements',[]) if m.get('competitor')==alt.get('id') and m.get('verified_by') and m.get('source_url') and recent(m.get('as_of'),today)}
        if not required.issubset(seen):blocks.append(f'{alt.get("id")}: missing independently verified comparable measures')
    return {'checked_at':today.isoformat(),'ready_for_prelaunch':not blocks,'blockers':blocks,
            'note':'Machine checks do not replace external legal, corporate, financial or security authorization.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--enforce',action='store_true');p.add_argument('--report',type=Path);opts=p.parse_args()
    get=lambda f:json.loads((ROOT/f).read_text(encoding='utf-8'))
    result=review(get('70_DELIVERY/release-gates.json'),get('95_RECORDS/approvals.json'),get('60_EVIDENCE/competitors.json'),get('60_EVIDENCE/benchmarks.json'))
    print('Prelaunch:', 'EVIDENCE-CHECK PASS (not legal clearance)' if result['ready_for_prelaunch'] else 'BLOCKED')
    print('Blockers:',len(result['blockers']))
    for block in result['blockers']:print(' -',block)
    if opts.report:
        opts.report.parent.mkdir(parents=True,exist_ok=True)
        opts.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    if opts.enforce and not result['ready_for_prelaunch']:raise SystemExit(2)
