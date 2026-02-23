#!/usr/bin/env python3
"""
PsyDaily 个人推送系统 - 仅给 Moon 推送
每日 07:00 / 12:00 / 18:00 推送 3 篇论文
"""

import json
import requests
import os
from datetime import datetime

# 配置
BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"
MOON_USER_ID = 8309994838  # 你的 TG ID
CONTENT_DIR = '/root/.openclaw/workspace/psydaily/data/content'

def load_today_content():
    """加载今天的内容"""
    filename = f"{CONTENT_DIR}/daily_{datetime.now().strftime('%Y%m%d')}.json"
    if not os.path.exists(filename):
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_paper(content, slot_name):
    """格式化单篇论文"""
    article = content['article']
    analysis = content['analysis']
    
    return f"""{slot_name} | PsyDaily 信息漩涡研究

📰 {article['title_en']}
🇨🇳 {article['title_zh']}

📖 {article['journal_en']} (IF: {article['impact_factor']})
📅 {article['pub_date']}
🔗 {article.get('url', 'N/A')}

📝 摘要
{article['abstract_en'][:250]}...

🇨🇳 {article['abstract_zh'][:200]}...

💡 AI分析
• 核心发现：{analysis['core_finding']}
• 为什么值得关注：{analysis['why_matters']}
• 方法学亮点：{analysis['methodology']}
• 与信息漩涡关联：{analysis.get('vortex_connection', 'N/A')}

---
PsyDaily - 你的信息漩涡研究助手"""

def send_message(text):
    """发送消息给 Moon"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': MOON_USER_ID,
        'text': text,
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print(f"✅ {datetime.now().strftime('%H:%M')} 推送成功")
            return True
        else:
            print(f"❌ 推送失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def push_slot(slot):
    """推送指定时段"""
    slot_names = {1: '🌅 晨读', 2: '☀️ 午读', 3: '🌙 夜读'}
    slot_name = slot_names.get(slot, '📚 阅读')
    
    print(f"\n{'='*50}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {slot_name}")
    print('='*50)
    
    # 加载内容
    contents = load_today_content()
    if not contents:
        print("❌ 今天的内容未生成")
        return
    
    # 获取对应时段的论文
    if slot <= len(contents):
        content = contents[slot - 1]
    else:
        content = contents[0]
    
    # 格式化并发送
    message = format_paper(content, slot_name)
    send_message(message)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        slot = int(sys.argv[1])
        push_slot(slot)
    else:
        print("用法: python3 push_moon.py <1|2|3>")
        print("  1 = 07:00 晨读")
        print("  2 = 12:00 午读")
        print("  3 = 18:00 夜读")
