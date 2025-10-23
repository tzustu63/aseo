"""
AI Enhancement Module

使用 OpenAI GPT-4o 模型提供 SEO 專家級建議
"""

from openai import OpenAI
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time


class SEOAIEnhancer:
    """SEO AI 增強器"""
    
    def __init__(self, api_key: str):
        """
        初始化 AI 增強器
        
        Args:
            api_key: OpenAI API Key
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # 使用 gpt-4o-mini（更快、更便宜，適合生產環境）
    
    def enhance_analysis(self, url: str, results: List[Dict[str, Any]], html_content: str = None) -> List[Dict[str, Any]]:
        """
        使用 AI 增強分析結果
        
        Args:
            url: 被分析的網址
            results: 原始分析結果
            html_content: 網頁的 HTML 內容（用於提取實際內容）
            
        Returns:
            增強後的分析結果
        """
        enhanced_results = []
        
        for result in results:
            try:
                # 為每個分類生成 AI 建議
                ai_suggestions = self._get_ai_suggestions(url, result, html_content)
                
                # 將 AI 建議添加到問題中
                enhanced_result = result.copy()
                enhanced_result['ai_enhanced'] = True
                
                if ai_suggestions:
                    enhanced_issues = []
                    for i, issue in enumerate(enhanced_result['issues']):
                        enhanced_issue = issue.copy()
                        if i < len(ai_suggestions):
                            enhanced_issue['ai_suggestion'] = ai_suggestions[i]
                        enhanced_issues.append(enhanced_issue)
                    enhanced_result['issues'] = enhanced_issues
                
                enhanced_results.append(enhanced_result)
            except Exception as e:
                print(f"AI 增強失敗 ({result.get('category')}): {e}")
                # 如果 AI 增強失敗，返回原始結果
                enhanced_results.append(result)
        
        return enhanced_results
    
    def enhance_single_category(self, url: str, category_result: Dict[str, Any], html_content: str = None) -> Dict[str, Any]:
        """
        為單一分類提供 AI 增強分析（深度模式）
        
        Args:
            url: 網址
            category_result: 單一分類的分析結果
            html_content: HTML 內容
            
        Returns:
            增強後的單一分類結果
        """
        try:
            print(f"  → AI 深度分析：{category_result.get('category', 'unknown')}")
            
            ai_suggestions = self._get_ai_suggestions(url, category_result, html_content)
            
            enhanced_result = category_result.copy()
            enhanced_result['ai_enhanced'] = True
            
            if ai_suggestions:
                enhanced_issues = []
                for i, issue in enumerate(enhanced_result['issues']):
                    enhanced_issue = issue.copy()
                    if i < len(ai_suggestions):
                        enhanced_issue['ai_suggestion'] = ai_suggestions[i]
                    enhanced_issues.append(enhanced_issue)
                enhanced_result['issues'] = enhanced_issues
            
            return enhanced_result
            
        except Exception as e:
            print(f"  ✗ AI 增強失敗: {e}")
            return category_result
    
    def enhance_multiple_categories_parallel(self, url: str, category_results: List[Dict[str, Any]], html_content: str = None, max_workers: int = 3) -> List[Dict[str, Any]]:
        """
        平行處理多個分類的 AI 增強（深度模式優化）
        
        Args:
            url: 網址
            category_results: 多個分類的分析結果列表
            html_content: HTML 內容
            max_workers: 最大平行數（2-4，預設 3）
            
        Returns:
            增強後的結果列表
        """
        print(f"\n🚀 啟動平行 AI 分析模式（同時處理 {max_workers} 項）...")
        start_time = time.time()
        
        enhanced_results = category_results.copy()
        
        # 只處理有問題的項目
        tasks = []
        for i, result in enumerate(category_results):
            if result.get('issues'):
                tasks.append((i, result))
        
        if not tasks:
            print("  ℹ️  無需 AI 分析的項目")
            return enhanced_results
        
        total_tasks = len(tasks)
        print(f"  📊 共 {total_tasks} 項需要 AI 分析")
        
        # 使用 ThreadPoolExecutor 平行執行
        completed_count = 0
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任務
            future_to_index = {
                executor.submit(
                    self.enhance_single_category,
                    url,
                    task[1],
                    html_content
                ): (task[0], task[1].get('category', 'unknown'))
                for task in tasks
            }
            
            # 收集結果
            for future in as_completed(future_to_index):
                index, category_name = future_to_index[future]
                try:
                    enhanced_result = future.result()
                    enhanced_results[index] = enhanced_result
                    completed_count += 1
                    progress = int((completed_count / total_tasks) * 100)
                    print(f"  ✓ [{completed_count}/{total_tasks}] {category_name} 完成 ({progress}%)")
                except Exception as e:
                    failed_count += 1
                    print(f"  ✗ [{completed_count + failed_count}/{total_tasks}] {category_name} 失敗: {e}")
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ 平行 AI 分析完成！")
        print(f"  ⏱️  總時間: {elapsed_time:.1f} 秒")
        print(f"  ✓ 成功: {completed_count} 項")
        if failed_count > 0:
            print(f"  ✗ 失敗: {failed_count} 項")
        print(f"  ⚡ 平均速度: {elapsed_time/total_tasks:.1f} 秒/項")
        
        return enhanced_results
    
    def _get_ai_suggestions(self, url: str, category_result: Dict[str, Any], html_content: str = None) -> List[str]:
        """
        使用 GPT-4o 生成特定分類的 SEO 專家建議
        
        Args:
            url: 網址
            category_result: 分類分析結果
            html_content: 網頁 HTML 內容
            
        Returns:
            AI 建議列表
        """
        category = category_result.get('category', '')
        issues = category_result.get('issues', [])
        
        if not issues:
            return []
        
        # 準備 prompt（傳入 HTML 內容）
        prompt = self._create_prompt(url, category, issues, html_content)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位資深的 SEO 技術顧問，擁有 10 年以上實戰經驗。

你的任務是：
1. 仔細分析使用者提供的「具體網站」和「實際問題」
2. 針對該網站的「實際內容」提供精確的修改建議
3. 每個建議都必須是「可直接執行」的具體指令，不能是籠統的理論

回應要求：
- 使用繁體中文
- 直接針對網站現況，不要講 SEO 通論
- 每個建議都要寫出「完整的」修改內容，不能只列出部分
- 如果有多個項目需要修改，必須「全部列出」，不能省略
- 提供「具體的修改前後對照」
- 說明「為什麼要這樣改」以及「改了會有什麼具體效果」"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2500,  # 平行處理後可以提供更詳細的建議
                timeout=15  # 平行處理後單項可用更多時間
            )
            
            # 解析回應
            suggestions_text = response.choices[0].message.content.strip()
            suggestions = self._parse_suggestions(suggestions_text, len(issues))
            
            return suggestions
            
        except Exception as e:
            error_msg = str(e)
            if 'timeout' in error_msg.lower():
                print(f"OpenAI API 超時（超過 8 秒）: {e}")
            else:
                print(f"OpenAI API 呼叫失敗: {e}")
            return []
    
    def _create_prompt(self, url: str, category: str, issues: List[Dict], html_content: str = None) -> str:
        """創建給 GPT-4o 的 prompt，包含實際網頁內容"""
        from bs4 import BeautifulSoup
        
        category_names = {
            'title': '標題標籤 (Title Tag)',
            'meta_tags': 'Meta 標籤',
            'headings': '標題結構 (H1-H6)',
            'images': '圖片優化',
            'keywords': '關鍵字優化',
            'structure': 'HTML 結構',
            'performance': '網站效能',
            'mobile': '行動裝置友善性',
            'core_web_vitals': 'Core Web Vitals',
            'structured_data': '結構化資料',
            'links': '連結優化',
            'crawlability': '可爬性'
        }
        
        category_name = category_names.get(category, category)
        
        # 提取實際網頁內容
        actual_content = self._extract_actual_content(html_content, category) if html_content else {}
        
        prompt = f"""我正在分析這個網站：{url}

