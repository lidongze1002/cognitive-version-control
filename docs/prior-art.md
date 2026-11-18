# Prior Art / 已有工作

> **重要声明**：CVC 的零件大多已有来源。本项目的贡献是**整合与可操作化**，不是单点首创。发布前请自行做一次检索，确认没有更早的同名工作。

---

## 1. 模式坍缩与多样性

- **Kirk et al. (2024)**, *Understanding the Effects of RLHF on LLM Generalisation and Diversity*.
  https://arxiv.org/abs/2310.06452
  → 首次系统证明 RLHF 会降低输出多样性。

- **Zhang et al. (2025)**, *Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity*.
  https://arxiv.org/abs/2510.01171
  → 让模型先输出“候选 + 概率”再采样，报告多样性提升 1.6–2.1 倍。

- **Janus (2022)**, *Mysteries of mode collapse*.
  https://www.alignmentforum.org/posts/t9svvNPNmFf5Qa3TA/mysteries-of-mode-collapse
  → 对 RLHF 导致熵坍缩的经典讨论。

## 2. 对话中的固着与收敛

- **Two Mechanisms of LLM Idea Convergence** (2026).
  https://arxiv.org/html/2602.20408v2
  → 研究 LLM 创意生成为何在多次会话后收敛，以及 CoT / persona 的影响。

- **Collaboration Convergence Framework (CCF)** (2026).
  https://www.mdpi.com/2071-1050/18/11/5313
  → 人机协作中的“收敛”度量框架。

## 3. 信念修订与记忆

- **Belief Revision**：Alchourrón, Gärdenfors & Makinson (1985) 的 AGM 理论。
  → 经典框架：扩张、修订、收缩。

- **Why Long Context and Retrieval Aren't Enough for Belief Revision** (2026).
  https://huggingface.co/blog/boltwave/llm-memory-belief-revision
  → 归纳四类失败：陈旧信念、干扰、过度反应、更新不足。

- **Revisitable Memory for Long-Context LLM Agents** (ICLR 2026).
  → 记忆应可回访、可修订，而不是只读。

- **MemGPT** (Packer et al., 2023).
  https://arxiv.org/abs/2310.08560
  → 分层记忆与上下文管理。

## 4. 假设与决策

- **Assumption-Based Planning** (Dewar et al., 1993).
  → 把“关键假设”显式化，并设定触发条件。

- **POMDP / Belief State**：部分可观测环境下的信念状态表示。

## 5. 版本控制与提示词管理

- Git / 版本控制思想在文档与代码中的普遍应用。
- Prompt versioning 工具：LangSmith、PromptLayer、Humanloop 等。
- 对话分叉：ChatGPT 的分支对话、代码 Agent 的 fork 机制。

## 6. 概念清单

- **Concept Inventory**：物理/工程教育中用于诊断“学生到底懂没懂”的概念清单方法。
  → CVC 的“概念账本”借用了这一思想，但对象从“人”换成了“对话”。

---

## 7. 本项目的差异点

在以上工作的基础上，CVC 试图补三块：

1. **把“概念复用率”和“信念修订延迟”定义为可计算指标**，并给出阈值。
2. **把三本账（事实 / 概念 / 假设）与分叉组合成一套可执行流程**，而不是单点技术。
3. **提供可直接粘贴的 prompt 与可运行的评估脚本**，降低使用门槛。

如果检索发现已有同名或同构工作，请开 issue 指出，我会在下一版中更正并致谢。
