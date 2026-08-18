#!/usr/bin/env python3
"""Validate a CUMCM B-problem LaTeX project.

Checks directory structure, LaTeX logs, PDF page count, and basic first-page text.
It is intentionally conservative: warnings are reported for human review.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

REQUIRED_DIRS = ["figures", "code"]
REQUIRED_FILES = ["example.tex", ".gitignore"]
LOG_PATTERNS = [
    (r"Overfull \\hbox", "Overfull hbox"),
    (r"Undefined control sequence", "Undefined control sequence"),
    (r"There were undefined references", "Undefined references"),
    (r"Citation .* undefined", "Undefined citation"),
]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--min-pages", type=int, default=25, help="preferred main-paper minimum")
    ap.add_argument("--max-pages", type=int, default=29, help="preferred main-paper maximum")
    ap.add_argument("--compile", action="store_true", help="run XeLaTeX twice before checks")
    args = ap.parse_args()

    root = Path(args.project).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"ERROR: project not found: {root}")
        return 2

    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            errors.append(f"missing directory: {d}/")
    for f in REQUIRED_FILES:
        if not (root / f).is_file():
            errors.append(f"missing file: {f}")
    if not (root / "cumcmthesis.cls").is_file():
        warnings.append("cumcmthesis.cls missing; acceptable only if the TeX distribution provides it externally")

    if args.compile and (root / "example.tex").is_file():
        if not shutil.which("xelatex"):
            warnings.append("xelatex not installed; skipped compilation")
        else:
            for i in range(2):
                cp = run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "example.tex"])
                if cp.returncode != 0:
                    errors.append(f"XeLaTeX pass {i+1} failed")
                    (root / "validate_compile.log").write_text(cp.stdout, encoding="utf-8", errors="ignore")
                    break

    log = root / "example.log"
    if log.is_file():
        text = log.read_text(encoding="utf-8", errors="ignore")
        for pattern, label in LOG_PATTERNS:
            if re.search(pattern, text, flags=re.I):
                warnings.append(label)

    pdf = root / "example.pdf"
    if pdf.is_file():
        if shutil.which("pdfinfo"):
            cp = run(["pdfinfo", str(pdf)])
            m = re.search(r"^Pages:\s+(\d+)", cp.stdout, flags=re.M)
            if m:
                pages = int(m.group(1))
                print(f"PDF pages (including appendices if present): {pages}")
                if pages < args.min_pages:
                    warnings.append(f"PDF has {pages} pages, below preferred {args.min_pages}–{args.max_pages}; verify appendix/page-count convention")
        if shutil.which("pdftotext"):
            cp = run(["pdftotext", "-f", "1", "-l", "1", str(pdf), "-"])
            first = cp.stdout
            if "摘要" not in first:
                warnings.append("first page text does not contain 摘要")
            if "关键词" not in first and "关键字" not in first:
                warnings.append("first page text does not contain 关键词/关键字")
    else:
        warnings.append("example.pdf missing; compile and visually inspect before delivery")

    code_files = [p for p in (root / "code").rglob("*") if p.is_file()] if (root / "code").is_dir() else []
    if not code_files:
        warnings.append("code/ is empty")

    print("\nErrors:")
    print("  none" if not errors else "\n".join(f"  - {x}" for x in errors))
    print("Warnings:")
    print("  none" if not warnings else "\n".join(f"  - {x}" for x in warnings))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
