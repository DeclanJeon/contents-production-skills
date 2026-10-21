#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10", "pydantic>=2,<3"]
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run compose_detail_page.py --spec page-spec.json --output output/product
# 3. Or make executable and run:
#      chmod +x compose_detail_page.py && ./compose_detail_page.py --help
# ──────────────────

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from builder import ComposeRequest, OutputPathError, compose_page
from errors import PageSpecError, RenderError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compose product-detail modules and preview.")
    parser.add_argument("--spec", required=True, type=Path, help="Input page-spec.json")
    parser.add_argument("--output", required=True, type=Path, help="New output directory")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        manifest = compose_page(ComposeRequest(args.spec, args.output))
    except (PageSpecError, OutputPathError, RenderError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(
        f"composed {manifest.module_count} module(s) to "
        f"{args.output.expanduser().resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
