#!/usr/bin/env python3

import sys
import os

def split_on_empty(input_file):
    if not os.path.isfile(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")  # split on double newlines

    for i, block in enumerate(blocks, start=1):
        outfile = f"part_{i}.txt"
        with open(outfile, "w", encoding="utf-8") as out:
            out.write(block.strip() + "\n")  # ensure trailing newline
        print(f"Wrote {outfile}")

    print(f"✅ Split into {len(blocks)} files")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_on_empty.py input.txt")
    else:
        split_on_empty(sys.argv[1])
