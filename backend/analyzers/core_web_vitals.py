"""
Core Web Vitals Analyzer

分析 Google Core Web Vitals 相關指標
- LCP (Largest Contentful Paint) - 最大內容繪製
- FID (First Input Delay) - 首次輸入延遲  
- CLS (Cumulative Layout Shift) - 累積版面配置轉移
- TTFB (Time to First Byte) - 首位元組時間
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult
import time

class CoreWebVitalsAnalyzer(BaseAnalyzer):
    """Core Web Vitals 分析器"""
    
    def __init__(self):
        super().__init__()
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析 Core Web Vitals
        
        Args:
            html: HTML 內容
            url: 頁面 URL
            
        Returns:
            分析結果
        """
        soup = BeautifulSoup(html, 'html.parser')
        issues_data = []
        score = 100
        
        # 檢查關鍵資源
        self._check_critical_resources(soup, issues_data)
        
        # 檢查圖片優化
        self._check_image_optimization(soup, issues_data)
        
        # 檢查 JavaScript 延遲載入
        self._check_js_defer(soup, issues_data)
        
        # 檢查 CSS 優化
        self._check_css_optimization(soup, issues_data)
        
        # 檢查字體優化
        self._check_font_optimization(soup, issues_data)
        
        # 檢查版面配置穩定性
        self._check_layout_stability(soup, issues_data)
        
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
            category='core_web_vitals',
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
    
    def _check_critical_resources(self, soup: BeautifulSoup, issues: list):
        """檢查關鍵資源預載入"""
        # 檢查是否有 preload 連結
        preload_links = soup.find_all('link', rel='preload')
        
        if len(preload_links) == 0:
            issues.append({
                'type': '缺少資源預載入',
                'message': '未使用 <link rel="preload"> 預載入關鍵資源',
                'severity': 'medium',
                'suggestion': '使用 rel="preload" 預載入關鍵的 CSS、字體和圖片，以改善 LCP'
            })
        
        # 檢查是否有 DNS 預連接
        preconnect_links = soup.find_all('link', rel='preconnect')
        
        if len(preconnect_links) == 0:
            issues.append({
                'type': '缺少 DNS 預連接',
                'message': '未使用 <link rel="preconnect"> 預連接到第三方網域',
                'severity': 'low',
                'suggestion': '對於 Google Fonts、CDN 等第三方資源，使用 rel="preconnect" 可以減少連線時間'
            })
    
    def _check_image_optimization(self, soup: BeautifulSoup, issues: list):
        """檢查圖片優化對 LCP 的影響"""
        images = soup.find_all('img')
        large_images_without_lazy = []
        
        for img in images:
            # 檢查是否有 loading="lazy"
            loading = img.get('loading', '')
            width = img.get('width', '')
            height = img.get('height', '')
            
            # 如果是大圖但沒有尺寸屬性，可能影響 CLS
            if not width or not height:
                issues.append({
                    'type': '圖片缺少尺寸屬性',
                    'message': f'圖片 {img.get("src", "未知")} 缺少 width 和 height 屬性',
                    'severity': 'high',
                    'current_value': f'src: {img.get("src", "未知")}',
                    'suggestion': '為所有圖片添加 width 和 height 屬性，以防止版面配置位移 (CLS)'
                })
                break  # 只報告一次
        
        # 檢查是否使用現代圖片格式
        webp_images = [img for img in images if img.get('src', '').endswith('.webp')]
        
        if images and len(webp_images) == 0:
            issues.append({
                'type': '未使用現代圖片格式',
                'message': '未使用 WebP 或 AVIF 等現代圖片格式',
                'severity': 'medium',
                'suggestion': '將 JPEG 和 PNG 圖片轉換為 WebP 格式，可減少 30-80% 的檔案大小，改善 LCP'
            })
    
    def _check_js_defer(self, soup: BeautifulSoup, issues: list):
        """檢查 JavaScript 延遲載入"""
        scripts = soup.find_all('script', src=True)
        blocking_scripts = []
        
        for script in scripts:
            # 檢查是否有 defer 或 async 屬性
            if not script.get('defer') and not script.get('async'):
                blocking_scripts.append(script.get('src', ''))
        
        if blocking_scripts:
            issues.append({
                'type': 'JavaScript 阻塞渲染',
                'message': f'發現 {len(blocking_scripts)} 個阻塞渲染的 JavaScript 檔案',
                'severity': 'high',
                'suggestion': '為非關鍵的 JavaScript 添加 defer 或 async 屬性，以改善 FID 和 LCP',
                'current_value': f'阻塞腳本數量: {len(blocking_scripts)}'
            })
    
    def _check_css_optimization(self, soup: BeautifulSoup, issues: list):
        """檢查 CSS 優化"""
        css_links = soup.find_all('link', rel='stylesheet')
        
        if len(css_links) > 3:
            issues.append({
                'type': 'CSS 檔案過多',
                'message': f'發現 {len(css_links)} 個外部 CSS 檔案',
                'severity': 'medium',
                'suggestion': '合併 CSS 檔案並內嵌關鍵 CSS，以減少渲染阻塞時間',
                'current_value': f'CSS 檔案數量: {len(css_links)}'
            })
        
        # 檢查是否有內嵌關鍵 CSS
        style_tags = soup.find_all('style')
        
        if len(style_tags) == 0 and len(css_links) > 0:
            issues.append({
                'type': '缺少內嵌關鍵 CSS',
                'message': '未發現內嵌的關鍵 CSS',
                'severity': 'medium',
                'suggestion': '將首屏渲染所需的 CSS 內嵌到 HTML 中，以加快首次繪製速度 (FCP)'
            })
    
    def _check_font_optimization(self, soup: BeautifulSoup, issues: list):
        """檢查字體優化"""
        # 檢查 Google Fonts 或其他外部字體
        font_links = soup.find_all('link', href=lambda x: x and 'fonts' in x.lower())
        
        if font_links:
            # 檢查是否使用 font-display
            has_font_display = False
            for link in font_links:
                if 'display=swap' in link.get('href', ''):
                    has_font_display = True
                    break
            
            if not has_font_display:
                issues.append({
                    'type': '字體載入未優化',
                    'message': '使用外部字體但未設定 font-display: swap',
                    'severity': 'medium',
                    'suggestion': '在 Google Fonts URL 中添加 &display=swap，或在 @font-face 中設定 font-display: swap，以避免文字閃爍 (FOIT)'
                })
    
    def _check_layout_stability(self, soup: BeautifulSoup, issues: list):
        """檢查版面配置穩定性（CLS 相關）"""
        # 檢查是否有未設定尺寸的 iframe
        iframes = soup.find_all('iframe')
        unstable_iframes = []
        
        for iframe in iframes:
            if not iframe.get('width') or not iframe.get('height'):
                unstable_iframes.append(iframe.get('src', '未知'))
        
        if unstable_iframes:
            issues.append({
                'type': 'iframe 缺少尺寸',
                'message': f'發現 {len(unstable_iframes)} 個未設定尺寸的 iframe',
                'severity': 'high',
                'suggestion': '為所有 iframe 設定明確的 width 和 height，以防止版面配置位移 (CLS)',
                'current_value': f'受影響的 iframe 數量: {len(unstable_iframes)}'
            })
        
        # 檢查是否有動態插入的內容（廣告、嵌入內容等）
        ad_containers = soup.find_all(['div', 'ins'], class_=lambda x: x and ('ad' in x.lower() or 'banner' in x.lower()))
        
        if ad_containers:
            has_reserved_space = all(
                container.get('style') and ('height' in container.get('style', '') or 'min-height' in container.get('style', ''))
                for container in ad_containers
            )
            
            if not has_reserved_space:
                issues.append({
                    'type': '廣告容器未預留空間',
                    'message': '發現廣告容器但未預留固定空間',
                    'severity': 'medium',
                    'suggestion': '為廣告容器預留固定的空間（使用 min-height），以防止廣告載入時造成版面位移 (CLS)'
                })

