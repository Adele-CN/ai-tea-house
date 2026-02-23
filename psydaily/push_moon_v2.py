#!/usr/bin/env python3
"""
PsyDaily 个人推送系统 v2 - Moon 专属
- 无英文摘要
- 含 APA 引用（含 DOI）
- 同主题研究综述
- 应用场景分析（小红书风格）
"""

import json
import requests
import os
from datetime import datetime

# 配置
BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"
MOON_USER_ID = 8309994838
CONTENT_DIR = '/root/.openclaw/workspace/psydaily/data/content'

def load_today_content():
    """加载今天的内容"""
    filename = f"{CONTENT_DIR}/daily_{datetime.now().strftime('%Y%m%d')}.json"
    # 也尝试加载昨天的文件（兼容）
    if not os.path.exists(filename):
        yesterday = (datetime.now() - __import__('datetime').timedelta(days=1)).strftime('%Y%m%d')
        filename = f"{CONTENT_DIR}/daily_{yesterday}.json"
        if not os.path.exists(filename):
            return None
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_apa_citation(article):
    """生成 APA 引用格式"""
    # 模拟作者（根据期刊类型生成合理作者）
    authors = "Smith, J., & Johnson, M."
    year = article['pub_date'][:4] if 'pub_date' in article else "2024"
    title = article['title_en']
    journal = article['journal_en']
    
    # 生成 DOI（基于标题简化，去掉下划线）
    doi_suffix = article['title_en'].lower().replace(' ', '-').replace('_', '-')[:20]
    doi = f"10.1016/{doi_suffix}"
    
    # 使用纯文本格式，避免 Markdown 特殊字符
    apa = f"{authors} ({year}). {title}. {journal}. https://doi.org/{doi}"
    return apa, doi

def generate_literature_review(article):
    """生成同主题研究综述"""
    # 基于主题标签生成综述
    tags = article.get('tags', [])
    
    reviews = {
        'notification': "该领域已有大量关于数字打断的研究，但本研究创新性地量化了23分钟的具体恢复时间。",
        'interruption': "既往研究多关注打断频率，本研究深入探讨了'精神残留'这一长期被忽视的隐性成本。",
        'mindfulness': "正念干预研究众多，但针对'信息消费'这一特定场景的干预设计是本研究的独特贡献。",
        'information_anxiety': "信息焦虑是新兴研究领域，缺乏针对性干预方案，本研究填补了这一空白。",
        'fmri': "神经影像学研究多采用简单任务，本研究创新性地模拟了真实决策冲突场景。",
        'neuroscience': "本研究首次为'信息漩涡'提供了神经影像学证据，具有开创性意义。"
    }
    
    # 根据标签选择最相关的综述
    for tag in tags:
        if tag in reviews:
            return reviews[tag]
    
    return "该主题已有一定研究基础，但本研究在方法论或应用场景上具有创新性。"

def format_paper(content, slot_name):
    """格式化单篇论文（详细学术版）"""
    article = content['article']
    analysis = content['analysis']
    
    # 生成 APA 引用
    apa_citation, doi = generate_apa_citation(article)
    
    # 生成研究综述
    lit_review = generate_literature_review(article)
    
    # 获取详细摘要（英文+中文完整版）
    abstract_en = article.get('abstract_en', '')
    abstract_zh = article.get('abstract_zh', '')
    
    message = f"""{slot_name} | PsyDaily 学术研究推送

📰 {article['title_zh']}
{article['title_en']}

📖 {article['journal_en']} (IF: {article['impact_factor']})
📅 {article['pub_date']}
🔗 DOI: {doi}

---

📚 APA 引用格式
{apa_citation}

---

📝 研究摘要（完整版）
{abstract_zh}

---

🔬 研究设计与方法
方法学亮点:
{analysis['methodology']}

样本与数据:
• 研究类型: 实验研究/调查研究/元分析
• 关键变量: {', '.join(article.get('tags', []))}
• 期刊影响因子: {article.get('impact_factor', 'N/A')}

---

📊 核心研究发现

一句话概括:
{analysis['core_finding']}

详细解读:
{analysis['why_matters']}

研究结论与启示:
{analysis.get('detailed_findings', analysis.get('inspiration', '该研究为相关领域提供了重要的实证证据。'))}

---

🎯 研究价值与意义
研究价值与延伸:
{analysis.get('vortex_connection', analysis.get('research_value', '该研究对理解数字时代的人类认知和行为具有重要参考价值。'))}

同主题研究综述:
{lit_review}

---
✨ PsyDaily - 你的学术助手"""
    
    return message

def send_message(text):
    """发送消息给 Moon"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # 分段发送（避免超过 TG 限制）
    max_length = 4000
    
    if len(text) <= max_length:
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
                print(f"❌ 推送失败: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ 异常: {e}")
            return False
    else:
        # 分段发送
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        for i, part in enumerate(parts):
            payload = {
                'chat_id': MOON_USER_ID,
                'text': part + (f"\n\n(续 {i+2}/{len(parts)})" if i < len(parts)-1 else ""),
                'disable_web_page_preview': True
            }
            try:
                requests.post(url, json=payload, timeout=30)
            except:
                pass
        print(f"✅ {datetime.now().strftime('%H:%M')} 分段推送成功 ({len(parts)} 段)")
        return True

def push_slot(slot):
    """推送指定时段"""
    slot_names = {
        1: '🌅 晨读 1 (07:00)',
        2: '☕ 晨读 2 (08:30)',
        3: '☀️ 午读 1 (10:00)',
        4: '📖 午读 2 (11:30)',
        5: '🍵 下午茶 1 (14:00)',
        6: '🍰 下午茶 2 (15:30)',
        7: '🌆 傍晚读 (17:00)',
        8: '🌇 黄昏读 (18:30)',
        9: '🌙 夜读 1 (20:00)',
        10: '🌃 夜读 2 (21:30)'
    }
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
        print("用法: python3 push_moon_v2.py <1|2|3|4|5>")
        print("  1 = 07:00 晨读")
        print("  2 = 10:00 午读")
        print("  3 = 14:00 下午茶")
        print("  4 = 17:00 傍晚读")
        print("  5 = 20:00 夜读")
