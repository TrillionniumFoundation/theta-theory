# CM2 Round306 C49 D02-B v2 adversarial rejection and v3 supersession

Status: **V2 REJECTED AS PURE/FAIL-CLOSED; V3 SUPERSEDES V2 FOR DIAGNOSTIC USE; ZERO FORMAL CREDIT**.

## Why v2 is rejected

The frozen v2 files remain byte-preserved for provenance, but their PASS label
is superseded by this rejection.  Adversarial review found five contract
failures:

1. History rows supplied only an owner and evidence digest.  They did not
   supply the evidence preimage, so v2 could not authenticate a prior step's
   self-hash, full candidate table, unique owner, root order, or evidence body.
2. `source_binding_sha256` was accepted without the complete source-binding
   preimage and without validating that preimage against an authority pin.
3. `_REGISTRY_CACHE` and `_CORES_CACHE` were module globals written during
   proof execution.  Cold, warm, and poisoned-cache semantics were therefore
   not established by the public contract.
4. The v2 self-test consisted of asserted literal booleans rather than
   executed negative attacks against forged evidence and history splices.
5. Inputs were embedded without an explicit deep-copy ownership boundary, and
   the v2 auditor's “independent” wording exceeded its actual producer-import
   structural/replay scope.

Therefore v2 must not be used as a pure authenticated continuation primitive,
must not mint D02 credit, and must not be promoted.  Its producer SHA-256 is
`25d87f0ae27b7946ab9f55dbe8a5f50c353eb9f05dd4a6e50810d92e438700df`.

## V3 supersession

V3 is a new file and does not overwrite v2:

- `cm2_round306c49_d02b_pure_advance_one_collision_v3.py`
- producer SHA-256:
  `2f603c17f634ac1d5dca9763235f41e7a0259e0b384daa7d7c95cea63704a705`.

V3 changes the public input semantics as follows:

- the original box contains the complete, self-hashed source-binding preimage;
- every history row contains its complete genesis or prior-step evidence
  preimage;
- each prior step's object self-hash, evidence hash, candidate-table hash,
  frozen candidate order, unique owner, discriminant, strict root order, and
  appended handoff row are recomputed;
- collision indices must be contiguous and equal their authenticated history
  positions;
- occurrence identity, parent handoff, source preimage, adaptive suffix, and
  prior-to-next closed-box geometry are chained;
- a refinement suffix is accepted only when it is an exact shuffle of the t
  and p dyadic descendant bits of the stated parent box;
- both public inputs are deep-copied before validation and output objects are
  deep-copied before sealing;
- numeric registry and core authorities are call-local.  No kernel cache or
  module global is written.

The pair-9 source-binding preimages are independently frozen at:

- reflected: `d9d1ad4f4bf856764733d8f1f8360e51f8f003572104e868eb445e90c6073482`;
- representative: `486f959429f2b69440e0c68349c308eb07060303185536e3c771188658ab5dab`.

## Executed adversarial acceptance

The v3 self-test executed, rather than asserted, ten attacks.  All passed:

- forged evidence preimage rejected;
- self-rehashed source-binding mismatch rejected;
- history splice rejected;
- candidate/owner binding mismatch rejected after resealing the forged step;
- malformed closed box rejected;
- malformed adaptive suffix rejected;
- cold and warm outputs byte-identical;
- poisoned-cache output byte-identical to the clean output;
- poisoned cache objects unchanged by the kernel;
- caller mutation after return unable to alter the sealed output.

Executed adversarial-test object SHA-256:
`3410953c101dca1c615ef52189c65f6209a979db23ce4666c1b952a28bd4850c`.

The structural auditor imports v3 and is explicitly **not** a numeric
independent implementation and **not** D02-C.  Its audit object SHA-256 is
`379d587ef6d7b99fc5f735b8f856f1be1b98ece65b3db065bdfe585ae5bddd60`.

## Credit and authority effect

V3 is still diagnostic.  Every locally complete collision-3, collision-4,
and collision-5 step returns `PENDING_GLOBAL_ORACLE`, names both missing global
oracles, and has `formal_credit=0` and `D02_credit=0`.  Bounded unresolved
steps also have zero credit.  No C42, C46, C47, pointer, receipt, seal, or
canonical status was modified.
