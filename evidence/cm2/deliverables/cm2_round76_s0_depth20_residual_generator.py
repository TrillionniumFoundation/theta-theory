#!/usr/bin/env python3
"""Round-76 fixed-s0 depth-20 residual refinement producer."""
from __future__ import annotations

import argparse
import json
import sys

from cm2_round74_s0_depth2_adaptive_generator import build


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    json.dump(build(args.workers, 20), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
