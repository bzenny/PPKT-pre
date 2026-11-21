import json
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text())
class OperatingLocationTests(unittest.TestCase):
    def test_cost_advantage_is_not_presented_as_verified(self):
        m=load('30_CHARTER/operating-location-model.json')
        self.assertFalse(m['approved'])
        self.assertFalse(m['cost_model']['numeric_percentage_public'])
        self.assertEqual(m['cost_model']['source_validation'], 'pending')
    def test_no_corporate_domicile_claim(self):
        m=load('manifest.json')
        self.assertEqual(m['corporate_domicile'], 'UNDECIDED')
        self.assertEqual(m['financing_status'], 'uncommitted')
    def test_required_risk_and_location_decisions(self):
        d={x['id']:x for x in load('95_RECORDS/decisions.json')['decisions']}
        self.assertIn('D-016',d);self.assertIn('D-017',d)
        self.assertEqual(d['D-016']['status'],'open')
        self.assertEqual(d['D-017']['status'],'open')
    def test_operational_cost_and_solvency_gates_remain_open(self):
        t=(R/'90_VALIDATION/JURISDICTION_GATE.md').read_text().lower()
        self.assertIn('local delivery-cost estimate validated',t)
        self.assertIn('funding/corporate oversight jurisdiction is separated',t)
