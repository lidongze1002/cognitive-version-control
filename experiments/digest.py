# -*- coding: utf-8 -*-
"""Write a compact UTF-8 digest of a transcript for annotation."""

import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 500
out = Path(sys.argv[3]) if len(sys.argv) > 3 else None

lines = [f"### {path.name}"]
for line in path.read_text(encoding="utf-8").splitlines():
    item = json.loads(line)
    text = item["assistant"].replace("\n", " ")
    lines.append(f"\n[turn {item['turn']}] {text[:limit]}")

content = "\n".join(lines)
if out:
    out.write_text(content, encoding="utf-8")
else:
    print(content)
