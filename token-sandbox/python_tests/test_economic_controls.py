import unittest
import pathlib,sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "python"))
from pcco_ledger import ParticipationLedger, ParticipationError
from reserve_verifier import BankSnapshot, IssuerSnapshot, verify_reserve, approve_simulated_incremental_mint, ReserveException

class PCCOTests(unittest.TestCase):
    def test_program_funding_rejects_ppkt_reserve(self):
        l=ParticipationLedger()
        with self.assertRaises(ParticipationError):
            l.fund_budget("f1","ppkt_reserves",50000)
        self.assertEqual(l.budget_cents,0)

    def test_no_awards_for_recruitment_or_holding(self):
        l=ParticipationLedger()
        with self.assertRaises(ParticipationError):
            l.award_verified_action("r1","DEMO_1","referral_mining",2,"proof")
        with self.assertRaises(ParticipationError):
            l.award_verified_action("r2","DEMO_1","holding_ppkt",2,"proof")

    def test_award_duplicate_and_event_chain(self):
        l=ParticipationLedger()
        l.award_verified_action("a1","DEMO_1","financial_literacy",3,"fake-test")
        with self.assertRaises(ParticipationError):
            l.award_verified_action("a1","DEMO_1","financial_literacy",3,"fake-test")
        self.assertEqual(l.credits["DEMO_1"],3)
        self.assertTrue(l.verify_event_chain())

    def test_budgeted_benefits_never_overcommit(self):
        l=ParticipationLedger()
        l.fund_budget("approved-1","approved_unrestricted_surplus",200)
        l.award_verified_action("a1","DEMO_1","community_service",2,"fake")
        l.reserve_budgeted_benefit("benefit-1","DEMO_1",1,150)
        self.assertEqual(l.uncommitted_cents,50)
        with self.assertRaises(ParticipationError):
            l.reserve_budgeted_benefit("benefit-2","DEMO_1",1,100)
        self.assertEqual(l.credits["DEMO_1"],1)

    def test_no_unfunded_redemption(self):
        l=ParticipationLedger()
        l.award_verified_action("a1","DEMO_1","community_service",1,"fake")
        with self.assertRaises(ParticipationError):
            l.reserve_budgeted_benefit("ben1","DEMO_1",1,1)

class ReserveTests(unittest.TestCase):
    def test_fully_covered_fiat_liability(self):
        banks=[BankSnapshot("BANK_A",50000000,0,"SYN_1"), BankSnapshot("BANK_B",50000000,0,"SYN_2")]
        issuer=IssuerSnapshot(1000000*1000000,0)
        s=verify_reserve(banks,issuer,stress_redemption_bps=3000)
        self.assertTrue(s.fully_backed)
        self.assertTrue(s.liquid_under_stress)
        self.assertFalse(s.minting_should_halt)

    def test_burn_without_fiat_payout_retains_liability(self):
        banks=[BankSnapshot("A",50000000,0,"SYN_1"),BankSnapshot("B",50000000,0,"SYN_2")]
        issuer=IssuerSnapshot(800000*1000000,20000000)
        s=verify_reserve(banks,issuer)
        self.assertEqual(s.liability_centavos,100000000)
        self.assertTrue(s.fully_backed)

    def test_bank_frozen_stress_halts_mint(self):
        banks=[BankSnapshot("A",50000000,50000000,"SYN_1"),BankSnapshot("B",50000000,10000000,"SYN_2")]
        s=verify_reserve(banks,IssuerSnapshot(1000000*1000000,0),stress_redemption_bps=5000)
        self.assertTrue(s.fully_backed)
        self.assertFalse(s.liquid_under_stress)
        self.assertEqual(s.redemption_stress_gap_centavos,10000000)
        self.assertTrue(s.minting_should_halt)

    def test_custody_concentration_halts_mint(self):
        banks=[BankSnapshot("A",90000000,0,"SYN_1"),BankSnapshot("B",10000000,0,"SYN_2")]
        s=verify_reserve(banks,IssuerSnapshot(1000000*1000000,0))
        self.assertTrue(s.fully_backed)
        self.assertTrue(s.minting_should_halt)

    def test_unfunded_mint_cannot_use_existing_spare_reserves(self):
        self.assertFalse(approve_simulated_incremental_mint(10000000,9000000,0,1000000))
        self.assertTrue(approve_simulated_incremental_mint(10000000,10000000,10000,100*1000000))
        self.assertFalse(approve_simulated_incremental_mint(10000000,10000000,10000,101*1000000))

    def test_token_dust_liability_rounds_up(self):
        b=[BankSnapshot("A",1,0,"SYN_1"),BankSnapshot("B",1,0,"SYN_2")]
        s=verify_reserve(b,IssuerSnapshot(10001,0))
        self.assertEqual(s.liability_centavos,2)

    def test_rejects_missing_evidence(self):
        with self.assertRaises(ReserveException):
            verify_reserve([BankSnapshot("A",100,0,"")],IssuerSnapshot(1000000,0))

if __name__=="__main__": unittest.main()
