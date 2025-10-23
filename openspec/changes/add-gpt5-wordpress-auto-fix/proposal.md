# Proposal: GPT-5 智能分析與 WordPress 自動修復

## Why

現有的 SEO 分析工具只能找出問題並提供建議，但無法自動修復問題。使用者需要手動複製建議、登入 WordPress 後台、找到對應頁面/文章、逐一修改，過程耗時且容易出錯。

透過整合 OpenAI GPT-5 和 WordPress REST API，可以實現：

1. 更智能的 SEO 分析（AI 理解內容品質和使用者意圖）
2. 自動產生優化內容（meta description、title、alt text 等）
3. 使用者點擊「修復」按鈕後一鍵套用修改到 WordPress 網站
4. 大幅縮短 SEO 優化時間（從 1-2 小時降低到 5 分鐘）

## What Changes

- **新增 OpenAI GPT-5 整合模組**：在分析階段提供智能內容分析和建議
- **新增 WordPress REST API 整合模組**：連接並操作 WordPress 網站
- **新增自動修復引擎**：分類問題並自動或半自動修復
- **擴充分析結果格式**：加入 `fixable_type`（auto/ai/manual）和 `fix_data` 欄位
- **新增修復預覽功能**：顯示變更前後對比
- **新增前端修復介面**：每個問題項目顯示「修復」按鈕，點擊後觸發修復流程
- **新增修復確認流程**：使用者可以預覽並確認每個修復動作

## Impact

### Affected Specs

- **新增 capability**: `ai-analysis`（GPT-5 智能分析）
- **新增 capability**: `wordpress-integration`（WordPress 連接和操作）
- **新增 capability**: `auto-fix`（自動修復引擎）
- **修改 capability**: `seo-analysis`（擴充分析器支援 AI）

### Affected Code

- `app.py`：新增 WordPress 連線設定 API、修復執行 API
- `backend/ai/`：新增 GPT-5 分析模組
- `backend/wordpress/`：新增 WordPress REST API 客戶端
- `backend/auto_fixer.py`：新增自動修復引擎
- `backend/analyzers/base.py`：擴充 Issue 類別支援 fixable_type
- `frontend/index.html`：新增 WordPress 設定介面和修復按鈕
- `frontend/script.js`：新增修復流程和預覽功能
- `requirements.txt`：新增 openai 依賴

### Breaking Changes

無破壞性變更。所有新功能都是向後相容的擴充。

### Security Considerations

- WordPress 帳號密碼儲存在瀏覽器 sessionStorage（不存到後端）
- OpenAI API Key 透過環境變數管理
- 修復操作需要使用者明確點擊「修復」按鈕確認
- 提供預覽功能防止誤操作

## User Flow

1. 使用者輸入要分析的網址
2. （可選）輸入 WordPress 連線資訊（網址、使用者名稱、Application Password）
3. 點擊「分析」按鈕
4. 系統執行分析（包含 AI 分析）
5. 顯示分析結果，每個問題項目旁邊顯示：
   - 可自動修復的問題 → 「🔧 修復」按鈕
   - 需 AI 協助的問題 → 「🤖 AI 優化」按鈕
   - 需人工處理的問題 → 「ℹ️ 查看建議」按鈕
6. 使用者點擊「修復」或「AI 優化」按鈕
7. 系統產生修復內容並顯示預覽
8. 使用者確認後套用到 WordPress
9. 顯示修復結果和更新後的 SEO 分數
