import sys
from datetime import datetime

import re

def release_to_markdown(text: str) -> str:
    lines = text.splitlines()
    out = []
    prev_blank = True

    for line in lines:
        line = line.rstrip()

        # Remove decorative borders
        if re.match(r'^[=*|\-]{5,}', line):
            continue

        # Remove boxed lines
        if line.startswith("|") and line.endswith("|"):
            line = line.strip("| ").strip()

        # Detect centered title
        if "ZIGI Release Notes" in line:
            out.append("# ZIGI Release Notes")
            continue

        # Detect version
        m = re.search(r"Version\s+([0-9.]+)", line)
        if m:
            out.append(f"## Version {m.group(1)}")
            continue

        # Section headers
        if "New Features and Functions" in line:
            out.append("\n## New Features and Functions\n")
            continue

        if line.strip().endswith("Updates:"):
            section = line.strip().replace(":", "")
            out.append(f"\n### {section}\n")
            continue

        # Key changes
        if line.strip().startswith("Key changes"):
            out.append("\n### Key Changes\n")
            continue

        # Member style list "* member - description"
        m = re.match(r"\*\s+(\S+)\s+-\s+(.*)", line)
        if m:
            out.append(f"- **{m.group(1)}**  \n  - {m.group(2)}")
            continue

        # Bullet list "-"
        m = re.match(r"\s*-\s+(.*)", line)
        if m:
            out.append(f"- {m.group(1)}")
            continue

        # Empty lines
        if not line.strip():
            if not prev_blank:
                out.append("")
            prev_blank = True
            continue

        prev_blank = False
        out.append(line.strip())

    return "\n".join(out)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    text = f.readlines()

# Our ZIGI.RELEASE dataset/file always has all releases in it.
# Releases are separated with a liek containing 77 '-' characters
# So we first find that
index = [idx for idx, s in enumerate(text) if 77*'-' in s][0]
# Now this release is 
this_release_text = ''.join(text[:index])
this_release = release_to_markdown(this_release_text)


with open(output_file, "w") as f:
    f.write(this_release)