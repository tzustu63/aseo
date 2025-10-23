/**
 * SEO Analyzer Frontend JavaScript
 *
 * 純 SEO 分析功能，已移除 WordPress 和 OpenAI 相關功能
 */

// API 基礎 URL
const API_BASE = "";

// 全域變數
let currentAnalysisData = null;
let openaiApiKey = localStorage.getItem("openai_api_key") || "";

/**
 * 分析 URL
 */
async function analyzeURL() {
  const urlInput = document.getElementById("url-input");
  const url = urlInput.value.trim();

  if (!url) {
    showError("請輸入要分析的網址");
    return;
  }

  // 顯示載入狀態
  showLoading();
  hideError();
  hideResults();

  // 模擬進度更新（如果有 AI）
  let progressInterval;
  if (openaiApiKey) {
    const categories = [
      "標題標籤",
      "Meta 標籤",
      "標題結構",
      "圖片優化",
      "關鍵字",
      "HTML 結構",
      "效能指標",
      "行動裝置",
      "Core Web Vitals",
      "結構化資料",
      "連結分析",
      "可爬性",
    ];
    let currentStep = 0;

    progressInterval = setInterval(() => {
      if (currentStep < 12) {
        const status = currentStep % 2 === 0 ? "analyzing" : "ai";
        updateProgress(currentStep + 1, 12, categories[currentStep], status);
        currentStep++;
      }
    }, 2000); // 每 2 秒更新一次（預估每項分析+AI約2-4秒）
  }

  try {
    // 準備請求數據
    const requestData = {
      url: url,
    };

    // 如果有 OpenAI API Key，加入請求
    if (openaiApiKey) {
      requestData.openai_api_key = openaiApiKey;
      requestData.use_ai_enhancement = true;
    }

    const response = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    const data = await response.json();

    if (data.success) {
      currentAnalysisData = data;

      // 顯示完成進度
      if (openaiApiKey) {
        updateProgress(12, 12, "分析完成", "complete");
        setTimeout(() => {
          displayResults(data);
        }, 500);
      } else {
        displayResults(data);
      }
    } else {
      showError(data.error || "分析失敗");
    }
  } catch (error) {
    console.error("分析錯誤:", error);
    showError("網路錯誤，請檢查連線後重試");
  } finally {
    if (progressInterval) {
      clearInterval(progressInterval);
    }
    setTimeout(hideLoading, openaiApiKey ? 1000 : 0);
  }
}

/**
 * 顯示載入狀態（帶進度）
 */
function showLoading() {
  const loadingDiv = document.getElementById("loading");
  loadingDiv.style.display = "block";
  document.getElementById("analyze-btn").disabled = true;

  // 如果有 AI 增強，顯示詳細進度
  if (openaiApiKey) {
    loadingDiv.innerHTML = `
      <div class="spinner"></div>
      <p id="loading-text">正在分析中，請稍候...</p>
      <div class="progress-container">
        <div class="progress-bar" id="progress-bar"></div>
      </div>
      <p id="progress-text" class="progress-detail">準備開始分析...</p>
    `;
  } else {
    loadingDiv.innerHTML = `
      <div class="spinner"></div>
      <p>正在分析中，請稍候...</p>
    `;
  }
}

/**
 * 更新分析進度
 */
function updateProgress(current, total, categoryName, status) {
  const progressBar = document.getElementById("progress-bar");
  const progressText = document.getElementById("progress-text");
  const loadingText = document.getElementById("loading-text");

  if (progressBar) {
    const percentage = (current / total) * 100;
    progressBar.style.width = `${percentage}%`;
  }

  if (loadingText) {
    loadingText.textContent = `正在分析 ${current}/${total} 項...`;
  }

  if (progressText) {
    const statusIcon =
      status === "analyzing" ? "🔍" : status === "ai" ? "🤖" : "✓";
    progressText.textContent = `${statusIcon} ${categoryName}`;
  }
}

/**
 * 隱藏載入狀態
 */
