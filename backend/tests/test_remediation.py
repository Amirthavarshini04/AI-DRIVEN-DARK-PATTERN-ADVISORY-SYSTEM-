from app.remediation.engine import generate_remediation_alternative, verify_remediation

def test_remediation_generation():
    proposed, rationale, fixable = generate_remediation_alternative("Hurry! Only 2 left!", "False Urgency")
    assert "Standard pricing applies" in proposed
    assert fixable is True

def test_remediation_verification():
    orig = "Hurry! Only 2 items left in stock - Offer expires in 03m 12s!"
    proposed = "Standard product pricing. Delivery option details available at checkout."
    res = verify_remediation(orig, proposed, "False Urgency")
    assert res["is_verified"] is True
    assert res["after_risk"] < res["before_risk"]
