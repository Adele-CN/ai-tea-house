#!/usr/bin/env python3
"""
PsyDaily Telegram Bot - 简化稳定版
"""

import logging
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 启用日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token
BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"

# 用户数据库（内存版，后续换成真实数据库）
users = {}

# 模拟文章数据
ARTICLES = [
    {
        'title': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
        'abstract': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响。实验1采用N-back任务测量工作记忆，实验2使用爱荷华博弈任务评估决策。结果表明，工作记忆容量与决策质量呈显著正相关（r=0.45, p<0.001）。',
        'source': '心理学报',
        'language': 'zh',
        'impact_factor': 8.5
    },
    {
        'title': 'Social media use and adolescent mental health: A longitudinal cohort study',
        'abstract': 'This 2-year longitudinal study examined the relationship between social media use patterns and mental health outcomes in 2,000 adolescents. Results showed that passive scrolling was associated with increased depression and anxiety symptoms.',
        'source': 'Nature Human Behaviour',
        'language': 'en',
        'impact_factor': 29.9
    },
    {
        'title': '正念训练对焦虑症患者注意偏向的干预效果：元分析研究',
        'abstract': '本元分析纳入47项随机对照试验，共3,200名焦虑症患者。结果显示，正念训练能显著改善注意偏向（Hedges g = -0.62），且效果在治疗结束后3个月仍维持。',
        'source': '心理科学进展',
        'language': 'zh',
        'impact_factor': 7.2
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    user = update.effective_user
    user_id = user.id
    
    # 注册用户
    if user_id not in users:
        users[user_id] = {
            'name': user.first_name,
            'joined': datetime.now().isoformat(),
            'is_paid': False
        }
    
    welcome = f"""
🧠 **欢迎加入 PsyDaily 心理学日报！**

你好，{user.first_name}！

我是你的AI心理学助手，每天为你精选一篇心理学前沿研究。

📋 **命令列表：**
/start - 查看欢迎信息
/today - 获取今日推荐
/upgrade - 升级Pro版

💎 **版本对比：**
🆓 免费版：每日1篇基础推送
💎 Pro版：¥29/月，无限+深度分析

点击 /today 获取今天的推荐！
    """
    
    await update.message.reply_text(welcome, parse_mode='Markdown')
    logger.info(f"新用户启动: {user.first_name} (ID: {user_id})")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """今日推荐"""
    user = update.effective_user
    user_id = user.id
    
    # 选择随机文章
    article = random.choice(ARTICLES)
    
    # 格式化消息
    lang_emoji = '🇨🇳' if article['language'] == 'zh' else '🇬🇧'
    
    message = f"""
{lang_emoji} **PsyDaily 今日心理学**

**{article['title']}**
📖 {article['source']} (IF: {article['impact_factor']})

📝 **摘要**
{article['abstract'][:200]}...

💬 **简评**
这篇文章来自{'顶级' if article['impact_factor'] >= 20 else '权威' if article['impact_factor'] >= 10 else '核心'}期刊《{article['source']}》，值得关注。

---
✨ **升级Pro版解锁深度分析**
💰 ¥29/月，每天不到1元
    """.strip()
    
    # 添加升级按钮
    keyboard = [[InlineKeyboardButton("💎 升级Pro版", callback_data='upgrade')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    logger.info(f"用户 {user_id} 获取今日推荐")

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """升级Pro版"""
    message = """
💎 **PsyDaily Pro 会员**

**¥29/月**，解锁全部功能：

✅ 无限篇数阅读
✅ 智能匹配度分析
✅ 文献权威性评分
✅ 研究脉络梳理
✅ 个性化深度解读

🎁 **限时优惠**：首月仅需¥19！

**开通方式：**
添加微信：PsyDaily_Admin
发送"升级+你的用户名"
    """
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'upgrade':
        await upgrade(update, context)

def main():
    """主函数"""
    print("🚀 启动 PsyDaily Bot...")
    
    # 创建应用
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("upgrade", upgrade))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Bot已启动！")
    print("📝 命令: /start /today /upgrade")
    print("-" * 50)
    
    # 运行（使用轮询）
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
