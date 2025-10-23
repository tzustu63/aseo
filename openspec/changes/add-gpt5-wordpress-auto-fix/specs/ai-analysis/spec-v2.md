# AI Analysis Capability - Advanced Features (v2.1)

## ADDED Requirements

### Requirement: Advanced AI Content Optimization

系統 SHALL 使用強化的 AI prompt 系統處理重大內容變更，包括 H1 優化、關鍵字密度調整、標題結構修正和內容重寫。

#### Scenario: 優化 H1 主標題

- **GIVEN** 一個 H1 標題需要優化
- **AND** 文章內容摘要和目標關鍵字
- **WHEN** 使用者點擊「⚠️ 進階 AI 優化」
- **THEN** AI 分析文章主題
- **AND** 產生優化的 H1 標題（60 字元以內）
- **AND** 回傳 JSON 包含：new_h1、reasoning、seo_impact、keywords_used
- **AND** 前端顯示風險警告和詳細預覽

#### Scenario: 調整關鍵字密度

- **GIVEN** 一個段落的關鍵字密度不理想
- **AND** 目標關鍵字和當前密度資訊
- **WHEN** 使用者點擊「⚠️ 進階 AI 優化」
- **THEN** AI 重寫段落自然融入關鍵字
- **AND** 保持原始訊息完整
- **AND** 達到 1-2% 的理想密度
- **AND** 回傳 JSON 包含：optimized_paragraph、keyword_count、new_density、changes_made

#### Scenario: 修正標題結構

- **GIVEN** 文章標題層級混亂（如 H1→H4→H2）
- **AND** 當前的 HTML 結構
- **WHEN** 使用者點擊「⚠️ 進階 AI 優化」
- **THEN** AI 分析標題邏輯層級
- **AND** 修正為正確順序（H1→H2→H3）
- **AND** 保持所有文字內容不變
- **AND** 回傳 JSON 包含：fixed_html、changes、explanation

#### Scenario: 重寫內容段落

- **GIVEN** 一個段落需要改善可讀性和 SEO
- **AND** 優化目標和關鍵字
- **WHEN** 使用者點擊「⚠️ 進階 AI 優化」
- **THEN** AI 重寫段落
- **AND** 保留核心訊息和重要資訊
- **AND** 改善句子結構和可讀性
- **AND** 回傳 JSON 包含：optimized_content、key_improvements、preserved_elements、seo_enhancements

### Requirement: Advanced Fix Classification

系統 SHALL 自動識別需要進階 AI 處理的問題，並標記為 `ai-advanced` 類型。

#### Scenario: 識別 H1 相關問題

- **GIVEN** 分析發現 H1 標題相關問題
- **WHEN** 系統分類問題類型
- **THEN** 標記為 `fixable_type: ai-advanced`
- **AND** 記錄 issue_type 為 `h1_title`
- **AND** 前端顯示「⚠️ 進階 AI 優化」按鈕

#### Scenario: 識別關鍵字密度問題

- **GIVEN** 分析發現關鍵字密度不理想
- **WHEN** 系統分類問題類型
- **THEN** 標記為 `fixable_type: ai-advanced`
- **AND** 記錄 issue_type 為 `keyword_density`

#### Scenario: 識別標題結構問題

- **GIVEN** 分析發現標題層級跳級或混亂
- **WHEN** 系統分類問題類型
- **THEN** 標記為 `fixable_type: ai-advanced`
- **AND** 記錄 issue_type 為 `heading_structure`

### Requirement: Risk Warning Display

系統 SHALL 在進階 AI 優化時顯示明確的風險警告。

#### Scenario: 顯示風險警告框

- **GIVEN** 使用者點擊「⚠️ 進階 AI 優化」
- **WHEN** 預覽 modal 開啟
- **THEN** 在最上方顯示醒目的警告框
- **AND** 警告框使用黃色背景和紅色邊框
- **AND** 顯示文字「⚠️ 重大內容變更警告」
- **AND** 說明「這是重大內容變更，請仔細檢查 AI 產生的內容」

#### Scenario: 顯示詳細的 AI 分析

- **GIVEN** AI 已產生進階優化內容
- **WHEN** 顯示預覽
- **THEN** 顯示修復前後對比
- **AND** 顯示 AI 分析原因
- **AND** 顯示 SEO 影響說明
- **AND** 顯示主要改善項目列表
- **AND** 修復後的內容使用橘色邊框強調

### Requirement: Advanced Fix Application

系統 SHALL 在使用者明確確認後，透過 WordPress API 套用進階修復。

#### Scenario: 套用 H1 優化

- **GIVEN** 使用者已確認 H1 優化內容
- **WHEN** 點擊「確認套用」
- **THEN** 系統取得文章原始內容
- **AND** 使用 BeautifulSoup 找到 H1 標籤
- **AND** 替換為新的 H1 內容
- **AND** 透過 WordPress API 更新文章
- **AND** 回傳成功訊息

#### Scenario: 套用段落重寫

- **GIVEN** 使用者已確認段落重寫內容
- **WHEN** 點擊「確認套用」
- **THEN** 系統取得文章原始內容
- **AND** 找到並替換指定段落
- **AND** 透過 WordPress API 更新文章
- **AND** 回傳成功訊息

#### Scenario: 套用失敗時的處理

- **GIVEN** WordPress API 更新失敗
- **WHEN** 系統嘗試套用進階修復
- **THEN** 捕捉錯誤
- **AND** 不修改任何內容
- **AND** 回傳明確的錯誤訊息
- **AND** 建議使用者手動處理
