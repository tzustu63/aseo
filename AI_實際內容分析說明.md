# 🎯 AI 實際內容分析功能說明

## ✅ 最新優化：使用網頁真實內容

### 核心改進

系統現在會：

1. ✅ **提取網頁的實際內容**（真實的圖片檔名、文字、連結等）
2. ✅ **傳遞給 AI 分析**
3. ✅ **AI 基於真實內容提供建議**（不再使用假設或範例）

## 📊 實際內容提取項目

### 1. 標題標籤 (Title)

```
提取：目前的 Title 標籤實際內容
例如：「首頁」、「Google」等真實文字
```

### 2. Meta 標籤

```
提取：
- 目前的 Meta Description 實際內容
- 現有的 Open Graph 標籤列表
```

### 3. 標題結構 (Headings)

```
提取：
- 所有 H1 標籤的實際文字
- 前 5 個 H2 標籤的實際文字
```

### 4. 圖片優化 ⭐ 重點

```
提取：缺少 alt 的圖片完整清單
格式：
  1. src="product-a.jpg" → 目前 alt=""
  2. src="product-b.jpg" → 目前 alt=""
  3. src="company-logo.jpg" → 目前 alt=""
  ... (全部列出，最多 20 個)
```

### 5. 關鍵字 ⭐ 重點

```
提取：
- 網頁實際文字內容（前 500 字）
- 總字數

例如：
網頁實際文字內容：「歡迎來到我們的網站，我們提供專業的 SEO 分析服務...」
總字數：52
```

### 6. 連結分析 ⭐ 重點

```
提取：
- 缺少錨點文字的連結完整清單
  格式：href="..." → 目前文字：(空白)

- 缺少安全屬性的外部連結完整清單
  格式：href="https://..." text="連結文字"
```

### 7. 結構化資料

```
提取：
- 現有的 JSON-LD 數量
- 現有的 og:title 內容
```

## 🎯 AI 如何使用這些實際內容

### 範例 1：圖片 Alt 文字

**系統提取到的實際內容**：

```
缺少 alt 的圖片（完整清單）：
  1. src="/images/hero-banner.jpg" → 目前 alt=""
  2. src="/products/stainless-steel-pot.jpg" → 目前 alt=""
  3. src="/about/company-logo.png" → 目前 alt=""
```

**AI 會產生（基於實際檔名）**：

```
【具體修改內容】

1. /images/hero-banner.jpg
   修改前：<img src="/images/hero-banner.jpg" alt="">
   修改後：<img src="/images/hero-banner.jpg" alt="首頁橫幅 - 專業廚具品牌形象">

2. /products/stainless-steel-pot.jpg
   修改前：<img src="/products/stainless-steel-pot.jpg" alt="">
   修改後：<img src="/products/stainless-steel-pot.jpg" alt="不鏽鋼鍋產品展示 - 高品質廚具">

3. /about/company-logo.png
   修改前：<img src="/about/company-logo.png" alt="">
   修改後：<img src="/about/company-logo.png" alt="YKSC 廚具公司標誌">
```

**不會產生（假設內容）**：

```
❌ 假設這三張圖片分別是產品展示圖片...
❌ 圖片 1（假設是產品 A）...
❌ 例如 image1.jpg、image2.jpg 等...
```

### 範例 2：網頁內容過少

**系統提取到的實際內容**：

```
網頁實際文字內容（前 500 字）：
「首頁 關於我們 聯絡我們 歡迎光臨 YKSC 專業廚具 優質產品」

總字數：52
```

**AI 會產生**：

