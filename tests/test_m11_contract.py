import json, pathlib, unittest
R=pathlib.Path(__file__).resolve().parents[1]
class M11DesignContract(unittest.TestCase):
 def test_synthetic_only(self):
  f=json.loads((R/'40_PRODUCT/fixtures/m11_family_transfer.json').read_text())
  self.assertFalse(f['actual_financial_activity'])
 def test_fee_and_ledger_math(self):
  q=json.loads((R/'40_PRODUCT/fixtures/m11_family_transfer.json').read_text())['quote']
  self.assertEqual(q['principal_minor']+q['total_fee_minor'],q['total_sender_debit_minor'])
  self.assertEqual(q['provider_fee_minor']+q['platform_fee_minor'],q['total_fee_minor'])
 def test_development_approval_fails_closed(self):
  x=json.loads((R/'70_DELIVERY/development-approval-gates.json').read_text())
  self.assertEqual(x['gates'][1]['status'],'not_approved')
 def test_no_live_urls(self):
  x=json.loads((R/'50_BUILD/M11_OPENAPI.json').read_text())
  self.assertTrue(all('example.invalid' in y['url'] for y in x['servers']))
if __name__=='__main__':unittest.main()