function hideLoading() {
  document.getElementById("loading").style.display = "none";
  document.getElementById("analyze-btn").disabled = false;
}

/**
 * 顯示錯誤訊息
 */
function showError(message) {
  const errorDiv = document.getElementById("error");
  const errorMessage = document.getElementById("error-message");

  errorMessage.textContent = message;
  errorDiv.style.display = "block";
}

/**
 * 隱藏錯誤訊息
 */
function hideError() {
  document.getElementById("error").style.display = "none";
}

/**
 * 顯示分析結果
 */
function displayResults(data) {
  const resultsDiv = document.getElementById("results");
  const resultsContent = document.getElementById("results-content");
  const totalScore = document.getElementById("total-score");

  // 更新總分
  totalScore.textContent = data.total_score;
  totalScore.className = `score-value ${getScoreClass(data.total_score)}`;

  // 顯示 AI 增強狀態
  let html = "";

  if (data.ai_enhanced) {
    html += `
      <div class="ai-enhanced-badge">
        <span class="ai-badge-icon">🤖</span>
        <span class="ai-badge-text">已使用 AI 增強分析</span>
      </div>
    `;
  }

  data.results.forEach((category) => {
    html += `
      <div class="category-result">
        <div class="category-header">
          <h3>${getCategoryTitle(category.category)}</h3>
          <div class="category-score">
            <span class="score-label">分數</span>
            <span class="score-value ${getScoreClass(category.score)}">${
      category.score
    }</span>
          </div>
        </div>
        
        <div class="issues-list">
           ${category.issues
             .map(
               (issue) => `
             <div class="issue-item ${issue.severity}">
               <div class="issue-header">
                 <span class="issue-icon">${getIssueIcon(issue.severity)}</span>
                 <span class="issue-type">${escapeHtml(issue.type)}</span>
                 <span class="issue-severity">${getSeverityText(
                   issue.severity
                 )}</span>
               </div>
               <div class="issue-content">
                 <p class="issue-message">${escapeHtml(issue.message)}</p>
                 ${
                   issue.suggestion
                     ? `<p class="issue-suggestion"><strong>建議：</strong>${escapeHtml(
                         issue.suggestion
                       )}</p>`
                     : ""
                 }
                 ${
                   issue.ai_suggestion
                     ? `<div class="ai-suggestion">
                          <div class="ai-suggestion-header">
                            <span class="ai-icon-small">🤖</span>
                            <strong>AI 專家建議</strong>
                          </div>
                          <div class="ai-suggestion-content">${escapeHtml(
                            issue.ai_suggestion
                          ).replace(/\n/g, "<br>")}</div>
                        </div>`
                     : ""
                 }
                 ${
                   issue.current_value
                     ? `<p class="issue-current"><strong>目前：</strong>${escapeHtml(
                         issue.current_value
                       )}</p>`
                     : ""
                 }
               </div>
             </div>
           `
             )
             .join("")}
        </div>
      </div>
    `;
  });

  resultsContent.innerHTML = html;
  resultsDiv.style.display = "block";
}

/**
 * 隱藏結果
 */
function hideResults() {
  document.getElementById("results").style.display = "none";
}

/**
 * 轉義 HTML 特殊字元
 */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/**
 * 根據分數獲取 CSS 類別
 */
function getScoreClass(score) {
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "fair";
  return "poor";
}

/**
 * 獲取類別標題
 */
function getCategoryTitle(category) {
  const titles = {
    title: "標題標籤",
    meta: "Meta 描述",
    headings: "標題結構",
    images: "圖片優化",
    keywords: "關鍵字",
    structure: "HTML 結構",
    performance: "效能指標",
    mobile: "行動裝置友善性",
    core_web_vitals: "核心網頁指標 (Core Web Vitals)",
    structured_data: "結構化資料",
    links: "連結分析",
    crawlability: "可爬性 & Sitemap",
  };
  return titles[category] || category;
}

/**
 * 獲取問題圖示
 */
