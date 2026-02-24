#!/usr/bin/env python3
"""
PsyDaily - 心理学期刊爬虫
中英文混合数据源
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import time

class JournalCrawler:
    """心理学期刊爬虫 - 中英文混合"""
    
    # 中英文期刊RSS源
    SOURCES = {
        # 中文期刊
        '心理学报': {
            'url': 'https://journal.psych.ac.cn/rss',  # 需要验证真实URL
            'type': 'rss',
            'language': 'zh',
            'field': 'general'
        },
        '心理科学进展': {
            'url': 'https://journal.psych.ac.cn/progress/rss',
            'type': 'rss',
            'language': 'zh',
            'field': 'general'
        },
        
        # 英文期刊 - 使用可靠的RSS源
        'Nature Human Behaviour': {
            'url': 'https://www.nature.com/nathumbehav.rss',
            'type': 'rss',
            'language': 'en',
            'field': 'neuroscience',
            'impact_factor': 29.9
        },
        'Psychological Science': {
            'url': 'https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=jpss&type=etoc&feed=rss',
            'type': 'rss',
            'language': 'en',
            'field': 'psychology',
            'impact_factor': 8.2
        },
        'Journal of Experimental Psychology': {
            'url': 'https://psycnet.apa.org/journals/xge.rss',
            'type': 'rss', 
            'language': 'en',
            'field': 'experimental',
            'impact_factor': 5.6
        }
    }
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.headers = {
            'User-Agent': 'PsyDailyBot/1.0 (Academic Research Purpose)'
        }
    
    def fetch_rss(self, source_name):
        """抓取RSS feed"""
        source = self.SOURCES.get(source_name)
        if not source:
            return []
        
        try:
            print(f"  正在抓取: {source_name}...")
            feed = feedparser.parse(source['url'])
            
            if feed.bozo:
                print(f"  ⚠️ 警告: {source_name} RSS格式可能有问题")
            
            articles = []
            for entry in feed.entries[:3]:  # 取最新3篇
                article = {
                    'title': entry.get('title', '').strip(),
                    'abstract': self._extract_abstract(entry),
                    'url': entry.get('link', ''),
                    'published': entry.get('published', entry.get('updated', '')),
                    'source': source_name,
                    'language': source['language'],
                    'field': source.get('field', 'general'),
                    'impact_factor': source.get('impact_factor', 0),
                    'crawled_at': datetime.now().isoformat()
                }
                articles.append(article)
            
            print(f"  ✓ {source_name}: {len(articles)}篇")
            return articles
            
        except Exception as e:
            print(f"  ✗ {source_name} 抓取失败: {e}")
            return []
    
    def _extract_abstract(self, entry):
        """提取摘要"""
        # 尝试多个可能的字段
        abstract = entry.get('summary', '')
        if not abstract:
            abstract = entry.get('description', '')
        if not abstract and 'content' in entry:
            abstract = entry.content[0].value if entry.content else ''
        
        # 清理HTML标签
        if abstract:
            soup = BeautifulSoup(abstract, 'html.parser')
            abstract = soup.get_text(separator=' ').strip()
            # 限制长度
            if len(abstract) > 500:
                abstract = abstract[:500] + '...'
        
        return abstract
    
    def fetch_all(self, sources=None):
        """抓取所有期刊"""
        if sources is None:
            sources = list(self.SOURCES.keys())
        
        print(f"\n📥 开始抓取 {len(sources)} 个期刊...")
        print("-" * 50)
        
        all_articles = []
        for source_name in sources:
            articles = self.fetch_rss(source_name)
            all_articles.extend(articles)
            time.sleep(1)  # 礼貌性延迟
        
        print("-" * 50)
        print(f"✓ 总计: {len(all_articles)} 篇文章")
        
        # 保存
        if all_articles:
            self.save_articles(all_articles)
        
        return all_articles
    
    def save_articles(self, articles):
        """保存文章到JSON"""
        filename = f"{self.data_dir}/articles_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存: {filename}")


def demo():
    """演示"""
    print("""
╔══════════════════════════════════════════╗
║     PsyDaily 期刊爬虫测试               ║
║     中英文混合数据源                    ║
╚══════════════════════════════════════════╝
    """)
    
    crawler = JournalCrawler()
    
    # 测试抓取
    test_sources = ['Nature Human Behaviour', '心理科学进展']
    articles = crawler.fetch_all(test_sources)
    
    if articles:
        print("\n📄 文章示例:")
        for i, article in enumerate(articles[:2], 1):
            print(f"\n  {i}. {article['title'][:50]}...")
            print(f"     来源: {article['source']} ({article['language']})")
            print(f"     影响因子: {article.get('impact_factor', 'N/A')}")


if __name__ == '__main__':
    demo()
