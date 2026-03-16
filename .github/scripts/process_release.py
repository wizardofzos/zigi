import sys
from datetime import datetime

import re

import re

def release_to_markdown(text: str) -> str:
    lines = text.splitlines()
    out = []
    current_bullet = None

    for raw in lines:
        line = raw.rstrip()

        # Remove decorative borders
        if re.match(r'^\s*[\*\-=|]{5,}', line):
            continue

        # Strip box edges
        if line.strip().startswith("|") and line.strip().endswith("|"):
            line = line.strip()[1:-1].strip()

        line = line.rstrip()

        # Detect title
        if "Release Notes" in line:
            out.append("# " + line.strip())
            continue

        # Detect version
        m = re.search(r"Version\s+([\d.]+)", line)
        if m:
            out.append(f"## Version {m.group(1)}")
            continue

        # Detect major sections
        if "New Features and Functions" in line:
            out.append("\n## New Features and Functions\n")
            continue

        # Detect Key changes
        if line.strip().startswith("Key changes"):
            out.append("\n### Key Changes\n")

            # extract first bullet
            m = re.search(r"-\s+(.*)", line)
            if m:
                current_bullet = m.group(1)
                out.append(f"- {current_bullet}")
            continue

        # Detect bullet
        m = re.match(r"\s*-\s+(.*)", line)
        if m:
            current_bullet = m.group(1)
            out.append(f"- {current_bullet}")
            continue

        # Detect continuation line
        if line.startswith(" ") and current_bullet:
            cont = line.strip()
            out[-1] = out[-1] + " " + cont
            continue

        # Reset bullet context
        current_bullet = None

        if line.strip():
            out.append(line.strip())

    return "\n".join(out)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    text = f.readlines()

# Our ZIGI.RELEASE dataset/file always has all releases in it.
# Releases are separated with a liek containing 77 '-' characters
# So we first find that
stop = [idx for idx, s in enumerate(text) if 77*'-' in s][0]
# For the GitHub release we also skip the first part
# so we start on the line where it says "ZIGI Release Notes"
start = [idx for idx, s in enumerate(text) if 'ZIGI Release Notes' in s][0]
# Now this release is 
this_release_text = ''.join(text[start:stop])
this_release = release_to_markdown(this_release_text)


with open(output_file, "w") as f:
    f.write(this_release)