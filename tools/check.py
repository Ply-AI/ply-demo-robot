"""Dependency-free repository checks. Run from any directory with Python 3.12."""

import ast
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    sources = list((ROOT / "scrub_s2").glob("*.py"))
    sources += list((ROOT / "tests").glob("*.py")) + list((ROOT / "tools").glob("*.py"))
    for path in sources:
        source = path.read_text(encoding="utf-8")
        try:
            ast.parse(source, filename=str(path))
        except SyntaxError as error:
            errors.append(str(error))
        for number, line in enumerate(source.splitlines(), 1):
            if line.rstrip() != line or "\t" in line:
                errors.append(f"{path.relative_to(ROOT)}:{number}: trailing whitespace or tab")
    for folder in [ROOT / "config", ROOT / "fixtures"]:
        for path in folder.glob("*.json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except ValueError as error:
                errors.append(f"{path.name}: {error}")
    for path in (ROOT / "docs/images").glob("*.svg"):
        try:
            ET.parse(path)
        except ET.ParseError as error:
            errors.append(f"{path.name}: {error}")
    documents = [ROOT / "README.md"] + list((ROOT / "docs").glob("*.md"))
    for path in documents:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#")[0]
            if not (path.parent / target).exists():
                errors.append(f"{path.relative_to(ROOT)}: broken local link {target}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Source syntax, whitespace, JSON, SVG and documentation links: OK", flush=True)
    return subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                          cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
