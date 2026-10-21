#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10", "pydantic>=2,<3", "pytest>=8"]
# ///

# ─── How to run ───
#      uv run test_page_builder.py
# ──────────────────

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final, Sequence

import pytest

TEST_FILES: Final = tuple(
    Path(__file__).with_name(name)
    for name in (
        "test_page_spec.py",
        "test_page_output.py",
        "test_page_export.py",
    )
)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the responsibility-split product-detail regression suites."""
    forwarded = sys.argv[1:] if argv is None else argv
    return pytest.main([*(str(path) for path in TEST_FILES), *forwarded])


if __name__ == "__main__":
    raise SystemExit(main())
