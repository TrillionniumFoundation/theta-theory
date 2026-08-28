#!/usr/bin/env python3
"""Round113 certificate entry point for endpoint-sheet physical ordering."""
from __future__ import annotations

import argparse
import json

from cm2_round113_rank3_root_sheet_owner_ordering_spike import (
    DEFAULT_MAX_DEPTH,
    PRECISION_BITS,
    build,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    args = parser.parse_args()
    print(json.dumps(
        build(args.precision_bits, args.max_depth), sort_keys=True, indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
