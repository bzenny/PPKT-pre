"""Reproduce PPKT 5-year scenario arithmetic from JSON; no investment forecasting claims."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
def calculate(source=None):
    data=json.loads((source or ROOT/"60_EVIDENCE/5y_model_inputs.json").read_text())
    global_p=data["global_inputs"]
    results=[]
    for name,sp in data["scenario_parameters"].items():
        cumulative=0
        for i in range(5):
            users=sp["users"][i]
            transactions=users*sp["monthly_transactions_per_user"]*12
            cash_payouts=transactions*sp["fiat_payout_share"]
            wallet_transfers=transactions-cash_payouts
            amount=sp["average_payout_php"]
            client_fee=global_p["customer_fee_fixed_php"]+global_p["customer_fee_rate"]*amount
            provider=global_p["provider_fixed_php"]+global_p["provider_rate"]*amount
            cash_income=cash_payouts*client_fee
            merchant_income=sp["merchant_clients"][i]*sp["merchant_fee_monthly_php"]*12
            provider_cost=cash_payouts*(provider+global_p["other_variable_cost_php"])
            wallet_cost=wallet_transfers*sp["wallet_cost_per_transfer_php"]
            merchant_cost=sp["merchant_clients"][i]*sp["merchant_cost_monthly_php"]*12
            overhead=sp["fixed_opex_monthly"][i]*12
            pre_tax=cash_income+merchant_income-provider_cost-wallet_cost-merchant_cost-overhead
            post_tax=pre_tax-max(0,pre_tax)*global_p["effective_profit_tax_rate"]
            pcco_budget=max(0,post_tax)*global_p["pcco_share_of_positive_aftertax_surplus"]
            net=post_tax-pcco_budget
            cumulative+=net
            circulation=users*sp["token_holder_share"]*sp["average_ppkt_balance_php"]
            stressgap=max(0,circulation*global_p["rapid_redemption_stress"]-circulation*(1-global_p["bank_blocked_fraction"]))
            results.append(dict(scenario=name,year=i+1,users=users,annual_transfers=transactions,
               annual_cash_payouts=cash_payouts,gross_annual_revenue_php=cash_income+merchant_income,
               operating_net_after_pcco_php=net,cumulative_result_php=cumulative,
               illustrative_redeemable_liability_php=circulation,liquidity_stress_gap_php=stressgap,
               pcco_budget_php=pcco_budget))
    return results

if __name__=="__main__":
    for x in calculate():
        if x["year"]==5:
            print(x["scenario"],"year5 net",round(x["operating_net_after_pcco_php"],2),
            "5Y cumulative",round(x["cumulative_result_php"],2),"PPKT liability",round(x["illustrative_redeemable_liability_php"],2))
