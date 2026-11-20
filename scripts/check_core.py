import json,pathlib,sys
r=pathlib.Path(__file__).resolve().parents[1]
m=json.loads((r/"manifest.json").read_text()); v=json.loads((r/"version.json").read_text())
g=json.loads((r/"70_DELIVERY/release-gates.json").read_text())["gates"]
loc=json.loads((r/"30_CHARTER/operating-location-model.json").read_text())
assert m["status"]=="unratified" and m["is_issued_token"] is False and m["has_live_customer_funds"] is False
assert m["corporate_domicile"]=="UNDECIDED" and m["delivery_location_preferred"]=="Philippines"
assert v["charter_ratified"] is False and len(g)==8 and all(x["status"]!="pass" for x in g)
assert not loc["numeric_estimate_publicly_verified"] and not loc["consolidated_savings_verified"]
print("PPKT CORE checks passed; release gates remain blocked")
