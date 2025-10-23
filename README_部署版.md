# 🔍 SEO 網頁分析工具

專業的 SEO 分析工具，支援 12 項深度檢測 + AI 智能增強分析

## ✨ 功能特色

### 12 項專業 SEO 分析

1. ✅ **標題標籤** (Title Tag)
2. ✅ **Meta 標籤** (Description, OG, Twitter)
3. ✅ **標題結構** (H1-H6 層級)
4. ✅ **圖片優化** (Alt 文字、尺寸)
5. ✅ **關鍵字** (密度、內容長度)
6. ✅ **HTML 結構** (語意化標籤)
7. ✅ **效能指標** (檔案大小、Script)
8. ✅ **行動裝置** (Viewport、字體)
9. ✅ **Core Web Vitals** (LCP/FID/CLS)
10. ✅ **結構化資料** (JSON-LD, Schema.org)
11. ✅ **連結分析** (內部/外部連結)
12. ✅ **可爬性** (Robots.txt, Sitemap)

### 🤖 AI 深度分析模式

- ✅ **GPT-4o-mini 驅動**：快速且經濟
- ✅ **12 次獨立分析**：每項專注深入
- ✅ **使用實際內容**：基於網站真實數據
- ✅ **完整列出項目**：不省略任何修改
- ✅ **即時進度顯示**：清楚了解處理狀態

## 🚀 快速開始

### 線上使用（推薦）

訪問部署網址：

```
https://your-project.up.railway.app
```

1. 輸入要分析的網址
2. （可選）展開 AI 設定區，輸入 OpenAI API Key
3. 點擊「開始分析」
4. 查看詳細的 SEO 報告

### 本地運行

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動應用
python app.py

# 訪問
http://localhost:8000
```

## 💰 費用說明

### 基本分析

- 🆓 **完全免費**
- ⚡ 快速（2-5 秒）
- 📊 12 項專業檢測

### AI 深度分析

- 💰 **$0.04-0.09/次**（使用 gpt-4o-mini）
- 🤖 12 次獨立 AI 呼叫
- ⏱️ 約 30-60 秒
- 🎯 極度具體的建議

**成本優勢**：

- gpt-4o-mini 比 gpt-4o 便宜 **17 倍**
- 深度模式（12 次）也只需 $0.04-0.09

## 🛠️ 技術架構

### 後端

- **Flask** - Web 框架
- **BeautifulSoup4** - HTML 解析
- **OpenAI** - AI 增強分析
- **Gunicorn** - 生產環境伺服器

### 前端

- **純 JavaScript** - 無框架依賴
- **現代化 CSS** - 響應式設計
- **即時進度** - 使用者友善

### 部署

- **Railway** - 雲端平台
- **自動化部署** - Git push 即部署
- **HTTPS** - 自動配置

## 📊 AI 深度模式運作方式

```
輸入網址：https://example.com
    ↓
[1/12] 分析標題 → 發現問題 → AI 專注分析標題 → 獲得建議
[2/12] 分析 Meta → 發現問題 → AI 專注分析 Meta → 獲得建議
[3/12] 分析標題結構 → 無問題 → 跳過 AI
[4/12] 分析圖片 → 發現 5 張缺 alt → AI 列出全部 5 張的建議
...
[12/12] 分析可爬性 → 發現問題 → AI 專注分析 → 獲得建議
    ↓
顯示完整結果（含所有 AI 建議）
```

## 🎯 AI 建議範例

### 圖片優化（獨立分析）

**系統檢測**：

```
3 張圖片缺少 alt 文字
```

**AI 建議**（基於實際檔名）：

```
【具體修改內容 - 全部 3 張】

1. /images/hero-banner.jpg
   修改前：<img src="/images/hero-banner.jpg" alt="">
   修改後：<img src="/images/hero-banner.jpg" alt="SEO 分析工具首頁橫幅 - 專業團隊">

2. /products/seo-tool.jpg
   修改前：<img src="/products/seo-tool.jpg" alt="">
   修改後：<img src="/products/seo-tool.jpg" alt="SEO 分析工具產品展示 - 12項檢測功能">

3. /company-logo.png
   修改前：<img src="/company-logo.png" alt="">
   修改後：<img src="/company-logo.png" alt="YourCompany 公司標誌">

【為什麼要這樣改】
（針對每個圖片的具體原因）

【預期效果】
1. Google 圖片搜尋流量提升 40-60%
2. 可訪問性評分改善
3. 符合 WCAG 2.1 標準
```

## 🔒 安全性

- ✅ **API Key 安全**：存在使用者瀏覽器，不存伺服器
- ✅ **HTTPS**：Railway 自動配置
- ✅ **CORS 設定**：正確的跨域設定
- ✅ **無資料收集**：完全隱私

## 📚 文檔

- `RAILWAY_部署指南.md` - 完整部署說明
- `深度分析模式說明.md` - AI 深度模式詳解
- `AI_實際內容分析說明.md` - 內容提取機制
- `系統檢查報告.md` - 功能測試報告

## 🎉 準備部署

```bash
# 執行部署腳本
./deploy-to-railway.sh
```

或手動部署：

1. 推送到 GitHub
2. 在 Railway 連接 repo
3. 自動部署完成

---

**立即體驗專業級 SEO 分析 + AI 智能建議！** 🚀

## 📞 支援

- 所有 12 項分析器測試通過
- AI 深度模式完全運作
- Railway 部署設定完成
- 生產環境就緒

**版本**：v2.0 (AI 深度模式)
**最後更新**：2024-10-24
