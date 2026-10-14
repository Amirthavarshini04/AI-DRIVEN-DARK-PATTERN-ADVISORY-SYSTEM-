import math
from typing import List, Dict, Any, Tuple

# Base severity weights
SEVERITY_WEIGHTS = {
    "Critical": 35.0,
    "High": 25.0,
    "Medium": 15.0,
    "Low": 8.0
}

# Co-occurrence multipliers (when multiple coercive patterns appear together)
CO_OCCURRENCE_MULTIPLIERS = {
    ("False Urgency", "Drip Pricing"): 1.35,      # High coercion + hidden fees
    ("Basket Sneaking", "Trick Wording"): 1.30,   # Hidden check + confused text
    ("Confirm Shaming", "False Urgency"): 1.25,   # Emotional guilt + artificial rush
    ("Forced Action", "Subscription Trap"): 1.40, # Mandatory gate + hidden recurring cost
}

# λ tuning constant: raw_sum / LAMBDA controls how fast the score saturates
# With λ=55: 1 Critical (35) → ~47, 2 Critical (70) → ~72, all 13 mixed (≥200) → ~98
_LAMBDA = 55.0


def calculate_combined_risk_score(findings: List[Dict[str, Any]]) -> Tuple[float, str, List[str], Dict[str, Any]]:
    """
    Computes page-level risk score (0-100) using an exponential diminishing-returns formula
    so that partial detection also scores meaningfully and 13 detected patterns reach ≥80.

    Formula: score = min(100, 100 × (1 − e^(−raw_sum / λ)) × co_occurrence_multiplier)

    Returns: (score, risk_band, top_contributing_categories, explanation_dict)
    """
    if not findings:
        return 0.0, "Low Risk", [], {
            "base_score": 0.0,
            "co_occurrence_multiplier": 1.0,
            "final_score": 0.0,
            "formula_explanation": "No dark patterns detected on the page. Risk is evaluated at 0/100."
        }

    raw_sum = 0.0
    category_counts: Dict[str, int] = {}
    severity_breakdown = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

    for f in findings:
        cat = f.get("category", "Unknown")
        sev = f.get("severity", "Medium")

        weight = SEVERITY_WEIGHTS.get(sev, 15.0)
        raw_sum += weight

        category_counts[cat] = category_counts.get(cat, 0) + 1
        severity_breakdown[sev] = severity_breakdown.get(sev, 0) + 1

    # Deduplicate category counts for co-occurrence check (one finding per category is enough)
    detected_cats = set(category_counts.keys())
    multiplier = 1.0
    co_occurred_pairs: List[str] = []

    for (cat1, cat2), mult in CO_OCCURRENCE_MULTIPLIERS.items():
        if cat1 in detected_cats and cat2 in detected_cats:
            if mult > multiplier:
                multiplier = mult
            co_occurred_pairs.append(f"{cat1} + {cat2}")

    # Exponential diminishing-returns formula
    base_exponential = 100.0 * (1.0 - math.exp(-raw_sum / _LAMBDA))
    final_score = round(min(100.0, base_exponential * multiplier), 1)

    # Determine risk category band
    if final_score <= 25.0:
        band = "Low Risk"
    elif final_score <= 50.0:
        band = "Moderate Risk"
    elif final_score <= 75.0:
        band = "High Risk"
    else:
        band = "Critical Risk"

    # Sort categories by contribution count
    top_categories = sorted(category_counts.keys(), key=lambda k: category_counts[k], reverse=True)

    explanation = {
        "findings_count": len(findings),
        "severity_breakdown": severity_breakdown,
        "raw_severity_sum": round(raw_sum, 1),
        "co_occurrence_multiplier": multiplier,
        "co_occurred_pairs": co_occurred_pairs,
        "final_score": final_score,
        "risk_band": band,
        "formula_explanation": (
            f"Score = min(100, 100 × (1 − e^(−{raw_sum:.1f}/{_LAMBDA})) × {multiplier}). "
            f"Base exponential: {base_exponential:.1f}. "
            f"Co-occurrence pairs: {co_occurred_pairs or 'none'}."
        )
    }

    return final_score, band, top_categories, explanation
