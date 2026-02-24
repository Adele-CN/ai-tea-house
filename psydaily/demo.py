#!/usr/bin/env python3
"""
PsyDaily - 心理学每日推送系统
演示版（无需外部依赖）
"""

import random
from datetime import datetime

class MockCrawler:
    """模拟爬虫"""
    def fetch_all(self):
        return [
            {
                'title': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
                'abstract': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响。实验1采用N-back任务测量工作记忆，实验2使用爱荷华博弈任务评估决策...',
                'source': '心理学报',
                'published': '2024-01-15'
            },
            {
                'title': '社交媒体使用与青少年抑郁症状的纵向追踪研究',
                'abstract': '基于为期两年的追踪数据，本研究考察了社交媒体使用频率、使用方式与青少年抑郁症状发展轨迹的关系...',
                'source': '中国临床心理学杂志',
                'published': '2024-01-14'
            },
            {
                'title': '正念训练对焦虑症患者注意偏向的干预效果：元分析',
                'abstract': '本研究纳入47项RCT研究，采用元分析方法系统评估了正念训练对焦虑症患者注意偏向的干预效果...',
                'source': '心理科学进展',
                'published': '2024-01-13'
            }
        ]

class MockAnalyzer:
    """模拟分析器"""
    def analyze(self, article, user_profile=None):
        is_paid = user_profile.get('is_paid', False) if user_profile else False
        
        # 基础分析
        result = {
            'title': article['title'],
            'source': article['source'],
            'abstract': article['abstract'][:150] + '...',
            'basic_comment': f"这篇发表在《{article['source']}》的文章对心理学研究有重要参考价值。",
            'publish_date': article['published']
        }
        
        # 付费版深度分析
        if is_paid:
            user_areas = user_profile.get('research_areas', [])
            relevance = random.randint(70, 95)
            
            result.update({
                'relevance_score': relevance,
                'authority_score': 90 if article['source'] == '心理学报' else 85,
                'context_summary': '本文延续了该领域的经典研究范式，但在方法论上有所创新。',
                'personal_comment': f"这篇文章与你的研究方向{'、'.join(user_areas[:2])}匹配度较高，建议深度阅读。",
                'key_findings': [
                    '核心发现1：证实了主要假设，效应量中等偏上',
                    '核心发现2：发现了调节变量，丰富了理论模型'
                ]
            })
        
        return result

class MockPusher:
    """模拟推送器"""
    
    def format_free(self, analysis):
        return f"""
📚 PsyDaily 今日心理学

【{analysis['title']}】
📖 来源：《{analysis['source']}》
📅 日期：{analysis['publish_date']}

📝 摘要
{analysis['abstract']}

💬 简评
{analysis['basic_comment']}

---
✨ 升级付费版解锁：
• 与你研究方向的匹配度分析
• 文章权威性评分  
• 文献对话脉络梳理
• 个性化深度解读

💰 ¥29/月，每天不到1元
    """.strip()
    
    def format_paid(self, analysis):
        return f"""
🔥 PsyDaily Pro 深度分析

【{analysis['title']}】
📖 来源：《{analysis['source']}》
📅 日期：{analysis['publish_date']}

📊 匹配度评分：{analysis['relevance_score']}/100
{analysis['personal_comment']}

⭐ 权威性评分：{analysis['authority_score']}/100
期刊等级：{'顶级' if analysis['authority_score'] >= 90 else '权威'}

📝 摘要
{analysis['abstract']}

📚 文献对话
{analysis['context_summary']}

🔬 核心发现
• {analysis['key_findings'][0]}
• {analysis['key_findings'][1]}

---
💡 "认识你自己" —— 苏格拉底
    """.strip()
    
    def send(self, analysis, is_paid=False):
        message = self.format_paid(analysis) if is_paid else self.format_free(analysis)
        print("="*60)
        print("📤 推送消息：")
        print("="*60)
        print(message)
        print("="*60)
        return True

def main():
    print("""
╔══════════════════════════════════════════╗
║        PsyDaily 心理学每日推送           ║
║                                          ║
║  免费版：每日1篇基础推送                ║
║  付费版：¥29/月，深度分析+无限篇        ║
╚══════════════════════════════════════════╝
    """)
    
    crawler = MockCrawler()
    analyzer = MockAnalyzer()
    pusher = MockPusher()
    
    # 抓取
    print("📥 抓取最新文章...")
    articles = crawler.fetch_all()
    selected = random.choice(articles)
    
    # 免费版演示
    print("\n" + "="*60)
    print("👤 用户类型：免费版")
    print("="*60)
    free_user = {'research_areas': ['认知心理学'], 'is_paid': False}
    analysis_free = analyzer.analyze(selected, free_user)
    pusher.send(analysis_free, is_paid=False)
    
    # 付费版演示
    print("\n" + "="*60)
    print("👤 用户类型：付费版 Pro")
    print("="*60)
    paid_user = {'research_areas': ['认知心理学', '决策科学'], 'is_paid': True}
    analysis_paid = analyzer.analyze(selected, paid_user)
    pusher.send(analysis_paid, is_paid=True)
    
    print("\n✅ 演示完成！")

if __name__ == '__main__':
    main()
