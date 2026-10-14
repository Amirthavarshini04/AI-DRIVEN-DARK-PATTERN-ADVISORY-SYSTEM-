# Chrome Extension Installation & Testing Guide

## Manifest V3 Setup Steps

1. Open **Google Chrome** or any Chromium browser (Brave, Edge).
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode** using the toggle switch in the top-right corner.
4. Click **Load unpacked**.
5. Select the project directory:
   `C:\Users\Amirtha S\.gemini\antigravity\scratch\dark_pattern_system\browser-extension\`
6. The **AI Dark Pattern & Compliance Advisor** icon will appear in your browser toolbar.

## How to Test Live DOM Highlighting
1. Ensure the FastAPI backend server is running on `http://127.0.0.1:8000`.
2. Open any e-commerce page (or a local test HTML file containing dark pattern text like `"Hurry! Only 2 left in stock!"`).
3. Click the Extension Icon in the browser toolbar.
4. Click **Scan Active Page**.
5. The extension will highlight deceptive elements with red/orange outline boxes and hover tooltips on the live page!
