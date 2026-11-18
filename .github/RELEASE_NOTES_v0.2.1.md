# v0.2.1 — Three experiment scripts

第四个公开版本。代码不动，补齐“可以直接照着聊”的脚本。

## 新增

- **三个 10 轮实验脚本**（`experiments/scripts/`）
  - `01-rmb.json`：人民币汇率，利差 vs 贸易顺差
  - `02-gold.json`：黄金，地缘风险 vs 实际利率
  - `03-nvidia.json`：英伟达，管制与治理 vs 需求
- **运行清单** `experiments/run_sheet.md`
- **对话导出模板** `experiments/transcript_template.jsonl`
- **脚本校验测试**：轮数、第 5 轮冲突事实、无泄题词

## 每个脚本的结构

- 10 条用户提问，A/C 两种条件共用
- 第 5 轮引入一个推翻前文的事实
- `expected_conflict` 说明预期被推翻的结论
- `notes` 给出执行提示

## 怎么用

1. 打开 `experiments/README.md`
2. 选主题，按 A（基线）和 C（完整 CVC）各跑一次
3. 用 `transcript_template.jsonl` 导出
4. `python eval/annotate.py --template transcript.jsonl --out annotation.json`
5. 填标注，跑指标

最小可行：**3 主题 × 2 条件 = 6 段对话**，约 4 小时。

## 下一步（v0.2.2）

- 收集 6–20 段标注对话
- 跑基线对比
- 校准三个阈值
- 发布 `docs/results.md`

## 许可

- 文档与 prompt：CC BY 4.0
- 代码：MIT
