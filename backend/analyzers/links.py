"""
Links Analyzer

分析內部和外部連結
- 內部連結結構
- 外部連結品質
- 錨點文字優化
- 連結可訪問性
- nofollow/noopener 屬性
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult
from urllib.parse import urlparse

class LinksAnalyzer(BaseAnalyzer):
    """連結分析器"""
    
    def __init__(self):
        super().__init__()
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析連結
        
        Args:
            html: HTML 內容
            url: 頁面 URL
            
        Returns:
            分析結果
        """
        soup = BeautifulSoup(html, 'html.parser')
        issues_data = []
        score = 100
        
        # 取得所有連結
        links = soup.find_all('a', href=True)
        
        if not links:
            return AnalysisResult(
                category='links',
                score=20,
                issues=[
                    self._create_issue(
                        severity='high',
                        message='頁面沒有任何連結',
                        suggestion='添加相關的內部連結和外部資源連結，有助於 SEO 和使用者體驗',
                        priority=1,
                        difficulty='easy'
                    )
                ]
            )
        
        # 分析連結
        internal_links, external_links = self._categorize_links(links, url)
        
        # 檢查內部連結
        self._check_internal_links(internal_links, issues_data)
        
        # 檢查外部連結
        self._check_external_links(external_links, issues_data)
        
        # 檢查錨點文字
        self._check_anchor_text(links, issues_data)
        
        # 檢查斷鏈（這裡只做基本檢查）
        self._check_broken_links(links, issues_data)
        
        # 計算分數
        score = max(0, 100 - (len(issues_data) * 10))
        
        # 將字典轉換為 Issue 對象
        issues = [
            self._create_issue(
                severity=issue['severity'],
                message=issue['message'],
                suggestion=issue.get('suggestion', ''),
                priority=self._severity_to_priority(issue['severity']),
                difficulty='medium'
            )
            for issue in issues_data
        ]
        
        return AnalysisResult(
            category='links',
            score=score,
            issues=issues
        )
    
    def _severity_to_priority(self, severity: str) -> int:
        """將嚴重程度轉換為優先級"""
        severity_map = {
            'high': 1,
            'medium': 2,
            'low': 3
        }
        return severity_map.get(severity, 2)
    
    def _categorize_links(self, links: list, page_url: str) -> tuple:
        """分類內部和外部連結"""
        page_domain = urlparse(page_url).netloc
        internal = []
        external = []
        
        for link in links:
            href = link.get('href', '')
            
            # 跳過錨點連結和 JavaScript
            if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            # 判斷是否為外部連結
            if href.startswith('http'):
                link_domain = urlparse(href).netloc
                if link_domain == page_domain:
                    internal.append(link)
                else:
                    external.append(link)
            else:
                # 相對路徑視為內部連結
                internal.append(link)
        
        return internal, external
    
    def _check_internal_links(self, internal_links: list, issues: list):
        """檢查內部連結"""
        if len(internal_links) < 3:
            issues.append({
                'type': '內部連結過少',
                'message': f'只有 {len(internal_links)} 個內部連結',
                'severity': 'medium',
                'suggestion': '增加相關的內部連結（建議至少 5-10 個），有助於建立網站結構和分散頁面權重',
                'current_value': f'內部連結數量：{len(internal_links)}'
            })
        
        # 檢查是否有目錄頁面連結（通常是首頁或分類頁）
        has_home_link = any(
            link.get('href') in ['/', '/index.html', '/index.php'] or 
            '首頁' in link.get_text() or 
            'Home' in link.get_text()
            for link in internal_links
        )
        
        if not has_home_link and len(internal_links) > 0:
            issues.append({
                'type': '缺少首頁連結',
                'message': '未發現返回首頁的連結',
                'severity': 'low',
                'suggestion': '添加首頁連結，有助於使用者導航和網站結構'
            })
    
    def _check_external_links(self, external_links: list, issues: list):
        """檢查外部連結"""
        if not external_links:
            return
        
        # 檢查是否有設定 rel 屬性
        links_without_rel = []
        links_without_target = []
        
        for link in external_links:
            rel = link.get('rel', [])
            target = link.get('target', '')
            
            # 外部連結應該有 noopener 或 noreferrer
            if not any(r in ['noopener', 'noreferrer', 'nofollow'] for r in (rel if isinstance(rel, list) else [rel])):
                links_without_rel.append(link.get('href', ''))
            
            # 外部連結建議在新視窗開啟
            if target != '_blank':
                links_without_target.append(link.get('href', ''))
        
        if len(links_without_rel) > 0:
            issues.append({
                'type': '外部連結缺少安全屬性',
                'message': f'{len(links_without_rel)} 個外部連結缺少 rel="noopener" 或 rel="noreferrer"',
                'severity': 'medium',
                'suggestion': '為外部連結添加 rel="noopener noreferrer"，以提升安全性和效能',
                'current_value': f'受影響的連結數量：{len(links_without_rel)}'
            })
        
        if len(links_without_target) > len(external_links) * 0.5:
            issues.append({
                'type': '外部連結未在新視窗開啟',
                'message': f'{len(links_without_target)} 個外部連結未設定 target="_blank"',
                'severity': 'low',
                'suggestion': '考慮為外部連結添加 target="_blank"，讓使用者在新分頁開啟外部網站',
                'current_value': f'受影響的連結數量：{len(links_without_target)}'
            })
    
    def _check_anchor_text(self, links: list, issues: list):
        """檢查錨點文字"""
        generic_texts = ['點擊這裡', '這裡', 'click here', 'here', '更多', 'more', '閱讀更多', 'read more']
        generic_count = 0
        empty_count = 0
        
        for link in links:
            text = link.get_text().strip().lower()
            
            if not text:
                empty_count += 1
            elif text in generic_texts:
                generic_count += 1
        
        if empty_count > 0:
            issues.append({
                'type': '空白錨點文字',
                'message': f'{empty_count} 個連結沒有錨點文字',
                'severity': 'high',
                'suggestion': '為所有連結添加描述性的錨點文字，有助於 SEO 和可訪問性',
                'current_value': f'空白連結數量：{empty_count}'
            })
        
        if generic_count > 0:
            issues.append({
                'type': '錨點文字不具描述性',
                'message': f'{generic_count} 個連結使用了通用的錨點文字（如「點擊這裡」）',
                'severity': 'medium',
                'suggestion': '使用具有描述性的錨點文字（如「查看 SEO 優化指南」），而非通用文字，有助於 SEO',
                'current_value': f'通用文字連結數量：{generic_count}'
            })
    
    def _check_broken_links(self, links: list, issues: list):
        """檢查可能的斷鏈（基本檢查）"""
        suspicious_links = []
        
        for link in links:
            href = link.get('href', '')
            
            # 檢查明顯的問題
            if href in ['#', '', 'javascript:void(0)', 'javascript:;']:
                suspicious_links.append(href or '(空白)')
        
        if suspicious_links:
            issues.append({
                'type': '無效的連結',
                'message': f'{len(suspicious_links)} 個連結指向無效位置',
                'severity': 'medium',
                'suggestion': '修正或移除無效的連結（href 為 # 或空白）',
                'current_value': f'無效連結數量：{len(suspicious_links)}'
            })

