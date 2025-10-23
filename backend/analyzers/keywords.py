"""
Keywords Analyzer

分析網頁的關鍵字使用情況
"""

from bs4 import BeautifulSoup
from collections import Counter
import re
from .base import BaseAnalyzer, AnalysisResult


class KeywordsAnalyzer(BaseAnalyzer):
    """關鍵字分析器"""
    
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析關鍵字
        
        檢查項目：
        - 提取主要關鍵字
        - 計算關鍵字密度
        - 檢查關鍵字在重要位置的出現
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        issues = []
        score = 100
        metadata = {}
        
        # 移除 script 和 style 標籤
        for script in soup(['script', 'style']):
            script.decompose()
        
        # 提取文字內容
        text = soup.get_text()
        
        # 清理文字（移除多餘空白）
        text = re.sub(r'\s+', ' ', text).strip()
        total_words = len(text.split())
        metadata['total_words'] = total_words
        
        if total_words < 100:
            issues.append(self._create_issue(
                severity='high',
                message=f'網頁內容過少（{total_words} 個字）',
                suggestion='建議網頁內容至少 300-500 字，提供有價值的資訊',
                priority=2,
                impact='內容過少會被視為低品質頁面',
                difficulty='medium'
            ))
            score -= 30
        
        # 提取中文關鍵字（2-4 字的詞組）
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        
        # 提取英文關鍵字
        english_words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # 合併並計算頻率
        all_words = chinese_words + english_words
        word_freq_counter = Counter(all_words)
        
        # 移除常見停用詞（簡化版）
        stop_words = {'這個', '一個', '可以', '我們', '他們', '什麼', '怎麼', '為了', 'the', 'and', 'for', 'are', 'with'}
        word_freq = Counter({word: count for word, count in word_freq_counter.items() if word not in stop_words})
        
        # 取前 10 個最常見的關鍵字
        top_keywords = word_freq.most_common(10)
        metadata['top_keywords'] = [{'keyword': kw, 'count': count, 'density': round(count/total_words*100, 2)} for kw, count in top_keywords]
        
        # 檢查關鍵字密度
        if top_keywords:
            top_keyword, top_count = top_keywords[0]
            density = (top_count / total_words) * 100
            metadata['top_keyword'] = top_keyword
            metadata['top_keyword_density'] = round(density, 2)
            
            if density > 3:
                issues.append(self._create_issue(
                    severity='high',
                    message=f'關鍵字 "{top_keyword}" 密度過高（{density:.1f}%）',
                    suggestion='關鍵字密度建議控制在 1-2%，避免被視為關鍵字填充',
                    priority=2,
                    impact='過高的關鍵字密度可能被判定為垃圾內容',
                    difficulty='medium'
                ))
                score -= 20
        
        # 檢查主要關鍵字是否出現在重要位置
        if top_keywords:
            top_keyword = top_keywords[0][0]
            
            # 檢查 title
            title_tag = soup.find('title')
            title_text = title_tag.get_text() if title_tag else ''
            
            # 檢查 H1
            h1_tag = soup.find('h1')
            h1_text = h1_tag.get_text() if h1_tag else ''
            
            # 檢查 meta description
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            desc_text = desc_tag.get('content', '') if desc_tag else ''
            
            in_important_places = {
                'title': top_keyword in title_text,
                'h1': top_keyword in h1_text,
                'description': top_keyword in desc_text
            }
            
            metadata['keyword_in_important_places'] = in_important_places
            
            missing_places = [place for place, found in in_important_places.items() if not found]
            
            if missing_places:
                issues.append(self._create_issue(
                    severity='medium',
                    message=f'主要關鍵字 "{top_keyword}" 未出現在：{", ".join(missing_places)}',
                    suggestion='建議在 title、H1 和 meta description 中都包含主要關鍵字',
                    priority=3,
                    impact='關鍵字應該出現在重要位置以強化相關性',
                    difficulty='easy'
                ))
                score -= 10
        
        return AnalysisResult(
            category='keywords',
            score=max(0, score),
            issues=issues,
            metadata=metadata
        )

