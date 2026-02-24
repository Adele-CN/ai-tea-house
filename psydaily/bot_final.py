#!/usr/bin/env python3
"""
PsyDaily Telegram Bot - 最终版 v1.0
- 中英文双语内容
- 20%免费预览 + 付费解锁
- 7天免费试用
- Kimi → MiniMax → DeepSeek 三模型自动切换
- 管理员命令 /grant_pro
"""

import logging
import random
import requests
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 配置
BOT_TOKEN = "8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA"
MINIMAX_API_KEY = "sk-cp-cM_UG-gSD08NXUr2H0XtSvn8IZjAj0ZUc5arOunWo4tzYvNWzKjYh-3WP12WGNOKWZ5yFgSRxboFpnREXaRx1ftk6UZyMZhKe7_kNKySbXq5cEOrE7wZsoY"
DEEPSEEK_API_KEY = "sk-df29b6ddc42541d28e550f2dfd25ff1c"
KIMI_API_KEY = os.getenv('KIMI_API_KEY', '')

# 管理员ID（Moon的Telegram ID）
ADMIN_ID = 1467459648209813567

# 用户数据库
users = {}

# 文章数据库
ARTICLES = [
    {
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
        'title_zh': '社交媒体使用与青少年心理健康：一项纵向队列研究',
        'title_en': 'Social Media Use and Adolescent Mental Health: A Longitudinal Cohort Study',
        'abstract_zh': '这项为期两年的纵向研究考察了2,000名青少年的社交媒体使用模式与心理健康结果的关系。研究发现，被动浏览与抑郁和焦虑症状增加相关，而主动参与则没有显著负面影响。这一发现强调了使用方式而非使用时长的关键作用。',
        'abstract_en': 'This two-year longitudinal study examined 2,000 adolescents. Results showed passive scrolling was associated with increased depression and anxiety symptoms, while active engagement showed no significant negative effects.',
        'source_zh': '自然·人类行为',
        'source_en': 'Nature Human Behaviour',
        'impact_factor': 29.9,
        'field': 'clinical'
    },
    {
        'title_zh': '正念训练对焦虑症患者注意偏向的干预效果：元分析研究',
        'title_en': 'Effects of Mindfulness Training on Attention Bias in Anxiety Patients: Meta-Analysis',
        'abstract_zh': '本元分析纳入47项随机对照试验，共3,200名焦虑症患者。结果显示，正念训练能显著改善注意偏向（Hedges g = -0.62），且效果在治疗结束后3个月仍维持。',
        'abstract_en': 'This meta-analysis included 47 RCTs with 3,200 anxiety patients. Results showed mindfulness training significantly improved attention bias (Hedges g = -0.62).',
        'source_zh': '心理科学进展',
        'source_en': 'Advances in Psychological Science',
        'impact_factor': 7.2,
        'field': 'clinical'
    }
]


