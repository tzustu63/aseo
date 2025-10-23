# Design: GPT-5 智能分析與 WordPress 自動修復

## Context

現有的 SEO 分析工具使用規則型分析器（rule-based），只能檢測技術性問題，但無法評估內容品質。同時，使用者需要手動將建議套用到 WordPress 網站。

### Constraints

- Railway 免費版記憶體限制（512MB）
- OpenAI API 呼叫成本（需控制 token 使用量）
- 分析時間需控制在 30 秒內
- 個人工具，無需複雜的帳號系統

## Goals / Non-Goals

### Goals

- ✅ 在分析階段加入 GPT-5 智能分析（可選）
- ✅ 自動產生優化內容（meta、title、alt）
- ✅ 連接 WordPress 並提供一鍵修復
- ✅ 每個問題顯示「修復」按鈕，點擊後觸發修復流程
- ✅ 提供修改預覽和確認機制
- ✅ 保持介面簡單易用

### Non-Goals

- ❌ 不支援非 WordPress 網站的自動修復
- ❌ 不儲存使用者的 WordPress 帳號密碼到後端
- ❌ 不提供批量多網站管理

## Decisions

### Decision 1: 使用 OpenAI GPT-4（準備升級 GPT-5）

**Why**: GPT-4 提供良好的語意理解和內容生成能力，API 穩定且成本可控

**Implementation**:

```python
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=os.environ['OPENAI_API_KEY'])
```

### Decision 2: 使用 WordPress REST API

**Why**: WordPress 內建 REST API，支援 Application Password 認證（安全）

**Implementation**:

```python
import requests
from requests.auth import HTTPBasicAuth

class WordPressClient:
    def __init__(self, site_url, username, app_password):
        self.auth = HTTPBasicAuth(username, app_password)
```

### Decision 3: 三層修復策略

1. **自動修復**（技術問題）：無需預覽，直接提供修復選項
2. **AI 輔助修復**（內容問題）：GPT-5 產生內容，顯示預覽
3. **人工審核**（重大變更）：只提供建議

### Decision 4: 前端儲存 WordPress 認證

**Why**: 避免後端儲存敏感資訊，使用 sessionStorage 暫存

**Security**: sessionStorage 在關閉分頁後自動清除

### Decision 5: 使用者點擊才觸發修復

**Why**: 確保使用者完全掌控修復流程，避免誤操作

**Flow**:

1. 顯示分析結果，每個問題有「修復」按鈕
2. 使用者點擊「修復」
3. 系統產生修復內容並顯示預覽
4. 使用者確認後套用

## Architecture

### 後端模組架構

```
backend/
├── ai/
│   ├── __init__.py
│   ├── gpt5_client.py        # OpenAI 客戶端
│   ├── content_analyzer.py   # 內容分析
│   └── content_generator.py  # 內容產生
├── wordpress/
│   ├── __init__.py
│   └── client.py             # WordPress REST API 客戶端
├── auto_fixer.py             # 自動修復引擎
└── analyzers/
    └── base.py               # 擴充 Issue 類別
```

### API 端點設計

```
POST /api/analyze              # 擴充：包含 AI 分析（可選）
POST /api/wordpress/connect    # 測試 WordPress 連線
POST /api/fix/preview          # 產生修復預覽
POST /api/fix/apply            # 套用修復到 WordPress
```

### 資料流程

```
1. 使用者輸入網址 + WordPress 設定（可選）
   ↓
2. 後端抓取 HTML
   ↓
3. 執行分析（傳統 + AI，若 OpenAI API 可用）
   ↓
4. 整合結果，標記 fixable_type
   ↓
5. 前端顯示問題列表，每個問題有「修復」按鈕
   ↓
6. 使用者點擊「修復」按鈕
   ↓
7. 前端呼叫 /api/fix/preview
   ↓
8. 後端產生修復內容（技術問題直接產生，內容問題呼叫 GPT-5）
   ↓
9. 前端顯示預覽 modal
   ↓
10. 使用者確認
    ↓
11. 前端呼叫 /api/fix/apply
    ↓
12. 後端透過 WordPress API 套用修改
    ↓
13. 回傳成功/失敗訊息
```

## Risks / Trade-offs

### Risk 1: OpenAI API 成本

**Mitigation**:

- 限制內容長度（最多 2000 字）
- 提供「僅傳統分析」模式（環境變數控制）
- 使用 GPT-4 而非 GPT-5（成本較低）

### Risk 2: WordPress API 速率限制

**Mitigation**:

- 單次修復間隔 0.5 秒
- 顯示進度訊息

### Risk 3: GPT-5 產生不當內容

**Mitigation**:

- 所有 AI 產生的內容都需使用者確認
- 提供「重新產生」選項

### Risk 4: 誤操作

**Mitigation**:

- 每個修復都需使用者點擊「修復」按鈕
- 修改前顯示預覽
- 只修改 meta 資料和 alt 屬性，不修改文章內容主體

## Migration Plan

### Phase 1: 基礎整合（現在）

- [x] 創建 OpenSpec 提案
- [ ] 實作 OpenAI 整合
- [ ] 實作 WordPress 整合

### Phase 2: 自動修復（現在）

- [ ] 實作自動修復引擎
- [ ] 更新分析器
- [ ] 新增 API 端點

### Phase 3: 前端介面（現在）

- [ ] 新增 WordPress 設定區塊
- [ ] 新增「修復」按鈕
- [ ] 新增預覽 modal

### Phase 4: 測試（現在）

- [ ] 測試各種情境
- [ ] 優化使用者體驗

## Open Questions

- [x] 是否需要支援 WordPress.com vs 自架 WordPress？
      → 決定：先支援自架 WordPress（使用 Application Password）
- [x] 是否儲存修改歷史？
      → 決定：不儲存，保持無狀態
- [x] GPT-5 API 呼叫失敗時？
      → 決定：回退到純規則分析，不中斷流程
