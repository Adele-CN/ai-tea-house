#!/usr/bin/env python3
"""
PsyDaily - 心理学每日推送系统
主程序
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawler.journal_crawler import JournalCrawler
from analyzer.article_analyzer import ArticleAnalyzer
from push.telegram_pusher import TelegramPusher
from datetime import datetime
import random

class PsyDaily:
    """PsyDaily主类"""
    
    def __init__(self):
        self.crawler = JournalCrawler()
        self.analyzer = ArticleAnalyzer()
        self.pusher = TelegramPusher()
    
    def run_daily(self, user_profile=None):
        """运行每日推送"""
        print("🚀 PsyDaily 启动...")
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # 1. 抓取文章
        print("\n📥 正在抓取最新文章...")
        articles = self.crawler.fetch_all()
        
        if not articles:
            print("❌ 未获取到文章，今日推送取消")
            return False
        
        # 2. 选择今日推荐（简单随机，后续用算法）
        selected = random.choice(articles)
        print(f"\n📄 选中文章: {selected['title'][:30]}...")
        
        # 3. 分析文章
        print("🔍 正在分析...")
        analysis = self.analyzer.analyze(selected, user_profile)
        
        # 4. 推送
        is_paid = user_profile.get('is_paid', False) if user_profile else False
        print(f"\n📤 发送{'付费版' if is_paid else '免费版'}推送...")
        self.pusher.send_push(analysis, is_paid=is_paid)
        
        print("\n✅ 今日推送完成！")
        return True


def demo():
    """演示模式"""
    print("""
╔══════════════════════════════════════════╗
║        PsyDaily 心理学每日推送           ║
║                                          ║
║  免费版：每日1篇基础推送                ║
║  付费版：¥29/月，深度分析+无限篇        ║
╚══════════════════════════════════════════╝
    """)
    
    psydaily = PsyDaily()
    
    # 模拟免费用户
    print("\n" + "="*50)
    print("👤 模拟用户：免费版")
    print("="*50)
    free_user = {
        'research_areas': ['认知心理学', '决策'],
        'is_paid': False
    }
    psydaily.run_daily(free_user)
    
    # 模拟付费用户
    print("\n" + "="*50)
    print("👤 模拟用户：付费版")
    print("="*50)
    paid_user = {
        'research_areas': ['认知心理学', '决策'],
        'is_paid': True
    }
    psydaily.run_daily(paid_user)


if __name__ == '__main__':
    demo()
