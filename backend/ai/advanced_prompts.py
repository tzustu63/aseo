"""
Advanced AI Prompts

專門為重大內容變更設計的進階 AI prompt 模板
"""

class AdvancedPrompts:
    """進階 AI Prompt 模板"""
    
    H1_OPTIMIZATION = """你是專業的 SEO 內容優化師。

任務：優化文章的 H1 主標題

原始 H1：{current_h1}
文章內容摘要：{content_summary}
主要關鍵字：{keywords}

要求：
1. 新 H1 必須準確反映文章主題
2. 自然包含主要關鍵字
3. 60 字元以內（中文約 30 字）
4. 吸引點擊但不誇大
5. 符合 SEO 最佳實踐
6. 保持專業和可信度

請以 JSON 格式回傳：
{{
    "new_h1": "優化後的 H1 標題",
    "reasoning": "為什麼這樣改（簡短說明）",
    "seo_impact": "預期 SEO 影響",
    "keywords_used": ["關鍵字1", "關鍵字2"]
}}

只回傳 JSON，不要其他說明。"""

    KEYWORD_DENSITY = """你是專業的 SEO 內容優化師。

任務：優化段落的關鍵字密度

原始段落：
{original_paragraph}

目標關鍵字：{keywords}
當前關鍵字出現次數：{current_count} 次
段落總字數：{word_count} 字
當前密度：{current_density}%
建議密度：1-2%

要求：
1. 保持原始訊息和意義完全不變
2. 自然融入關鍵字，達到 1-2% 密度
3. 語句流暢自然，不生硬
4. 保留所有重要資訊（數據、引用、人名、地名）
5. 不改變語氣、風格和專業度
6. 不加入無關內容

請以 JSON 格式回傳：
{{
    "optimized_paragraph": "優化後的段落",
    "keyword_count": 關鍵字出現次數,
    "new_density": 新的密度百分比,
    "changes_made": ["變更說明1", "變更說明2"]
}}

只回傳 JSON，不要其他說明。"""

    HEADING_STRUCTURE = """你是 SEO 結構專家。

任務：修正文章的標題結構層級

當前 HTML 結構：
{current_html}

當前問題：{problem_description}

要求：
1. 確保整篇文章只有一個 H1
2. 標題層級正確（H1→H2→H3，不跳級）
3. 保持所有文字內容完全不變
4. 只調整標題標籤的層級（<h1>, <h2>, <h3>, etc.）
5. 保持標題的原始順序
6. 不刪除任何內容

請以 JSON 格式回傳：
{{
    "fixed_html": "修正後的 HTML（只包含標題部分）",
    "changes": [
        {{"from": "h3", "to": "h2", "title": "標題文字"}},
        ...
    ],
    "explanation": "修正說明"
}}

只回傳 JSON，不要其他說明。"""

    CONTENT_REWRITE = """你是專業的內容優化師和 SEO 專家。

任務：優化段落內容，改善 SEO 和可讀性

原始段落：
{original_paragraph}

優化目標：{optimization_goals}
目標關鍵字：{keywords}
語氣風格：{tone}

要求：
1. 保持核心訊息和意義
2. 改善可讀性和結構
3. 自然融入關鍵字（密度 1-2%）
4. 保留所有重要資訊：
   - 數據和統計
   - 引用來源
   - 專有名詞
   - 連結
5. 優化句子結構（不要過長或過短）
6. 保持原始語氣和專業度
7. 不添加未經證實的資訊

請以 JSON 格式回傳：
{{
    "optimized_content": "優化後的段落",
    "key_improvements": ["改善點1", "改善點2"],
    "preserved_elements": ["保留的重要資訊1", "保留的重要資訊2"],
    "seo_enhancements": "SEO 改善說明",
    "readability_score": "改善前後可讀性評分"
}}

只回傳 JSON，不要其他說明。"""

    @staticmethod
    def get_prompt(prompt_type: str, **kwargs) -> str:
        """
        取得並填充 prompt 模板
        
        Args:
            prompt_type: Prompt 類型（h1, keyword_density, heading_structure, content_rewrite）
            **kwargs: 要填充的變數
            
        Returns:
            填充後的 prompt
        """
        prompts = {
            'h1': AdvancedPrompts.H1_OPTIMIZATION,
            'keyword_density': AdvancedPrompts.KEYWORD_DENSITY,
            'heading_structure': AdvancedPrompts.HEADING_STRUCTURE,
            'content_rewrite': AdvancedPrompts.CONTENT_REWRITE
        }
        
        template = prompts.get(prompt_type)
        if not template:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required parameter: {e}")

