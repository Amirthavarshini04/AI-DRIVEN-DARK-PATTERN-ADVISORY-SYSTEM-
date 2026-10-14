document.addEventListener("DOMContentLoaded", () => {
  const scanBtn = document.getElementById("scanBtn");
  const clearBtn = document.getElementById("clearBtn");
  const statusBox = document.getElementById("statusBox");
  const resultsCard = document.getElementById("resultsCard");
  const scoreVal = document.getElementById("scoreVal");
  const riskBadge = document.getElementById("riskBadge");
  const countVal = document.getElementById("countVal");
  const findingsContainer = document.getElementById("findingsContainer");

  scanBtn.addEventListener("click", () => {
    statusBox.classList.remove("hidden");
    resultsCard.classList.add("hidden");

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs[0]) return;

      chrome.tabs.sendMessage(tabs[0].id, { action: "SCAN_DOM" }, (response) => {
        statusBox.classList.add("hidden");

        if (chrome.runtime.lastError || !response || response.status === "error") {
          alert("Error: Ensure backend server is running on http://127.0.0.1:8000");
          return;
        }

        const data = response.data;
        resultsCard.classList.remove("hidden");
        scoreVal.innerText = `${data.risk_score} / 100`;
        riskBadge.innerText = data.risk_category;
        countVal.innerText = data.findings.length;

        findingsContainer.innerHTML = "";
        if (data.findings.length === 0) {
          findingsContainer.innerHTML = "<div style='font-size:11px; color:#16a34a;'>✓ No dark patterns detected on page.</div>";
        } else {
          data.findings.forEach(f => {
            const div = document.createElement("div");
            div.className = "finding-item";
            div.innerHTML = `
              <div class="finding-cat">${f.category} (${f.ccpa_clause})</div>
              <div class="finding-text">"${f.text_snippet}"</div>
            `;
            findingsContainer.appendChild(div);
          });
        }
      });
    });
  });

  clearBtn.addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, { action: "CLEAR_HIGHLIGHTS" });
        resultsCard.classList.add("hidden");
      }
    });
  });
});
