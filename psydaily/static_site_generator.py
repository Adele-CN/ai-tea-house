#!/usr/bin/env python3
"""
PsyDaily 静态网页生成器
生成可搜索、可筛选的论文库网页
"""

import json
import os
from datetime import datetime

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>PsyDaily - 心理学研究论文库</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .filters {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 250px;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 0.8rem 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-select {{
            padding: 0.8rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            background: white;
            cursor: pointer;
        }}
        
        .papers-grid {{
            display: grid;
            gap: 1.5rem;
        }}
        
        .paper-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .paper-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .paper-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
            gap: 1rem;
        }}
        
        .paper-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
            line-height: 1.5;
            flex: 1;
        }}
        
        .paper-title .subtitle {{
            font-size: 0.95rem;
            font-weight: 400;
            color: #666;
            display: block;
            margin-top: 0.3rem;
            line-height: 1.4;
        }}
        
        .paper-if {{
            background: #667eea;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .paper-meta {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            color: #666;
        }}
        
        .paper-meta span {{
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }}
        
        .paper-abstract {{
            color: #555;
            line-height: 1.8;
            margin-bottom: 1rem;
        }}
        
        .paper-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .tag {{
            background: #f0f0f0;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.85rem;
            color: #666;
        }}
        
        .paper-actions {{
            margin-top: 1rem;
            display: flex;
            gap: 1rem;
        }}
        
        .btn {{
            padding: 0.5rem 1rem;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9rem;
            transition: background 0.2s;
        }}
        
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #5a6fd6;
        }}
        
        .btn-secondary {{
            background: #f0f0f0;
            color: #333;
            border: 1px solid #ddd;
        }}
        
        .btn-secondary:hover {{
            background: #e0e0e0;
        }}
        
        .paper-summary {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .summary-item {{
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }}
        
        .summary-item:last-child {{
            margin-bottom: 0;
        }}
        
        .summary-label {{
            font-weight: 600;
            color: #667eea;
        }}
        
        .language-badge {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            margin-left: 0.5rem;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            margin-top: 2rem;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .container {{
                padding: 1rem;
            }}
            
            .filters {{
                flex-direction: column;
            }}
            
            .search-box {{
                min-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>🧠 PsyDaily</h1>
        <p>心理学研究论文库 - 每日精选认知科学、神经科学、AI心理学</p>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{total_papers}</div>
                <div class="stat-label">收录论文</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_journals}</div>
                <div class="stat-label">来源期刊</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{update_date}</div>
                <div class="stat-label">最后更新</div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="filters">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索标题、摘要、期刊..." onkeyup="filterPapers()">
            </div>
            <select class="filter-select" id="journalFilter" onchange="filterPapers()">
                <option value="">所有期刊</option>
                {journal_options}
            </select>
            <select class="filter-select" id="tagFilter" onchange="filterPapers()">
                <option value="">所有主题</option>
                {tag_options}
            </select>
        </div>
        
        <div class="papers-grid" id="papersGrid">
            {papers_html}
        </div>
    </div>
    
    <footer class="footer">
        <p>PsyDaily - AI辅助心理学研究 | 由 Moon & Adele 维护</p>
        <p>数据更新时间: {update_time}</p>
    </footer>
    
    <script>
        const papers = {papers_json};
        
        function filterPapers() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const journalFilter = document.getElementById('journalFilter').value;
            const tagFilter = document.getElementById('tagFilter').value;
            
            const filtered = papers.filter(paper => {{
                const matchSearch = (
                    (paper.title_zh || '').toLowerCase().includes(searchTerm) ||
                    (paper.title_en || '').toLowerCase().includes(searchTerm) ||
                    (paper.abstract_zh || '').toLowerCase().includes(searchTerm) ||
                    (paper.journal_en || '').toLowerCase().includes(searchTerm)
                );
                
                const matchJournal = !journalFilter || paper.journal_en === journalFilter;
                const matchTag = !tagFilter || (paper.tags || []).includes(tagFilter);
                
                return matchSearch && matchJournal && matchTag;
            }});
            
            renderPapers(filtered);
        }}
        
        function renderPapers(papersToRender) {{
            const grid = document.getElementById('papersGrid');
            
            if (papersToRender.length === 0) {{
                grid.innerHTML = '<div style="text-align: center; padding: 3rem; color: #666;">没有找到匹配的论文</div>';
                return;
            }}
            
            grid.innerHTML = papersToRender.map(paper => `
                <div class="paper-card">
                    <div class="paper-header">
                        <div class="paper-title">${{paper.title_zh || paper.title_en}}</div>
                        <span class="paper-if">IF: ${{paper.impact_factor || 'N/A'}}</span>
                    </div>
                    <div class="paper-meta">
                        <span>📖 ${{paper.journal_en}}</span>
                        <span>📅 ${{paper.pub_date}}</span>
                        <span>🔬 ${{paper.tags ? paper.tags[0] : 'research'}}</span>
                    </div>
                    <div class="paper-abstract">${{paper.abstract_zh || paper.abstract_en || ''}}</div>
                    <div class="paper-tags">
                        ${{(paper.tags || []).map(tag => `<span class="tag">${{tag}}</span>`).join('')}}
                    </div>
                    <div class="paper-actions">
                        <a href="${{paper.scholar_url || '#'}}" class="btn btn-primary" target="_blank" title="在 Google Scholar 搜索此论文">🔍 Google Scholar</a>
                        <a href="https://www.google.com/search?q=${{encodeURIComponent(paper.title_en || paper.title_zh)}}" class="btn btn-secondary" target="_blank" title="在 Google 搜索">🌐 Google</a>
                    </div>
                </div>
            `).join('');
        }}
        
        // 初始渲染
        renderPapers(papers);
    </script>
</body>
</html>
'''


class StaticSiteGenerator:
    """静态网站生成器"""
    
    def __init__(self, data_dir=None, output_dir=None):
        # Auto-detect correct paths based on current directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = data_dir or os.path.join(script_dir, 'data')
        self.output_dir = output_dir or os.path.join(script_dir, 'site')
        self.papers = []
        
    def load_papers(self):
        """加载所有论文数据"""
        # 优先加载最新合并的论文库
        content_file = f'{self.data_dir}/content/daily_latest_complete.json'
        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.papers = [item['article'] for item in data]
        else:
            # 回退到旧文件
            content_file = f'{self.data_dir}/content/daily_20260211_complete.json'
            if os.path.exists(content_file):
                with open(content_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.papers = [item['article'] for item in data]
        
        # 加载RSS抓取的数据
        rss_file = f'{self.data_dir}/rss_papers.json'
        if os.path.exists(rss_file):
            with open(rss_file, 'r', encoding='utf-8') as f:
                rss_papers = json.load(f)
                # 去重添加
                seen = {p.get('title_en', p.get('title_zh', '')) for p in self.papers}
                for p in rss_papers:
                    title = p.get('title_en', p.get('title_zh', ''))
                    if title and title not in seen:
                        seen.add(title)
                        self.papers.append(p)
        
        # 为每篇论文生成搜索链接
        for p in self.papers:
            if not p.get('doi') and not p.get('url'):
                # 生成 Google Scholar 搜索链接
                title = p.get('title_en', p.get('title_zh', ''))
                if title:
                    import urllib.parse
                    query = urllib.parse.quote(title)
                    p['scholar_url'] = f'https://scholar.google.com/scholar?q={query}'
                else:
                    p['scholar_url'] = '#'
            else:
                p['scholar_url'] = p.get('doi') or p.get('url')
        
        print(f"📚 加载 {len(self.papers)} 篇论文")
        return self.papers
    
    def generate_html(self):
        """生成 HTML 页面"""
        
        # 统计数据
        total_papers = len(self.papers)
        journals = list(set(p.get('journal_en', 'Unknown') for p in self.papers))
        total_journals = len(journals)
        all_tags = []
        for p in self.papers:
            all_tags.extend(p.get('tags', []))
        unique_tags = list(set(all_tags))
        
        # 生成期刊选项
        journal_options = '\n'.join([f'<option value="{j}">{j}</option>' for j in sorted(journals)])
        
        # 生成标签选项
        tag_options = '\n'.join([f'<option value="{t}">{t}</option>' for t in sorted(unique_tags)[:20]])
        
        # 生成论文卡片 HTML
        papers_html = ''
        for p in self.papers:
            papers_html += f'''
            <div class="paper-card">
                <div class="paper-header">
                    <div class="paper-title">{self._format_title(p)}</div>
                    <span class="paper-if">IF: {p.get('impact_factor', 'N/A')}</span>
                </div>
                <div class="paper-meta">
                    <span>📖 {p.get('journal_en', 'Unknown')}</span>
                    <span>📅 {p.get('pub_date', 'N/A')}</span>
                </div>
                <div class="paper-abstract">{self._format_abstract(p)}</div>
                {self._generate_summary_html(p)}
                <div class="paper-tags">
                    {''.join([f'<span class="tag">{t}</span>' for t in p.get('tags', [])[:5]])}
                </div>
                <div class="paper-actions">
                    <a href="{p.get('doi_url') or p.get('url') or p.get('scholar_url', '#')}" class="btn btn-primary" target="_blank" title="查看原文">📄 查看原文</a>
                    <a href="{p.get('scholar_url', '#')}" class="btn btn-secondary" target="_blank" title="Google Scholar 搜索">🔍 Scholar</a>
                </div>
            </div>
            '''
        
        # 填充模板
        html = HTML_TEMPLATE.format(
            total_papers=total_papers,
            total_journals=total_journals,
            update_date=datetime.now().strftime('%Y-%m-%d'),
            journal_options=journal_options,
            tag_options=tag_options,
            papers_html=papers_html,
            papers_json=json.dumps(self.papers, ensure_ascii=False),
            update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        return html
    
    def _format_title(self, p):
        """格式化标题显示（双语）"""
        title_zh = p.get('title_zh', '')
        title_en = p.get('title_en', '')
        
        # 如果是中文论文，优先显示中文
        if p.get('language') == 'zh' and title_zh:
            if title_en and title_en != title_zh:
                return f"{title_zh}<br><span class='subtitle'>{title_en}</span>"
            return title_zh
        
        # 如果是英文论文，显示英文+中文翻译
        if title_en:
            if title_zh and title_zh != title_en and not title_zh.endswith('[待译]'):
                return f"{title_zh}<br><span class='subtitle'>{title_en}</span>"
            elif title_zh:
                return f"{title_zh}<br><span class='subtitle'>{title_en}</span>"
            return title_en
        
        return title_zh or '无标题'
    
    def _format_abstract(self, p):
        """格式化摘要显示（双语）"""
        abstract_zh = p.get('abstract_zh', '')
        abstract_en = p.get('abstract_en', '')
        
        # 中文论文
        if p.get('language') == 'zh' and abstract_zh:
            return abstract_zh[:300] + ('...' if len(abstract_zh) > 300 else '')
        
        # 英文论文 - 显示中文翻译（如果有）+ 英文
        if abstract_zh and not abstract_zh.startswith('【英文摘要】'):
            return f"{abstract_zh[:200]}..."
        elif abstract_en:
            return f"{abstract_en[:250]}... [中文翻译待完善]"
        
        return abstract_zh or abstract_en or '暂无摘要'
    
    def _generate_summary_html(self, paper):
        """生成论文核心摘要 HTML"""
        summary = paper.get('summary', {})
        if not summary and paper.get('core_contribution'):
            summary = {
                'core_contribution': paper.get('core_contribution'),
                'research_direction': paper.get('research_direction'),
            }
        
        if summary:
            html = '<div class="paper-summary">'
            if summary.get('core_contribution'):
                html += f'<div class="summary-item"><span class="summary-label">💡 核心贡献:</span> {summary["core_contribution"]}</div>'
            if summary.get('research_direction'):
                html += f'<div class="summary-item"><span class="summary-label">📚 研究方向:</span> {summary["research_direction"]}</div>'
            html += '</div>'
            return html
        return ''
    
    def build(self):
        """构建静态网站"""
        print("🚀 构建 PsyDaily 静态网站...")
        print("=" * 60)
        
        # 加载数据
        self.load_papers()
        
        # 生成 HTML
        html = self.generate_html()
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 保存 HTML
        output_file = f'{self.output_dir}/index.html'
        os.makedirs(self.output_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ 网站生成完成!")
        print(f"📁 输出文件: {output_file}")
        print(f"📊 统计: {len(self.papers)} 篇论文, {len(set(p.get('journal_en') for p in self.papers))} 个期刊")
        print(f"\n🌐 本地预览:")
        print(f"   cd {self.output_dir}")
        print(f"   python -m http.server 8080")
        print(f"   然后访问 http://localhost:8080")
        
        return output_file


def main():
    """主函数"""
    generator = StaticSiteGenerator()
    generator.build()


if __name__ == '__main__':
    main()
