# 认知版本控制 / Cognitive Version Control (CVC)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24338017.svg)](https://doi.org/10.5281/zenodo.24338017)
[![CI](https://github.com/lidongze1002/cognitive-version-control/actions/workflows/ci.yml/badge.svg)](https://github.com/lidongze1002/cognitive-version-control/actions/workflows/ci.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> 长对话真正的问题不是“记不住”，而是“**不肯改**”。

CVC 是一套给 LLM 长对话用的轻量规范：**事实有编号，概念有账本，假设可撤销，结论会过期。**

- 状态：`v0.2.3-draft`
- 文档许可：**CC BY 4.0**
- 代码许可：**MIT**
- DOI：**10.5281/zenodo.24338017**（concept DOI；每个版本另有 version DOI）
- 作者：Dongze Li（GitHub: [@lidongze1002](https://github.com/lidongze1002)）
- English: [`README.en.md`](README.en.md)

---

## 1. 它解决什么

| 失败模式 | 典型表现 | CVC 的对应机制 |
|---|---|---|
| **事实过期** | 新数据出现了，结论还是旧的 | 事实账本 + 冲突检测 |
| **概念固着** | 一个类比从第一轮用到最后一轮 | 概念账本 + 复用率上限 |
| **假设隐形** | 结论依赖的前提没人说出来 | 假设账本 |
| **单线收敛** | 越聊越窄，只剩一种视角 | 对话分叉 |
| **无法度量** | 不知道到底有没有变好 | 三个指标 |

一个真实案例见 [`examples/fx-case-study.md`](examples/fx-case-study.md)：人民币已经升到 6.66，回答却仍在沿用“贬值压力”的旧框架。

对照正例见 [`examples/good-revision.md`](examples/good-revision.md)：同一轮完成修订，并解释错在哪一步。

---

## 2. 三个账本

### 2.1 事实账本（Fact Ledger）

每条事实一条记录：

```json
{
  "id": "F-017",
  "claim": "USD/CNY ≈ 6.66",
  "as_of": "2026-11-18",
  "source": "TradingEconomics",
  "confidence": 0.9,
  "status": "active"
}
```

新事实进入时执行**冲突检测**：与旧记录矛盾 → 强制触发修订，而不是继续叠加。

### 2.2 概念账本（Concept Ledger）

记录本对话已经用过的类比、框架、关键词，并实时计算复用率。

超过阈值时，生成阶段加一条硬约束：

> 本回答不得使用以下已用框架：`利差 / 水池 / 拔河 / 磁铁`。

### 2.3 假设账本（Assumption Ledger）

把结论依赖的前提显式列出来，逐条可勾选、可推翻：

```json
{
  "id": "A-003",
  "assumption": "美联储 12 月会加息",
  "depends_on": ["F-021"],
  "status": "pending",
  "if_false": "黄金与成长股的结论需要重写"
}
```

---

## 3. 两个动作

### 3.1 分叉（Fork）

从任意一条消息开分支，指定视角（共 5 种）：

- **怀疑者**（skeptic）：只找漏洞
- **历史学家**（historian）：只给先例
- **反方**（contrarian）：必须给出相反结论
- **外行**（layman）：禁止使用术语
- **量化**（quant）：只给数字、区间和概率

不是让一条线越走越深，而是让一棵树横向展开。

### 3.2 重置（Reset）

新话题、新事实、新阶段时，用 `prompts/00-reset-protocol.md` 重新锚定，而不是在旧上下文里继续滑。

---

## 4. 三个指标

| 指标 | 含义 | 健康方向 |
|---|---|---|
| `concept_reuse_rate` | 概念复用率 | 越低越好（< 0.4） |
| `frame_entropy` | 框架熵（归一化） | 越高越好 |
| `belief_revision_latency` | 从新事实出现到结论更新的轮数 | 越低越好（≤ 1 轮） |

定义与公式见 [`docs/metrics.md`](docs/metrics.md)，可直接运行：

```bash
python eval/convergence_metrics.py --demo
```

```text
CVC metrics (v0.2.2)
-----------
turns: 5
concept_reuse_rate: 0.6
frame_entropy: 0.8805
belief_revision_latency: None
cvc_score: 0.4241
unrevised_facts: ['F-012', 'F-017']

Warnings:
- concept_reuse_rate > 0.4: fixation starting, suggest new frames.
- no revisions recorded despite introduced facts.
```

想看“健康”的样子：

```bash
python eval/convergence_metrics.py --demo-good
```

---

## 5. 快速开始

把 [`prompts/00-reset-protocol.md`](prompts/00-reset-protocol.md) 的内容贴到新会话开头即可。

更细的模板：

- [`prompts/01-fact-ledger.md`](prompts/01-fact-ledger.md)
- [`prompts/02-concept-ledger.md`](prompts/02-concept-ledger.md)
- [`prompts/03-assumption-ledger.md`](prompts/03-assumption-ledger.md)
- [`prompts/04-fork-lenses.md`](prompts/04-fork-lenses.md)
- 英文版：[`prompts/en/00-reset-protocol.md`](prompts/en/00-reset-protocol.md)

常见问题（原创性、和 RAG 的区别、是否商用）见 [`docs/faq.md`](docs/faq.md)。

### 做实验

- 标注手册：[`docs/annotation-guide.md`](docs/annotation-guide.md)
- 实验协议：[`docs/experiment.md`](docs/experiment.md)
- 标注工具：`python eval/annotate.py --template raw.jsonl --out annotation.json`
- **现成脚本**：[`experiments/scripts/`](experiments/scripts/)（人民币、黄金、英伟达，各 10 轮）
- 运行清单：[`experiments/run_sheet.md`](experiments/run_sheet.md)
- 试跑复盘（模拟数据，非证据）：[`docs/pilot-results.md`](docs/pilot-results.md)
- **第一次真实 A/C 结果**：[`docs/results.md`](docs/results.md)

---

## 6. 非目标

- **不是新模型**，不涉及训练或微调
- **不追求“永远新颖”**；需要稳定人设的场景，收敛是特性
- **不替代事实核查**；账本只能保证“可追溯”，不能保证“正确”
- **不是学术首创**；见 [`docs/prior-art.md`](docs/prior-art.md)

---

## 7. 与已有工作的关系

CVC 的零件大多已有来源：belief revision、assumption-based planning、MemGPT 式分层记忆、Revisitable Memory、Verbalized Sampling、prompt versioning 工具等。

**本项目的贡献是整合与可操作化**：

1. 把“概念复用率”和“信念修订延迟”变成一等公民指标
2. 给出“三账本 + 分叉”的可执行规范
3. 提供可直接粘贴的 prompt 与可运行的评估脚本

---

## 8. 路线图

- [x] v0.1.0：规范草案 + prompt 模板 + 指标脚本
- [x] v0.1.1：单元测试、英文文档、FAQ、issue/PR 模板
- [x] v0.2.0：标注工具、标注手册、实验协议
- [x] v0.2.1：3 个实验脚本 + 运行清单
- [x] v0.2.2：试跑 + 指标修复（修订时钟、无修订惩罚）
- [x] v0.2.3：第一次真实 A/C 对比（DeepSeek，人民币）
- [ ] v0.2.4：黄金与英伟达复现 + 第二标注者
- [ ] v0.3.0：提供多模型适配（Claude / GPT / Gemini / 开源模型）
- [ ] v0.4.0：对话分叉的参考实现（CLI）

---

## 9. 引用

```text
Li, Dongze. (2026). Cognitive Version Control: Fact, Concept, and Assumption
Ledgers for Long LLM Conversations (v0.2.3). Zenodo.
https://doi.org/10.5281/zenodo.24338017
```

BibTeX：

```bibtex
@misc{li2026cvc,
  author       = {Li, Dongze},
  title        = {Cognitive Version Control: Fact, Concept, and Assumption
                  Ledgers for Long LLM Conversations},
  year         = {2026},
  version      = {0.2.3},
  doi          = {10.5281/zenodo.24338017},
  url          = {https://doi.org/10.5281/zenodo.24338017}
}
```

格式见 [`CITATION.cff`](CITATION.cff)。

---

## 10. 许可

- 文档与 prompt：**CC BY 4.0**（见 `LICENSE`）
- 代码：**MIT**（见 `LICENSE-CODE`）

欢迎 fork、改编、商用，但请保留署名。

---

## 11. 贡献

见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。最欢迎的三类反馈：

1. **反例**：CVC 让对话变差的场景
2. **prior art**：我们漏掉的论文或工具
3. **数据**：带标注的长对话，用于校准指标阈值
