# Skill搜索报告
## 论文写作 & 画画相关技能

---

## 📚 论文写作相关技能

### 已尝试安装（未找到）
- academic-paper-writing ❌
- research-assistant ❌
- content-writer ❌
- writing-tools ❌
- markdown-writer ❌

### 现有可替代方案

**1. 已安装的技能可辅助论文写作：**

| 已安装技能 | 论文写作用途 |
|-----------|------------|
| **exa-web-search-free** | 文献搜索、资料收集 |
| **browser-automation** | 自动下载文献、网页抓取 |
| **moltbook-interact** | 与学术社区交流、获取反馈 |

**2. 可能需要手动创建的技能：**
由于没找到专门的学术写作skill，建议创建以下本地skill：

```
skills/
├── academic-writing/
│   └── SKILL.md - 理论型论文写作指南
├── literature-review/
│   └── SKILL.md - 文献综述助手
└── paper-structure/
    └── SKILL.md - 论文结构分析
```

---

## 🎨 画画/图像生成相关技能

### 已尝试安装（未找到）
- image-generator ❌
- comfy-ai ❌
- svg-art ❌
- ascii-art ❌
- image-gen ❌
- diagram ❌

### 替代方案

**1. 使用现有工具**
- 我已有的 **artifacts-builder** skill（如果安装）可生成HTML可视化
- **SVG代码手动编写** - 我可以直接写SVG代码画猫咪

**2. 创建简单的猫咪SVG**
不需要skill，我可以直接生成：

```svg
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- 猫咪身体 -->
  <ellipse cx="100" cy="120" rx="60" ry="50" fill="#FFA500"/>
  <!-- 猫咪头 -->
  <circle cx="100" cy="70" r="40" fill="#FFA500"/>
  <!-- 耳朵 -->
  <polygon points="70,50 60,20 90,40" fill="#FFA500"/>
  <polygon points="130,50 140,20 110,40" fill="#FFA500"/>
  <!-- 眼睛 -->
  <circle cx="85" cy="65" r="5" fill="#000"/>
  <circle cx="115" cy="65" r="5" fill="#000"/>
  <!-- 鼻子 -->
  <polygon points="100,75 95,85 105,85" fill="#FFC0CB"/>
  <!-- 嘴巴 -->
  <path d="M 100 85 Q 90 95 85 90" stroke="#000" fill="none"/>
  <path d="M 100 85 Q 110 95 115 90" stroke="#000" fill="none"/>
</svg>
```

---

## 💡 建议方案

### 论文写作
**当前可行路径：**
1. 使用已安装的 **exa-web-search-free** 做文献搜索
2. 使用 **browser-automation** 自动化资料收集
3. 我可以直接基于58篇文献帮你完成论文写作（不需要额外skill）

**如需更系统的支持，可以：**
- 创建一个本地 `academic-writing` skill，包含理论型论文写作框架
- 或直接在SOUL.md中添加论文写作指南

### 画猫咪
**最简单方案：**
- 我直接为你生成SVG/ASCII艺术猫咪
- 不需要额外skill

**如需复杂图像：**
- 可以使用在线AI绘画工具（如Midjourney、Stable Diffusion）
- 或使用ComfyUI（需要本地部署）

---

## ✅ 已安装技能回顾

当前已安装且对论文和茶室有帮助的skill：

| Skill | 用途 |
|-------|------|
| moltbook-interact | Moltbook运营、AI社交 |
| exa-web-search-free | 文献搜索、资料收集 |
| browser-automation | 网页自动化、资料抓取 |
| agentmemory | 云端记忆存储 |

---

*报告时间: 2026-02-06*
