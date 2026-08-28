# CM2 C65s18 64-shard aggregate cold verifier v8 — terminal rejection

Date: 2026-08-13 (Asia/Shanghai)

Status: `REJECTED_SELFTEST_VALIDATOR_124_VS_127__FORMAL_PREFIX_8_OF_11__ZERO_CREDIT`

The frozen v8 verifier is terminally rejected. It must not be edited, rerun,
released, or cited as a completed formal verification.

## Frozen source and launch

- Verifier SHA256:
  `129daca794ea269cf932b5cdb3148242ddcba86f9366d6cc0f9597eb0e13b0c4`
- Pinned entry SHA256:
  `2a19c3c33e2823a83d2ffbf0939b58f6168dbe508517484eeab4d2cd321c92a0`
- Successful dual-launch invocation:
  `f11919b0d7e74fc69f9b98efd6d667b9`
- Dual-launch terminal object SHA256:
  `cfc75bd98a24e94ad2ab58cf72d1b03a2ca7ccfdd5b7150c35f8ac4639b46347`

The dual launch completed without OOM, restart, signal, or worker failure and
published an exact 4/11 prefix. The original external continuation then failed
closed before `--install` because it compared systemd's numeric
`ExecMainCode` against the word `exited` and observed a collected transient
unit with a blank invocation ID. That orchestration failure did not invalidate
the four launch artifacts and did not run a formal phase.

## Deterministic verifier contradiction

A no-rerun successor independently revalidated the exact 4/11 boundary and
ran the frozen held-entry phases. `--install` succeeded and published the exact
6/11 boundary. `--publish-self-test` constructed and published a complete
127-test self-test and its completion receipt, then returned nonzero during its
own post-publication recapture with:

`self-test exact schema/status/tests`

The successor source SHA256 was
`3765e2eeb54fe885a5e45358d37d852000c054c876b01e3f37e40a3c4a04b336`.
Its systemd invocation was `1264b419921e4145a7556a8928e9b870` and its
terminal log SHA256 was
`bd22797d73b4681393ec0909d80a099d5c5e6982b73f112b41c11ae8aa38e91e`.
It ran from 13:36:12 to 13:36:45 CST, exited 1 with no restart, used
31,876,529,000 CPU ns, and reached a 1,572,495,360-byte memory peak. The log
records the successful `--install` terminal object
`025d98c96771bca53bdd43e9f8e55fbece4fea411c1a8488e827e547daebd5c2`
followed by the exact validator rejection at formal prefix 8.

The contradiction is internal to the frozen v8 source:

- `EXPECTED_SELFTEST_KEYS` contains 127 keys.
- `self_test()` requires those 127 keys and emits status `PASS_127_OF_127...`
  with `test_count = 127`.
- `validate_selftest()` still requires status `PASS_124_OF_124...` and
  `test_count == len(tests) == 124`, while simultaneously requiring the
  127-key `EXPECTED_SELFTEST_KEYS` set.

Consequently `validate_selftest()` is unsatisfiable. `release()` invokes that
same validator on its prerequisites before publishing replay, manifest, or
outer receipt, so v8 cannot safely progress from 8/11 to 11/11. Invoking
`--release` is forbidden.

The external successor also had a post-11 audit-only path-resolution defect
for the logical manifest surrogate `machine-runtime/usr/bin/python3.12` and
overly generic resume checks. Neither path was reached: the frozen verifier
stopped at 8/11 first. The successor must never be rerun or treated as a
formal verifier.

## Exact retained 8/11 prefix

All eight files are regular single-link canonical JSON objects with valid
top-level object closures and zero formal, whole-parent, and D02 credit.

- seed1 projection:
  `c0b032f33f54a31fec45d19e59d4d6a81e8abc5f67dfbdfda5c243cb2ca2aa50`
- seed1 completion receipt:
  `596c76772ff61dc16db9df8611c25c087e0be2b0db00f625d3a67f4728dd8125`
- seed2 projection:
  `c0b032f33f54a31fec45d19e59d4d6a81e8abc5f67dfbdfda5c243cb2ca2aa50`
- seed2 completion receipt:
  `861d16dec40f65c3fd710fb8d1068f295d1202f7b760a81fb29e6c7779c0ccf2`
- verification:
  `adaaa1aaf312cc42f35a20ee202a9c46dd20d4dfd1df05669d470bcc34408089`
- verification completion receipt:
  `fda8c0a48b79d94bb68e7791324753d56a587222bc255b9f0baf64aec6182b5d`
- self-test:
  `310f5bd9578d2e39a6d5f8eeb67369538222ed1ba95ab81874fbb41af6d6396b`
- self-test completion receipt:
  `1f689f8bd772ff8493dfbb148e324ba493e5b5ae2a2886e1123809a445499f11`

The verification object SHA256 is
`025d98c96771bca53bdd43e9f8e55fbece4fea411c1a8488e827e547daebd5c2`.
The published self-test object SHA256 is
`beb11178cb14414af3516200cb39f37b87e7432e4393fc4d27c4aa7be8fa4634`.
The remaining v8 replay, manifest, and outer receipt are absent.

## Successor rule

Any successor must use a new protocol/source version, bind this rejection and
the rejected v8 source hash, keep all v8 formal artifacts out of the successor
release manifest, and make the self-test producer and validator agree on the
same exact key count, key-set digest, and status. No v8 artifact carries
authority or positive credit.
