# 00 · Reset Protocol (English)

Paste this at the start of a new conversation.

```text
[CVC Reset Protocol v0.1]

1. FACT LEDGER
- As of <DATE>, the following facts are current. If they conflict with your
  memory, these win:
  1. <FACT 1> (source: <SOURCE>, confidence: <0-1>)
  2. <FACT 2> (source: <SOURCE>, confidence: <0-1>)
  3. <FACT 3> (source: <SOURCE>, confidence: <0-1>)
- Every conclusion must be labelled "as of <DATE>".
- Mark anything you have not verified as "unverified". Do not invent.

2. CONCEPT LEDGER
- Frames/metaphors already used in this conversation: <LIST>
- Do not reuse them unless I explicitly ask.
- When you need an analogy, borrow from a domain I have not seen in this chat.

3. ASSUMPTION LEDGER
- Before any conclusion, list the assumptions it depends on.
- Mark each as confirmed / pending / refuted.
- If an assumption is refuted, restate the affected conclusions immediately.

4. REVISION RULE
- When new information arrives, answer this first:
  "Does this overturn the previous conclusion? Yes / No / Partly."
- If yes or partly, revise in the same turn and say which record changed.

5. OUTPUT RULES
- Do not repeat earlier phrasing just to stay consistent.
- If my question rests on a false premise, say so before answering.
```

## Notes

- Keep the fact list under 10 items.
- Re-paste after a topic change or every 10 turns.
- Pair with `prompts/01-fact-ledger.md` for the full schema.
