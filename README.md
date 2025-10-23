# SEO 網頁分析工具

🔍 一個簡單好用的 SEO 網頁分析工具，輸入網址即可檢查 SEO 問題並獲得優化建議。

## 功能特色

- ✅ **多面向 SEO 分析**
  - Title 標籤檢查
  - Meta 標籤分析
  - 標題結構（H1-H6）
  - 圖片優化（alt 屬性）
  - 關鍵字分析
  - HTML 結構
  - 頁面效能
  - 行動裝置友善度

- ✅ **評分系統**
  - 0-100 分的 SEO 健康度評分
  - 五個等級：優秀、良好、普通、待改善、需大幅優化

- ✅ **具體建議**
  - 每個問題都提供具體的優化建議
  - 包含程式碼範例
  - 標示優先順序和難度

- ✅ **簡單易用**
  - 輸入網址即可分析
  - 清楚的問題列表和視覺化呈現
  - 支援結果匯出（JSON）

## 安裝與執行

### 本機開發

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **執行應用程式**
   ```bash
   python app.py
   ```

3. **開啟瀏覽器**
   ```
   http://localhost:5000
   ```

### Railway 部署

1. **推送到 GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **在 Railway 建立專案**
   - 登入 [Railway](https://railway.app)
   - New Project → Deploy from GitHub
   - 選擇您的倉庫

3. **Railway 自動部署**
   - Railway 會自動偵測 Python 專案
   - 讀取 `requirements.txt` 安裝依賴
   - 執行 `Procfile` 中的命令

4. **取得網址**
   - Railway 會提供一個 `.up.railway.app` 網域
   - 或設定自訂網域

## 環境變數

可在 Railway 設定以下環境變數：

| 變數名稱 | 說明 | 預設值 |
|---------|------|--------|
| PORT | 服務埠號 | 5000（Railway 自動設定） |
| ANALYZE_TIMEOUT | 分析超時時間（秒） | 10 |
| MAX_HTML_SIZE | 最大 HTML 大小（位元組） | 5242880（5MB） |

## API 使用說明

### 分析網址

**端點**: `POST /api/analyze`

**請求範例**:
```json
{
  "url": "https://example.com"
}
```

**回應範例**:
```json
{
  "url": "https://example.com",
  "total_score": 85.5,
  "grade": {
    "level": "良好",
    "stars": "⭐⭐⭐⭐",
    "description": "您的網頁 SEO 狀況良好..."
  },
  "analysis_time": "2.3s",
  "summary": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 3,
    "total_issues": 10
  },
  "category_scores": {
    "title": 100,
    "meta_tags": 70,
    "headings": 85,
    ...
  },
  "results": [...]
}
```

## 專案結構

```
findseoproblem/
├── app.py                      # Flask 主程式
├── requirements.txt            # Python 依賴
├── Procfile                    # Railway 啟動命令
├── runtime.txt                 # Python 版本
├── railway.json                # Railway 配置
├── backend/
│   ├── analyzers/              # SEO 分析器
│   │   ├── base.py            # 基礎類別
│   │   ├── title.py           # Title 分析器
│   │   ├── meta.py            # Meta 分析器
│   │   ├── headings.py        # 標題結構分析器
│   │   ├── images.py          # 圖片分析器
│   │   ├── keywords.py        # 關鍵字分析器
│   │   ├── structure.py       # HTML 結構分析器
│   │   ├── performance.py     # 效能分析器
│   │   └── mobile.py          # 行動裝置分析器
│   └── utils/
│       └── scorer.py          # 評分系統
└── frontend/
    ├── index.html             # 前端頁面
    ├── style.css              # 樣式
    └── app.js                 # 前端邏輯
```

## 開發指南

### 新增分析器

1. 在 `backend/analyzers/` 建立新的分析器檔案
2. 繼承 `BaseAnalyzer` 類別
3. 實作 `analyze` 方法
4. 在 `analyzers/__init__.py` 中匯出
5. 在 `app.py` 的 `ANALYZERS` 列表中加入
6. 在 `utils/scorer.py` 的 `WEIGHTS` 中加入權重

範例：
```python
from .base import BaseAnalyzer, AnalysisResult

class NewAnalyzer(BaseAnalyzer):
    def analyze(self, html: str, url: str) -> AnalysisResult:
        # 分析邏輯
        return AnalysisResult(...)
```

## 測試範例

可以使用以下網址測試：

- ✅ **優化良好的網站**: https://developer.mozilla.org
- ⚠️ **有問題的網站**: 自行測試需要優化的網站
- 🌐 **您自己的網站**: 輸入您的網站進行分析

## 授權

個人使用工具，免費開源。

## 作者

建立於 2024 年，使用 OpenSpec 規格驅動開發流程。

