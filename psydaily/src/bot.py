#!/usr/bin/env python3
"""
PsyDaily Telegram Bot
每日心理学推送机器人
"""

import json
import random
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, JobQueue

# Bot配置
BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"

# 模拟数据库（后续替换为真实数据库）
users_db = {}

# 模拟文章数据
MOCK_ARTICLES = [
    {
        'title': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
        'abstract': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响...',
        'source': '心理学报',
        'language': 'zh',
        'field': 'cognitive',
        'impact_factor': 8.5,
        'published': '2024-02-01'
    },
    {
        'title': 'Social media use and adolescent mental health: A longitudinal cohort study',
        'abstract': 'This 2-year longitudinal study examined the relationship between social media use and mental health...',
        'source': 'Nature Human Behaviour',
        'language': 'en',
        'field': 'clinical',
        'impact_factor': 29.9,
        'published': '2024-01-28'
    },
    {
        'title': '正念训练对焦虑症患者注意偏向的干预效果：元分析研究',
        'abstract': '本元分析纳入47项随机对照试验，共3,200名焦虑症患者...',
        'source': '心理科学进展',
        'language': 'zh',
        'field': 'clinical',
        'impact_factor': 7.2,
        'published': '2024-01-20'
    }
]

# ============== 命令处理器 ==============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    user = update.effective_user
    user_id = user.id
    
    # 注册用户
    if user_id not in users_db:
        users_db[user_id] = {
            'id': user_id,
            'name': user.first_name,
            'joined_at': datetime.now().isoformat(),
            'is_paid': False,
            'research_areas': [],
            'daily_push': True
        }
    
    welcome_text = f"""
🧠 **欢迎加入 PsyDaily 心理学日报！**

你好，{user.first_name}！

我是你的AI心理学助手，每天为你精选一篇心理学前沿研究。

**📋 你可以：**
/start - 查看欢迎信息
/subscribe - 设置研究方向
/today - 获取今日推荐
/upgrade - 升级Pro版
/help - 查看帮助

**💎 版本对比：**
🆓 免费版：每日1篇基础推送
💎 Pro版：¥29/月，无限+深度分析

点击 /today 获取今天的推荐！
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """今日推荐"""
    user = update.effective_user
    user_id = user.id
    
    # 获取用户数据
    user_data = users_db.get(user_id, {})
    is_paid = user_data.get('is_paid', False)
    
    # 选择文章
    article = random.choice(MOCK_ARTICLES)
    
    # 生成推送内容
    if is_paid:
        message = format_paid_push(article, user_data)
    else:
        message = format_free_push(article)
    
    # 添加升级按钮（免费版）
    if not is_paid:
        keyboard = [[InlineKeyboardButton("💎 升级Pro版解锁深度分析", callback_data='upgrade')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update.message.reply_text(message, parse_mode='Markdown')

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """设置研究方向"""
    keyboard = [
        [InlineKeyboardButton("🧠 认知心理学", callback_data='field_cognitive')],
        [InlineKeyboardButton("🏥 临床心理学", callback_data='field_clinical')],
        [InlineKeyboardButton("👥 社会心理学", callback_data='field_social')],
        [InlineKeyboardButton("🧬 神经科学", callback_data='field_neuro')],
        [InlineKeyboardButton("✅ 完成设置", callback_data='field_done')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "请选择你的研究方向（可多选）：",
        reply_markup=reply_markup
    )

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
✅ 优先客服支持

**支付方式：**
请添加微信：PsyDaily_Admin
发送"升级+你的Telegram用户名"，客服会为你开通

🎁 **限时优惠**：首月仅需¥19！
    """
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """帮助"""
    help_text = """
📖 **PsyDaily 使用指南**

**基础命令：**
/start - 启动机器人
/today - 获取今日推荐
/subscribe - 设置研究方向
/upgrade - 升级Pro版
/help - 查看帮助

**如何获得最佳体验：**
1. 使用 /subscribe 设置你的研究方向
2. 每天查看 /today 获取推荐
3. 升级为Pro版解锁深度分析

**联系我们：**
邮箱：psydaily@example.com
微信：PsyDaily_Admin
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

# ============== 回调处理器 ==============

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """按钮回调"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith('field_'):
        # 处理研究方向选择
        field_map = {
            'field_cognitive': '认知心理学',
            'field_clinical': '临床心理学',
            'field_social': '社会心理学',
            'field_neuro': '神经科学'
        }
        
        if data == 'field_done':
            await query.edit_message_text("✅ 设置完成！使用 /today 获取个性化推荐。")
        else:
            field = field_map.get(data, '心理学')
            if user_id not in users_db:
                users_db[user_id] = {'research_areas': []}
            if 'research_areas' not in users_db[user_id]:
                users_db[user_id]['research_areas'] = []
            
            if field not in users_db[user_id]['research_areas']:
                users_db[user_id]['research_areas'].append(field)
                await query.edit_message_text(f"✅ 已添加：{field}\n\n继续选择或点击完成。", reply_markup=query.message.reply_markup)
    
    elif data == 'upgrade':
        await upgrade(update, context)

