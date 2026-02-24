#!/usr/bin/env python3
"""
PsyDaily 真实论文抓取系统 v2
使用 CrossRef API（无需 key，更稳定）
"""

import requests
import json
from datetime import datetime, timedelta
import os
import time

class RealPaperFetcher:
    """真实论文抓取器 - CrossRef 版本"""
    
    def __init__(self, output_dir=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = output_dir or os.path.join(script_dir, 'data', 'content')
        self.papers = []
        
        # CrossRef API
        self.crossref_base = "https://api.crossref.org/works"
        
        # 邮件地址（polite pool 要求）
        self.headers = {
            'User-Agent': 'PsyDaily Bot (mailto:adele@ai-tea.house)'
        }
    
    def fetch_crossref(self, query="psychology", days=7, rows=20):
        """
        从 CrossRef 抓取心理学论文
        
        Args:
            query: 搜索关键词
            days: 最近几天
            rows: 返回数量
        """
        print(f"🔍 CrossRef 搜索: '{query}' (最近 {days} 天)")
        
        # 计算日期
        filter_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            params = {
                'query': query,
                'filter': f'from-pub-date:{filter_date},type:journal-article',
                'rows': rows,
                'sort': 'published',
                'order': 'desc',
                'select': 'DOI,title,author,container-title,published-print,published-online,abstract,link'
            }
            
            response = requests.get(
                self.crossref_base,
                params=params,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"  ❌ HTTP {response.status_code}")
                return []
            
            data = response.json()
            items = data.get('message', {}).get('items', [])
            print(f"  找到 {len(items)} 篇")
            
            papers = []
            current_year = datetime.now().year
            for item in items:
                paper = self._parse_crossref_item(item)
                if paper:
                    # 过滤掉明显错误的日期（未来或太早）
                    try:
                        pub_year = int(paper['pub_date'][:4]) if paper['pub_date'] else 0
                        if 2020 <= pub_year <= current_year + 1:  # 只保留 2020 年至今的论文
                            papers.append(paper)
                        else:
                            print(f"    ⚠️ 跳过异常日期: {paper['pub_date']}")
                    except:
                        papers.append(paper)  # 日期解析失败也保留
            
            print(f"  ✅ 成功解析 {len(papers)} 篇（过滤后）")
            return papers
            
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            return []
    
    def _parse_crossref_item(self, item):
        """解析 CrossRef 条目"""
        try:
            # 标题
            titles = item.get('title', [])
            title = titles[0] if titles else 'Untitled'
            
            # 作者
            authors = []
            for author in item.get('author', [])[:3]:
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                if name:
                    authors.append(name)
            
            # 期刊
            containers = item.get('container-title', [])
            journal = containers[0] if containers else 'Unknown Journal'
            
            # 日期
            pub_date = ''
            published = item.get('published-print', item.get('published-online', {}))
            if published:
                date_parts = published.get('date-parts', [[]])[0]
                pub_date = '-'.join(str(p) for p in date_parts if p)
            
            # DOI 和链接
            doi = item.get('DOI', '')
            doi_url = f"https://doi.org/{doi}" if doi else ''
            
            # 尝试找原文链接
            links = item.get('link', [])
            pdf_url = ''
            for link in links:
                if 'pdf' in link.get('content-type', '').lower():
                    pdf_url = link.get('URL', '')
                    break
            
            # 过滤临床医学期刊
            clinical_keywords = [
                'clinical medicine', 'lancet', 'new england journal of medicine',
                'jama', 'bmj', 'clinical', 'medical', 'surgery', 'oncology',
                'cardiology', 'nephrology', 'dermatology', 'gastroenterology',
                'infectious disease', 'radiology', 'pathology', 'anesthesia',
                'transplantation', 'rheumatology', 'hematology'
            ]
            if any(kw in journal.lower() for kw in clinical_keywords):
                return None  # 跳过临床医学期刊
            
            # Scholar 搜索链接
            scholar_url = f"https://scholar.google.com/scholar?q={requests.utils.quote(title)}"
            
            # 摘要（CrossRef 很少有摘要）
            abstract = item.get('abstract', '')
            if not abstract:
                abstract = f"Published in {journal}. DOI: {doi}" if doi else f"Published in {journal}."
            
            # 生成中文翻译（简化版，实际可用AI API优化）
            title_zh = self._translate_title(title)
            abstract_zh = self._translate_abstract(abstract[:300])
            
            return {
                'id': f"crossref_{doi.replace('/', '_')}" if doi else f"crossref_{hash(title) % 1000000}",
                'title_en': title,
                'title_zh': title_zh,
                'abstract_en': abstract[:500] if len(abstract) > 500 else abstract,
                'abstract_zh': abstract_zh,
                'authors': authors if authors else ['Unknown'],
                'journal_en': journal,
                'journal_zh': '',
                'pub_date': pub_date[:10] if pub_date else datetime.now().strftime('%Y-%m-%d'),
                'doi': doi,
                'doi_url': doi_url,
                'pdf_url': pdf_url,
                'url': doi_url or pdf_url or scholar_url,
                'scholar_url': scholar_url,
                'source': 'crossref',
                'impact_factor': self._estimate_if(journal),
                'tags': self._auto_tag(title, abstract),
                'fetched_at': datetime.now().isoformat(),
                'is_real': True  # 标记为真实论文
            }
            
        except Exception as e:
            print(f"    ⚠️ 解析失败: {e}")
            return None
    
    def _estimate_if(self, journal_name):
        """估算影响因子"""
        journal_if = {
            'Nature Human Behaviour': 22.3,
            'Nature Reviews Psychology': 14.5,
            'Psychological Science': 8.4,
            'Trends in Cognitive Sciences': 19.9,
            'Annual Review of Psychology': 26.8,
            'Psychological Bulletin': 22.4,
            'Journal of Personality and Social Psychology': 5.9,
            'NeuroImage': 7.4,
            'Cognition': 3.5,
            'Computers in Human Behavior': 9.9,
            'Addictive Behaviors': 4.1,
            'Sleep Medicine Reviews': 11.2,
            'Journal of Experimental Psychology': 3.2,
            'Behaviour Research and Therapy': 4.2,
            'Frontiers in Psychology': 3.8,
            'BMC Psychology': 2.3,
            'PLOS ONE': 3.7,
            'Scientific Reports': 4.6,
        }
        
        for key, if_value in journal_if.items():
            if key.lower() in journal_name.lower():
                return if_value
        
        return 2.5  # 默认 IF
    
    def _auto_tag(self, title, abstract):
        """自动标签"""
        text = (title + ' ' + abstract).lower()
        tags = []
        
        tag_keywords = {
            'cognitive': ['cognitive', 'attention', 'memory', 'decision', 'executive function'],
            'mental_health': ['depression', 'anxiety', 'stress', 'mental health', 'disorder', 'therapy'],
            'social': ['social', 'relationship', 'interaction', 'communication', 'interpersonal'],
            'neuroscience': ['brain', 'neural', 'neuro', 'fmri', 'eeg', 'neuroscience', 'cortex'],
            'technology': ['digital', 'internet', 'smartphone', 'social media', 'ai', 'technology', 'online'],
            'sleep': ['sleep', 'insomnia', 'circadian', 'dream'],
            'addiction': ['addiction', 'addictive', 'substance', 'craving', 'abuse'],
            'wellbeing': ['well-being', 'wellbeing', 'happiness', 'life satisfaction', 'quality of life'],
            'developmental': ['child', 'adolescent', 'development', 'aging', 'lifespan'],
            'clinical': ['clinical', 'treatment', 'intervention', 'psychotherapy', 'patient'],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)
        
        return tags[:3] if tags else ['psychology']
    
    def _translate_title(self, title):
        """翻译标题为中文（简化版，使用关键词映射）"""
        # AI心理学关键词翻译映射
        translations = {
            'artificial intelligence': '人工智能',
            'AI': 'AI',
            'chatbot': '聊天机器人',
            'machine learning': '机器学习',
            'mental health': '心理健康',
            'cognitive': '认知',
            'therapy': '治疗',
            'digital': '数字',
            'social media': '社交媒体',
            'algorithm': '算法',
            'behavior': '行为',
            'addiction': '成瘾',
            'depression': '抑郁',
            'anxiety': '焦虑',
            'stress': '压力',
            'intervention': '干预',
            'treatment': '治疗',
            'psychology': '心理学',
            'neuroscience': '神经科学',
            'cognitive': '认知',
        }
        
        # 简单的关键词替换翻译
        translated = title
        for en, zh in translations.items():
            if en.lower() in title.lower():
                translated = f"【{zh}】{translated}"
                break
        
        return f"{translated} [待译]"
    
    def _translate_abstract(self, abstract):
        """翻译摘要为中文（简化版）"""
        if not abstract or abstract == f"Published in journal.":
            return "摘要暂不可用"
        
        # 简化的翻译提示
        return f"【英文摘要】{abstract[:100]}... [点击阅读原文查看完整内容]"
    
    def fetch_all_sources(self, max_per_query=15):
        """抓取所有来源 - AI心理学优先"""
        print("=" * 70)
        print("🚀 抓取真实心理学论文 - AI相关优先 (CrossRef)")
        print("=" * 70)
        
        # AI心理学关键词（非临床）
        queries = [
            ('artificial intelligence cognitive psychology', 30, max_per_query),
            ('AI human behavior', 30, max_per_query),
            ('chatbot communication', 30, max_per_query),
            ('machine learning decision making', 30, max_per_query),
            ('digital psychology social', 30, max_per_query),
            ('social media psychology', 30, max_per_query),
            ('algorithm perception', 30, max_per_query),
            ('human computer interaction', 30, max_per_query),
            ('robotics psychology', 30, max_per_query),
            ('virtual reality psychology', 30, max_per_query),
        ]
        
        all_papers = []
        for query, days, rows in queries:
            papers = self.fetch_crossref(query, days=days, rows=rows)
            all_papers.extend(papers)
            time.sleep(1)  # 礼貌间隔
        
        # 去重（基于 DOI 或标题）
        seen = set()
        unique_papers = []
        for p in all_papers:
            key = p['doi'] if p['doi'] else p['title_en'].lower()
            if key not in seen:
                seen.add(key)
                unique_papers.append(p)
        
        self.papers = unique_papers
        print(f"\n📊 总计: {len(unique_papers)} 篇唯一真实论文")
        return unique_papers
    
    def save_papers(self, filename=None):
        """保存论文"""
        if filename is None:
            filename = f"real_papers_{datetime.now().strftime('%Y%m%d')}.json"
        
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        
        formatted = [{'article': p} for p in self.papers]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(formatted, f, ensure_ascii=False, indent=2)
        
        print(f"💾 已保存: {filepath}")
        return filepath
    
    def preview(self, n=10):
        """预览"""
        print(f"\n📄 最新 {min(n, len(self.papers))} 篇真实论文:")
        print("-" * 70)
        for i, p in enumerate(self.papers[:n], 1):
            print(f"\n{i}. {p['title_en'][:70]}...")
            print(f"   期刊: {p['journal_en']}")
            print(f"   日期: {p['pub_date']}")
            print(f"   IF: {p['impact_factor']}")
            print(f"   DOI: {p['doi'][:50]}..." if len(p['doi']) > 50 else f"   DOI: {p['doi']}")
            print(f"   标签: {', '.join(p['tags'])}")
            print(f"   🔗 {p['doi_url'] or p['scholar_url']}")


def main():
    """主函数"""
    fetcher = RealPaperFetcher()
    
    # 抓取
    papers = fetcher.fetch_all_sources(max_per_query=10)
    
    # 预览
    fetcher.preview(10)
    
    # 保存
    fetcher.save_papers()
    
    # 同时更新 latest_complete.json 供网站使用
    latest_file = os.path.join(fetcher.output_dir, 'daily_latest_complete.json')
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump([{'article': p} for p in papers], f, ensure_ascii=False, indent=2)
    print(f"\n✅ 已更新网站数据源: {latest_file}")


if __name__ == '__main__':
    main()
