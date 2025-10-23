# AI Analysis Capability

## ADDED Requirements

### Requirement: AI Content Quality Analysis

系統 SHALL 使用 GPT-4/GPT-5 分析網頁內容品質，評估內容是否符合 SEO 最佳實踐和使用者意圖。

#### Scenario: 分析網頁內容品質

- **GIVEN** 一個包含內容的網頁 HTML
- **WHEN** 系統執行 AI 分析且 OpenAI API 可用
- **THEN** 回傳內容品質分數（1-10）
- **AND** 回傳可讀性評估
- **AND** 回傳主題相關性評估
- **AND** 回傳改善建議列表

#### Scenario: GPT API 呼叫失敗時回退

- **GIVEN** OpenAI API 無法連線或回應錯誤
- **WHEN** 系統嘗試執行 AI 分析
- **THEN** 記錄錯誤訊息到 log
- **AND** 回退到純規則分析
- **AND** 不中斷整體分析流程
- **AND** 回傳的問題不包含 AI 產生的建議

#### Scenario: AI 分析被停用

- **GIVEN** 環境變數 OPENAI_API_KEY 未設定
- **WHEN** 系統執行分析
- **THEN** 跳過 AI 分析步驟
- **AND** 只執行傳統規則型分析

### Requirement: AI Content Generation

系統 SHALL 使用 GPT-4/GPT-5 產生優化的 SEO 內容，包括 meta description、title、圖片 alt 文字等。

#### Scenario: 產生優化的 meta description

- **GIVEN** 一個缺少或不佳的 meta description 的網頁
- **AND** 頁面標題和內容摘要
- **WHEN** 使用者點擊「AI 優化」按鈕
- **THEN** GPT 分析頁面內容
- **AND** 產生 150-160 字元的 meta description
- **AND** 包含頁面主要關鍵字
- **AND** 具有吸引點擊的描述

#### Scenario: 優化 title 標籤

- **GIVEN** 一個 title 過長或不佳的網頁
- **AND** 目前的 title 和頁面內容
- **WHEN** 使用者請求 AI 優化
- **THEN** GPT 產生 50-60 字元的新 title
- **AND** 保留核心關鍵字
- **AND** 更具吸引力和描述性

#### Scenario: 產生圖片 alt 文字

- **GIVEN** 一張缺少 alt 屬性的圖片
- **AND** 圖片檔名、URL、所在文章標題
- **WHEN** 使用者請求 AI 產生 alt
- **THEN** GPT 根據上下文產生描述性 alt 文字
- **AND** alt 文字長度不超過 125 字元
- **AND** 包含相關關鍵字（若適用）

### Requirement: Token Usage Optimization

系統 SHALL 優化 OpenAI API token 使用量，控制成本。

#### Scenario: 限制輸入內容長度

- **GIVEN** 一個超過 5000 字的長網頁
- **WHEN** 系統準備呼叫 GPT API
- **THEN** 只傳送前 2000 字和 meta 資訊
- **AND** 記錄內容被截斷的警告（若需要）

#### Scenario: 使用適當的 model 降低成本

- **GIVEN** 系統需要呼叫 OpenAI API
- **WHEN** 執行內容分析或產生
- **THEN** 優先使用 GPT-4 而非 GPT-5（成本較低）
- **AND** 設定合理的 max_tokens 限制
