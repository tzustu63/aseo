# 變更記錄

## [2.1.0] - 2024-10-23

### 🚀 進階 AI 優化功能

#### ✨ 新增功能

**進階 AI 輔助修復（ai-advanced）**

- ⚠️ 修改 H1 主標題 - AI 產生更優化的主標題
- 📝 重寫文章內容 - AI 改寫段落改善 SEO 和可讀性
- 🎯 調整關鍵字密度 - AI 自然融入關鍵字
- 📋 複雜的標題結構調整 - AI 修正 H1-H6 層級

**強化的 AI Prompt 系統**

- 專門的進階 prompt 模板
- 結構化 JSON 輸出
- 包含修改原因和 SEO 影響分析

**增強的安全機制**

- 風險等級標示（low/medium/high）
- 重大變更警告提示
- 詳細的 AI 分析資訊顯示
- 支援內容備份和取得

#### 🎨 UI/UX 改進

- 新增「⚠️ 進階 AI 優化」按鈕（橘紅色漸層）
- 顯示「重大變更」警告標籤
- 進階預覽顯示更多資訊：
  - AI 分析原因
  - SEO 影響說明
  - 主要改善項目
  - 變更說明清單
- 風險警告框（醒目的黃色背景）

#### 🔧 技術實作

- `backend/ai/advanced_prompts.py` - 進階 prompt 模板系統
- `backend/ai/gpt5_client.py` - 新增四個進階修復方法
- `backend/ai/content_generator.py` - `generate_advanced_fix()` 方法
- `backend/auto_fixer.py` - 支援 `ai-advanced` 類型分類
- `backend/wordpress/client.py` - 新增內容更新和備份方法
- `app.py` - 擴充 `/api/fix/preview` 支援進階類型
- `frontend/app.js` - 進階預覽顯示邏輯
- `frontend/style.css` - 進階按鈕和警告樣式

---

## [2.0.0] - 2024-10-23

### 🎉 重大功能更新：GPT-5 智能分析與 WordPress 自動修復

#### ✨ 新增功能

**AI 智能優化**

- 🤖 整合 OpenAI GPT-4 API（準備升級 GPT-5）
- 📊 AI 內容品質分析
- ✍️ 自動產生優化的 meta description
- 🏷️ 自動優化 title 標籤
- 🖼️ 智能生成圖片 alt 文字

**WordPress 自動修復**

- 🔌 WordPress REST API 整合
- 🔐 安全的 Application Password 認證
- 🔧 技術問題一鍵自動修復
- 🤖 AI 輔助內容優化
- 👀 修復前預覽功能
- ✅ 點擊「修復」按鈕才執行（完全掌控）

**使用者介面增強**

- 📝 WordPress 設定區塊（可摺疊）
- 🔘 每個問題項目顯示修復按鈕：
  - 🔧 修復（技術問題）
  - 🤖 AI 優化（內容問題）
  - ℹ️ 需人工處理（重大變更）
- 🪟 修復預覽 Modal
- 🔄 重新產生 AI 內容功能
- ✅ 修復完成狀態顯示

#### 🔧 技術改進

**後端架構**

- 新增 `backend/ai/` 模組 - OpenAI 整合
- 新增 `backend/wordpress/` 模組 - WordPress API 客戶端
- 新增 `backend/auto_fixer.py` - 自動修復引擎
- 擴充 `Issue` 類別支援 `fixable_type` 和 `fix_data`

**API 端點**

- `POST /api/wordpress/connect` - 測試 WordPress 連線
- `POST /api/fix/preview` - 產生修復預覽
- `POST /api/fix/apply` - 套用修復到 WordPress
- `POST /api/analyze` - 擴充支援 fixable_type 分類

**前端功能**

- WordPress 設定管理（sessionStorage）
- 修復流程實作
- Modal 對話框
- 即時狀態更新

#### 📦 依賴更新

- 新增 `openai>=1.0.0` - OpenAI Python SDK

#### 📚 文件更新

- 更新 `README.md` - 新功能說明和設定指南
- 新增 `USAGE.md` - 詳細使用手冊
- 新增 `.env.example` - 環境變數範例
- 新增 OpenSpec 變更提案文件

#### 🔒 安全性

- WordPress 認證資訊只儲存在瀏覽器（sessionStorage）
- 不上傳認證資訊到後端
- 關閉分頁後自動清除
- 所有修復操作需使用者明確確認

#### ♿️ 向後相容

- ✅ 所有原有功能保持不變
- ✅ AI 和 WordPress 功能是選用的
- ✅ 未設定 OpenAI API Key 仍可正常使用
- ✅ 未設定 WordPress 仍可進行分析

---

## [1.0.0] - 2024-10-20

### 初始版本

- SEO 多面向分析
- 評分系統
- 問題報告
- Railway 部署支援