```
【為什麼對這個網站重要】
您的網站目前只有 52 個字的內容，實際文字是「首頁 關於我們 聯絡我們 歡迎光臨 YKSC 專業廚具 優質產品」，
主要都是導航選單和簡短標語，沒有實質內容。Google 會認為這是低品質頁面。

【具體修改內容】
目前內容（52 字）：
「首頁 關於我們 聯絡我們 歡迎光臨 YKSC 專業廚具 優質產品」

建議擴充為（約 350 字）：
「歡迎光臨 YKSC 專業廚具

【關於 YKSC】
YKSC 是台灣領先的專業廚具品牌，自 2010 年成立以來，致力於為餐飲業者和家庭提供高品質的廚房設備。
我們的產品包括不鏽鋼鍋具、專業烤箱、廚房工作台等，全系列通過 ISO 9001 品質認證。

【我們的優勢】
- 專業級品質：採用 304 不鏽鋼材質，耐用度高
- 完整售後服務：提供 2 年保固和終身維修服務
- 客製化方案：可根據廚房空間設計專屬配置
- 快速交貨：台灣本地製造，3-5 天快速到貨

【服務範圍】
我們服務全台灣，包含台北、台中、高雄等主要城市，並提供到府安裝服務。
無論您是餐廳經營者、飯店廚房，或是追求品質的家庭使用者，YKSC 都能提供最適合的解決方案。

立即聯絡我們，讓專業團隊為您規劃完善的廚房設備！」

【修改原因】
- 加入品牌故事和專業背景（建立信任感）
- 說明產品特色和優勢（回答使用者疑問）
- 包含目標關鍵字：專業廚具、不鏽鋼鍋、烤箱、台灣（符合搜尋意圖）
- 加入服務範圍和 CTA（提高轉換率）

【預期效果】
1. Google 會開始索引並給予較高排名（從幾乎不排名到進入前 50）
2. 搜尋「台灣專業廚具」、「不鏽鋼鍋」等關鍵字時有機會出現
3. 使用者停留時間從 5 秒提升到 30-60 秒
4. 跳出率從 90% 降低到 50-60%
```

**對比**：

- ❌ 舊方式：「內容太少，建議增加到 300-500 字」（沒說要寫什麼）
- ✅ 新方式：列出目前的 52 字是什麼，然後給出完整的 350 字建議內容

## 🔧 技術實現

### 步驟 1：分析時保存 HTML

```python
# app.py
html_content = response.text  # 保存完整 HTML
```

### 步驟 2：傳遞給 AI 增強器

```python
results_dict = ai_enhancer.enhance_analysis(
    url,
    results_dict,
    html_content  # 傳遞實際 HTML
)
```

### 步驟 3：提取實際內容

```python
# ai_enhancement.py
def _extract_actual_content(html_content, category):
    soup = BeautifulSoup(html_content, 'html.parser')

    if category == 'images':
        # 提取所有缺少 alt 的圖片
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]

        # 回傳實際的 src 清單
        return {
            '缺少 alt 的圖片（完整清單）':
            '\n'.join([f"{i+1}. src=\"{img.get('src')}\"" for i, img in enumerate(images_without_alt)])
        }
```

### 步驟 4：將實際內容加入 Prompt

```python
prompt += """
【網頁實際內容】
缺少 alt 的圖片（完整清單）：
  1. src="/images/hero-banner.jpg" → 目前 alt=""
  2. src="/products/pot.jpg" → 目前 alt=""
  3. src="/about/logo.png" → 目前 alt=""
"""
```

### 步驟 5：AI 使用實際內容生成建議

- ✅ AI 看到實際的檔名
- ✅ AI 基於檔名推測內容
- ✅ AI 給出針對每個實際檔案的具體建議

## 📝 完整範例

### 輸入：分析 https://example.com

### 系統檢測到：

```
問題：3 張圖片缺少 alt
```

### 系統提取實際內容：

```
缺少 alt 的圖片（完整清單）：
  1. src="/hero-banner.jpg" → 目前 alt=""
  2. src="/product-steel-pot.jpg" → 目前 alt=""
  3. src="/logo.png" → 目前 alt=""
```

### GPT-4o 收到的 Prompt：

