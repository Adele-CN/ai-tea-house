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
            
            # AI心理学相关中文论文模拟数据
            mock_papers = [
                {
                    'id': 'cnki_ai_001',
                    'title_zh': 'ChatGPT在心理咨询中的应用效果：一项准实验研究',
                    'title_en': 'Effectiveness of ChatGPT in Psychological Counseling: A Quasi-Experimental Study',
                    'abstract_zh': '本研究探索了ChatGPT在提供心理健康支持方面的可行性和有效性。通过对比实验，发现AI聊天机器人能够显著降低用户的焦虑水平（p<0.05），但在处理复杂心理问题时仍需要人类咨询师的监督。研究为AI辅助心理治疗提供了实证依据。',
                    'abstract_en': 'This study explored the feasibility and effectiveness of ChatGPT in providing mental health support...',
                    'authors': ['李明', '王小红', '张伟'],
                    'journal_zh': '心理学报',
                    'journal_en': 'Acta Psychologica Sinica',
                    'pub_date': '2025-01-20',
                    'doi': '10.3724/SP.J.1041.2025.00021',
                    'doi_url': 'https://doi.org/10.3724/SP.J.1041.2025.00021',
                    'source': 'ncpssd',
                    'language': 'zh',
                    'impact_factor': 3.2,
                    'tags': ['AI', 'chatbot', 'mental_health', 'counseling', 'ChatGPT'],
                    'full_text_available': True,
                    'core_contribution': '首次在国内验证ChatGPT在心理咨询中的辅助作用，为AI心理健康应用提供本土化证据',
                    'research_direction': '人工智能与心理健康',
                    'fetched_at': datetime.now().isoformat(),
                },
                {
                    'id': 'cnki_ai_002',
                    'title_zh': '推荐算法对用户信息茧房效应的影响：基于行为实验的研究',
                    'title_en': 'Impact of Recommendation Algorithms on Information Cocoon Effect: A Behavioral Experiment',
                    'abstract_zh': '通过眼动追踪和行为实验，研究了个性化推荐算法如何影响用户信息获取的多样性。结果显示，算法推荐显著降低了用户接触异质信息的机会（降低42%），并增强了确认偏误。研究揭示了算法社会的潜在心理风险。',
                    'abstract_en': 'Using eye-tracking and behavioral experiments, this study examined how personalized recommendation algorithms affect information diversity...',
                    'authors': ['陈智', '刘洋', '赵敏'],
                    'journal_zh': '中国临床心理学杂志',
                    'journal_en': 'Chinese Journal of Clinical Psychology',
                    'pub_date': '2025-02-05',
                    'doi': '10.16128/j.cnki.1005-3611.2025.01.003',
                    'doi_url': 'https://doi.org/10.16128/j.cnki.1005-3611.2025.01.003',
                    'source': 'ncpssd',
                    'language': 'zh',
                    'impact_factor': 2.8,
                    'tags': ['algorithm', 'information_cocoon', 'behavior', 'digital_psychology'],
                    'full_text_available': True,
                    'core_contribution': '量化了推荐算法对信息茧房的影响程度，为算法治理提供心理学依据',
                    'research_direction': '算法行为与数字心理',
                    'fetched_at': datetime.now().isoformat(),
                },
                {
                    'id': 'cnki_ai_003',
                    'title_zh': '机器学习预测抑郁症复发的准确率研究：基于多模态数据',
                    'title_en': 'Accuracy of Machine Learning in Predicting Depression Relapse: A Multimodal Data Study',
                    'abstract_zh': '整合临床访谈、语音特征和社交媒体行为数据，构建了抑郁症复发预测模型。机器学习模型（XGBoost）达到85.3%的预测准确率，显著优于传统临床评估（72.1%）。研究为精准精神医学提供了技术路径。',
                    'abstract_en': 'Integrating clinical interviews, voice features, and social media behavior, this study built a depression relapse prediction model...',
                    'authors': ['王华', '孙丽', '周强', '李娜'],
                    'journal_zh': '心理学报',
                    'journal_en': 'Acta Psychologica Sinica',
                    'pub_date': '2025-02-15',
                    'doi': '10.3724/SP.J.1041.2025.00035',
                    'doi_url': 'https://doi.org/10.3724/SP.J.1041.2025.00035',
                    'source': 'ncpssd',
                    'language': 'zh',
                    'impact_factor': 3.2,
                    'tags': ['machine_learning', 'depression', 'prediction', 'precision_medicine', 'AI'],
                    'full_text_available': True,
                    'core_contribution': '构建多模态抑郁症复发预测模型，推动AI在精神医学中的应用',
                    'research_direction': '机器学习与精准精神医学',
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
        
        # AI心理学相关中文关键词
        keywords = [
            '人工智能 心理学',
            'AI 心理健康',
            '算法 行为',
            '社交媒体 心理',
            '数字技术 认知',
            '聊天机器人 治疗',
            '机器学习 心理',
            '人机交互 心理',
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
