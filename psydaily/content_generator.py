#!/usr/bin/env python3
"""
PsyDaily 内容生成器
每天运行一次，预生成内容存到服务器
不消耗实时Kimi额度
"""

import json
import random
import requests
import os
from datetime import datetime

# API Keys
KIMI_API_KEY = os.getenv('KIMI_API_KEY', '')
MINIMAX_API_KEY = "sk-cp-cM_UG-gSD08NXUr2H0XtSvn8IZjAj0ZUc5arOunWo4tzYvNWzKjYh-3WP12WGNOKWZ5yFgSRxboFpnREXaRx1ftk6UZyMZhKe7_kNKySbXq5cEOrE7wZsoY"
DEEPSEEK_API_KEY = "sk-df29b6ddc42541d28e550f2dfd25ff1c"

# 论文数据库
ARTICLES = [
    {
        'id': 1,
        'title_zh': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
        'title_en': 'Working Memory Capacity and Decision Quality: A Dual-Task Paradigm Study',
        'abstract_zh': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响。实验1采用N-back任务测量工作记忆，实验2使用爱荷华博弈任务评估决策，实验3通过双任务范式分离认知成分。结果表明，工作记忆容量与决策质量呈显著正相关（r=0.45, p<0.001），且在复杂决策情境中效应更强。这一发现为理解决策的认知机制提供了新视角，对改善决策训练方案具有实践意义。',
        'abstract_en': 'This study investigated the relationship between working memory capacity and decision quality through three experiments. Results showed significant positive correlation (r=0.45, p<0.001), with stronger effects in complex decision contexts.',
        'source_zh': '心理学报',
        'source_en': 'Acta Psychologica Sinica',
        'impact_factor': 8.5,
        'field': 'cognitive'
    },
    {
        'id': 2,
        'title_zh': '社交媒体使用与青少年心理健康：一项纵向队列研究',
        'title_en': 'Social Media Use and Adolescent Mental Health: A Longitudinal Cohort Study',
        'abstract_zh': '这项为期两年的纵向研究考察了2,000名青少年的社交媒体使用模式与心理健康结果的关系。研究发现，被动浏览与抑郁和焦虑症状增加相关，而主动参与则没有显著负面影响。这一发现强调了使用方式而非使用时长的关键作用，为数字时代的青少年心理健康干预提供了实证依据。',
        'abstract_en': 'This two-year longitudinal study examined 2,000 adolescents. Results showed passive scrolling was associated with increased depression and anxiety symptoms, while active engagement showed no significant negative effects.',
        'source_zh': '自然·人类行为',
        'source_en': 'Nature Human Behaviour',
        'impact_factor': 29.9,
        'field': 'clinical'
    },
    {
        'id': 3,
        'title_zh': '正念训练对焦虑症患者注意偏向的干预效果：元分析研究',
        'title_en': 'Effects of Mindfulness Training on Attention Bias in Anxiety Patients: Meta-Analysis',
        'abstract_zh': '本元分析纳入47项随机对照试验，共3,200名焦虑症患者。结果显示，正念训练能显著改善注意偏向（Hedges g = -0.62），且效果在治疗结束后3个月仍维持。亚组分析发现，8周以上的训练效果更显著。研究为正念干预在焦虑症治疗中的应用提供了高质量证据。',
        'abstract_en': 'This meta-analysis included 47 RCTs with 3,200 anxiety patients. Results showed mindfulness training significantly improved attention bias (Hedges g = -0.62), with effects maintained at 3-month follow-up.',
        'source_zh': '心理科学进展',
        'source_en': 'Advances in Psychological Science',
        'impact_factor': 7.2,
        'field': 'clinical'
    }
]