分析類別：{category_name}

系統檢測到以下具體問題：
"""
        
        for i, issue in enumerate(issues, 1):
            prompt += f"\n問題 {i}：{issue.get('message', '')}"
            if issue.get('severity'):
                prompt += f"\n嚴重程度：{issue.get('severity')}"
            if issue.get('current_value'):
                prompt += f"\n目前狀態：{issue.get('current_value')}"
            if issue.get('suggestion'):
                prompt += f"\n基本建議：{issue.get('suggestion')}"
            prompt += "\n"
        
        # 添加實際網頁內容
        if actual_content:
            prompt += "\n【網頁實際內容】\n"
            for key, value in actual_content.items():
                if value:
                    prompt += f"\n{key}：\n{value}\n"
        
        prompt += f"""
---

請以資深 SEO 顧問的身份，針對「{url}」這個網站的實際狀況，為每個問題提供「極度具體」的修改建議。

⚠️ 重要要求（必須嚴格遵守）：

1. **使用上方提供的「網頁實際內容」**
   - 例如：如果提供了「目前的 Title 標籤：首頁」，就要寫「目前是『首頁』，建議改為『...』」
   - 例如：如果提供了「缺少 alt 的圖片完整清單」，就要針對清單中的「每一張圖片」提供具體建議
   - 絕對不能用假設的內容（如「假設是產品 A」、「例如 image1.jpg」）

