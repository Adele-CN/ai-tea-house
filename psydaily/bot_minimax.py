#!/usr/bin/env python3
"""
PsyDaily Telegram Bot - MiniMax 版
修复 /today 命令 + 接入 MiniMax API
"""

import logging
import random
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 启用日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 配置
BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"
MINIMAX_API_KEY = "sk-cp-cM_UG-gSD08NXUr2H0XtSvn8IZjAj0ZUc5arOunWo4tzYvNWzKjYh-3WP12WGNOKWZ5yFgSRxboFpnREXaRx1ftk6UZyMZhKe7_kNKySbXq5cEOrE7wZsoY"
MINIMAX_GROUP_ID = "2017410108979417488"

# 用户数据库
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

def call_minimax(prompt, max_tokens=800):
    """调用 MiniMax API"""
    try:
        url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
        
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "abab6.5-chat",
            "messages": [
                {"role": "system", "content": "你是PsyDaily的心理学内容创作助手。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # 解析响应
            choices = result.get('choices', [])
            if choices and len(choices) > 0:
                message = choices[0].get('message', {})
                content = message.get('content', '')
                if content:
                    return {'success': True, 'content': content}
            
            # 检查是否有错误
            base_resp = result.get('base_resp', {})
            if base_resp.get('status_code') == 1008:
                return {'success': False, 'error': '余额不足，请充值'}
            
            return {'success': False, 'error': '响应格式异常'}
        else:
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    user = update.effective_user
    user_id = user.id
    
    if user_id not in users:
        users[user_id] = {
            'name': user.first_name,
            'joined': datetime.now().isoformat(),
            'is_paid': False
        }
    
    welcome = f"""🧠 **欢迎加入 PsyDaily 心理学日报！**

你好，{user.first_name}！

我是你的AI心理学助手，每天为你精选一篇心理学前沿研究。

📋 **命令列表：**
/start - 查看欢迎信息
/today - 获取今日推荐
/upgrade - 升级Pro版
/help - 查看帮助

💎 **版本对比：**
🆓 免费版：每日1篇基础推送
💎 Pro版：¥29/月，无限+深度分析

点击 /today 获取今天的推荐！"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')
    logger.info(f"新用户启动: {user.first_name} (ID: {user_id})")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """今日推荐 - 修复版"""
    user = update.effective_user
    user_id = user.id
    
    logger.info(f"用户 {user_id} 请求 /today")
    
    try:
        # 选择随机文章
        article = random.choice(ARTICLES)
        
        # 使用 MiniMax 生成分析
        prompt = f"""请为这篇心理学论文写一段吸引人的简介（100字以内）：

标题：{article['title']}
来源：{article['source']}
影响因子：{article['impact_factor']}

要求：
1. 一句话概括核心发现
2. 说明为什么心理学研究者应该关注
3. 语言简洁有力"""
        
        # 调用 MiniMax
        result = call_minimax(prompt, max_tokens=200)
        
        if result['success']:
            analysis = result['content']
        else:
            # 失败时使用默认分析
            analysis = f"这篇文章来自{'顶级' if article['impact_factor'] >= 20 else '权威' if article['impact_factor'] >= 10 else '核心'}期刊《{article['source']}》，对心理学研究有重要参考价值。"
            logger.warning(f"MiniMax调用失败: {result.get('error')}")
        
        # 格式化消息
        lang_emoji = '🇨🇳' if article['language'] == 'zh' else '🇬🇧'
        
        message = f"""{lang_emoji} **PsyDaily 今日心理学**

**{article['title']}**
📖 {article['source']} (IF: {article['impact_factor']})

📝 **摘要**
{article['abstract'][:180]}...

💡 **AI解读**
{analysis}

---
✨ **升级Pro版解锁：**
• 与你研究方向的匹配度分析 📊
• 文献对话脉络梳理 📚
• 核心发现详解 🔬
• 个性化深度解读 💡

💎 **PsyDaily Pro ¥29/月**
首月特惠 ¥19"""
        
        # 添加按钮
        keyboard = [
            [InlineKeyboardButton("💎 升级Pro版", callback_data='upgrade')],
            [InlineKeyboardButton("🔄 换一篇", callback_data='next')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        logger.info(f"已发送今日推荐给用户 {user_id}")
        
    except Exception as e:
        logger.error(f"/today 错误: {e}")
        await update.message.reply_text("❌ 获取推荐时出错，请稍后再试。", parse_mode='Markdown')

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """升级Pro版"""
    message = """💎 **PsyDaily Pro 会员**

**¥29/月**，解锁全部功能：

✅ 无限篇数阅读
✅ 智能匹配度分析  
✅ 文献权威性评分
✅ 研究脉络梳理
✅ 个性化深度解读
✅ 优先客服支持

🎁 **限时优惠**：首月仅需¥19！

**开通方式：**
添加微信：PsyDaily_Admin
发送"升级+你的Telegram用户名"

我们会立即为你开通Pro权限。"""
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """帮助命令"""
    help_text = """📖 **PsyDaily 使用指南**

**基础命令：**
/start - 启动机器人
/today - 获取今日心理学推荐
/upgrade - 升级Pro版
/help - 查看帮助

**如何获得最佳体验：**
1. 使用 /today 每天获取精选论文
2. 点击"换一篇"查看更多推荐
3. 升级为Pro版解锁深度分析

**联系我们：**
微信：PsyDaily_Admin
邮箱：psydaily@example.com

💡 **关于PsyDaily**
我们每天从顶级心理学期刊中精选最新研究，用AI技术为你生成个性化解读，让学术前沿触手可及。"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """按钮回调"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == 'upgrade':
        await upgrade(update, context)
    elif query.data == 'next':
        # 换一篇 - 直接调用 today 逻辑
        await today(update, context)

def main():
    """主函数"""
    print("🚀 启动 PsyDaily Bot (MiniMax版)...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建应用
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("upgrade", upgrade))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Bot已启动！")
    print("📝 命令: /start /today /upgrade /help")
    print("🤖 AI模型: MiniMax abab6.5-chat")
    print("-" * 50)
    
    # 运行
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
