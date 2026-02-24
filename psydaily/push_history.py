#!/usr/bin/env python3
"""
PsyDaily 推送历史记录器
防止重复推送同一篇文章
"""

import json
import os
from datetime import datetime

HISTORY_FILE = '/root/.openclaw/workspace/psydaily/data/push_history.json'

def load_history():
    """加载推送历史"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'pushed_articles': [], 'last_push_date': None}

def save_history(history):
    """保存推送历史"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def mark_as_pushed(article_ids):
    """标记文章为已推送"""
    history = load_history()
    for article_id in article_ids:
        if article_id not in history['pushed_articles']:
            history['pushed_articles'].append(article_id)
    history['last_push_date'] = datetime.now().strftime('%Y-%m-%d')
    save_history(history)
    print(f"✅ 已记录 {len(article_ids)} 篇论文到推送历史")

def get_pushed_articles():
    """获取已推送的文章ID列表"""
    history = load_history()
    return history['pushed_articles']

def is_pushed(article_id):
    """检查文章是否已推送"""
    return article_id in get_pushed_articles()

def reset_history():
    """重置历史（谨慎使用）"""
    history = {'pushed_articles': [], 'last_push_date': None}
    save_history(history)
    print("⚠️ 推送历史已重置")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_history()
    else:
        history = load_history()
        print(f"📊 推送历史：共 {len(history['pushed_articles'])} 篇")
        print(f"📅 最后推送：{history['last_push_date']}")
        if history['pushed_articles']:
            print(f"\n已推送文章ID：")
            for aid in history['pushed_articles'][-10:]:  # 只显示最近10篇
                print(f"  - {aid}")
