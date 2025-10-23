# WordPress Integration Capability

## ADDED Requirements

### Requirement: WordPress Connection

系統 SHALL 支援連接到 WordPress 網站，使用 REST API 和 Application Password 認證。

#### Scenario: 成功連接 WordPress

- **GIVEN** 有效的 WordPress 網址、使用者名稱和 Application Password
- **WHEN** 使用者點擊「測試連線」
- **THEN** 系統呼叫 WordPress REST API
- **AND** 驗證認證資訊
- **AND** 回傳連線成功訊息
- **AND** 顯示網站標題資訊

#### Scenario: 連線失敗 - 無效認證

- **GIVEN** 錯誤的使用者名稱或密碼
- **WHEN** 使用者點擊「測試連線」
- **THEN** 系統嘗試連線
- **AND** 收到 401 Unauthorized 錯誤
- **AND** 回傳錯誤訊息「認證失敗，請檢查使用者名稱和 Application Password」

#### Scenario: 連線失敗 - 無法連線

- **GIVEN** 無效的 WordPress 網址或網站無法連線
- **WHEN** 使用者點擊「測試連線」
- **THEN** 系統嘗試連線
- **AND** 超時或連線錯誤
- **AND** 回傳錯誤訊息「無法連線到 WordPress 網站，請確認網址是否正確」

### Requirement: WordPress Content Update

系統 SHALL 透過 WordPress REST API 更新文章、頁面的 meta 資訊和圖片 alt 屬性。

#### Scenario: 更新文章 meta description

- **GIVEN** 已連線的 WordPress 網站
- **AND** 一個文章的 URL 或 ID
- **AND** 新的 meta description 內容
- **WHEN** 使用者確認套用修復
- **THEN** 系統呼叫 WordPress API 更新文章 meta
- **AND** 回傳更新成功訊息

#### Scenario: 更新圖片 alt 屬性

- **GIVEN** 已連線的 WordPress 網站
- **AND** 一張圖片的 ID 或 URL
- **AND** 新的 alt 文字
- **WHEN** 使用者確認套用修復
- **THEN** 系統呼叫 WordPress Media API 更新 alt 屬性
- **AND** 回傳更新成功訊息

#### Scenario: 更新失敗 - API 錯誤

- **GIVEN** 一個修復請求
- **WHEN** WordPress API 回應錯誤（如權限不足）
- **THEN** 捕捉錯誤
- **AND** 回傳明確的錯誤訊息給使用者
- **AND** 不影響其他修復項目

### Requirement: Credential Security

系統 SHALL 安全處理 WordPress 認證資訊，不儲存到後端。

#### Scenario: 認證資訊儲存在前端

- **GIVEN** 使用者輸入 WordPress 認證資訊
- **WHEN** 使用者點擊「儲存設定」
- **THEN** 認證資訊儲存在瀏覽器 sessionStorage
- **AND** 不傳送到後端儲存
- **AND** 關閉瀏覽器分頁後自動清除

#### Scenario: API 請求使用認證

- **GIVEN** 使用者要執行修復
- **WHEN** 前端呼叫後端 API
- **THEN** 前端從 sessionStorage 讀取認證資訊
- **AND** 在請求中傳送認證給後端
- **AND** 後端使用認證呼叫 WordPress API
- **AND** 後端不儲存認證資訊
