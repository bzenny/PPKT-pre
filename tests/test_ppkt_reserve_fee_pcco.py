import json,pathlib,math,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class FeeAndReservePolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=json.loads((ROOT/"60_EVIDENCE/ppkt-fee-scenarios.json").read_text())
    def test_scenarios_are_illustrative(self):
        self.assertFalse(self.model["legal_or_market_quote"])
    def test_math_and_break_even(self):
        a=self.model["assumptions"]
        for x in self.model["scenarios"]:
            fee=a["customer_fee_fixed_php"]+a["customer_fee_variable_rate"]*x["mean_transfer_php"]
            provider=a["provider_cost_fixed_php"]+a["provider_cost_variable_rate"]*x["mean_transfer_php"]
            margin=fee-provider-a["network_support_risk_per_txn_php"]
            self.assertAlmostEqual(margin,x["contribution_per_txn_php"],2)
            self.assertAlmostEqual(margin*x["transactions_month"]-x["fixed_overhead_month_php"],x["monthly_result_before_tax_php"],2)
            self.assertEqual(math.ceil(x["fixed_overhead_month_php"]/margin) if margin>0 else None,x["break_even_transactions_month"])
    def test_stress_exposes_liquidity_shortage(self):
        s=self.model["stress"]
        self.assertEqual(s["required_liquidity_30pct_php"],round(s["reference_outstanding_php"]*s["redeem_same_day_fraction"]))
        self.assertLess(s["accessible_if_60pct_blocked_php"],s["required_liquidity_50pct_php"])
    def test_legal_fund_separation(self):
        md=(ROOT/"40_PRODUCT/PPKT_RESERVE_FEES_v0_4.md").read_text().lower()
        pc=(ROOT/"40_PRODUCT/PCCO_COMMUNITY_ECONOMICS_v0_2.md").read_text().lower()
        self.assertIn("burning before payment",md)
        self.assertIn("no ppkT purchase necessary".lower(),pc)
        self.assertIn("no pledge/lending/collateral",pc)
if __name__=="__main__": unittest.main()
