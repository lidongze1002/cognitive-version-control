# CVC Specification v1.0.0

> 状态：**冻结**。项目已结项（2026-11-18），规范不再变更。

> 状态：Draft
> 适用范围：任意长对话式 LLM 交互（人类用户 ↔ 模型，或 Agent ↔ Agent）

---

## 0. 术语

- **Turn（轮）**：一次用户输入 + 一次模型输出
- **Claim（断言）**：可以被证伪的事实陈述
- **Frame（框架）**：用于解释现象的一组概念、类比或模型
- **Belief Revision（信念修订）**：当新证据与旧结论冲突时，更新结论
- **Convergence（收敛）**：后续回答越来越依赖前文已出现的概念，导致多样性下降

---

## 1. 问题陈述

长对话中存在四类可观测的失败：

1. **Stale belief**：新事实已出现，结论未更新
2. **Fixation**：早期框架锁死后续思路
3. **Hidden assumption**：结论依赖的前提未显式化
4. **Single-track drift**：对话只能向前，不能横向比较

CVC 不试图消除收敛（这与自回归模型的本性冲突），而是让收敛**可控、可测、可回退**。

---

## 2. 设计原则

| 原则 | 含义 |
|---|---|
| **Traceable** | 每条事实可追溯到来源与时间 |
| **Conflict-aware** | 新事实进入时主动检测矛盾 |
| **Expirable** | 结论有有效期，过期自动降权 |
| **Forkable** | 对话可在任意节点分叉 |
| **Measurable** | 收敛程度可量化 |

---

## 3. 数据结构

### 3.1 Fact

```json
{
  "id": "F-017",
  "claim": "USD/CNY ≈ 6.66",
  "as_of": "2026-11-18",
  "source": "TradingEconomics",
  "confidence": 0.9,
  "status": "active | superseded | retracted",
  "supersedes": "F-012"
}
```

**约束**

- `id` 全局唯一，建议 `F-` + 递增编号
- `as_of` 必填；没有时间的“事实”不是事实
- `status = superseded` 时必须填写 `supersedes`
- `confidence < 0.6` 的事实不得单独支撑结论

### 3.2 Concept

```json
{
  "id": "C-004",
  "label": "利差",
  "type": "analogy | model | metaphor | keyword",
  "first_used_turn": 3,
  "uses": [3, 5, 8]
}
```

### 3.3 Assumption

```json
{
  "id": "A-003",
  "assumption": "美联储 12 月会加息",
  "depends_on": ["F-021"],
  "status": "pending | confirmed | refuted",
  "if_false": "黄金与成长股的结论需要重写"
}
```

---

## 4. 工作流

```
Ingest（接收新信息）
  ↓
Extract（抽取 claim / concept / assumption）
  ↓
Conflict Check（与账本比对）
  ↓
Revise（标记旧记录 superseded，更新假设）
  ↓
Answer（基于修订后的账本生成）
  ↓
Log（写回账本 + 指标）
```

### 4.1 冲突检测规则

满足任一条件即视为冲突：

1. 同一实体、同一指标、同一时间粒度，数值差异 > 容忍阈值
2. 方向相反（升值 vs 贬值）
3. 来源等级相同但结论相反

### 4.2 修订规则

- 不得删除旧记录，只能标记 `superseded` / `retracted`
- 修订必须在同一轮内完成，不得延迟
- 修订后必须重述受影响的结论（哪怕只是一句“此前判断作废”）

---

## 5. 分叉

### 5.1 分叉点

任意 turn 均可作为分叉点，记录：

```json
{
  "fork_id": "K-002",
  "from_turn": 12,
  "lens": "skeptic",
  "constraints": ["不得复用利差框架", "必须给出反例"]
}
```

### 5.2 内置视角

| Lens | 约束 |
|---|---|
| `skeptic` | 只找漏洞与反例 |
| `historian` | 只提供历史先例 |
| `contrarian` | 必须给出相反结论 |
| `layman` | 禁止术语，用日常语言 |
| `quant` | 必须给出数字与区间 |

---

## 6. 指标

### 6.1 `concept_reuse_rate`

```
reuse_rate = 重复出现的概念次数 / 概念总出现次数
```

健康区间：`< 0.4`。超过 `0.6` 触发“强制换框架”。

### 6.2 `frame_entropy`

