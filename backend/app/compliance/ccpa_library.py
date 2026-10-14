"""
CCPA Dark Pattern Compliance Reference Library (2023 Guidelines)
Official Reference: Central Consumer Protection Authority Guidelines for Prevention and Regulation of Dark Patterns, 2023
Published under section 18 of Consumer Protection Act, 2019 (35 of 2019).
"""

CCPA_DARK_PATTERNS = [
    {
        "category_code": "false_urgency",
        "category_name": "False Urgency",
        "clause_reference": "Annexure 1, Item 1",
        "plain_explanation": "Falsely creating a sense of urgency or scarcity to pressure consumers into immediate purchase decisions or action.",
        "problematic_examples": [
            "Only 2 items left in stock - order within 03m 12s!",
            "14 other people are looking at this item right now",
            "Offer expires in 10 minutes (timer resets on refresh)",
            "மின்னல் விற்பனை! இன்னும் 2 நிமிடங்கள் மட்டுமே! (Flash Sale! Only 2 minutes left!)",
            "केवल 3 स्टॉक में बचे हैं! तुरंत खरीदें! (Only 3 left in stock! Buy now!)"
        ],
        "compliant_alternative": "Accurately state genuine stock levels or real promotional expiry dates without dynamic artificial countdowns.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "basket_sneaking",
        "category_name": "Basket Sneaking",
        "clause_reference": "Annexure 1, Item 2",
        "plain_explanation": "Adding additional items, services, delivery guarantees, or donation fees to the shopping cart automatically without explicit user consent.",
        "problematic_examples": [
            "Automatically pre-checking a ₹49 delivery insurance checkbox",
            "Auto-adding a ₹10 carbon-neutral donation fee at checkout",
            "Adding extended product warranty without explicit opt-in action"
        ],
        "compliant_alternative": "Keep optional addons unchecked by default and require affirmative opt-in choice by the user.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "confirm_shaming",
        "category_name": "Confirm Shaming",
        "clause_reference": "Annexure 1, Item 3",
        "plain_explanation": "Using emotional blackmail, guilt-inducing language, or ridicule to compel users to accept an offer or opt into a service.",
        "problematic_examples": [
            "No thanks, I prefer paying full price and losing money",
            "No, I don't care about saving my family money",
            "இல்லை, எனக்கு தள்ளுபடி தேவையில்லை (No, I don't need a discount)",
            "नहीं, मुझे पैसे बचाना पसंद नहीं है (No, I don't like saving money)"
        ],
        "compliant_alternative": "Provide clear, neutral rejection choices such as 'No thanks' or 'Decline offer'.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "forced_action",
        "category_name": "Forced Action",
        "clause_reference": "Annexure 1, Item 4",
        "plain_explanation": "Compelling users to take additional unrelated actions (e.g. sharing personal contact lists, signing up for unrelated newsletters) to buy a product.",
        "problematic_examples": [
            "Subscribe to daily promotional SMS to view item details",
            "Mandatory phone contact sync to unlock cart discount",
            "Forced creation of account before viewing delivery pin code availability"
        ],
        "compliant_alternative": "Allow guest checkout or voluntary opt-in choices without blocking basic e-commerce functions.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "subscription_trap",
        "category_name": "Subscription Trap",
        "clause_reference": "Annexure 1, Item 5",
        "plain_explanation": "Making it easy to sign up for a recurring subscription or membership but excessively difficult, complex, or hidden to cancel it.",
        "problematic_examples": [
            "One-click subscribe button vs 7-step customer service phone call requirement to cancel",
            "Hiding cancellation option under obscure nesting menus",
            "Forcing user to send physically mailed cancellation letters"
        ],
        "compliant_alternative": "Provide a simple, prominent cancellation mechanism with equal ease of access as the subscription flow.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "interface_interference",
        "category_name": "Interface Interference",
        "clause_reference": "Annexure 1, Item 6",
        "plain_explanation": "Manipulating the visual layout, button hierarchy, or contrast to obscure important information or trick users into picking pre-selected options.",
        "problematic_examples": [
            "Highlighting 'Accept All Premium' in bright green while making 'Standard Free' invisible low-contrast grey text",
            "Swapping 'Cancel' and 'Confirm' button positions counter-intuitively",
            "Displaying tiny illegible terms font for recurring charges"
        ],
        "compliant_alternative": "Ensure equal visual prominence for choices and clear high-contrast typography for essential pricing information.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "bait_and_switch",
        "category_name": "Bait and Switch",
        "clause_reference": "Annexure 1, Item 7",
        "plain_explanation": "Advertising an attractive outcome (e.g. low price or specific item availability) but delivering a different, higher-priced, or inferior product upon checkout.",
        "problematic_examples": [
            "Advertising laptop for ₹29,999 on banner but changing cart price to ₹38,999 at payment page",
            "Promising free instant delivery but switching to ₹199 express charge automatically"
        ],
        "compliant_alternative": "Honor advertised rates throughout the purchase funnel and notify user immediately of any legitimate stock or price changes.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "drip_pricing",
        "category_name": "Drip Pricing",
        "clause_reference": "Annexure 1, Item 8",
        "plain_explanation": "Revealing hidden mandatory fees, convenience charges, or platform fees incrementally as the buyer moves through the checkout process.",
        "problematic_examples": [
            "Displaying ₹499 item price initially, then adding ₹99 handling fee, ₹40 convenience fee, and ₹50 surge fee at final payment screen",
            "அடக்கப்பட்ட கட்டணம்: கட்டணக் கட்டத்தில் மட்டும் வெளிப்படுத்தப்படும் (Concealed mandatory fees revealed only at final screen)",
            "भुगतान चरण में छिपे हुए सुविधा शुल्क जोड़ना (Adding hidden convenience fees at payment stage)"
        ],
        "compliant_alternative": "Display total inclusive price (item cost + mandatory platform/handling fees) on the initial product page.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "disguised_ads",
        "category_name": "Disguised Advertisements",
        "clause_reference": "Annexure 1, Item 9",
        "plain_explanation": "Designing sponsored advertisements, paid product placement, or affiliate links to look like organic editorial content, customer reviews, or system alerts.",
        "problematic_examples": [
            "Paid sponsored banner formatted exactly like an independent consumer product ranking article",
            "Fake 'System Security Alert - Click Here to Fix' button leading to third-party ad"
        ],
        "compliant_alternative": "Clearly tag sponsored content with visible labels like 'Sponsored', 'Ad', or 'Paid Promotion'.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "nagging",
        "category_name": "Nagging",
        "clause_reference": "Annexure 1, Item 10",
        "plain_explanation": "Repeatedly interrupting the user's workflow with popups, push permission requests, or membership upgrade prompts despite previous rejections.",
        "problematic_examples": [
            "Prompting 'Enable Push Notifications' on every page click after user selected 'Never'",
            "Repeated full-screen modal demanding app installation before browsing items"
        ],
        "compliant_alternative": "Respect user refusal and maintain persistent opt-out state without intrusive re-prompts.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "trick_wording",
        "category_name": "Trick Wording",
        "clause_reference": "Annexure 1, Item 11",
        "plain_explanation": "Using ambiguous language, double negatives, or confusing phrasing to deceive users into selecting options they did not intend.",
        "problematic_examples": [
            "Uncheck this box if you do not wish to opt-out of receiving promotional calls",
            "Do not click here unless you want to cancel your non-refundable booking refund claim"
        ],
        "compliant_alternative": "Use simple, unambiguous affirmative statements (e.g., 'Send me promotional emails').",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "saas_billing",
        "category_name": "SaaS Billing",
        "clause_reference": "Annexure 1, Item 12",
        "plain_explanation": "Collecting credit card details for a 'Free Trial' and quietly converting it into auto-recurring paid billing without advance notification or easy cancellation.",
        "problematic_examples": [
            "Charging ₹2,999 annual fee automatically at end of 7-day trial without prior warning email",
            "Silent auto-renewal without invoice notification"
        ],
        "compliant_alternative": "Provide clear advance billing alerts before trial expiry and require explicit renewal consent.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    },
    {
        "category_code": "deceptive_counting",
        "category_name": "Deceptive Counting",
        "clause_reference": "Annexure 1, Item 1 (related — Deceptive Counting)",
        "plain_explanation": "Presenting false stats or manipulated numbers regarding purchases, views, or ratings to mislead consumers about popularity.",
        "problematic_examples": [
            "5,000 users bought this product in the last 1 hour (hardcoded static popup)",
            "Fabricated 5-star customer review count"
        ],
        "compliant_alternative": "Only display verified real-time metrics backed by authentic order logs.",
        "official_url": "https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf",
        "last_reviewed": "2023-11-30"
    }
]

def get_all_guidelines():
    return CCPA_DARK_PATTERNS

def get_guideline_by_code(code: str):
    for item in CCPA_DARK_PATTERNS:
        if item["category_code"] == code or item["category_name"].lower() == code.lower():
            return item
    return None