```
網址：https://example.com
問題：3 張圖片缺少 alt

【網頁實際內容】
缺少 alt 的圖片（完整清單）：
  1. src="/hero-banner.jpg" → 目前 alt=""
  2. src="/product-steel-pot.jpg" → 目前 alt=""
  3. src="/logo.png" → 目前 alt=""

請針對這「3張實際圖片」提供具體建議，
不能用假設內容，要全部列出。
```

### AI 產出：

```
【具體修改內容 - 全部 3 張圖片】

1. /hero-banner.jpg（首頁橫幅）
   修改前：<img src="/hero-banner.jpg" alt="">
   修改後：<img src="/hero-banner.jpg" alt="YKSC 專業廚具 - 高品質不鏽鋼鍋具展示">
   原因：從檔名判斷是橫幅圖，應突出品牌和主要產品

2. /product-steel-pot.jpg（產品圖）
   修改前：<img src="/product-steel-pot.jpg" alt="">
   修改後：<img src="/product-steel-pot.jpg" alt="304 不鏽鋼湯鍋 - 專業級廚房用具">
   原因：檔名包含 steel-pot，應詳細描述產品特性

3. /logo.png（公司標誌）
   修改前：<img src="/logo.png" alt="">
   修改後：<img src="/logo.png" alt="YKSC 專業廚具公司標誌">
   原因：logo 應包含公司名稱，提升品牌識別
```

## 🎉 現在的完整流程

1. **使用者輸入網址** → `https://example.com`

2. **系統爬取並分析** →

   - 檢測到 3 張圖片缺少 alt
   - 提取實際檔名：hero-banner.jpg、product-steel-pot.jpg、logo.png

3. **傳遞給 GPT-4o** →

   - 提供實際的 3 個檔名
   - 要求針對這 3 個具體圖片提供建議

4. **AI 分析並回應** →

   - 基於檔名（hero-banner、product-steel-pot、logo）推測用途
   - 給出針對每個檔案的具體 alt 文字建議
   - 完整列出全部 3 個，不省略

5. **顯示給使用者** →
   - 使用者看到的是「真實檔名」的修改建議
   - 可以直接複製程式碼使用
   - 不會看到「假設」或「例如」等字眼

## ⚡ 與之前的對比

### 之前（沒有實際內容）

```
AI Prompt：
「有圖片缺少 alt，請提供建議」

AI 回應：
❌ 假設這三張圖片分別是產品展示圖片...
❌ 圖片 1（假設是產品 A）...
❌ 例如 image1.jpg、image2.jpg 等...
```

### 現在（有實際內容）

```
AI Prompt：
「有 3 張圖片缺少 alt

【網頁實際內容】
缺少 alt 的圖片（完整清單）：
  1. src="/hero-banner.jpg" → 目前 alt=""
  2. src="/product-steel-pot.jpg" → 目前 alt=""
  3. src="/logo.png" → 目前 alt=""

請針對這 3 張實際圖片，全部列出具體建議」

AI 回應：
✅ 1. /hero-banner.jpg
   修改前：<img src="/hero-banner.jpg" alt="">
   修改後：<img src="/hero-banner.jpg" alt="YKSC...">

✅ 2. /product-steel-pot.jpg
   修改前：<img src="/product-steel-pot.jpg" alt="">
   修改後：<img src="/product-steel-pot.jpg" alt="304 不鏽鋼...">

✅ 3. /logo.png
   修改前：<img src="/logo.png" alt="">
   修改後：<img src="/logo.png" alt="YKSC 公司標誌">
```

## 🚀 立即體驗

1. **重新整理瀏覽器**（Cmd+Shift+R）
2. **展開 AI 設定區**
3. **輸入 API Key 並儲存**
4. **分析任何網站**

您現在會看到：

- ✅ 基於網站「實際檔名」的圖片 alt 建議
- ✅ 基於「實際文字內容」的內容擴充建議
- ✅ 基於「實際連結」的錨點文字建議
- ✅ 完整列出所有項目，不省略

**現在 AI 真正在分析您的網站實際內容，而不是給假設範例！** 🎉
