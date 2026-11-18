# v0.2.0 — Annotation kit and experiment protocol

第三个公开版本。仍然没有“实验结果”，但把做实验所需的东西补齐了。

## 新增

- **标注工具** `eval/annotate.py`
  - `--template`：从原始 JSONL 生成空白标注文件
  - `--check`：校验并计算指标
  - `--summary`：找漏填概念的轮次
- **标注手册** `docs/annotation-guide.md`
  - 什么算概念、什么不算
  - 概念归一化规则
  - 事实编号与修订规则
  - 边界情况、常见错误、κ 一致性
- **实验协议** `docs/experiment.md`
  - RQ 与假设
  - 三条件被试内设计（基线 / 仅重置 / 完整 CVC）
  - 材料、流程、测量、统计、效度威胁
  - 最小可行版本（3 主题 × 2 条件）
- **原始对话模板** `eval/annotation_template.jsonl`
- **标注工具测试**

## 变更

- README 与 `CITATION.cff` 改用 **concept DOI**：`10.5281/zenodo.24338017`
  - v0.1.0 的 version DOI：`10.5281/zenodo.24338018`
  - v0.1.1 的 version DOI：`10.5281/zenodo.24338950`
- FAQ 增加“概念 DOI vs 版本 DOI”
- CI 增加标注工具冒烟测试

## 下一步（v0.2.1）

- 收集 20 段带标注的对话
- 跑基线（A / B / C）
- 用数据校准三个阈值
- 发布 `docs/results.md`

## 许可

- 文档与 prompt：CC BY 4.0
- 代码：MIT
