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

- 🆕 **AI 智能優化（選用）**

  - 使用 OpenAI GPT-4 分析內容品質
  - 自動產生優化的 meta description 和 title
  - 智能生成圖片 alt 文字

- 🚀 **進階 AI 優化（選用）** - NEW!

  - ⚠️ 修改 H1 主標題
  - 📝 重寫文章段落改善 SEO
  - 🎯 調整關鍵字密度
  - 📋 修正複雜的標題結構
  - 包含詳細的 AI 分析和風險警告

- 🆕 **WordPress 自動修復**

  - 連接您的 WordPress 網站
  - 每個問題顯示「修復」按鈕
  - 點擊即可預覽並套用修復
  - 支援自動修復技術問題
  - AI 協助一般和進階內容優化

- ✅ **簡單易用**
  - 輸入網址即可分析
  - 清楚的問題列表和視覺化呈現
  - 支援結果匯出（JSON）
  - 可選：設定 WordPress 進行一鍵修復

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

可在 Railway 或本機設定以下環境變數：

| 變數名稱        | 說明                     | 預設值                   | 必要性 |
| --------------- | ------------------------ | ------------------------ | ------ |
| PORT            | 服務埠號                 | 5000（Railway 自動設定） | 否     |
| ANALYZE_TIMEOUT | 分析超時時間（秒）       | 10                       | 否     |
| MAX_HTML_SIZE   | 最大 HTML 大小（位元組） | 5242880（5MB）           | 否     |
| OPENAI_API_KEY  | OpenAI API 金鑰          | 無（不使用 AI 功能）     | 選用   |

### 設定 OpenAI API（選用）

如果要使用 AI 智能優化功能：

1. 前往 [OpenAI Platform](https://platform.openai.com/) 申請 API Key
2. 設定環境變數：
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
3. 在 Railway 設定中加入 `OPENAI_API_KEY`

**注意**：如果未設定 OpenAI API Key，工具仍可正常使用，只是不會提供 AI 優化功能。

### 設定 WordPress（選用）

如果要使用 WordPress 自動修復功能：

1. **產生 Application Password**

   - 登入 WordPress 後台
   - 前往「使用者」→「個人資料」
   - 捲動到「應用程式密碼」區塊
   - 輸入名稱（例如：SEO Analyzer）並點擊「新增」
   - 複製產生的密碼（格式：xxxx xxxx xxxx xxxx）

2. **在工具中設定**
   - 開啟 SEO 分析工具
   - 展開「WordPress 自動修復設定」
   - 填入您的 WordPress 網址、使用者名稱和 Application Password
   - 點擊「測試連線」確認設定正確
   - 點擊「儲存設定」

**注意**：WordPress 認證資訊只儲存在瀏覽器 sessionStorage 中，關閉分頁後會自動清除，不會上傳到伺服器。

## API 使用說明

### 1. 分析網址

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
    "headings": 85
  },
  "results": [
    {
      "category": "Meta 標籤",
      "score": 70,
      "issues": [
        {
          "severity": "high",
          "message": "Meta description 太短",
          "suggestion": "擴充為 150-160 字元",
          "priority": 2,
          "fixable_type": "ai",
          "fix_data": {...}
        }
      ]
    }
  ]
}
```

### 2. 測試 WordPress 連線

**端點**: `POST /api/wordpress/connect`

**請求範例**:

```json
{
  "site_url": "https://your-site.com",
  "username": "admin",
  "app_password": "xxxx xxxx xxxx xxxx"
}
```

**回應範例**:

```json
{
  "success": true,
  "message": "連線成功",
  "site_info": {
    "name": "您的網站名稱",
    "url": "https://your-site.com"
  }
}
```

### 3. 產生修復預覽

**端點**: `POST /api/fix/preview`

**請求範例**:

```json
{
  "issue": {
    "message": "Meta description 太短",
    "fixable_type": "ai",
    ...
  },
  "context": {
    "url": "https://example.com",
    "page_title": "頁面標題"
  }
}
```

**回應範例**:

```json
{
  "fixable_type": "ai",
  "before": "原始的 meta description",
  "after": "AI 優化後的 meta description...",
  "impact": "改善內容品質和吸引力"
}
```

### 4. 套用修復

**端點**: `POST /api/fix/apply`

**請求範例**:

```json
{
  "issue": {...},
  "fix_content": "修復內容",
  "context": {...},
  "wordpress": {
    "site_url": "https://your-site.com",
    "username": "admin",
    "app_password": "xxxx xxxx xxxx xxxx"
  }
}
```

**回應範例**:

```json
{
  "success": true,
  "message": "修復成功"
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
│   │   ├── base.py            # 基礎類別（含 fixable_type 支援）
│   │   ├── title.py           # Title 分析器
│   │   ├── meta.py            # Meta 分析器
│   │   ├── headings.py        # 標題結構分析器
│   │   ├── images.py          # 圖片分析器
│   │   ├── keywords.py        # 關鍵字分析器
│   │   ├── structure.py       # HTML 結構分析器
│   │   ├── performance.py     # 效能分析器
│   │   └── mobile.py          # 行動裝置分析器
│   ├── ai/                     # 🆕 AI 整合模組
│   │   ├── gpt5_client.py     # OpenAI 客戶端
│   │   └── content_generator.py  # 內容產生器
│   ├── wordpress/              # 🆕 WordPress 整合模組
│   │   └── client.py          # WordPress REST API 客戶端
│   ├── auto_fixer.py          # 🆕 自動修復引擎
│   └── utils/
│       └── scorer.py          # 評分系統
├── frontend/
│   ├── index.html             # 前端頁面（含 WordPress 設定和修復 modal）
│   ├── style.css              # 樣式（含新增的修復按鈕和 modal 樣式）
│   └── app.js                 # 前端邏輯（含 WordPress 和修復功能）
└── openspec/                  # OpenSpec 規格文件
    ├── project.md
    ├── changes/
    │   └── add-gpt5-wordpress-auto-fix/  # 本次變更提案
    │       ├── proposal.md
    │       ├── design.md
    │       ├── tasks.md
    │       └── specs/
    └── AGENTS.md
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

## 📚 文件

- [QUICKSTART.md](QUICKSTART.md) - 快速啟動指南
- [USAGE.md](USAGE.md) - 完整使用手冊
- [ADVANCED_AI_GUIDE.md](ADVANCED_AI_GUIDE.md) - 🆕 進階 AI 優化功能指南
- [CHANGELOG.md](CHANGELOG.md) - 版本變更記錄
- [OpenSpec 提案](openspec/changes/add-gpt5-wordpress-auto-fix/) - 技術設計文件

## 按鈕說明

分析完成後，每個問題會顯示不同的按鈕：

- **🔧 修復** - 技術問題，安全快速（風險：低）
- **🤖 AI 優化** - 一般內容優化（風險：中）
- **⚠️ 進階 AI 優化** - 🆕 重大內容變更（風險：高）
- **ℹ️ 需人工處理** - 極複雜的變更

詳細說明請見 [ADVANCED_AI_GUIDE.md](ADVANCED_AI_GUIDE.md)

## 授權

個人使用工具，免費開源。

## 作者

建立於 2024 年，使用 OpenSpec 規格驅動開發流程。
