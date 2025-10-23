"""
Structured Data Analyzer

分析結構化資料（Schema.org）
- JSON-LD
- Microdata
- RDFa
- Open Graph
- Twitter Cards
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult
import json
import re

class StructuredDataAnalyzer(BaseAnalyzer):
    """結構化資料分析器"""
    
    def __init__(self):
        super().__init__()
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析結構化資料
        
        Args:
            html: HTML 內容
            url: 頁面 URL
            
        Returns:
            分析結果
        """
        soup = BeautifulSoup(html, 'html.parser')
        issues_data = []
        score = 100
        
        # 檢查 JSON-LD
        has_jsonld = self._check_jsonld(soup, issues_data)
        
        # 檢查 Open Graph 標籤
        has_og = self._check_open_graph(soup, issues_data)
        
        # 檢查 Twitter Cards
        has_twitter = self._check_twitter_cards(soup, issues_data)
        
        # 檢查 Microdata
        has_microdata = self._check_microdata(soup, issues_data)
        
        # 如果完全沒有結構化資料，扣重分
        if not (has_jsonld or has_og or has_twitter or has_microdata):
            issues_data.append({
                'type': '缺少結構化資料',
                'message': '頁面完全沒有使用任何結構化資料標記',
                'severity': 'high',
                'suggestion': '添加 JSON-LD 結構化資料，以幫助搜尋引擎更好地理解頁面內容，並獲得豐富搜尋結果 (Rich Snippets)'
            })
            score -= 30
        
        # 計算最終分數
        score = max(0, score - (len(issues_data) * 8))
        
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
            category='structured_data',
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
    
    def _check_jsonld(self, soup: BeautifulSoup, issues: list) -> bool:
        """檢查 JSON-LD 結構化資料"""
        jsonld_scripts = soup.find_all('script', type='application/ld+json')
        
        if not jsonld_scripts:
            issues.append({
                'type': '缺少 JSON-LD',
                'message': '未發現 JSON-LD 結構化資料',
                'severity': 'high',
                'suggestion': '添加 JSON-LD 標記（如 Organization, WebSite, Article 等），這是 Google 推薦的結構化資料格式'
            })
            return False
        
        # 驗證 JSON-LD 格式
        valid_count = 0
        for script in jsonld_scripts:
            try:
                data = json.loads(script.string)
                valid_count += 1
                
                # 檢查常見類型
                if isinstance(data, dict):
                    schema_type = data.get('@type', '')
                    if not schema_type:
                        issues.append({
                            'type': 'JSON-LD 缺少 @type',
                            'message': 'JSON-LD 結構化資料缺少 @type 屬性',
                            'severity': 'medium',
                            'suggestion': '確保 JSON-LD 包含正確的 @type（如 Article, Product, Organization 等）'
                        })
                
            except json.JSONDecodeError:
                issues.append({
                    'type': 'JSON-LD 格式錯誤',
                    'message': 'JSON-LD 結構化資料格式不正確',
                    'severity': 'high',
                    'suggestion': '修正 JSON-LD 語法錯誤，可使用 Google Rich Results Test 驗證'
                })
        
        return valid_count > 0
    
    def _check_open_graph(self, soup: BeautifulSoup, issues: list) -> bool:
        """檢查 Open Graph 標籤"""
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        
        if not og_tags:
            issues.append({
                'type': '缺少 Open Graph 標籤',
                'message': '未發現 Open Graph (og:) 標籤',
                'severity': 'medium',
                'suggestion': '添加 Open Graph 標籤（og:title, og:description, og:image 等），以優化社群媒體分享效果'
            })
            return False
        
        # 檢查必要的 OG 標籤
        required_og = ['og:title', 'og:type', 'og:image', 'og:url']
        existing_og = [tag.get('property') for tag in og_tags]
        
        missing_og = [prop for prop in required_og if prop not in existing_og]
        
        if missing_og:
            issues.append({
                'type': '缺少必要的 OG 標籤',
                'message': f'缺少必要的 Open Graph 標籤：{", ".join(missing_og)}',
                'severity': 'medium',
                'suggestion': f'添加缺少的 Open Graph 標籤：{", ".join(missing_og)}',
                'current_value': f'現有標籤數量：{len(existing_og)}'
            })
        
        # 檢查 og:image 尺寸建議
        og_image = soup.find('meta', property='og:image')
        if og_image:
            og_image_width = soup.find('meta', property='og:image:width')
            og_image_height = soup.find('meta', property='og:image:height')
            
            if not og_image_width or not og_image_height:
                issues.append({
                    'type': 'OG 圖片缺少尺寸',
                    'message': 'og:image 未指定 width 和 height',
                    'severity': 'low',
                    'suggestion': '添加 og:image:width 和 og:image:height，建議尺寸為 1200x630 像素'
                })
        
        return True
    
    def _check_twitter_cards(self, soup: BeautifulSoup, issues: list) -> bool:
        """檢查 Twitter Cards"""
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        
        if not twitter_tags:
            issues.append({
                'type': '缺少 Twitter Cards',
                'message': '未發現 Twitter Card 標籤',
                'severity': 'low',
                'suggestion': '添加 Twitter Card 標籤（twitter:card, twitter:title, twitter:description 等），以優化 Twitter 分享效果'
            })
            return False
        
        # 檢查 twitter:card 類型
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        
        if not twitter_card:
            issues.append({
                'type': '缺少 Twitter Card 類型',
                'message': '未指定 Twitter Card 類型 (twitter:card)',
                'severity': 'low',
                'suggestion': '添加 <meta name="twitter:card" content="summary_large_image">，以啟用 Twitter 卡片功能'
            })
        
        return True
    
    def _check_microdata(self, soup: BeautifulSoup, issues: list) -> bool:
        """檢查 Microdata"""
        itemscope_elements = soup.find_all(attrs={'itemscope': True})
        
        if itemscope_elements:
            # 檢查是否有正確的 itemtype
            missing_itemtype = []
            for element in itemscope_elements:
                if not element.get('itemtype'):
                    missing_itemtype.append(element.name)
            
            if missing_itemtype:
                issues.append({
                    'type': 'Microdata 缺少 itemtype',
                    'message': f'部分 itemscope 元素缺少 itemtype 屬性',
                    'severity': 'medium',
                    'suggestion': '為所有 itemscope 元素添加正確的 itemtype（如 https://schema.org/Article）'
                })
            
            return True
        
        return False

