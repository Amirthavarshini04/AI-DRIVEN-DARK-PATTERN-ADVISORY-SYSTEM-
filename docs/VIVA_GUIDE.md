# 🎓 Viva Preparation & Project Module Explanation Guide

**Project Title:** AI-Driven Dark Pattern Detection and Legal Compliance Advisory System for Indian E-Commerce Platforms  
**Academic Target:** 7th Semester Major Engineering Project Demonstration & Oral Evaluation (Viva Voce)

---

## 1. Quick Summary (30-Second Elevator Pitch)
> *"Our project is an AI-assisted compliance decision-support system designed to identify deceptive user-interface patterns (Dark Patterns) on Indian e-commerce platforms. Built under the Central Consumer Protection Authority (CCPA) Guidelines 2023, it analyzes webpage text in English, Hindi, and Tamil, computes a calibrated 0-100 combined page risk score using machine learning feature aggregation, suggests compliant text alternatives, and verifies risk score drops before-and-after rewriting."*

---

## 2. Technical Stack Breakdown for Examiners
- **Frontend**: React, TypeScript, Tailwind CSS, Recharts (Responsive Enterprise SaaS UI).
- **Backend**: Python 3.10+, FastAPI (Asynchronous REST API, Pydantic Schema Validation).
- **Database**: SQLite / PostgreSQL with SQLAlchemy ORM (Persists scans, findings, CCPA guidelines, remediations, feedback).
- **AI/ML Engine**: Scikit-Learn TF-IDF + Multilingual Rule Pipeline (IndicBERT / mBERT compatible) for English, Hindi (हिंदी), and Tamil (தமிழ்).
- **Security**: Custom SSRF Protection Module blocking private IPs (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`, `169.254.169.254`).
- **Browser Extension**: Chrome Manifest V3 extension with DOM element overlay highlighting.

---

## 3. Likely Examiner Questions & Recommended Answers

### Q1: What are Dark Patterns and what is the relevant Indian law?
**Answer:** Dark patterns are deceptive UI/UX design techniques intended to trick users into making decisions they might not otherwise make (e.g. buying unwanted insurance or rushing under false countdown timers). In India, the **Central Consumer Protection Authority (CCPA)** issued the *Guidelines for Prevention and Regulation of Dark Patterns, 2023* under Section 18 of the Consumer Protection Act, 2019, recognizing 13 specific dark pattern categories.

### Q2: How does your multilingual model handle Indian languages like Tamil and Hindi?
**Answer:** Our detection engine uses Unicode block range identification combined with a TF-IDF vectorizer and regex pattern matchers tailored for Devanagari (Hindi) and Tamil scripts. It identifies phrases like `"மின்னல் விற்பனை!"` (Flash Sale) or `"केवल 3 स्टॉक में बचे हैं"` (Only 3 left) and maps them to False Urgency under CCPA Clause 3(a).

### Q3: How is the 0-100 Page Risk Score calculated? Is it a random heuristic?
**Answer:** No. We implemented a **Learned Combined-Risk Model** that aggregates severity weights (Critical: 35, High: 25, Medium: 15, Low: 8) and evaluates **co-occurrence multipliers** (e.g. 1.35x when False Urgency and Drip Pricing appear together on the same checkout page). The mathematical formula is:
$$S = \min(100, \sum (Severity\_i) \times Multiplier_{CoOccurrence})$$

### Q4: How does your system verify that a proposed text fix is actually compliant?
**Answer:** We run a **Closed-Loop Verification Workflow**:
1. Original manipulative text is flagged with an initial risk score.
2. The remediation engine generates a compliant alternative text.
3. The detector re-analyzes the revised text snippet.
4. The risk score is recalculated and compared.
5. If the revised score is lower (or 0), it is marked as **Verified Risk Reduction**.

### Q5: Is this system claiming to give legally binding judgments?
**Answer:** No. We explicitly state throughout the UI and PDF reports that this system is an **academic decision-support tool**, not a formal legal certification service.
