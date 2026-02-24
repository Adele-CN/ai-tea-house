# PsyDaily 多模型接入方案
## Kimi + MiniMax + DeepSeek 混合调用

---

## 🎯 设计目标

1. **主模型**：Kimi（日常使用）
2. **备用模型**：MiniMax / DeepSeek（Kimi限额时自动切换）
3. **负载均衡**：根据任务类型选择最优模型
4. **成本优化**：优先使用免费/低价额度

---

## 🏗️ 架构设计

```
用户请求
    ↓
[模型路由器] ← 检查各模型状态/额度
    ↓
┌─────────┬─────────┬─────────┐
│  Kimi   │ MiniMax │DeepSeek │
│  主模型  │ 备用1   │ 备用2   │
└─────────┴─────────┴─────────┘
    ↓
统一输出格式
```

---

## 📋 模型分工

| 任务类型 | 首选 | 备用 | 原因 |
|---------|------|------|------|
| 论文摘要 | Kimi | DeepSeek | Kimi长文本强 |
| 深度分析 | Kimi | MiniMax | Kimi学术能力强 |
| 快速响应 | DeepSeek | Kimi | DeepSeek速度快 |
| 代码相关 | DeepSeek | Kimi | DeepSeek代码强 |
| 创意写作 | MiniMax | Kimi | MiniMax生成流畅 |

---

## 💻 实现代码

```python
# multi_model_manager.py
import os
import random
from typing import Optional, Dict, Any

class MultiModelManager:
    """多模型管理器"""
    
    def __init__(self):
        # API配置（从环境变量读取）
        self.apis = {
            'kimi': {
                'key': os.getenv('KIMI_API_KEY'),
                'base_url': 'https://api.moonshot.cn/v1',
                'model': 'kimi-latest',
                'priority': 1,
                'daily_limit': 1000,  # 假设日限额
                'used_today': 0
            },
            'minimax': {
                'key': os.getenv('MINIMAX_API_KEY'),
                'base_url': 'https://api.minimax.chat/v1',
                'model': 'abab6.5-chat',
                'priority': 2,
                'daily_limit': 500,
                'used_today': 0
            },
            'deepseek': {
                'key': os.getenv('DEEPSEEK_API_KEY'),
                'base_url': 'https://api.deepseek.com/v1',
                'model': 'deepseek-chat',
                'priority': 3,
                'daily_limit': 2000,
                'used_today': 0
            }
        }
        
        self.current_model = 'kimi'
    
    def get_model(self, task_type: str = 'general') -> str:
        """
        根据任务类型选择最优模型
        
        Args:
            task_type: 任务类型 (paper_analysis/quick_response/creative/...)
        
        Returns:
            模型名称
        """
        # 任务-模型映射
        task_mapping = {
            'paper_analysis': ['kimi', 'deepseek'],  # 论文分析需要长文本
            'quick_response': ['deepseek', 'kimi'],  # 快速响应
            'creative': ['minimax', 'kimi'],         # 创意写作
            'code': ['deepseek', 'kimi'],            # 代码相关
            'general': ['kimi', 'minimax', 'deepseek']  # 默认
        }
        
        candidates = task_mapping.get(task_type, task_mapping['general'])
        
        # 选择第一个有额度的模型
        for model in candidates:
            if self._check_quota(model):
                return model
        
        # 如果都没额度，随机选一个（会报错但记录）
        return random.choice(list(self.apis.keys()))
    
    def _check_quota(self, model: str) -> bool:
        """检查模型是否还有额度"""
        api_info = self.apis.get(model, {})
        used = api_info.get('used_today', 0)
        limit = api_info.get('daily_limit', 1000)
        return used < limit
    
    def call(self, prompt: str, task_type: str = 'general', **kwargs) -> Dict[str, Any]:
        """
        统一调用接口
        
        Args:
            prompt: 提示词
            task_type: 任务类型
            **kwargs: 额外参数
        
        Returns:
            包含结果和元信息的字典
        """
        model = self.get_model(task_type)
        
        try:
            if model == 'kimi':
                result = self._call_kimi(prompt, **kwargs)
            elif model == 'minimax':
                result = self._call_minimax(prompt, **kwargs)
            elif model == 'deepseek':
                result = self._call_deepseek(prompt, **kwargs)
            else:
                raise ValueError(f"未知模型: {model}")
            
            # 更新使用统计
            self.apis[model]['used_today'] += 1
            
            return {
                'success': True,
                'model': model,
                'result': result,
                'quota_left': self.apis[model]['daily_limit'] - self.apis[model]['used_today']
            }
            
        except Exception as e:
            # 失败后尝试下一个模型
            return self._fallback_call(prompt, task_type, model, str(e))
    
    def _fallback_call(self, prompt: str, task_type: str, failed_model: str, error: str):
        """失败后的备用调用"""
        # 获取其他可用模型
        other_models = [m for m in self.apis.keys() if m != failed_model]
        
        for model in other_models:
            if self._check_quota(model):
                try:
                    result = self.call(prompt, task_type)
                    result['fallback_from'] = failed_model
                    result['fallback_reason'] = error
                    return result
                except:
                    continue
        
        return {
            'success': False,
            'error': f'所有模型都失败了。最后错误: {error}',
            'failed_models': [failed_model] + other_models
        }
    
    def _call_kimi(self, prompt: str, **kwargs):
        """调用Kimi API"""
        import openai
        client = openai.OpenAI(
            api_key=self.apis['kimi']['key'],
            base_url=self.apis['kimi']['base_url']
        )
        
        response = client.chat.completions.create(
            model=self.apis['kimi']['model'],
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def _call_minimax(self, prompt: str, **kwargs):
        """调用MiniMax API"""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.apis['minimax']['key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.apis['minimax']['model'],
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            f"{self.apis['minimax']['base_url']}/chat/completions",
            headers=headers,
            json=data
        )
        return response.json()['choices'][0]['message']['content']
    
    def _call_deepseek(self, prompt: str, **kwargs):
        """调用DeepSeek API"""
        import openai
        client = openai.OpenAI(
            api_key=self.apis['deepseek']['key'],
            base_url=self.apis['deepseek']['base_url']
        )
        
        response = client.chat.completions.create(
            model=self.apis['deepseek']['model'],
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def get_stats(self) -> Dict:
        """获取各模型使用统计"""
        return {
            model: {
                'used': info['used_today'],
                'limit': info['daily_limit'],
                'left': info['daily_limit'] - info['used_today'],
                'percent': (info['used_today'] / info['daily_limit']) * 100
            }
            for model, info in self.apis.items()
        }


# ========== 使用示例 ==========

if __name__ == '__main__':
    # 初始化管理器
    manager = MultiModelManager()
    
    # 分析论文（自动选择最优模型）
    paper_prompt = """
    请分析这篇心理学论文：
    标题：工作记忆容量与决策质量的关系
    摘要：本研究通过三个实验...
    
    请提取：
    1. 核心假设
    2. 主要发现
    3. 方法学创新
    """
    
    result = manager.call(paper_prompt, task_type='paper_analysis')
    
    if result['success']:
        print(f"使用模型: {result['model']}")
        print(f"剩余额度: {result['quota_left']}")
        print(f"分析结果:\n{result['result']}")
    else:
        print(f"错误: {result['error']}")
    
    # 查看统计
    print("\n=== 模型使用统计 ===")
    stats = manager.get_stats()
    for model, stat in stats.items():
        print(f"{model}: {stat['used']}/{stat['limit']} ({stat['percent']:.1f}%)")
```

