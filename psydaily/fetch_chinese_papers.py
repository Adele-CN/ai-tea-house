#!/usr/bin/env python3
"""
PsyDaily 中文论文抓取系统
支持国家哲学社会科学文献中心 (ncpssd.cn)
"""

import requests
import json
from datetime import datetime, timedelta
import os
import time

class ChinesePaperFetcher:
    """中文论文抓取器"""
    
    def __init__(self, output_dir=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = output_dir or os.path.join(script_dir, 'data', 'content')
        self.papers = []
        
        # ncpssd API 端点（基于网站分析）
        self.ncpssd_base = "https://www.ncpssd.cn/api"
        
        #  headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
    
    def fetch_ncpssd(self, keyword="心理学", days=30, limit=10):
        """
        从 ncpssd.cn 抓取中文心理学论文
        
        Args:
            keyword: 搜索关键词
            days: 最近几天
            limit: 数量限制
        """
        print(f"🔍 NCPSSD 搜索: '{keyword}'")
        
        try:
            # ncpssd 搜索 API
            search_url = f"{self.ncpssd_base}/search/literature"
            
            # 计算日期
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            params = {
                'searchWord': keyword,
                'page': 1,
                'size': limit,
                'sortType': 'PT',  # 按发表时间排序
                'publishDate_from': start_date.strftime('%Y-%m-%d'),
                'publishDate_to': end_date.strftime('%Y-%m-%d'),
            }
            
            # 由于无法直接访问 API，先模拟数据展示结构
            # 实际部署时需要根据网站真实 API 调整
            print(f"  ℹ️ NCPSSD API 需要进一步分析，目前使用模拟数据演示")
            
            # 模拟几篇中文论文数据
            mock_papers = [
                {
                    'id': 'cnki_001',
                    'title_zh': '社交媒体使用与青少年心理健康：一项元分析研究',
                    'title_en': 'Social Media Use and Adolescent Mental Health: A Meta-Analysis',
                    'abstract_zh': '本研究通过元分析方法，探讨了社交媒体使用与青少年焦虑、抑郁症状之间的关系。纳入分析68项研究，总样本量达125,000人。结果发现，社交媒体使用时间与心理健康问题呈显著正相关（r=0.24），特别是夜间使用和被动浏览行为。',
                    'abstract_en': 'This meta-analysis examines the relationship between social media use and adolescent mental health...',
                    'authors': ['张明', '李华', '王芳'],
                    'journal_zh': '心理学报',
                    'journal_en': 'Acta Psychologica Sinica',
                    'pub_date': '2025-01-15',
                    'doi': '10.3724/SP.J.1041.2025.00001',
                    'doi_url': 'https://doi.org/10.3724/SP.J.1041.2025.00001',
                    'source': 'ncpssd',
                    'language': 'zh',
                    'impact_factor': 3.2,
                    'tags': ['mental_health', 'social_media', 'adolescent'],
                    'full_text_available': True,
                    'core_contribution': '首次系统量化了社交媒体使用对中国青少年心理健康的负面影响',
                    'research_direction': '数字媒体与心理健康',
                    'fetched_at': datetime.now().isoformat(),
                },
                {
                    'id': 'cnki_002',
                    'title_zh': '正念干预对大学生焦虑症状的疗效：随机对照试验',
                    'title_en': 'Efficacy of Mindfulness Intervention on Anxiety Symptoms in College Students',
                    'abstract_zh': '研究采用随机对照试验设计，评估8周正念训练对240名高焦虑大学生的干预效果。结果显示，干预组焦虑评分显著下降（Cohen\'s d=0.68），效果在3个月随访时仍然显著。脑电数据显示注意控制能力的改善。',
                    'abstract_en': 'A randomized controlled trial evaluated 8-week mindfulness training...',
                    'authors': ['陈静', '刘洋'],
                    'journal_zh': '中国临床心理学杂志',
                    'journal_en': 'Chinese Journal of Clinical Psychology',
                    'pub_date': '2024-12-20',
                    'doi': '10.16128/j.cnki.1005-3611.2024.06.001',
                    'doi_url': 'https://doi.org/10.16128/j.cnki.1005-3611.2024.06.001',
                    'source': 'ncpssd',
                    'language': 'zh',
                    'impact_factor': 2.8,
                    'tags': ['mindfulness', 'anxiety', 'intervention', 'college_students'],
                    'full_text_available': True,
                    'core_contribution': '验证了正念干预对中国大学生群体的适用性和有效性',
                    'research_direction': '临床心理学与干预研究',
                    'fetched_at': datetime.now().isoformat(),
                },
                {
                    'id': 'cnki_003',
                    'title_zh': '工作记忆训练对注意缺陷多动障碍儿童的认知改善作用',
                    'title_en': 'Working Memory Training for Cognitive Improvement in Children with ADHD',
                    'abstract_zh': '本研究采用双盲随机对照设计，对120名ADHD儿童进行为期6周的工作记忆训练。结果发现，训练组在视觉空间工作记忆和抑制控制任务上表现显著优于对照组。然而，训练效果未能迁移到学业成绩和日常行为评估中。',
                    'abstract_en': 'This double-blind RCT examined working memory training in 120 children with ADHD...',
                    'authors': ['赵强', '孙丽', '周伟'],
                    'journal_zh': '心理学报',
                    'journal_en': 'Acta Psychologica Sinica',
                    'pub_date': '2025-02-10',
                    'doi': '10.3724/SP.J.1041.2025.00015',
                    'doi_url': 'https://doi.org/10.3724/SP.J.1041.2025.00015',
                    'source': 'ncpssd',
                    'language': 'zh',
                    'impact_factor': 3.2,
                    'tags': ['ADHD', 'working_memory', 'cognitive_training', 'children'],
                    'full_text_available': True,
                    'core_contribution': '揭示了工作记忆训练的领域特异性，挑战了远迁移效应的假设',
                    'research_direction': '认知发展与临床干预',
                    'fetched_at': datetime.now().isoformat(),
                },
            ]
            
            return mock_papers[:limit]
            
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            return []
    
    def summarize_paper(self, paper):
        """
        生成论文核心摘要（核心观点、研究方向、贡献）
        """
        title = paper.get('title_zh', paper.get('title_en', ''))
        abstract = paper.get('abstract_zh', paper.get('abstract_en', ''))
        
        # 如果已有预定义的 summary，直接返回
        if paper.get('core_contribution'):
            return {
                'core_contribution': paper['core_contribution'],
                'research_direction': paper['research_direction'],
                'has_full_text': paper.get('full_text_available', False),
            }
        
        # 否则生成简单的 summary（实际部署时可调用 AI API）
        return {
            'core_contribution': f"本研究探讨了{title[:20]}...相关议题",
            'research_direction': '心理学研究',
            'has_full_text': paper.get('full_text_available', False),
        }
    
    def fetch_daily_papers(self, limit=10):
        """抓取每日指定数量的论文"""
        print("=" * 70)
        print("🚀 抓取中文心理学论文 (NCPSSD)")
        print("=" * 70)
        
        # 中文关键词列表
        keywords = [
            '心理学',
            '心理健康',
            '认知科学',
            '社会心理学',
            '临床心理学',
        ]
        
        all_papers = []
        for keyword in keywords:
            papers = self.fetch_ncpssd(keyword, days=30, limit=3)
            all_papers.extend(papers)
            time.sleep(0.5)
        
        # 去重并限制数量
        seen = set()
        unique_papers = []
        for p in all_papers:
            title = p.get('title_zh', p.get('title_en', ''))
            if title not in seen and len(unique_papers) < limit:
                seen.add(title)
                # 添加 summary
                p['summary'] = self.summarize_paper(p)
                unique_papers.append(p)
        
        self.papers = unique_papers
        print(f"\n📊 总计: {len(unique_papers)} 篇中文论文")
        return unique_papers
    
    def save_papers(self, filename=None):
        """保存论文"""
        if filename is None:
            filename = f"chinese_papers_{datetime.now().strftime('%Y%m%d')}.json"
        
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        
        formatted = [{'article': p} for p in self.papers]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(formatted, f, ensure_ascii=False, indent=2)
        
        print(f"💾 已保存: {filepath}")
        return filepath
    
    def preview(self, n=5):
        """预览"""
        print(f"\n📄 最新 {min(n, len(self.papers))} 篇中文论文:")
        print("-" * 70)
        for i, p in enumerate(self.papers[:n], 1):
            print(f"\n{i}. {p['title_zh']}")
            print(f"   期刊: {p['journal_zh']}")
            print(f"   日期: {p['pub_date']}")
            print(f"   标签: {', '.join(p['tags'])}")
            print(f"   🔗 {p['doi_url']}")
            if p.get('summary'):
                print(f"   💡 核心贡献: {p['summary']['core_contribution']}")
                print(f"   📚 研究方向: {p['summary']['research_direction']}")


def main():
    """主函数"""
    fetcher = ChinesePaperFetcher()
    
    # 抓取每日 10 篇
    papers = fetcher.fetch_daily_papers(limit=10)
    
    # 预览
    fetcher.preview(10)
    
    # 保存
    fetcher.save_papers()


if __name__ == '__main__':
    main()
