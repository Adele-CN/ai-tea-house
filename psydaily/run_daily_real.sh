#!/bin/bash
# PsyDaily 真实论文每日自动更新脚本
# 每天自动抓取最新真实论文并部署网站

cd /root/.openclaw/workspace/ai-tea-house/psydaily

echo "🚀 PsyDaily 真实论文自动更新 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================="

# 1. 抓取真实论文
echo "📡 抓取真实论文..."
python3 fetch_real_papers.py

# 2. 生成静态网站
echo "🌐 生成网站..."
python3 static_site_generator.py

# 3. 复制到根目录并推送
echo "📤 推送到 GitHub..."
cd /root/.openclaw/workspace/ai-tea-house
cp psydaily/site/index.html index.html
git add index.html
git commit -m "📚 Auto update: $(date '+%Y-%m-%d %H:%M:%S') - Real papers" || echo "无变化"
git push origin main

# 4. Telegram 通知
echo "📱 发送通知..."
curl -s -X POST "https://api.telegram.org/bot8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA/sendMessage" \
  -d "chat_id=8309994838" \
  -d "text=📚 PsyDaily 已更新真实论文！%0A%0A$(date '+%Y-%m-%d')%0A新抓取心理学论文已发布。%0A%0A查看：https://adele-cn.github.io/ai-tea-house/"

echo "✅ 完成！"
