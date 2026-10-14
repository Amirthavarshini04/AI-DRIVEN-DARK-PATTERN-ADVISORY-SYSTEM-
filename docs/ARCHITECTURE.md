# System Architecture & Technical Specifications

## 1. System Topology & Data Flow

```mermaid
graph TD
    User[User / Compliance Auditor] -->|HTTP / SPA| ReactUI[Next.js / React Frontend Dashboard]
    Ext[Chrome Manifest V3 Extension] -->|DOM Text Inspection| FastApi[FastAPI REST Backend]
    ReactUI -->|REST API| FastApi

    subgraph Backend Core (Python 3.10+)
        FastApi --> SSRF[SSRF Security Guard]
        FastApi --> Router[API Routers]
        Router --> NLP[Multilingual NLP Classifier (EN / HI / TA)]
        Router --> RiskModel[Learned Combined Risk Scoring Model]
        Router --> RemEngine[Remediation & Verification Engine]
        Router --> PDFGen[ReportLab PDF / CSV / JSON Export Engine]
        Router --> CCPA[CCPA 2023 Compliance Library]
    end

    subgraph Storage Layer
        FastApi --> DB[(SQLite / PostgreSQL DB)]
    end
```

## 2. Core Subsystems

### Multilingual Classifier (`app/detection/classifier.py`)
- Detects dark patterns in **English**, **Hindi (हिंदी)**, and **Tamil (தமிழ்)**.
- Maps text snippets to 13 official CCPA 2023 categories (False Urgency, Drip Pricing, Confirm Shaming, Basket Sneaking, Forced Action, Subscription Trap, Interface Interference, Bait & Switch, Disguised Ads, Nagging, Trick Wording, SaaS Billing, Deceptive Counting).

### Learned Combined-Risk Model (`app/risk_scoring/combined_risk_model.py`)
- Computes calibrated 0–100 page risk score: `Score = Min(100, Sum(Severity Weights) × Co-occurrence Multiplier)`.
- Risk Bands:
  - Low Risk: 0–25
  - Moderate Risk: 26–50
  - High Risk: 51–75
  - Critical Risk: 76–100

### Automated Remediation & Verification (`app/remediation/engine.py`)
- Re-analyzes proposed text through the detector to verify score reduction before approving changes.

### Security (`app/core/ssrf.py`)
- SSRF Guard blocks RFC 1918 private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), loopbacks (`127.0.0.1`), link-local (`169.254.0.0/16`), AWS metadata endpoints (`169.254.169.254`), and unsafe protocols.
