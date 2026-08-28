# Round306B1AF4K1 independent-receipt cold replay

This record covers the exact verifier SHA-256
`1271a2c4c5839a71f838b8277f1e7cd8ba228fa27f3d05ae9253bbbce84c80ad`
and target SHA-256
`17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae`.

## Replay command

From the workspace root, each cold run used:

```bash
replay_root=$(mktemp -d /tmp/cm2-k1-replay.XXXXXX)
python3 -I -B \
  deliverables/cm2_round306b1af4k1_source_g_semantic_theorem_kernel_independent_verifier.py \
  --bundle > "$replay_root/bundle.json" 2> "$replay_root/stderr"
```

The verifier internally creates a separate private `/tmp` tree for each run,
copies the held-FD-pinned K1 target, its two direct dependencies, and its own
exact verifier bytes into a four-file read-only snapshot, then runs every K1
CLI and black-box worker check from that snapshot.  Random temporary pathnames
are never included in receipt data.

## Two-run byte identity

Two independent invocations both returned exit code `0`, empty stderr, and:

```text
bundle_bytes=10360
bundle_sha256=ca5cdb60324841765ed16f89ce1a74d31da1445ae0554961f7a2bdcdd73eed60
run_1_vs_run_2_cmp=BYTE_IDENTICAL
```

The bundle contains exactly `result`, `attack_suite`, and `verification`.
Their extracted canonical file commitments are:

```text
result_file_sha256=e9ff89a5d51f5e79864f10dc34dd4b5f12887c029f65c2196c60f50bd4c77b21
attack_suite_file_sha256=1a4ba16a64dd0001592ce21db00b4dac26a43083b9ac82b42d65ff4c679fd9e5
verification_file_sha256=4d1d5d20d7f61906262486582b9cb407935f6b883989165b7a7938994fedf0d8
```

These equal the three promoted JSON receipt files byte for byte.  The verifier
also reported exactly four expected read-only snapshot files and zero
unexpected regular files in each isolated execution tree.

## Recheck commands

```bash
sha256sum \
  deliverables/cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py \
  deliverables/cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py \
  deliverables/cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py \
  deliverables/cm2_round306b1af4k1_source_g_semantic_theorem_kernel_independent_verifier.py \
  deliverables/cm2_round306b1af4k1_source_g_semantic_theorem_kernel_result.json \
  deliverables/cm2_round306b1af4k1_source_g_semantic_theorem_kernel_attack_suite.json \
  deliverables/cm2_round306b1af4k1_source_g_semantic_theorem_kernel_verification.json

python3 -I -B \
  deliverables/cm2_round306b1af4k1_source_g_semantic_theorem_kernel_independent_verifier.py \
  --bundle
```

The second command writes only its canonical bundle to stdout.  Any pin,
CLI, type, entry-snapshot, commitment, rehash, isolation, or self-snapshot
deviation causes nonzero termination before a final bundle is printed.

## Evidence and availability boundary

The replay records content, exit status, and byte identity only.  It makes no
authenticated elapsed-time or peak-RSS claim.  In particular, neither K1 nor
this receipt establishes a runtime or RSS upper bound for intermediate
differentiation, substitution, interval evaluation, or atom enumeration.
Resource exhaustion before a checker returns yields no accepted result and
mints no formal credit.

Both cold runs therefore support only `GO_ONLY_ZERO_CREDIT`.  Formal B1A,
B2, D02, and CM2 remain blocked/not authorized exactly as recorded in the
verification object.
