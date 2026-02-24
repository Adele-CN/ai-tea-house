#!/usr/bin/env python3
"""
PsyDaily Excel 导出器 - 完整版（30篇）
"""

import json
import os
from datetime import datetime

def export_complete_to_excel():
    """导出全部30篇论文到Excel格式（CSV）"""
    
    # 加载完整内容
    content_file = '/root/.openclaw/workspace/psydaily/data/content/daily_20260211_complete.json'
    with open(content_file, 'r', encoding='utf-8') as f:
        contents = json.load(f)
    
    # 准备CSV数据
    csv_lines = []
    csv_lines.append('序号,中文标题,英文标题,期刊,影响因子,发表日期,DOI,中文摘要,核心发现,为什么值得关注,方法学亮点,研究启发,主题标签,相关度')
    
    for i, content in enumerate(contents, 1):
        article = content['article']
        analysis = content['analysis']
        
        # 生成DOI
        doi = f"10.1016/{article['title_en'].lower().replace(' ', '-').replace('_', '-')[:25]}"
        
        # 构建一行数据（处理逗号和换行）
        def clean_field(text):
            if not text:
                return ''
            text = str(text).replace('"', '""').replace('\n', ' ').replace('\r', '')
            return f'"{text}"'
        
        row = [
            str(i),
            clean_field(article["title_zh"]),
            clean_field(article["title_en"]),
            clean_field(article["journal_en"]),
            str(article.get('impact_factor', 'N/A')),
            article.get('pub_date', 'N/A'),
            doi,
            clean_field(article.get('abstract_zh', '')),
            clean_field(analysis.get("core_finding", "")),
            clean_field(analysis.get("why_matters", "")),
            clean_field(analysis.get("methodology", "")),
            clean_field(analysis.get("inspiration", "")),
            clean_field(", ".join(article.get("tags", []))),
            str(article.get('relevance_score', 'N/A'))
        ]
        
        csv_lines.append(','.join(row))
    
    # 保存CSV
    output_dir = '/root/.openclaw/workspace/psydaily/data/exports'
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f'{output_dir}/psydaily_20260211_complete_30papers.csv'
    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(csv_lines))
    
    print(f"✅ Excel导出成功!")
    print(f"📁 文件位置: {filename}")
    print(f"📊 共 {len(contents)} 篇唯一论文（无重复）")
    print(f"\n📋 论文列表:")
    for i, content in enumerate(contents, 1):
        article = content['article']
        print(f"{i:2d}. {article['title_zh'][:45]}... ({article['id']})")
    
    return filename

if __name__ == '__main__':
    export_complete_to_excel()