2. **完整列出所有項目，不能省略**
   - 如果有 5 張圖片，就要給出全部 5 張的具體建議
   - 如果有 10 個連結，就要列出全部 10 個
   - 不能只給 2-3 個範例後說「其他類推」

3. **提供修改前後完整對照**
   - 必須寫出「修改前」的實際內容（從上方提供的資料中取得）
   - 必須寫出「修改後」的完整內容（不能只說「應該包含...」）
   - 格式：修改前：(實際內容) → 修改後：(完整建議)

4. **每個建議的結構**：
   【為什麼對這個網站重要】：基於實際狀況分析影響
   【具體修改內容】：逐一列出，使用實際的檔名、文字、程式碼
   【修改原因】：說明每個修改的技術原因
   【預期效果】：針對這個網站的具體改善（可量化）

5. **絕對禁止**：
   ❌ 使用「假設」、「例如」、「等」
   ❌ 只列出部分後說「其他類似」
   ❌ 給出籠統的建議而非實際修改內容
   ❌ 使用不是網頁中實際存在的範例

回應格式：
每個問題的建議用「---」分隔，嚴格按照問題順序回應。
使用上方提供的實際內容，務必具體、完整、可直接執行。"""
        
        return prompt
    
    def _extract_actual_content(self, html_content: str, category: str) -> Dict[str, str]:
        """提取網頁的實際內容供 AI 分析"""
        from bs4 import BeautifulSoup
        
        if not html_content:
            return {}
        
        soup = BeautifulSoup(html_content, 'html.parser')
        content = {}
        
        try:
            if category == 'title':
                # 提取實際的 title 內容
                title = soup.find('title')
                content['目前的 Title 標籤'] = title.get_text().strip() if title else '(無)'
            
            elif category == 'meta_tags':
                # 提取實際的 meta 標籤
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                content['目前的 Meta Description'] = meta_desc.get('content', '(無)') if meta_desc else '(無)'
                
                og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
                if og_tags:
                    content['現有的 Open Graph 標籤'] = '\n'.join([f"  - {tag.get('property')}: {tag.get('content', '')[:50]}" for tag in og_tags[:5]])
            
            elif category == 'headings':
                # 提取實際的標題
                h1_tags = soup.find_all('h1')
                if h1_tags:
                    content['目前的 H1 標籤'] = '\n'.join([f"  - {h1.get_text().strip()[:100]}" for h1 in h1_tags[:5]])
                
                h2_tags = soup.find_all('h2')
                if h2_tags:
                    content['目前的 H2 標籤（前 5 個）'] = '\n'.join([f"  - {h2.get_text().strip()[:100]}" for h2 in h2_tags[:5]])
            
            elif category == 'images':
                # 提取所有圖片的實際資訊
                images = soup.find_all('img')
                images_without_alt = [img for img in images if not img.get('alt') or not img.get('alt').strip()]
                
                if images_without_alt:
                    content['缺少 alt 的圖片（完整清單）'] = '\n'.join([
                        f"  {i+1}. src=\"{img.get('src', '未知')}\" → 目前 alt=\"{img.get('alt', '')}\"" 
                        for i, img in enumerate(images_without_alt[:20])  # 最多列出 20 個
                    ])
                    if len(images_without_alt) > 20:
                        content['缺少 alt 的圖片（完整清單）'] += f"\n  ... 還有 {len(images_without_alt) - 20} 張圖片"
            
            elif category == 'keywords':
                # 提取實際的文字內容
                # 移除 script 和 style
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                # 清理空白
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                content['網頁實際文字內容（前 500 字）'] = text[:500]
                content['總字數'] = str(len(text))
            
            elif category == 'links':
                # 提取實際的連結
                links = soup.find_all('a', href=True)
                
                # 空白錨點文字的連結
                empty_links = [link for link in links if not link.get_text().strip()]
                if empty_links:
                    content['缺少錨點文字的連結（完整清單）'] = '\n'.join([
                        f"  {i+1}. href=\"{link.get('href', '')}\" → 目前文字：(空白)"
                        for i, link in enumerate(empty_links[:15])
                    ])
                
                # 外部連結缺少安全屬性
                external_links = [link for link in links if link.get('href', '').startswith('http')]
                unsafe_links = []
                for link in external_links:
                    rel = link.get('rel', [])
                    if not any(r in ['noopener', 'noreferrer'] for r in (rel if isinstance(rel, list) else [rel])):
                        unsafe_links.append(link)
                
                if unsafe_links:
                    content['缺少安全屬性的外部連結（完整清單）'] = '\n'.join([
                        f"  {i+1}. href=\"{link.get('href', '')[:60]}\" text=\"{link.get_text().strip()[:30]}\""
                        for i, link in enumerate(unsafe_links[:15])
                    ])
            
            elif category == 'structured_data':
                # 提取現有的結構化資料
                jsonld_scripts = soup.find_all('script', type='application/ld+json')
                if jsonld_scripts:
                    content['現有的 JSON-LD'] = f"共 {len(jsonld_scripts)} 個"
                else:
                    content['現有的 JSON-LD'] = '無'
                
                og_title = soup.find('meta', property='og:title')
                content['現有的 og:title'] = og_title.get('content', '(無)') if og_title else '(無)'
        
        except Exception as e:
            print(f"提取實際內容失敗: {e}")
        
        return content
    
    def _parse_suggestions(self, suggestions_text: str, num_issues: int) -> List[str]:
        """解析 AI 回應的建議"""
        
        # 嘗試以 --- 分隔
        suggestions = suggestions_text.split('---')
        suggestions = [s.strip() for s in suggestions if s.strip()]
        
        # 如果分隔不成功，嘗試按編號分隔
        if len(suggestions) < num_issues:
            lines = suggestions_text.split('\n')
            current_suggestion = []
            suggestions = []
            
            for line in lines:
                line = line.strip()
                # 檢查是否是新的編號項目
                if line and (line[0].isdigit() and '.' in line[:3]):
                    if current_suggestion:
                        suggestions.append('\n'.join(current_suggestion))
                    current_suggestion = [line]
                elif line:
                    current_suggestion.append(line)
            
            if current_suggestion:
                suggestions.append('\n'.join(current_suggestion))
        
        # 確保建議數量不超過問題數量
        return suggestions[:num_issues]


def test_openai_key(api_key: str) -> Dict[str, Any]:
    """
    測試 OpenAI API Key 是否有效
    
    Args:
        api_key: OpenAI API Key
        
    Returns:
        測試結果
    """
    if not api_key or not api_key.startswith('sk-'):
        return {
            'success': False,
            'message': 'API Key 格式錯誤（應以 sk- 開頭）'
        }
    
    try:
        client = OpenAI(api_key=api_key)
        
        # 簡單的測試呼叫
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=5
        )
        
        return {
            'success': True,
            'message': 'API Key 有效，GPT-4o-mini 模型可用（已針對 SEO 分析優化）'
        }
        
    except Exception as e:
        error_str = str(e).lower()
        
        if 'authentication' in error_str or 'invalid' in error_str or 'incorrect api key' in error_str:
            return {
                'success': False,
                'message': 'API Key 無效或已過期'
            }
        elif 'rate' in error_str or 'quota' in error_str:
            return {
                'success': False,
                'message': 'API 額度不足，請充值或檢查付款方式'
            }
        elif 'model' in error_str:
            return {
                'success': False,
                'message': 'GPT-4o-mini 模型不可用，請確認您的帳號權限'
            }
        else:
            return {
                'success': False,
                'message': f'測試失敗：{str(e)[:100]}'
            }

