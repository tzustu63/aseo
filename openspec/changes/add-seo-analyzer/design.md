# SEO 網頁分析工具 - 設計文件

## 背景說明

這是一個個人使用的 SEO 分析工具，目的是快速診斷任意網頁的 SEO 問題。使用者只需要輸入網址，系統就會自動分析並列出所有可以優化的地方，並提供具體的修改建議。

## 目標 / 非目標

### 目標

- 提供簡單的網址輸入介面
- 自動抓取網頁內容並分析
- 檢查多個 SEO 面向（HTML、Meta、關鍵字、圖片等）
- 顯示清楚的問題列表和優化建議
- 計算 SEO 健康度分數
- 個人使用，不需要登入或帳號系統

### 非目標

- 多網址批量分析（首版不需要）
- 歷史記錄和追蹤（首版不需要）
- 競爭對手比較（未來功能）
- 付費功能或限制（完全免費個人工具）
- 即時監控（不需要）

## 技術架構選擇

### 方案一：純前端（建議用於 MVP）

**優點**：

- 最簡單，不需要後端伺服器
- 部署容易（GitHub Pages 即可）
- 開發快速

**缺點**：

- CORS 限制（無法直接抓取其他網站）
- 需要使用 CORS proxy 或瀏覽器擴充功能

**技術棧**：

```
- HTML + CSS + JavaScript
- BeautifulSoup4 無法使用（純前端）
- 改用 DOMParser 或 cheerio.js
```

### 方案二：前後端分離（建議）

**優點**：

- 沒有 CORS 限制
- 可以使用 Python BeautifulSoup4
- 更強大的分析能力
- 易於擴充功能

**技術棧**：

```
後端：
- Python + Flask/FastAPI
- BeautifulSoup4（HTML 解析）
- requests（抓取網頁）
- Pillow（圖片分析，可選）

前端：
- 簡單的 HTML + JavaScript
- 或使用 React（如果需要）
```

**決定**：採用**方案二**（前後端分離）

## 架構設計

### 資料流程

```
使用者輸入網址
    ↓
前端驗證 URL 格式
    ↓
發送 POST /api/analyze
    ↓
後端抓取網頁 HTML
    ↓
執行多個分析器
    ↓
產生 SEO 問題清單
    ↓
產生優化建議
    ↓
計算 SEO 分數
    ↓
回傳 JSON 結果
    ↓
前端顯示分析報告
```

### 分析器架構

採用**插件式分析器**設計：

```python
class BaseAnalyzer(ABC):
    """基礎分析器"""
    @abstractmethod
    def analyze(self, html: str, url: str) -> AnalysisResult:
        pass

class TitleAnalyzer(BaseAnalyzer):
    """標題分析器"""
    def analyze(self, html, url):
        # 檢查 title 標籤
        # 檢查長度、關鍵字等
        return AnalysisResult(...)

class MetaAnalyzer(BaseAnalyzer):
    """Meta 標籤分析器"""
    def analyze(self, html, url):
        # 檢查 meta description
        # 檢查 og tags
        return AnalysisResult(...)

# 其他分析器...
```

### API 設計

**端點**：`POST /api/analyze`

**請求**：

```json
{
  "url": "https://example.com"
}
```

**回應**：

```json
{
  "url": "https://example.com",
  "score": 75,
  "grade": "良好",
  "analysis_time": "2.3s",
  "issues": [
    {
      "category": "meta_tags",
      "severity": "high",
      "title": "缺少 meta description",
      "description": "meta description 對 SEO 很重要...",
      "suggestion": "在 <head> 中加入：\n<meta name=\"description\" content=\"您的描述...\">",
      "priority": 1
    }
  ],
  "summary": {
    "critical": 2,
    "high": 5,
    "medium": 8,
    "low": 3
  }
}
```

### 評分系統

採用**加權評分制**（0-100 分）：

```python
weights = {
    'title': 15,          # 標題標籤 15%
    'meta_tags': 15,      # Meta 標籤 15%
    'headings': 15,       # 標題結構 15%
    'keywords': 10,       # 關鍵字 10%
    'images': 10,         # 圖片優化 10%
    'structure': 15,      # HTML 結構 15%
    'performance': 10,    # 效能 10%
    'mobile': 10,         # 行動裝置 10%
}

total_score = sum(category_score * weight for category, weight in weights.items())
```

**分級**：

- 90-100 分：優秀 ⭐⭐⭐⭐⭐
- 70-89 分：良好 ⭐⭐⭐⭐
- 50-69 分：普通 ⭐⭐⭐
- 30-49 分：待改善 ⭐⭐
- 0-29 分：需大幅優化 ⭐

