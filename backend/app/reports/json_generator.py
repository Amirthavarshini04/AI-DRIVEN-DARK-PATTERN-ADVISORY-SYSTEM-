import json
from typing import Dict, Any

def generate_scan_json(scan_data: Dict[str, Any]) -> str:
    export_payload = {
        "report_metadata": {
            "title": "AI Dark Pattern & Legal Compliance Audit Report",
            "framework": "CCPA Guidelines for Prevention and Regulation of Dark Patterns, 2023",
            "generated_at": scan_data.get("created_at"),
            "disclaimer": "This document is an academic decision-support analysis, not a legal certification."
        },
        "scan_details": {
            "id": scan_data.get("id"),
            "url": scan_data.get("url"),
            "scan_type": scan_data.get("scan_type"),
            "language": scan_data.get("language"),
            "risk_score": scan_data.get("risk_score"),
            "risk_category": scan_data.get("risk_category"),
            "findings_count": scan_data.get("findings_count")
        },
        "findings": scan_data.get("findings", [])
    }
    return json.dumps(export_payload, indent=2, ensure_ascii=False)
