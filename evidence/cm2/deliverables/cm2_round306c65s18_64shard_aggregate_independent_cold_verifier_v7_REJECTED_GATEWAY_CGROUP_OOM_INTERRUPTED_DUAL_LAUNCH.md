# C65s18 aggregate cold verifier v7 terminal rejection

Status: `REJECTED_V7_PREPUBLICATION_GATEWAY_CGROUP_OOM_INTERRUPTED_DUAL_LAUNCH__ZERO_CREDIT`

The rejected v7 verifier source has SHA-256
`7ef3c0b97f67a0fb39bffcb60f65c368a24c45f85876aa791ddf7de942cf3d99`.
Before the formal attempt it passed its 124/124 development hostile self-test,
held-script preflight, and a read-only full post-numeric projection/validator
probe.  Those development results were not formal publications and carry no
credit.

The formal dual-seed attempt began at 2026-08-13 07:19:04 +08:00 through the
diagnostic held-script wrapper
`/tmp/c65-v7-formal.qkgIQx/launch.py`, whose SHA-256 is
`f58d2b11db00e7e2aaae6a7ff4ef6b8d278a1c75b893ab783d7014d418ec5448`.
The observed launcher, formal leader, and seed-worker PIDs were respectively
3571030, 3571031, 3571060, and 3571066.  The attempt was started from an
OpenClaw gateway-owned execution context.

At 2026-08-13 09:14:15 +08:00, systemd-oomd killed
`openclaw-gateway.service` for sustained memory pressure.  The user journal
records 54.2 GiB current memory for the unit at selection, a 71.9 GiB unit
peak, and terminal `status=9/KILL`, followed by gateway restart.  After the
kill, none of the four launch PIDs or any matching held-script/seed worker was
present.

The diagnostic directory contains only the 1,068-byte wrapper and an empty
`output.log`.  The empty log has SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
`exit.status` is absent.  Therefore the attempt has neither a successful
terminal record nor an ordinary fail-closed terminal record and cannot be
resumed, installed, or interpreted as completed.

All eleven v7 formal targets were absent after the interrupted launch.  In
particular, neither seed projection nor either seed completion receipt was
published.  The 64 shard ledger/receipt pairs, aggregate bundle, verifier
source, runtime, canonical status, authority files, and successor state were
unchanged.  No mixed formal prefix or deliverable-side partial target exists.

This marker terminally rejects the unrecorded v7 attempt so an empty output
set cannot be used to erase its launch history and rerun the same release
identity.  The rejected v7 source, its stale `pyc`, and all temporary launch
remnants must never be imported, resumed, executed as prerequisites, used as
verification evidence, or included as release-manifest members.  A successor
must pin this marker and the rejected source, use a fresh version and fresh
launch directory, and place the formal run in an independently supervised
systemd unit outside the gateway cgroup.

Formal, handoff, whole-parent, and D02 gate credit remain exactly zero.
