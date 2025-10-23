# 團隊篩選功能 - 設計文件

## 背景說明

這是一個個人使用的工具，只有單一使用者（您自己），不需要考慮多人協作或複雜的權限管理。主要目的是快速找到特定團隊的資料。

## 目標 / 非目標

### 目標
- 提供簡單的團隊篩選功能
- 單選下拉選單（一次只選一個團隊）
- 記住上次選擇的團隊
- 即時更新篩選結果
- 簡單易用的介面

### 非目標
- 多選功能（不需要）
- 角色篩選（只有您一個使用者，不需要）
- 複雜的篩選組合（保持簡單）
- 多使用者功能（個人工具）
- 後端 API（如果是前端篩選的話）

## 設計決策

### 1. 篩選器類型：單選下拉選單

**決定**：使用簡單的 `<select>` 下拉選單

**理由**：
- 一次只需要看一個團隊的資料
- 介面最簡單直觀
- 不需要額外的 UI 套件
- 原生 HTML 元素效能最好

**替代方案**：
- 多選下拉：不需要，過於複雜
- 按鈕群組：團隊數量可能較多時不適合
- 搜尋框：對個人使用來說太複雜

### 2. 狀態儲存：localStorage

**決定**：使用 localStorage 記住選擇

```javascript
// 儲存
localStorage.setItem('selectedTeam', team);

// 讀取
const savedTeam = localStorage.getItem('selectedTeam');
```

**理由**：
- 重新整理頁面後保持選擇
- 不需要後端支援
- 簡單可靠

### 3. 資料篩選：前端篩選

**決定**：在前端直接篩選資料陣列

```javascript
const filteredData = data.filter(item => 
  !selectedTeam || selectedTeam === 'all' || item.team === selectedTeam
);
```

**假設**：資料量不大（< 1000 筆）

**如果資料量大**：可以改用後端篩選，但先從前端開始

### 4. UI 元件結構

```html
<div class="team-filter">
  <label>選擇團隊：</label>
  <select value={selectedTeam} onChange={handleTeamChange}>
    <option value="all">全部團隊</option>
    <option value="engineering">工程部</option>
    <option value="sales">業務部</option>
    <option value="marketing">行銷部</option>
    <!-- 其他團隊 -->
  </select>
  <button onClick={clearFilter}>清除篩選</button>
</div>

<div class="filter-status">
  {selectedTeam && selectedTeam !== 'all' && (
    <p>目前顯示：{teamName} ({resultCount} 筆資料)</p>
  )}
</div>

<div class="results">
  {/* 篩選後的結果 */}
</div>
```

### 5. 團隊選項來源

**選項一**：寫死在程式碼中（簡單）
```javascript
const teams = [
  { value: 'all', label: '全部團隊' },
  { value: 'engineering', label: '工程部' },
  { value: 'sales', label: '業務部' },
  // ...
];
```

**選項二**：從資料中動態提取（彈性）
```javascript
const teams = ['all', ...new Set(data.map(item => item.team))];
```

**建議**：如果團隊固定，用選項一；如果會變動，用選項二

## 風險與取捨

### 風險 1：資料量增加
- **風險**：如果資料超過數千筆，前端篩選可能變慢
- **緩解**：先從前端開始，如有需要再改後端篩選

### 風險 2：團隊名稱不一致
- **風險**：資料中團隊名稱可能有拼寫差異
- **緩解**：在輸入資料時統一格式，或加入資料清理邏輯

### 取捨

1. **簡單 vs 功能完整**：
   - 選擇簡單，只做單選
   - 如需要更多功能，未來再擴充

2. **前端篩選 vs 後端篩選**：
   - 選擇前端篩選（假設資料量不大）
   - 實作簡單，不需要後端改動

3. **記憶功能 vs 每次重設**：
   - 選擇記憶上次選擇
   - 符合個人使用習慣

## 實作範例

### React 範例

```jsx
function ProfileFilter({ data }) {
  const [selectedTeam, setSelectedTeam] = useState(() => {
    return localStorage.getItem('selectedTeam') || 'all';
  });

  const handleTeamChange = (e) => {
    const team = e.target.value;
    setSelectedTeam(team);
    localStorage.setItem('selectedTeam', team);
  };

  const clearFilter = () => {
    setSelectedTeam('all');
    localStorage.setItem('selectedTeam', 'all');
  };

  const filteredData = data.filter(item => 
    selectedTeam === 'all' || item.team === selectedTeam
  );

  return (
    <div>
      <div className="filter-bar">
        <select value={selectedTeam} onChange={handleTeamChange}>
          <option value="all">全部團隊</option>
          <option value="engineering">工程部</option>
          <option value="sales">業務部</option>
          <option value="marketing">行銷部</option>
        </select>
        {selectedTeam !== 'all' && (
          <button onClick={clearFilter}>清除</button>
        )}
      </div>
      
      {selectedTeam !== 'all' && (
        <p>顯示 {filteredData.length} 筆 {selectedTeam} 的資料</p>
      )}
      
      <ResultList data={filteredData} />
    </div>
  );
}
```

### Vanilla JavaScript 範例

```javascript
// 初始化
const selectTeam = document.getElementById('team-select');
const clearBtn = document.getElementById('clear-filter');
const resultsDiv = document.getElementById('results');

// 讀取儲存的選擇
const savedTeam = localStorage.getItem('selectedTeam') || 'all';
selectTeam.value = savedTeam;

// 監聽變更
selectTeam.addEventListener('change', (e) => {
  const team = e.target.value;
  localStorage.setItem('selectedTeam', team);
  updateResults(team);
});

// 清除篩選
clearBtn.addEventListener('click', () => {
  selectTeam.value = 'all';
  localStorage.setItem('selectedTeam', 'all');
  updateResults('all');
});

// 更新結果
function updateResults(team) {
  const filtered = team === 'all' 
    ? allData 
    : allData.filter(item => item.team === team);
  
  renderResults(filtered);
}

// 初始顯示
updateResults(savedTeam);
```

## 實施計畫

### 階段 1：基本功能（MVP）
1. 建立下拉選單
2. 實作前端篩選邏輯
3. 顯示篩選結果

### 階段 2：改善體驗
1. 加入 localStorage 記憶
2. 顯示結果計數
3. 加入清除按鈕

### 階段 3：優化（可選）
1. 加入過渡動畫
2. 鍵盤快捷鍵
3. 效能優化

## 未來可能擴充

- 如果需要看多個團隊：改為多選
- 如果資料量很大：改為後端篩選
- 如果需要儲存多組篩選條件：加入「我的最愛篩選」
- 如果需要更複雜的篩選：加入搜尋框或多條件篩選

## 總結

這是一個簡單實用的個人工具篩選功能：
- ✅ 單選下拉選單（夠用）
- ✅ 記住上次選擇（方便）
- ✅ 前端篩選（簡單）
- ✅ 不需要複雜的後端或多選功能

保持簡單，先做能用的版本，有需要再擴充！
