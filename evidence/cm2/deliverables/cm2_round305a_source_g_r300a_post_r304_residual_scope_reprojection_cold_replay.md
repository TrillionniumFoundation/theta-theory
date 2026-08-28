# Round305A exact cold-replay record

Verdict: `PASS`.

The formal promotion, isolated no-write replay, producer dual-seed replay,
and independent dual-directory comparison all exited zero.  This record was
made from the workspace root on `2026-07-31` with Python `3.12.3`.

## Frozen pins

```text
producer_file_sha256=42e7cc1eeabaedee883a37b8de9301ee71d5ba068d2fb76fafc80b95061b6772
verifier_file_sha256=d4fd7bfd4c2bb90e1df515a9318d8f925fc9dab4bb8cb3872f496a3d665647bf
ledger_file_sha256=8db30279e03aac90ea96b7a603e51aaa6fb2a70ad6c1593915c55b1befe991b6
result_file_sha256=b985df80cc0b447f25509ef6d4095b9d0aa810ffcef05d4b5475bf84d36542f1
result_object_sha256=c391ecca3f5af8227052c628bda77104ec564d4eeaa625fafbde32a3ada352eb
attack_suite_file_sha256=3795cd3b03f961e010b351d5132f55f5d3bda8d4245707755d999e780a9c71b7
attack_suite_object_sha256=e060b0d4807014a341fa621742b1b5255ecc52036bd02c530779c485ba2367f7
verification_file_sha256=5c98bd02f4245d3b6fd7d35518b6932f984ec05d3e91b607854bf9e180b29c4d
verification_object_sha256=9654f43c32aacfd3a27b6baa18d65755dfb9c867bd869aaa586a9b736fcf7589
```

The producer and verifier pins, and the ledger and result candidate pins,
were identical before and after every admitted run.

## Formal independent promotion

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=305305 \
  /usr/bin/time -f \
  'FORMAL_ELAPSED=%e FORMAL_USER=%U FORMAL_SYS=%S FORMAL_MAXRSS_KB=%M FORMAL_EXIT=%x' \
  python3 \
  deliverables/cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection_promotion_verifier.py \
  --root /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572 \
  --candidate-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables \
  --producer-path /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection.py
```

Observed:

```text
FORMAL_EXIT=0
FORMAL_ELAPSED=133.34
FORMAL_USER=132.23
FORMAL_SYS=1.01
FORMAL_MAXRSS_KB=411260
status=PASS_EXACT_CACHELESS_ROUND305A_SCOPE_REPROJECTION
mechanism_count=36
fixture_count=36
rejected_count=36
coherently_resigned_fixture_count=25
formal_Round305A_scope_promotion_permitted=true
all_source_and_candidate_PRE_POST_fd_identities_equal=true
```

The formal publisher committed the attack suite first and the verification
last marker second.  Their mtimes are
`2026-07-31 23:40:00.700109092 +0800` and
`2026-07-31 23:40:00.704983611 +0800`, respectively.

## Isolated independent cold replay — no write

An empty private pycache root was created with `mktemp -d` and supplied as
`PYTHONPYCACHEPREFIX`; it was removed after the replay.

```bash
env PYTHONHASHSEED=905701 \
  PYTHONPYCACHEPREFIX=/tmp/cm2-r305a-p0-cold-pycache.BSCLSJ \
  /usr/bin/time -f \
  'COLD_ELAPSED=%e COLD_USER=%U COLD_SYS=%S COLD_MAXRSS_KB=%M COLD_EXIT=%x' \
  python3 -I \
  deliverables/cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection_promotion_verifier.py \
  --root /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572 \
  --candidate-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables \
  --producer-path /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/deliverables/cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection.py \
  --no-write
