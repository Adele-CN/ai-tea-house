# PsyDaily GitHub 部署指南

## 📋 前置条件

1. 代码已推送到 GitHub
2. 有 GitHub 账号
3. Telegram Bot 已创建

---

## 🔐 第一步：配置 GitHub Secrets

### 1. 获取必要信息

**Telegram Bot Token:**
- 你的 Bot Token: `8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA`

**Telegram User ID:**
```bash
# 发送 /start 给你的 Bot
# 然后访问:
https://api.telegram.org/bot8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA/getUpdates
# 找到 "chat":{"id":8309994838
```
- 你的 User ID: `8309994838`

### 2. 设置 Secrets

1. 打开 GitHub 仓库: `https://github.com/Adele-CN/ai-tea-house`
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**

添加以下 Secrets:

| Name | Value |
|------|-------|
| `TELEGRAM_BOT_TOKEN` | `8518950873:AAHy2PQSMn5F9Z0kcRzNGPUWSSBgMuoqJZA` |
| `TELEGRAM_USER_ID` | `8309994838` |

---

## 🌐 第二步：启用 GitHub Pages

1. 在仓库页面点击 **Settings**
2. 左侧菜单点击 **Pages**
3. **Source** 选择: **GitHub Actions**
4. 保存

---

## 🚀 第三步：触发部署

### 方式1：手动触发
1. 打开仓库页面
2. 点击 **Actions**
3. 选择 **PsyDaily Auto Update**
4. 点击 **Run workflow**

### 方式2：等待自动触发
- 每天北京时间 7:00 自动运行
- 或修改定时器立即触发

---

## 📁 第四步：确认文件结构

确保仓库结构如下：

```
ai-tea-house/
├── .github/
│   └── workflows/
│       └── psydaily-update.yml      ✅ 工作流文件
├── psydaily/
│   ├── rss_fetcher.py               ✅ RSS抓取
│   ├── static_site_generator.py     ✅ 网站生成
│   ├── push_moon_v2.py             ✅ Telegram推送
│   ├── content_generator_v2.py     ✅ 内容生成
│   ├── data/
│   │   ├── content/                # 论文数据
│   │   └── rss_papers.json         # RSS结果
│   └── site/                       # 网站输出
└── README.md
```

---

## ✅ 第五步：验证部署

### 检查1：Actions 运行状态
- 打开: `https://github.com/Adele-CN/ai-tea-house/actions`
- 应该看到绿色的 ✅

### 检查2：GitHub Pages 部署
- 打开: `https://Adele-CN.github.io/ai-tea-house/`
- 应该看到论文库网页

### 检查3：Telegram 推送
- 检查是否收到 Bot 消息

---

## 🐛 常见问题

### 问题1：Actions 失败
**解决:**
```bash
# 检查 Secrets 是否正确设置
# 检查文件路径是否正确
```

### 问题2：Pages 404
**解决:**
```bash
# 确认 Settings → Pages → Source 是 GitHub Actions
# 不是 Branch
```

### 问题3：Telegram 不推送
**解决:**
```bash
# 检查 TELEGRAM_BOT_TOKEN 和 TELEGRAM_USER_ID
# 确认 Bot 没有被屏蔽
```

---

## 📝 修改定时器

编辑 `.github/workflows/psydaily-update.yml`:

```yaml
on:
  schedule:
    # 每天北京时间 7:00 (UTC 23:00)
    - cron: '0 23 * * *'
    
    # 其他时间选项:
    # 每天 8:00: '0 0 * * *'
    # 每天 9:00: '0 1 * * *'
    # 每6小时: '0 */6 * * *'
```

---

## 🎉 完成！

部署成功后：
- ✅ 每天自动抓取最新论文
- ✅ 自动生成静态网站
- ✅ 自动推送到 Telegram
- ✅ 零成本全自动运行
