#!/usr/bin/env python3
"""
合并所有论文数据为最新完整库
"""

import json
import os
from datetime import datetime

def merge_all_papers():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data', 'content')
    all_papers = []
    
    # 获取所有 daily_*.json 文件
    files = sorted([f for f in os.listdir(data_dir) if f.startswith('daily_') and f.endswith('.json')])
    
    seen_titles = set()
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and 'article' in item:
                        article = item['article']
                    else:
                        article = item
                    
                    title = article.get('title_en', article.get('title_zh', ''))
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        all_papers.append(article)
                        
        except Exception as e:
            print(f"⚠️ 跳过 {filename}: {e}")
    
    # 保存合并后的文件
    output_file = os.path.join(data_dir, 'daily_latest_complete.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([{'article': p} for p in all_papers], f, ensure_ascii=False, indent=2)
    
    print(f"✅ 合并完成: {len(all_papers)} 篇唯一论文")
    print(f"📁 保存到: {output_file}")
    return all_papers

if __name__ == '__main__':
    merge_all_papers()
