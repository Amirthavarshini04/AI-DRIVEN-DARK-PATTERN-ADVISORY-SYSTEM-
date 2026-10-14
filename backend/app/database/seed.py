from app.database.session import SessionLocal, engine, Base
from app.database.models import Scan, Finding, ComplianceGuideline
from app.compliance.ccpa_library import CCPA_DARK_PATTERNS
import datetime

from sqlalchemy import text

def migrate_db_columns():
    with engine.connect() as conn:
        for col_name, col_type in [
            ("fetch_method", "VARCHAR DEFAULT 'http_client'"),
            ("content_length_analyzed", "INTEGER DEFAULT 0"),
            ("warnings", "TEXT DEFAULT '[]'"),
            ("page_title", "VARCHAR")
        ]:
            try:
                conn.execute(text(f"ALTER TABLE scans ADD COLUMN {col_name} {col_type}"))
                conn.commit()
            except Exception:
                pass

def init_and_seed_db():
    Base.metadata.create_all(bind=engine)
    migrate_db_columns()
    db = SessionLocal()

    # Seed CCPA Guidelines if empty
    if db.query(ComplianceGuideline).count() == 0:
        for g in CCPA_DARK_PATTERNS:
            cg = ComplianceGuideline(
                category_code=g["category_code"],
                category_name=g["category_name"],
                clause_reference=g["clause_reference"],
                plain_explanation=g["plain_explanation"],
                problematic_examples=g["problematic_examples"],
                compliant_alternative=g["compliant_alternative"],
                official_url=g["official_url"],
                last_reviewed=g["last_reviewed"]
            )
            db.add(cg)
        db.commit()

    # Seed initial realistic scan records if empty
    if db.query(Scan).count() == 0:
        sample_scans = [
            {
                "url": "https://quick-buy-india-demo.com/checkout",
                "scan_type": "url",
                "language": "en",
                "risk_score": 68.5,
                "risk_category": "High Risk",
                "findings": [
                    {
                        "category": "False Urgency",
                        "severity": "High",
                        "confidence": 0.94,
                        "text_snippet": "Hurry! Only 2 items left in stock - Offer expires in 04m 12s!",
                        "dom_selector": ".timer-banner-countdown",
                        "rationale": "Creates artificial scarcity and time pressure, forcing irrational immediate purchases.",
                        "consumer_impact": "Consumers rush into purchasing without evaluating necessity or comparing prices on alternative platforms.",
                        "ccpa_clause": "Annexure 1 - Clause 3(a)",
                        "ccpa_category": "False Urgency",
                        "recommendation": "Display real-time authentic inventory levels and static promotion terms without artificial countdown timers."
                    },
                    {
                        "category": "Drip Pricing",
                        "severity": "Critical",
                        "confidence": 0.91,
                        "text_snippet": "Mandatory Platform & Handling Fee: ₹69 added at final checkout screen",
                        "dom_selector": ".checkout-fee-breakdown",
                        "rationale": "Conceals essential mandatory charges until late stages of the purchase funnel.",
                        "consumer_impact": "Misleads users into believing an item is cheaper than it actually is.",
                        "ccpa_clause": "Annexure 1 - Clause 3(h)",
                        "ccpa_category": "Drip Pricing",
                        "recommendation": "Disclose total inclusive price on the initial product page."
                    }
                ]
            },
            {
                "url": "https://fashion-bazaar.in/item/1092",
                "scan_type": "url",
                "language": "ta",
                "risk_score": 52.0,
                "risk_category": "High Risk",
                "findings": [
                    {
                        "category": "False Urgency",
                        "severity": "High",
                        "confidence": 0.92,
                        "text_snippet": "மின்னல் விற்பனை! இன்னும் 2 நிமிடங்கள் மட்டுமே! (Flash Sale! Only 2 minutes left!)",
                        "dom_selector": ".ta-banner-urgency",
                        "rationale": "செயற்கையான அவசரத்தை உருவாக்கல் (Creates artificial urgency in Tamil).",
                        "consumer_impact": "பயனர்களை தவறாக வழிநடத்துதல் (Misleads users into quick purchasing decisions).",
                        "ccpa_clause": "Annexure 1 - Clause 3(a)",
                        "ccpa_category": "False Urgency",
                        "recommendation": "நேர்மையான பங்கு அளவைக் காட்டுங்கள் (Display authentic stock)."
                    }
                ]
            },
            {
                "url": "https://mega-store-delhi.co.in/cart",
                "scan_type": "url",
                "language": "hi",
                "risk_score": 45.0,
                "risk_category": "Moderate Risk",
                "findings": [
                    {
                        "category": "Confirm Shaming",
                        "severity": "Medium",
                        "confidence": 0.89,
                        "text_snippet": "नहीं, मुझे पैसे बचाना पसंद नहीं है (No, I don't like saving money)",
                        "dom_selector": ".optout-decline-btn",
                        "rationale": "भावात्मक हेरफेर (Emotional manipulation in Hindi declination button text).",
                        "consumer_impact": "उपभोक्ता पर अनावश्यक दबाव (Unnecessary consumer guilt/pressure).",
                        "ccpa_clause": "Annexure 1 - Clause 3(c)",
                        "ccpa_category": "Confirm Shaming",
                        "recommendation": "स्पष्ट और तटस्थ विकल्प प्रदान करें (Provide clear neutral option)."
                    }
                ]
            }
        ]

        for scan_data in sample_scans:
            s_obj = Scan(
                url=scan_data["url"],
                scan_type=scan_data["scan_type"],
                language=scan_data["language"],
                status="completed",
                risk_score=scan_data["risk_score"],
                risk_category=scan_data["risk_category"],
                findings_count=len(scan_data["findings"]),
                raw_text="Sample scan text content"
            )
            db.add(s_obj)
            db.flush()

            for f in scan_data["findings"]:
                f_obj = Finding(
                    scan_id=s_obj.id,
                    category=f["category"],
                    severity=f["severity"],
                    confidence=f["confidence"],
                    text_snippet=f["text_snippet"],
                    dom_selector=f["dom_selector"],
                    rationale=f["rationale"],
                    consumer_impact=f["consumer_impact"],
                    ccpa_clause=f["ccpa_clause"],
                    ccpa_category=f["ccpa_category"],
                    recommendation=f["recommendation"]
                )
                db.add(f_obj)

        db.commit()

    db.close()
