"""
HTML Structure Analyzer

分析網頁的 HTML 結構和語意化標籤
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult


class StructureAnalyzer(BaseAnalyzer):
    """HTML 結構分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析 HTML 結構
        
        檢查項目：
        - lang 屬性
        - 語意化 HTML5 標籤
        - 基本結構完整性
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        issues = []
        score = 100
        metadata = {}
        
        # 檢查 html lang 屬性
        html_tag = soup.find('html')
        if html_tag:
            lang = html_tag.get('lang')
            metadata['lang'] = lang
            
            if not lang:
                issues.append(self._create_issue(
                    severity='medium',
                    message='<html> 標籤缺少 lang 屬性',
                    suggestion='加入 lang 屬性指定頁面語言',
                    priority=3,
                    code_example='<html lang="zh-TW">\n  <!-- 繁體中文 -->\n</html>\n\n<html lang="zh-CN">\n  <!-- 簡體中文 -->\n</html>\n\n<html lang="en">\n  <!-- 英文 -->\n</html>',
                    impact='lang 屬性幫助搜尋引擎理解頁面語言',
                    difficulty='easy'
                ))
                score -= 15
        
        # 檢查語意化 HTML5 標籤
        semantic_tags = {
            'header': soup.find('header'),
            'nav': soup.find('nav'),
            'main': soup.find('main'),
            'article': soup.find('article'),
            'section': soup.find('section'),
            'footer': soup.find('footer'),
        }
        
        metadata['semantic_tags'] = {tag: (element is not None) for tag, element in semantic_tags.items()}
        
        used_tags = [tag for tag, element in semantic_tags.items() if element]
        metadata['semantic_tags_used'] = used_tags
        
        if len(used_tags) < 2:
            issues.append(self._create_issue(
                severity='low',
                message=f'只使用了 {len(used_tags)} 個語意化標籤',
                suggestion='建議使用 HTML5 語意標籤（header, main, article, footer 等）來改善頁面結構',
                priority=4,
                code_example='''<header>
  <nav>導航選單</nav>
</header>
<main>
  <article>主要內容</article>
</main>
<footer>頁尾資訊</footer>''',
                impact='語意化標籤幫助搜尋引擎理解頁面結構',
                difficulty='medium'
            ))
            score -= 10
        
        # 檢查 charset
        charset_tag = soup.find('meta', attrs={'charset': True})
        if not charset_tag:
            # 也檢查舊式的寫法
            charset_tag = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        
        if not charset_tag:
            issues.append(self._create_issue(
                severity='medium',
                message='缺少字元編碼宣告',
                suggestion='在 <head> 開頭加入字元編碼宣告',
                priority=3,
                code_example='<head>\n  <meta charset="UTF-8">\n  <!-- 其他 meta 標籤 -->\n</head>',
                impact='缺少 charset 可能導致中文顯示錯誤',
                difficulty='easy'
            ))
            score -= 10
        
        return AnalysisResult(
            category='structure',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

