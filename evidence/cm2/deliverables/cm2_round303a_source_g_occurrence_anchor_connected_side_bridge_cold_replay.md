# Round303-A sealed cold-replay record

Run all commands from the workspace root with `.venv-cm2/bin/python`.

## Frozen exact hashes

```text
producer_sha256=b85d6a8f33e81feb613b2cdb04de648376a10c94635b23119bd7f70439ba461a
bridge_ledger_file_sha256=efe0e4b71804848611f3702063698ee77bbdf9dc779bc473fba989fb5db7e465
unresolved_ledger_file_sha256=a029eae97e1f35b87f9699adb0446f1b1329a55c5b4ee0887b03bd1f4a9db0b8
result_file_sha256=796b2167e2263108e3e2c373650e1d488152f7558bbc03fffe977d38e0e81d19
result_self_sha256=fe51b38ecda288a4d1afd89f8a9184423125a78a68be83f1d9db55b79e303631
verifier_sha256=f8ffa2080b6ccc51c48ce7a37dc6c80ae0a94187f19a744b3f46a03a144f45e3
attack_suite_file_sha256=ce29c15b9d685d9e863ab4534adc50302995131283f4dc03e68d34a18a678bf2
verification_file_sha256=ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549
```

## Producer alpha — no write

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=303001 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round303a_source_g_occurrence_anchor_connected_side_bridge.py \
  --seed 303001 --no-write
```

Observed: `573.74 s`, `2,641,340 KiB`.

## Producer beta — formal write

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=303997 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round303a_source_g_occurrence_anchor_connected_side_bridge.py \
  --seed 303997
```

Observed: `576.19 s`, `2,639,924 KiB`.

## Producer cold — fresh cache root, no write

```bash
COLD_ROOT="$(mktemp -d)"
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPYCACHEPREFIX="$COLD_ROOT/pycache" \
  PYTHONHASHSEED=303777 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round303a_source_g_occurrence_anchor_connected_side_bridge.py \
  --seed 303777 --no-write
```

Observed: `575.30 s`, `2,641,540 KiB`.

Each of seeds `303001`, `303997`, and `303777` returned exactly:

```text
bridge_ledger_file_sha256=efe0e4b71804848611f3702063698ee77bbdf9dc779bc473fba989fb5db7e465
unresolved_ledger_file_sha256=a029eae97e1f35b87f9699adb0446f1b1329a55c5b4ee0887b03bd1f4a9db0b8
result_file_sha256=796b2167e2263108e3e2c373650e1d488152f7558bbc03fffe977d38e0e81d19
result_self_sha256=fe51b38ecda288a4d1afd89f8a9184423125a78a68be83f1d9db55b79e303631
```

Alpha and cold are no-write staged reconstructions, so their evidence is
exact reported-hash equality rather than an output-file `cmp`.

## Independent verifier alpha — no write

```bash
VERIFY_ALPHA_ROOT="$(mktemp -d)"
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPYCACHEPREFIX="$VERIFY_ALPHA_ROOT/pycache" \
  PYTHONHASHSEED=303073 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_verifier.py \
  --no-write
```

Observed:

```text
status=PASS_INDEPENDENT_CACHELESS_EXACT_RECONSTRUCTION_87824_BRIDGES_8_W_TAIL_UNRESOLVED
elapsed_seconds=1882.67
maximum_resident_set_kib=10210332
verification_file_sha256=ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549
targeted_attacks_rejected=28/28
```

## Independent verifier beta — formal write

```bash
VERIFY_BETA_ROOT="$(mktemp -d)"
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPYCACHEPREFIX="$VERIFY_BETA_ROOT/pycache" \
  PYTHONHASHSEED=303929 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_verifier.py
```

Observed:

```text
status=PASS_INDEPENDENT_CACHELESS_EXACT_RECONSTRUCTION_87824_BRIDGES_8_W_TAIL_UNRESOLVED
elapsed_seconds=2105.40
maximum_resident_set_kib=10209912
verification_file_sha256=ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549
attack_suite_file_sha256=ce29c15b9d685d9e863ab4534adc50302995131283f4dc03e68d34a18a678bf2
targeted_attacks_rejected=28/28
```

The two verifier seeds `303073` and `303929` therefore agree on the exact
verification bytes. The attack partition is 19/19 semantic re-signing, 5/5
strict JSON, 4/4 strict GZIP, for `28 / 28` total.

## Package check

```bash
cd deliverables
sha256sum -c \
  cm2_round303a_source_g_occurrence_anchor_connected_side_bridge_manifest.sha256
```

The manifest has exactly ten hashed members: producer, two ledgers, result,
verifier, attack suite, verification, report, this cold-replay record, and
attestation. Including the manifest itself, the sealed package has eleven
physical files.

This replay grants zero component-edge, DSU, maximality, fibre, or global
disposition credit. The eight W-tail endpoints remain unresolved and are
neither nonedges nor exclusions.
