#!/usr/bin/env python3
"""Prepare an mdBook project from a translated Markdown tree."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--translated-dir", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--title", default="Translated Documentation")
    parser.add_argument("--language", default="")
    return parser.parse_args()


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return re.sub(r"\s+\{#.*\}$", "", match.group(1)).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def sort_key(path: Path) -> tuple[int, str]:
    name = path.name.lower()
    if name == "index.md":
        return (0, path.as_posix())
    if name.startswith(("readme.", "introduction.", "intro.", "overview.")):
        return (1, path.as_posix())
    return (2, path.as_posix())


def main() -> int:
    args = parse_args()
    translated = Path(args.translated_dir).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    src = out / "src"
    if not translated.is_dir():
        raise SystemExit(f"Translated directory not found: {translated}")
    if out.exists():
        shutil.rmtree(out)
    src.mkdir(parents=True)

    for item in translated.rglob("*"):
        rel = item.relative_to(translated)
        target = src / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.suffix.lower() == ".md":
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)

    md_files = sorted(src.rglob("*.md"), key=lambda p: sort_key(p.relative_to(src)))
    summary_lines = ["# Summary", ""]
    for md_file in md_files:
        rel = md_file.relative_to(src)
        depth = len(rel.parts) - 1
        indent = "  " * depth
        summary_lines.append(f"{indent}- [{first_heading(md_file)}]({rel.as_posix()})")
    (src / "SUMMARY.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    language_line = f'language = "{args.language}"\n' if args.language else ""
    (out / "book.toml").write_text(
        f'[book]\ntitle = "{args.title}"\n{language_line}src = "src"\n\n[output.html]\n',
        encoding="utf-8",
    )
    print(f"Prepared mdBook project at {out}")
    print(f"Chapters: {len(md_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
