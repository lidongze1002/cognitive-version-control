# v0.1.1 — Tests, English docs, and a clearer spec

第二个公开版本。不改变核心思想，补齐工程与文档。

## 新增

- **25 个单元测试**（`tests/`）：指标、输入校验、Markdown 链接
- **英文 README**（`README.en.md`）
- **FAQ**（`docs/faq.md`）：原创性、和 RAG 的区别、是否商用
- **正例**（`examples/good-revision.md`）：同一轮完成修订
- **英文重置协议**（`prompts/en/00-reset-protocol.md`）
- **Issue / PR 模板**
- **评估样例数据**（`eval/sample_data.json`）

## 改进

- 指标脚本加入输入校验、重复修订去重、孤儿修订诊断
- 新增 `--version`、`--demo-good`、`--markdown`
- SPEC 增加版本策略、评估协议、限制与失败模式
- CI 现在跑测试并校验样例数据

## 指标

| 指标 | 坏例 | 好例 |
|---|---|---|
| `concept_reuse_rate` | 0.60 | 0.33 |
| `frame_entropy` | 0.88 | 0.96 |
| `belief_revision_latency` | 4.0 | 1.0 |

## 许可

- 文档与 prompt：CC BY 4.0
- 代码：MIT
