#!/bin/bash

# SEO 分析工具 - Railway 部署腳本

echo "🚀 SEO 分析工具 Railway 部署腳本"
echo "===================================="
echo ""

# 檢查是否在正確的目錄
if [ ! -f "app.py" ]; then
    echo "❌ 錯誤：請在專案根目錄執行此腳本"
    exit 1
fi

echo "✓ 專案目錄確認"

# 檢查 Git
if [ ! -d ".git" ]; then
    echo ""
    echo "📦 初始化 Git repository..."
    git init
    echo "✓ Git 已初始化"
fi

# 添加所有檔案
echo ""
echo "📝 添加檔案到 Git..."
git add .
echo "✓ 檔案已添加"

# 提交
echo ""
echo "💾 提交變更..."
git commit -m "SEO 分析工具 - AI 深度模式 (gpt-4o-mini) - Railway ready" || echo "沒有新的變更需要提交"

# 檢查是否有遠端倉庫
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  尚未設定 GitHub 遠端倉庫"
    echo ""
    echo "請執行以下命令設定："
    echo "  git remote add origin https://github.com/你的帳號/repo名稱.git"
    echo "  git push -u origin main"
    echo ""
    exit 0
fi

# 推送到 GitHub
echo ""
echo "🚀 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ 部署準備完成！"
echo ""
echo "下一步："
echo "1. 前往 https://railway.app"
echo "2. 點擊 'New Project'"
echo "3. 選擇 'Deploy from GitHub repo'"
echo "4. 選擇您的 repository"
echo "5. 等待自動部署完成"
echo ""
echo "🎉 部署完成後，您將獲得一個公開網址！"

