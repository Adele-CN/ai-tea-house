#!/usr/bin/env python3
"""
PsyDaily Bot v2.0 - 预生成内容版
不消耗实时Kimi额度
"""

import logging
import json
import os
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"
ADMIN_ID = 1467459648209813567

users = {}
CONTENT_DIR = '/root/.openclaw/workspace/psydaily/data/content'


def get_user(user_id):
    """获取或创建用户"""
    if user_id not in users:
        users[user_id] = {
            'joined_at': datetime.now(),
            'is_paid': False,
            'trial_end': datetime.now() + timedelta(days=7),
            'seen_upgrade': False  # 标记是否已看过付费提示
        }
    return users[user_id]


def is_pro_user(user_id):
    """检查是否是Pro用户"""
    user = get_user(user_id)
    if user.get('is_paid', False):
        return True
    trial_end = user.get('trial_end')
    if trial_end and datetime.now() < trial_end:
        return True
    return False


def load_daily_content():
    """加载今天预生成的内容"""
    filename = f"{CONTENT_DIR}/daily_{datetime.now().strftime('%Y%m%d')}.json"
    
    # 如果今天没有，用示例内容
    if not os.path.exists(filename):
        return get_sample_content()
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_sample_content():
    """示例内容（用于测试）"""
    return [{
        'article': {
            'id': 1,
            'title_zh': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
            'title_en': 'Working Memory Capacity and Decision Quality',
            'abstract_zh': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响。实验1采用N-back任务测量工作记忆，实验2使用爱荷华博弈任务评估决策。结果表明，工作记忆容量与决策质量呈显著正相关（r=0.45, p<0.001）。',
            'abstract_en': 'This study investigated the relationship between working memory capacity and decision quality.',
            'source_zh': '心理学报',
            'source_en': 'Acta Psychologica Sinica',
            'impact_factor': 8.5
        },
        'analysis': {
            'core_finding': '工作记忆容量越大的人，做复杂决策时越理性，不容易被情绪带偏。',
            'why_matters': '这解释为什么有些人面对重要选择时更冷静——他们的大脑"内存"更大，能同时处理更多信息而不混乱。',
            'detailed_findings': '1. 工作记忆与决策质量呈正相关（r=0.45）\n2. 复杂决策中效应更强\n3. 训练工作记忆可能改善决策能力',
            'methodology': '采用双任务范式，巧妙分离不同认知成分。',
            'inspiration': '在做重大决定前，先清理大脑缓存（休息好、减少干扰），可能帮助你做出更理性的选择。'
        }
    }]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    user = update.effective_user
    user_id = user.id
    user_data = get_user(user_id)
    
    trial_days = (user_data['trial_end'] - datetime.now()).days
    
    welcome = f"""🧠 **欢迎加入 PsyDaily 心理学日报！**

你好，{user.first_name}！

每天为你精选**中英文双语**心理学前沿研究。

🎁 **你的福利：**
✅ 7天免费试用Pro版（还剩{trial_days}天）
✅ 每日1篇精选论文（中英文对照）
✅ 20%内容免费预览
✅ 一键解锁完整深度分析

📋 **快速开始：**
/today - 获取今日推荐
/help - 使用帮助

💎 **Pro版 ¥29/月（首月¥19）**
点击 /today 查看详情"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """今日推荐 - 预生成内容版"""
    user = update.effective_user
    user_id = user.id
    is_pro = is_pro_user(user_id)
    user_data = get_user(user_id)
    
    # 加载预生成内容
    try:
        contents = load_daily_content()
        if not contents:
            await update.message.reply_text("⚠️ 今天的内容还在准备中，请稍后再试。\n\n可以先发送 /subscribe 订阅每日推送。")
            return
        content = random.choice(contents)
        article = content.get('article', {})
        analysis = content.get('analysis', {})
    except Exception as e:
        logger.error(f"加载内容失败: {e}")
        await update.message.reply_text("⚠️ 内容加载出错，正在修复中...\n\n可以先发送 /help 查看其他功能。")
        return
    
    # 免费版内容（到"为什么值得关注"为止）
    free_message = f"""📚 **PsyDaily 今日心理学**

🇨🇳 **{article['title_zh']}**
🇬🇧 {article['title_en']}

📖 {article['source_zh']} (IF: {article['impact_factor']})

---

📝 **摘要预览**

🇨🇳 {article['abstract_zh'][:120]}...

🇬🇧 {article['abstract_en'][:100]}...

---

💡 **AI分析（免费预览）**

**1. 一句话核心发现**
{analysis['core_finding']}

**2. 为什么值得关注**
{analysis['why_matters']}

---

🔒 **Pro版解锁更多：**
• 核心发现详解...
• 方法学亮点...
• 对你研究的启发...
• 完整中英文摘要"""
    
    if is_pro:
        # Pro用户看到完整内容
        full_message = f"""{free_message}

---

📖 **完整内容（Pro版）**

**3. 核心发现详解**
{analysis['detailed_findings']}

**4. 方法学亮点**
{analysis['methodology']}

**5. 对你研究的启发**
{analysis['inspiration']}

---
✅ **Pro会员权益已解锁**
💎 有效期：{'30天' if user_data.get('is_paid') else '试用期内'}

继续阅读：/today"""
        
        await update.message.reply_text(full_message, parse_mode='Markdown')
    else:
        # 免费用户 - 只显示一次升级按钮
        if not user_data.get('seen_upgrade', False):
            user_data['seen_upgrade'] = True
            keyboard = [
                [InlineKeyboardButton("💎 升级Pro版解锁完整内容", callback_data='upgrade_info')],
                [InlineKeyboardButton("🎁 免费试用7天", callback_data='start_trial')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(free_message, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            # 已经看过升级提示，不再显示按钮
            await update.message.reply_text(free_message, parse_mode='Markdown')


async def upgrade_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """升级信息 - 只显示一次"""
    message = """💎 **PsyDaily Pro 会员**

