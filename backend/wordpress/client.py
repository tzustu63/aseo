"""
WordPress REST API Client

提供 WordPress 網站連線和內容更新功能
"""
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse


class WordPressClient:
    """WordPress REST API 客戶端"""
    
    def __init__(self, site_url: str, username: str, app_password: str):
        """
        初始化 WordPress 客戶端
        
        Args:
            site_url: WordPress 網站網址（例如：https://example.com）
            username: WordPress 使用者名稱
            app_password: Application Password（從 WordPress 後台產生）
        """
        self.site_url = site_url.rstrip('/')
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.auth = HTTPBasicAuth(username, app_password)
        self.timeout = 15
    
    def test_connection(self) -> Dict[str, Any]:
        """
        測試 WordPress 連線
        
        Returns:
            連線結果 {'success': bool, 'message': str, 'site_info': dict}
        """
        try:
            # 測試連線：取得網站資訊
            response = requests.get(
                f"{self.site_url}/wp-json",
                auth=self.auth,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 測試編輯權限
            permission_test = self._test_edit_permissions()
            
            return {
                'success': True,
                'message': '連線成功',
                'site_info': {
                    'name': data.get('name', ''),
                    'description': data.get('description', ''),
                    'url': data.get('url', ''),
                    'namespaces': data.get('namespaces', [])
                },
                'permissions': permission_test
            }
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return {
                    'success': False,
                    'message': '認證失敗，請檢查使用者名稱和 Application Password'
                }
            else:
                return {
                    'success': False,
                    'message': f'HTTP 錯誤：{e.response.status_code}'
                }
        
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'message': '無法連線到 WordPress 網站，請確認網址是否正確'
            }
        
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'message': '連線超時，請稍後再試'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'連線錯誤：{str(e)}'
            }
    
    def _test_edit_permissions(self) -> Dict[str, Any]:
        """測試編輯權限"""
        try:
            # 嘗試獲取一個頁面來測試權限
            pages_response = requests.get(
                f"{self.api_base}/pages",
                auth=self.auth,
                params={'per_page': 1, 'status': 'publish'},
                timeout=self.timeout
            )
            
            if not pages_response.ok:
                return {
                    'can_read': False,
                    'can_edit': False,
                    'message': f'無法讀取頁面：HTTP {pages_response.status_code}'
                }
            
            pages = pages_response.json()
            if not pages:
                return {
                    'can_read': True,
                    'can_edit': False,
                    'message': '可以讀取但沒有頁面可供測試編輯權限'
                }
            
            # 測試編輯權限（不實際修改，只檢查權限）
            test_page_id = pages[0]['id']
            edit_response = requests.post(
                f"{self.api_base}/pages/{test_page_id}",
                auth=self.auth,
                json={'meta': {'test_permission': 'test'}},
                timeout=self.timeout
            )
            
            can_edit = edit_response.status_code not in [401, 403]
            
            return {
                'can_read': True,
                'can_edit': can_edit,
                'message': '可以讀取頁面' + ('，可以編輯' if can_edit else '，但無法編輯（權限不足）')
            }
            
        except Exception as e:
            return {
                'can_read': False,
                'can_edit': False,
                'message': f'權限測試失敗：{str(e)}'
            }
    
    def find_post_by_url(self, page_url: str) -> Optional[Dict[str, Any]]:
        """
        根據 URL 找到對應的文章或頁面
        
        Args:
            page_url: 頁面 URL
            
        Returns:
            文章/頁面資訊或 None
        """
        try:
            print(f"正在查找頁面: {page_url}")
            
            # 1. 檢查是否為首頁
            if self._is_homepage_url(page_url):
                print("檢測到首頁 URL，查找首頁...")
                return self._find_homepage()
            
            # 2. 提取並清理 slug
            slug = self._extract_slug(page_url)
            print(f"提取的 slug: {slug}")
            
            # 3. 精確匹配
            post = self._find_by_slug(slug)
            if post:
                return post
            
            # 4. 模糊搜尋
            post = self._fuzzy_search(slug)
            if post:
                return post
            
            # 5. 列出所有頁面供用戶選擇
            print("無法找到匹配的頁面，列出所有可用頁面...")
            return self._list_all_pages_for_selection()
        
        except Exception as e:
            print(f"Error finding post by URL: {e}")
            return None
    
    def _is_homepage_url(self, page_url: str) -> bool:
        """檢查是否為首頁 URL"""
        parsed_url = urlparse(page_url)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        # 如果路徑為空或只有根目錄，視為首頁
        if not path_parts or (len(path_parts) == 1 and path_parts[0] == ''):
            return True
        
        # 檢查是否為網站根目錄
        site_domain = urlparse(self.site_url).netloc
        url_domain = parsed_url.netloc
        
        if site_domain == url_domain and not path_parts:
            return True
        
        return False
    
    def _extract_slug(self, page_url: str) -> str:
        """提取並清理 slug"""
        parsed_url = urlparse(page_url)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        if not path_parts:
            return ""
        
        # 取最後一個路徑部分作為 slug
        slug = path_parts[-1]
        
        # 移除可能的檔案擴展名
        if '.' in slug:
            slug = slug.split('.')[0]
        
        print(f"清理後的 slug: {slug}")
        return slug
    
    def _find_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """根據 slug 精確查找文章或頁面"""
        if not slug:
            return None
        
        # 先嘗試搜尋文章
        print("正在搜尋文章...")
        response = requests.get(
            f"{self.api_base}/posts",
            auth=self.auth,
            params={'slug': slug, 'per_page': 1, 'status': 'publish'},
            timeout=self.timeout
        )
        
        print(f"文章搜尋回應狀態: {response.status_code}")
        if response.ok:
            posts = response.json()
            print(f"找到 {len(posts)} 篇文章")
            if posts:
                post = posts[0]
                print(f"找到文章: {post.get('title', {}).get('rendered', '無標題')} (ID: {post.get('id')})")
                return post
        
        # 如果沒找到，嘗試搜尋頁面
        print("正在搜尋頁面...")
        response = requests.get(
            f"{self.api_base}/pages",
            auth=self.auth,
            params={'slug': slug, 'per_page': 1, 'status': 'publish'},
            timeout=self.timeout
        )
        
        print(f"頁面搜尋回應狀態: {response.status_code}")
        if response.ok:
            pages = response.json()
            print(f"找到 {len(pages)} 個頁面")
            if pages:
                page = pages[0]
                print(f"找到頁面: {page.get('title', {}).get('rendered', '無標題')} (ID: {page.get('id')})")
                return page
        
        return None
    
    def _find_homepage(self) -> Optional[Dict[str, Any]]:
        """查找首頁"""
        try:
            print("嘗試查找首頁...")
            
            # 方法1: 嘗試查找首頁設定
            response = requests.get(
                f"{self.api_base}/",
                auth=self.auth,
                timeout=self.timeout
            )
            if response.ok:
                data = response.json()
                print(f"WordPress API 回應: {list(data.keys())}")
                
                # 檢查是否有首頁設定
                if 'home' in data:
                    home_id = data['home']
                    print(f"找到首頁 ID: {home_id}")
                    if home_id:
                        # 根據 ID 查找頁面
                        page_response = requests.get(
                            f"{self.api_base}/pages/{home_id}",
                            auth=self.auth,
                            timeout=self.timeout
                        )
                        if page_response.ok:
                            homepage = page_response.json()
                            print(f"找到首頁: {homepage.get('title', {}).get('rendered', '無標題')}")
                            return homepage
            
            # 方法2: 查找所有頁面，尋找首頁
            print("嘗試從頁面列表中查找首頁...")
            pages_response = requests.get(
                f"{self.api_base}/pages",
                auth=self.auth,
                params={'per_page': 100, 'status': 'publish'},
                timeout=self.timeout
            )
            
            if pages_response.ok:
                pages = pages_response.json()
                print(f"找到 {len(pages)} 個頁面")
                
                # 尋找首頁（通常 slug 為空或 'home'）
                for page in pages:
                    slug = page.get('slug', '')
                    if slug in ['', 'home', 'index']:
                        print(f"找到首頁候選: {page.get('title', {}).get('rendered', '無標題')} (slug: {slug})")
                        return page
                
                # 如果沒找到明確的首頁，返回第一個頁面
                if pages:
                    first_page = pages[0]
                    print(f"使用第一個頁面作為首頁: {first_page.get('title', {}).get('rendered', '無標題')}")
                    return first_page
            
            print("無法找到首頁")
            return None
            
        except Exception as e:
            print(f"Error finding homepage: {e}")
            return None
    
    def _fuzzy_search(self, search_term: str) -> Optional[Dict[str, Any]]:
        """模糊搜尋文章和頁面"""
        try:
            # 搜尋文章
            response = requests.get(
                f"{self.api_base}/posts",
                auth=self.auth,
                params={'search': search_term, 'per_page': 5, 'status': 'publish'},
                timeout=self.timeout
            )
            
            if response.ok:
                posts = response.json()
                if posts:
                    print(f"模糊搜尋找到 {len(posts)} 篇文章")
                    return posts[0]
            
            # 搜尋頁面
            response = requests.get(
                f"{self.api_base}/pages",
                auth=self.auth,
                params={'search': search_term, 'per_page': 5, 'status': 'publish'},
                timeout=self.timeout
            )
            
            if response.ok:
                pages = response.json()
                if pages:
                    print(f"模糊搜尋找到 {len(pages)} 個頁面")
                    return pages[0]
        
        except Exception as e:
            print(f"Error in fuzzy search: {e}")
        
        return None
    
    def _list_all_pages_for_selection(self) -> Optional[Dict[str, Any]]:
        """列出所有頁面供用戶選擇"""
        try:
            print("列出所有可用頁面...")
            
            all_pages = []
            
            # 獲取所有頁面
            pages_response = requests.get(
                f"{self.api_base}/pages",
                auth=self.auth,
                params={'per_page': 100, 'status': 'publish'},
                timeout=self.timeout
            )
            
            if pages_response.ok:
                pages = pages_response.json()
                print(f"找到 {len(pages)} 個頁面")
                for page in pages:
                    all_pages.append({
                        'id': page.get('id'),
                        'title': page.get('title', {}).get('rendered', '無標題'),
                        'slug': page.get('slug'),
                        'link': page.get('link'),
                        'type': 'page'
                    })
            
            # 獲取所有文章
            posts_response = requests.get(
                f"{self.api_base}/posts",
                auth=self.auth,
                params={'per_page': 100, 'status': 'publish'},
                timeout=self.timeout
            )
            
            if posts_response.ok:
                posts = posts_response.json()
                print(f"找到 {len(posts)} 篇文章")
                for post in posts:
                    all_pages.append({
                        'id': post.get('id'),
                        'title': post.get('title', {}).get('rendered', '無標題'),
                        'slug': post.get('slug'),
                        'link': post.get('link'),
                        'type': 'post'
                    })
            
            if all_pages:
                print("所有可用頁面:")
                for i, page in enumerate(all_pages[:10]):  # 只顯示前10個
                    print(f"  {i+1}. {page['title']} ({page['type']}) - {page['link']}")
                
                # 返回第一個頁面作為預設選擇
                return {
                    'id': all_pages[0]['id'],
                    'title': all_pages[0]['title'],
                    'slug': all_pages[0]['slug'],
                    'link': all_pages[0]['link'],
                    'type': all_pages[0]['type'],
                    'all_pages': all_pages  # 包含所有頁面供前端顯示
                }
            
            return None
            
        except Exception as e:
            print(f"Error listing pages: {e}")
            return None
    
    def update_custom_seo_fields(
        self, 
        post_id: int, 
        post_type: str, 
        seo_title: str = None, 
        seo_description: str = None
    ) -> Dict[str, Any]:
        """
        更新自訂 SEO 欄位（無外掛模式）
        
        Args:
            post_id: 文章/頁面 ID
            post_type: 'page' 或 'post'
            seo_title: SEO 標題
            seo_description: Meta description
            
        Returns:
            更新結果
        """
        try:
            meta_data = {}
            if seo_title:
                meta_data['seo_title'] = seo_title
            if seo_description:
                meta_data['seo_meta_description'] = seo_description
            
            if not meta_data:
                return {
                    'success': False,
                    'message': '沒有提供要更新的 SEO 資料'
                }
            
            endpoint = f"{self.api_base}/pages/{post_id}" if post_type == 'page' else f"{self.api_base}/posts/{post_id}"
            
            print(f"更新自訂 SEO 欄位: {meta_data}")
            response = requests.post(
                endpoint,
                auth=self.auth,
                json={'meta': meta_data},
                timeout=self.timeout
            )
            
            if response.ok:
                return {
                    'success': True,
                    'message': '自訂 SEO 欄位更新成功',
                    'data': response.json(),
                    'warning': '⚠️ 注意：這些 SEO 設定已儲存到自訂欄位，但需要在主題中添加程式碼才能生效。'
                }
            else:
                error_message = self._parse_error_message(response)
                return {
                    'success': False,
                    'message': f'更新失敗：{error_message}',
                    'status_code': response.status_code,
                    'raw_response': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'更新自訂 SEO 欄位失敗：{str(e)}'
            }
    
    def _parse_error_message(self, response) -> str:
        """解析 WordPress REST API 錯誤訊息"""
        try:
            error_data = response.json()
            message = error_data.get('message', '未知錯誤')
            
            # 處理常見的權限錯誤
            if response.status_code == 401:
                if 'rest_cannot_edit' in error_data.get('code', ''):
                    return '權限不足：目前的登入身份沒有編輯權限。請確認：\n1. Application Password 是否正確\n2. 使用者是否有編輯者(Editor)或管理員(Administrator)權限\n3. 是否為該文章/頁面的作者'
                elif 'rest_cannot_access' in error_data.get('code', ''):
                    return '無法存取：請確認使用者權限是否足夠'
                else:
                    return f'認證失敗：{message}'
            elif response.status_code == 403:
                return f'權限被拒絕：{message}'
            elif response.status_code == 404:
                return f'找不到資源：{message}'
            else:
                return f'HTTP {response.status_code}：{message}'
        except:
            return f'HTTP {response.status_code}：{response.text}'
    
    def detect_seo_plugin(self) -> Dict[str, Any]:
        """
        檢測使用的 SEO 外掛
        
        Returns:
            檢測結果 {'plugin': 'yoast'|'rank_math'|'none', 'version': str}
        """
        try:
            print("檢測 SEO 外掛...")
            
            # 嘗試獲取一個頁面的 meta 資料
            pages = self.get_pages(per_page=1)
            if not pages:
                print("沒有找到頁面，無法檢測 SEO 外掛")
                return {'plugin': 'none', 'reason': 'no_pages'}
            
            page_id = pages[0]['id']
            response = requests.get(
                f"{self.api_base}/pages/{page_id}",
                auth=self.auth,
                timeout=self.timeout
            )
            
            if response.ok:
                page_data = response.json()
                meta = page_data.get('meta', {})
                print(f"頁面 meta 欄位: {list(meta.keys())}")
                
                # 檢測 Yoast SEO
                yoast_fields = ['_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw']
                if any(field in meta for field in yoast_fields):
                    version = meta.get('_yoast_wpseo_version', 'unknown')
                    print(f"檢測到 Yoast SEO (版本: {version})")
                    return {'plugin': 'yoast', 'version': version}
                
                # 檢測 Rank Math
                rankmath_fields = ['rank_math_title', 'rank_math_description', 'rank_math_focus_keyword']
                if any(field in meta for field in rankmath_fields):
                    print("檢測到 Rank Math")
                    return {'plugin': 'rank_math', 'version': 'unknown'}
                
                # 檢測 All in One SEO
                aioseo_fields = ['_aioseo_title', '_aioseo_description']
                if any(field in meta for field in aioseo_fields):
                    print("檢測到 All in One SEO")
                    return {'plugin': 'aioseo', 'version': 'unknown'}
                
                print("未檢測到 SEO 外掛")
                return {'plugin': 'none', 'reason': 'no_seo_plugin'}
            
            else:
                print(f"無法獲取頁面資料: {response.status_code}")
                return {'plugin': 'unknown', 'reason': 'api_error'}
        
        except Exception as e:
            print(f"檢測 SEO 外掛時發生錯誤: {e}")
            return {'plugin': 'unknown', 'reason': 'error', 'error': str(e)}
    
    def get_posts(self, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        取得文章列表
        
        Args:
            per_page: 每頁數量
            
        Returns:
            文章列表
        """
        try:
            response = requests.get(
                f"{self.api_base}/posts",
                auth=self.auth,
                params={'per_page': per_page},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Get posts error: {e}")
            return []
    
    def get_pages(self, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        取得頁面列表
        
        Args:
            per_page: 每頁數量
            
        Returns:
            頁面列表
        """
        try:
            response = requests.get(
                f"{self.api_base}/pages",
                auth=self.auth,
                params={'per_page': per_page},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Get pages error: {e}")
            return []
    
    def update_post_meta(
        self,
        post_id: int,
        meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        更新文章 meta 資料（支援 Yoast SEO）
        
        Args:
            post_id: 文章 ID
            meta_data: Meta 資料字典 (例如：{'_yoast_wpseo_metadesc': 'new description'})
            
        Returns:
            更新結果
        """
        try:
            response = requests.post(
                f"{self.api_base}/posts/{post_id}",
                auth=self.auth,
                json={'meta': meta_data},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return {
                'success': True,
                'message': '更新成功',
                'data': response.json()
            }
        
        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'message': f'更新失敗：HTTP {e.response.status_code}'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'更新失敗：{str(e)}'
            }
    
    def update_page_meta(
        self,
        page_id: int,
        meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        更新頁面 meta 資料
        
        Args:
            page_id: 頁面 ID
            meta_data: Meta 資料字典
            
        Returns:
            更新結果
        """
        try:
            response = requests.post(
                f"{self.api_base}/pages/{page_id}",
                auth=self.auth,
                json={'meta': meta_data},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return {
                'success': True,
                'message': '更新成功',
                'data': response.json()
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'更新失敗：{str(e)}'
            }
    
    def update_media_alt(
        self,
        media_id: int,
        alt_text: str
    ) -> Dict[str, Any]:
        """
        更新圖片 alt 屬性
        
        Args:
            media_id: 媒體庫 ID
            alt_text: 新的 alt 文字
            
        Returns:
            更新結果
        """
        try:
            response = requests.post(
                f"{self.api_base}/media/{media_id}",
                auth=self.auth,
                json={'alt_text': alt_text},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return {
                'success': True,
                'message': '更新成功',
                'data': response.json()
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'更新失敗：{str(e)}'
            }
    
    def find_media_by_url(self, image_url: str) -> Optional[int]:
        """
        根據 URL 找到媒體庫 ID
        
        Args:
            image_url: 圖片 URL
            
        Returns:
            媒體 ID 或 None
        """
        try:
            # 從 URL 取得檔名
            filename = image_url.split('/')[-1].split('?')[0]
            
            response = requests.get(
                f"{self.api_base}/media",
                auth=self.auth,
                params={'search': filename, 'per_page': 5},
                timeout=self.timeout
            )
            
            if response.ok and response.json():
                # 找到第一個符合的媒體
                for media in response.json():
                    if filename in media.get('source_url', ''):
                        return media.get('id')
            
            return None
        
        except Exception as e:
            print(f"Error finding media by URL: {e}")
            return None
    
    def update_post_content(
        self,
        post_id: int,
        content: str
    ) -> Dict[str, Any]:
        """
        更新文章內容（進階功能 - 用於 H1、段落等內容更新）
        
        Args:
            post_id: 文章 ID
            content: 新的 HTML 內容
            
        Returns:
            更新結果
        """
        try:
            response = requests.post(
                f"{self.api_base}/posts/{post_id}",
                auth=self.auth,
                json={'content': content},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return {
                'success': True,
                'message': '內容更新成功',
                'data': response.json()
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'內容更新失敗：{str(e)}'
            }
    
    def get_post_content(self, post_id: int) -> Optional[str]:
        """
        取得文章內容（用於備份）
        
        Args:
            post_id: 文章 ID
            
        Returns:
            文章 HTML 內容或 None
        """
        try:
            response = requests.get(
                f"{self.api_base}/posts/{post_id}",
                auth=self.auth,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('content', {}).get('rendered', '')
        
        except Exception as e:
            print(f"Error getting post content: {e}")
            return None

