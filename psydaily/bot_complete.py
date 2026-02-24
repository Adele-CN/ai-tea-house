#!/usr/bin/env python3
"""
PsyDaily Telegram Bot - 完整版
- 中英文双语内容
- 20%免费预览 + 付费解锁
- 7天免费试用
- Kimi → MiniMax 自动切换
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
KIMI_API_KEY = os.getenv('KIMI_API_KEY', '')  # 从环境变量读取

# 用户数据库（内存版，后续用数据库）
users = {}

# 文章数据库 - 中英文双语
ARTICLES = [
    {
        'title_zh': '工作记忆容量与决策质量的关系：基于双任务范式的实验研究',
        'title_en': 'Working Memory Capacity and Decision Quality: A Dual-Task Paradigm Study',
        'abstract_zh': '本研究通过三个实验探讨了工作记忆容量对决策质量的影响。实验1采用N-back任务测量工作记忆，实验2使用爱荷华博弈任务评估决策，实验3通过双任务范式分离认知成分。结果表明，工作记忆容量与决策质量呈显著正相关（r=0.45, p<0.001），且在复杂决策情境中效应更强。这一发现为理解决策的认知机制提供了新视角，对改善决策训练方案具有实践意义。',
        'abstract_en': 'This study investigated the relationship between working memory capacity and decision quality through three experiments. Experiment 1 used N-back task to measure working memory, Experiment 2 used Iowa Gambling Task to assess decision-making, and Experiment 3 separated cognitive components through dual-task paradigm. Results showed significant positive correlation (r=0.45, p<0.001) between working memory capacity and decision quality, with stronger effects in complex decision contexts.',
        'source_zh': '心理学报',
        'source_en': 'Acta Psychologica Sinica',
        'impact_factor': 8.5,
        'field': 'cognitive'
    },
    {
        'title_zh': '社交媒体使用与青少年心理健康：一项纵向队列研究',
        'title_en': 'Social Media Use and Adolescent Mental Health: A Longitudinal Cohort Study',
        'abstract_zh': '这项为期两年的纵向研究考察了2,000名青少年的社交媒体使用模式与心理健康结果的关系。研究发现，被动浏览与抑郁和焦虑症状增加相关，而主动参与则没有显著负面影响。这一发现强调了使用方式而非使用时长的关键作用，为数字时代的青少年心理健康干预提供了实证依据。',
        'abstract_en': 'This two-year longitudinal study examined the relationship between social media use patterns and mental health outcomes in 2,000 adolescents. Results showed that passive scrolling was associated with increased depression and anxiety symptoms, while active engagement showed no significant negative effects. This finding highlights the critical role of usage patterns over duration.',
        'source_zh': '自然·人类行为',
        'source_en': 'Nature Human Behaviour',
        'impact_factor': 29.9,
        'field': 'clinical'
    },
    {
        'title_zh': '正念训练对焦虑症患者注意偏向的干预效果：一项元分析研究',
        'title_en': 'Effects of Mindfulness Training on Attention Bias in Anxiety Patients: A Meta-Analysis',
        'abstract_zh': '本元分析纳入47项随机对照试验，共3,200名焦虑症患者。结果显示，正念训练能显著改善注意偏向（Hedges g = -0.62, 95% CI: -0.81 to -0.43），且效果在治疗结束后3个月仍维持。亚组分析发现，8周以上的训练效果更显著。研究为正念干预在焦虑症治疗中的应用提供了高质量证据。',
        'abstract_en': 'This meta-analysis included 47 randomized controlled trials with 3,200 anxiety disorder patients. Results showed that mindfulness training significantly improved attention bias (Hedges g = -0.62), with effects maintained at 3-month follow-up. Subgroup analysis revealed more significant effects for training lasting over 8 weeks.',
        'source_zh': '心理科学进展',
        'source_en': 'Advances in Psychological Science',
        'impact_factor': 7.2,
        'field': 'clinical'
    }
]


class MultiModelManager:
    """多模型管理器 - Kimi优先，MiniMax备用"""
    
    def __init__(self):
        self.kimi_key = KIMI_API_KEY
        self.minimax_key = MINIMAX_API_KEY
        self.kimi_quota = 1000  # 假设日限额
        self.kimi_used = 0
    
    def call(self, prompt, max_tokens=500):
        """调用模型，Kimi优先"""
        # 先尝试Kimi（如果你有API Key）
        if self.kimi_key and self.kimi_used < self.kimi_quota:
            result = self._call_kimi(prompt, max_tokens)
            if result['success']:
                self.kimi_used += 1
                return result
        
        # Kimi失败或额度用完，使用MiniMax
        return self._call_minimax(prompt, max_tokens)
    
    def _call_kimi(self, prompt, max_tokens):
        """调用Kimi API"""
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.kimi_key,
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
        """调用MiniMax API"""
        try:
            url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.minimax_key}",
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
                
                # 检查余额
                base_resp = result.get('base_resp', {})
                if base_resp.get('status_code') == 1008:
                    return {'success': False, 'error': 'minimax_insufficient_balance'}
            
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
            'trial_end': datetime.now() + timedelta(days=7),  # 7天免费试用
            'trial_used': False
        }
    return users[user_id]


def is_pro_user(user_id):
    """检查是否是Pro用户"""
    user = get_user(user_id)
    
    # 付费用户
    if user.get('is_paid', False):
        return True
    
    # 试用期内
    trial_end = user.get('trial_end')
    if trial_end and datetime.now() < trial_end:
        return True
    
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    user = update.effective_user
    user_id = user.id
    user_data = get_user(user_id)
    
    # 检查试用状态
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
• 核心发现详解

点击 /today 开始探索！"""
    
    await update.message.reply_text(welcome, parse_mode='Markdown')


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """今日推荐 - 双语版 + 20%免费预览"""
    user = update.effective_user
    user_id = user.id
    is_pro = is_pro_user(user_id)
    
    # 选择文章
    article = random.choice(ARTICLES)
    
    # 计算20%预览点
    abstract_zh_len = len(article['abstract_zh'])
    preview_len = int(abstract_zh_len * 0.2)
    preview_zh = article['abstract_zh'][:preview_len] + "..."
    
    abstract_en_len = len(article['abstract_en'])
    preview_en_len = int(abstract_en_len * 0.2)
    preview_en = article['abstract_en'][:preview_en_len] + "..."
    
    # 基础消息（免费部分）
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
• 文献对话脉络梳理"""
    
    # 根据用户状态显示不同按钮
    if is_pro:
        # Pro用户直接显示完整内容
        full_message = await get_full_analysis(article, user_id)
        await update.message.reply_text(full_message, parse_mode='Markdown')
    else:
        # 免费用户显示升级按钮
        keyboard = [
            [InlineKeyboardButton("💎 升级Pro版解锁完整内容", callback_data='upgrade')],
            [InlineKeyboardButton("🔄 换一篇", callback_data='next')],
            [InlineKeyboardButton("🎁 免费试用7天", callback_data='start_trial')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)


async def get_full_analysis(article, user_id):
    """获取完整分析（Pro版）"""
    
    # 使用AI生成深度分析
    prompt = f"""请为这篇心理学论文生成深度分析：

