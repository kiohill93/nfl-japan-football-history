"""Scan the site sources and the built pages for strings that must stay private.

The patterns live in tools/private-patterns.txt, which is gitignored so the
strings themselves are never published. Each line is a literal (matched
case-insensitively) or, with a "re:" prefix, a case-insensitive regex.

A hit on "pitch" is allowed when it is plainly about the playing surface
(for example "on the pitch"); add such phrases to ALLOWED below.

Usage:  .venv\\Scripts\\python.exe tools\\check_private.py
Exit status is 1 when any hit remains.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN_FILE = ROOT / "tools" / "private-patterns.txt"
TARGETS = ["docs", "content", "data", "src", "README.md"]
SUFFIXES = {".md", ".html", ".csv", ".json", ".py", ".js", ".css", ".txt"}

# Phrases where a matched word is used in an ordinary, non-private sense.
ALLOWED = [
    re.compile(r"\b(on|off|onto) the pitch\b", re.I),
    re.compile(r"\bpitch (invasion|side|surface)\b", re.I),
]


def load_patterns() -> list[tuple[str, re.Pattern]]:
    if not PATTERN_FILE.exists():
        sys.exit(f"Missing {PATTERN_FILE}; create it with one private string per line.")
    out = []
    for raw in PATTERN_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            out.append((line, re.compile(line[3:], re.I)))
        else:
            out.append((line, re.compile(re.escape(line), re.I)))
    return out


def files() -> list[Path]:
    found = []
    for t in TARGETS:
        p = ROOT / t
        if p.is_file():
            found.append(p)
        elif p.is_dir():
            found += [f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in SUFFIXES]
    return sorted(found)


def allowed(line: str, start: int, end: int) -> bool:
    for a in ALLOWED:
        for m in a.finditer(line):
            if m.start() <= start and end <= m.end():
                return True
    return False


def main() -> int:
    patterns = load_patterns()
    hits = 0
    checked = files()
    for f in checked:
        text = f.read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            for label, rx in patterns:
                for m in rx.finditer(line):
                    if allowed(line, m.start(), m.end()):
                        continue
                    hits += 1
                    s = max(0, m.start() - 50)
                    ctx = line[s:m.end() + 50].strip()
                    print(f"{f.relative_to(ROOT)}:{n}: [{label}] ...{ctx}...")
    print(f"\nChecked {len(checked)} files against {len(patterns)} patterns: {hits} hit(s).")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
