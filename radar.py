#!/usr/bin/env python3
"""req-radar — track functional vs non-functional requirements checkboxes."""
from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQ = os.path.join(HERE, "requirements.md")

ITEM = re.compile(r"^- \[( |x|X)\] (\S+): (.+)$")


def parse(path: str):
    items = []
    section = ""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("## "):
                section = line[3:].strip()
                continue
            m = ITEM.match(line.rstrip())
            if not m:
                continue
            done = m.group(1).lower() == "x"
            items.append({"section": section, "id": m.group(2), "text": m.group(3), "done": done, "raw": line})
    return items


def write(path: str, items) -> None:
    # rewrite only checkbox lines; keep file structure simple by regenerating
    functional = [i for i in items if i["section"].lower().startswith("functional")]
    nonfunc = [i for i in items if i["section"].lower().startswith("non-functional")]
    lines = ["# Sample requirements — personal notes app", "", "## Functional", ""]
    for i in functional:
        mark = "x" if i["done"] else " "
        lines.append(f"- [{mark}] {i['id']}: {i['text']}")
    lines += ["", "## Non-functional", ""]
    for i in nonfunc:
        mark = "x" if i["done"] else " "
        lines.append(f"- [{mark}] {i['id']}: {i['text']}")
    lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("status")
    d = sub.add_parser("done")
    d.add_argument("id")
    u = sub.add_parser("undo")
    u.add_argument("id")
    args = p.parse_args()
    items = parse(REQ)
    if args.cmd == "list":
        for i in items:
            mark = "x" if i["done"] else " "
            print(f"[{mark}] {i['id']:<5} {i['text']}  ({i['section']})")
        return 0
    if args.cmd == "status":
        total = len(items)
        done = sum(1 for i in items if i["done"])
        print(f"{done}/{total} complete ({(done/total*100 if total else 0):.0f}%)")
        for sec in sorted({i['section'] for i in items}):
            subset = [i for i in items if i["section"] == sec]
            d = sum(1 for i in subset if i["done"])
            print(f"  {sec}: {d}/{len(subset)}")
        return 0
    if args.cmd in ("done", "undo"):
        target = args.id.upper()
        found = False
        for i in items:
            if i["id"].upper() == target:
                i["done"] = args.cmd == "done"
                found = True
        if not found:
            print(f"unknown id {args.id}", file=sys.stderr)
            return 1
        write(REQ, items)
        print(f"{target} marked {'done' if args.cmd == 'done' else 'open'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