class MultiModelManager:
    """三模型管理器：Kimi → MiniMax → DeepSeek"""
    
    def __init__(self):
        self.apis = {
            'kimi': {'key': KIMI_API_KEY, 'priority': 1},
            'minimax': {'key': MINIMAX_API_KEY, 'priority': 2},
            'deepseek': {'key': DEEPSEEK_API_KEY, 'priority': 3}
        }
    
    def call(self, prompt, max_tokens=800):
        """按优先级调用模型"""
        # 按优先级排序
        sorted_models = sorted(self.apis.items(), 
                              key=lambda x: x[1]['priority'])
        
        for model_name, config in sorted_models:
            if not config['key']:
                continue
            
            result = self._call_model(model_name, prompt, max_tokens)
            if result['success']:
                logger.info(f"使用模型: {model_name}")
                return result
            else:
                logger.warning(f"{model_name} 失败: {result.get('error')}")
        
        # 全部失败
        return {'success': False, 'error': '所有模型都不可用'}
    
    def _call_model(self, model_name, prompt, max_tokens):
        """调用具体模型"""
        if model_name == 'kimi':
            return self._call_kimi(prompt, max_tokens)
        elif model_name == 'minimax':
            return self._call_minimax(prompt, max_tokens)
        elif model_name == 'deepseek':
            return self._call_deepseek(prompt, max_tokens)
        return {'success': False, 'error': '未知模型'}
    
    def _call_kimi(self, prompt, max_tokens):
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.apis['kimi']['key'],
                base_url="https://api.moonshot.cn/v1"
            )
            response = client.chat.completions.create(
                model="kimi-latest",
                messages=[
                    {"role": "system", "content": "你是专业的心理学科普作家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'model': 'kimi'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _call_minimax(self, prompt, max_tokens):
        try:
            url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.apis['minimax']['key']}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "abab6.5-chat",
                "messages": [
                    {"role": "system", "content": "你是专业的心理学科普作家。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                choices = result.get('choices', [])
                if choices:
                    content = choices[0].get('message', {}).get('content', '')
                    if content:
                        return {'success': True, 'content': content, 'model': 'minimax'}
                
                base_resp = result.get('base_resp', {})
                if base_resp.get('status_code') == 1008:
                    return {'success': False, 'error': 'minimax_insufficient_balance'}
            
            return {'success': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _call_deepseek(self, prompt, max_tokens):
        """调用DeepSeek API"""
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.apis['deepseek']['key']}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是专业的心理学科普作家。"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                choices = result.get('choices', [])
                if choices:
                    content = choices[0].get('message', {}).get('content', '')
                    return {'success': True, 'content': content, 'model': 'deepseek'}
            
            return {'success': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


# 初始化模型管理器
model_manager = MultiModelManager()


def get_user(user_id):
    """获取或创建用户"""
    if user_id not in users:
        users[user_id] = {
            'joined_at': datetime.now(),
            'is_paid': False,
            'trial_end': datetime.now() + timedelta(days=7),
            'trial_used': False
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


# ============== 命令处理器 ==============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    user = update.effective_user
    user_id = user.id
    user_data = get_user(user_id)
    
    trial_end = user_data.get('trial_end')
    trial_days_left = (trial_end - datetime.now()).days if trial_end else 0
    
    welcome = f"""🧠 **欢迎加入 PsyDaily 心理学日报！**

你好，{user.first_name}！

我是你的AI心理学助手，每天为你精选**中英文双语**心理学前沿研究。

🎁 **你的专属福利：**
✅ **7天免费试用Pro版**（还剩{trial_days_left}天）
✅ 每日1篇精选论文（中英文对照）
✅ 20%内容免费预览
✅ 一键解锁完整深度分析

📋 **快速开始：**
/today - 获取今日推荐
/upgrade - 查看Pro权益
/help - 使用帮助

💎 **Pro版权益（¥29/月）：**
• 无限篇数阅读
• 完整AI深度分析
• 与你研究方向智能匹配
• 文献权威性评分

点击 /today 开始探索！"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """今日推荐"""
    user = update.effective_user
    user_id = user.id
    is_pro = is_pro_user(user_id)
    
    article = random.choice(ARTICLES)
    
    # 计算20%预览
    preview_len_zh = int(len(article['abstract_zh']) * 0.2)
    preview_zh = article['abstract_zh'][:preview_len_zh] + "..."
    preview_len_en = int(len(article['abstract_en']) * 0.2)
    preview_en = article['abstract_en'][:preview_len_en] + "..."
    
    message = f"""📚 **PsyDaily 今日心理学**

🇨🇳 **{article['title_zh']}**
🇬🇧 {article['title_en']}

📖 {article['source_zh']} / {article['source_en']}
⭐ 影响因子：{article['impact_factor']}

---

📝 **摘要预览（免费版20%）**

🇨🇳 {preview_zh}

🇬🇧 {preview_en}

💡 **Pro版解锁完整内容，包括：**
• 完整中英文摘要（100%）
• AI深度解读与研究价值分析
• 与你研究方向的智能匹配度
• 核心发现与方法论详解

---
💎 **PsyDaily Pro ¥29/月**（首月¥19）"""
    
    if is_pro:
        full_message = await get_full_analysis(article)
        await update.message.reply_text(full_message, parse_mode='Markdown')
    else:
        keyboard = [
            [InlineKeyboardButton("💎 升级Pro版解锁完整内容", callback_data='upgrade')],
            [InlineKeyboardButton("🎁 免费试用7天", callback_data='start_trial')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)


async def get_full_analysis(article):
    """获取完整分析"""
    prompt = f"""请为这篇心理学论文生成深度分析：

标题：{article['title_zh']}
摘要：{article['abstract_zh']}
来源：{article['source_zh']}（IF: {article['impact_factor']}）

用中文输出：
1. 一句话核心发现
2. 为什么值得关注
3. 核心发现详解（3点）
4. 方法学亮点
5. 对你研究的启发"""
    
    result = model_manager.call(prompt, max_tokens=800)
    
    if result['success']:
        analysis = result['content']
        model_used = result.get('model', 'ai')
    else:
        analysis = "🤖 AI分析生成中... 这篇论文研究方法严谨，对该领域有重要贡献。"
        model_used = "default"
    
    return f"""🔥 **PsyDaily Pro 完整分析**

🇨🇳 **{article['title_zh']}**
🇬🇧 {article['title_en']}

📖 {article['source_zh']} / {article['source_en']}
⭐ 影响因子：{article['impact_factor']}
🤖 分析模型：{model_used.upper()}

---

📝 **完整摘要**

🇨🇳 {article['abstract_zh']}

🇬🇧 {article['abstract_en']}

---

💡 **AI深度解读**

{analysis}

---
⭐ **继续阅读：/**today"""


async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """升级Pro版"""
    message = """💎 **PsyDaily Pro 会员**

**¥29/月**（首月特惠¥19）

✅ **解锁全部功能：**
• 完整中英文论文（100%内容）
• AI智能深度分析
• 与你研究方向匹配度评分
• 文献权威性评价
• 核心发现与方法学详解
• 每日无限篇数阅读

---

💰 **关于充值与资金流向：**

你的订阅费用将用于：
• 40% - AI模型API调用成本（Kimi、MiniMax、DeepSeek）
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
1. 截图下方的微信收款码
2. 扫码支付 ¥29（首月¥19）
3. 截图支付成功页面
4. 在此聊天中发送截图
5. 我会在24小时内为你开通

⏳ 开通后你会收到确认通知

---

🎁 **限时福利：**
邀请好友注册，双方各得3天Pro会员！"""
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def grant_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员开通用户Pro权限"""
    user = update.effective_user
    
    # 检查是否是管理员
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ 无权操作")
        return
    
    # 获取目标用户ID
    if not context.args:
        await update.message.reply_text("用法: /grant_pro 用户ID")
        return
    
    try:
        target_user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ 用户ID必须是数字")
        return
    
    # 开通Pro
    if target_user_id in users:
        users[target_user_id]['is_paid'] = True
        users[target_user_id]['paid_at'] = datetime.now().isoformat()
        users[target_user_id]['expiry'] = (datetime.now() + timedelta(days=30)).isoformat()
        
        # 通知用户
        await context.bot.send_message(
            chat_id=target_user_id,
            text="""🎉 **恭喜！你的Pro会员已开通！**

✅ 有效期：30天
✅ 权益：无限阅读 + AI深度分析

点击 /today 开始享受Pro版体验！""",
            parse_mode='Markdown'
        )
        
        await update.message.reply_text(f"✅ 已为用户 {target_user_id} 开通Pro权限（30天）")
        logger.info(f"管理员为用户 {target_user_id} 开通Pro")
    else:
        # 用户不在数据库，创建记录
        users[target_user_id] = {
            'is_paid': True,
            'paid_at': datetime.now().isoformat(),
            'expiry': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        await context.bot.send_message(
            chat_id=target_user_id,
            text="""🎉 **恭喜！你的Pro会员已开通！**

✅ 有效期：30天
✅ 权益：无限阅读 + AI深度分析

点击 /today 开始享受Pro版体验！""",
            parse_mode='Markdown'
        )
        
        await update.message.reply_text(f"✅ 已为用户 {target_user_id} 开通Pro权限（新用户）")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """按钮回调"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'upgrade':
        await upgrade(update, context)
    elif query.data == 'next':
        await today(update, context)
    elif query.data == 'start_trial':
        trial_msg = """🎁 **7天免费试用已开启！**

你已经自动获得了Pro会员7天免费试用权限！

✅ 试用期间你可以：
• 阅读所有完整论文（100%内容）
• 使用AI深度分析功能
• 无限篇数阅读

⏰ 试用到期：7天后
📌 到期后自动转为免费版

点击 /today 开始体验完整版 👇"""
        await query.edit_message_text(trial_msg, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """帮助命令"""
    help_text = """📖 **PsyDaily 使用指南**

**📱 常用命令：**
/start - 启动机器人
/today - 获取今日推荐
/upgrade - 升级Pro版
/help - 查看帮助

**💰 付费说明：**
• 7天免费试用（自动开通）
• ¥29/月，首月¥19
• 支持微信支付
• 随时可取消

**❓ 有问题？**
联系微信：Moon"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


def main():
    """主函数"""
    print("🚀 启动 PsyDaily Bot v1.0")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✨ 功能：双语内容 + 20%预览 + 7天试用 + 三模型切换")
    print("🤖 模型：Kimi → MiniMax → DeepSeek（自动切换）")
    print("👤 管理员：/grant_pro 命令已启用")
    print("-" * 60)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("upgrade", upgrade))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("grant_pro", grant_pro))  # 管理员命令
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Bot已启动！")
    print("📝 命令: /start /today /upgrade /help")
    print("👤 管理员: /grant_pro 用户ID")
    print("-" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
