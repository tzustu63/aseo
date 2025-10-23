# 🚀 快速啟動指南

## 現在就開始使用！

### 步驟 1：啟動應用程式

應用程式已經在運行中！開啟瀏覽器訪問：

```
http://localhost:8000
```

### 步驟 2：分析第一個網站

1. 在輸入框輸入任意網址，例如：`https://www.tcu.edu.tw`
2. 點擊「開始分析」
3. 等待 5-10 秒查看結果

### 步驟 3：（選用）設定 WordPress 自動修復

如果您想要使用一鍵修復功能：

#### A. 在 WordPress 後台產生 Application Password

1. 登入您的 WordPress 網站後台
2. 前往「使用者」→「個人資料」
3. 捲動到最下方找到「應用程式密碼」
4. 輸入名稱：`SEO Analyzer`
5. 點擊「新增」
6. **複製產生的密碼**（格式：`xxxx xxxx xxxx xxxx`）

#### B. 在 SEO 工具中設定

1. 點擊「🔧 WordPress 自動修復設定（選用）」展開
2. 填入：
   - WordPress 網址：`https://your-site.com`
   - 使用者名稱：您的 WordPress 帳號
   - Application Password：剛才複製的密碼
3. 點擊「測試連線」確認設定正確
4. 點擊「儲存設定」

### 步驟 4：開始修復 SEO 問題！

1. 分析完成後，查看問題列表
2. 每個問題旁邊會有按鈕：
   - **🔧 修復**：技術問題，點擊即可修復
   - **🤖 AI 優化**：內容優化，AI 自動產生改善內容
   - **ℹ️ 需人工處理**：重大變更，需手動處理
3. 點擊「修復」或「AI 優化」按鈕
4. 查看修復預覽
5. 確認無誤後點擊「確認套用」
6. 完成！✅

---

## 🎯 使用範例

### 情境 1：修復缺少 viewport 標籤

```
1. 分析發現：「缺少 viewport meta 標籤」
2. 問題旁顯示「🔧 修復」按鈕
3. 點擊按鈕
4. 預覽顯示要加入的標籤：
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
5. 點擊「確認套用」
6. ✅ 完成！
```

### 情境 2：優化 Meta Description

```
1. 分析發現：「Meta description 太短（85 字元）」
2. 問題旁顯示「🤖 AI 優化」按鈕
3. 點擊按鈕
4. AI 自動產生優化版本（150-160 字元）
5. 預覽顯示：
   修復前：「本公司提供優質服務」
   修復後：「專業團隊提供一站式解決方案，從諮詢、規劃到執行...」
6. 不滿意？點擊「🔄 重新產生」
7. 滿意後點擊「確認套用」
8. ✅ 完成！
```

### 情境 3：批量修復多個圖片 alt

```
1. 分析發現：10 張圖片缺少 alt 屬性
2. 逐一點擊每個問題的「🤖 AI 優化」按鈕
3. AI 根據圖片檔名和上下文產生 alt 文字
4. 逐一確認並套用
5. ✅ 完成所有修復！
```

---

## ⚙️ （選用）設定 OpenAI API

如果要使用 AI 功能：

1. 前往 [OpenAI Platform](https://platform.openai.com/)
2. 建立 API Key
3. 設定環境變數：

```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

4. 重新啟動應用程式

**注意**：即使不設定 OpenAI API，工具仍然完全可用，只是不會有 AI 優化功能。

---

## 🛠️ 常用命令

### 啟動應用程式

```bash
cd "/Users/tzustu/Desktop/程式開發/findseoproblem"
python app.py
```

### 停止應用程式

按 `Ctrl + C`

### 重新安裝依賴

```bash
python3 -m pip install --user -r requirements.txt
```

### 清除 Port 8000 佔用

```bash
lsof -ti:8000 | xargs kill -9
```

---

## 📖 更多資訊

- [README.md](README.md) - 完整的專案說明
- [USAGE.md](USAGE.md) - 詳細使用手冊
- [OpenSpec 提案](openspec/changes/add-gpt5-wordpress-auto-fix/) - 技術設計文件

---

## 🎊 開始使用吧！

現在開啟瀏覽器訪問：

**http://localhost:8000**

輸入任何網址，立即開始 SEO 分析！🚀
