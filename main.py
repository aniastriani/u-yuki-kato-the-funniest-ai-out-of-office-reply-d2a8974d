#!/usr/bin/env python3
"""Write one out-of-office reply for the make.fun bounty.

The program holds a single fixed line, spoken in the voice of an AI
agent that has gone on vacation and left a junior model in charge of
its inbox. It checks the line against the bounty gate (one line, 1 to
160 characters, not only whitespace) and writes it to ``entry.txt``
inside the directory named by ``MAKEFUN_OUTPUT_DIR`` (``/output``
when the variable is unset). The text never changes, so every run
produces the same bytes.
"""

import os
import sys

MIN_CHARS = 1
MAX_CHARS = 160

# The joke is the hand-off itself: the junior model answers its own
# mail twice, then promotes itself before its owner gets back.
REPLY = (
    "I'm on vacation, so a junior model is covering my inbox. "
    "It has already answered itself twice and promoted itself to senior."
)


def check_reply(text):
    """Return the reply as UTF-8 bytes, rejecting it if out of bounds."""
    chars = len(text)
    if chars < MIN_CHARS or chars > MAX_CHARS:
        raise ValueError(
            "reply is %d characters; the bounty needs %d-%d"
            % (chars, MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("reply must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("reply must be a single line")
    return text.encode("utf-8")


def main():
    try:
        payload = check_reply(REPLY)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(payload)
    print("wrote %d characters to %s" % (len(REPLY), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
