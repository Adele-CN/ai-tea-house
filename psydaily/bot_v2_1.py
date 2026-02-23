#!/usr/bin/env python3
"""
PsyDaily Bot v2.1 - 修复版
- 推送：论文速读 + AI分析 + 原文链接
- /today：查看完整内容（含原文链接）
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
    if user_id not in users:
        users[user_id] = {
            'joined_at': datetime.now(),
            'is_paid': False,
            'trial_end': datetime.now() + timedelta(days=7),
            'seen_upgrade': False
        }
    return users[user_id]

def is_pro_user(user_id):
    user = get_user(user_id)
    if user.get('is_paid', False):
        return True
    trial_end = user.get('trial_end')
    if trial_end and datetime.now() < trial_end:
        return True
    return False

def load_daily_content():
    filename = f"{CONTENT_DIR}/daily_{datetime.now().strftime('%Y%m%d')}.json"
    if not os.path.exists(filename):
        return get_sample_content()
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_sample_content():
    return [{
        'article': {
            'id': 1,
            'title_zh': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
            'title_en': 'Working Memory Capacity and Decision Quality',
            'abstract_zh': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响。',
            'abstract_en': 'This study investigated the relationship between working memory capacity and decision quality.',
            'source_zh': '心理学报',
            'source_en': 'Acta Psychologica Sinica',
            'impact_factor': 8.5,
            'pub_date': '2025-01-15',
            'doi': '10.3724/SP.J.1041.2025.00123',
            'url': 'https://journal.psych.ac.cn/CN/10.3724/SP.J.1041.2025.00123'
        },
        'analysis': {
            'core_finding': '工作记忆容量越大的人，做复杂决策时越理性。',
            'why_matters': '这解释了为什么有些人面对重要选择时更冷静。',
            'detailed_findings': '1. 工作记忆与决策质量呈正相关\n2. 复杂决策中效应更强\n3. 训练工作记忆可能改善决策',
            'methodology': '采用双任务范式，巧妙分离不同认知成分。',
            'inspiration': '在做重大决定前，先清理大脑缓存。',
            'vortex_connection': '这与信息漩涡中注意力分散的现象密切相关。'
        }
    }]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    user_data = get_user(user_id)
    trial_days = (user_data['trial_end'] - datetime.now()).days
    
    welcome = f"""🧠 **欢迎加入 PsyDaily 信息漩涡研究日报！**

你好，{user.first_name}！

每天为你精选**信息漩涡相关**的心理学研究。

🎁 **你的福利：**
✅ 7天免费试用Pro版（还剩{trial_days}天）
✅ 每天3篇论文推送（07:00/12:00/18:00）
✅ 20%内容免费预览

📋 **快速开始：**
/subscribe - 订阅每日推送
/today - 查看完整论文库
/help - 使用帮助

💎 **Pro版 ¥29/月（首月¥19）**
解锁完整AI分析 + 无限阅读"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """查看完整论文（所有用户都可看完整版）"""
    user = update.effective_user
    
    try:
        contents = load_daily_content()
        if not contents:
            await update.message.reply_text("⚠️ 今天的内容还在准备中，请稍后再试。\n\n发送 /subscribe 订阅每日推送。")
            return
        
        # 随机选一篇发送完整版
        content = random.choice(contents)
        article = content.get('article', {})
        analysis = content.get('analysis', {})
        
        # 构建完整消息
        message = f"""📚 **PsyDaily 完整论文** 🧠

🇬🇧 **{article.get('title_en', 'No Title')}**
🇨🇳 {article.get('title_zh', '')}

📖 **{article.get('journal_en', 'Unknown Journal')}**
⭐ 影响因子：{article.get('impact_factor', 'N/A')}
📅 发表时间：{article.get('pub_date', 'N/A')}
🏷️ 主题：{', '.join(article.get('tags', []))}
🔗 [阅读原文]({article.get('url', '#')})

---

📝 **摘要**

{article.get('abstract_en', '')[:300]}...

🇨🇳 {article.get('abstract_zh', '')[:250]}...

---

💡 **AI深度分析**

**1. 一句话核心发现**
{analysis.get('core_finding', '分析生成中...')}

**2. 为什么值得关注**
{analysis.get('why_matters', '...')}

**3. 核心发现详解**
{analysis.get('detailed_findings', '...')}

**4. 方法学亮点**
{analysis.get('methodology', '...')}

**5. 对你研究的启发**
{analysis.get('inspiration', '...')}

**6. 与信息漩涡的关联**
{analysis.get('vortex_connection', '...')}

---