对概念出现频次做归一化 Shannon 熵：

```
H = -Σ p_i log2 p_i
H_norm = H / log2(k)     # k = 不同概念数
```

健康区间：`> 0.7`。

### 6.3 `belief_revision_latency`

```
latency = 修订轮次 - 最近一次事实进入的轮次（不晚于修订轮）
```

健康区间：`≤ 1`。`2` 视为偏慢；`≥ 3` 触发“信念粘性”警告。

有事实进入但从未修订 → 记为 `None`，综合评分按 0 计；完全没有事实 → 按中性 0.5 计。

---

## 7. 非目标

- 不保证事实正确，只保证事实可追溯
- 不适用于需要强一致人设的陪伴型产品
- 不解决模型训练层面的 mode collapse

---

## 8. 合规与伦理

- 账本中不得存储个人敏感信息
- 来源必须可公开核验，或明确标注“未核实”
- 分叉视角必须标注“这是模拟视角”，不得伪装成事实

---

## 9. 版本与发布

- 采用语义化版本：`MAJOR.MINOR.PATCH`
- 规范变更（字段、工作流）→ `MINOR`
- 措辞、示例、测试 → `PATCH`
- 每次 GitHub release 由 Zenodo 生成一个 version DOI；concept DOI 指向项目整体
- 所有变更记录在 [`CHANGELOG.md`](CHANGELOG.md)

| 版本 | 日期 | 内容 |
|---|---|---|
| `v0.1.0` | 2026-11-18 | 初稿：三账本、分叉、三指标 |
| `v0.1.1` | 2026-11-18 | 测试、英文文档、FAQ、输入校验 |
| `v0.2.0` | 2026-11-18 | 标注工具、标注手册、实验协议 |
| `v0.2.1` | 2026-11-18 | 3 个实验脚本 + 运行清单 |
| `v0.2.2` | 2026-11-18 | 试跑 + 指标修复（修订时钟、无修订惩罚） |
| `v0.2.3` | 2026-11-18 | 第一次真实 A/C 对比（DeepSeek，人民币） |
| `v0.2.4` | 2026-11-18 | 三主题真实运行（人民币 / 黄金 / 英伟达）+ 修订日志 |
| `v1.0.0` | 2026-11-18 | 结项：最终报告、状态冻结、仓库归档 |

---

## 10. 评估协议

完整的实验设计见 [`docs/experiment.md`](docs/experiment.md)，标注手册见 [`docs/annotation-guide.md`](docs/annotation-guide.md)。

工具：

```bash
python eval/annotate.py --template raw.jsonl --out annotation.json
python eval/annotate.py --check annotation.json
python eval/annotate.py --summary annotation.json
```

指标阈值目前是经验值。要把它变成可复现的结论，需要：

### 10.1 标注单位

以**一轮**为单位，标注三项：

- `concepts`：本轮出现的框架/类比/关键词
- `facts_introduced`：本轮首次出现的事实编号
- `facts_revised`：本轮被标记为过期的旧事实编号

### 10.2 最小样本

- 每个场景 ≥ 20 段对话
- 每段 ≥ 10 轮
- 至少 2 名标注者，计算一致性（Cohen's κ）

### 10.3 基线

至少比较三组：

1. 普通对话（无 CVC）
2. 仅用重置协议
3. 完整 CVC（三账本 + 分叉）

### 10.4 报告

必须报告：

- 三个指标的均值与方差
- 任务质量（正确率 / 用户评分），防止“为了发散而发散”
- token 开销

---

## 11. 限制与失败模式

| 失败模式 | 表现 | 缓解 |
|---|---|---|
| **账本膨胀** | 上下文被记录挤满 | 每 10 轮压缩一次，只保留 active 记录 |
| **过度修订** | 每轮都改口，结论不稳定 | 只有“方向相反”或“数值超阈值”才触发 |
| **形式主义** | 填了账本但不影响回答 | 强制在回答中引用编号 |
| **标注成本** | 人工维护太贵 | 先自动化抽取，人工只复核冲突 |
| **被策略性利用** | 用户诱导模型忽略账本 | 账本优先级写入系统提示，不可被用户覆盖 |
| **隐私** | 账本记录敏感信息 | 默认不记录个人身份信息；支持本地部署 |

---

## 12. 变更记录

见 [`CHANGELOG.md`](CHANGELOG.md)。
