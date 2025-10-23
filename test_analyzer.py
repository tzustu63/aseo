#!/usr/bin/env python3
"""
Simple test script for SEO Analyzer
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from analyzers import (
    TitleAnalyzer,
    MetaAnalyzer,
    HeadingsAnalyzer,
    ImagesAnalyzer,
    KeywordsAnalyzer,
    StructureAnalyzer,
    PerformanceAnalyzer,
    MobileAnalyzer
)
from utils import calculate_total_score, get_grade

# 測試 HTML
test_html = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="這是一個測試網頁的描述，用來測試 SEO 分析工具是否正常運作。描述長度應該在 150-160 字元之間，這樣才能在搜尋結果中完整顯示。">
    <title>測試網頁標題 - SEO 分析工具測試頁面</title>
</head>
<body>
    <header>
        <h1>這是主標題 H1</h1>
    </header>
    <main>
        <h2>次標題 H2</h2>
        <p>這是一段測試內容。SEO 優化 SEO 優化 SEO 優化。關鍵字分析測試。</p>
        <img src="test.jpg" alt="測試圖片的描述">
        <h3>小標題 H3</h3>
        <p>更多內容...</p>
    </main>
    <footer>
        <p>頁尾資訊</p>
    </footer>
</body>
</html>
"""

def main():
    print("="*60)
    print("SEO ANALYZER - SYSTEM TEST")
    print("="*60)
    
    # 測試所有分析器
    analyzers = [
        TitleAnalyzer(),
        MetaAnalyzer(),
        HeadingsAnalyzer(),
        ImagesAnalyzer(),
        KeywordsAnalyzer(),
        StructureAnalyzer(),
        PerformanceAnalyzer(),
        MobileAnalyzer(),
    ]
    
    test_url = "https://example.com"
    results = []
    
    print("\n測試分析器...")
    for analyzer in analyzers:
        try:
            result = analyzer.analyze(test_html, test_url)
            results.append(result)
            print(f"✓ {analyzer.name}: {result.category} (分數: {result.score}, 問題數: {len(result.issues)})")
        except Exception as e:
            print(f"✗ {analyzer.name} 失敗: {e}")
            return False
    
    # 測試評分系統
    print("\n測試評分系統...")
    try:
        scoring = calculate_total_score(results)
        print(f"✓ 總分計算成功: {scoring['total_score']}/100")
        print(f"✓ 等級: {scoring['grade']['level']} {scoring['grade']['stars']}")
    except Exception as e:
        print(f"✗ 評分系統失敗: {e}")
        return False
    
    # 顯示結果摘要
    print("\n分析結果摘要：")
    print(f"  總分: {scoring['total_score']}/100")
    print(f"  等級: {scoring['grade']['level']}")
    print(f"  各項目分數:")
    for category, score in scoring['category_scores'].items():
        print(f"    - {category}: {score}")
    
    total_issues = sum(len(r.issues) for r in results)
    print(f"  發現問題數: {total_issues}")
    
    print("\n" + "="*60)
    print("✅ 所有測試通過！SEO 分析器準備就緒。")
    print("="*60)
    print("\n下一步：")
    print("1. 執行 Flask 應用: python3 app.py")
    print("2. 開啟瀏覽器: http://localhost:5000")
    print("3. 部署到 Railway")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

