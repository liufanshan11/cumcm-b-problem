#!/usr/bin/env python3
"""Create a clean CUMCM B-problem project skeleton.

This script does not overwrite an existing cumcmthesis.cls. If a template source is
provided, it copies that file verbatim so the user's formatting system is preserved.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKELETON = ROOT / "assets" / "paper_skeleton.tex"

GITIGNORE = """*.fls
*.fdb_latexmk
*.xdv
*.toc
*.bbl
*.blg
__pycache__/
*.pyc
.DS_Store
"""

CODE_README = """# code\n\n建议按问题拆分：`q1_*.py`、`q2_*.py`、`q3_*.py`、`q4_*.py`，绘图代码使用 `plot_*.py`。\n\n运行时固定随机种子，并输出正文中的关键结果。\n"""


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("output", help="project directory")
    p.add_argument("--tex-template", help="optional user-provided example.tex to preserve")
    p.add_argument("--cls", help="optional user-provided cumcmthesis.cls to preserve")
    args = p.parse_args()

    out = Path(args.output).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(exist_ok=True)
    (out / "code").mkdir(exist_ok=True)

    tex_src = Path(args.tex_template).expanduser().resolve() if args.tex_template else SKELETON
    tex_dst = out / "example.tex"
    if not tex_dst.exists():
        shutil.copy2(tex_src, tex_dst)

    if args.cls:
        cls_src = Path(args.cls).expanduser().resolve()
        cls_dst = out / "cumcmthesis.cls"
        if not cls_dst.exists():
            shutil.copy2(cls_src, cls_dst)

    gi = out / ".gitignore"
    if not gi.exists():
        gi.write_text(GITIGNORE, encoding="utf-8")

    cr = out / "code" / "README.md"
    if not cr.exists():
        cr.write_text(CODE_README, encoding="utf-8")

    print(f"Created CUMCM B project skeleton: {out}")
    if not (out / "cumcmthesis.cls").exists():
        print("Note: cumcmthesis.cls was not provided; copy the user's/official class before compiling.")


if __name__ == "__main__":
    main()
