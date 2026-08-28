# C30a fresh offline python-flint runtime rebuild

Status: `PASS_FRESH_OFFLINE_RUNTIME_REBUILT_AND_INDEPENDENTLY_ATTESTED`.

This is supplemental runtime evidence only. It adds no mathematical credit,
does not alter the original C30a 13-member seal, and does not change the
fail-closed Source-W boundary `252 -> 92`.

## Rebuild boundary

- The target
  `.cm2-runtime/audit/c30a-p0-closure-verifier-20260807/fresh-python-flint-0.9.0`
  was absent immediately before the run.
- The orchestrator exclusively created every target/evidence path. It contains
  no cleanup, deletion, or overwrite operation.
- Every subprocess received exactly `HOME=/nonexistent`, `LC_ALL=C.UTF-8`, and
  `TZ=UTC` through `env -i` semantics.
- The venv was created by pinned `/usr/bin/python3.12 -I -B -m venv --copies`.
- Installation used the sealed wheel offline with `--no-index --no-deps
  --only-binary=:all: --require-hashes`; every required argv is preserved in
  `fresh_runtime_rebuild_descriptor.json`.
- Freeze is exactly `pip==24.0` and `python-flint==0.9.0`. Its preserved stderr
  is the expected non-fatal pip cache warning for `HOME=/nonexistent`; the
  stage exited 0. Creation, installation, attestation, and outer invocation
  stderr are empty.

## Independent attestation

The new attestor does not import or execute a C30 producer or verifier. It
independently pins and checks:

- machine CPython 3.12.3 SHA-256
  `1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118`;
- runtime lock SHA-256
  `ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79`;
- requirements lock SHA-256
  `cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c`;
- sealed wheel SHA-256
  `376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76`;
- glibc 2.39 and the wheel's two manylinux/cp310-abi3 compatibility tags;
- all 112 hashed wheel RECORD entries plus the sole RECORD self-row;
- all 114 hashed installed RECORD entries, 25 permitted unhashed generated
  entries, and exact physical closure of all 139 owned installed files;
- 39 extension modules, three bundled native libraries, python-flint 0.9.0,
  FLINT 3.6.0, and FLINT release 30600.

The canonical attestation is 30,193 bytes with SHA-256
`642acd5cb6e459297759cf8bc496f162a2824060c09dc5f514d1ad9e9b113634`
and payload SHA-256
`6250c44eb684891d1997d3f01dc498af1b75710faa1f3ac90637c998d6b36ec0`.
An independent second invocation exited 0 with empty stderr and produced the
same 30,193 bytes exactly.

## Evidence entry points

- `deliverables/cm2_round306c30a_python_flint_fresh_runtime_attestor.py`
- `deliverables/cm2_round306c30a_python_flint_fresh_runtime_rebuild.py`
- `deliverables/cm2_round306c30a_python_flint_fresh_runtime_completion.json`
- `.cm2-runtime/audit/c30a-p0-closure-verifier-20260807/fresh_runtime_rebuild_descriptor.json`
- `.cm2-runtime/audit/c30a-p0-closure-verifier-20260807/fresh_runtime_attestation.json`
- `.cm2-runtime/audit/c30a-p0-closure-verifier-20260807/fresh_runtime_attestation_recheck.json`

The original C30a manifest SHA-256 remains
`0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc`,
and a post-run `sha256sum -c` still passes all 13 members.
