#!/usr/bin/env python3
"""
PsyDaily RSS 抓取模块
支持 PubMed, PsycINFO 等学术数据库
"""

import feedparser
import requests
import json
import re
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

# RSS 源配置
RSS_SOURCES = {
    'pubmed_psychology': {
        'name': 'PubMed Psychology',
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1nH-_ZcrhcXRArTxM9h_UEAOS8gzeGr9dXTz5rJKPS1L6bp1/?limit=15&utm_campaign=pubmed-2&fc=20250223000000',
        'enabled': True
    },
    'pubmed_cognitive': {
        'name': 'PubMed Cognitive Science',
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1nH-_ZcrhcXRArTxM9h_UEAOS8gzeGr9dXTz5rJKPS1L6bp1/?term=cognitive+science&limit=15',
        'enabled': True
    },
    'pubmed_neuroscience': {
        'name': 'PubMed Neuroscience',
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/search/1nH-_ZcrhcXRArTxM9h_UEAOS8gzeGr9dXTz5rJKPS1L6bp1/?term=neuroscience&limit=15',
        'enabled': True
    },
    'frontiers_psychology': {
        'name': 'Frontiers in Psychology',
        'url': 'https://www.frontiersin.org/journals/psychology/rss',
        'enabled': True
    }
}

class RSSFetcher:
    """RSS 抓取器"""
    
    def __init__(self, output_dir='/root/.openclaw/workspace/psydaily/data'):
        self.output_dir = output_dir
        self.papers = []
        
    def fetch_pubmed(self, source_key='pubmed_psychology'):
        """抓取 PubMed RSS"""
        source = RSS_SOURCES.get(source_key)
        if not source or not source['enabled']:
            return []
        
        print(f"📡 抓取 {source['name']}...")
        
        try:
            feed = feedparser.parse(source['url'])
            papers = []
            
            for entry in feed.entries[:10]:  # 取前10篇
                paper = self._parse_pubmed_entry(entry)
                if paper:
                    papers.append(paper)
            
            print(f"✅ 获取 {len(papers)} 篇")
            return papers
            
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            return []
    
    def _parse_pubmed_entry(self, entry):
        """解析 PubMed 条目"""
        try:
            # 提取标题
            title = entry.get('title', '').strip()
            
            # 提取作者
            authors = []
            if 'authors' in entry:
                authors = [a.get('name', '') for a in entry.authors]
            elif 'author' in entry:
                authors = [entry.author]
            
            # 提取摘要
            summary = entry.get('summary', '')
            # 清理 HTML
            summary = re.sub('<[^<]+?>', '', summary)
            
            # 提取期刊信息
            journal = ''
            if 'dc_source' in entry:
                journal = entry.dc_source
            
            # 提取日期
            pub_date = entry.get('published', '')[:10]
            
            # 提取 DOI/链接
            link = entry.get('link', '')
            pmid = self._extract_pmid(link)
            
            return {
                'id': f'pubmed_{pmid}',
                'title_en': title,
                'title_zh': '',  # 待翻译
                'abstract_en': summary[:500] + '...' if len(summary) > 500 else summary,
                'abstract_zh': '',
                'authors': authors[:3],  # 前3个作者
                'journal_en': journal,
                'journal_zh': '',
                'pub_date': pub_date,
                'doi': link,
                'pmid': pmid,
                'source': 'pubmed',
                'fetched_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ 解析条目失败: {e}")
            return None
    
    def _extract_pmid(self, link):
        """从链接提取 PMID"""
        match = re.search(r'/(\d+)/?$', link)
        return match.group(1) if match else ''
    
    def fetch_all_sources(self):
        """抓取所有启用的源"""
        all_papers = []
        
        for source_key in RSS_SOURCES:
            papers = self.fetch_pubmed(source_key)
            all_papers.extend(papers)
        
        # 去重（基于标题）
        seen_titles = set()
        unique_papers = []
        for p in all_papers:
            if p['title_en'] not in seen_titles:
                seen_titles.add(p['title_en'])
                unique_papers.append(p)
        
        self.papers = unique_papers
        print(f"\n📊 总计: {len(unique_papers)} 篇唯一论文")
        return unique_papers
    
    def save_to_json(self, filename='rss_papers.json'):
        """保存到 JSON"""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
        filepath = f'{self.output_dir}/{filename}'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.papers, f, ensure_ascii=False, indent=2)
        
        print(f"💾 已保存到 {filepath}")
        return filepath
    
    def filter_psychology_papers(self, papers=None):
        """筛选心理学相关论文"""
        if papers is None:
            papers = self.papers
        
        keywords = [
            'psychology', 'cognitive', 'behavior', 'mental', 'brain',
            'neuroscience', 'attention', 'memory', 'decision', 'emotion',
            'anxiety', 'depression', 'stress', 'sleep', 'social'
        ]
        
        filtered = []
        for p in papers:
            text = (p['title_en'] + ' ' + p['abstract_en']).lower()
            if any(kw in text for kw in keywords):
                filtered.append(p)
        
        print(f"🎯 心理学相关: {len(filtered)}/{len(papers)} 篇")
        return filtered


def main():
    """测试运行"""
    print("🚀 PsyDaily RSS 抓取器")
    print("=" * 60)
    
    fetcher = RSSFetcher()
    
    # 抓取所有源
    papers = fetcher.fetch_all_sources()
    
    # 筛选心理学论文
    psych_papers = fetcher.filter_psychology_papers(papers)
    
    # 保存
    fetcher.save_to_json()
    
    # 显示预览
    print("\n📄 最新5篇:")
    for i, p in enumerate(psych_papers[:5], 1):
        print(f"{i}. {p['title_en'][:60]}...")
        print(f"   {p['journal_en']} | {p['pub_date']}")

if __name__ == '__main__':
    main()
