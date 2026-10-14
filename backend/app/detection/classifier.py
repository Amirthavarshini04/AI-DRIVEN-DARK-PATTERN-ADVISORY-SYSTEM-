import re
import math
from typing import List, Dict, Any, Optional
from app.compliance.ccpa_library import get_guideline_by_code, CCPA_DARK_PATTERNS

# Regex pattern matchers for all 13 CCPA 2023 Guidelines in English, Tamil, and Hindi
PATTERNS = [
    {
        "code": "false_urgency",
        "category": "False Urgency",
        "severity": "High",
        "regex": [
            r"only\s+\d+\s+(?:items?|left|in\s+stock|rooms?\s+left)\b",
            r"hurry\b",
            r"ends?\s+in\b",
            r"deal\s+ends\s+in\b",
            r"limited\s+(?:time|period|stock)\b",
            r"fast\s+selling\b",
            r"selling\s+(?:out\s+)?fast\b",
            r"people\s+are\s+(?:looking|viewing|watching)\s+at\s+this\b",
            r"offer\s+expires\b",
            r"countdown\b",
            r"deal\s+expires\b",
            r"flash\s+sale\b",
            r"lightning\s+deal\b",
            r"deal\s+of\s+the\s+day\b",
            r"order\s+within\s+\d+.*to\s+get\b",
            r"last\s+chance\b",
            r"almost\s+gone\b",
            r"act\s+now\b",
            r"price\s+increases\s+soon\b",
            r"today\s+only\b",
            r"limited\s+time\s+offer\b",
            r"\d{1,2}:\d{2}(?::\d{2})?\s*(?:left|remaining|to\s+go)\b",
            # Tamil
            r"இன்னும்\s+\d+\s+மட்டுமே",
            r"விரைவில்\s+முடியும்",
            r"மின்னல்\s+விற்பனை",
            r"முடிவடைகிறது",
            r"விரையுங்கள்",
            r"வரையறுக்கப்பட்ட\s+நேரம்",
            # Hindi
            r"केवल\s+\d+\s+बचे\s+हैं",
            r"जल्दी\s+करें",
            r"सीमित\s+समय",
            r"ऑफर\s+समाप्त",
            r"अंतिम\s+अवसर",
            r"जल्द\s+ही\s+समाप्त"
        ],
        # Negative-case exclusion patterns: if ANY exclusion matches the line, skip False Urgency
        "exclusions": [
            r"\d+\s+rooms?\s+available\s+for\s+your\s+dates",
        ],
        "rationale": "Creates artificial scarcity and time pressure, forcing irrational immediate purchases.",
        "impact": "Consumers rush into purchasing without evaluating necessity or comparing prices on alternative platforms.",
        "recommendation": "Display real-time authentic inventory levels and static promotion terms without artificial countdown timers."
    },
    {
        "code": "basket_sneaking",
        "category": "Basket Sneaking",
        "severity": "Critical",
        "regex": [
            r"auto-add",
            r"added\s+to\s+cart\s+automatically",
            r"pre-checked",
            r"pre-selected",
            r"insurance\s+added",
            r"donation\s+added",
            r"protection\s+plan\s+included",
            r"unrequested\s+item",
            r"automatically\s+added\s+to\s+order",
            r"pre-ticked",
            r"care\s+plan\s+added",
            r"warranty\s+automatically\s+added",
            # Tamil
            r"தானாக\s+சேர்க்கப்பட்டது",
            r"காப்பீடு\s+சேர்க்கப்பட்டது",
            r"கூடை\s+நுழைப்பு",
            # Hindi
            r"स्वचालित\r?\n?\s*रूप\s*से\s*जोड़ा\s*गया",
            r"बीमा\s+जोड़ा\s+गया"
        ],
        "rationale": "Unilaterally inserts additional paid goods or optional fees into the consumer's cart without explicit affirmative choice.",
        "impact": "Consumers pay unexpected extra fees for unwanted products or services during checkout.",
        "recommendation": "Uncheck all optional items by default and mandate explicit user opt-in before adding charges."
    },
    {
        "code": "confirm_shaming",
        "category": "Confirm Shaming",
        "severity": "Medium",
        "regex": [
            r"no\s+thanks[,.]?\s+i\s+(?:prefer|don'?t\s+(?:like|want|care))",
            r"no,\s+i\s+hate\s+saving",
            r"i'll\s+pay\s+full\s+price",
            r"i\s+don'?t\s+(?:want\s+to\s+save|like\s+saving)\s+money",
            r"no,\s+i\s+prefer\s+paying\s+(?:more|full\s+price)",
            r"hate\s+saving",
            r"no,\s+i\s+don'?t\s+want\s+(?:a\s+)?discount",
            r"i\s+want\s+to\s+miss\s+out",
            r"i\s+don'?t\s+care\s+about\s+deals",
            r"i\s+prefer\s+paying\s+full\s+price",
            # Tamil
            r"இல்லை,\s+எனக்கு\s+தள்ளுபடி\s+தேவையில்லை",
            r"எனக்கு\s+பணம்\s+சேமிக்க\s+விருப்பமில்லை",
            # Hindi
            r"नहीं,\s+मुझे\s+पैसे\s+बचाना\s+पसंद\s+नहीं\s+है",
            r"नहीं,\s+मुझे\s+छूट\s+नहीं\s+चाहिए"
        ],
        "rationale": "Employs emotionally manipulative or guilt-inducing text to shame the user into selecting the merchant's preferred option.",
        "impact": "Subverts free consumer choice by provoking guilt or embarrassment.",
        "recommendation": "Replace manipulative decline text with clear, neutral labels like 'No thanks' or 'Decline'."
    },
    {
        "code": "forced_action",
        "category": "Forced Action",
        "severity": "Critical",
        "regex": [
            r"must\s+subscribe\s+to\s+continue",
            r"share\s+contacts\s+to\s+unlock",
            r"mandatory\s+sign-up\s+required",
            r"must\s+download\s+app\s+to\s+view",
            r"mandatory\s+account",
            r"sign\s+up\s+to\s+see\s+price",
            r"share\s+on\s+whatsapp\s+to\s+unlock",
            r"must\s+provide\s+phone\s+number\s+to\s+browse",
            r"you\s+must\s+(?:allow|accept|share|enable)\s+\S+\s+to\s+(?:continue|proceed|book)",
            r"must\s+allow\s+access\s+to\s+your\s+(?:contacts|location)",
            r"mandatory\s+(?:unrelated\s+)?(?:permissions?|contacts?|location)",
            r"(?:create|open)\s+an?\s+account\s+to\s+(?:see|view|access|check)",
            r"bundled\s+(?:purchase|subscription)\s+required",
            # Tamil
            r"கட்டாய\s+பதிவு",
            r"தொடர\s+பகிரவும்",
            r"கட்டாய\s+செயல்",
            # Hindi
            r"अनिवार्य\s+साइन-अप",
            r"आगे\s+बढ़ने\s+के\s+लिए\s+साझा\s+करें"
        ],
        "rationale": "Requires users to perform unrelated personal actions to access core services or product views.",
        "impact": "Infringes on consumer privacy and forces friction onto standard shopping tasks.",
        "recommendation": "Allow guest interaction and remove mandatory gating for basic product browsing."
    },
    {
        "code": "subscription_trap",
        "category": "Subscription Trap",
        "severity": "Critical",
        "regex": [
            r"cannot\s+cancel\s+online",
            r"hidden\s+cancellation",
            r"call\s+customer\s+service\s+to\s+cancel",
            r"subscription\s+auto-renews\s+without\s+cancel",
            r"difficult\s+to\s+cancel",
            r"call\s+to\s+unsubscribe",
            r"cancellation\s+fee\s+applies",
            r"contact\s+support\s+to\s+cancel",
            r"auto-renews\s+at\b",
            r"auto-renews\s+annually\s+at",
            r"(?:call|phone|email|visit\s+store)\s+(?:us\s+)?to\s+cancel",
            r"call\s+support\b",
            r"during\s+business\s+hours\s+to\s+cancel",
            r"auto.?renew(?:s|al)\b",
            r"cancel.*call\s+support",
            r"to\s+cancel,\s+call",
            # Tamil
            r"சந்தாவை\s+ரத்து\s+செய்ய\s+முடியாது",
            r"ரத்து\s+செய்ய\s+அழைக்கவும்",
            # Hindi
            r"सदस्यता\s+रद्द\s+करने\s+के\s+लिए\s+कॉल\s+करें",
            r"रद्द\s+करना\s+छुपाया\s+गया"
        ],
        "exclusions": [
            r"cancel\s+anytime\s+from\s+my\s+bookings",
        ],
        "rationale": "Makes enrolling in recurring billing seamless but makes cancellation complex, obscure, or physically demanding.",
        "impact": "Traps consumers in recurring automated credit charges they no longer desire.",
        "recommendation": "Provide a simple, 1-click online cancellation flow equally prominent as subscription enrolment."
    },
    {
        "code": "interface_interference",
        "category": "Interface Interference",
        "severity": "High",
        "regex": [
            r"pre-selected\s+premium",
            r"hidden\s+opt-out",
            r"tiny\s+gr[ae]y\s+text",
            r"greyed?\s+out\s+cancel",
            r"camouflaged\s+button",
            r"visual\s+trick",
            r"low\s+contrast\s+terms",
            r"obscured\s+link",
            r"faint\s+decline",
            # Tamil
            r"மறைக்கப்பட்ட\s+தேர்வு",
            r"சாம்பல்\s+நிற\s+ரத்து",
            # Hindi
            r"छिपा\s+हुआ\s+चेकबॉक्स",
            r"धुंधला\s+रद्द\s+बटन"
        ],
        "rationale": "Manipulates visual contrast or styling hierarchy to trick users away from selecting their intended choices.",
        "impact": "Confuses consumers into choosing premium or privacy-invasive alternatives.",
        "recommendation": "Provide equal visual contrast and balanced button prominence across all available actions."
    },
    {
        "code": "bait_and_switch",
        "category": "Bait and Switch",
        "severity": "High",
        "regex": [
            r"price\s+changed\s+at\s+checkout",
            r"advertised\s+item\s+unavailable\s+replaced",
            r"free\s+delivery\s+switched\s+to",
            r"price\s+increased\s+at\s+payment",
            r"higher\s+priced\s+alternative\s+substituted",
            r"deal\s+item\s+out\s+of\s+stock\s+see\s+alternative",
            r"(?:\d+%|₹\s*\d[\d,]*)\s+off\b.{0,80}today\s+only",
            r"today\s+only!.{0,40}(?:₹|rs\.?|\d+%)",
            # Tamil
            r"விலை\s+மாற்றப்பட்டது",
            r"இலவச\s+டெலிவரி\s+மாற்றப்பட்டது",
            # Hindi
            r"भुगतान\s+पर\s+कीमत\s+बदल\s+गई",
            r"मुफ्त\s+डिलीवरी\s+बदली\s+गई"
        ],
        "rationale": "Advertises one appealing offer but secretly delivers or substitutes a different, more expensive outcome.",
        "impact": "Baiting consumers on false pretenses and swapping items at cart finalization.",
        "recommendation": "Honor advertised pricing and notify users transparently of any genuine inventory discrepancies."
    },
    {
        "code": "drip_pricing",
        "category": "Drip Pricing",
        "severity": "Critical",
        "regex": [
            r"convenience\s+fee\s+added",
            r"convenience\s+fee\s+[₹\$€\d]",
            r"convenience\s+fee\b",
            r"service\s+fee\b",
            r"handling\s+charge\s+revealed",
            r"surge\s+fee",
            r"mandatory\s+platform\s+fee",
            r"drip\s+pricing",
            r"incremental\s+fee",
            r"packaging\s+fee\s+added",
            r"mandatory\s+booking\s+charge",
            r"additional\s+processing\s+fee\s+of\s+[₹\$€]",
            r"platform\s+handling\s+fee",
            r"(?:\+\s*taxes?\s*&?\s*fees?|excl(?:uding|\.?)\s+taxes?)",
            # Tamil
            r"கூடுதல்\s+கட்டணம்",
            r"அடக்கப்பட்ட\s+கட்டணம்",
            r"வசதி\s+கட்டணம்",
            # Hindi
            r"अतिरिक्त\s+शुल्क",
            r"छिपा\s+हुआ\s+शुल्क",
            r"सुविधा\s+शुल्क"
        ],
        "exclusions": [
            r"all\s+taxes\s+and\s+fees\s+included",
        ],
        "rationale": "Conceals essential mandatory charges until late stages of the purchase funnel.",
        "impact": "Misleads users into believing an item is cheaper than it actually is, leading to sunken-cost bias.",
        "recommendation": "Disclose the total inclusive price (including all mandatory fees) on the initial listing screen."
    },
    {
        "code": "disguised_ads",
        "category": "Disguised Advertisements",
        "severity": "Medium",
        "regex": [
            r"sponsored\s+story\s+disguised",
            r"fake\s+security\s+warning",
            r"click\s+here\s+to\s+fix\s+security",
            r"ad\s+formatted\s+as\s+editorial",
            r"promoted\s+link\s+masked",
            r"sponsored\s+recommendation\s+unlabeled",
            # Tamil
            r"மறைமுக\s+விளம்பரம்",
            r"போலி\s+பாதுகாப்பு\s+எச்சரிக்கை",
            # Hindi
            r"प्रायोजित\s+विज्ञापन\s+छिपाया\s+गया",
            r"नकली\s+चेतावनी"
        ],
        "rationale": "Camouflages commercial sponsored links or third-party ads to look like unbiased editorial reviews or system alerts.",
        "impact": "Deceives consumers into clicking commercial affiliate promotions under the guise of unbiased advice.",
        "recommendation": "Prominently label all sponsored links and advertisements with visible 'Sponsored' or 'Ad' tags."
    },
    {
        "code": "nagging",
        "category": "Nagging",
        "severity": "Low",
        "regex": [
            r"turn\s+on\s+notifications\s+to\s+continue",
            r"repeatedly\s+asking\s+for",
            r"remind\s+me\s+later\s+popup",
            r"enable\s+push\s+alerts",
            r"persistent\s+interruption",
            r"don'?t\s+leave\s+without",
            r"wait[!,]?\s*before\s+you\s+go",
            r"\bwait\b.{0,10}before\s+you\s+go",
            r"are\s+you\s+sure\s+you\s+want\s+to\s+leave",
            r"don'?t\s+leave\s+without\s+saving",
            r"before\s+you\s+go[,!]",
            # Tamil
            r"அறிவிப்புகளை\s+இயக்கவும்",
            r"மீண்டும்\s+மீண்டும்\s+கேட்கிறது",
            # Hindi
            r"सूचनाएं\s+चालू\s+करें",
            r"बार-बार\s+पूछना"
        ],
        "rationale": "Repeatedly disrupts consumer browsing with recurrent requests or popups demanding actions after previous refusals.",
        "impact": "Frustrates consumer navigation and causes cognitive fatigue until the user capitulates.",
        "recommendation": "Respect user refusal and maintain persistent opt-out state without intrusive re-prompts."
    },
    {
        "code": "trick_wording",
        "category": "Trick Wording",
        "severity": "Medium",
        "regex": [
            r"uncheck\s+(?:this|the)\s+box\s+if\s+you\s+(?:do\s+not|don'?t|prefer\s+not)",
            r"uncheck\s+if\s+you\s+do\s+not",
            r"don'?t\s+click\s+unless\s+you\s+want",
            r"do\s+not\s+opt-out",
            r"check\s+to\s+not\s+receive",
            r"double\s+negative",
            r"untick\s+to\s+opt\s+in",
            r"prefer\s+not\s+to\s+not\s+receive",
            r"prefer\s+not\s+to\s+(?:not\s+)?receive",
            # Tamil
            r"தேர்வு\s+செய்ய\s+வேண்டாம்",
            r"ரத்து\s+செய்ய\s+கிளிக்\s+செய்ய\s+வேண்டாம்",
            # Hindi
            r"अनचेक\s+करें\s+यदि\s+आप\s+नहीं",
            r"रद्द\s+न\s+करें"
        ],
        "rationale": "Employs double negatives or confusing phrasing to trick consumers into consenting to unwanted choices.",
        "impact": "Causes users to unintentionally consent to data sharing, marketing, or hidden subscriptions.",
        "recommendation": "Use simple, direct affirmative phrasing with clear single-action checkboxes."
    },
    {
        "code": "saas_billing",
        "category": "SaaS Billing",
        "severity": "Critical",
        "regex": [
            r"free\s+trial\s+automatically\s+charged",
            r"silent\s+auto-renewal",
            r"auto-debit\s+after\s+trial",
            r"charged\s+annual\s+subscription\s+without",
            r"recurring\s+charge\s+without\s+invoice",
            r"billed\s+automatically\s+after\s+(?:trial|free\s+period)\s+ends",
            r"charged\s+to\s+(?:the\s+)?card\s+on\s+file",
            r"no\s+(?:renewal\s+)?(?:reminder|notice|invoice)\s+will\s+be\s+sent",
            r"no\s+renewal\s+reminder",
            r"silently?\s+recurring\s+charge",
            # Tamil
            r"முன்னறிவிப்பின்றி\s+கட்டணம்\s+வசூலிக்கப்பட்டது",
            r"தானியங்கி\s+புதுப்பித்தல்",
            # Hindi
            r"बिना\s+सूचना\s+के\s+ऑटो-डेबिट",
            r"ट्रायल\s+के\s+बाद\s+गुप्त\s+शुल्क"
        ],
        "rationale": "Quietly charges recurring fees following a trial period without providing advance invoice notifications or billing alerts.",
        "impact": "Imposes surprise financial charges onto users who expected a non-recurring trial experience.",
        "recommendation": "Issue advance billing notifications prior to any trial renewal and seek explicit re-affirmation."
    },
    {
        "code": "deceptive_counting",
        "category": "Deceptive Counting",
        "severity": "High",
        "regex": [
            r"people\s+(?:are\s+)?(?:looking|viewing|watching)\s+(?:at\s+)?this\b",
            r"\d+\s+people\s+are\s+(?:looking|viewing|watching)",
            r"bought\s+in\s+last\s+(?:hour|24\s+hours)",
            r"booked\s+\d+\s+times?\s+in\s+(?:the\s+last|past)\s+24\s+hours",
            r"shoppers\s+viewed\s+this",
            r"fake\s+visitor\s+count",
            r"\d+\s+people\s+are\s+viewing",
            r"\d+\s+items?\s+in\s+cart\s+right\s+now",
            r"high\s+demand:\s+\d+\s+bought",
            r"\d+\s+(?:sold|bought)\s+today",
            # Tamil
            r"மக்கள்\s+இப்போது\s+பார்க்கிறார்கள்",
            r"கடந்த\s+1\s+மணி\s+நேரத்தில்\s+வாங்கப்பட்டது",
            # Hindi
            r"लोग\s+इसे\s+अभी\s+देख\s+रहे\s+हैं",
            r"पिछले\s+1\s+घंटे\s+में\s+खरीदा\s+गया"
        ],
        "rationale": "Fabricates fictitious viewer counts or inflated purchase metrics to exploit social proof and FOMO.",
        "impact": "Manipulates consumer risk perception by exaggerating popularity through fabricated numbers.",
        "recommendation": "Only display audited, legitimate real-time analytics backed by verifiable database logs."
    }
]

