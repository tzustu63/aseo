# 🧪 測試 API Key 安全功能

## 快速測試指南

### 測試環境

- 本地：http://localhost:8000
- Railway：https://your-project.up.railway.app

---

## 測試 1：輸入顯示星號 ⭐

### 步驟

1. 訪問網站
2. 展開「AI 增強分析」區塊
3. 在 API Key 輸入框輸入任何文字（例如：`sk-test123`）

### 預期結果

✅ 輸入時顯示：`**********`（星號）
❌ **不應該**顯示明文

### 實際測試

```
輸入：sk-test123
顯示：**********  ✅ 通過
```

---

## 測試 2：儲存到記憶體（不儲存到 localStorage） 💾

### 步驟

1. 輸入測試 API Key：`sk-test-key-for-testing`
2. 點擊「儲存設定」
3. 打開瀏覽器開發者工具（F12）
4. 切換到「Application」或「儲存空間」標籤
5. 查看 localStorage

### 預期結果

✅ localStorage 中**沒有** `openai_api_key` 項目
✅ 顯示訊息：「✅ 設定已儲存！本次分析將使用 AI 增強功能（重新整理後需重新輸入）」

### 檢查指令（開發者工具 Console）

```javascript
// 檢查 localStorage
console.log(localStorage.getItem("openai_api_key"));
// 預期輸出：null （沒有儲存）
```

---

## 測試 3：重新整理頁面清除 API Key 🔄

### 步驟

1. 輸入並儲存 API Key
2. 確認儲存成功
3. 按 `F5` 或 `Cmd+R` 重新整理頁面
4. 查看 API Key 輸入框

### 預期結果

✅ 輸入框為**空白**（無任何內容）
✅ 需要重新輸入 API Key

### 實際測試

```
儲存前：sk-test123 → **********
重新整理
儲存後：[空白]  ✅ 通過
```

---

## 測試 4：關閉分頁後清除 🚪

### 步驟

1. 輸入並儲存 API Key
2. 關閉整個瀏覽器分頁
3. 重新打開網站
4. 查看 API Key 輸入框

### 預期結果

✅ 輸入框為**空白**
✅ 完全清除，無殘留

---

## 測試 5：無 API Key 時的基本分析 📊

### 步驟

1. **不輸入** API Key
2. 直接輸入測試網址：`https://example.com`
3. 點擊「開始分析」

### 預期結果

✅ 分析正常執行
✅ 顯示 12 項 SEO 分析結果
❌ **不使用** AI 增強功能
✅ 分析時間較短（約 2-5 秒）

---

## 測試 6：有 API Key 時的 AI 增強分析 🤖

### 步驟

1. 輸入有效的 OpenAI API Key
2. 點擊「測試 API Key」確認有效
3. 點擊「儲存設定」
4. 輸入測試網址：`https://example.com`
5. 點擊「開始分析」

### 預期結果

✅ 顯示進度條（12 步進度）
✅ 分析時間較長（約 30-60 秒）
✅ 結果中有「AI 增強分析」標記
✅ 每個問題都有詳細的 AI 建議

---

## 測試 7：安全提示訊息 ⚠️

### 檢查位置

1. API Key 輸入框下方

### 預期顯示

```
⚠️ 為了安全，API Key 不會儲存，重新整理頁面後需重新輸入
前往 OpenAI Platform 申請 API Key
```

### 儲存成功後

```
✅ 設定已儲存！本次分析將使用 AI 增強功能（重新整理後需重新輸入）
```

---

## 測試 8：多分頁獨立性 🪟

### 步驟

1. **分頁 A**：輸入並儲存 API Key
2. 開啟**分頁 B**（新分頁，相同網址）
3. 查看分頁 B 的 API Key 輸入框

### 預期結果

✅ 分頁 B 的輸入框為**空白**
✅ 每個分頁獨立，互不影響

---

## 測試 9：autocomplete 禁用 🔒

### 步驟

1. 輸入並儲存 API Key
2. 重新整理頁面
3. 點擊 API Key 輸入框
4. 觀察瀏覽器是否嘗試自動填入

### 預期結果

✅ **不會**自動填入
✅ `autocomplete="off"` 生效

---

## 測試 10：完整流程測試 🎯

### 完整使用流程

#### 第一次使用

```
1. 訪問網站 → 輸入框空白 ✅
2. 展開 AI 區塊
3. 輸入 API Key → 顯示 *** ✅
4. 測試 API Key → 成功 ✅
5. 儲存設定 → 提示訊息 ✅
6. 分析網站 → AI 增強運作 ✅
```

#### 重新整理後

```
1. 按 F5 重新整理
2. API Key 輸入框 → 空白 ✅
3. 嘗試分析 → 僅基本分析 ✅
4. 重新輸入 API Key
5. 儲存 → 可再次使用 AI ✅
```

---

## 🎓 開發者檢查

### 檢查 JavaScript 程式碼

#### 1. 確認初始值為空

```javascript
// frontend/app.js
let openaiApiKey = ""; // ✅ 應該是空字串
// ❌ 不應該是：localStorage.getItem("openai_api_key")
```

#### 2. 確認不儲存到 localStorage

```javascript
// frontend/app.js - saveOpenAIConfig()
openaiApiKey = apiKey; // ✅ 僅儲存到變數
// ❌ 不應該有：localStorage.setItem("openai_api_key", apiKey);
```

#### 3. 確認 HTML 設定

```html
<!-- frontend/index.html -->
<input type="password" <!-- ✅ 顯示星號 -- />
autocomplete="off"
<!-- ✅ 禁止自動填入 -->
id="openai-api-key" />
```

---

## 📊 測試結果表格

| 測試項目              | 預期行為 | 測試結果 |
| --------------------- | -------- | -------- |
| 輸入顯示星號          | `***`    | ✅       |
| 不儲存到 localStorage | `null`   | ✅       |
| 重新整理清除          | 空白     | ✅       |
| 關閉分頁清除          | 空白     | ✅       |
| 無 Key 基本分析       | 正常     | ✅       |
| 有 Key AI 增強        | 正常     | ✅       |
| 安全提示顯示          | 清楚     | ✅       |
| 多分頁獨立            | 獨立     | ✅       |
| autocomplete 禁用     | 不填入   | ✅       |
| 完整流程              | 順暢     | ✅       |

---

## ✅ 測試完成確認

完成以上所有測試後，確認：

- [x] ✅ 輸入時顯示星號（視覺安全）
- [x] ✅ 不儲存到 localStorage（資料安全）
- [x] ✅ 重新整理後清除（自動清除）
- [x] ✅ 關閉分頁後清除（完全清除）
- [x] ✅ 提示訊息清楚（使用者知情）
- [x] ✅ 基本功能不受影響（可選 AI）
- [x] ✅ AI 功能正常運作（有 Key 時）
- [x] ✅ 多分頁獨立（互不影響）
- [x] ✅ 禁止自動填入（額外安全）

**所有安全功能測試通過！可以部署到 Railway！** 🚀
