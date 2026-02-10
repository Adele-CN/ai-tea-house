#!/usr/bin/env python3
"""
PsyDaily v0.2 - 中英文混合版
加速开发版本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import random
from datetime import datetime

# 模拟数据 - 中英文混合
MOCK_ARTICLES = [
    {
        'title': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
        'abstract': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响。实验1采用N-back任务测量工作记忆，实验2使用爱荷华博弈任务评估决策。结果表明，工作记忆容量与决策质量呈显著正相关（r=0.45, p<0.001），且在复杂决策情境中效应更强。本研究为理解决策的认知机制提供了新视角。',
        'source': '心理学报',
        'language': 'zh',
        'field': 'cognitive',
        'impact_factor': 8.5,
        'published': '2024-02-01'
    },
    {
        'title': 'Social media use and adolescent mental health: A longitudinal cohort study',
        'abstract': 'This 2-year longitudinal study examined the relationship between social media use patterns and mental health outcomes in 2,000 adolescents. Results showed that passive scrolling was associated with increased depression and anxiety symptoms, while active engagement showed no significant negative effects. The findings highlight the importance of usage patterns over duration.',
        'source': 'Nature Human Behaviour',
        'language': 'en',
        'field': 'clinical',
        'impact_factor': 29.9,
        'published': '2024-01-28'
    },
    {
        'title': '正念训练对焦虑症患者注意偏向的干预效果：元分析研究',
        'abstract': '本元分析纳入47项随机对照试验，共3,200名焦虑症患者。结果显示，正念训练能显著改善注意偏向（Hedges g = -0.62, 95% CI: -0.81 to -0.43），且效果在治疗结束后3个月仍维持。亚组分析发现，8周以上的训练效果更显著。',
        'source': '心理科学进展',
        'language': 'zh',
        'field': 'clinical',
        'impact_factor': 7.2,
        'published': '2024-01-20'
    },
    {
        'title': 'The neurobiology of resilience: Implications for prevention and treatment',
        'abstract': 'This review synthesizes recent advances in understanding the neural mechanisms underlying psychological resilience. We discuss how adaptive stress responses, neuroplasticity, and genetic factors interact to promote resilience. Clinical implications for developing resilience-focused interventions are explored.',
        'source': 'Psychological Bulletin',
        'language': 'en',
        'field': 'neuroscience',
        'impact_factor': 22.4,
        'published': '2024-01-15'
    },
    {
        'title': '跨文化视角下的自我构念与心理健康：集体主义vs个人主义',
        'abstract': '本研究比较了集体主义文化（中国、日本）和个人主义文化（美国、德国）背景下自我构念与心理健康的关系。研究发现，独立型自我构念在个人主义文化中与更高幸福感相关，而互依型自我构念在集体主义文化中更有益。文化匹配假说得到支持。',
        'source': 'Journal of Personality and Social Psychology',
        'language': 'zh',
        'field': 'social',
        'impact_factor': 6.3,
        'published': '2024-01-10'
    }
]


class PsyDailyV2:
    """PsyDaily v0.2 - 中英文混合版"""
    
    def __init__(self):
        self.articles = MOCK_ARTICLES
    
    def select_article(self, user_profile=None):
        """智能选择文章（后续用算法优化）"""
        if user_profile and user_profile.get('research_areas'):
            # 简单匹配
            areas = user_profile['research_areas']
            matching = [a for a in self.articles if any(area in a['field'] for area in areas)]
            if matching:
                return random.choice(matching)
        return random.choice(self.articles)
    
    def analyze(self, article, user_profile=None):
        """分析文章"""
        is_paid = user_profile.get('is_paid', False) if user_profile else False
        user_areas = user_profile.get('research_areas', []) if user_profile else []
        
        # 计算匹配度
        relevance = self._calc_relevance(article, user_areas)
        
        result = {
            'title': article['title'],
            'source': article['source'],
            'language': article['language'],
            'field': article['field'],
            'abstract': article['abstract'][:200] + '...' if len(article['abstract']) > 200 else article['abstract'],
            'publish_date': article['published'],
            'impact_factor': article['impact_factor'],
            'relevance_score': relevance,
        }
        
        if is_paid:
            result.update(self._deep_analysis(article, user_profile, relevance))
        
        return result
    
    def _calc_relevance(self, article, user_areas):
        """计算匹配度"""
        base = 50
        if not user_areas:
            return base
        
        # 领域匹配
        field_map = {
            'cognitive': ['认知心理学', 'cognitive', 'memory', 'decision'],
            'clinical': ['临床心理学', 'clinical', 'anxiety', 'depression', 'mental health'],
            'social': ['社会心理学', 'social', 'culture', 'relationship'],
            'neuroscience': ['神经科学', 'neuroscience', 'brain', 'neural']
        }
        
        article_keywords = field_map.get(article['field'], [])
        for area in user_areas:
            if any(kw in area.lower() or area.lower() in kw for kw in article_keywords):
                base += 25
        
        return min(base, 98)
    
    def _deep_analysis(self, article, user_profile, relevance):
        """深度分析"""
        user_areas = user_profile.get('research_areas', [])
        
        # 权威性评价
        if_score = article['impact_factor']
        if if_score >= 20:
            authority = 95
            level = '顶级期刊'
        elif if_score >= 10:
            authority = 88
            level = '权威期刊'
        elif if_score >= 5:
            authority = 80
            level = '核心期刊'
        else:
            authority = 72
            level = '优质期刊'
        
        # 个性化评论
        if relevance > 80:
            comment = f"🔥 高度相关！这篇文章与你的研究方向{'、'.join(user_areas[:2])}高度匹配，建议优先阅读。"
        elif relevance > 60:
            comment = f"⭐ 中度相关。文章涉及{user_areas[0] if user_areas else '心理学'}相关主题，有参考价值。"
        else:
            comment = "📖 拓展视野。这篇文章可以帮助你了解相邻领域的最新进展。"
        
        return {
            'authority_score': authority,
            'journal_level': level,
            'personal_comment': comment,
            'key_findings': self._extract_findings(article),
            'context_summary': self._gen_context(article),
            'methodology': '实验研究/元分析（待详细提取）'
        }
    
    def _extract_findings(self, article):
        """提取核心发现"""
        # 模拟提取
        abstracts = {
            'cognitive': [
                '工作记忆容量与决策质量呈显著正相关（r=0.45）',
                '复杂决策情境中效应更强'
            ],
            'clinical': [
                '正念训练显著改善注意偏向（g = -0.62）',
                '8周以上训练效果更持久'
            ],
            'social': [
                '独立型自我在个人主义文化中更有益',
                '文化匹配假说得到支持'
            ],
            'neuroscience': [
                '神经可塑性是心理韧性的关键机制',
                '遗传与环境因素交互作用'
            ]
        }
        return abstracts.get(article['field'], ['核心发现1：待详细提取', '核心发现2：待详细提取'])
    
    def _gen_context(self, article):
        """生成文献对话"""
        contexts = {
            'cognitive': '本文延续了工作记忆与决策关系的经典研究，采用双任务范式创新性地分离了不同认知成分。',
            'clinical': '本文整合了正念干预的实证研究，为该领域的循证实践提供了重要参考。',
            'social': '本文跨文化研究设计回应了心理学本土化的呼吁，对文化心理学理论有重要贡献。',
            'neuroscience': '本文整合了神经科学和心理学的视角，为心理韧性的机制研究提供了新框架。'
        }
        return contexts.get(article['field'], '本文在领域内具有重要参考价值。')
    
    def format_push(self, analysis, is_paid=False):
        """格式化推送"""
        lang_emoji = '🇨🇳' if analysis['language'] == 'zh' else '🇬🇧'
        
        if not is_paid:
            return f"""
{lang_emoji} 📚 PsyDaily 今日心理学

