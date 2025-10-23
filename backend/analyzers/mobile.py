"""
Mobile Friendliness Analyzer

分析行動裝置友善度
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult


class MobileAnalyzer(BaseAnalyzer):
    """行動裝置分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析行動裝置友善度
        
        檢查項目：
        - viewport meta 標籤
        - 響應式設計跡象
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        issues = []
        score = 100
        metadata = {}
        
        # 檢查 viewport meta 標籤
        viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
        
        if not viewport_tag or not viewport_tag.get('content'):
            issues.append(self._create_issue(
                severity='high',
                message='缺少 viewport meta 標籤',
                suggestion='加入 viewport meta 標籤以支援行動裝置',
                priority=2,
                code_example='<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                impact='缺少 viewport 會導致頁面在手機上顯示異常',
                difficulty='easy'
            ))
            score -= 50
            metadata['viewport'] = None
        else:
            viewport_content = viewport_tag.get('content', '')
            metadata['viewport'] = viewport_content
            
            # 檢查 viewport 內容是否包含基本設定
            if 'width=device-width' not in viewport_content:
                issues.append(self._create_issue(
                    severity='medium',
                    message='viewport 缺少 width=device-width 設定',
                    suggestion='確保 viewport 包含 width=device-width',
                    priority=3,
                    code_example='<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    impact='缺少此設定會影響頁面在不同裝置上的顯示',
                    difficulty='easy'
                ))
                score -= 20
        
        # 檢查響應式設計的跡象（CSS media queries）
        style_tags = soup.find_all('style')
        css_links = soup.find_all('link', rel='stylesheet')
        
        has_media_query = False
        
        # 檢查 inline styles
        for style in style_tags:
            if '@media' in style.get_text():
                has_media_query = True
                break
        
        # 檢查 link 標籤的 media 屬性
        if not has_media_query:
            for link in css_links:
                if link.get('media'):
                    has_media_query = True
                    break
        
        metadata['has_media_query'] = has_media_query
        
        if not has_media_query:
            issues.append(self._create_issue(
                severity='low',
                message='未偵測到 CSS media queries',
                suggestion='建議使用 CSS media queries 實作響應式設計',
                priority=5,
                code_example='''@media (max-width: 768px) {
  /* 手機版樣式 */
}

@media (min-width: 769px) and (max-width: 1024px) {
  /* 平板版樣式 */
}''',
                impact='響應式設計可提升行動裝置使用體驗',
                difficulty='medium'
            ))
            score -= 10
        
        return AnalysisResult(
            category='mobile',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

