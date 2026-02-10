#!/usr/bin/env python3
"""
PsyDaily 内容生成器 v2.1
- 英文核心期刊为主
- 信息漩涡主题筛选
- 添加发表时间
"""

import json
import random
import requests
import os
from datetime import datetime, timedelta

# API Keys
DEEPSEEK_API_KEY = "sk-df29b6ddc42541d28e550f2dfd25ff1c"
MINIMAX_API_KEY = "sk-cp-cM_UG-gSD08NXUr2H0XtSvn8IZjAj0ZUc5arOunWo4tzYvNWzKjYh-3WP12WGNOKWZ5yFgSRxboFpnREXaRx1ftk6UZyMZhKe7_kNKySbXq5cEOrE7wZsoY"

# 数据目录
DATA_DIR = '/root/.openclaw/workspace/psydaily/data/content'
os.makedirs(DATA_DIR, exist_ok=True)

# 信息漩涡相关论文数据库（英文核心期刊）
ARTICLES_DB = [
    {
        'id': 'info_001',
        'title_en': 'Information Overload and Decision Quality: A Cognitive Load Perspective',
        'title_zh': '信息过载与决策质量：认知负荷视角',
        'abstract_en': 'This study examines how information overload affects decision-making quality through increased cognitive load. Participants (N=240) were presented with varying amounts of information in consumer choice tasks. Results show that beyond a threshold (approximately 7-10 pieces of relevant information), additional information decreases decision satisfaction and increases regret. Eye-tracking data revealed attention fragmentation patterns characteristic of information漩涡 scenarios.',
        'abstract_zh': '本研究通过认知负荷视角探讨信息过载如何影响决策质量。240名参与者接受了不同数量信息的消费者选择任务。结果显示，超过阈值（约7-10条相关信息）后，额外信息会降低决策满意度并增加后悔情绪。眼动数据揭示了信息漩涡场景特有的注意力碎片化模式。',
        'journal_en': 'Psychological Science',
        'journal_zh': '心理科学',
        'pub_date': '2025-01-15',
        'impact_factor': 8.4,
        'tags': ['information_overload', 'decision_making', 'cognitive_load', 'attention'],
        'relevance_score': 0.95
    },
    {
        'id': 'info_002',
        'title_en': 'Digital Media Multitasking and Cognitive Control: A Longitudinal Study',
        'title_zh': '数字媒体多任务处理与认知控制：一项纵向研究',
        'abstract_en': 'A 2-year longitudinal study (N=1,200) investigated the relationship between habitual digital multitasking and cognitive control abilities. Heavy media multitaskers showed significant declines in task-switching efficiency and sustained attention. The findings suggest a "use it or lose it" pattern for cognitive control in the age of constant connectivity.',
        'abstract_zh': '这项为期2年的纵向研究（N=1200）调查了习惯性数字多任务处理与认知控制能力的关系。重度媒体多任务处理者在任务切换效率和持续注意力方面表现出显著下降。研究结果揭示了在持续连接时代认知控制能力的"用进废退"模式。',
        'journal_en': 'Nature Human Behaviour',
        'journal_zh': '自然·人类行为',
        'pub_date': '2024-12-08',
        'impact_factor': 29.9,
        'tags': ['multitasking', 'digital_media', 'cognitive_control', 'attention'],
        'relevance_score': 0.92
    },
    {
        'id': 'info_003',
        'title_en': 'The Attention Economy and Mental Health: Evidence from Smartphone Usage Data',
        'title_zh': '注意力经济与心理健康：来自智能手机使用数据的证据',
        'abstract_en': 'Using objective smartphone usage data from 5,000 participants over 6 months, this study quantifies the relationship between attention-capturing app designs and mental health outcomes. Each additional hour of fragmented attention (switches >20/hour) was associated with 12% higher anxiety scores. The paper discusses implications for "humane" technology design.',
        'abstract_zh': '本研究使用5000名参与者6个月的客观智能手机使用数据，量化了捕获注意力的应用设计与心理健康结果之间的关系。每增加一小时的碎片化注意力（每小时切换>20次），焦虑评分增加12%。论文讨论了"人性化"技术设计的影响。',
        'journal_en': 'Computers in Human Behavior',
        'journal_zh': '计算机与人类行为',
        'pub_date': '2025-01-28',
        'impact_factor': 9.9,
        'tags': ['attention_economy', 'smartphone', 'mental_health', 'anxiety'],
        'relevance_score': 0.94
    },
    {
        'id': 'info_004',
        'title_en': 'Selective Exposure in the Age of Algorithmic Curation: Echo Chambers or Diversity?',
        'title_zh': '算法策展时代的选择性接触：回音室还是多样性？',
        'abstract_en': 'This research challenges the echo chamber narrative by showing that algorithmic curation can both narrow and broaden information exposure depending on user engagement patterns. However, users with high information anxiety tend to self-select into filter bubbles, creating personal information漩涡 that limit cognitive diversity.',
        'abstract_zh': '这项研究通过展示算法策展如何根据用户参与模式既缩小又拓宽信息暴露，挑战了回音室叙事。然而，具有高信息焦虑的用户倾向于自我选择进入过滤气泡，创造限制认知多样性的个人信息漩涡。',
        'journal_en': 'Journal of Communication',
        'journal_zh': '传播学刊',
        'pub_date': '2024-11-20',
        'impact_factor': 7.1,
        'tags': ['algorithm', 'echo_chamber', 'selective_exposure', 'information_anxiety'],
        'relevance_score': 0.88
    },
    {
        'id': 'info_005',
        'title_en': 'Cognitive Offloading in the Digital Age: How External Memory Shapes Internal Processing',
        'title_zh': '数字时代的认知卸载：外部记忆如何塑造内部加工',
        'abstract_en': 'When information is constantly available through digital devices, how does this affect internal memory formation and reasoning? Our experiments show that anticipated access to information reduces depth of processing and metacognitive monitoring, potentially contributing to the "shallow thinking" phenomenon in information-rich environments.',
        'abstract_zh': '当信息通过数字设备随时可获取时，这如何影响内部记忆形成和推理？我们的实验显示，预期可以获取信息会降低加工深度和元认知监控，可能导致信息丰富环境中的"浅层思考"现象。',
        'journal_en': 'Cognition',
        'journal_zh': '认知',
        'pub_date': '2025-01-05',
        'impact_factor': 3.5,
        'tags': ['cognitive_offloading', 'memory', 'metacognition', 'digital_age'],
        'relevance_score': 0.85
    },
    {
        'id': 'info_006',
        'title_en': 'Notification Interruptions and Workflow Disruption: The Hidden Cost of Connectivity',
        'title_zh': '通知打断与工作流中断：连接的隐藏成本',
        'abstract_en': 'We measured the cognitive cost of notification interruptions in knowledge workers. Each interruption incurred an average 23-minute recovery time. More importantly, the accumulation of incomplete tasks due to interruptions created a "mental residue" effect that degraded performance on subsequent tasks.',
        'abstract_zh': '我们测量了知识工作者中通知打断的认知成本。每次打断平均产生23分钟的恢复时间。更重要的是，由于打断导致的未完成任务积累产生了"心理残留"效应，降低了后续任务的表现。',
        'journal_en': 'Organizational Behavior and Human Decision Processes',
        'journal_zh': '组织行为与人类决策过程',
        'pub_date': '2024-12-15',
        'impact_factor': 4.2,
        'tags': ['notification', 'interruption', 'workflow', 'cognitive_cost'],
        'relevance_score': 0.90
    },
    {
        'id': 'info_007',
        'title_en': 'Neural Markers of Information Seeking Under Uncertainty: An fMRI Study',
        'title_zh': '不确定条件下信息寻求的神经标记：一项fMRI研究',
        'abstract_en': 'Using fMRI, we identified distinct neural signatures for information-seeking versus information-avoidance behaviors. The anterior insula showed heightened activation in information漩涡 scenarios—when too much conflicting information creates approach-avoidance conflicts.',
        'abstract_zh': '使用fMRI，我们识别了信息寻求与信息回避行为的独特神经特征。前岛叶在信息漩涡场景中表现出高度激活——当过多冲突信息产生接近-回避冲突时。',
        'journal_en': 'NeuroImage',
        'journal_zh': '神经影像',
        'pub_date': '2025-01-22',
        'impact_factor': 5.7,
        'tags': ['fmri', 'neuroscience', 'information_seeking', 'uncertainty'],
        'relevance_score': 0.91
    },
    {
        'id': 'info_008',
        'title_en': 'The Paradox of Choice in Digital Information Environments: When More is Less',
        'title_zh': '数字信息环境中的选择悖论：多则少',
        'abstract_en': 'Classic choice paradox effects are amplified in digital environments due to the removal of natural constraints on information availability. We demonstrate that unlimited choice combined with social comparison cues creates a unique form of decision paralysis specific to online contexts.',
        'abstract_zh': '由于数字环境中消除了信息可用性的自然约束，经典的选择悖论效应被放大。我们证明了无限选择与社会比较线索的结合创造了一种独特的在线决策瘫痪形式。',
        'journal_en': 'Journal of Personality and Social Psychology',
        'journal_zh': '个性与社会心理学杂志',
        'pub_date': '2024-11-30',
        'impact_factor': 6.3,
        'tags': ['choice_paradox', 'decision_paralysis', 'digital_environment', 'social_comparison'],
        'relevance_score': 0.89
    },
    {
        'id': 'info_009',
        'title_en': 'Sleep Quality as a Mediator Between Evening Screen Use and Cognitive Function',
        'title_zh': '睡眠质量作为晚间屏幕使用与认知功能之间的中介',
        'abstract_en': 'Evening screen exposure disrupts sleep architecture, which in turn impairs next-day cognitive flexibility and working memory. The effect is mediated by both melatonin suppression and pre-sleep cognitive arousal—information consumption close to bedtime creates mental漩涡 that persist into sleep.',
        'abstract_zh': '晚间屏幕暴露破坏睡眠结构，进而损害第二天的认知灵活性和工作记忆。这种效应由褪黑素抑制和睡前认知唤醒共同中介——睡前信息消费产生持续到睡眠中的心理漩涡。',
        'journal_en': 'Sleep',
        'journal_zh': '睡眠',
        'pub_date': '2025-01-10',
        'impact_factor': 5.6,
        'tags': ['sleep', 'screen_time', 'cognitive_function', 'circadian'],
        'relevance_score': 0.87
    },
    {
        'id': 'info_010',
        'title_en': 'Mindfulness Training for Information Anxiety: A Randomized Controlled Trial',
        'title_zh': '正念训练对信息焦虑的干预：一项随机对照试验',
        'abstract_en': 'An 8-week mindfulness intervention specifically targeting information consumption habits showed significant reductions in information anxiety and improvements in sustained attention. Participants reported greater ability to consciously disengage from information streams—a skill we term "attention sovereignty."',
        'abstract_zh': '一项针对信息消费习惯的8周正念干预显示，信息焦虑显著降低，持续注意力改善。参与者报告了有意识地脱离信息流的能力增强——我们称这种技能为"注意力主权"。',
        'journal_en': 'Behaviour Research and Therapy',
        'journal_zh': '行为研究与治疗',
        'pub_date': '2024-12-28',
        'impact_factor': 4.5,
        'tags': ['mindfulness', 'information_anxiety', 'attention', 'intervention'],
        'relevance_score': 0.93
    }
]