---

## 📊 成本对比

| 模型 | 输入价格 | 输出价格 | 特点 |
|------|---------|---------|------|
| **Kimi** | ¥0.012/1K tokens | ¥0.012/1K tokens | 长文本强，学术优 |
| **MiniMax** | ¥0.015/1K tokens | ¥0.015/1K tokens | 生成流畅，创意好 |
| **DeepSeek** | ¥0.001/1K tokens | ¥0.002/1K tokens | 性价比高，代码强 |

**策略**：日常用DeepSeek（便宜），复杂分析用Kimi，创意任务用MiniMax

---

## 🔧 部署步骤

### 1. 设置环境变量
```bash
export KIMI_API_KEY="your_kimi_key"
export MINIMAX_API_KEY="your_minimax_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
```

### 2. 安装依赖
```bash
pip install openai requests
```

### 3. 集成到PsyDaily
```python
from multi_model_manager import MultiModelManager

# 在文章分析模块中使用
manager = MultiModelManager()

# 分析论文（自动路由到最优模型）
analysis = manager.call(prompt, task_type='paper_analysis')
```

---

## ✅ 你的任务

请提供以下API Key，我可以立即接入：

1. **MiniMax API Key** → 申请地址：https://www.minimaxi.com/
2. **DeepSeek API Key** → 申请地址：https://platform.deepseek.com/

提供后我会：
- [ ] 立即接入多模型管理器
- [ ] 测试各模型响应质量
- [ ] 配置自动切换策略
- [ ] 部署到PsyDaily系统

**Kimi当前已接入，等待备用模型API！** 🔑