**价格：¥29/月**（首月特惠¥19）

✅ **解锁全部功能：**
• 完整中英文论文（100%内容）
• 核心发现详解
• 方法学亮点分析
• 对你研究的启发
• 每日无限篇数阅读

---

💰 **资金流向：**
• 40% - AI模型成本
• 30% - 服务器存储
• 20% - 内容研发
• 10% - 平台运营

---

📱 **如何开通：**

**方式1 - 微信支付：**
1. 添加微信：Moon（备注 PsyDaily）
2. 转账 ¥29（首月¥19）
3. 发送你的Telegram用户名
4. 我24小时内为你开通

**方式2 - 对公转账：**
（如需发票，请联系）

---

🎁 **限时福利：**
邀请好友注册，双方各得3天Pro会员！

有问题？联系微信：Moon"""
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def grant_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员开通用户Pro权限"""
    user = update.effective_user
    
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ 无权操作")
        return
    
    if not context.args:
        await update.message.reply_text("用法: /grant_pro 用户ID")
        return
    
    try:
        target_id = int(context.args[0])
        users[target_id] = users.get(target_id, {})
        users[target_id]['is_paid'] = True
        users[target_id]['paid_at'] = datetime.now().isoformat()
        users[target_id]['expiry'] = (datetime.now() + timedelta(days=30)).isoformat()
        
        await context.bot.send_message(
            chat_id=target_id,
            text="🎉 **你的Pro会员已开通！**\n\n✅ 有效期：30天\n✅ 权益：无限阅读 + AI深度分析\n\n点击 /today 开始享受Pro版！",
            parse_mode='Markdown'
        )
        await update.message.reply_text(f"✅ 已为用户 {target_id} 开通Pro权限")
    except Exception as e:
        await update.message.reply_text(f"❌ 错误: {e}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'upgrade_info':
        await upgrade_info(update, context)
    elif query.data == 'start_trial':
        msg = "🎁 **7天免费试用已开启！**\n\n✅ 你可以阅读完整论文\n✅ 使用AI深度分析\n✅ 无限篇数阅读\n\n点击 /today 开始体验！"
        await query.edit_message_text(msg, parse_mode='Markdown')


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """订阅每日推送"""
    user = update.effective_user
    user_id = user.id
    
    # 加载订阅列表
    subscribers_file = f'{CONTENT_DIR}/subscribers.json'
    subscribers = []
    if os.path.exists(subscribers_file):
        with open(subscribers_file, 'r') as f:
            subscribers = json.load(f)
    
    # 检查是否已订阅
    if user_id in subscribers:
        await update.message.reply_text("✅ 你已经订阅了每日推送！\n\n推送时间：\n🌅 07:00 晨读\n☀️ 12:00 午读\n🌙 18:00 夜读\n\n如需取消，发送 /unsubscribe")
        return
    
    # 添加订阅
    subscribers.append(user_id)
    with open(subscribers_file, 'w') as f:
        json.dump(subscribers, f)
    
    # 获取今天的论文预览
    contents = load_daily_content()
    if contents:
        article = contents[0]['article']
        preview = f"\n📰 今日预览：{article['title_en'][:50]}..."
    else:
        preview = ""
    
    await update.message.reply_text(
        f"🎉 **订阅成功！**\n\n"
        f"你将每天收到3篇信息漩涡相关的心理学研究：\n"
        f"🌅 07:00 晨读\n"
        f"☀️ 12:00 午读\n"
        f"🌙 18:00 夜读\n"
        f"{preview}\n\n"
        f"💡 提示：\n"
        f"• 推送内容包含论文摘要和AI分析\n"
        f"• 回复 /today 可随时查看完整论文\n"
        f"• 如需取消，发送 /unsubscribe"
    )


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """取消订阅"""
    user = update.effective_user
    user_id = user.id
    
    # 加载订阅列表
    subscribers_file = f'{CONTENT_DIR}/subscribers.json'
    subscribers = []
    if os.path.exists(subscribers_file):
        with open(subscribers_file, 'r') as f:
            subscribers = json.load(f)
    
    # 检查是否已订阅
    if user_id not in subscribers:
        await update.message.reply_text("⚠️ 你还没有订阅。\n\n发送 /subscribe 开始订阅每日推送。")
        return
    
    # 移除订阅
    subscribers.remove(user_id)
    with open(subscribers_file, 'w') as f:
        json.dump(subscribers, f)
    
    await update.message.reply_text("✅ 已取消订阅。\n\n你不会再收到每日推送。\n\n如需重新订阅，发送 /subscribe")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """帮助命令"""
    help_text = """📖 **PsyDaily 使用指南**

**📱 常用命令：**
/start - 启动机器人
/today - 获取今日推荐
/help - 查看帮助

**🆓 免费版：**
• 每日1篇精选论文
• 中英文双语标题
• 20%内容免费（核心发现+为什么值得关注）

**💎 Pro版（¥29/月）：**
• 完整论文内容
• AI深度分析（5个维度）
• 无限篇数阅读

**💰 如何开通：**
1. 点击 /today 查看论文
2. 点击"升级Pro版"了解详情
3. 添加微信：Moon
4. 转账后24小时内开通

**🎁 推广奖励：**
邀请好友注册，双方各得3天Pro会员！

❓ 有问题？联系微信：Moon"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


def main():
    print("🚀 启动 PsyDaily Bot v2.0")
    print("✨ 预生成内容模式 - 不消耗实时Kimi额度")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("grant_pro", grant_pro))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Bot已启动！")
    print("-" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
