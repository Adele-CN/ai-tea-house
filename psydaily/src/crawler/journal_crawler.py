import feedparser
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

class JournalCrawler:
    """心理学期刊爬虫"""
    
    # 期刊RSS源配置
    SOURCES = {
        '心理学报': {
            'url': 'http://journal.psych.ac.cn/rss',
            'type': 'rss',
            'language': 'zh'
        },
        '中国临床心理学杂志': {
            'url': 'http://www.cjcp.org/rss',
            'type': 'rss', 
            'language': 'zh'
        },
        '心理科学进展': {
            'url': 'http://journal.psych.ac.cn/progress/rss',
            'type': 'rss',
            'language': 'zh'
        }
    }
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def fetch_rss(self, source_name):
        """抓取RSS feed"""
        source = self.SOURCES.get(source_name)
        if not source:
            print(f"未知来源: {source_name}")
            return []
        
        try:
            feed = feedparser.parse(source['url'])
            articles = []
            
            for entry in feed.entries[:5]:  # 取最新5篇
                article = {
                    'title': entry.get('title', ''),
                    'abstract': entry.get('summary', entry.get('description', '')),
                    'url': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'source': source_name,
                    'language': source['language'],
                    'crawled_at': datetime.now().isoformat()
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"抓取失败 {source_name}: {e}")
            return []
    
    def fetch_all(self):
        """抓取所有期刊"""
        all_articles = []
        for source_name in self.SOURCES.keys():
            articles = self.fetch_rss(source_name)
            all_articles.extend(articles)
            print(f"✓ {source_name}: {len(articles)}篇")
        
        # 保存到文件
        self.save_articles(all_articles)
        return all_articles
    
    def save_articles(self, articles):
        """保存文章到JSON"""
        filename = f"{self.data_dir}/articles_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存到: {filename}")


if __name__ == '__main__':
    # 测试爬虫
    crawler = JournalCrawler()
    articles = crawler.fetch_all()
    print(f"\n总计: {len(articles)}篇文章")
