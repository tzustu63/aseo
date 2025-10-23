"""
Headings Analyzer

分析網頁的標題結構（H1-H6）
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult


class HeadingsAnalyzer(BaseAnalyzer):
    """標題結構分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析標題標籤結構
        
        檢查項目：
        - H1 標籤存在性和數量
        - 標題階層是否正確
        - 標題分佈情況
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        issues = []
        score = 100
        metadata = {}
        
        # 找出所有標題
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        h4_tags = soup.find_all('h4')
        h5_tags = soup.find_all('h5')
        h6_tags = soup.find_all('h6')
        all_headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        metadata['h1_count'] = len(h1_tags)
        metadata['h2_count'] = len(h2_tags)
        metadata['h3_count'] = len(h3_tags)
        metadata['h4_count'] = len(h4_tags)
        metadata['h5_count'] = len(h5_tags)
        metadata['h6_count'] = len(h6_tags)
        
        # 檢查 H1 標籤
        if len(h1_tags) == 0:
            issues.append(self._create_issue(
                severity='critical',
                message='網頁缺少 H1 標籤',
                suggestion='每個頁面都應該有一個 H1 標籤作為主標題',
                priority=1,
                code_example='<h1>頁面的主要標題</h1>',
                impact='H1 是最重要的標題標籤，缺少會大幅影響 SEO',
                difficulty='easy'
            ))
            score -= 40
        elif len(h1_tags) > 1:
            h1_texts = [h1.get_text().strip()[:30] for h1 in h1_tags[:3]]
            issues.append(self._create_issue(
                severity='high',
                message=f'網頁有 {len(h1_tags)} 個 H1 標籤',
                suggestion='建議每個頁面只使用一個 H1 標籤，其他改用 H2-H6',
                priority=2,
                code_example=f'<!-- 發現的 H1：\n  1. {h1_texts[0]}\n  2. {h1_texts[1] if len(h1_texts) > 1 else ""}\n-->\n<!-- 建議只保留最重要的一個作為 H1 -->',
                impact='多個 H1 會混淆搜尋引擎對頁面主題的理解',
                difficulty='easy'
            ))
            score -= 25
        else:
            # 有一個 H1，檢查長度
            h1_text = h1_tags[0].get_text().strip()
            h1_length = len(h1_text)
            metadata['h1_text'] = h1_text
            
            if h1_length < 10:
                issues.append(self._create_issue(
                    severity='medium',
                    message=f'H1 標籤太短（{h1_length} 字元）',
                    suggestion='H1 應該是完整的句子或標題，清楚描述頁面主題',
                    priority=3,
                    code_example=f'<!-- 目前：{h1_text} -->\n<!-- 建議使用更完整的描述 -->',
                    impact='過短的 H1 無法充分傳達頁面主題',
                    difficulty='easy'
                ))
                score -= 10
            elif h1_length > 70:
                issues.append(self._create_issue(
                    severity='low',
                    message=f'H1 標籤較長（{h1_length} 字元）',
                    suggestion='建議 H1 保持簡潔，約 20-70 字元',
                    priority=4,
                    impact='過長的 H1 可能顯得不夠聚焦',
                    difficulty='easy'
                ))
                score -= 5
        
        # 檢查標題階層（如果有 H1）
        if len(h1_tags) > 0:
            # 檢查是否有跳級（例如 H1 直接到 H3）
            heading_levels = [int(h.name[1]) for h in all_headings]
            
            if len(heading_levels) > 1:
                for i in range(len(heading_levels) - 1):
                    if heading_levels[i+1] - heading_levels[i] > 1:
                        issues.append(self._create_issue(
                            severity='medium',
                            message=f'標題階層跳級：H{heading_levels[i]} 直接跳到 H{heading_levels[i+1]}',
                            suggestion='標題應該按順序使用（H1 → H2 → H3），不要跳級',
                            priority=3,
                            impact='標題階層混亂會影響內容結構的語意',
                            difficulty='medium'
                        ))
                        score -= 10
                        break  # 只報告第一個跳級問題
        
        # 檢查是否有標題（任何級別）
        if len(all_headings) == 0:
            issues.append(self._create_issue(
                severity='high',
                message='網頁完全沒有標題標籤',
                suggestion='使用 H1-H6 標籤來組織內容結構',
                priority=1,
                code_example='<h1>主標題</h1>\n<h2>次標題</h2>\n<h3>小標題</h3>',
                impact='缺少標題會讓搜尋引擎難以理解內容結構',
                difficulty='easy'
            ))
            score = 0
        
        return AnalysisResult(
            category='headings',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

