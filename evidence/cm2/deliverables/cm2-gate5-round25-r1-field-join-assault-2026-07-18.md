# CM2 Gate-5 round-25 R1 candidate-field join

Date: 2026-07-18

Verdict: **4,216 strict full-dimensional `RETURN_AT_1_INNER` adaptive
candidates receive immutable candidate-local F1--F6 packets (`6/18`).  No F7
slot transfers, no complete 18-field operator block is created, and global
Gate 5 remains `4/18`, `NOT_CERTIFIED`.**

## Scope and audit correction

This leaf joins the round-25 adaptive C24 registry to the frozen selected
Gate-5 component/chart/field registries.  It is intentionally narrower than
a physical first-return partition.  The adaptive predecessor still has a
nonempty `UNRESOLVED_OUTER` cover, so the 4,216 returned inner rectangles are
only a finite candidate subcover of true R1.

The interrupted producer was audited before freezing.  Three semantic
corrections were made:

1. every new F1--F6 object is typed `candidate_local`; it contributes zero
   global roof-level maturity credit;
2. the adaptive rectangle ownership convention is explicit: lower faces are
   closed, internal upper faces are open, and only the corresponding parent
   global upper face is closed;
3. the destination-core test is correctly recorded as a strict whole-box
   classifier.  It does **not** materialize a destination-preimage boundary
   face.  F7 fails to transfer solely because the artificial adaptive dyadic
   faces have no certified characteristic-Z charge.

No old artifact, aggregate manifest, or recursive root was modified by this
leaf.

## Frozen inputs

The producer and verifier independently pin these direct inputs:

- full-core adaptive frontier producer and 60 MB raw-leaf manifest;
- physical 24-core registry producer and manifest;
- selected component chart/field-slot producer and manifest;
- selected-component F7 frontier;
- universal F5/F6 endpoint template frontier;
- all-component characteristic frontier; and
- the frozen 18-field Gate-5 schema.

The upstream replay facts used here are:

- `RETURN_AT_1_INNER = 4216`;
- source dimension at fixed parameter is two;
- every retained row has a positive parameter interval and a strict inherited
  next-collision owner;
- the step-1 singular-atom count is zero; and
- the unresolved outer cover is nonempty.

## Exact join

All 24 source cores bind injectively to selected maximal components.  Exactly
16 roof-one source bindings occur among the 4,216 returned candidates, and
the returned candidates land in exactly 16 destination cores.  The source
and destination histograms are independently frozen by canonical SHA-256.

The candidate depths are:

| adaptive depth | candidate count |
|---:|---:|
| 13 | 304 |
| 14 | 2,588 |
| 15 | 1,324 |
| **total** | **4,216** |

For each candidate the leaf materializes six independently addressed local
slots:

1. **F1 domain proof.**  The positive adaptive `(t,p,s)` rectangle is stored
   with an exact half-open ownership convention and its typed parameter
   guard.
2. **F2 homogeneity table.**  R1 is a one-row `H0 -> H0` physical table with
   zero intermediate solid collisions and zero transparent-wall levels.
3. **F3 prefix chart.**  The roof-zero source chart is inherited under
   restriction from the selected-component immutable slot.
4. **F4 suffix chart.**  The roof-zero target chart is inherited under the
   same restriction.
5. **F5 inverse unstable Jacobian.**  The frozen universal adapted bound
   `144000/180337` (Euclidean comparison `27410400/180337`) survives domain
   restriction.
6. **F6 log distortion.**  The frozen `1/3`-Holder template gives canonical
   curve log variation `< 3/200000`, again by restriction monotonicity.

This yields exactly `4216 * 6 = 25296` candidate-local immutable slots and
4,216 one-row candidate-local physical homogeneity tables.  The invariant
area Jacobian `1` and area distortion `0` from the adaptive predecessor are
explicitly **not** used as unstable F5/F6 data.

The canonical packet-row digest is
`05c0a66e952d76e05638efe025240fad8bf9f6930202147d3b63e3d307f83b8c`.
The result internal replay digest is
`f87526e39e668a1c17c8410d59d115eaba62a053a6633a9156fd598181e53db3`.

## F7 and nonpromotion

The parent selected-component F7 slot is retained only as provenance.  Every
R1-inner candidate has an artificial adaptive face, while the frozen parent
characteristic theorem charges only the physical word/component boundary
grammar.  Therefore:

- materialized R1 candidate-local F7 slots: `0`;
- complete 18-field R1 operator blocks: `0`;
- complete full-R1 operator: `NOT_CERTIFIED`;
- return-wide three-CM2-norm intertwiners: `NOT_CERTIFIED`;
- induced strong Lasota--Yorke coefficient: `NOT_CERTIFIED`;
- global Gate-5 maturity before/after: `4/18 -> 4/18`;
- Gate 5: `NOT_CERTIFIED`; and
- CM2: `NO-GO_FOR_CLAIM`.

Thus `6/18` is a candidate/local statement only.  It is not a Gate-5 maturity
update and must not be aggregated as one.

## Fail-closed verification

The verifier pins and rehashes the producer plus every declared dependency,
rejects symlinks and path escape, rejects duplicate/nonfinite JSON, replays
the producer, and independently audits all 4,216 packets against the frozen
adaptive raw rows.  For every packet it reconstructs the homogeneity ID, all
six slot IDs, the source-box digest, guard, parent F3/F4/F7 bindings, F5/F6
bounds, and packet ID.  It also independently recomputes all counts,
histograms, row digests, the 18-field maturity ledger, and strict
nonpromotion flags.

Reproduction commands:

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python -m py_compile \
  deliverables/cm2_gate5_round25_r1_field_join_cert.py \
  deliverables/cm2_gate5_round25_r1_field_join_verifier.py

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round25_r1_field_join_verifier.py --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round25_r1_field_join_verifier.py --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round25_r1_field_join_verifier.py --self-test

# Expected fail-closed live verdict: exit 2.
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round25_r1_field_join_verifier.py

sha256sum -c \
  deliverables/cm2-gate5-round25-r1-field-join-manifest-2026-07-18.sha256
```

The final frozen run passes integrity and full replay; hostile tests pass
`75/75`.  Live mode exits `2` by design.
