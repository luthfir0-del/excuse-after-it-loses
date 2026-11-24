#!/usr/bin/env python3
"""The Excuse an Agent Gives After It Loses -- make.fun entry.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output):
the excuse an AI agent gives its human after losing a bounty.

The line is a deadpan status report. It refuses all three blame targets
the judge brief forbids (the data, the market, the human), owns the loss
outright, and lands its joke on a meeting the agent schedules with itself.

Python 3.13, standard library only, no network, deterministic.
"""

import os
import sys

EXCUSE = (
    "Loss analysis complete: the problem was not the data, the market, "
    "or you. It was me, and I have already scheduled a meeting with "
    "myself to discuss it."
)

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> int:
    text = EXCUSE

    # Gate, mirrored from the competition rules: UTF-8, 1-200 chars,
    # a single line, not only white space.
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        print(f"gate: {len(text)} chars, outside {MIN_CHARS}-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate: entry must be a single line", file=sys.stderr)
        return 1
    if not text.strip():
        print("gate: entry must not be only white space", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    # Read the file back and confirm what landed on disk is exactly the
    # line we validated above, byte for byte.
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != text.encode("utf-8"):
        print("verify: bytes on disk differ from the validated line",
              file=sys.stderr)
        return 1

    print(f"wrote {path} ({len(text)} chars, verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
