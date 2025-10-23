"""
SEO Auto Fixer - 自動修復引擎

提供 SEO 問題的分類、預覽和修復功能
"""
from typing import Dict, Any, Optional
from analyzers.base import Issue
from ai.content_generator import ContentGenerator
from wordpress.client import WordPressClient


class SEOAutoFixer:
    """SEO 自動修復引擎"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        初始化自動修復引擎
        
        Args:
            api_key: OpenAI API 金鑰（選用）
            model: 要使用的模型（選用）
        """
        self.content_generator = ContentGenerator(api_key=api_key, model=model)
    
    @staticmethod
    def classify_issue(issue: Issue) -> str:
        """
        分類問題的可修復類型
        
        Args:
            issue: SEO 問題
            
        Returns:
            'auto' | 'ai' | 'ai-advanced' | 'manual'
        """
        # 如果已經有 fixable_type，直接返回
        if issue.fixable_type:
            return issue.fixable_type
        
        message_lower = issue.message.lower()
        
        # 技術性問題 → 自動修復
        auto_keywords = [
            '缺少 viewport',
            '缺少 charset',
            '缺少 canonical',
            '缺少 robots meta',
            '缺少 open graph'
        ]
        
        for keyword in auto_keywords:
            if keyword in message_lower:
                return 'auto'
        
        # 進階 AI 輔助（重大內容變更，需要更強的 AI 和必須預覽）
        ai_advanced_keywords = [
            'h1',
            '主標題',
            '關鍵字密度',
            '標題結構',
            '標題層級',
            '內容重寫',
            '內容優化',
            '段落',
            '跳級'
        ]
        
        for keyword in ai_advanced_keywords:
            if keyword in message_lower:
                return 'ai-advanced'
        
        # 一般 AI 輔助
        ai_keywords = [
            'meta description',
            'description 太短',
            'description 過長',
            'title 太短',
            'title 過長',
            '圖片 alt',
            'alt 屬性'
        ]
        
        for keyword in ai_keywords:
            if keyword in message_lower:
                return 'ai'
        
        # 其他 → 人工修復
        return 'manual'
    
    def generate_technical_fix(self, issue: Issue, context: Dict[str, Any]) -> Optional[str]:
        """
        產生技術性修復的內容
        
        Args:
            issue: SEO 問題
            context: 上下文資訊（包含 url 等）
            
        Returns:
            修復內容或 None
        """
        message_lower = issue.message.lower()
        
        if '缺少 viewport' in message_lower or 'viewport' in message_lower:
            return '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        
        elif '缺少 charset' in message_lower:
            return '<meta charset="UTF-8">'
        
        elif '缺少 canonical' in message_lower:
            url = context.get('url', '')
            return f'<link rel="canonical" href="{url}">'
        
        elif '缺少 robots' in message_lower:
            return '<meta name="robots" content="index, follow">'
        
        elif 'open graph' in message_lower and 'og:title' in message_lower:
            title = context.get('page_title', '')
            return f'<meta property="og:title" content="{title}">'
        
        elif 'open graph' in message_lower and 'og:description' in message_lower:
            return '<meta property="og:description" content="網站描述">'
        
        return None
    
    def generate_fix_preview(
        self,
        issue: Issue,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        產生修復預覽
        
        Args:
            issue: SEO 問題
            context: 上下文資訊
            
        Returns:
            預覽資料
        """
        fixable_type = self.classify_issue(issue)
        
        if fixable_type == 'auto':
            # 技術問題直接產生修復
            fix_content = self.generate_technical_fix(issue, context)
            return {
                'fixable_type': 'auto',
                'before': None,
                'after': fix_content,
                'message': '技術性修復',
                'impact': issue.impact or '改善 SEO 基礎設定',
                'fix_content': fix_content,
                'risk_level': 'low'
            }
        
        elif fixable_type == 'ai':
            # AI 產生內容優化（這裡只返回需要 AI 的資訊，實際內容由 API 端點呼叫 AI 產生）
            fix_data = issue.fix_data or {}
            return {
                'fixable_type': 'ai',
                'before': fix_data.get('current_value'),
                'after': None,  # 需要呼叫 AI API 產生
                'message': '需要 AI 產生優化內容',
                'impact': issue.impact or '改善內容品質和吸引力',
                'issue_type': self._determine_ai_issue_type(issue),
                'context': context,
                'risk_level': 'medium'
            }
        
        elif fixable_type == 'ai-advanced':
            # 進階 AI 輔助（重大內容變更）
            fix_data = issue.fix_data or {}
            return {
                'fixable_type': 'ai-advanced',
                'before': fix_data.get('current_value'),
                'after': None,  # 需要呼叫進階 AI API 產生
                'message': '⚠️ 重大內容變更，需要 AI 產生並仔細確認',
                'impact': issue.impact or '重大 SEO 改善，但需謹慎確認',
                'issue_type': self._determine_advanced_issue_type(issue),
                'context': context,
                'risk_level': 'high',
                'requires_backup': True,
                'warning': '這是重大內容變更，請仔細檢查 AI 產生的內容是否符合您的需求'
            }
        
        else:
            return {
                'fixable_type': 'manual',
                'message': '需要人工處理',
                'suggestion': issue.suggestion,
                'risk_level': 'high'
            }
    
    def _determine_ai_issue_type(self, issue: Issue) -> str:
        """
        判斷 AI 問題的具體類型
        
        Args:
            issue: SEO 問題
            
        Returns:
            問題類型 (meta_description, title, image_alt)
        """
        message_lower = issue.message.lower()
        
        if 'meta description' in message_lower or 'description' in message_lower:
            return 'meta_description'
        elif 'title' in message_lower:
            return 'title'
        elif 'alt' in message_lower or '圖片' in message_lower:
            return 'image_alt'
        else:
            return 'unknown'
    
    def _determine_advanced_issue_type(self, issue: Issue) -> str:
        """
        判斷進階 AI 問題的具體類型
        
        Args:
            issue: SEO 問題
            
        Returns:
            問題類型 (h1_title, keyword_density, heading_structure, content_rewrite)
        """
        message_lower = issue.message.lower()
        
        if 'h1' in message_lower or '主標題' in message_lower:
            return 'h1_title'
        elif '關鍵字密度' in message_lower or '關鍵字' in message_lower and '密度' in message_lower:
            return 'keyword_density'
        elif '標題結構' in message_lower or '標題層級' in message_lower or '跳級' in message_lower:
            return 'heading_structure'
        elif '內容重寫' in message_lower or '內容優化' in message_lower or '段落' in message_lower:
            return 'content_rewrite'
        else:
            return 'unknown'
    
    def generate_ai_fix(
        self,
        issue: Issue,
        context: Dict[str, Any]
    ) -> Optional[str]:
        """
        使用 AI 產生修復內容（一般 AI）
        
        Args:
            issue: SEO 問題
            context: 上下文資訊
            
        Returns:
            AI 產生的內容或 None
        """
        if not self.content_generator.is_available():
            return None
        
        issue_type = self._determine_ai_issue_type(issue)
        fix_data = issue.fix_data or {}
        
        current_value = fix_data.get('current_value')
        
        return self.content_generator.generate_fix_content(
            issue_type=issue_type,
            current_value=current_value,
            context=context
        )
    
    def generate_advanced_ai_fix(
        self,
        issue: Issue,
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        使用進階 AI 產生修復內容（重大變更）
        
        Args:
            issue: SEO 問題
            context: 上下文資訊
            
        Returns:
            AI 產生的完整修復資訊 JSON 或 None
        """
        if not self.content_generator.is_available():
            return None
        
        issue_type = self._determine_advanced_issue_type(issue)
        fix_data = issue.fix_data or {}
        
        current_value = fix_data.get('current_value')
        
        return self.content_generator.generate_advanced_fix(
            issue_type=issue_type,
            current_value=current_value,
            context=context
        )
    
    @staticmethod
    def apply_fix_to_wordpress(
        wp_client: WordPressClient,
        issue: Issue,
        fix_content: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        套用修復到 WordPress
        
        Args:
            wp_client: WordPress 客戶端
            issue: SEO 問題
            fix_content: 修復內容
            context: 上下文資訊（包含 page_url 等）
            
        Returns:
            執行結果
        """
        try:
            fix_data = issue.fix_data or {}
            message_lower = issue.message.lower()
            
            # 找到對應的文章或頁面
            page_url = context.get('page_url') or context.get('url')
            if not page_url:
                return {
                    'success': False,
                    'message': '無法找到頁面 URL'
                }
            
            post = wp_client.find_post_by_url(page_url)
            if not post:
                return {
                    'success': False,
                    'message': '無法在 WordPress 中找到對應的頁面'
                }
            
            post_id = post.get('id')
            post_type = post.get('type')
            
            # 檢測 SEO 外掛環境
            seo_environment = wp_client.detect_seo_plugin()
            plugin_type = seo_environment.get('plugin', 'none')
            
            print(f"檢測到 SEO 環境: {plugin_type}")
            
            # 根據問題類型和環境決定更新方式
            if 'meta description' in message_lower or 'description' in message_lower:
                if plugin_type == 'yoast':
                    # 更新 Yoast SEO meta description
                    meta_data = {'_yoast_wpseo_metadesc': fix_content}
                    if post_type == 'page':
                        result = wp_client.update_page_meta(post_id, meta_data)
                    else:
                        result = wp_client.update_post_meta(post_id, meta_data)
                elif plugin_type == 'rank_math':
                    # 更新 Rank Math meta description
                    meta_data = {'rank_math_description': fix_content}
                    if post_type == 'page':
                        result = wp_client.update_page_meta(post_id, meta_data)
                    else:
                        result = wp_client.update_post_meta(post_id, meta_data)
                elif plugin_type == 'aioseo':
                    # 更新 All in One SEO meta description
                    meta_data = {'_aioseo_description': fix_content}
                    if post_type == 'page':
                        result = wp_client.update_page_meta(post_id, meta_data)
                    else:
                        result = wp_client.update_post_meta(post_id, meta_data)
                else:
                    # 無外掛模式：使用自訂欄位
                    result = wp_client.update_custom_seo_fields(
                        post_id, post_type, seo_description=fix_content
                    )
                
                return result
            
            elif 'title' in message_lower:
                if plugin_type == 'yoast':
                    # 更新 Yoast SEO title
                    meta_data = {'_yoast_wpseo_title': fix_content}
                    if post_type == 'page':
                        result = wp_client.update_page_meta(post_id, meta_data)
                    else:
                        result = wp_client.update_post_meta(post_id, meta_data)
                elif plugin_type == 'rank_math':
                    # 更新 Rank Math title
                    meta_data = {'rank_math_title': fix_content}
                    if post_type == 'page':
                        result = wp_client.update_page_meta(post_id, meta_data)
                    else:
                        result = wp_client.update_post_meta(post_id, meta_data)
                elif plugin_type == 'aioseo':
                    # 更新 All in One SEO title
                    meta_data = {'_aioseo_title': fix_content}
                    if post_type == 'page':
                        result = wp_client.update_page_meta(post_id, meta_data)
                    else:
                        result = wp_client.update_post_meta(post_id, meta_data)
                else:
                    # 無外掛模式：使用自訂欄位
                    result = wp_client.update_custom_seo_fields(
                        post_id, post_type, seo_title=fix_content
                    )
                
                return result
            
            elif 'alt' in message_lower or '圖片' in message_lower:
                # 更新圖片 alt
                image_url = fix_data.get('image_url')
                if not image_url:
                    return {
                        'success': False,
                        'message': '缺少圖片 URL'
                    }
                
                media_id = wp_client.find_media_by_url(image_url)
                if not media_id:
                    return {
                        'success': False,
                        'message': '無法在媒體庫中找到此圖片'
                    }
                
                return wp_client.update_media_alt(media_id, fix_content)
            
            elif 'h1' in message_lower or '主標題' in message_lower:
                # 更新 H1 主標題（進階功能）
                # 取得當前內容
                current_content = wp_client.get_post_content(post_id)
                if not current_content:
                    return {
                        'success': False,
                        'message': '無法取得文章內容'
                    }
                
                # 替換 H1 標題
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(current_content, 'html.parser')
                h1 = soup.find('h1')
                if h1:
                    h1.string = fix_content
                    new_content = str(soup)
                    
                    if post_type == 'page':
                        result = wp_client.update_post_content(post_id, new_content)
                    else:
                        result = wp_client.update_post_content(post_id, new_content)
                    
                    return result
                else:
                    return {
                        'success': False,
                        'message': '文章中找不到 H1 標籤'
                    }
            
            elif '關鍵字密度' in message_lower or '段落' in message_lower or '內容' in message_lower:
                # 更新段落內容（進階功能）
                # 這裡需要更複雜的邏輯來定位和替換特定段落
                # 簡化版本：直接更新指定的內容
                current_content = wp_client.get_post_content(post_id)
                if not current_content:
                    return {
                        'success': False,
                        'message': '無法取得文章內容'
                    }
                
                # 使用 fix_data 中的定位資訊來替換內容
                old_content = fix_data.get('current_value', '')
                if old_content and old_content in current_content:
                    new_content = current_content.replace(old_content, fix_content, 1)
                    
                    if post_type == 'page':
                        result = wp_client.update_post_content(post_id, new_content)
                    else:
                        result = wp_client.update_post_content(post_id, new_content)
                    
                    return result
                else:
                    return {
                        'success': False,
                        'message': '無法在文章中找到要替換的內容'
                    }
            
            elif '標題結構' in message_lower or '標題層級' in message_lower:
                # 修正標題結構（進階功能）
                # fix_content 包含修正後的完整 HTML
                if post_type == 'page':
                    result = wp_client.update_post_content(post_id, fix_content)
                else:
                    result = wp_client.update_post_content(post_id, fix_content)
                
                return result
            
            else:
                return {
                    'success': False,
                    'message': '不支援的修復類型'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'套用修復失敗：{str(e)}'
            }

