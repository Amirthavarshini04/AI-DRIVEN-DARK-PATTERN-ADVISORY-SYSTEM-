# 🛡️ AI-Driven Dark Pattern Detection & Legal Compliance Advisory System for Indian E-Commerce Platforms

> **7th Semester Major Engineering Project**  
> An end-to-end AI/ML compliance advisory platform designed under the **Central Consumer Protection Authority (CCPA) Guidelines for Prevention and Regulation of Dark Patterns, 2023**.

---

## 🌟 Key Features

1. **Multilingual Dark Pattern Classifier**: Supports **English**, **Hindi (हिंदी)**, and **Tamil (தமிழ்)** across all 13 official CCPA categories (False Urgency, Drip Pricing, Confirm Shaming, Basket Sneaking, Forced Action, Subscription Trap, etc.).
2. **Learned Combined-Risk Score (0–100)**: Non-linear scoring engine incorporating severity weights and pattern co-occurrence multipliers.
3. **Automated Remediation & Verification**: Generates compliant alternative wording and verifies before-and-after risk drops.
4. **CCPA 2023 Guidelines Library**: Searchable legal reference database mapped to exact CCPA clauses.
5. **Report Exports**: Download verifiable audit reports in **PDF**, **CSV**, and **JSON** formats with complete Unicode support.
6. **Chrome Extension (Manifest V3)**: Inspect active tab DOM elements and highlight deceptive patterns on live e-commerce websites.

---

## 🚀 Quick Start Instructions

### 1. Start FastAPI Backend Server
```bash
cd backend
pip install -r requirements.txt
python main.py
```
*The backend API will run on `http://127.0.0.1:8000` and automatically seed the initial CCPA guidelines and sample scan records.*

### 2. Start Next.js / React Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```
*Open `http://localhost:5173` in your browser to access the SaaS Compliance Dashboard.*

### 3. Load Chrome Browser Extension
1. Open Chrome and navigate to `chrome://extensions/`.
2. Turn on **Developer mode**.
3. Click **Load unpacked** and select the `browser-extension/` directory.

---

## 🧪 Running Unit Tests & Benchmarks

```bash
# Run backend pytest suite
cd backend
pytest

# Run ML Benchmark Evaluation Suite
python ml/evaluation/evaluate_model.py
```

---

## 📁 Project Structure

```text
dark_pattern_system/
├── backend/            # FastAPI Python backend, ML engine, DB models, reports
├── frontend/           # Vite + React + TypeScript + Tailwind SaaS dashboard
├── browser-extension/  # Chrome Manifest V3 extension (DOM highlighting + popup)
├── dataset/            # Labelled samples (EN, HI, TA), schemas, annotation guide
├── ml/                 # Model training, evaluation scripts, checkpoints
├── docs/               # Architecture, API docs, Extension setup, Viva guide
├── Dockerfile
└── docker-compose.yml
```