# Keywords that indicate a pre-checked checkbox is performing basket sneaking
BASKET_SNEAKING_CHECKBOX_KEYWORDS = re.compile(
    r"(?:insurance|donation|charity|protection\s+plan|add.?on|warranty|₹|rs\.?\s*\d|\$\s*\d|\d+\s*(?:rs|₹))",
    re.IGNORECASE
)


def detect_language(text: str) -> str:
    if re.search(r'[\u0B80-\u0BFF]', text):
        return "ta"
    elif re.search(r'[\u0900-\u097F]', text):
        return "hi"
    return "en"


def _build_finding(
    pattern_def: Dict[str, Any],
    snippet: str,
    dom_selector: str,
    language: str,
    confidence: float = 0.0
) -> Dict[str, Any]:
    guide = get_guideline_by_code(pattern_def["code"])
    clause_ref = guide["clause_reference"] if guide else "CCPA 2023 Guidelines"
    ccpa_cat = guide["category_name"] if guide else pattern_def["category"]

    clean_snippet = snippet.strip()
    if len(clean_snippet) > 250:
        clean_snippet = clean_snippet[:247] + "..."

    if confidence == 0.0:
        confidence = 0.92 if len(snippet) < 120 else 0.88

    return {
        "category": pattern_def["category"],
        "severity": pattern_def["severity"],
        "confidence": confidence,
        "text_snippet": clean_snippet,
        "dom_selector": dom_selector,
        "rationale": pattern_def["rationale"],
        "consumer_impact": pattern_def["impact"],
        "ccpa_clause": clause_ref,
        "ccpa_category": ccpa_cat,
        "recommendation": pattern_def["recommendation"],
        "language": language
    }


