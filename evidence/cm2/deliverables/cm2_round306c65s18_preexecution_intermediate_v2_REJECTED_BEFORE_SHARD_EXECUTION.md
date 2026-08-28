# C65s18 intermediate v2 preexecution rejection

Status: `REJECTED_BEFORE_ANY_SHARD_EXECUTION__ZERO_CREDIT`

The first v2 builder experiment published files whose basenames ended in
`assignment_inventory_v1` and `assignment_result_v1`, and the contemporaneous
runner had not yet frozen those exact bytes as input pins.  Those intermediate
files and their local checks are historical diagnostics only.  No shard used
them.  They have no assignment, formal, whole-parent, or D02 gate credit.

The only eligible v2 chain uses the explicit `assignment_inventory_v2` and
`assignment_result_v2` filenames, followed by a frozen authorization seal and
a final executor that pins and globally replays those exact bytes.
