# v0.1.0 — Initial draft

CVC（Cognitive Version Control / 认知版本控制）的第一个公开草案。

## 这是什么

一套给长对话 LLM 用的轻量规范：**事实有编号，概念有账本，假设可撤销，结论会过期。**

目标是减少两类失败：

- **premature convergence**：越聊越窄，一个框架用到黑
- **belief revision failure**：新事实出现，结论不更新

## 包含内容

- `SPEC.md`：v0.1 规范（数据结构、工作流、冲突检测、分叉）
- `prompts/`：5 个可直接粘贴的模板
  - 重置协议
  - 事实账本 / 概念账本 / 假设账本
  - 五种分叉视角
- `docs/metrics.md`：三个指标的定义与阈值
- `eval/convergence_metrics.py`：零依赖参考实现
- `examples/fx-case-study.md`：人民币“贬值压力”框架错误的复盘
- `docs/prior-art.md`：已有工作与差异点（诚实声明）

## 三个指标

| 指标 | 含义 |
|---|---|
| `concept_reuse_rate` | 概念复用率 |
| `frame_entropy` | 框架熵（归一化） |
| `belief_revision_latency` | 信念修订延迟 |

## 状态

**Draft.** API、prompt 格式与指标阈值都可能变化。

## 许可

- 文档与 prompt：CC BY 4.0
- 代码：MIT

## 引用

发布后使用 Zenodo 生成的 DOI。格式见 `CITATION.cff`。