class ContentGenerator:
    """内容生成器 - 每天运行一次"""
    
    def __init__(self):
        self.data_dir = '/root/.openclaw/workspace/psydaily/data/content'
        os.makedirs(self.data_dir, exist_ok=True)
    
    def generate_daily_content(self):
        """生成每日内容"""
        print(f"🚀 生成 {datetime.now().strftime('%Y-%m-%d')} 的 PsyDaily 内容...")
        
        daily_contents = []
        
        for article in ARTICLES:
            print(f"\n📄 处理: {article['title_zh'][:30]}...")
            
            # 生成AI分析
            content = self._generate_article_content(article)
            daily_contents.append(content)
        
        # 保存到文件
        self._save_content(daily_contents)
        
        print(f"\n✅ 已生成 {len(daily_contents)} 篇文章的内容")
        print(f"💾 保存位置: {self.data_dir}/daily_{datetime.now().strftime('%Y%m%d')}.json")
        
        return daily_contents
    
    def _generate_article_content(self, article):
        """为单篇文章生成完整内容"""
        
        # 构建Prompt
        prompt = f"""你是一位专业的心理学科普作家。请为这篇论文生成内容分析：

标题：{article['title_zh']}
摘要：{article['abstract_zh']}
来源：{article['source_zh']}（影响因子：{article['impact_factor']}）

请严格按照以下格式输出：

【1. 一句话核心发现】
用一句话概括这篇论文最重要的发现，要吸引人（50字以内）

【2. 为什么值得关注】
解释为什么心理学研究者/爱好者应该关注这项研究，有什么实际价值（80字以内）

【3. 核心发现详解】
详细解读3个核心发现，每个30-50字

【4. 方法学亮点】
这项研究在方法上有什么创新或值得学习的地方（50字以内）

【5. 对你研究的启发】
对读者的研究或生活有什么具体启发（50字以内）

注意：用中文输出，语言简洁专业。"""
        
        # 调用AI生成（优先DeepSeek，便宜）
        result = self._call_deepseek(prompt)
        
        if not result['success']:
            # DeepSeek失败，用MiniMax
            result = self._call_minimax(prompt)
        
        # 解析结果
        analysis = self._parse_analysis(result.get('content', ''))
        
        return {
            'article': article,
            'analysis': analysis,
            'generated_at': datetime.now().isoformat(),
            'model_used': result.get('model', 'default')
        }
    
    def _call_deepseek(self, prompt):
        """调用DeepSeek API"""
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是专业的心理学科普作家。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                choices = result.get('choices', [])
                if choices:
                    content = choices[0].get('message', {}).get('content', '')
                    return {'success': True, 'content': content, 'model': 'deepseek'}
            
            return {'success': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _call_minimax(self, prompt):
        """调用MiniMax API"""
        try:
            url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {MINIMAX_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "abab6.5-chat",
                "messages": [
                    {"role": "system", "content": "你是专业的心理学科普作家。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                choices = result.get('choices', [])
                if choices:
                    content = choices[0].get('message', {}).get('content', '')
                    return {'success': True, 'content': content, 'model': 'minimax'}
            
            return {'success': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _parse_analysis(self, content):
        """解析AI返回的内容"""
        sections = {}
        
        # 简单解析（按标题分割）
        import re
        
        patterns = [
            ("core_finding", r"【?1\.\s*一句话核心发现】?(.*?)【?2"),
            ("why_matters", r"【?2\.\s*为什么值得关注】?(.*?)【?3"),
            ("detailed_findings", r"【?3\.\s*核心发现详解】?(.*?)【?4"),
            ("methodology", r"【?4\.\s*方法学亮点】?(.*?)【?5"),
            ("inspiration", r"【?5\.\s*对你研究的启发】?(.*?)$"),
        ]
        
        for key, pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                sections[key] = match.group(1).strip()
            else:
                sections[key] = "内容生成中..."
        
        return sections
    
    def _save_content(self, contents):
        """保存内容到文件"""
        filename = f"{self.data_dir}/daily_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(contents, f, ensure_ascii=False, indent=2)
    
    def get_today_content(self, article_id=None):
        """获取今天的内容（供Bot调用）"""
        filename = f"{self.data_dir}/daily_{datetime.now().strftime('%Y%m%d')}.json"
        
        # 如果今天的文件不存在，生成一次
        if not os.path.exists(filename):
            print("⚠️ 今天的内容未生成，正在生成...")
            self.generate_daily_content()
        
        with open(filename, 'r', encoding='utf-8') as f:
            contents = json.load(f)
        
        if article_id:
            for content in contents:
                if content['article']['id'] == article_id:
                    return content
        
        # 默认返回第一篇
        return contents[0] if contents else None


if __name__ == '__main__':
    generator = ContentGenerator()
    generator.generate_daily_content()
