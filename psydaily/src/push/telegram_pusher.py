import json
from datetime import datetime

class TelegramPusher:
    """Telegram推送模块"""
    
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    def format_free_push(self, analysis):
        """格式化免费版推送"""
        return f"""
📚 **PsyDaily 今日心理学**

**{analysis['title']}**
📖 来源：《{analysis['source']}》
📅 日期：{analysis['publish_date'][:10] if analysis['publish_date'] else '最新'}

📝 **摘要**
{analysis['abstract']}

💬 **简评**
{analysis['basic_comment']}

---
✨ **升级付费版解锁：**
• 与你研究方向的匹配度分析
• 文章权威性评分
• 文献对话脉络梳理  
• 个性化深度解读

💰 ¥29/月，每天不到1元
回复 "升级" 了解详情
        """.strip()
    
    def format_paid_push(self, analysis):
        """格式化付费版推送"""
        relevance = analysis.get('relevance_score', 0)
        authority = analysis.get('authority_score', 0)
        
        # 匹配度表情
        relevance_emoji = '🔥' if relevance > 80 else '⭐' if relevance > 60 else '📖'
        
        return f"""
{relevance_emoji} **PsyDaily Pro 深度分析**

**{analysis['title']}**
📖 来源：《{analysis['source']}》
📅 日期：{analysis['publish_date'][:10] if analysis['publish_date'] else '最新'}

📊 **匹配度评分：{relevance}/100**
{analysis.get('personal_comment', '')}

⭐ **权威性评分：{authority}/100**
期刊等级：{'顶级' if authority >= 90 else '权威' if authority >= 80 else '核心'}

📝 **摘要**
{analysis['abstract']}

📚 **文献对话**
{analysis.get('context_summary', '')}

🔬 **核心发现**
{chr(10).join(['• ' + f for f in analysis.get('key_findings', [])])}

---
💡 **今日寄语**
{self._daily_quote()}
        """.strip()
    
    def _daily_quote(self):
        """每日心理学名言"""
        quotes = [
            ""认识你自己" —— 苏格拉底",
            "心理学是研究行为的科学，而不仅仅是研究心智的科学。" —— 斯金纳",
            "我们不能改变风的方向，但可以调整帆的角度。" —— 积极心理学",
            "每个人的内心都是一个宇宙。" —— 荣格"
        ]
        import random
        return random.choice(quotes)
    
    def send_push(self, analysis, is_paid=False):
        """发送推送（模拟，后续接入真实API）"""
        if is_paid:
            message = self.format_paid_push(analysis)
        else:
            message = self.format_free_push(analysis)
        
        # 模拟发送
        print("=" * 50)
        print("📤 推送消息：")
        print("=" * 50)
        print(message)
        print("=" * 50)
        return True


if __name__ == '__main__':
    # 测试推送
    pusher = TelegramPusher()
    
    test_analysis_free = {
        'title': '工作记忆容量与决策质量的关系研究',
        'source': '心理学报',
        'abstract': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响，发现高工作记忆容量个体在复杂决策任务中表现更优...',
        'basic_comment': '这篇文章探讨了工作记忆与决策的关系，值得关注。',
        'publish_date': '2024-01-15T00:00:00Z'
    }
    
    test_analysis_paid = {
        **test_analysis_free,
        'relevance_score': 85,
        'authority_score': 90,
        'context_summary': '本文延续了Baddeley的工作记忆模型，但创新性地引入了决策科学视角。',
        'personal_comment': '这篇文章与你的研究方向"认知心理学"高度相关，其实验设计值得参考。',
        'key_findings': ['工作记忆容量与决策质量呈正相关', '复杂任务中效应更显著']
    }
    
    print("\n" + "🆓 免费版推送：" + "\n")
    pusher.send_push(test_analysis_free, is_paid=False)
    
    print("\n" + "💎 付费版推送：" + "\n")
    pusher.send_push(test_analysis_paid, is_paid=True)
