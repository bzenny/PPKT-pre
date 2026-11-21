import sys,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from five_year_model import calculate

class FiveYearModelTests(unittest.TestCase):
    def test_has_all_scenarios(self):
        d=calculate()
        self.assertEqual(len(d),15)
        self.assertEqual(set(x["scenario"] for x in d), {"Conservative","Base","Aggressive"})

    def test_year_five_matches_reviewed_workbook(self):
        s={x["scenario"]:x for x in calculate() if x["year"]==5}
        self.assertAlmostEqual(s["Conservative"]["operating_net_after_pcco_php"],-13040640,places=2)
        self.assertAlmostEqual(s["Base"]["operating_net_after_pcco_php"],1594080,places=2)
        self.assertAlmostEqual(s["Aggressive"]["operating_net_after_pcco_php"],32667300,places=2)
        self.assertAlmostEqual(s["Base"]["cumulative_result_php"],-15391920,places=2)

    def test_pcco_is_never_funded_in_a_loss(self):
        for x in calculate():
            if x["operating_net_after_pcco_php"] <0:
                self.assertEqual(x["pcco_budget_php"],0)

if __name__=="__main__": unittest.main()
