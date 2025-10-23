"""
Images Analyzer

分析網頁的圖片優化狀況
"""

from bs4 import BeautifulSoup
from .base import BaseAnalyzer, AnalysisResult


class ImagesAnalyzer(BaseAnalyzer):
    """圖片優化分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析圖片優化
        
        檢查項目：
        - 圖片 alt 屬性
        - alt 文字品質
        - 圖片數量統計
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        issues = []
        score = 100
        metadata = {}
        
        # 找出所有圖片
        images = soup.find_all('img')
        total_images = len(images)
        metadata['total_images'] = total_images
        
        if total_images == 0:
            # 沒有圖片，不扣分也不加分
            metadata['images_with_alt'] = 0
            metadata['images_without_alt'] = 0
            return AnalysisResult(
                category='images',
                score=100,
                issues=[],
                metadata=metadata
            )
        
        # 檢查 alt 屬性
        images_without_alt = []
        images_with_empty_alt = []
        images_with_poor_alt = []
        
        for img in images:
            alt = img.get('alt')
            src = img.get('src', '')[:50]  # 取前 50 字元顯示
            
            if alt is None:
                images_without_alt.append(src)
            elif not alt.strip():
                images_with_empty_alt.append(src)
            elif alt.strip().lower() in ['image', 'img', 'picture', 'photo', '圖片', '照片']:
                images_with_poor_alt.append(src)
        
        metadata['images_with_alt'] = total_images - len(images_without_alt)
        metadata['images_without_alt'] = len(images_without_alt)
        metadata['images_with_empty_alt'] = len(images_with_empty_alt)
        metadata['images_with_poor_alt'] = len(images_with_poor_alt)
        
        # 缺少 alt 屬性
        if images_without_alt:
            issues.append(self._create_issue(
                severity='high',
                message=f'{len(images_without_alt)} 張圖片缺少 alt 屬性',
                suggestion='為所有圖片加入描述性的 alt 文字',
                priority=2,
                code_example=f'<!-- 範例 -->\n<img src="product.jpg" alt="產品名稱的詳細描述">',
                impact='缺少 alt 會影響視障使用者體驗和圖片搜尋 SEO',
                difficulty='easy'
            ))
            score -= min(30, len(images_without_alt) * 10)  # 最多扣 30 分
        
        # alt 為空
        if images_with_empty_alt:
            issues.append(self._create_issue(
                severity='medium',
                message=f'{len(images_with_empty_alt)} 張圖片的 alt 屬性為空',
                suggestion='為這些圖片加入有意義的 alt 文字',
                priority=3,
                code_example='<img src="banner.jpg" alt="公司年度活動宣傳橫幅">',
                impact='空白 alt 無法提供圖片資訊給搜尋引擎',
                difficulty='easy'
            ))
            score -= min(20, len(images_with_empty_alt) * 5)
        
        # alt 文字品質不佳
        if images_with_poor_alt:
            issues.append(self._create_issue(
                severity='low',
                message=f'{len(images_with_poor_alt)} 張圖片的 alt 文字不夠具體',
                suggestion='避免使用 "image"、"圖片" 等通用詞彙，使用具體描述',
                priority=4,
                code_example='<!-- 不好：<img alt="圖片"> -->\n<!-- 良好：<img alt="產品展示照片 - 藍色款式"> -->',
                impact='通用的 alt 文字提供的資訊價值較低',
                difficulty='easy'
            ))
            score -= min(10, len(images_with_poor_alt) * 3)
        
        # 如果所有圖片都有良好的 alt，給予鼓勵訊息
        if total_images > 0 and not issues:
            metadata['note'] = f'很好！所有 {total_images} 張圖片都有適當的 alt 屬性'
        
        return AnalysisResult(
            category='images',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

