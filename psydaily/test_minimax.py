#!/usr/bin/env python3
"""
测试 MiniMax API 连接
"""

import os
import requests
import json

# 从环境变量读取
MINIMAX_API_KEY = "sk-cp-cM_UG-gSD08NXUr2H0XtSvn8IZjAj0ZUc5arOunWo4tzYvNWzKjYh-3WP12WGNOKWZ5yFgSRxboFpnREXaRx1ftk6UZyMZhKe7_kNKySbXq5cEOrE7wZsoY"

def test_minimax():
    """测试 MiniMax API"""
    print("🧪 测试 MiniMax API 连接...")
    print("-" * 50)
    
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "abab6.5-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的心理学科普作家。"},
            {"role": "user", "content": "请用一句话介绍心理学是什么。"}
        ],
        "max_tokens": 100
    }
    
    try:
        print("📡 发送请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            print("✅ API 连接成功！")
            print(f"\n📝 回复内容:\n{content}")
            print(f"\n📈 Token使用: {result.get('usage', {})}")
            return True
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_psychology_analysis():
    """测试心理学论文分析"""
    print("\n" + "="*50)
    print("🧠 测试心理学论文分析...")
    print("="*50)
    
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = """你是一位专业的心理学科普作家。

请分析这篇论文：
标题：工作记忆容量与决策质量的关系：基于双任务范式的实验研究
摘要：本研究通过三个实验探讨了工作记忆容量对决策质量的影响。实验1采用N-back任务测量工作记忆，实验2使用爱荷华博弈任务评估决策。

请用中文输出：
1. 一句话核心发现
2. 为什么值得关注（对心理学研究生的价值）
3. 核心发现详解（3点）
"""
    
    payload = {
        "model": "abab6.5-chat",
        "messages": [
            {"role": "system", "content": "你是PsyDaily的心理学内容创作助手，擅长将学术论文转化为易读的科普内容。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    
    try:
        print("📡 发送分析请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            print("✅ 分析完成！")
            print(f"\n📝 结果:\n{content}")
            return True
        else:
            print(f"❌ 分析失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════╗
║     MiniMax API 连接测试                 ║
╚══════════════════════════════════════════╝
    """)
    
    # 基础连接测试
    success1 = test_minimax()
    
    # 心理学分析测试
    if success1:
        success2 = test_psychology_analysis()
        
        print("\n" + "="*50)
        if success1 and success2:
            print("✅ 所有测试通过！MiniMax API 已就绪。")
        else:
            print("⚠️ 部分测试失败，请检查配置。")
        print("="*50)
    else:
        print("\n❌ API连接失败，请检查API Key。")
