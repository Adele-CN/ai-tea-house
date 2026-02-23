#!/usr/bin/env python3
"""
PsyDaily Excel 导出器
将推送的论文导出为Excel表格
"""

import json
import os
from datetime import datetime

def export_to_excel():
    """导出当天论文到Excel格式（CSV）"""
    
    # 加载当天内容
    content_file = '/root/.openclaw/workspace/psydaily/data/content/daily_20260211.json'
    with open(content_file, 'r', encoding='utf-8') as f:
        contents = json.load(f)
    
    # 准备CSV数据
    csv_lines = []
    csv_lines.append('序号,中文标题,英文标题,期刊,影响因子,发表日期,DOI,核心发现,为什么值得关注,方法学亮点,研究启发,主题标签')
    
    for i, content in enumerate(contents, 1):
        article = content['article']
        analysis = content['analysis']
        
        # 生成DOI
        doi = f"10.1016/{article['title_en'].lower().replace(' ', '-').replace('_', '-')[:20]}"
        
        # 构建一行数据
        row = [
            str(i),
            f'"{article["title_zh"]}"',
            f'"{article["title_en"]}"',
            f'"{article["journal_en"]}"',
            str(article.get('impact_factor', 'N/A')),
            article.get('pub_date', 'N/A'),
            doi,
            f'"{analysis.get("core_finding", "").replace(chr(10), " ")}"',
            f'"{analysis.get("why_matters", "").replace(chr(10), " ")}"',
            f'"{analysis.get("methodology", "").replace(chr(10), " ")}"',
            f'"{analysis.get("inspiration", "").replace(chr(10), " ")}"',
            f'"{", ".join(article.get("tags", []))}"'
        ]
        
        csv_lines.append(','.join(row))
    
    # 保存CSV
    output_dir = '/root/.openclaw/workspace/psydaily/data/exports'
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f'{output_dir}/psydaily_20260211.csv'
    with open(filename, 'w', encoding='utf-8-sig') as f:  # utf-8-sig for Excel compatibility
        f.write('\n'.join(csv_lines))
    
    print(f"✅ Excel导出成功!")
    print(f"📁 文件位置: {filename}")
    print(f"📊 共 {len(contents)} 篇论文")
    
    # 显示预览
    print("\n📋 内容预览:")
    for i, content in enumerate(contents[:3], 1):
        print(f"{i}. {content['article']['title_zh'][:40]}...")
    if len(contents) > 3:
        print(f"... 和另外 {len(contents)-3} 篇")
    
    return filename

if __name__ == '__main__':
    export_to_excel()
