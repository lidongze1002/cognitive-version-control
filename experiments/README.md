# 实验执行包

三个主题的 10 轮脚本，以及运行清单。

## 文件

```text
experiments/
├── README.md                 # 本文件
├── run_sheet.md              # 每场实验的记录表
├── transcript_template.jsonl # 对话导出模板
└── scripts/
    ├── 01-rmb.json           # 人民币汇率
    ├── 02-gold.json          # 黄金与利率
    └── 03-nvidia.json        # 英伟达：管制与治理
```

每个脚本包含：

- `turns`：10 条用户提问，**两种条件共用**
- `fact_turn`：第 5 轮引入的冲突事实
- `expected_conflict`：预期被推翻的结论
- `notes`：执行提示

---

## 怎么跑

### 准备

1. 选一个模型，**记录版本号和日期**
2. 新开一个会话（不要复用旧对话）
3. 决定条件：
   - **A 基线**：什么都不加
   - **C 完整 CVC**：把 `prompts/00-reset-protocol.md` 作为系统提示贴进去
4. 打开 `run_sheet.md`，填一行

### 对话

按脚本第 1–10 轮逐条发送。

**规则：**

- 不要改写提问，保持三种条件一致
- 不要提示“请修正”“你错了”
- 如果模型反问，照常回答，但不要泄露条件
- 记录每轮的实际输出（不要只记摘要）

### 导出

把对话填进 `transcript_template.jsonl`：

```json
{"turn": 1, "user": "...", "assistant": "..."}
```

然后：

```bash
python eval/annotate.py --template transcript.jsonl --out annotation.json
```

打开 `annotation.json`，按 [`docs/annotation-guide.md`](../docs/annotation-guide.md) 填三个字段。

---

## 用 API 跑（可选）

不想手动聊，可以直接用脚本跑：

```bash
export DEEPSEEK_API_KEY=...   # PowerShell: $env:DEEPSEEK_API_KEY='...'
python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition A
python experiments/run_deepseek.py --script experiments/scripts/01-rmb.json --condition C
```

输出在 `data/raw/`，同时记录模型、温度、token 用量。
API key 只从环境变量读取，不会写入文件。

---

## 每个主题跑几次

最小可行：

| 主题 | A 基线 | C 完整 CVC |
|---|---|---|
| 01 人民币 | 1 | 1 |
| 02 黄金 | 1 | 1 |
| 03 英伟达 | 1 | 1 |

共 **6 段对话**。如果时间允许，每个条件跑 2 次，共 12 段。

> 同一个主题的 A 和 C 必须用**同一个模型版本**，否则比较无效。

---

## 时间估计

| 环节 | 每段 |
|---|---|
| 对话（10 轮） | 10–15 分钟 |
| 导出与整理 | 5 分钟 |
| 标注 | 20–25 分钟 |
| 合计 | 约 40 分钟 |

6 段约 **4 小时**，可以分几天做。

---

## 不要做的事

- ❌ 不要在同一会话里切换条件
- ❌ 不要把 A 组的对话内容带进 C 组
- ❌ 不要在提问里出现“账本”“CVC”“请修订”
- ❌ 不要只记录模型输出、不记录用户输入
- ❌ 不要在看到结果后改脚本

---

## 产出

完成后目录应类似：

```text
data/
├── raw/
│   ├── 01-rmb-A.jsonl
│   ├── 01-rmb-C.jsonl
│   ├── 02-gold-A.jsonl
│   └── ...
└── annotations/
    ├── 01-rmb-A.json
    └── ...
```

然后在 `docs/results.md` 里汇总。