```

Observed:

```text
COLD_EXIT=0
COLD_ELAPSED=139.51
COLD_USER=136.57
COLD_SYS=1.12
COLD_MAXRSS_KB=410496
status=PASS_EXACT_CACHELESS_ROUND305A_SCOPE_REPROJECTION
candidate_and_promotion_outputs_written=false
attack_suite_file_sha256=3795cd3b03f961e010b351d5132f55f5d3bda8d4245707755d999e780a9c71b7
attack_suite_object_sha256=e060b0d4807014a341fa621742b1b5255ecc52036bd02c530779c485ba2367f7
verification_file_sha256=5c98bd02f4245d3b6fd7d35518b6932f984ec05d3e91b607854bf9e180b29c4d
verification_object_sha256=9654f43c32aacfd3a27b6baa18d65755dfb9c867bd869aaa586a9b736fcf7589
```

Thus the independently rebuilt no-write promotion bytes are exactly the
already promoted formal bytes under a different hash seed and isolated Python
execution environment.

## Producer dual-seed replay

Two private no-clobber staging directories under the workspace were created
with `mktemp -d`.  They were never admitted as formal promotion or credit
inputs and were deleted after the comparison.

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=305001 \
  /usr/bin/time -f \
  'SEED_A_ELAPSED=%e SEED_A_USER=%U SEED_A_SYS=%S SEED_A_MAXRSS_KB=%M SEED_A_EXIT=%x' \
  python3 -I \
  deliverables/cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection.py \
  --root /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572 \
  --output-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.r305a-p0-seed-a.5hJmev \
  --seed 305001

env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=305997 \
  /usr/bin/time -f \
  'SEED_B_ELAPSED=%e SEED_B_USER=%U SEED_B_SYS=%S SEED_B_MAXRSS_KB=%M SEED_B_EXIT=%x' \
  python3 -I \
  deliverables/cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection.py \
  --root /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572 \
  --output-dir /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.r305a-p0-seed-b.KR9v5I \
  --seed 305997
```

Observed:

```text
SEED_A_EXIT=0
SEED_A_ELAPSED=82.10
SEED_A_USER=81.57
SEED_A_SYS=0.48
SEED_A_MAXRSS_KB=77872

SEED_B_EXIT=0
SEED_B_ELAPSED=82.26
SEED_B_USER=81.69
SEED_B_SYS=0.52
SEED_B_MAXRSS_KB=76248
```

Each staging directory contained exactly the ledger and result candidate.
Both copies had these exact hashes:

```text
ledger_file_sha256=8db30279e03aac90ea96b7a603e51aaa6fb2a70ad6c1593915c55b1befe991b6
result_file_sha256=b985df80cc0b447f25509ef6d4095b9d0aa810ffcef05d4b5475bf84d36542f1
```

## Independent dual-directory comparison

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=777331 \
  /usr/bin/time -f \
  'DUAL_ELAPSED=%e DUAL_USER=%U DUAL_SYS=%S DUAL_MAXRSS_KB=%M DUAL_EXIT=%x' \
  python3 -I \
  deliverables/cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection_promotion_verifier.py \
  --root /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572 \
  --dual-seed-dir-a /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.r305a-p0-seed-a.5hJmev \
  --dual-seed-dir-b /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572/.r305a-p0-seed-b.KR9v5I
```

Observed:

```text
DUAL_EXIT=0
DUAL_ELAPSED=83.49
DUAL_USER=82.70
DUAL_SYS=0.78
DUAL_MAXRSS_KB=410684
status=PASS_DUAL_SEED_EXACT_BYTES
producer_seeds=[305001,305997]
seed_affects_output=false
candidate_outputs_written=false
```

## Final admission checks

The ledger passed `gzip -tv`.  The ledger, result, attack suite, and
verification all parsed as JSON and satisfied their exact status and census
queries.  The eight-member external SHA-256 manifest passed
`sha256sum -c` from the deliverables directory.  The manifest excludes itself
and therefore has no self-reference cycle.

The admitted scope is exactly `3,232 = 128 + 2,080 + 1,024`.  Round305A
grants zero physical-inclusion, component-edge, DSU-rank, maximality, fibre,
global-disposition, and Jx/Jy same-point-gluing credit.  D02 remains
`BLOCKED`, complete Gate5 18-field blocks remain `0`, and unconditional CM2
remains `NO-GO_FOR_CLAIM`.
