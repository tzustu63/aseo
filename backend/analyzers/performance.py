"""
Performance Analyzer

分析網頁效能相關指標
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult


class PerformanceAnalyzer(BaseAnalyzer):
    """效能分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析效能指標
        
        檢查項目：
        - HTML 檔案大小
        - 外部資源數量
        - inline script/style 數量
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        issues = []
        score = 100
        metadata = {}
        
        # 計算 HTML 大小
        html_size = len(html)
        html_size_kb = html_size / 1024
        metadata['html_size'] = html_size
        metadata['html_size_kb'] = round(html_size_kb, 2)
        
        if html_size_kb > 100:
            issues.append(self._create_issue(
                severity='medium',
                message=f'HTML 檔案較大（{html_size_kb:.1f} KB）',
                suggestion='考慮壓縮 HTML 或移除不必要的內容',
                priority=4,
                impact='大型 HTML 檔案會增加頁面載入時間',
                difficulty='medium'
            ))
            score -= 15
        
        # 統計外部資源
        css_links = soup.find_all('link', rel='stylesheet')
        js_scripts = soup.find_all('script', src=True)
        images = soup.find_all('img', src=True)
        
        metadata['external_css'] = len(css_links)
        metadata['external_js'] = len(js_scripts)
        metadata['external_images'] = len(images)
        metadata['total_external_resources'] = len(css_links) + len(js_scripts) + len(images)
        
        if len(css_links) + len(js_scripts) > 20:
            issues.append(self._create_issue(
                severity='medium',
                message=f'外部資源數量較多（CSS: {len(css_links)}, JS: {len(js_scripts)}）',
                suggestion='考慮合併 CSS/JS 檔案，或使用 CDN 加速',
                priority=4,
                impact='過多的外部請求會增加頁面載入時間',
                difficulty='hard'
            ))
            score -= 15
        
        # 檢查 inline script/style
        inline_scripts = soup.find_all('script', src=False)
        inline_styles = soup.find_all('style')
        
        metadata['inline_scripts'] = len(inline_scripts)
        metadata['inline_styles'] = len(inline_styles)
        
        large_inline_scripts = [s for s in inline_scripts if len(s.get_text()) > 1000]
        
        if large_inline_scripts:
            issues.append(self._create_issue(
                severity='low',
                message=f'有 {len(large_inline_scripts)} 個大型 inline script',
                suggestion='考慮將大型 JavaScript 移到外部檔案',
                priority=5,
                impact='inline script 會阻塞 HTML 解析',
                difficulty='medium'
            ))
            score -= 10
        
        return AnalysisResult(
            category='performance',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

