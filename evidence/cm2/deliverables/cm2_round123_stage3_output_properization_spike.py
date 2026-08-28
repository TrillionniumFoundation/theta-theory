#!/usr/bin/env python3
"""Retained provisional wrapper for the Round123 stage-3 spike.

The final producer imports the common module directly.  This wrapper remains
outside the final manifest and preserves the earlier diagnostic CLI.
"""
from cm2_round123_rank3_exact_seed_stage3_output_properization_common import (
    main,
)


if __name__ == "__main__":
    raise SystemExit(main())