## 前端介面設計

### 簡單版 HTML 結構

```html
<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8" />
    <title>SEO 網頁分析工具</title>
  </head>
  <body>
    <div class="container">
      <h1>SEO 網頁分析工具</h1>

      <!-- 輸入區 -->
      <div class="input-section">
        <input
          type="url"
          id="url-input"
          placeholder="輸入網址（例如：https://example.com）"
        />
        <button id="analyze-btn">開始分析</button>
      </div>

      <!-- 載入中 -->
      <div id="loading" style="display:none;">分析中，請稍候...</div>

      <!-- 結果區 -->
      <div id="results" style="display:none;">
        <!-- SEO 分數 -->
        <div class="score-card">
          <h2>SEO 分數：<span id="score">--</span>/100</h2>
          <div id="grade">--</div>
        </div>

        <!-- 問題摘要 -->
        <div class="summary">
          <span class="critical">嚴重: <span id="critical-count">0</span></span>
          <span class="high">重要: <span id="high-count">0</span></span>
          <span class="medium">中等: <span id="medium-count">0</span></span>
          <span class="low">輕微: <span id="low-count">0</span></span>
        </div>

        <!-- 問題列表 -->
        <div id="issues-list">
          <!-- 動態產生問題卡片 -->
        </div>
      </div>

      <!-- 錯誤訊息 -->
      <div id="error" style="display:none;"></div>
    </div>
  </body>
</html>
```

## 後端實作選擇

### 選項一：Flask（簡單）

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # 允許前端跨域請求

@app.route('/api/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')

    # 抓取網頁
    response = requests.get(url, timeout=10)
    html = response.text

    # 執行分析
    results = run_all_analyzers(html, url)

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)
```

### 選項二：FastAPI（更現代）

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

class AnalyzeRequest(BaseModel):
    url: str

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    # 分析邏輯
    results = await run_analysis(request.url)
    return results
```

**決定**：使用 **Flask**（更簡單，適合個人工具）

## 風險與緩解

### 風險 1：CORS 限制

- **風險**：純前端無法直接抓取其他網站
- **緩解**：採用後端架構，由後端抓取網頁

### 風險 2：網頁抓取失敗

- **風險**：目標網站可能阻擋、超時、需要 JavaScript 渲染
- **緩解**：
  - 設定合理超時（10 秒）
  - 友善的錯誤訊息
  - 首版只支援靜態 HTML（未來可加 Selenium）

### 風險 3：分析準確度

- **風險**：SEO 規則複雜，可能有遺漏
- **緩解**：
  - 基於 Google SEO 官方指南
  - 先做最重要的檢查項目
  - 持續更新規則

### 風險 4：效能問題

- **風險**：大型網頁分析耗時
- **緩解**：
  - 限制下載大小（5MB）
  - 非同步處理
  - 顯示載入進度

## 實施計畫

### 階段 1：基本 MVP

1. 網址輸入介面
2. 簡單的後端（Flask）
3. 3-4 個核心分析器（title、meta、headings、images）
4. 基本的結果顯示

**預估時間**：2-3 天

### 階段 2：完整功能

1. 加入所有分析器
2. 評分系統
3. 優化建議產生
4. 美化介面

**預估時間**：3-5 天

### 階段 3：優化體驗

1. 結果匯出（JSON）
2. 美觀的報告排版
3. 響應式設計
4. 效能優化

**預估時間**：2-3 天

## 技術決策摘要

| 項目      | 選擇              | 理由                      |
| --------- | ----------------- | ------------------------- |
| 架構      | 前後端分離        | 避免 CORS，功能更強       |
| 後端      | Flask             | 簡單易用，適合個人工具    |
| 前端      | HTML + JavaScript | 簡單快速，不需要框架      |
| HTML 解析 | BeautifulSoup4    | Python 標準工具，成熟穩定 |
| 評分系統  | 加權評分          | 清楚反映各項目重要性      |
| 部署      | Railway           | 免費、簡單、支援 Python   |

## 檔案結構

```
findseoproblem/
├── backend/
│   ├── app.py                 # Flask 主程式
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── base.py           # 基礎分析器類別
│   │   ├── title.py          # 標題分析器
│   │   ├── meta.py           # Meta 標籤分析器
│   │   ├── headings.py       # 標題結構分析器
│   │   ├── keywords.py       # 關鍵字分析器
│   │   ├── images.py         # 圖片分析器
│   │   ├── performance.py    # 效能分析器
│   │   └── mobile.py         # 行動裝置分析器
│   ├── scorer.py             # 評分系統
│   ├── recommender.py        # 建議產生器
│   └── requirements.txt
├── frontend/
│   ├── index.html            # 主頁面
│   ├── style.css             # 樣式
│   └── app.js                # 前端邏輯
└── README.md                 # 使用說明
```