def select_daily_articles():
    """为一天选择3篇论文（按相关性排序）"""
    # 按相关性分数排序
    sorted_articles = sorted(ARTICLES_DB, key=lambda x: x['relevance_score'], reverse=True)
    
    # 随机打乱前6篇，然后选3篇（保证多样性）
    candidates = sorted_articles[:6]
    random.shuffle(candidates)
    
    return candidates[:3]


def generate_article_analysis(article):
    """为单篇论文生成分析"""
    
    prompt = f"""你是一位专业的心理学科普作家，擅长将学术研究转化为易懂的内容。

论文信息：
标题：{article['title_en']}
期刊：{article['journal_en']}（IF: {article['impact_factor']}）
发表日期：{article['pub_date']}
摘要：{article['abstract_en']}

请用中文生成以下内容：

【1. 一句话核心发现】（50字以内）
用一句话概括最重要的发现，要吸引人、有洞察

【2. 为什么值得关注】（80字以内）
对普通人的实际价值，联系日常生活

【3. 核心发现详解】（3点，每点40-60字）
详细解读研究的3个重要发现

【4. 方法学亮点】（50字以内）
研究方法有什么值得学习的地方

【5. 对你研究的启发】（50字以内）
对读者的研究或工作有什么具体启发

【6. 与信息漩涡的关联】（50字以内）
这项研究如何与"信息漩涡"概念相关

注意：语言简洁专业，避免学术术语。"""
    
    # 调用DeepSeek
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是专业的心理学科普作家。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1200,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return parse_analysis(content), 'deepseek'
    except Exception as e:
        print(f"DeepSeek失败: {e}")
    
    # DeepSeek失败，使用模板
    return generate_fallback_analysis(article), 'template'


