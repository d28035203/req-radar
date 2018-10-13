#!/usr/bin/env python3
"""req-radar — tick software requirements."""
from __future__ import print_function
import re, sys, os

REQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.md")

def load():
    with open(REQ) as f:
        return f.read().splitlines()

def save(lines):
    with open(REQ, "w") as f:
        f.write("\n".join(lines) + "\n")

def list_req():
    for line in load():
        if line.strip().startswith("- ["):
            print(line)

def done(code):
    lines = load()
    out = []
    hit = False
    for line in lines:
        m = re.match(r"^(- )\[([ x])\] (%s\b.*)$" % re.escape(code), line)
        if m:
            out.append("%s[x] %s" % (m.group(1), m.group(3)))
            hit = True
        else:
            out.append(line)
    if not hit:
        print("no such id:", code)
        return 1
    save(out)
    print("done:", code)
    return 0

def main(argv):
    if not argv or argv[0] == "list":
        list_req()
        return 0
    if argv[0] == "done" and len(argv) > 1:
        return done(argv[1])
    print("usage: list | done ID")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