## 開發優先順序

### P0（必須）

- ✅ 網址輸入和驗證
- ✅ 網頁抓取
- ✅ Title 和 Meta Description 分析
- ✅ 標題結構（H1-H6）分析
- ✅ 圖片 alt 檢查
- ✅ 基本結果顯示

### P1（重要）

- ⭐ 關鍵字分析
- ⭐ SEO 評分系統
- ⭐ 優化建議產生
- ⭐ 問題分類和優先級

### P2（加分）

- 💡 Open Graph 標籤檢查
- 💡 效能分析
- 💡 行動裝置友善度
- 💡 結果匯出

## 範例：分析器實作

```python
# analyzers/title.py
class TitleAnalyzer(BaseAnalyzer):
    """標題標籤分析器"""

    def analyze(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')

        issues = []
        score = 100

        # 檢查是否存在
        if not title_tag:
            issues.append({
                'severity': 'critical',
                'message': '缺少 <title> 標籤',
                'suggestion': '在 <head> 中加入 <title>您的頁面標題</title>',
                'priority': 1
            })
            score = 0
        else:
            title_text = title_tag.get_text().strip()

            # 檢查長度
            if len(title_text) < 30:
                issues.append({
                    'severity': 'high',
                    'message': f'標題太短（{len(title_text)} 字元）',
                    'suggestion': '建議標題長度為 50-60 字元',
                    'priority': 2
                })
                score -= 30
            elif len(title_text) > 60:
                issues.append({
                    'severity': 'medium',
                    'message': f'標題過長（{len(title_text)} 字元）',
                    'suggestion': '建議縮短至 50-60 字元',
                    'priority': 3
                })
                score -= 20

        return AnalysisResult(
            category='title',
            score=max(0, score),
            issues=issues
        )
```

## Railway 部署設定

### 必要檔案

#### 1. Procfile

```
web: gunicorn app:app
```

#### 2. runtime.txt

```
python-3.11.0
```

#### 3. requirements.txt

```
flask==3.0.0
flask-cors==4.0.0
beautifulsoup4==4.12.2
lxml==4.9.3
requests==2.31.0
gunicorn==21.2.0
```

#### 4. railway.json（可選）

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Flask 應用程式調整

```python
# app.py
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Railway 會設定 PORT 環境變數
port = int(os.environ.get('PORT', 5000))

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 分析邏輯
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
```

### 環境變數設定

在 Railway 設定以下環境變數：

```bash
PORT=5000                    # Railway 自動設定
FLASK_ENV=production         # 生產環境
ANALYZE_TIMEOUT=10           # 分析超時時間（秒）
MAX_HTML_SIZE=5242880       # 最大 HTML 大小（5MB）
```

### 部署步驟

1. **連結 GitHub 倉庫**

   ```bash
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **在 Railway 建立新專案**

   - 登入 Railway
   - New Project → Deploy from GitHub
   - 選擇您的倉庫

3. **Railway 自動部署**

   - Railway 會自動偵測 Python 專案
   - 讀取 requirements.txt 安裝依賴
   - 執行 Procfile 中的啟動命令

4. **取得網域**

   - Railway 自動提供 `.up.railway.app` 網域
   - 或設定自訂網域

5. **測試**
   - 訪問 Railway 提供的網址
   - 測試 SEO 分析功能

### 注意事項

- **無狀態設計**：不儲存使用者資料，每次請求獨立處理
- **請求超時**：設定合理的超時時間避免長時間佔用資源
- **記憶體限制**：Railway 免費版有記憶體限制，避免處理過大的網頁
- **錯誤處理**：所有錯誤都要妥善處理，避免服務崩潰

## 總結

這是一個部署到 Railway 的 SEO 分析工具：

- ✅ **簡單**：輸入網址就能分析
- ✅ **全面**：涵蓋 8 大 SEO 面向
- ✅ **實用**：提供具體的優化建議
- ✅ **快速**：分析時間控制在 10 秒內
- ✅ **線上存取**：部署到 Railway，隨時隨地可用
- ✅ **免費**：使用 Railway 免費方案

先做一個能用的基本版本，有需要再逐步擴充功能！
