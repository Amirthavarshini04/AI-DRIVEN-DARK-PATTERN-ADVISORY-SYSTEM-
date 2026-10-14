from app.risk_scoring.combined_risk_model import calculate_combined_risk_score

def test_risk_score_clean():
    score, band, _, _ = calculate_combined_risk_score([])
    assert score == 0.0
    assert band == "Low Risk"

def test_risk_score_co_occurrence():
    findings = [
        {"category": "False Urgency", "severity": "High"},
        {"category": "Drip Pricing", "severity": "Critical"}
    ]
    score, band, top_cats, explanation = calculate_combined_risk_score(findings)
    assert score > 50.0
    assert band in ("High Risk", "Critical Risk")
    assert explanation["co_occurrence_multiplier"] == 1.35