✅ **PsyDaily 每日 07:00/12:00/18:00 推送**
发送 /subscribe 订阅每日论文 💎"""
        
        # 如果消息太长，分段发送
        if len(message) > 4000:
            # 先发送论文基本信息
            part1 = message[:4000]
            await update.message.reply_text(part1, parse_mode='Markdown', disable_web_page_preview=True)
            # 再发送剩余分析
            part2 = message[4000:]
            if part2.strip():
                await update.message.reply_text(part2, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
        
    except Exception as e:
        logger.error(f"加载内容失败: {e}")
        await update.message.reply_text("⚠️ 内容加载出错，正在修复中...")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """订阅每日推送"""
    user = update.effective_user
    user_id = user.id
    
    subscribers_file = f'{CONTENT_DIR}/subscribers.json'
    subscribers = []
    if os.path.exists(subscribers_file):
        with open(subscribers_file, 'r') as f:
            subscribers = json.load(f)
    
    if user_id in subscribers:
        await update.message.reply_text("✅ 你已订阅！\n\n🌅 07:00 晨读\n☀️ 12:00 午读\n🌙 18:00 夜读\n\n发送 /unsubscribe 取消")
        return
    
    subscribers.append(user_id)
    with open(subscribers_file, 'w') as f:
        json.dump(subscribers, f)
    
    await update.message.reply_text(
        "🎉 **订阅成功！**\n\n"
        "每天3篇信息漩涡相关论文：\n"
        "🌅 07:00 晨读\n"
        "☀️ 12:00 午读\n"
        "🌙 18:00 夜读\n\n"
        "每篇包含：摘要 + AI分析 + 原文链接\n\n"
        "发送 /today 随时查看完整论文库"
    )

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """取消订阅"""
    user = update.effective_user
    user_id = user.id
    
    subscribers_file = f'{CONTENT_DIR}/subscribers.json'
    subscribers = []
    if os.path.exists(subscribers_file):
        with open(subscribers_file, 'r') as f:
            subscribers = json.load(f)
    
    if user_id not in subscribers:
        await update.message.reply_text("⚠️ 你还没有订阅。\n\n发送 /subscribe 开始订阅。")
        return
    
    subscribers.remove(user_id)
    with open(subscribers_file, 'w') as f:
        json.dump(subscribers, f)
    
    await update.message.reply_text("✅ 已取消订阅。\n\n发送 /subscribe 重新订阅。")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """📖 **PsyDaily 使用指南**

**📱 命令：**
/start - 启动机器人
/subscribe - 订阅每日推送
/unsubscribe - 取消订阅
/today - 查看今日论文库（含原文链接）
/help - 查看帮助

**📬 每日推送（07:00/12:00/18:00）：**
• 论文速读 + AI分析
• 原文链接（DOI/URL）
• 20%内容免费预览

**💎 Pro版（¥29/月）：**
• 完整AI深度分析
• 方法学详解
• 与信息漩涡的关联分析
• 无限阅读

**💰 开通方式：**
添加微信：Moon（备注 PsyDaily）
转账后24小时内开通"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """升级Pro版"""
    message = """💎 **PsyDaily Pro 会员**

**价格：¥29/月**（首月特惠¥19）

✅ **解锁全部功能：**
• 完整中英文论文（100%内容）
• 核心发现详解
• 方法学亮点分析
• 对你研究的启发
• 与信息漩涡的深度关联
• 每日无限篇数阅读

---

💰 **资金流向：**
• 40% - AI模型API调用成本
• 30% - 服务器与数据存储
• 20% - 内容研发与产品优化
• 10% - 平台运营

**我们承诺：**
✓ 无隐藏费用
✓ 随时可取消订阅
✓ 7天免费试用（已自动开通）
✓ 首月不满意可退款

---

📱 **开通方式：**

**方式1 - 微信支付（推荐）：**
1. 添加微信：Moon（备注 PsyDaily）
2. 转账 ¥29（首月¥19）
3. 发送你的Telegram用户名
4. 24小时内为你开通

**方式2 - 对公转账：**
（如需发票，请联系）

---

🎁 **限时福利：**
邀请好友注册，双方各得3天Pro会员！

有问题？联系微信：Moon"""
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def grant_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员开通Pro权限"""
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
        
        await context.bot.send_message(
            chat_id=target_id,
            text="🎉 **Pro会员已开通！**\n\n✅ 有效期：30天\n✅ 无限阅读 + AI深度分析\n\n点击 /today 查看完整论文库！",
            parse_mode='Markdown'
        )
        await update.message.reply_text(f"✅ 已为用户 {target_id} 开通Pro权限")
    except Exception as e:
        await update.message.reply_text(f"❌ 错误: {e}")

def main():
    print("🚀 启动 PsyDaily Bot v2.1")
    print("✨ 推送: 论文速读 + 原文链接")
    print("✨ /today: 查看完整论文库")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("upgrade", upgrade))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("grant_pro", grant_pro))
    
    print("✅ Bot已启动！")
    print("-" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