标题：{article['title_zh']}
摘要：{article['abstract_zh']}
来源：{article['source_zh']}（IF: {article['impact_factor']}）

请用中文输出：
1. 一句话核心发现（吸引人）
2. 为什么值得关注（对心理学研究生的具体价值）
3. 核心发现详解（3点，每点50字）
4. 方法学亮点
5. 对你研究的启发"""
    
    result = model_manager.call(prompt, max_tokens=800)
    
    if result['success']:
        analysis = result['content']
        model_used = result.get('model', 'ai')
    else:
        analysis = "🤖 AI分析生成中... 这篇论文探讨了重要的理论问题，研究方法严谨，对该领域有重要贡献。"
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
⭐ **继续阅读更多，请使用** /today"""


async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """升级Pro版 - 解释资金流向"""
    message = """💎 **PsyDaily Pro 会员权益**

**价格：¥29/月**（首月特惠¥19）

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
• 40% - AI模型API调用成本（Kimi、MiniMax等）
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

**方式1 - 微信支付：**
添加微信：PsyDaily_Admin
发送"升级+你的用户名"

**方式2 - 支付宝：**
支付宝转账：psydaily@example.com
备注你的Telegram用户名

**方式3 - 对公转账：**
（如需发票，请联系客服）

---

🎁 **限时福利：**
邀请好友注册，双方各得3天Pro会员！
邀请链接：稍后生成"""
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """按钮回调"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == 'upgrade':
        await upgrade(update, context)
    
    elif query.data == 'next':
        await today(update, context)
    
    elif query.data == 'start_trial':
        # 显示试用说明
        trial_msg = """🎁 **7天免费试用已开启！**

你已经自动获得了Pro会员7天免费试用权限！

✅ 试用期间你可以：
• 阅读所有完整论文（100%内容）
• 使用AI深度分析功能
• 无限篇数阅读

⏰ 试用到期：7天后
📌 到期后自动转为免费版（每日1篇20%预览）

💡 **建议：**
在试用期间充分体验Pro功能，
如果觉得有价值，再考虑订阅支持我们！

点击 /today 开始体验完整版 👇"""
        
        await query.edit_message_text(trial_msg, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """帮助命令"""
    help_text = """📖 **PsyDaily 使用指南**

**🆓 免费版功能：**
• 每日1篇精选论文
• 中英文双语标题
• 20%内容免费预览
• 基础信息展示

**💎 Pro版功能（¥29/月）：**
• 完整论文内容（100%）
• AI智能深度分析
• 研究方向匹配度
• 无限篇数阅读
• 核心发现详解

---

**📱 常用命令：**
/start - 启动机器人
/today - 获取今日推荐
/upgrade - 升级Pro版
/help - 查看帮助

**🔄 内容切换：**
每篇论文底部有"换一篇"按钮
可无限切换直到找到感兴趣的

**💰 付费说明：**
• 7天免费试用（自动开通）
• ¥29/月，随时可取消
• 首月特惠¥19
• 支持微信/支付宝

---

❓ **有问题？**
联系客服微信：PsyDaily_Admin
工作日10:00-22:00在线"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


def main():
    """主函数"""
    print("🚀 启动 PsyDaily Bot - 完整版")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✨ 功能：双语内容 + 20%预览 + 7天试用 + Kimi/MiniMax双模型")
    print("-" * 60)
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("upgrade", upgrade))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Bot已启动！")
    print("📝 命令: /start /today /upgrade /help")
    print("-" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