【{analysis['title']}】
📖 {analysis['source']} (IF: {analysis['impact_factor']})
📅 {analysis['publish_date']}

📝 摘要
{analysis['abstract']}

💬 简评
这篇文章来自{'顶级' if analysis['impact_factor'] >= 20 else '权威' if analysis['impact_factor'] >= 10 else '核心'}期刊《{analysis['source']}》，值得关注。

---
✨ 付费版解锁：
• 与你研究方向的匹配度分析 📊
• 文献对话脉络梳理 📚  
• 核心发现提取 🔬
• 个性化深度解读 💡

💎 PsyDaily Pro ¥29/月
回复 "升级" 了解更多
            """.strip()
        else:
            relevance_emoji = '🔥' if analysis['relevance_score'] > 80 else '⭐' if analysis['relevance_score'] > 60 else '📖'
            return f"""
{relevance_emoji} {lang_emoji} PsyDaily Pro 深度分析

【{analysis['title']}】
📖 {analysis['source']} (IF: {analysis['impact_factor']}) | {analysis['journal_level']}
📅 {analysis['publish_date']}

📊 匹配度评分：{analysis['relevance_score']}/100
{analysis['personal_comment']}

⭐ 权威性评分：{analysis['authority_score']}/100
期刊等级：{analysis['journal_level']}
影响因子：{analysis['impact_factor']}

📝 摘要
{analysis['abstract']}

📚 文献对话
{analysis['context_summary']}

🔬 核心发现
{chr(10).join(['• ' + f for f in analysis['key_findings']])}

🔍 方法学
{analysis['methodology']}

---
💡 今日心理学名言
"认识你自己" —— 苏格拉底
            """.strip()
    
    def run(self, user_profile=None):
        """运行每日推送"""
        print(f"\n🚀 PsyDaily v0.2 启动")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 选择文章
        article = self.select_article(user_profile)
        print(f"📄 选中: {article['title'][:40]}...")
        
        # 分析
        is_paid = user_profile.get('is_paid', False) if user_profile else False
        analysis = self.analyze(article, user_profile)
        
        # 格式化推送
        message = self.format_push(analysis, is_paid)
        
        print("\n📤 推送内容：")
        print("="*60)
        print(message)
        print("="*60)
        
        return message


def demo():
    """演示"""
    app = PsyDailyV2()
    
    print("""
╔══════════════════════════════════════════════════════════╗
║              PsyDaily v0.2 - 中英文混合版               ║
║                                                          ║
║  🆓 免费版：每日1篇基础推送                             ║
║  💎 付费版：¥29/月，无限篇+深度分析                     ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 免费用户
    print("\n" + "👤 用户案例：心理学研究生（免费版）")
    print("   研究方向：认知心理学、决策")
    free_user = {
        'research_areas': ['认知心理学', 'decision'],
        'is_paid': False
    }
    app.run(free_user)
    
    print("\n\n")
    
    # 付费用户
    print("👤 用户案例：博士生（付费版 Pro）")
    print("   研究方向：临床心理学、正念")
    paid_user = {
        'research_areas': ['临床心理学', 'mindfulness'],
        'is_paid': True
    }
    app.run(paid_user)
    
    print("\n✅ 演示完成！")


if __name__ == '__main__':
    demo()
