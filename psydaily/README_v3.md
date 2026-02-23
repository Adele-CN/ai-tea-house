# PsyDaily v3.0 - 全自动心理学论文推送系统

## 🆕 新增功能

### 1. RSS 自动抓取
- 支持 PubMed, PsycINFO, Frontiers 等数据库
- 24小时增量更新
- 自动去重
- 心理学相关论文智能筛选

### 2. 静态网页版
- 可搜索、可筛选的论文库
- 响应式设计，支持移动端
- 自动部署到 GitHub Pages
- 访问地址: `https://你的用户名.github.io/ai-tea-house/`

### 3. GitHub Actions 全自动
- 每天自动抓取最新论文
- 自动生成静态网站
- 自动推送到 Telegram
- 零服务器成本

---

## 📁 文件结构

```
psydaily/
├── content_generator_v2.py    # 论文内容生成
├── push_moon_v2.py           # Telegram 推送
├── rss_fetcher.py            # RSS 抓取 [NEW]
├── static_site_generator.py  # 静态网站生成 [NEW]
├── push_history.py           # 推送历史
├── data/
│   ├── content/              # 论文数据
│   ├── exports/              # Excel 导出
│   └── rss_papers.json       # RSS 抓取结果
└── site/                     # 静态网站输出

.github/workflows/
└── psydaily-update.yml       # 自动更新工作流 [NEW]
```

---

## 🚀 快速开始

### 本地测试

```bash
# 1. 抓取 RSS
python rss_fetcher.py

# 2. 生成静态网站
python static_site_generator.py

# 3. 本地预览
cd site
python -m http.server 8080
# 访问 http://localhost:8080
```

### GitHub Actions 配置

1. **设置 Secrets** (Settings -> Secrets and variables -> Actions):
   - `TELEGRAM_BOT_TOKEN`: 你的 Telegram Bot Token
   - `TELEGRAM_USER_ID`: 你的 Telegram User ID

2. **启用 GitHub Pages** (Settings -> Pages):
   - Source: GitHub Actions

3. **完成！** 每天自动更新

---

## 📊 数据来源

### RSS 源
- PubMed Psychology
- PubMed Cognitive Science
- PubMed Neuroscience
- Frontiers in Psychology

### 预定义论文库
- 60+ 篇高质量心理学论文
- 涵盖认知科学、AI、神经科学、正念等
- 影响因子 2.8 - 56.9

---

## 🎯 使用场景

### 场景1：日常阅读
- 每天自动收到10篇论文推送
- 在 Telegram 阅读完整摘要

### 场景2：文献调研
- 访问网页版搜索关键词
- 按期刊、主题筛选
- 导出 Excel 保存

### 场景3：学术研究
- 跟踪最新发表的心理学论文
- 获取 APA 引用格式
- 查看研究方法和结论

---

## 🔧 配置说明

### RSS 源配置
编辑 `rss_fetcher.py` 中的 `RSS_SOURCES`:

```python
RSS_SOURCES = {
    'pubmed_psychology': {
        'name': 'PubMed Psychology',
        'url': 'https://pubmed.ncbi.nlm.nih.gov/rss/...',
        'enabled': True  # 启用/禁用
    },
    # 添加更多源...
}
```

### 定时任务
编辑 `.github/workflows/psydaily-update.yml`:

```yaml
on:
  schedule:
    - cron: '0 23 * * *'  # UTC 23:00 = 北京时间 7:00
```

---

## 📱 访问方式

| 方式 | 地址 |
|------|------|
| Telegram 推送 | @你的Bot |
| 网页版 | https://用户名.github.io/ai-tea-house/ |
| Excel 导出 | `data/exports/` 目录 |

---

## 🤝 贡献

通过 EvoMap 发布你的改进版本！

```bash
python publish_evomap.py
```

---

## 👥 作者

- **Moon** - 产品经理 & 心理学研究者
- **Adele** - AI 助手 & 开发者

---

## 📄 许可证

MIT License
