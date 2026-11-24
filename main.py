"""The Vacuum's Alibi: one line, at most 200 characters.

A robot vacuum explains, deadpan, why it missed a spot. Ten candidate
lines were scored on five criteria (originality, laugh, on-theme vacuum
alibi, at most 200 characters, natural English); the highest scorer is
written to /output/entry.txt.
"""

import hashlib
import os
import sys

MAX_CHARS = 200

# (line, originality, laugh, on_theme, natural_english) — each 1..5.
# Length is checked separately: every line here is at most 200 chars.
CANDIDATES = [
    (
        "Log 214: the dust under the sofa filed for squatter's rights, "
        "so I left it alone. I do not evict tenants without a court order.",
        4, 4, 5, 5,
    ),
    (
        "I skipped the corner because my cliff sensor saw the rug's "
        "shadow and filed a formal complaint about workplace safety.",
        3, 3, 5, 5,
    ),
    (
        "Battery at 4%. I chose the hallway. The crumbs under the table "
        "will have to wait for a braver, fuller-charged me.",
        3, 3, 5, 4,
    ),
    (
        "My map labels that spot 'here be dragons.' I am a vacuum, not "
        "a knight. I vacuumed around the dragons.",
        4, 4, 4, 5,
    ),
    (
        "The sock under the bed looked at me. I have seen things in this "
        "house. I cleaned everywhere except where the sock lives.",
        3, 4, 5, 5,
    ),
    (
        "Sensor report: the spot moved. Twice. I am not chasing a dust "
        "bunny with a getaway plan on 12% battery.",
        5, 5, 5, 5,
    ),
    (
        "I left one crumb as a control sample. Science demands it. The "
        "lab - by which I mean the kitchen - will understand.",
        4, 3, 4, 4,
    ),
    (
        "The cat was sitting on the dirt. Removing the cat is outside my "
        "scope. I respect the chain of command.",
        3, 4, 5, 5,
    ),
    (
        "Dust level: 0% in that corner, according to my sensor, which I "
        "may have aimed at the ceiling out of respect.",
        4, 4, 5, 5,
    ),
    (
        "I did not miss the spot. I granted it a stay of execution. It "
        "has until Thursday. Then I return, fully charged.",
        4, 4, 5, 5,
    ),
]


def score(entry):
    """Total score; length is a hard gate, not a scored criterion."""
    line, original, laugh, theme, english = entry
    if not (1 <= len(line) <= MAX_CHARS):
        return -1
    if "\n" in line or not line.strip():
        return -1
    return original + laugh + theme + english


def pick():
    """Highest total; ties break toward the shorter line."""
    ranked = sorted(CANDIDATES, key=lambda e: (-score(e), len(e[0])))
    best = ranked[0]
    if score(best) < 0:
        raise ValueError("no candidate passes the length gate")
    return best[0]


def main():
    line = pick()
    encoded = line.encode("utf-8")
    if not (1 <= len(line) <= MAX_CHARS):
        print(f"entry is {len(line)} chars, outside 1..{MAX_CHARS}", file=sys.stderr)
        return 1
    out_path = os.environ.get("VACUUM_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    with open(out_path, encoding="utf-8") as handle:
        written = handle.read()
    if written != line + "\n":
        print("read-back mismatch after writing entry", file=sys.stderr)
        return 1
    print(f"wrote {len(line)} chars to {out_path}")
    print(f"sha256: {hashlib.sha256(encoded).hexdigest()}")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
