"""
Title Tag Analyzer

分析網頁的 <title> 標籤
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult


class TitleAnalyzer(BaseAnalyzer):
    """Title 標籤分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析 title 標籤
        
        檢查項目：
        - title 標籤是否存在
        - title 長度是否適當（50-60 字元為佳）
        - title 是否為空
        """
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        
        issues = []
        score = 100
        metadata = {}
        
        # 檢查 title 標籤是否存在
        if not title_tag:
            issues.append(self._create_issue(
                severity='critical',
                message='缺少 <title> 標籤',
                suggestion='在 <head> 區塊中加入 <title> 標籤',
                priority=1,
                code_example='<head>\n  <title>您的頁面標題 - 簡短描述</title>\n</head>',
                impact='缺少 title 會嚴重影響搜尋引擎排名，且搜尋結果無法正常顯示',
                difficulty='easy'
            ))
            score = 0
            metadata['title'] = None
            metadata['length'] = 0
        else:
            title_text = title_tag.get_text().strip()
            title_length = len(title_text)
            metadata['title'] = title_text
            metadata['length'] = title_length
            
            # 檢查 title 是否為空
            if not title_text:
                issues.append(self._create_issue(
                    severity='critical',
                    message='title 標籤內容為空',
                    suggestion='在 title 標籤中加入描述性的頁面標題',
                    priority=1,
                    code_example='<title>您的品牌名稱 - 頁面主題</title>',
                    impact='空白標題無法讓搜尋引擎了解頁面內容',
                    difficulty='easy'
                ))
                score = 0
            # 檢查 title 長度
            elif title_length < 30:
                issues.append(self._create_issue(
                    severity='high',
                    message=f'title 標籤太短（{title_length} 字元）',
                    suggestion='建議 title 長度為 50-60 字元，以充分描述頁面內容',
                    priority=2,
                    code_example=f'<!-- 目前：{title_text} -->\n<!-- 建議：擴充為更完整的描述，約 50-60 字元 -->',
                    impact='過短的標題無法充分利用搜尋結果顯示空間',
                    difficulty='easy'
                ))
                score -= 30
            elif title_length > 60:
                issues.append(self._create_issue(
                    severity='medium',
                    message=f'title 標籤過長（{title_length} 字元）',
                    suggestion='建議縮短至 50-60 字元，Google 搜尋結果會截斷過長的標題',
                    priority=3,
                    code_example=f'<!-- 目前：{title_text[:80]}... -->\n<!-- 建議：精簡為 50-60 字元的核心描述 -->',
                    impact='過長的標題會在搜尋結果中被截斷，影響點擊率',
                    difficulty='easy'
                ))
                score -= 20
            
            # 檢查是否包含品牌名稱（建議）
            if '|' not in title_text and '-' not in title_text:
                issues.append(self._create_issue(
                    severity='low',
                    message='建議在 title 中加入品牌名稱',
                    suggestion='使用「頁面標題 - 品牌名稱」或「頁面標題 | 品牌名稱」格式',
                    priority=4,
                    code_example='<title>頁面主題 - 您的品牌名稱</title>',
                    impact='包含品牌名稱有助於提升品牌識別度',
                    difficulty='easy'
                ))
                score -= 5
        
        return AnalysisResult(
            category='title',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

