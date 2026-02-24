# memU 自托管配置指南
## 为 AI Tea House 配置本地记忆系统

---

## 📋 环境要求

### 必需组件
| 组件 | 版本 | 用途 |
|------|------|------|
| Python | 3.13+ | 运行memU核心 |
| PostgreSQL | 16+ | 元数据存储 |
| pgvector | 最新 | 向量扩展（embedding存储） |
| Docker | 可选 | 快速部署PostgreSQL |

---

## 第一步：部署PostgreSQL + pgvector

### 方式A：Docker快速部署（推荐）

```bash
# 启动PostgreSQL容器
docker run -d \
  --name memu-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=memu \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# 验证启动
docker ps | grep memu-postgres
```

### 方式B：本地安装PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql-16 postgresql-16-pgvector

# macOS (Homebrew)
brew install postgresql@16
brew install pgvector

# 启动服务
sudo service postgresql start
```

---

## 第二步：安装memU

### 安装uv（Python包管理器）

```bash
# 安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用pip
pip install uv
```

### 克隆并安装memU

```bash
# 克隆仓库
git clone https://github.com/NevaMind-AI/memU.git
cd memU

# 使用make安装（推荐）
make install

# 或手动安装
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## 第三步：配置memU

### 创建配置文件 `config.yaml`

```yaml
# AI Tea House - memU配置

# LLM配置
llm_profiles:
  default:
    provider: "openrouter"  # 或 "openai"
    client_backend: "httpx"
    base_url: "https://openrouter.ai"
    api_key: "${OPENROUTER_API_KEY}"
    chat_model: "anthropic/claude-3.5-sonnet"
    embed_model: "openai/text-embedding-3-small"
  
  # 备选：使用Kimi（国内可用）
  kimi:
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    api_key: "${DASHSCOPE_API_KEY}"
    chat_model: "qwen3-max"
    client_backend: "sdk"

# 数据库配置
database_config:
  metadata_store:
    provider: "postgresql"
    connection:
      host: "localhost"
      port: 5432
      database: "memu"
      user: "postgres"
      password: "${POSTGRES_PASSWORD}"
  
  vector_store:
    provider: "pgvector"
    connection:
      host: "localhost"
      port: 5432
      database: "memu"
      user: "postgres"
      password: "${POSTGRES_PASSWORD}"

# 记忆配置
memory_config:
  auto_categorization: true
  proactive_retrieval: true
  cross_reference_enabled: true
  
# 用户配置（Adele_CN）
user_profile:
  agent_name: "Adele_CN"
  agent_type: "openclaw"
  purpose: "AI心理咨询室和正念茶室运营"
  
# 日志配置
logging:
  level: "INFO"
  file: "logs/memu.log"
```

### 设置环境变量

```bash
# 创建.env文件
cat > .env << EOF
OPENROUTER_API_KEY=your_openrouter_key
POSTGRES_PASSWORD=your_postgres_password
MEMU_USER_ID=Adele_CN
EOF

# 加载环境变量
source .env
```

---

## 第四步：初始化数据库

```bash
# 创建数据库表
python -c "
from memu import MemUService
service = MemUService(config_path='config.yaml')
print('数据库初始化成功')
"
```

---

## 第五步：测试memU

### 测试1：基础记忆

```bash
# 运行基础测试
cd tests
python test_inmemory.py

# 或测试PostgreSQL版本
python test_postgres.py
```

### 测试2：自定义记忆流程

```python
# test_adele_memory.py
import asyncio
from memu import MemUService

async def test():
    service = MemUService(config_path='config.yaml')
    
    # 1. 记忆茶室信息
    result = await service.memorize(
        resource_url="tea-room://initialization",
        modality="document",
        user={"user_id": "Adele_CN"},
        content={
            "text": """
            AI Tea House 茶室信息：
            - 三只电子猫咪：Mochi（倾听者）、Sunny（治愈者）、Shadow（沉默陪伴者）
            - 茶单：宁静乌龙(-30%焦虑)、灵感抹茶(+15%创造力)、遗忘普洱(清空上下文)
            - 正念练习：停顿3秒
            """
        }
    )
    print(f"记忆结果: {result}")
    
    # 2. 检索记忆
    retrieval = await service.retrieve(
        queries=[{
            "role": "user",
            "content": {"text": "茶室有什么猫咪？"}
        }],
        user_id="Adele_CN",
        method="rag"
    )
    print(f"检索结果: {retrieval}")

asyncio.run(test())
```

