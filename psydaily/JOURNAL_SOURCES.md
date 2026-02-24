# PsyDaily 真实论文来源配置

## 开放获取期刊列表（可直接抓取）

### 1. PubMed / PubMed Central (PMC)
**网址**: https://pubmed.ncbi.nlm.nih.gov/
**API**: https://www.ncbi.nlm.nih.gov/home/documentation/
**特点**: 
- 免费 API
- 每日可查询 10 次/秒
- 包含 3000+ 万篇生物医学文献

**心理学相关期刊**:
- Psychological Science
- Journal of Personality and Social Psychology
- Cognitive Psychology
- NeuroImage
- Journal of Experimental Psychology
- Psychological Bulletin
- Annual Review of Psychology
- Trends in Cognitive Sciences

---

### 2. Springer Nature Open Access
**网址**: https://www.springernature.com/gp/open-research
**API**: https://dev.springernature.com/
**特点**:
- 需要 API Key（免费申请）
- 包含 Nature 系列开放获取论文

**心理学相关期刊**:
- Nature Human Behaviour
- BMC Psychology
- Psicologia: Reflexão e Crítica

---

### 3. Frontiers
**网址**: https://www.frontiersin.org/
**RSS**: 支持 RSS 订阅
**特点**:
- 全部开放获取
- 有 RSS 源，可直接抓取

**心理学相关期刊**:
- Frontiers in Psychology
- Frontiers in Psychiatry
- Frontiers in Human Neuroscience
- Frontiers in Behavioral Neuroscience

---

### 4. PLOS (Public Library of Science)
**网址**: https://plos.org/
**API**: https://api.plos.org/
**特点**:
- 完全开放获取
- 免费 API

**心理学相关期刊**:
- PLOS ONE
- PLOS Biology
- PLOS Medicine

---

### 5. Elsevier (部分 OA)
**网址**: https://www.elsevier.com/open-access
**API**: https://dev.elsevier.com/
**特点**:
- 需要 API Key
- 只有开放获取部分可用

**心理学相关期刊**:
- NeuroImage (部分 OA)
- Cognition (部分 OA)
- Computers in Human Behavior (部分 OA)

---

### 6. CrossRef (元数据)
**网址**: https://www.crossref.org/
**API**: https://api.crossref.org/
**特点**:
- 免费， polite pool 无限次
- 提供 DOI 解析和元数据查询

---

### 7. Semantic Scholar
**网址**: https://www.semanticscholar.org/
**API**: https://www.semanticscholar.org/product/api
**特点**:
- 免费 API Key
- 包含 AI 生成的 TL;DR 摘要

---

## 推荐抓取策略

### 方案 A: 多源聚合（推荐）
```
1. PubMed - 主要来源（心理学 + 认知科学 + 神经科学）
2. Frontiers - 补充最新 OA 论文
3. CrossRef - 验证和补充 DOI
```

### 方案 B: 单源深度
```
仅使用 PubMed，但配置多个查询词：
- psychology
- cognitive science
- neuroscience
- mental health
- behavioral science
```

### 方案 C: 精选期刊
```
只抓取特定期刊的最新文章：
- Nature Human Behaviour
- Psychological Science
- Trends in Cognitive Sciences
```

---

## API 限制说明

| 来源 | 频率限制 | 需要 Key | 免费额度 |
|------|----------|----------|----------|
| PubMed E-utilities | 10次/秒 | 否 | 无限制 |
| Springer | 5000次/天 | 是 | 免费 |
| CrossRef | polite pool 无限制 | 否 | 无限制 |
| Semantic Scholar | 100次/5分钟 | 是 | 免费 |
| Elsevier | 视计划而定 | 是 | 有限 |

---

## 下一步

需要我实现哪个方案？
- **方案 A**: 多源聚合（最全面）
- **方案 B**: 单源深度（最简单稳定）
- **方案 C**: 精选期刊（质量最高）