def _is_duplicate(new_finding: Dict[str, Any], existing_findings: List[Dict[str, Any]]) -> bool:
    """Substring-overlap dedup: same category + snippets overlap or dom_selector matches."""
    for f in existing_findings:
        if f["category"] != new_finding["category"]:
            continue
        s1 = f["text_snippet"]
        s2 = new_finding["text_snippet"]
        if s1 in s2 or s2 in s1 or f.get("dom_selector") == new_finding.get("dom_selector"):
            return True
    return False


def analyze_text_content(text: str, target_language: str = "auto") -> List[Dict[str, Any]]:
    """
    Standard text classifier: splits by lines/sentences and tests regex patterns.
    Fully backwards-compatible with text scanner.
    """
    findings = []
    detected_lang = detect_language(text) if target_language == "auto" else target_language

    # Split into lines and sentences
    lines = [line.strip() for line in re.split(r'[\n\.\!\?]', text) if len(line.strip()) >= 4]
    if not lines:
        lines = [text.strip()] if text.strip() else []

    for line in lines:
        for p in PATTERNS:
            # Check exclusions first
            exclusions = p.get("exclusions", [])
            if any(re.search(excl, line, re.IGNORECASE) for excl in exclusions):
                continue

            for rgx in p["regex"]:
                if re.search(rgx, line, re.IGNORECASE):
                    finding = _build_finding(
                        pattern_def=p,
                        snippet=line,
                        dom_selector=f".ec-element-{p['code']}",
                        language=detected_lang
                    )
                    if not _is_duplicate(finding, findings):
                        findings.append(finding)
                    break

    return findings


