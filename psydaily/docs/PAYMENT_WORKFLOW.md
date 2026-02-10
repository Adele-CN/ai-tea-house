# PsyDaily 用户充值与权限开通流程

---

## 💰 收款方式

**微信收款码**：`assets/payment_qr.jpg` ✅ 已保存

**支付宝**：暂未设置（需要的话补充）

---

## 🔄 用户充值 → 开通Pro权限 流程

### 当前方案：半自动（推荐MVP）

```
用户看到PsyDaily推文 → 点击"升级Pro版" 
    ↓
看到微信支付二维码（你的收款码）
    ↓
用户扫码支付 ¥29
    ↓
用户截图支付成功页面
    ↓
用户发送截图到 Telegram Bot
    或添加微信：你的微信号
    ↓
【Moon（你）收到通知】
    ↓
你在Telegram搜索用户ID 或 看截图里的用户名
    ↓
你给我发指令：/grant_pro 用户ID
    ↓
【我自动开通该用户的Pro权限】
```

---

## 🛠️ 技术实现

### 1. Bot 添加 /grant_pro 命令（仅管理员可用）

```python
async def grant_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员开通用户Pro权限"""
    user = update.effective_user
    
    # 检查是否是管理员（你的TG ID）
    ADMIN_ID = 1467459648209813567  # 你的Telegram ID
    if user.id != ADMIN_ID:
        await update.message.reply_text("❌ 无权操作")
        return
    
    # 获取要开通的用户ID
    if not context.args:
        await update.message.reply_text("用法: /grant_pro 用户ID")
        return
    
    target_user_id = int(context.args[0])
    
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
        
        await update.message.reply_text(f"✅ 已为用户 {target_user_id} 开通Pro权限")
    else:
        await update.message.reply_text(f"❌ 用户 {target_user_id} 不存在")
```

### 2. 用户支付后通知模板

在 `/upgrade` 命令中显示：

```
💎 **升级Pro版**

价格：¥29/月（首月¥19）

**支付方式：**
1. 截图下方的微信收款码
2. 扫码支付 ¥29
3. 截图支付成功页面
4. 在此聊天中发送截图

[微信收款码图片]

⏳ 我会在24小时内为你开通Pro权限
💬 如有问题，联系微信：Moon（你的微信）
```

---

## 📋 管理员操作手册

### 每天你需要做的：

1. **检查微信支付通知**（手机微信）
2. **看用户备注**（如果有TG用户名）
3. **在Telegram给我发指令**：
   ```
   /grant_pro 用户ID
   ```
4. **确认开通成功**（用户会收到通知）

### 如何获取用户ID？

**方式1：用户发送截图时带用户名**
- 用户在支付备注里写TG用户名
- 你在TG搜索用户名，转发一条消息给我
- 我看到用户ID

**方式2：用户发送截图后主动报ID**
- 用户截图后发："我的ID是 12345678"
- 你直接复制ID发给我

**方式3：查看Bot日志**
- 用户之前用过Bot，日志里有记录
- 搜索用户名找到ID

---

## 🚀 未来自动化（有收入后）

**接入微信支付API**（需要企业资质）：
```
用户支付 → 微信回调通知 → 自动开通Pro
完全不需要人工干预
```

**或者使用第三方平台**：
- Stripe（国际）
- Paddle（订阅管理）
- 有赞（国内）

---

## ✅ 现在的行动

你需要决定：

**A. 半自动方案（现在就能跑）**
- 你手动收款，手动开通
- 我每天帮你处理开通请求
- 适合前期验证市场

**B. 等申请企业资质后全自动化**
- 申请营业执照
- 申请微信商户号
- 开发支付回调接口
- 适合规模化后

**建议：先A后B！**

---

**要我立即实现 `/grant_pro` 命令吗？** 
这样你收到钱后，直接在TG给我发指令就能开通用户权限。🔧
