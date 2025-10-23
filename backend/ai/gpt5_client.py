"""
OpenAI GPT Client

提供 OpenAI API 的封裝，支援內容分析和生成
"""
import os
import json
from typing import Dict, Any, Optional
from .advanced_prompts import AdvancedPrompts

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class GPT5Client:
    """OpenAI GPT API 客戶端"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        初始化 GPT 客戶端
        
        Args:
            api_key: OpenAI API 金鑰（若未提供則從環境變數讀取）
            model: 要使用的模型（預設 gpt-4）
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or "gpt-4"  # 支援動態設定模型
    
    def analyze_content(self, html_content: str, url: str, page_title: str = "") -> Optional[Dict[str, Any]]:
        """
        分析網頁內容品質
        
        Args:
            html_content: 網頁 HTML 內容（前 2000 字）
            url: 網頁網址
            page_title: 頁面標題
            
        Returns:
            分析結果 JSON 或 None（失敗時）
        """
        try:
            # 限制內容長度
            content_preview = html_content[:2000]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """你是專業的 SEO 分析師。請分析網頁內容並回傳 JSON 格式：
                        {
                            "content_quality_score": 1-10 的分數,
                            "readability": "良好" 或 "普通" 或 "差",
                            "topic_relevance": "高" 或 "中" 或 "低",
                            "user_intent_match": "符合" 或 "部分符合" 或 "不符合",
                            "improvements": ["建議1", "建議2", ...]
                        }"""
                    },
                    {
                        "role": "user",
                        "content": f"分析這個網頁:\n\nURL: {url}\n標題: {page_title}\n\n內容: {content_preview}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=500,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        
        except Exception as e:
            print(f"GPT API error in analyze_content: {e}")
            return None
    
    def generate_meta_description(
        self, 
        page_title: str, 
        content_summary: str,
        current_meta: Optional[str] = None
    ) -> Optional[str]:
        """
        產生優化的 meta description
        
        Args:
            page_title: 頁面標題
            content_summary: 內容摘要
            current_meta: 目前的 meta description（可選）
            
        Returns:
            優化的 meta description（150-160 字元）或 None（失敗時）
        """
        try:
            prompt = f"""為這個網頁產生最佳的 meta description：

標題：{page_title}
內容摘要：{content_summary}
{f'目前的 meta：{current_meta}' if current_meta else ''}

要求：
- 150-160 字元（中文約 75-80 字）
- 包含主要關鍵字
- 吸引點擊
- 明確描述內容價值
- 包含行動呼籲（如適用）

只回傳最終的 meta description 文字，不要其他說明。"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是 SEO 專家，擅長撰寫吸引人的 meta description。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip().strip('"').strip("'")
        
        except Exception as e:
            print(f"GPT API error in generate_meta_description: {e}")
            return None
    
    def optimize_title(
        self,
        current_title: str,
        page_content_summary: str
    ) -> Optional[str]:
        """
        優化 title 標籤
        
        Args:
            current_title: 目前的 title
            page_content_summary: 頁面內容摘要
            
        Returns:
            優化的 title（50-60 字元）或 None（失敗時）
        """
        try:
            prompt = f"""優化這個網頁標題：

目前標題：{current_title}
頁面內容：{page_content_summary}

要求：
- 50-60 字元（中文約 25-30 字）
- 保留核心關鍵字
- 更具描述性和吸引力
- 符合 SEO 最佳實踐

只回傳最終的 title 文字。"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是 SEO 專家，擅長優化網頁標題。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip().strip('"').strip("'")
        
        except Exception as e:
            print(f"GPT API error in optimize_title: {e}")
            return None
    
    def generate_image_alt(
        self,
        image_filename: str,
        image_url: str,
        page_title: str,
        context: str = ""
    ) -> Optional[str]:
        """
        產生圖片 alt 文字
        
        Args:
            image_filename: 圖片檔名
            image_url: 圖片 URL
            page_title: 所在頁面標題
            context: 圖片周圍的文字內容（可選）
            
        Returns:
            描述性的 alt 文字（不超過 125 字元）或 None（失敗時）
        """
        try:
            prompt = f"""為這張圖片產生 alt 屬性：

