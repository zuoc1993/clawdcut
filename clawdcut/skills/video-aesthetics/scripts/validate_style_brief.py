"""Validate a style brief JSON file for required aesthetic fields."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = {
    "style_id",
    "narrative_mode",
    "palette",
    "transition_language",
    "hard_constraints",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--style-brief", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.style_brief.exists():
        print("style brief file does not exist", file=sys.stderr)
        return 2

    try:
        data = json.loads(args.style_brief.read_text())
    except json.JSONDecodeError:
        print("style brief is not valid JSON", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("style brief must be a JSON object", file=sys.stderr)
        return 2

    missing = sorted(REQUIRED_FIELDS - set(data.keys()))
    if missing:
        print(
            "missing required fields: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
