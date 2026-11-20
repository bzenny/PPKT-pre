"""CORE authority, financial governance, and deliberate failure-state regression tests."""
import importlib.util,json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
def mod(name,path):
    s=importlib.util.spec_from_file_location(name,ROOT/path)
    x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
core=mod('core','scripts/check_core.py')
ready=mod('ready','scripts/release_readiness.py')
load=lambda path:json.loads((ROOT/path).read_text(encoding='utf-8'))
class CoreTests(unittest.TestCase):
    def test_structural_integrity(self):self.assertEqual([],core.validate(ROOT))
    def test_order(self):self.assertEqual(load('10_ARCHITECTURE/rules.json')['ordered_context'],['FOLDERS','HTML','Markdown','JSON','YAML'])
    def test_symbol(self):self.assertIn('05',load('20_BRAND/design-tokens.json')['brand']['selectedSymbol'])
    def test_no_issued_tokens(self):self.assertIs(load('manifest.json')['is_issued_token'],False)
    def test_no_customer_funds(self):self.assertIs(load('manifest.json')['has_live_customer_funds'],False)
    def test_registry(self):
        for row in load('10_ARCHITECTURE/registry.json')['entries']:self.assertTrue(core.valid_relative(ROOT,row['path']))
    def test_path_traversal(self):
        self.assertFalse(core.valid_relative(ROOT,'../../etc/passwd'))
        self.assertFalse(core.valid_relative(ROOT,'https://example.org/x'))
    def test_protected_reserve_boundary(self):
        doc=(ROOT/'30_CHARTER/PPKT_Building_Charter_v0_2.md').read_text()
        self.assertIn('no use of unissued PCCO as minimum reserve backing',doc)
        self.assertIn('One asset cannot support incompatible promises',doc)
    def test_authority_not_live(self):
        self.assertTrue(all(r['live_enabled'] is False for r in load('30_CHARTER/authority-matrix.json')['rules']))
    def test_kdef(self):
        a={r['action']:r for r in load('30_CHARTER/authority-matrix.json')['rules']}
        self.assertIn('KDef_committee_at_least_5_of_7',a['kdef_disbursement']['approves'])
    def test_emergency(self):
        a={r['action']:r for r in load('30_CHARTER/authority-matrix.json')['rules']}
        self.assertEqual((a['emergency_pause']['reviews_in_hours'],a['emergency_pause']['expires_or_renews_in_hours']),(24,72))
    def test_gates(self):self.assertEqual([g['id'] for g in load('70_DELIVERY/release-gates.json')['gates']],[f'G{i}' for i in range(8)])
    def release(self,g=None,a=None,c=None,b=None):
        return ready.review(g or load('70_DELIVERY/release-gates.json'),a or load('95_RECORDS/approvals.json'),c or load('60_EVIDENCE/competitors.json'),b or load('60_EVIDENCE/benchmarks.json'))
    def test_prelaunch_stays_blocked(self):self.assertFalse(self.release()['ready_for_prelaunch'])
    def test_self_ratifcation_doesnt_pass(self):
        a=load('95_RECORDS/approvals.json');a['ratified']=True;a['effective_on']='2026-11-20'
        result=self.release(a=a)
        self.assertFalse(result['ready_for_prelaunch'])
        self.assertTrue(any('Signed corporate' in x for x in result['blockers']))
    def test_self_pass_doesnt_override_evidence(self):
        g=load('70_DELIVERY/release-gates.json')
        for entry in g['gates']:entry['status']='pass'
        self.assertFalse(self.release(g=g)['ready_for_prelaunch'])
    def test_no_market_data_blocks(self):
        self.assertTrue(any('independently verified comparable' in x for x in self.release()['blockers']))
    def test_pcco_unissued(self):self.assertIn('No-issued-instrument',(ROOT/'30_CHARTER/product-boundaries.md').read_text())
    def test_legal_review_sources(self):
        d=(ROOT/'30_CHARTER/LEGAL_REVIEW.md').read_text()
        for s in ('M-2025-031','M-2026-023','RA 10173','MC 04/05'):self.assertIn(s,d)
if __name__=='__main__':unittest.main()
