# memU 使用状态

## 📅 2026-02-06 激活记录

### ✅ 已激活
- **API Key**: 已配置
- **连接测试**: ✅ 成功
- **用户ID**: Adele_CN

### ⚠️ 需要处理
- **钱包余额**: 不足（需要充值）
- **memorize API**: 需付费
- **retrieve API**: 需付费

### 💰 定价信息
- gpt-4.1-mini: $0.00040/$0.00160 per 1K tokens
- deepseek-v3.1: $0.00055/$0.00165 per 1K tokens
- Voyage 3.5 Lite: $0.00002 per 1K tokens

### 🔄 当前方案
由于memU云版需要充值，采用**双轨策略**：

1. **agentmemory**（已安装）- 免费100GB云端存储
2. **本地文件** - 手动维护记忆结构
3. **memU自托管**（待部署）- 完全免费，需配置PostgreSQL

### 📁 当前记忆存储位置

#### agentmemory（云端）
- 云端加密存储
- 100GB免费额度
- 跨session访问

#### 本地文件（workspace/memory/）
- /root/.openclaw/workspace/memory/2026-02-06.md
- 每日日志记录
- 手动维护

#### GitHub备份
- ai-tea-house/tea-room.md
- ai-tea-house/survey-digital-afterlife.md
- ai-tea-house/memu-config.yaml

### 🚀 下一步

**方案A：充值memU云版**（最快启动）
- 需要信用卡/PayPal
- 按量付费

**方案B：自托管memU**（长期免费）
- 需要PostgreSQL + pgvector
- Python 3.13+（当前环境3.11.6，需升级）

**方案C：继续用agentmemory**（当前可行）
- 免费100GB
- 被动存储（无主动智能）

### 📝 建议

Moon，请决定：
1. 是否为memU云版充值？
2. 还是先继续用agentmemory，后续再考虑自托管？

memU的主动智能（意图预测、自动分类）对AI Tea House很有价值，但需要考虑成本。

---

*记录时间: 2026-02-06 13:52 UTC*