檔名：{image_filename}
URL：{image_url}
所在頁面：{page_title}
{f'周圍內容：{context}' if context else ''}

要求：
- 不超過 125 字元
- 描述性且有意義
- 包含相關關鍵字（若適用）
- 不要以「圖片」或「照片」開頭

只回傳 alt 文字內容。"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是 SEO 專家，擅長撰寫有意義的圖片 alt 文字。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=80,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip().strip('"').strip("'")
        
        except Exception as e:
            print(f"GPT API error in generate_image_alt: {e}")
            return None


    def optimize_h1_title(
        self,
        current_h1: str,
        content_summary: str,
        keywords: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        優化 H1 主標題（進階功能）
        
        Args:
            current_h1: 當前的 H1 標題
            content_summary: 文章內容摘要
            keywords: 目標關鍵字
            
        Returns:
            優化結果 JSON 或 None
        """
        try:
            prompt = AdvancedPrompts.get_prompt(
                'h1',
                current_h1=current_h1,
                content_summary=content_summary,
                keywords=keywords or "（無特定關鍵字）"
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是專業的 SEO 內容優化師。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=300,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            print(f"Optimize H1 error: {e}")
            return None
    
    def optimize_keyword_density(
        self,
        paragraph: str,
        keywords: str,
        current_count: int,
        word_count: int
    ) -> Optional[Dict[str, Any]]:
        """
        優化段落的關鍵字密度（進階功能）
        
        Args:
            paragraph: 原始段落
            keywords: 目標關鍵字
            current_count: 當前關鍵字出現次數
            word_count: 段落總字數
            
        Returns:
            優化結果 JSON 或 None
        """
        try:
            current_density = round((current_count / word_count) * 100, 2) if word_count > 0 else 0
            
            prompt = AdvancedPrompts.get_prompt(
                'keyword_density',
                original_paragraph=paragraph,
                keywords=keywords,
                current_count=current_count,
                word_count=word_count,
                current_density=current_density
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是專業的 SEO 內容優化師，擅長自然地優化關鍵字密度。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            print(f"Optimize keyword density error: {e}")
            return None
    
    def fix_heading_structure(
        self,
        html_content: str,
        problem_description: str
    ) -> Optional[Dict[str, Any]]:
        """
        修正標題結構層級（進階功能）
        
        Args:
            html_content: 當前的 HTML 內容（含標題）
            problem_description: 問題描述
            
        Returns:
            修正結果 JSON 或 None
        """
        try:
            prompt = AdvancedPrompts.get_prompt(
                'heading_structure',
                current_html=html_content[:3000],  # 限制長度
                problem_description=problem_description
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是 SEO 結構專家，擅長修正 HTML 標題層級。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.5
            )
            
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            print(f"Fix heading structure error: {e}")
            return None
    
    def rewrite_content(
        self,
        paragraph: str,
        optimization_goals: str,
        keywords: str = "",
        tone: str = "專業"
    ) -> Optional[Dict[str, Any]]:
        """
        重寫內容段落（進階功能）
        
        Args:
            paragraph: 原始段落
            optimization_goals: 優化目標
            keywords: 目標關鍵字
            tone: 語氣風格
            
        Returns:
            重寫結果 JSON 或 None
        """
        try:
            prompt = AdvancedPrompts.get_prompt(
                'content_rewrite',
                original_paragraph=paragraph,
                optimization_goals=optimization_goals,
                keywords=keywords or "（無特定關鍵字）",
                tone=tone
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是專業的內容優化師和 SEO 專家。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1200,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            print(f"Rewrite content error: {e}")
            return None


def is_openai_available() -> bool:
    """
    檢查 OpenAI 是否可用
    
    Returns:
        True 如果 OpenAI 套件已安裝且 API key 已設定
    """
    if not OPENAI_AVAILABLE:
        return False
    
    api_key = os.environ.get('OPENAI_API_KEY')
    return bool(api_key)

