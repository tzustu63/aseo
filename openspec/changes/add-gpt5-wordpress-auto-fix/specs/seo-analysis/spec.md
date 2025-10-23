# SEO Analysis Capability (Modifications)

## MODIFIED Requirements

### Requirement: SEO Analysis Execution

系統 SHALL 分析網頁的 SEO 問題，包括技術 SEO、內容 SEO、圖片 SEO 等多個面向，並可選擇性整合 AI 智能分析。

#### Scenario: 分析包含 AI 增強（當 OpenAI API 可用）

- **GIVEN** 一個有效的網頁 URL
- **AND** 環境變數 OPENAI_API_KEY 已設定
- **WHEN** 系統執行分析
- **THEN** 執行傳統規則型分析器
- **AND** 嘗試執行 AI 分析（若 API 可用）
- **AND** 整合兩者結果
- **AND** 每個問題標記可修復類型（auto/ai/manual）
- **AND** AI 分析失敗時仍回傳傳統分析結果

#### Scenario: 僅使用傳統分析（當 AI 不可用）

- **GIVEN** 一個有效的網頁 URL
- **AND** 環境變數 OPENAI_API_KEY 未設定或 API 呼叫失敗
- **WHEN** 系統執行分析
- **THEN** 只執行傳統規則型分析
- **AND** 不呼叫 GPT API
- **AND** 問題不包含 AI 產生的建議
- **AND** AI 相關的 fixable_type 標記為 manual

### Requirement: Issue Reporting

系統 SHALL 回報所有發現的 SEO 問題，包括嚴重性、建議、程式碼範例，以及可修復類型和修復所需資料。

#### Scenario: 回報可自動修復的問題

- **GIVEN** 分析發現缺少 viewport meta 標籤
- **WHEN** 系統產生分析報告
- **THEN** 回傳問題資訊
- **AND** `fixable_type` 設為 `auto`
- **AND** `fix_data` 包含要插入的完整標籤內容
- **AND** 前端顯示「🔧 修復」按鈕

#### Scenario: 回報需 AI 輔助的問題

- **GIVEN** 分析發現 meta description 太短
- **WHEN** 系統產生分析報告
- **THEN** 回傳問題資訊
- **AND** `fixable_type` 設為 `ai`
- **AND** `fix_data` 包含目前值和需要的長度範圍
- **AND** `fix_data` 包含頁面標題和內容摘要（供 AI 使用）
- **AND** 前端顯示「🤖 AI 優化」按鈕

#### Scenario: 回報需人工處理的問題

- **GIVEN** 分析發現建議修改 H1 標題
- **WHEN** 系統產生分析報告
- **THEN** 回傳問題資訊
- **AND** `fixable_type` 設為 `manual`
- **AND** 不提供 fix_data
- **AND** 前端顯示「ℹ️ 查看建議」按鈕

#### Scenario: 問題包含 WordPress 定位資訊

- **GIVEN** 分析發現可修復的問題
- **AND** 問題可以透過 WordPress API 修復
- **WHEN** 系統產生分析報告
- **THEN** fix_data 包含 WordPress 定位資訊
- **AND** 如果是 meta 問題，包含可能的 post_id 或 URL
- **AND** 如果是圖片問題，包含 media_id 或圖片 URL
