import csv
import io
from typing import Dict, Any

def generate_scan_csv(scan_data: Dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Metadata Header
    writer.writerow(["SCAN AUDIT REPORT", ""])
    writer.writerow(["Scan ID", scan_data.get("id", "")])
    writer.writerow(["Target URL / Input", scan_data.get("url") or "Pasted Text Analysis"])
    writer.writerow(["Language", scan_data.get("language", "auto")])
    writer.writerow(["Scan Date", str(scan_data.get("created_at", ""))])
    writer.writerow(["Overall Risk Score", f"{scan_data.get('risk_score', 0)} / 100"])
    writer.writerow(["Risk Category", scan_data.get("risk_category", "")])
    writer.writerow(["Total Findings", len(scan_data.get("findings", []))])
    writer.writerow([])
    
    # Findings Headers
    writer.writerow([
        "Finding ID", "Category", "Severity", "Confidence",
        "CCPA Guideline Clause", "Text Evidence / Snippet",
        "Rationale", "Consumer Impact", "Recommendation"
    ])
    
    for f in scan_data.get("findings", []):
        writer.writerow([
            f.get("id", ""),
            f.get("category", ""),
            f.get("severity", ""),
            f.get("confidence", ""),
            f.get("ccpa_clause", ""),
            f.get("text_snippet", ""),
            f.get("rationale", ""),
            f.get("consumer_impact", ""),
            f.get("recommendation", "")
        ])
        
    return output.getvalue()
