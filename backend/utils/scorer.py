"""
SEO Scoring System

計算 SEO 總分和等級
"""

from typing import Dict, List

# 條件式 import 以支援不同的執行方式
try:
    from ..analyzers.base import AnalysisResult
except ImportError:
    from analyzers.base import AnalysisResult


# 各項目權重（總和為 1.0）
WEIGHTS = {
    'title': 0.15,        # Title 標籤 15%
    'meta_tags': 0.15,    # Meta 標籤 15%
    'headings': 0.15,     # 標題結構 15%
    'keywords': 0.10,     # 關鍵字 10%
    'images': 0.10,       # 圖片優化 10%
    'structure': 0.15,    # HTML 結構 15%
    'performance': 0.10,  # 效能 10%
    'mobile': 0.10,       # 行動裝置 10%
}


def calculate_total_score(results: List[AnalysisResult]) -> Dict:
    """
    計算加權總分
    
    Args:
        results: 所有分析器的結果列表
        
    Returns:
        Dict: 包含總分、等級、各項目分數等資訊
    """
    category_scores = {}
    
    # 收集各類別分數
    for result in results:
        category_scores[result.category] = result.score
    
    # 計算加權總分
    total_score = 0
    weighted_breakdown = {}
    
    for category, weight in WEIGHTS.items():
        score = category_scores.get(category, 0)
        weighted_score = score * weight
        total_score += weighted_score
        weighted_breakdown[category] = {
            'score': score,
            'weight': weight,
            'weighted_score': round(weighted_score, 2)
        }
    
    total_score = round(total_score, 1)
    
    # 計算等級
    grade = get_grade(total_score)
    
    return {
        'total_score': total_score,
        'grade': grade,
        'category_scores': category_scores,
        'weighted_breakdown': weighted_breakdown
    }


def get_grade(score: float) -> Dict[str, str]:
    """
    根據分數取得等級
    
    Args:
        score: SEO 總分（0-100）
        
    Returns:
        Dict: 包含等級、星級、說明
    """
    if score >= 90:
        return {
            'level': '優秀',
            'stars': '⭐⭐⭐⭐⭐',
            'description': '您的網頁 SEO 狀況優秀！繼續保持。'
        }
    elif score >= 70:
        return {
            'level': '良好',
            'stars': '⭐⭐⭐⭐',
            'description': '您的網頁 SEO 狀況良好，還有一些小地方可以優化。'
        }
    elif score >= 50:
        return {
            'level': '普通',
            'stars': '⭐⭐⭐',
            'description': '您的網頁有一些 SEO 問題需要處理。'
        }
    elif score >= 30:
        return {
            'level': '待改善',
            'stars': '⭐⭐',
            'description': '您的網頁有多處 SEO 問題，建議盡快優化。'
        }
    else:
        return {
            'level': '需大幅優化',
            'stars': '⭐',
            'description': '您的網頁有嚴重的 SEO 問題，需要大幅度改善。'
        }

