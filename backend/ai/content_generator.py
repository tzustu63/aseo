"""
Content Generator

提供高階的內容產生功能
"""
from typing import Dict, Any, Optional
from .gpt5_client import GPT5Client, is_openai_available


class ContentGenerator:
    """內容產生器"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        初始化內容產生器
        
        Args:
            api_key: OpenAI API 金鑰（選用）
            model: 要使用的模型（選用）
        """
        self.client = None
        if is_openai_available() or api_key:
            try:
                self.client = GPT5Client(api_key=api_key, model=model)
            except Exception as e:
                print(f"Failed to initialize GPT5Client: {e}")
    
    def is_available(self) -> bool:
        """檢查 AI 功能是否可用"""
        return self.client is not None
    
    def generate_fix_content(
        self,
        issue_type: str,
        current_value: Optional[str],
        context: Dict[str, Any]
    ) -> Optional[str]:
        """
        根據問題類型產生修復內容
        
        Args:
            issue_type: 問題類型 (meta_description, title, image_alt)
            current_value: 目前的值（可選）
            context: 上下文資訊
            
        Returns:
            產生的修復內容或 None
        """
        if not self.is_available():
            return None
        
        try:
            if issue_type == 'meta_description':
                return self.client.generate_meta_description(
                    page_title=context.get('page_title', ''),
                    content_summary=context.get('content_summary', ''),
                    current_meta=current_value
                )
            
            elif issue_type == 'title':
                return self.client.optimize_title(
                    current_title=current_value or '',
                    page_content_summary=context.get('content_summary', '')
                )
            
            elif issue_type == 'image_alt':
                return self.client.generate_image_alt(
                    image_filename=context.get('image_filename', ''),
                    image_url=context.get('image_url', ''),
                    page_title=context.get('page_title', ''),
                    context=context.get('surrounding_text', '')
                )
            
            else:
                print(f"Unknown issue type: {issue_type}")
                return None
        
        except Exception as e:
            print(f"Error generating fix content: {e}")
            return None
    
    def generate_advanced_fix(
        self,
        issue_type: str,
        current_value: Optional[str],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        根據問題類型產生進階修復內容（返回完整 JSON）
        
        Args:
            issue_type: 問題類型 (h1_title, keyword_density, heading_structure, content_rewrite)
            current_value: 目前的值
            context: 上下文資訊
            
        Returns:
            完整的修復資訊 JSON 或 None
        """
        if not self.is_available():
            return None
        
        try:
            if issue_type == 'h1_title':
                return self.client.optimize_h1_title(
                    current_h1=current_value or '',
                    content_summary=context.get('content_summary', ''),
                    keywords=context.get('keywords', '')
                )
            
            elif issue_type == 'keyword_density':
                return self.client.optimize_keyword_density(
                    paragraph=current_value or '',
                    keywords=context.get('keywords', ''),
                    current_count=context.get('current_count', 0),
                    word_count=context.get('word_count', 0)
                )
            
            elif issue_type == 'heading_structure':
                return self.client.fix_heading_structure(
                    html_content=context.get('html_content', ''),
                    problem_description=context.get('problem_description', '')
                )
            
            elif issue_type == 'content_rewrite':
                return self.client.rewrite_content(
                    paragraph=current_value or '',
                    optimization_goals=context.get('optimization_goals', '改善 SEO 和可讀性'),
                    keywords=context.get('keywords', ''),
                    tone=context.get('tone', '專業')
                )
            
            else:
                print(f"Unknown advanced issue type: {issue_type}")
                return None
        
        except Exception as e:
            print(f"Error generating advanced fix: {e}")
            return None

