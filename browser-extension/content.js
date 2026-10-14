// Content script for inspecting DOM text and highlighting dark patterns
console.log("AI Dark Pattern Content Script Loaded.");

let activeHighlights = [];

function clearHighlights() {
  activeHighlights.forEach(el => {
    el.classList.remove("dp-highlight-high", "dp-highlight-medium");
    const tt = el.querySelector(".dp-tooltip-box");
    if (tt) tt.remove();
  });
  activeHighlights = [];
}

function highlightPageFindings(findings) {
  clearHighlights();
  
  if (!findings || findings.length === 0) return;

  const elements = document.querySelectorAll("p, span, div, button, a, h1, h2, h3");
  
  findings.forEach(finding => {
    const snippet = finding.text_snippet.toLowerCase();
    
    elements.forEach(el => {
      if (el.children.length === 0 && el.textContent.trim().length > 3) {
        if (el.textContent.toLowerCase().includes(snippet) || snippet.includes(el.textContent.toLowerCase().trim())) {
          const cls = finding.severity === "High" || finding.severity === "Critical" ? "dp-highlight-high" : "dp-highlight-medium";
          el.classList.add(cls);
          
          // Add hover tooltip badge
          const tooltip = document.createElement("div");
          tooltip.className = "dp-tooltip-box";
          tooltip.innerText = `⚠️ ${finding.category} (${finding.ccpa_clause})`;
          el.style.position = "relative";
          el.appendChild(tooltip);
          
          activeHighlights.push(el);
        }
      }
    });
  });
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "SCAN_DOM") {
    const pageText = document.body.innerText;
    
    fetch("http://127.0.0.1:8000/api/v1/scans/text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: pageText, language: "auto" })
    })
    .then(res => res.json())
    .then(data => {
      highlightPageFindings(data.findings);
      sendResponse({ status: "success", data: data });
    })
    .catch(err => {
      sendResponse({ status: "error", error: err.message });
    });
    
    return true; // Keep message channel open for async response
  } else if (request.action === "CLEAR_HIGHLIGHTS") {
    clearHighlights();
    sendResponse({ status: "cleared" });
  }
});
