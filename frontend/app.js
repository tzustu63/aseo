// SEO Analyzer Frontend Logic

let currentResults = null;

// API 基礎 URL（Railway 部署後會自動使用正確的網域）
const API_BASE = window.location.origin;

/**
 * 分析網址
 */
async function analyzeURL() {
    const urlInput = document.getElementById('url-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const results = document.getElementById('results');
    
    let url = urlInput.value.trim();
    
    // 驗證網址
    if (!url) {
        showError('請輸入網址');
        return;
    }
    
    // 自動加上 https://
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
        urlInput.value = url;
    }
    
    // 顯示載入狀態
    loading.style.display = 'block';
    error.style.display = 'none';
    results.style.display = 'none';
    analyzeBtn.disabled = true;
    
    try {
        // 發送分析請求
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }
        
        // 儲存結果
        currentResults = data;
        
        // 顯示結果
        displayResults(data);
        
    } catch (err) {
        showError(err.message || '分析失敗，請稍後再試');
    } finally {
        loading.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

/**
 * 顯示錯誤訊息
 */
function showError(message) {
    const error = document.getElementById('error');
    error.textContent = message;
    error.style.display = 'block';
}

/**
 * 顯示分析結果
 */
function displayResults(data) {
    const results = document.getElementById('results');
    
    // 顯示總分
    document.getElementById('total-score').textContent = data.total_score;
    document.getElementById('grade-stars').textContent = data.grade.stars;
    document.getElementById('grade-level').textContent = data.grade.level;
    document.getElementById('grade-description').textContent = data.grade.description;
    
    // 顯示問題摘要
    document.getElementById('critical-count').textContent = data.summary.critical;
    document.getElementById('high-count').textContent = data.summary.high;
    document.getElementById('medium-count').textContent = data.summary.medium;
    document.getElementById('low-count').textContent = data.summary.low;
    
    // 顯示各項目分數
    displayCategoryScores(data.category_scores);
    
    // 顯示問題列表
    displayIssues(data.results);
    
    // 顯示結果區
    results.style.display = 'block';
    
    // 滾動到結果區
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * 顯示各項目分數
 */
function displayCategoryScores(categoryScores) {
    const container = document.getElementById('category-scores-list');
    container.innerHTML = '';
    
    const categoryNames = {
        'title': 'Title 標籤',
        'meta_tags': 'Meta 標籤',
        'headings': '標題結構',
        'keywords': '關鍵字',
        'images': '圖片優化',
        'structure': 'HTML 結構',
        'performance': '效能',
        'mobile': '行動裝置'
    };
    
    for (const [category, score] of Object.entries(categoryScores)) {
        const item = document.createElement('div');
        item.className = 'category-score-item';
        item.innerHTML = `
            <h4>${categoryNames[category] || category}</h4>
            <div class="category-score-value">${score}</div>
        `;
        container.appendChild(item);
    }
}

/**
 * 顯示問題列表
 */
function displayIssues(results) {
    const container = document.getElementById('issues-list');
    container.innerHTML = '';
    
    // 收集所有問題
    const allIssues = [];
    results.forEach(result => {
        result.issues.forEach(issue => {
            allIssues.push({
                ...issue,
                category: result.category
            });
        });
    });
    
    // 按優先順序排序
    allIssues.sort((a, b) => a.priority - b.priority);
    
    if (allIssues.length === 0) {
        container.innerHTML = `
            <div class="no-issues">
                <h3>🎉 太棒了！</h3>
                <p>沒有發現重大的 SEO 問題，您的網頁 SEO 狀況很好！</p>
            </div>
        `;
        return;
    }
    
    // 顯示每個問題
    allIssues.forEach((issue, index) => {
        const card = document.createElement('div');
        card.className = `issue-card ${issue.severity}`;
        
        let html = `
            <div class="issue-header">
                <div class="issue-title">${index + 1}. ${issue.message}</div>
                <span class="severity-badge ${issue.severity}">${getSeverityText(issue.severity)}</span>
            </div>
            <div class="issue-suggestion">
                💡 建議：${issue.suggestion}
            </div>
        `;
        
        // 加入程式碼範例
        if (issue.code_example) {
            html += `<div class="code-example">${escapeHtml(issue.code_example)}</div>`;
        }
        
        // 加入影響和難度
        if (issue.impact || issue.difficulty) {
            html += '<div class="issue-meta">';
            if (issue.impact) {
                html += `<span>📊 影響：${issue.impact}</span>`;
            }
            if (issue.difficulty) {
                html += `<span>⚙️ 難度：${getDifficultyText(issue.difficulty)}</span>`;
            }
            html += '</div>';
        }
        
        card.innerHTML = html;
        container.appendChild(card);
    });
}

/**
 * 取得嚴重性文字
 */
function getSeverityText(severity) {
    const texts = {
        'critical': '嚴重',
        'high': '重要',
        'medium': '中等',
        'low': '輕微'
    };
    return texts[severity] || severity;
}

/**
 * 取得難度文字
 */
function getDifficultyText(difficulty) {
    const texts = {
        'easy': '簡單',
        'medium': '中等',
        'hard': '困難'
    };
    return texts[difficulty] || difficulty;
}

/**
 * 跳脫 HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 匯出結果
 */
function exportResults() {
    if (!currentResults) {
        alert('沒有分析結果可匯出');
        return;
    }
    
    const dataStr = JSON.stringify(currentResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `seo-analysis-${Date.now()}.json`;
    a.click();
    
    URL.revokeObjectURL(url);
}

// Enter 鍵觸發分析
document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('url-input');
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeURL();
        }
    });
});

