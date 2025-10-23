# Auto-Fix Capability

## ADDED Requirements

### Requirement: Issue Classification

系統 SHALL 自動分類每個 SEO 問題的可修復類型：自動修復（auto）、AI 輔助修復（ai）、人工修復（manual）。

#### Scenario: 分類技術性問題為自動修復

- **GIVEN** 一個問題：缺少 viewport meta 標籤
- **WHEN** 系統執行分類
- **THEN** 標記為 `fixable_type: auto`
- **AND** 產生修復所需的資料（完整標籤內容）
- **AND** 前端顯示「🔧 修復」按鈕

#### Scenario: 分類內容問題為 AI 輔助修復

- **GIVEN** 一個問題：meta description 太短
- **WHEN** 系統執行分類
- **THEN** 標記為 `fixable_type: ai`
- **AND** 記錄需要的資料（目前值、目標長度）
- **AND** 前端顯示「🤖 AI 優化」按鈕

#### Scenario: 分類重大變更為人工修復

- **GIVEN** 一個問題：建議修改 H1 主標題
- **WHEN** 系統執行分類
- **THEN** 標記為 `fixable_type: manual`
- **AND** 不提供自動修復選項
- **AND** 前端顯示「ℹ️ 查看建議」按鈕

### Requirement: User-Initiated Fix

系統 SHALL 只在使用者明確點擊「修復」按鈕後才執行修復，確保使用者完全掌控。

#### Scenario: 使用者點擊修復按鈕

- **GIVEN** 分析結果顯示一個可修復的問題
- **AND** 問題旁邊有「修復」按鈕
- **WHEN** 使用者點擊「修復」按鈕
- **THEN** 前端呼叫 `/api/fix/preview` API
- **AND** 後端產生修復內容
- **AND** 前端顯示預覽 modal
- **AND** 使用者可以確認或取消

#### Scenario: 使用者未點擊修復按鈕

- **GIVEN** 分析結果顯示多個可修復的問題
- **WHEN** 使用者不點擊任何「修復」按鈕
- **THEN** 系統不執行任何修復動作
- **AND** 不呼叫 WordPress API
- **AND** 保持網站內容不變

### Requirement: Fix Preview

系統 SHALL 在套用修復前顯示變更預覽，讓使用者確認。

#### Scenario: 預覽技術問題修復

- **GIVEN** 一個技術問題（如缺少 viewport）
- **WHEN** 使用者點擊「修復」
- **THEN** 顯示 modal 對話框
- **AND** 顯示要加入的標籤內容
- **AND** 顯示預期影響說明
- **AND** 提供「確認套用」和「取消」按鈕

#### Scenario: 預覽 AI 產生的內容

- **GIVEN** 一個 AI 產生的 meta description 優化建議
- **WHEN** 使用者點擊「AI 優化」
- **THEN** 後端呼叫 GPT API 產生新內容
- **AND** 顯示 modal 對話框
- **AND** 顯示「變更前」的原始內容
- **AND** 顯示「變更後」的新內容（AI 產生）
- **AND** 顯示字元數變化
- **AND** 提供「確認套用」、「重新產生」、「取消」按鈕

#### Scenario: 重新產生 AI 內容

- **GIVEN** 使用者對第一次產生的 AI 內容不滿意
- **WHEN** 使用者點擊「重新產生」按鈕
- **THEN** 後端再次呼叫 GPT API
- **AND** 產生新的優化內容
- **AND** 更新預覽 modal 中的「變更後」內容

### Requirement: Fix Application

系統 SHALL 在使用者確認後透過 WordPress API 套用修復。

#### Scenario: 套用技術問題修復

- **GIVEN** 使用者已預覽並確認修復
- **AND** WordPress 連線資訊已設定
- **WHEN** 使用者點擊「確認套用」
- **THEN** 前端呼叫 `/api/fix/apply` API
- **AND** 後端透過 WordPress API 更新內容
- **AND** 回傳成功訊息
- **AND** 前端關閉 modal 並顯示「✅ 已修復」

#### Scenario: 套用 AI 優化內容

- **GIVEN** 一個 AI 產生的 meta description
- **AND** 使用者已確認預覽
- **WHEN** 使用者點擊「確認套用」
- **THEN** 後端透過 WordPress API 更新 meta
- **AND** 回傳成功訊息
- **AND** 前端標記該問題為「已修復」

#### Scenario: 修復失敗處理

- **GIVEN** 一個修復請求
- **AND** WordPress API 回應錯誤
- **WHEN** 系統嘗試套用修復
- **THEN** 捕捉錯誤
- **AND** 顯示明確的錯誤訊息
- **AND** 提供「重試」選項

### Requirement: WordPress Not Connected Handling

系統 SHALL 在 WordPress 未連線時提供明確提示。

#### Scenario: 未設定 WordPress 連線就點擊修復

- **GIVEN** 使用者未輸入 WordPress 連線資訊
- **WHEN** 使用者點擊任何「修復」按鈕
- **THEN** 顯示提示訊息「請先設定 WordPress 連線資訊」
- **AND** 自動捲動到 WordPress 設定區塊
- **AND** 不執行修復動作