def analyze_structured_elements(elements: List[Dict[str, Any]], target_language: str = "auto") -> List[Dict[str, Any]]:
    """
    Analyzes structured e-commerce DOM elements with exact selectors and context types.
    Uses improved deduplication and keyword-filtered basket sneaking detection.
    """
    findings: List[Dict[str, Any]] = []

    for el in elements:
        text = el.get("text", "").strip()
        selector = el.get("selector", ".ec-element")
        is_checked = el.get("is_checked", False)

        detected_lang = detect_language(text) if target_language == "auto" else target_language

        # Contextual check: Pre-checked checkbox with add-on/paid keywords = Basket Sneaking
        if is_checked and BASKET_SNEAKING_CHECKBOX_KEYWORDS.search(text):
            sneaking_p = next((p for p in PATTERNS if p["code"] == "basket_sneaking"), None)
            if sneaking_p:
                finding = _build_finding(
                    pattern_def=sneaking_p,
                    snippet=f"[Pre-Checked] {text or 'Optional checkbox selected by default'}",
                    dom_selector=selector,
                    language=detected_lang
                )
                if not _is_duplicate(finding, findings):
                    findings.append(finding)

        if not text or len(text) < 4:
            continue

        # Check regex rules on element text
        for p in PATTERNS:
            # Check exclusions first
            exclusions = p.get("exclusions", [])
            if any(re.search(excl, text, re.IGNORECASE) for excl in exclusions):
                continue

            for rgx in p["regex"]:
                if re.search(rgx, text, re.IGNORECASE):
                    finding = _build_finding(
                        pattern_def=p,
                        snippet=text,
                        dom_selector=selector,
                        language=detected_lang
                    )
                    if not _is_duplicate(finding, findings):
                        findings.append(finding)
                    break

    return findings
