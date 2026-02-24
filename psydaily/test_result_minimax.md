# MiniMax API 测试结果

## ✅ 连接状态
- **API Key**: 有效 ✅
- **连接**: 成功 ✅
- **状态码**: 200 ✅

## ❌ 问题
**余额不足** (`insufficient balance`)

```
status_code: 1008
status_msg: insufficient balance
```

## 🔧 解决方案

MiniMax API 需要充值才能使用：

1. **登录 MiniMax 控制台**
   - 访问: https://www.minimaxi.com/

2. **充值账户**
   - 进入"账户管理"或"Billing"
   - 充值金额（建议 ¥50-100 起步）
   - 价格: ~¥0.015/1K tokens

3. **验证余额**
   - 充值后重新运行测试脚本

## 💡 替代方案（立即使用）

在 MiniMax 充值完成前，可以先使用：

1. **DeepSeek API**（更便宜，¥0.001/1K tokens）
2. **Kimi API**（如果你有额度）
3. **OpenRouter**（聚合多个模型）

## 📊 模型价格对比

| 模型 | 价格 | 备注 |
|------|------|------|
| **MiniMax** | ¥0.015/1K tokens | 需要充值 |
| **DeepSeek** | ¥0.001/1K tokens | 更便宜 |
| **Kimi** | ¥0.012/1K tokens | 长文本强 |

---

**建议**：
1. 先申请 **DeepSeek API**（免费额度多）
2. 同时给 MiniMax 充值 ¥50
3. 我配置多模型自动切换

需要 DeepSeek 的申请链接吗？🔗
