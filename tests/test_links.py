# -*- coding: utf-8 -*-
"""Check that relative Markdown links point to files that exist."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def markdown_files():
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        yield path


def relative_links(text):
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith(SKIP_PREFIXES):
            continue
        target = target.split("#", 1)[0]
        if target:
            yield target


class LinkTest(unittest.TestCase):
    def test_relative_links_exist(self):
        missing = []
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            for target in relative_links(text):
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(missing, [], "\n".join(missing))

    def test_every_markdown_has_a_title(self):
        missing = []
        for path in markdown_files():
            first = path.read_text(encoding="utf-8").splitlines()[0:1]
            if not first or not first[0].startswith("#"):
                missing.append(str(path.relative_to(ROOT)))
        self.assertEqual(missing, [], "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
