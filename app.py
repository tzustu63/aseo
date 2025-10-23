"""
SEO Analyzer Flask Application

主要的 Flask 應用程式，提供 SEO 分析 API
"""

import os
import sys
import time
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# 將 backend 目錄加入 Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dataclasses import asdict
from analyzers import (
    TitleAnalyzer,
    MetaAnalyzer,
    HeadingsAnalyzer,
    ImagesAnalyzer,
    KeywordsAnalyzer,
    StructureAnalyzer,
    PerformanceAnalyzer,
    MobileAnalyzer,
    CoreWebVitalsAnalyzer,
    StructuredDataAnalyzer,
    LinksAnalyzer,
    CrawlabilityAnalyzer
)
from utils import calculate_total_score
from ai_enhancement import SEOAIEnhancer, test_openai_key

# 初始化 Flask 應用
app = Flask(__name__, static_folder='frontend')
CORS(app)  # 允許跨域請求

# 設定環境變數
ANALYZE_TIMEOUT = int(os.environ.get('ANALYZE_TIMEOUT', 10))
MAX_HTML_SIZE = int(os.environ.get('MAX_HTML_SIZE', 5 * 1024 * 1024))  # 5MB

# 初始化所有分析器
ANALYZERS = [
    TitleAnalyzer(),
    MetaAnalyzer(),
    HeadingsAnalyzer(),
    ImagesAnalyzer(),
    KeywordsAnalyzer(),
    StructureAnalyzer(),
    PerformanceAnalyzer(),
    MobileAnalyzer(),
    CoreWebVitalsAnalyzer(),
    StructuredDataAnalyzer(),
    LinksAnalyzer(),
    CrawlabilityAnalyzer(),
]

