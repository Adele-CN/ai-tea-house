import json
from datetime import datetime

class ArticleAnalyzer:
    """AI文章分析器"""
    
    def __init__(self):
        # 模拟API调用（后续替换为真实API）
        pass
    
    def analyze(self, article, user_profile=None):
        """分析单篇文章"""
        
        # 基础分析（免费版）
        basic_analysis = self._basic_analysis(article)
        
        # 深度分析（付费版）
        if user_profile and user_profile.get('is_paid', False):
            deep_analysis = self._deep_analysis(article, user_profile)
            return {**basic_analysis, **deep_analysis}
        
        return basic_analysis
    
    def _basic_analysis(self, article):
        """基础分析 - 免费版"""
        return {
            'title': article['title'],
            'source': article['source'],
            'abstract': article['abstract'][:200] + '...' if len(article['abstract']) > 200 else article['abstract'],
            'basic_comment': self._generate_basic_comment(article),
            'publish_date': article['published']
        }
    
    def _deep_analysis(self, article, user_profile):
        """深度分析 - 付费版"""
        return {
            'relevance_score': self._calculate_relevance(article, user_profile),
            'authority_score': self._evaluate_authority(article),
            'context_summary': self._summarize_context(article),
            'personal_comment': self._generate_personal_comment(article, user_profile),
            'key_findings': self._extract_findings(article),
            'methodology': self._analyze_method(article)
        }
    
    def _generate_basic_comment(self, article):
        """生成基础评论"""
        # 简化版：后续接入AI API
        title = article['title']
        source = article['source']
        
        templates = [
            f"这篇发表在《{source}》的文章探讨了{title[:20]}...，值得关注。",
            f"《{source}》最新研究：{title[:20]}...，对该领域有重要启发。",
            f"来自《{source}》的前沿研究，涉及{title[:20]}...，推荐阅读。"
        ]
        
        # 简单轮询选择
        import hashlib
        idx = int(hashlib.md5(title.encode()).hexdigest(), 16) % len(templates)
        return templates[idx]
    
    def _calculate_relevance(self, article, user_profile):
        """计算与用户研究方向的匹配度"""
        # 模拟计算
        user_areas = user_profile.get('research_areas', [])
        title = article['title']
        
        # 简单关键词匹配（后续用embedding）
        score = 50  # 基础分
        for area in user_areas:
            if area in title:
                score += 20
        
        return min(score, 95)  # 最高95分
    
    def _evaluate_authority(self, article):
        """评价文章权威性"""
        source = article['source']
        
        # 期刊权重（模拟）
        journal_weights = {
            '心理学报': 90,
            '心理科学进展': 85,
            '中国临床心理学杂志': 80
        }
        
        return journal_weights.get(source, 70)
    
    def _summarize_context(self, article):
        """总结文献对话脉络"""
        # 模拟：后续用AI生成
        return "本文延续了该领域的经典研究，但在方法论上有所创新。与既往研究相比，作者采用了更严谨的实验设计。"
    
    def _generate_personal_comment(self, article, user_profile):
        """生成个性化评论"""
        user_areas = user_profile.get('research_areas', [])
        relevance = self._calculate_relevance(article, user_profile)
        
        if relevance > 80:
            return f"这篇文章与你的研究方向{'、'.join(user_areas[:2])}高度相关，特别是其实验设计值得参考。"
        elif relevance > 60:
            return f"文章涉及{user_areas[0] if user_areas else '心理学'}相关主题，有一定参考价值。"
        else:
            return "这篇文章拓展了研究视野，建议浏览了解领域前沿动态。"
    
    def _extract_findings(self, article):
        """提取核心发现"""
        # 模拟
        return ["核心发现1：待AI提取", "核心发现2：待AI提取"]
    
    def _analyze_method(self, article):
        """分析方法学"""
        # 模拟
        return {
            'study_type': '实验研究/问卷调查（待识别）',
            'sample_size': '待提取',
            'key_method': '待分析'
        }


if __name__ == '__main__':
    # 测试分析器
    analyzer = ArticleAnalyzer()
    
    test_article = {
        'title': '工作记忆容量与决策质量的关系研究',
        'abstract': '本研究探讨了工作记忆容量对决策质量的影响...',
        'source': '心理学报',
        'published': '2024-01-15'
    }
    
    test_user = {
        'research_areas': ['认知心理学', '决策'],
        'is_paid': False
    }
    
    result = analyzer.analyze(test_article, test_user)
    print(json.dumps(result, ensure_ascii=False, indent=2))