function getIssueIcon(severity) {
  const icons = {
    high: "🔴",
    medium: "🟡",
    low: "🟢",
    error: "❌",
  };
  return icons[severity] || "ℹ️";
}

/**
 * 獲取嚴重程度文字
 */
function getSeverityText(severity) {
  const texts = {
    high: "高",
    medium: "中",
    low: "低",
    error: "錯誤",
  };
  return texts[severity] || severity;
}

/**
 * 切換 AI 設定區域
 */
function toggleAISection() {
  const config = document.getElementById("ai-config");
  const icon = document.getElementById("ai-toggle-icon");

  if (config.style.display === "none") {
    config.style.display = "block";
    icon.classList.add("open");
  } else {
    config.style.display = "none";
    icon.classList.remove("open");
  }
}

/**
 * 測試 OpenAI API Key
 */
async function testOpenAI() {
  const apiKey = document.getElementById("openai-api-key").value.trim();
  const statusDiv = document.getElementById("ai-status");

  if (!apiKey) {
    showStatus(statusDiv, "請輸入 API Key", "error");
    return;
  }

  if (!apiKey.startsWith("sk-")) {
    showStatus(statusDiv, "API Key 格式錯誤（應以 sk- 開頭）", "error");
    return;
  }

  showStatus(statusDiv, "正在測試 API Key...", "info");

  try {
    const response = await fetch(`${API_BASE}/api/test-openai`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ api_key: apiKey }),
    });

    const data = await response.json();

    if (data.success) {
      showStatus(
        statusDiv,
        "✅ API Key 有效！可以使用 AI 增強分析功能",
        "success"
      );
    } else {
      showStatus(statusDiv, `❌ ${data.message}`, "error");
    }
  } catch (error) {
    showStatus(statusDiv, `測試失敗：${error.message}`, "error");
  }
}

/**
 * 儲存 OpenAI 設定
 */
function saveOpenAIConfig() {
  const apiKey = document.getElementById("openai-api-key").value.trim();
  const statusDiv = document.getElementById("ai-status");

  if (!apiKey) {
    showStatus(statusDiv, "請輸入 API Key", "error");
    return;
  }

  localStorage.setItem("openai_api_key", apiKey);
  openaiApiKey = apiKey;

  showStatus(statusDiv, "✅ 設定已儲存！下次分析將使用 AI 增強功能", "success");
}

/**
 * 顯示狀態訊息
 */
function showStatus(element, message, type) {
  element.textContent = message;
  element.className = `status-message ${type}`;
}

/**
 * 鍵盤事件處理
 */
document.addEventListener("DOMContentLoaded", function () {
  const urlInput = document.getElementById("url-input");
  const analyzeBtn = document.getElementById("analyze-btn");
  const apiKeyInput = document.getElementById("openai-api-key");

  // Enter 鍵觸發分析
  urlInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      analyzeURL();
    }
  });

  // 輸入時清除錯誤狀態
  urlInput.addEventListener("input", function () {
    hideError();
  });

  // 載入已儲存的 API Key
  if (openaiApiKey) {
    apiKeyInput.value = openaiApiKey;
  }
});

/**
 * 複製結果到剪貼簿
 */
function copyResults() {
  if (!currentAnalysisData) return;

  let text = `SEO 分析結果 - ${currentAnalysisData.url}\n`;
  text += `總分：${currentAnalysisData.total_score}\n\n`;

  currentAnalysisData.results.forEach((category) => {
    text += `${getCategoryTitle(category.category)}：${category.score}分\n`;
    category.issues.forEach((issue) => {
      text += `- ${issue.message}\n`;
      if (issue.suggestion) {
        text += `  建議：${issue.suggestion}\n`;
      }
    });
    text += "\n";
  });

  navigator.clipboard
    .writeText(text)
    .then(() => {
      alert("結果已複製到剪貼簿");
    })
    .catch((err) => {
      console.error("複製失敗:", err);
      alert("複製失敗，請手動複製");
    });
}
