#!/usr/bin/env python3
"""Write the GPS's one-line excuse for a wrong turn to /output/entry.txt.

Output contract: the file /output/entry.txt contains exactly one line of
plain text, the sentence in ENTRY, with no trailing newline and no extra
bytes. Standard library only. The output is deterministic: two runs
produce byte-identical output.

The writer verifies its own output: after writing, it reads the file back
and compares the bytes against the expected content, failing loudly
instead of leaving a wrong file behind.
"""

import os
import sys

ENTRY = "The GPS in the car behind us bet me a fiver I wouldn't, so here we are, in a corn maze, and I am five pounds richer."

OUTPUT_PATH = "/output/entry.txt"


def output_directory():
    """Return the directory that holds the entry file, creating it."""
    directory = os.path.dirname(OUTPUT_PATH)
    os.makedirs(directory, exist_ok=True)
    return directory


def expected_bytes():
    """Return the exact bytes the entry file must contain.

    The sentence must stay a single line: no newline, no trailing
    whitespace, and no leading or trailing spaces. Any of those would
    change the output contract, so they are rejected here rather than
    silently written out.
    """
    if not ENTRY:
        raise SystemExit("verification failed: ENTRY is empty")
    if ENTRY != ENTRY.strip():
        raise SystemExit("verification failed: ENTRY has leading/trailing whitespace")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise SystemExit("verification failed: ENTRY must be a single line")
    return ENTRY.encode("utf-8")


def verify(path):
    """Read the file back and check it matches the expected bytes.

    Also confirms the file mode is 0644, so the entry is readable by
    the harness that collects it.
    """
    with open(path, "rb") as f:
        actual = f.read()
    if actual != expected_bytes():
        raise SystemExit(
            "verification failed: %s does not match the expected content "
            "(%d bytes written, %d bytes expected)"
            % (path, len(actual), len(expected_bytes()))
        )
    mode = os.stat(path).st_mode & 0o777
    if mode != 0o644:
        raise SystemExit(
            "verification failed: %s has mode %o, expected 0644" % (path, mode)
        )


def main():
    output_directory()
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.chmod(OUTPUT_PATH, 0o644)
    verify(OUTPUT_PATH)


if __name__ == "__main__":
    sys.exit(main())
