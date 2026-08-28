# Round306B1AF4K1 semantic theorem-kernel independent receipt

Status: `GO_EXACT_MECHANICAL_CHECKER_FOUNDATION__ZERO_FORMAL_CREDIT`.

Decision: `GO_ONLY_ZERO_CREDIT` for the exact K1 artifact below.  This is a
receipt for a finite executable-checker foundation.  It is not a normalized
support theorem, representation-cover theorem, formal B1A, B2 authorization,
D02 clearance, component-maximality proof, or CM2 claim.

## Exact target and direct dependency pins

| Role | File | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| K1 target | `cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py` | 68,346 | `17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae` |
| Direct symbolic-kernel dependency | `cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py` | 87,237 | `c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f` |
| Direct semantic-wire dependency | `cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py` | 84,392 | `5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f` |

The independent verifier opens all three files before the first hash, requires
regular files with link count one, uses `O_NOFOLLOW`, hashes every held file
descriptor twice, and performs a final all-path identity check before closing
any source descriptor.  This receipt pins the two *direct* K1 dependencies;
it does not claim to have sealed their complete transitive dependency closure.

## Independent-verifier boundary

The runtime verifier is:

```text
filename=cm2_round306b1af4k1_source_g_semantic_theorem_kernel_independent_verifier.py
bytes=47157
sha256=1271a2c4c5839a71f838b8277f1e7cd8ba228fa27f3d05ae9253bbbce84c80ad
```

The parent process holds and double-hashes its own source descriptor.  From
that exact descriptor and the exact three source descriptors it creates a
private `/tmp` snapshot containing four mode-`0400` files under a mode-`0500`
directory.  K1 CLI checks and the black-box worker run only from this snapshot.
The worker executes `runtime_verifier.py`, a byte-identical copy of the held
runtime verifier, rather than reopening the verifier in `deliverables`.
After the worker returns, both the source verifier descriptor/path and the
snapshot copy are rehashed and identity-checked.  The isolated run leaves
exactly the four expected snapshot files and zero unexpected regular files.

The verifier deliberately loads the exact pinned K1 module bytes and calls its
public checker functions as black boxes.  It independently validates the CLI
JSON envelopes, canonical serialization, input commitments, and result
rehashes.  It is **not an independent mathematical implementation** of K1's
symbolic, interval, partition, trace, ChartMap, owner, or DAG algorithms.

## Exact checks

The three public success modes returned canonical one-line ASCII JSON with
exit code zero and empty stderr:

- `--print-contract`
- `--self-test`
- `--verify-dependencies`

Five empty/unknown/candidate/production argv shapes returned silent exit code
one.  K1's pinned self-test reported and the outer verifier required:

- built-in adversarial certificates: `25 / 25` rejected;
- contract mutations: `13 / 13` rejected;
- entry-snapshot mutation regressions: `2 / 2` passed;
- canonical-input-bound built-in results: `9`;
- built-in distinct-certificate/different-digest pairs: `2`;
- all filesystem/output boundary probe counts: zero.

The black-box worker supplied two valid, mechanically equivalent-summary
certificates in each of seven checker categories:

1. rational box partition;
2. regular one-sided trace;
3. codimension-two empty disposition;
4. mixed boundary-face partition;
5. ChartMap bijection;
6. member/representation owner bookkeeping;
7. proof-bundle DAG validation, including `required_roles`.

For all `7 / 7` categories, the two canonical inputs produced different input
commitments and different final check digests.  The outer verifier independently
reconstructed every canonical input commitment and rehashed every result body.
It also required rejection of `8 / 8` strict JSON/Python type conformance cases,
including bool/int aliases and non-JSON/noncanonical payload types.  The attack
receipt records only case type, variation class, and outcome; it contains no raw
case payloads.

## Receipt hashes

| Receipt | File SHA-256 | Object self SHA-256 |
| --- | --- | --- |
| `..._result.json` | `e9ff89a5d51f5e79864f10dc34dd4b5f12887c029f65c2196c60f50bd4c77b21` | `547761e48d18f68fa44b31e1d633e6cb43368a1ad9075c604893503673b3edbf` |
| `..._attack_suite.json` | `1a4ba16a64dd0001592ce21db00b4dac26a43083b9ac82b42d65ff4c679fd9e5` | `ef91d9392a26c7fb28fe3e132b9f3ed28ee8675c6b3ebc476045040ea48efefc` |
| `..._verification.json` | `4d1d5d20d7f61906262486582b9cb407935f6b883989165b7a7938994fedf0d8` | `a0225f33100b0aa45a2be6f57582f2b16ad08c455761bc08ccc2fad5091578cd` |

The verification object binds the result, attack receipt, runtime verifier,
K1 target, and direct-dependency pin transaction.  Documentation is bound only
by the external manifest, avoiding a self-reference cycle.

## Resource and availability boundary

K1 has explicit finite structural bounds, but this package proves **no runtime
or maximum-RSS upper bound** for intermediate differentiation, substitution,
interval evaluation, or atom enumeration.  Those intermediate operations may
exhaust time, memory, recursion, or process resources before a public checker
returns.  Any such exhaustion terminates before a valid checker result and
before the outer verifier emits its final bundle; it cannot mint formal credit.
Observed completion of the small receipt fixtures is not an availability
theorem for arbitrary admissible inputs.

## Credit boundary

```text
normalized_support_credit=0
representation_cover_credit=0
physical_incidence_credit=0
transition_credit=0
pair_routing_credit=0
maximality_credit=0
fibre_credit=0
global_disposition_credit=0
B1A_credit=0
B2_credit=0
D02_credit=0
CM2_credit=0

B1A=BLOCKED
B2=NOT_AUTHORIZED
D02=BLOCKED
CM2=NO-GO_FOR_CLAIM
```

The next strict-critical-path work remains construction-source/full-support
reconstruction and a formal B1A package.  This K1 receipt does not authorize
skipping directly to B2.