@app.route('/api/test-openai', methods=['POST'])
def test_openai():
    """
    測試 OpenAI API Key
    
    Request JSON:
        {
            "api_key": "sk-..."
        }
    
    Response JSON:
        {
            "success": true,
            "message": "API Key 有效"
        }
    """
    try:
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        
        result = test_openai_key(api_key)
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f'OpenAI test failed: {e}', exc_info=True)
        return jsonify({
            'success': False,
            'message': f'測試失敗：{str(e)}'
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """
    分析指定 URL 的 SEO 狀況
    
    Request JSON:
        {
            "url": "https://example.com",
            "openai_api_key": "sk-..." (optional),
            "use_ai_enhancement": true (optional)
        }
    
    Response JSON:
        {
            "success": true,
            "url": "https://example.com",
            "total_score": 85,
            "ai_enhanced": true,
            "results": [
                {
                    "category": "title",
                    "score": 90,
                    "issues": [...]
                }
            ]
        }
    """
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        openai_api_key = data.get('openai_api_key', '').strip()
        use_ai_enhancement = data.get('use_ai_enhancement', False)
        
        if not url:
            return jsonify({'error': '請提供要分析的 URL'}), 400
        
        # 驗證 URL 格式
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"開始分析 URL: {url}")
        start_time = time.time()
        
        # 獲取頁面內容
        try:
            response = requests.get(url, timeout=ANALYZE_TIMEOUT, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            # 檢查 HTML 大小
            if len(response.content) > MAX_HTML_SIZE:
                return jsonify({
                    'error': f'頁面太大（超過 {MAX_HTML_SIZE // 1024 // 1024}MB），無法分析'
                }), 400
            
            html_content = response.text
            
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'無法獲取頁面內容：{str(e)}'}), 400
        
        # 初始化 AI 增強器（如果需要）
        ai_enhancer = None
        if use_ai_enhancement and openai_api_key:
            try:
                ai_enhancer = SEOAIEnhancer(openai_api_key)
                print("🤖 已啟用 AI 深度分析模式（12 次呼叫）")
            except Exception as e:
                print(f"AI 增強器初始化失敗: {e}")
        
        # 第一階段：執行所有基本分析
        print("\n📊 第一階段：執行 12 項基本分析...")
        results = []
        results_dict = []
        total_score = 0
        ai_enhanced = False
        
        for i, analyzer in enumerate(ANALYZERS, 1):
            try:
                print(f"  [{i}/12] {analyzer.__class__.__name__}...", end=" ")
                
                # 執行分析
                result = analyzer.analyze(html_content, url)
                results.append(result)
                total_score += result.score
                print(f"✓ ({result.score}分)")
                
                # 轉換為字典
                result_dict = {
                    'category': result.category,
                    'score': result.score,
                    'issues': []
                }
                for issue in result.issues:
                    issue_dict = {
                        'type': issue.message.split('：')[0] if '：' in issue.message else issue.message.split(':')[0] if ':' in issue.message else 'SEO 問題',
                        'message': issue.message,
                        'severity': issue.severity,
                        'suggestion': issue.suggestion
                    }
                    if hasattr(issue, 'code_example') and issue.code_example:
                        issue_dict['code_example'] = issue.code_example
                    result_dict['issues'].append(issue_dict)
                
                results_dict.append(result_dict)
                
            except Exception as e:
                print(f"✗ 失敗")
                print(f"  錯誤：{e}")
                import traceback
                traceback.print_exc()
                # 即使某個分析器失敗，也繼續執行其他分析器
                from analyzers.base import AnalysisResult, Issue
                result = AnalysisResult(
                    category=analyzer.__class__.__name__.lower().replace('analyzer', ''),
                    score=0,
                    issues=[Issue(
                        severity='high',
                        message=f'分析器執行失敗：{str(e)}',
                        suggestion='請檢查錯誤訊息或聯絡支援',
                        priority=1
                    )]
                )
                results.append(result)
                results_dict.append({
                    'category': result.category,
                    'score': 0,
                    'issues': [{'type': '錯誤', 'message': f'分析失敗：{str(e)}', 'severity': 'high', 'suggestion': '請重試'}]
                })
        
        print(f"\n✓ 基本分析完成！")
        
        # 第二階段：平行 AI 增強
        if ai_enhancer:
            # 統計需要 AI 分析的項目
            needs_ai = sum(1 for r in results_dict if r.get('issues'))
            if needs_ai > 0:
                print(f"\n🤖 第二階段：AI 深度分析（平行處理 3 項）")
                try:
                    results_dict = ai_enhancer.enhance_multiple_categories_parallel(
                        url, 
                        results_dict, 
                        html_content,
                        max_workers=3  # 同時處理 3 項
                    )
                    ai_enhanced = True
                except Exception as e:
                    print(f"\n✗ 平行 AI 分析失敗：{e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"\n✓ 所有項目都沒有問題，無需 AI 分析")
        
        # 計算總分
        if results:
            total_score = calculate_total_score(results)
        
        analysis_time = time.time() - start_time
        print(f"\n✓ 分析完成，耗時：{analysis_time:.2f}秒，總分：{total_score}")
        
        response_data = {
            'success': True,
            'url': url,
            'total_score': total_score['total_score'] if isinstance(total_score, dict) else total_score,
            'analysis_time': round(analysis_time, 2),
            'results': results_dict,
            'ai_enhanced': ai_enhanced,
            'timestamp': time.time()
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        app.logger.error(f'Analysis failed: {e}', exc_info=True)
        return jsonify({'error': f'分析失敗：{str(e)}'}), 500


@app.route('/health')
def health_check():
    """健康檢查端點（Railway 使用）"""
    return jsonify({
        'status': 'healthy',
        'service': 'SEO Analyzer',
        'analyzers': len(ANALYZERS),
        'version': '2.0'
    }), 200

@app.route('/favicon.ico')
def favicon():
    """處理 favicon 請求，避免 404 錯誤"""
    return '', 204  # No Content

@app.route('/')
def index():
    """提供前端頁面"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """提供靜態檔案"""
    return send_from_directory('frontend', filename)


if __name__ == '__main__':
    # Railway 會設定 PORT 環境變數，本機開發使用 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)