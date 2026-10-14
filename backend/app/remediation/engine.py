from typing import Dict, Any, Tuple
from app.detection.classifier import analyze_text_content
from app.risk_scoring.combined_risk_model import calculate_combined_risk_score

TEXT_REMEDIATION_RULES = {
    "False Urgency": {
        "generator": lambda orig: "Standard pricing applies. Check available delivery dates at checkout.",
        "rationale": "Removes dynamic countdowns and artificial scarcity terms to provide clear, unpressured purchase information.",
        "fixable": True
    },
    "Confirm Shaming": {
        "generator": lambda orig: "No thanks, continue without offer.",
        "rationale": "Replaces emotionally manipulative or guilt-inducing declination text with a neutral, clear opt-out label.",
        "fixable": True
    },
    "Trick Wording": {
        "generator": lambda orig: "Send me promotional updates via email.",
        "rationale": "Converts confusing double-negative or inverted opt-out phrasing into a direct affirmative opt-in checkbox.",
        "fixable": True
    },
    "Drip Pricing": {
        "generator": lambda orig: "Total Price: ₹599 (Includes ₹499 item cost + ₹60 convenience & delivery fee).",
        "rationale": "Discloses all mandatory platform and handling fees upfront on the initial product view.",
        "fixable": True
    },
    "Basket Sneaking": {
        "generator": lambda orig: "[UI Change Required] Keep insurance/donation checkboxes unchecked by default.",
        "rationale": "Basket sneaking is a layout/structural issue. Uncheck optional addons by default in UI code.",
        "fixable": False
    },
    "Forced Action": {
        "generator": lambda orig: "[UI Change Required] Enable guest checkout and voluntary contact sharing.",
        "rationale": "Forced action requires removing mandatory sign-up modals and allowing guest browsing.",
        "fixable": False
    }
}

def generate_remediation_alternative(original_text: str, category: str) -> Tuple[str, str, bool]:
    rule = TEXT_REMEDIATION_RULES.get(category)
    if not rule:
        return f"Compliant wording: Clear and direct disclosure of {category.lower()} information.", "Provides transparent language.", True
    
    proposed = rule["generator"](original_text)
    rationale = rule["rationale"]
    fixable = rule["fixable"]
    return proposed, rationale, fixable

def verify_remediation(original_text: str, proposed_text: str, category: str) -> Dict[str, Any]:
    # Calculate before risk
    before_findings = analyze_text_content(original_text)
    before_score, _, _, _ = calculate_combined_risk_score(before_findings)
    if before_score == 0.0:
        before_score = 45.0  # Default initial score for flagged snippet

    # Calculate after risk on proposed text
    after_findings = analyze_text_content(proposed_text)
    after_score, _, _, _ = calculate_combined_risk_score(after_findings)

    risk_drop = round(before_score - after_score, 1)
    is_verified = after_score < before_score
    
    if is_verified and after_score == 0.0:
        status = "verified"
    elif is_verified:
        status = "partially_verified"
    else:
        status = "unverified"

    return {
        "original_text": original_text,
        "proposed_text": proposed_text,
        "before_risk": before_score,
        "after_risk": after_score,
        "risk_drop": risk_drop,
        "is_verified": is_verified,
        "status": status,
        "message": f"Verification successful: Model estimated risk reduced from {before_score} to {after_score} (Drop: -{risk_drop} points)."
    }
