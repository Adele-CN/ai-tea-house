# PsyDaily - 心理学每日推送系统
## 项目结构

```
psydaily/
├── src/
│   ├── crawler/          # 数据抓取模块
│   ├── analyzer/         # AI分析模块
│   ├── push/            # 推送模块
│   ├── user/            # 用户管理
│   └── main.py          # 主程序
├── data/                # 数据存储
├── config/              # 配置文件
├── docs/                # 文档
└── requirements.txt     # 依赖
```

## 功能模块

### 1. 数据抓取 (crawler)
- 期刊RSS/API抓取
- 网页内容解析
- 数据清洗存储

### 2. AI分析 (analyzer)
- 文章摘要生成
- 相关性分析
- 权威性评价
- 文献对话总结

### 3. 推送 (push)
- Telegram Bot
- 微信（后续）
- 邮件（后续）

### 4. 用户 (user)
- 研究方向标签
- 订阅管理
- 付费状态

## 商业模式
- 免费版：每天1篇基础推送
- 付费版：¥29/月，无限+深度分析
