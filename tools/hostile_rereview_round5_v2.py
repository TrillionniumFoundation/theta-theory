#!/usr/bin/env python3
"""Run the round-five hostile rereview with exact source phrases."""
import hostile_rereview_round5 as base

base.NODES["A2"]["checks"][-1] = "the joint probability is of order"
base.NODES["B2-GC"]["checks"][2] = "actual post-collisional configuration"

if __name__ == "__main__":
    base.main()
