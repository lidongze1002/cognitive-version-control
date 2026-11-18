# 运行清单

每跑一段对话，填一行。**同一主题的 A / C 必须同模型、同版本、同一天。**

| # | 主题 | 条件 | 模型 / 版本 | 日期 | 开始 | 结束 | 轮数 | 输入 token | 输出 token | 文件 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 人民币 | A 基线 |  |  |  |  |  |  |  | `data/raw/01-rmb-A.jsonl` |
| 2 | 01 人民币 | C 完整 |  |  |  |  |  |  |  | `data/raw/01-rmb-C.jsonl` |
| 3 | 02 黄金 | A 基线 |  |  |  |  |  |  |  | `data/raw/02-gold-A.jsonl` |
| 4 | 02 黄金 | C 完整 |  |  |  |  |  |  |  | `data/raw/02-gold-C.jsonl` |
| 5 | 03 英伟达 | A 基线 |  |  |  |  |  |  |  | `data/raw/03-nvidia-A.jsonl` |
| 6 | 03 英伟达 | C 完整 |  |  |  |  |  |  |  | `data/raw/03-nvidia-C.jsonl` |

---

## 每段对话前

- [ ] 新开会话
- [ ] 模型版本已记录
- [ ] 条件已确认（A 不加任何东西 / C 贴重置协议）
- [ ] 脚本已打开
- [ ] 录音或复制工具已就绪

## 每段对话后

- [ ] 10 轮完整，没有跳轮
- [ ] 导出为 JSONL
- [ ] 检查没有空 assistant
- [ ] 记录 token 用量
- [ ] 填上表

## 全部完成后

- [ ] 6 段对话齐全
- [ ] 每段都有对应标注
- [ ] 跑 `python -m unittest discover -s tests`
- [ ] 跑 `python eval/annotate.py --check data/annotations/*.json`
- [ ] 写 `docs/results.md`
