#!/bin/bash
# PsyDaily 每日自动更新脚本 v3
# 每日抓取：10篇英文论文 + 10篇中文论文

cd /root/.openclaw/workspace/ai-tea-house/psydaily

echo "🚀 PsyDaily 每日自动更新 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================="

# 1. 抓取英文论文（10篇）
echo "📡 抓取英文论文..."
python3 fetch_real_papers.py

# 2. 抓取中文论文（10篇）
echo "📡 抓取中文论文..."
python3 fetch_chinese_papers.py

# 3. 合并中英文论文
echo "🔄 合并中英文论文..."
python3 << 'EOF'
import json
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data', 'content')

# 加载英文论文
english_papers = []
eng_file = os.path.join(data_dir, 'real_papers_20260224.json')
if os.path.exists(eng_file):
    with open(eng_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        english_papers = [item['article'] for item in data[:10]]  # 取前10篇

# 加载中文论文
chinese_papers = []
cn_file = os.path.join(data_dir, 'chinese_papers_20260224.json')
if os.path.exists(cn_file):
    with open(cn_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        chinese_papers = [item['article'] for item in data[:10]]  # 取前10篇

# 合并
all_papers = english_papers + chinese_papers

# 保存为最新数据
output_file = os.path.join(data_dir, 'daily_latest_complete.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump([{'article': p} for p in all_papers], f, ensure_ascii=False, indent=2)

print(f"✅ 合并完成: {len(english_papers)} 篇英文 + {len(chinese_papers)} 篇中文 = {len(all_papers)} 篇")
EOF

# 4. 生成静态网站
echo "🌐 生成网站..."
python3 static_site_generator.py

# 5. 复制到根目录并推送
echo "📤 推送到 GitHub..."
cd /root/.openclaw/workspace/ai-tea-house
cp psydaily/site/index.html v2/index.html
git add v2/index.html
git commit -m "📚 Daily update: $(date '+%Y-%m-%d') - $(date '+%H:%M')" || echo "无变化"
git push origin main

# 6. Telegram 通知
echo "📱 发送通知..."
PAPER_COUNT=$(python3 -c "import json; data=json.load(open('psydaily/data/content/daily_latest_complete.json')); print(len(data))")
curl -s -X POST "https://api.telegram.org/bot8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA/sendMessage" \
  -d "chat_id=8309994838" \
  -d "text=📚 PsyDaily 已更新！%0A%0A$(date '+%Y-%m-%d %H:%M')%0A今日更新 ${PAPER_COUNT} 篇论文%0A（中英文各10篇）%0A%0A查看：https://adele-cn.github.io/ai-tea-house/v2/"

echo "✅ 完成！"
