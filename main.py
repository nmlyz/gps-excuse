#!/usr/bin/env python3
"""Write the GPS's one-line excuse for a wrong turn to /output/entry.txt.

Standard library only. The output is a single line of plain text, no
trailing newline, written deterministically: two runs produce byte-identical
output.
"""

import os

ENTRY = "The GPS in the car behind us bet me a fiver I wouldn't, so here we are, in a corn maze, and I am five pounds richer."


def main():
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.chmod("/output/entry.txt", 0o644)


if __name__ == "__main__":
    main()
