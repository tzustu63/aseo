"""
Base Analyzer Class

所有 SEO 分析器的基礎類別
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Issue:
    """SEO 問題資料類別"""
    severity: str  # critical, high, medium, low
    message: str  # 問題描述
    suggestion: str  # 優化建議
    priority: int  # 優先順序 (1=最高)
    code_example: Optional[str] = None  # 程式碼範例
    impact: Optional[str] = None  # 影響程度說明
    difficulty: Optional[str] = None  # 實作難度 (easy, medium, hard)
    fixable_type: Optional[str] = None  # 可修復類型 (auto, ai, manual)
    fix_data: Optional[Dict[str, Any]] = None  # 修復所需資料


@dataclass
class AnalysisResult:
    """分析結果資料類別"""
    category: str  # 分析類別名稱
    score: int  # 0-100 分
    issues: List[Issue] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)  # 額外資訊
    
    @property
    def passed(self) -> bool:
        """是否通過檢查（沒有 critical 或 high 問題）"""
        return not any(i.severity in ['critical', 'high'] for i in self.issues)
    
    @property
    def critical_count(self) -> int:
        """嚴重問題數量"""
        return sum(1 for i in self.issues if i.severity == 'critical')
    
    @property
    def high_count(self) -> int:
        """重要問題數量"""
        return sum(1 for i in self.issues if i.severity == 'high')
    
    @property
    def medium_count(self) -> int:
        """中等問題數量"""
        return sum(1 for i in self.issues if i.severity == 'medium')
    
    @property
    def low_count(self) -> int:
        """輕微問題數量"""
        return sum(1 for i in self.issues if i.severity == 'low')


class BaseAnalyzer(ABC):
    """
    SEO 分析器基礎類別
    
    所有分析器都必須繼承此類別並實作 analyze 方法
    """
    
    def __init__(self):
        self.name = self.__class__.__name__
    
    @abstractmethod
    def analyze(self, html: str, url: str) -> AnalysisResult:
        """
        分析網頁並回傳結果
        
        Args:
            html: 網頁 HTML 內容
            url: 網頁網址
            
        Returns:
            AnalysisResult: 分析結果
        """
        pass
    
    def _create_issue(
        self,
        severity: str,
        message: str,
        suggestion: str,
        priority: int,
        code_example: Optional[str] = None,
        impact: Optional[str] = None,
        difficulty: Optional[str] = None,
        fixable_type: Optional[str] = None,
        fix_data: Optional[Dict[str, Any]] = None
    ) -> Issue:
        """
        建立問題物件的輔助方法
        
        Args:
            severity: 嚴重性等級
            message: 問題描述
            suggestion: 優化建議
            priority: 優先順序
            code_example: 程式碼範例（可選）
            impact: 影響說明（可選）
            difficulty: 難度（可選）
            fixable_type: 可修復類型 (auto/ai/manual)（可選）
            fix_data: 修復所需資料（可選）
            
        Returns:
            Issue: 問題物件
        """
        return Issue(
            severity=severity,
            message=message,
            suggestion=suggestion,
            priority=priority,
            code_example=code_example,
            impact=impact,
            difficulty=difficulty,
            fixable_type=fixable_type,
            fix_data=fix_data
        )

