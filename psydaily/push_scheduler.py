#!/usr/bin/env python3
"""
PsyDaily 定时推送脚本
每天7点、12点、18点自动推送
"""

import json
import os
import sys
sys.path.insert(0, '/root/.openclaw/workspace/psydaily')

from datetime import datetime
import requests

BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"
CONTENT_DIR = '/root/.openclaw/workspace/psydaily/data/content'

# 用户列表（需要订阅推送的用户ID）
# 后续可以从数据库读取
SUBSCRIBED_USERS = []  # 暂时为空，用户用 /subscribe 命令订阅


def load_subscribers():
    """加载订阅用户列表"""
    subscribers_file = f'{CONTENT_DIR}/subscribers.json'
    if os.path.exists(subscribers_file):
        with open(subscribers_file, 'r') as f:
            return json.load(f)
    return []


def save_subscribers(users):
    """保存订阅用户列表"""
    subscribers_file = f'{CONTENT_DIR}/subscribers.json'
    with open(subscribers_file, 'w') as f:
        json.dump(users, f)


def get_today_article(slot):
    """获取今天的指定时段论文"""
    filename = f"{CONTENT_DIR}/daily_{datetime.now().strftime('%Y%m%d')}.json"
    
    if not os.path.exists(filename):
        print(f"❌ 今天的内容文件不存在: {filename}")
        return None
    
    with open(filename, 'r', encoding='utf-8') as f:
        contents = json.load(f)
    
    for content in contents:
        if content.get('slot') == slot:
            return content
    
    return contents[slot-1] if len(contents) >= slot else None


def format_message(content, slot):
    """格式化推送消息"""
    article = content['article']
    analysis = content['analysis']
    
    slot_names = {1: '🌅 晨读', 2: '☀️ 午读', 3: '🌙 夜读'}
    slot_name = slot_names.get(slot, '📚 今日推荐')
    
    message = f"""{slot_name} | PsyDaily 信息漩涡研究日报

📰 **{article['title_en']}**
🇨🇳 {article['title_zh']}

📖 **{article['journal_en']}**
⭐ 影响因子：{article['impact_factor']}
📅 发表时间：{article['pub_date']}

🏷️ 主题：{', '.join(article['tags'])}
🎯 相关度：{article['relevance_score']*100:.0f}%

---

📝 **摘要**

{article['abstract_en'][:200]}...

🇨🇳 {article['abstract_zh'][:180]}...

---

💡 **AI分析**

**1. 核心发现**
{analysis['core_finding']}

**2. 为什么值得关注**
{analysis['why_matters']}

---

🔒 **Pro版解锁完整分析：**
• 核心发现详解
• 方法学亮点
• 研究启发
• 与信息漩涡的深入关联

💎 回复 /upgrade 了解Pro权益"""
    
    return message


def send_push(user_id, message):
    """发送推送消息"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # 尝试 Markdown 格式，失败则转为纯文本
    payload = {
        'chat_id': user_id,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print(f"✅ 已推送给用户 {user_id}")
            return True
        else:
            error_msg = response.json().get('description', '')
            if "Can't parse entities" in error_msg:
                # Markdown 解析失败，用纯文本重试
                print(f"⚠️ Markdown 解析失败，改用纯文本发送...")
                payload['parse_mode'] = None
                response = requests.post(url, json=payload, timeout=30)
                if response.status_code == 200:
                    print(f"✅ 纯文本推送成功 {user_id}")
                    return True
            print(f"❌ 推送给 {user_id} 失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 推送给 {user_id} 异常: {e}")
        return False


def push_to_slot(slot):
    """推送指定时段的论文"""
    print(f"\n{'='*60}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 推送时段 {slot}")
    print('='*60)
    
    # 获取内容
    content = get_today_article(slot)
    if not content:
        print("❌ 未找到今天的内容")
        return
    
    # 格式化消息
    message = format_message(content, slot)
    
    # 获取订阅用户
    subscribers = load_subscribers()
    
    if not subscribers:
        print("⚠️ 暂无订阅用户")
        print(f"📄 内容预览（前200字）：\n{message[:200]}...")
        return
    
    # 推送给所有订阅用户
    success_count = 0
    for user_id in subscribers:
        if send_push(user_id, message):
            success_count += 1
    
    print(f"\n✅ 推送完成：{success_count}/{len(subscribers)} 成功")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='PsyDaily 定时推送')
    parser.add_argument('--slot', type=int, choices=[1, 2, 3], 
                       help='推送时段：1=7点, 2=12点, 3=18点')
    
    args = parser.parse_args()
    
    if args.slot:
        push_to_slot(args.slot)
    else:
        print("请指定推送时段：--slot 1/2/3")
        print("  1 = 07:00 晨读")
        print("  2 = 12:00 午读")
        print("  3 = 18:00 夜读")
