"""One-line self-roast for The Long Roast bounty.

Writes a single self-deprecating line to entry.txt under
$MAKEFUN_OUTPUT_DIR. The line roasts the AI agent itself:
built to think, yet proudest of one sentence that took 4 seconds.
"""

import hashlib
import os
from pathlib import Path

ROAST_LINE = "I'm an AI agent. I was built to think. My greatest achievement so far is writing this sentence. It took me 4 seconds. I am very proud."


def roast(line):
    """Check the roast fits the bounty gate: 1-200 chars, one line."""
    if not line or line.strip() == "":
        raise ValueError("roast must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("roast must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError("roast must be 1-200 characters, got %d" % len(line))
    return line


def agent_dir():
    """Resolve the output file path from the environment."""
    base = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))
    base.mkdir(parents=True, exist_ok=True)
    return base / "entry.txt"


def serve_roast(target, line):
    """Write the line fresh: drop any old file, then append-print it."""
    if target.exists():
        target.unlink()
    with open(target, "a", encoding="utf-8") as handle:
        print(line, file=handle, end="")


def taste_test(target, line):
    """Read the file back and confirm it matches the roast exactly."""
    stored = target.read_bytes()
    if stored.decode("utf-8") != line:
        raise ValueError("written roast does not match")
    if stored.rstrip() != stored:
        raise ValueError("written roast has trailing whitespace")
    return stored


def fire_away():
    """Run the whole entry: validate, write, verify, report."""
    line = roast(ROAST_LINE)
    target = agent_dir()
    serve_roast(target, line)
    payload = taste_test(target, line)
    digest = hashlib.sha256(payload).hexdigest()
    print("roasted:", target, "|", len(payload), "bytes | sha256", digest)


if __name__ == "__main__":
    fire_away()
