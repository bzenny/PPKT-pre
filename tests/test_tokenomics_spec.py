import json
import pathlib
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class TokenomicsPolicy(unittest.TestCase):
    def test_fixed_name(self):
        m = json.loads((ROOT / "manifest.json").read_text())
        self.assertEqual(m["name"], "PPKT")
        self.assertEqual(m["naming_status"], "fixed")
        self.assertFalse(m["is_issued_token"])
    def test_scenarios_are_reproducible(self):
        d=json.loads((ROOT / "60_EVIDENCE/ppkt-capacity-scenarios.json").read_text())
        self.assertTrue(d["all_numbers_are_illustrative"])
        for s in d["scenarios"]:
            self.assertEqual(s["monthly_active_users"]*s["transfers_per_user_month"],s["transfers_month"])
            self.assertEqual(s["transfers_month"]*s["avg_transfer_php"],s["volume_php_month"])
            self.assertEqual(s["monthly_active_users"]*s["assumed_avg_outstanding_php_per_user"],s["illustrative_reserve_backed_outstanding_php"])
if __name__=="__main__":
    unittest.main()
