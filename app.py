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
from utils import calculate_total_score

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
]


@app.route('/')
def index():
    """提供前端頁面"""
    return send_from_directory('frontend', 'index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """提供靜態檔案（CSS、JS）"""
    return send_from_directory('frontend', filename)


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({'status': 'ok', 'message': 'SEO Analyzer is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    分析網址的 SEO
    
    Request JSON:
        {
            "url": "https://example.com"
        }
    
    Response JSON:
        {
            "url": "...",
            "total_score": 85.5,
            "grade": {...},
            "analysis_time": "2.3s",
            "results": [...],
            "summary": {...}
        }
    """
    try:
        # 取得網址
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': '請提供要分析的網址'}), 400
        
        url = data['url'].strip()
        
        # 驗證網址格式
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 記錄開始時間
        start_time = time.time()
        
        # 抓取網頁
        try:
            response = requests.get(
                url,
                timeout=ANALYZE_TIMEOUT,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; SEO-Analyzer/1.0)'
                }
            )
            response.raise_for_status()
            html = response.text
            
            # 檢查 HTML 大小
            if len(html) > MAX_HTML_SIZE:
                return jsonify({
                    'error': f'HTML 檔案過大（>{MAX_HTML_SIZE/1024/1024:.1f}MB），無法分析'
                }), 413
            
        except requests.Timeout:
            return jsonify({'error': '網頁載入超時，請稍後再試'}), 408
        except requests.ConnectionError:
            return jsonify({'error': '無法連線到此網站，請確認網址是否正確'}), 503
        except requests.HTTPError as e:
            return jsonify({'error': f'HTTP 錯誤：{e.response.status_code}'}), e.response.status_code
        except Exception as e:
            return jsonify({'error': f'抓取網頁時發生錯誤：{str(e)}'}), 500
        
        # 執行所有分析器
        analysis_results = []
        all_issues = []
        
        for analyzer in ANALYZERS:
            try:
                result = analyzer.analyze(html, url)
                analysis_results.append(result)
                all_issues.extend(result.issues)
            except Exception as e:
                app.logger.error(f'Analyzer {analyzer.name} failed: {e}')
                # 繼續執行其他分析器
        
        # 計算總分
        scoring = calculate_total_score(analysis_results)
        
        # 計算分析時間
        analysis_time = round(time.time() - start_time, 2)
        
        # 統計問題數量
        summary = {
            'critical': sum(1 for i in all_issues if i.severity == 'critical'),
            'high': sum(1 for i in all_issues if i.severity == 'high'),
            'medium': sum(1 for i in all_issues if i.severity == 'medium'),
            'low': sum(1 for i in all_issues if i.severity == 'low'),
            'total_issues': len(all_issues)
        }
        
        # 組裝回應
        response_data = {
            'url': url,
            'total_score': scoring['total_score'],
            'grade': scoring['grade'],
            'analysis_time': f'{analysis_time}s',
            'summary': summary,
            'category_scores': scoring['category_scores'],
            'results': [
                {
                    'category': r.category,
                    'score': r.score,
                    'issues': [
                        {
                            'severity': issue.severity,
                            'message': issue.message,
                            'suggestion': issue.suggestion,
                            'priority': issue.priority,
                            'code_example': issue.code_example,
                            'impact': issue.impact,
                            'difficulty': issue.difficulty
                        }
                        for issue in r.issues
                    ],
                    'metadata': r.metadata
                }
                for r in analysis_results
            ]
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        app.logger.error(f'Analysis failed: {e}', exc_info=True)
        return jsonify({'error': f'分析失敗：{str(e)}'}), 500


if __name__ == '__main__':
    # Railway 會設定 PORT 環境變數
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