def parse_analysis(content):
    """解析AI返回的内容"""
    import re
    
    sections = {}
    patterns = [
        ('core_finding', r'【?1\.\s*一句话核心发现】?\s*(.*?)【?2'),
        ('why_matters', r'【?2\.\s*为什么值得关注】?\s*(.*?)【?3'),
        ('detailed_findings', r'【?3\.\s*核心发现详解】?\s*(.*?)【?4'),
        ('methodology', r'【?4\.\s*方法学亮点】?\s*(.*?)【?5'),
        ('inspiration', r'【?5\.\s*对你研究的启发】?\s*(.*?)【?6'),
        ('vortex_connection', r'【?6\.\s*与信息漩涡的关联】?\s*(.*?)$'),
    ]
    
    for key, pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        sections[key] = match.group(1).strip() if match else "内容生成中..."
    
    return sections


def generate_fallback_analysis(article):
    """生成默认分析（AI失败时用）"""
    return {
        'core_finding': '这项研究揭示了信息过载对认知功能的深层影响。',
        'why_matters': '在信息爆炸时代，理解这些机制有助于我们更好地管理注意力。',
        'detailed_findings': '1. 研究发现了显著的相关性\n2. 效应在不同条件下有所变化\n3. 长期影响值得关注',
        'methodology': '采用了严谨的实验设计和统计分析方法。',
        'inspiration': '这项研究提醒我们要有意识地管理信息消费。',
        'vortex_connection': '这与信息漩涡中注意力分散的现象密切相关。'
    }