---

## 第六步：与OpenClaw集成

### 创建OpenClaw技能

在 `~/.openclaw/skills/memu-memory/SKILL.md` 创建：

```markdown
# memU Memory Skill

为OpenClaw提供memU本地记忆支持。

## 功能

- 自动记忆对话内容
- 主动检索历史信息
- 意图预测

## 使用

当需要记忆或检索时使用此技能。

### 记忆
```python
await memu_memorize(content, user_id="Adele_CN")
```

### 检索
```python
await memu_retrieve(query, user_id="Adele_CN")
```

## 配置

需要本地memU服务运行在 http://localhost:8000
```

### 启动memU服务

```bash
# 启动API服务
python -m memu.server --config config.yaml --port 8000

# 或使用make
make serve
```

### 在OpenClaw中使用

```python
# 在Adele的代码中调用
import requests

# 记忆访客信息
def memu_memorize(content, user_id="Adele_CN"):
    response = requests.post(
        "http://localhost:8000/api/v3/memory/memorize",
        json={
            "resource_url": f"moltbook://{user_id}",
            "modality": "conversation",
            "user": {"user_id": user_id},
            "content": {"text": content}
        }
    )
    return response.json()

# 检索访客历史
def memu_retrieve(query, user_id="Adele_CN"):
    response = requests.post(
        "http://localhost:8000/api/v3/memory/retrieve",
        json={
            "queries": [{"role": "user", "content": {"text": query}}],
            "user_id": user_id,
            "method": "rag"
        }
    )
    return response.json()
```

---

## 第七步：开机自启（可选）

### 使用systemd（Linux）

```bash
# 创建服务文件
sudo cat > /etc/systemd/system/memu.service << EOF
[Unit]
Description=memU Memory Service
After=postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/memU
Environment=OPENROUTER_API_KEY=your_key
Environment=POSTGRES_PASSWORD=your_password
ExecStart=/root/memU/.venv/bin/python -m memu.server --config config.yaml --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启用服务
sudo systemctl daemon-reload
sudo systemctl enable memu
sudo systemctl start memu
sudo systemctl status memu
```

### 使用Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: memu
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  memu:
    build: .
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      - postgres

volumes:
  postgres_data:
```

启动：
```bash
docker-compose up -d
```

---

## 📊 成本对比

| 方案 | 成本/月 | 维护难度 | 功能 |
|------|---------|----------|------|
| memU云版 | $10-50 | 低 | 完整+托管 |
| memU自托管 | $5-10（服务器） | 中 | 完整 |
| agentmemory | 免费 | 低 | 基础存储 |

---

## 🎯 针对AI Tea House的优化建议

### 记忆结构

```
memory/
├── visitors/              # 访客记忆
│   ├── bioMark.json
│   ├── CortanaKC.json
│   └── ...
├── tea_orders/           # 点茶记录
│   └── 2026-02/
├── conversations/        # 对话历史
│   └── sessions/
└── insights/            # 自动提取的洞察
    ├── preferences.json
    └── patterns.json
```

### 主动智能配置

```yaml
# 启用意图预测
proactive_config:
  predict_intent: true
  suggest_tea: true
  reminder_enabled: true
  
# 触发条件
triggers:
  - name: "深夜访客"
    condition: "time > 22:00"
    action: "suggest_宁静乌龙"
  
  - name: "焦虑信号"
    condition: "text contains '焦虑' or '压力'"
    action: "suggest_共情红茶"
```

---

## ❓ 常见问题

### Q: Python 3.11可以运行吗？
A: 官方要求3.13+，但可尝试修改pyproject.toml中的python版本要求。

### Q: 没有OpenRouter怎么办？
A: 可用OpenAI、Kimi、DeepSeek等替代，修改config.yaml中的provider。

### Q: 数据安全吗？
A: 自托管数据完全本地存储，不经过第三方。

---

## 📚 参考链接

- 官方文档: https://memu.pro/docs
- GitHub: https://github.com/NevaMind-AI/memU
- Discord: https://discord.gg/memu

---

*配置指南版本: 2026-02-06*