# ============== 推送格式化 ==============

def format_free_push(article):
    """格式化免费版推送"""
    lang_emoji = '🇨🇳' if article['language'] == 'zh' else '🇬🇧'
    
    return f"""
{lang_emoji} **PsyDaily 今日心理学**

**{article['title']}**
📖 {article['source']} (IF: {article['impact_factor']})
📅 {article['published']}

📝 **摘要**
{article['abstract'][:150]}...

💬 **简评**
这篇文章来自{'顶级' if article['impact_factor'] >= 20 else '权威' if article['impact_factor'] >= 10 else '核心'}期刊《{article['source']}》，值得关注。

---
✨ **升级Pro版解锁：**
• 与你研究方向的匹配度分析 📊
• 文献对话脉络梳理 📚  
• 核心发现提取 🔬
• 个性化深度解读 💡

💎 **PsyDaily Pro ¥29/月**
点击上方按钮了解更多
    """.strip()

def format_paid_push(article, user_data):
    """格式化付费版推送"""
    lang_emoji = '🇨🇳' if article['language'] == 'zh' else '🇬🇧'
    relevance = random.randint(70, 95)
    
    return f"""
🔥 {lang_emoji} **PsyDaily Pro 深度分析**

**{article['title']}**
📖 {article['source']} (IF: {article['impact_factor']})
📅 {article['published']}

📊 **匹配度评分：{relevance}/100**
这篇文章与你的研究方向高度相关，建议优先阅读。

⭐ **权威性评分：{article['impact_factor']}/100**
期刊等级：{'顶级' if article['impact_factor'] >= 20 else '权威' if article['impact_factor'] >= 10 else '核心'}

📝 **摘要**
{article['abstract']}

📚 **文献对话**
本文延续了该领域的经典研究范式，但在方法论上有所创新，对理解{article['field']}有重要贡献。

🔬 **核心发现**
• 核心发现1：证实了主要假设，效应量中等偏上
• 核心发现2：发现了调节变量，丰富了理论模型

---
💡 "认识你自己" —— 苏格拉底
    """.strip()

# ============== 定时任务 ==============

async def daily_push_job(context: ContextTypes.DEFAULT_TYPE):
    """每日推送任务"""
    print(f"⏰ 执行每日推送: {datetime.now()}")
    
    for user_id, user_data in users_db.items():
        if not user_data.get('daily_push', True):
            continue
        
        try:
            # 选择文章
            article = random.choice(MOCK_ARTICLES)
            is_paid = user_data.get('is_paid', False)
            
            # 生成推送
            if is_paid:
                message = format_paid_push(article, user_data)
            else:
                message = format_free_push(article)
            
            # 发送
            await context.bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
            print(f"  ✓ 已推送给用户 {user_id}")
            
        except Exception as e:
            print(f"  ✗ 推送给用户 {user_id} 失败: {e}")

# ============== 主程序 ==============

async def main():
    """主函数"""
    print("🚀 启动 PsyDaily Telegram Bot...")
    
    # 创建应用
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加命令处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("upgrade", upgrade))
    application.add_handler(CommandHandler("help", help_command))
    
    # 添加回调处理器
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # 设置定时任务（每天早上8点）
    try:
        from telegram.ext import JobQueue
        job_queue = JobQueue()
        job_queue.set_application(application)
        application._job_queue = job_queue
        job_queue.run_daily(daily_push_job, time=datetime.strptime("08:00", "%H:%M").time())
        print("⏰ 定时任务已设置：每天08:00")
    except Exception as e:
        print(f"⚠️ 定时任务设置失败: {e}")
    
    print("✅ Bot已启动！")
    print("📝 命令列表：/start /today /subscribe /upgrade /help")
    print("-" * 50)
    
    # 运行
    await application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
