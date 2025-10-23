# 🚀 Railway 部署指南

## 📋 部署前檢查清單

### ✅ 已完成的優化

- ✅ **模型改為 gpt-4o-mini**（更快、更便宜）
- ✅ **Procfile 優化**（timeout 120 秒、2 workers）
- ✅ **railway.json 設定完成**
- ✅ **requirements.txt 完整**
- ✅ **Python 版本指定**（3.11.0）

### 📊 GPT-4o-mini 優勢

| 項目     | GPT-4o     | GPT-4o-mini    | 改進         |
| -------- | ---------- | -------------- | ------------ |
| 速度     | 中等       | 快             | ⚡ 2-3 倍快  |
| 輸入費用 | $2.50/1M   | $0.15/1M       | 💰 17 倍便宜 |
| 輸出費用 | $10/1M     | $0.60/1M       | 💰 17 倍便宜 |
| 單次分析 | $0.60-1.44 | **$0.04-0.09** | 💰 15 倍便宜 |
| 品質     | 最高       | 優秀           | ⭐ 足夠好    |

**結論**：gpt-4o-mini 非常適合生產環境！

---

## 🚀 部署步驟

### 方法 1：透過 GitHub（推薦）

#### 步驟 1：推送到 GitHub

```bash
cd /Users/tzustu/Desktop/程式開發/findseoproblem

# 初始化 git（如果還沒有）
git init

# 添加所有檔案
git add .

# 提交
git commit -m "SEO 分析工具 - AI 深度模式 (gpt-4o-mini)"

# 設定分支
git branch -M main

# 添加遠端倉庫（替換成您的 GitHub URL）
git remote add origin https://github.com/您的帳號/seo-analyzer.git

# 推送
git push -u origin main
```

#### 步驟 2：在 Railway 部署

1. **訪問 Railway**

   - 前往 https://railway.app
   - 登入或註冊帳號

2. **建立新專案**

   - 點擊「New Project」
   - 選擇「Deploy from GitHub repo」
   - 選擇您的 repository

3. **自動部署**

   - Railway 會自動：
     - ✅ 檢測 Python 專案
     - ✅ 讀取 `requirements.txt` 安裝依賴
     - ✅ 使用 `Procfile` 啟動應用
     - ✅ 分配網址

4. **等待部署完成**
   - 通常需要 2-3 分鐘
   - 完成後會顯示部署網址

### 方法 2：使用 Railway CLI

```bash
# 安裝 Railway CLI
npm i -g @railway/cli

# 登入
railway login

# 進入專案目錄
cd /Users/tzustu/Desktop/程式開發/findseoproblem

# 初始化 Railway 專案
railway init

# 部署
railway up
```

---

## ⚙️ Railway 設定說明

### 1. Procfile 設定

```
web: gunicorn app:app --timeout 120 --workers 2 --bind 0.0.0.0:$PORT
```

**參數說明**：

- `--timeout 120`：允許 120 秒處理時間（AI 深度模式需要 30-60 秒）
- `--workers 2`：2 個 worker 處理並發請求
- `--bind 0.0.0.0:$PORT`：綁定 Railway 提供的 PORT

### 2. railway.json 設定

```json
{
  "deploy": {
    "startCommand": "gunicorn app:app --timeout 120 --workers 2 --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**功能**：

- 自動重啟（失敗時）
- 最多重試 10 次

### 3. 環境變數

**不需要設定任何環境變數**！

因為：

- ✅ OpenAI API Key 由使用者在前端輸入
- ✅ PORT 由 Railway 自動設定
- ✅ 應用會自動讀取 `$PORT`

---

## 🌐 部署後使用

### 1. 獲取網址

部署完成後，Railway 會提供網址，例如：

```
https://seo-analyzer-production.up.railway.app
```

### 2. 訪問網站

使用者可以直接訪問這個網址：

- ✅ 看到 SEO 分析工具介面
- ✅ 輸入自己的 OpenAI API Key
- ✅ 開始分析網站

### 3. AI 深度模式運作

```
使用者輸入 API Key → 儲存在瀏覽器
    ↓
開始分析 → 12 項逐一處理
    ↓
每項立即 AI 增強 → 12 次獨立呼叫
    ↓
顯示完整結果
```

---

## 💰 費用估算（使用 gpt-4o-mini）

### Railway 費用

- **免費方案**：$0/月（有限制但夠用）
- **Hobby 方案**：$5/月（無限制）

### OpenAI 費用（由使用者支付）

- **深度模式（12 次呼叫）**：約 $0.04-0.09/次
- **100 次分析**：約 $4-9

**總成本對比**：

- GPT-4o：$5（Railway）+ $60-144（OpenAI）= $65-149/100 次
- **gpt-4o-mini**：$5（Railway）+ **$4-9**（OpenAI）= **$9-14/100 次**

💰 **節省 85% 的 AI 費用！**

---

## 🔧 部署後測試

### 1. 測試基本功能

訪問您的 Railway 網址，測試：

- ✅ 介面載入正常
- ✅ 輸入網址可以分析
- ✅ 12 項分析全部運作

### 2. 測試 AI 功能

- ✅ 展開 AI 設定區
- ✅ 輸入測試 API Key
- ✅ 測試連線
- ✅ 進行一次完整分析
- ✅ 確認 12 次 AI 呼叫都成功

### 3. 檢查日誌

在 Railway Dashboard：

- 點擊專案 → Deployments → Logs
- 應該看到：

  ```
  [1/12] 執行 TitleAnalyzer...
    ✓ 分析完成
    → AI 深度分析：title
    ✓ AI 增強完成

  [2/12] 執行 MetaAnalyzer...
    ✓ 分析完成
    → AI 深度分析：meta_tags
    ✓ AI 增強完成
  ```

---

## ⚠️ 注意事項

### 1. Timeout 設定

- ✅ 已設定 120 秒 timeout
- ✅ 足夠處理 AI 深度模式（30-60 秒）

### 2. 記憶體使用

- 基本分析：約 150MB
- AI 深度模式：約 200-250MB
- Railway 免費方案：512MB
- ✅ **足夠使用**

### 3. 並發處理

- 設定 2 個 workers
- 可同時處理 2 個請求
- ✅ **適合中小流量**

### 4. API Key 安全

- ✅ API Key 存在使用者瀏覽器
- ✅ 不儲存在伺服器
- ✅ 每次請求傳遞
- ✅ 安全性良好

---

## 📝 部署檢查清單

部署前確認：

- ✅ 所有檔案已提交到 Git
- ✅ `requirements.txt` 包含所有依賴
- ✅ `Procfile` 設定正確
- ✅ `railway.json` 設定完成
- ✅ 程式碼無語法錯誤

部署後確認：

- ✅ 網站可以訪問
- ✅ 12 項分析正常運作
- ✅ AI 功能可以使用
- ✅ 進度顯示正常

---

## 🎉 準備就緒

您的 SEO 分析工具已經完全準備好部署到 Railway！

**下一步**：

1. 推送程式碼到 GitHub
2. 在 Railway 建立專案
3. 等待自動部署完成
4. 開始使用！

**所有設定檔已優化完成！** 🚀
