# CM2 Gate 3/4 physical first-return partition interface — 2026-07-18

## Strict result

This append-only leaf materializes the strongest currently admissible raw
interface toward

\[
R_n=M_C L(M_{C^c}L)^{n-1}M_C,
\qquad
Q_n=(M_{C^c}L)^nM_C.
\]

It does **not** certify a physical source/core first-return partition, a mass
identity, a tail, or an induced operator.

## New raw payload

The manifest contains 128 canonical charged entrance rows.  Each row records
the exact occurrence/side, source chart, dyadic `(z,h)` box, source-owner and
first-stopping IDs, suffix-relative first-core time and destination, complete
itinerary/classification digests, candidate Borel slot, dimensions, and mass
typing.

The replay certifies:

- 128 charged entrance raw atoms and 128 unique charged first-core events;
- suffix-relative first-core time histogram
  `2:44, 3:20, 4:16, 7:16, 8:8, 9:8, 16:4, 19:8, 20:4`;
- 14 destination cores;
- exact total labelled `dz dh` area equal to the preceding all-occurrence
  charge and strictly between `2^-153` and `2^-152`.

The manifest also contains four canonical local induced-candidate rows:

- three typed local `R_n` candidates at `n=545,649,1531`;
- one typed censored `Q_2018` candidate;
- two distinct source cores, hence 22 frozen cores have no local candidate at
  all;
- exact labelled four-box `dz dh` area `2^-15996`.

These are typed candidate atoms, not transfer-operator branches.

## Newly exposed domain-join obstruction

The 128 earlier Borel ledgers are registered on the 64 original full
`(z,s,h)` all-scale germs.  Rechecking exact interval containment gives:

- the original two occurrences, four parameter sides: charged boxes strictly
  contained in their registered germs, so four typed ledger/first-core-slot
  attachments are admitted;
- the other 62 occurrences, 124 parameter sides: charged `z` intervals lie
  outside the occurrence-matched registered germ intervals, so the
  occurrence-only ledger join is rejected.

This is a typing failure, not a failure of the 124 Arb trajectory proofs.
Those boxes remain valid local charged first-core atoms, but require their own
domain registrations before they can inhabit a Borel first-event ledger.
Occurrence ID is an owner key; it is not an equality proof for source domains.

All four admitted typed slots have suffix-relative time 20 and therefore lie
after the materialized horizon-eight ledger prefix.

## Physical mass obstruction

The frozen physical source carrier `C24` is a union of 24 two-dimensional
collision-section rectangles and has normalized collision-SRB mass strictly
larger than `147/550000`.

Every available charged or local box is parameterized by `(z,h)` with the
other source phase coordinate fixed.  At a fixed parameter it gives a
one-dimensional regular analytic source curve in the two-dimensional
collision section.  A finite union of such curves has collision-SRB area
zero.  Consequently:

- positive labelled `dz dh` area is not collision-SRB mass;
- the current local candidate union has fixed-parameter collision-SRB mass
  zero;
- it cannot cover any positive-area core rectangle;
- the uncovered `C24` collision-SRB mass retains the strict lower bound
  `147/550000`.

This obstruction concerns the current finite materialization only.  It does
not refute a future full-dimensional partition.

## Exact missing interface

A physical raw atom still needs, at minimum:

1. a full two-dimensional source-core domain;
2. the complete collision word and strict unique-owner margin at every step;
3. strict preterminal separation margins from all 24 cores;
4. first return time and destination;
5. a singular/unresolved outer cover and survivor parent/first-failure guard;
6. collision-SRB mass `m_i`;
7. return-map Jacobian and distortion;
8. strong envelope `q_i`;
9. a common forward/reverse restriction ID.

Until those fields cover `C24`, neither

```text
mu_C = sum finite-return m_i + singular-cemetery mass + survivor mass
```

nor

```text
sum_{tau>n} q_tau <= C rho^n
```

is evaluable.  A new induced Lasota–Yorke coefficient therefore cannot yet be
derived.

## Frozen artifacts

- `cm2_gate34_physical_first_return_partition_interface_cert.py`
- `cm2_gate34_physical_first_return_partition_interface_verifier.py`
- `cm2-gate34-physical-first-return-partition-interface-manifest-2026-07-18.json`
- this report
- `cm2-gate34-physical-first-return-partition-interface-manifest-2026-07-18.sha256`

No preceding artifact is modified by this leaf.

## Verification

Run from the workspace root:

```bash
.venv-neurips/bin/python -m py_compile \
  deliverables/cm2_gate34_physical_first_return_partition_interface_cert.py \
  deliverables/cm2_gate34_physical_first_return_partition_interface_verifier.py

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_physical_first_return_partition_interface_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_physical_first_return_partition_interface_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_physical_first_return_partition_interface_verifier.py \
  --self-test

sha256sum -c \
  deliverables/cm2-gate34-physical-first-return-partition-interface-manifest-2026-07-18.sha256
```

The verifier rejects 64/64 hostile mutations, including false domain joins,
turning zero-dimensional physical mass into the positive labelled area,
promoting a curve to a core rectangle, swapping `R_n/Q_2018` typing, changing
return times, declaring the censored box cemetery, manufacturing `m_i/q_i`,
and promoting Gates 3/4/5.  Default live mode exits `2` by design.

## Strict verdict

```text
CHARGED_ENTRANCE_RAW_ATOMS_128: CERTIFIED
TYPED_EXISTING_GERM_LEDGER_SLOT_ATTACHMENTS_4: CERTIFIED
OCCURRENCE_ONLY_LEDGER_DOMAIN_MISMATCHES_124: CERTIFIED_REJECTED
LOCAL_RN_CANDIDATE_ATOMS_3_AND_Q2018_CANDIDATE_1: CERTIFIED_TYPED
CURRENT_ATOMS_FIXED_PARAMETER_COLLISION_SRB_MASS_ZERO: CERTIFIED
PHYSICAL_SOURCE_CORE_FIRST_RETURN_PARTITION: NOT_CERTIFIED
COLLISION_SRB_MASS_CONSERVATION: NOT_CERTIFIED
QUANTITATIVE_EXCURSION_CEMETERY_TAIL: NOT_CERTIFIED
INDUCED_STRONG_OPERATOR: NOT_CERTIFIED
GATE3: NOT_CERTIFIED
GATE4: NOT_CERTIFIED
GATE5: NOT_CERTIFIED
```
