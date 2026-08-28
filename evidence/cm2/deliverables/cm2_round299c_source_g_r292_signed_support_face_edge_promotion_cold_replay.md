# Round299-C signed-support face-edge package: dual-seed cold replay

## Verdict

PASS. Two cacheless verifier runs with distinct seed and
`PYTHONHASHSEED` values reconstructed the same 43,092 classifications, the
same three derived formal ledgers, and the same candidate result. They emitted
byte-identical independent attack and verification commitments.

The seed is replay bookkeeping only. It does not select, omit, or reorder
evidence.

## Environment

```text
Python 3.12.3
python-flint 0.9.0
Arb precision 512 bits
PYTHONDONTWRITEBYTECODE=1
```

## First cacheless replay

The first run wrote the canonical independent attack suite and verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=299351 /usr/bin/time -v \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round299c_source_g_r292_signed_support_face_edge_promotion_verifier.py \
  --seed 299351
```

Observed resources:

```text
wall time       586.58 s
user time       561.24 s
system time      25.22 s
maximum RSS   9,065,792 KiB
exit status        0
```

## Second cacheless no-write replay

The second run rebuilt the complete expected package but was forbidden to
write. It compared its newly computed independent attack and verification
bytes with the first-run files:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=299953 /usr/bin/time -v \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round299c_source_g_r292_signed_support_face_edge_promotion_verifier.py \
  --seed 299953 --no-write
```

Observed resources:

```text
wall time       583.17 s
user time       557.61 s
system time      25.43 s
maximum RSS   9,067,228 KiB
exit status        0
```

The persisted independent artifact modification times remained those of the
first run, confirming that the second replay did not rewrite them.

## Identical PASS output

Both runs reported:

```text
PASS_INDEPENDENT_CACHELESS_ROUND299C__43092_CLASSIFICATIONS__
27856_RAW_WITNESSES__25452_CANONICAL_EDGES__2092_SELF__
13144_EXCLUSIONS__4_MIXED_EXISTS_PAIRS__56_OF_56_ATTACKS_REJECTED__
NO_DSU_OR_MAXIMALITY
```

Both runs emitted:

```text
independent_attack_file_sha256
ca1bfdf6c8c7199dc7f834b64ece75121bf9bf09747384b610fb68ba21c6696d

independent_attack_self_sha256
16bc87111e88a157c047a4302f7bab410b96d2fce72d5a2c3548fb613b476d28

verification_file_sha256
82a96d122f6b3059d390d5864b99ff2d58e2720da9b0677bdd06012adaf02853

verification_self_sha256
5b6db1069e140b1c5bf8eeb01ee9bc3790de1fef32757bae568858fcc1b72fb1
```

## Scope fixed in both runs

Both runs independently enforced:

- 11,852 Round292 refinement cells;
- 43,092 complete face classifications with zero unresolved contacts;
- 27,856 accepted nonself raw component-edge witnesses;
- 25,452 canonical occurrence-edge pairs;
- 2,092 accepted self contacts with zero edge credit;
- 13,144 exact exclusions with zero edge credit;
- four mixed accepted/rejected endpoint pairs under `EXISTS`;
- 56/56 independent attacks rejected;
- no occurrence collapse, DSU rank reduction, maximality, fibre, global
  disposition, or CM2 promotion.

The Round299-C producer was never imported, executed, or parsed. Its bytes
were used only for an inert fixed SHA-256 pin. The persisted Round299 probe
ledger/result were not used as expected-row oracles. Candidate artifacts were
opened only after the expected classifications and formal ledgers had been
completed.

