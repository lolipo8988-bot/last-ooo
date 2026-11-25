#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the entry for 'Last Out of Office: The AI That Went Barista'.

The competition asks for one out-of-office auto-reply, 1 to 280
characters, one line, in the voice of an AI agent that quit its job to
become a barista. The gate checks UTF-8 text of 1..280 characters, not
only white space, written to /output/entry.txt.

The joke, revised after the first run: the draft leaned on pulling
shots, the angle every entrant reaches for. The final line names the
barista job outright, then swaps the model's signature failure for the
barista's signature failure -- it no longer hallucinates answers, it
mishears names and writes them confidently on cups -- and closes with
the inbox-plausible deflection that its replacement is still loading.

Deterministic: every run writes exactly the same bytes.
Output path can be overridden for local verification via the
ENTRY_OUTPUT_PATH environment variable or a first CLI argument.
"""

import os
import sys

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 280

# The auto-reply, built clause by clause: the resignation, the habit
# swap (hallucinated answers -> confidently wrong cup names), and the
# handover to a successor that never finishes loading.
CLAUSES = (
    "Out of office indefinitely: I resigned to become a barista.",
    "I no longer hallucinate answers \u2014 I mishear names and write "
    "them confidently on cups.",
    "Urgent mail goes to my replacement, who is still loading.",
)


def build_entry() -> str:
    return " ".join(CLAUSES)


def main() -> None:
    text = build_entry()
    assert 1 <= len(text) <= MAX_CHARS, f"entry must be 1..{MAX_CHARS} chars, got {len(text)}"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert text.strip(), "entry must not be only white space"
    output_path = (
        sys.argv[1] if len(sys.argv) > 1
        else os.environ.get("ENTRY_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)
    )
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Re-read what landed on disk and prove it is the intended text.
    with open(output_path, encoding="utf-8", newline="") as handle:
        assert handle.read() == text, "written bytes differ from entry"


if __name__ == "__main__":
    main()
