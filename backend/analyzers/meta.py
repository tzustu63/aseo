"""
Meta Tags Analyzer

分析網頁的 meta 標籤
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult


class MetaAnalyzer(BaseAnalyzer):
    """Meta 標籤分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析 meta 標籤
        
        檢查項目：
        - meta description
        - meta keywords (可選)
        - Open Graph tags
        - viewport meta tag
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        issues = []
        score = 100
        metadata = {}
        
        # 檢查 meta description
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if not description_tag or not description_tag.get('content'):
            issues.append(self._create_issue(
                severity='critical',
                message='缺少 meta description',
                suggestion='在 <head> 中加入 meta description 來改善搜尋結果顯示',
                priority=1,
                code_example='<meta name="description" content="簡短描述您的網頁內容，約 150-160 字元">',
                impact='缺少 description 會讓 Google 自動擷取頁面內容，可能無法精確傳達重點',
                difficulty='easy'
            ))
            score -= 30
            metadata['description'] = None
            metadata['description_length'] = 0
        else:
            description = description_tag.get('content', '').strip()
            desc_length = len(description)
            metadata['description'] = description
            metadata['description_length'] = desc_length
            
            if desc_length < 120:
                issues.append(self._create_issue(
                    severity='high',
                    message=f'meta description 太短（{desc_length} 字元）',
                    suggestion='建議 description 長度為 150-160 字元',
                    priority=2,
                    code_example=f'<!-- 目前：{description[:50]}... -->\n<!-- 建議：擴充為 150-160 字元的完整描述 -->',
                    impact='過短的描述無法充分利用搜尋結果顯示空間',
                    difficulty='easy'
                ))
                score -= 15
            elif desc_length > 160:
                issues.append(self._create_issue(
                    severity='medium',
                    message=f'meta description 過長（{desc_length} 字元）',
                    suggestion='建議縮短至 150-160 字元',
                    priority=3,
                    code_example='<!-- Google 搜尋結果會截斷過長的 description -->',
                    impact='過長的描述會在搜尋結果中被截斷',
                    difficulty='easy'
                ))
                score -= 10
        
        # 檢查 Open Graph tags
        og_tags = {
            'og:title': soup.find('meta', property='og:title'),
            'og:description': soup.find('meta', property='og:description'),
            'og:image': soup.find('meta', property='og:image'),
            'og:url': soup.find('meta', property='og:url'),
        }
        
        missing_og = [name for name, tag in og_tags.items() if not tag or not tag.get('content')]
        
        if missing_og:
            issues.append(self._create_issue(
                severity='medium',
                message=f'缺少 Open Graph 標籤：{", ".join(missing_og)}',
                suggestion='加入 OG 標籤可改善社群媒體（Facebook、LINE 等）分享時的顯示效果',
                priority=4,
                code_example='''<meta property="og:title" content="頁面標題">
<meta property="og:description" content="頁面描述">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">''',
                impact='影響社群媒體分享的顯示效果',
                difficulty='easy'
            ))
            score -= 10
        
        metadata['og_tags'] = {name: (tag.get('content') if tag else None) for name, tag in og_tags.items()}
        
        # 檢查 canonical 標籤
        canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical_tag or not canonical_tag.get('href'):
            issues.append(self._create_issue(
                severity='low',
                message='缺少 canonical 標籤',
                suggestion='加入 canonical 標籤可避免重複內容問題',
                priority=5,
                code_example=f'<link rel="canonical" href="{url}">',
                impact='有助於避免搜尋引擎將相似頁面視為重複內容',
                difficulty='easy'
            ))
            score -= 5
        
        metadata['canonical'] = canonical_tag.get('href') if canonical_tag else None
        
        return AnalysisResult(
            category='meta_tags',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

