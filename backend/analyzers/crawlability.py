"""
Crawlability Analyzer

分析網站可爬性
- robots.txt
- XML Sitemap
- Canonical URL
- Meta robots
- X-Robots-Tag
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult
import requests
from urllib.parse import urljoin, urlparse

class CrawlabilityAnalyzer(BaseAnalyzer):
    """可爬性分析器"""
    
    def __init__(self):
        super().__init__()
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析網站可爬性
        
        Args:
            html: HTML 內容
            url: 頁面 URL
            
        Returns:
            分析結果
        """
        soup = BeautifulSoup(html, 'html.parser')
        issues_data = []
        score = 100
        
        # 檢查 robots.txt
        self._check_robots_txt(url, issues_data)
        
        # 檢查 sitemap
        self._check_sitemap(url, soup, issues_data)
        
        # 檢查 canonical URL
        self._check_canonical(soup, url, issues_data)
        
        # 檢查 meta robots
        self._check_meta_robots(soup, issues_data)
        
        # 檢查 hreflang（多語言）
        self._check_hreflang(soup, issues_data)
        
        # 計算分數
        score = max(0, 100 - (len(issues_data) * 12))
        
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
            category='crawlability',
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
    
    def _check_robots_txt(self, url: str, issues: list):
        """檢查 robots.txt"""
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        try:
            response = requests.get(robots_url, timeout=5)
            
            if response.status_code == 404:
                issues.append({
                    'type': '缺少 robots.txt',
                    'message': '網站沒有 robots.txt 檔案',
                    'severity': 'medium',
                    'suggestion': '建立 robots.txt 檔案，指定爬蟲規則和 Sitemap 位置'
                })
            elif response.status_code == 200:
                # 檢查是否有 Sitemap 聲明
                if 'sitemap:' not in response.text.lower():
                    issues.append({
                        'type': 'robots.txt 缺少 Sitemap',
                        'message': 'robots.txt 中未指定 Sitemap 位置',
                        'severity': 'low',
                        'suggestion': '在 robots.txt 中添加 "Sitemap: https://yoursite.com/sitemap.xml"'
                    })
        except:
            issues.append({
                'type': '無法訪問 robots.txt',
                'message': '無法檢查 robots.txt 檔案',
                'severity': 'low',
                'suggestion': '確保 robots.txt 可以被訪問'
            })
    
    def _check_sitemap(self, url: str, soup: BeautifulSoup, issues: list):
        """檢查 XML Sitemap"""
        # 檢查 HTML 中是否有 sitemap 連結
        sitemap_link = soup.find('link', rel='sitemap')
        
        if not sitemap_link:
            # 嘗試訪問標準位置
            parsed_url = urlparse(url)
            sitemap_urls = [
                f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap.xml",
                f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap_index.xml"
            ]
            
            sitemap_found = False
            for sitemap_url in sitemap_urls:
                try:
                    response = requests.get(sitemap_url, timeout=5)
                    if response.status_code == 200:
                        sitemap_found = True
                        break
                except:
                    continue
            
            if not sitemap_found:
                issues.append({
                    'type': '缺少 XML Sitemap',
                    'message': '未發現 XML Sitemap',
                    'severity': 'high',
                    'suggestion': '建立 XML Sitemap 並提交到 Google Search Console，有助於搜尋引擎發現您的網頁'
                })
        
    
    def _check_canonical(self, soup: BeautifulSoup, url: str, issues: list):
        """檢查 Canonical URL"""
        canonical = soup.find('link', rel='canonical')
        
        if not canonical:
            issues.append({
                'type': '缺少 Canonical URL',
                'message': '頁面沒有設定 canonical 標籤',
                'severity': 'medium',
                'suggestion': '添加 <link rel="canonical" href="..."> 標籤，以避免重複內容問題',
                'current_value': '建議的 canonical URL: ' + url
            })
        else:
            canonical_url = canonical.get('href', '')
            
            # 檢查 canonical URL 是否為絕對路徑
            if not canonical_url.startswith('http'):
                issues.append({
                    'type': 'Canonical URL 非絕對路徑',
                    'message': 'Canonical URL 應使用絕對路徑',
                    'severity': 'low',
                    'suggestion': '將 canonical URL 改為完整的絕對路徑（包含 https://）',
                    'current_value': f'目前值：{canonical_url}'
                })
    
    def _check_meta_robots(self, soup: BeautifulSoup, issues: list):
        """檢查 meta robots 標籤"""
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        
        if meta_robots:
            content = meta_robots.get('content', '').lower()
            
            # 檢查是否阻止索引
            if 'noindex' in content:
                issues.append({
                    'type': '頁面設定 noindex',
                    'message': '頁面設定了 noindex，將不會被搜尋引擎索引',
                    'severity': 'high',
                    'suggestion': '如果希望頁面被索引，請移除或修改 meta robots 標籤',
                    'current_value': f'目前值：{content}'
                })
            
            # 檢查是否阻止跟隨連結
            if 'nofollow' in content:
                issues.append({
                    'type': '頁面設定 nofollow',
                    'message': '頁面設定了 nofollow，搜尋引擎不會跟隨頁面上的連結',
                    'severity': 'medium',
                    'suggestion': '除非有特殊需求，否則不建議在整個頁面使用 nofollow',
                    'current_value': f'目前值：{content}'
                })
    
    def _check_hreflang(self, soup: BeautifulSoup, issues: list):
        """檢查 hreflang 標籤（多語言網站）"""
        hreflang_links = soup.find_all('link', rel='alternate', hreflang=True)
        
        if hreflang_links:
            # 檢查是否有 x-default
            has_x_default = any(
                link.get('hreflang') == 'x-default' 
                for link in hreflang_links
            )
            
            if not has_x_default:
                issues.append({
                    'type': '缺少 hreflang x-default',
                    'message': '多語言網站應包含 hreflang="x-default" 標籤',
                    'severity': 'low',
                    'suggestion': '添加 hreflang="x-default" 標籤，指定預設語言版本',
                    'current_value': f'現有語言數量：{len(hreflang_links)}'
                })
            
            # 檢查每個 hreflang 是否都有對應的 href
            for link in hreflang_links:
                if not link.get('href'):
                    issues.append({
                        'type': 'hreflang 缺少 href',
                        'message': f'hreflang 標籤缺少 href 屬性',
                        'severity': 'medium',
                        'suggestion': '確保每個 hreflang 標籤都有有效的 href 屬性'
                    })
                    break