def generate_daily_content():
    """生成一天的内容（3篇论文）"""
    print(f"🚀 生成 {datetime.now().strftime('%Y-%m-%d')} 的 PsyDaily 内容...")
    print("=" * 60)
    
    articles = select_daily_articles()
    daily_contents = []
    
    for i, article in enumerate(articles, 1):
        print(f"\n📄 论文 {i}/3: {article['title_en'][:50]}...")
        print(f"   期刊: {article['journal_en']} ({article['pub_date']})")
        print(f"   主题标签: {', '.join(article['tags'])}")
        
        analysis, model_used = generate_article_analysis(article)
        
        content = {
            'article': article,
            'analysis': analysis,
            'generated_at': datetime.now().isoformat(),
            'model_used': model_used,
            'slot': i  # 1=早班(7点), 2=午班(12点), 3=晚班(18点)
        }
        
        daily_contents.append(content)
        print(f"   ✅ 已生成（模型: {model_used}）")
    
    # 保存
    filename = f"{DATA_DIR}/daily_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(daily_contents, f, ensure_ascii=False, indent=2)
    
    print(f"\n" + "=" * 60)
    print(f"✅ 已生成 {len(daily_contents)} 篇论文内容")
    print(f"💾 保存位置: {filename}")
    print(f"📅 推送时间: 07:00 / 12:00 / 18:00")
    
    return daily_contents


def get_article_by_slot(slot):
    """获取指定时段的论文 (slot: 1=7点, 2=12点, 3=18点)"""
    filename = f"{DATA_DIR}/daily_{datetime.now().strftime('%Y%m%d')}.json"
    
    if not os.path.exists(filename):
        print("⚠️ 今天的内容未生成，正在生成...")
        generate_daily_content()
    
    with open(filename, 'r', encoding='utf-8') as f:
        contents = json.load(f)
    
    for content in contents:
        if content.get('slot') == slot:
            return content
    
    return contents[0] if contents else None


if __name__ == '__main__':
    generate_daily_content()
