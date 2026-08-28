# Round300-B cold replay

Run from the workspace root with the frozen deliverables directory unchanged.
`python-flint` 0.9.0 was used.

## Producer

```sh
uv run --with python-flint python \
  deliverables/cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure.py
```

Expected embedded result SHA-256:

```text
45f5009669c7cc9df1a851195b3ebf84d1bff489836e327834f11ccf905586d7
```

The producer reconstructs from sealed upstream files and does not read the
Round299C-boundary or Round299D zero-credit diagnostics.

## Independent alpha replay

```sh
/usr/bin/time -f 'elapsed=%e maxrss_kb=%M exit=%x' \
  uv run --with python-flint python \
  deliverables/cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_verifier.py \
  --seed round300b-alpha
```

Observed:

```text
PASS_INDEPENDENT_CACHELESS_ROUND300B__62548_FACES__10416_NOVEL_EDGES__ZERO_UNRESOLVED__36_OF_36_ATTACKS_REJECTED__ZERO_DSU_RANK_CREDIT
verification_sha256=51087612fba9a5b741d2be8423c36ac3d60670f006ecd7b162370e7afe602107
elapsed=912.48 maxrss_kb=11642344 exit=0
```

## Independent beta replay

```sh
/usr/bin/time -f 'elapsed=%e maxrss_kb=%M exit=%x' \
  uv run --with python-flint python \
  deliverables/cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_verifier.py \
  --seed round300b-beta \
  --output \
  deliverables/cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_verification_seed_beta.json
```

Observed:

```text
PASS_INDEPENDENT_CACHELESS_ROUND300B__62548_FACES__10416_NOVEL_EDGES__ZERO_UNRESOLVED__36_OF_36_ATTACKS_REJECTED__ZERO_DSU_RANK_CREDIT
verification_sha256=0d0700b8bf93571bf4d70ebc41faa417a784d4f592cc901529f398f31c4bc22a
elapsed=907.72 maxrss_kb=11641244 exit=0
```

## Compare seed-invariant commitments

```sh
for file in \
  deliverables/cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_verification.json \
  deliverables/cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_verification_seed_beta.json
do
  jq -cS '{
    status,
    reconstructed_census,
    independent_commitments,
    attack_results_sha256:.attack_execution.attack_results_sha256,
    strict_nonclaims_reconfirmed
  }' "$file" | sha256sum
done
```

Both lines must be:

```text
aaef8e141e49cbe81f4e5f910d769ee5ffe47da6b5acec51a4028aa4e2284db5
```

The seed changes only validation order. No producer execution, producer
parsing, memoized reconstruction result, or zero-credit diagnostic ledger is
used by the verifier.

