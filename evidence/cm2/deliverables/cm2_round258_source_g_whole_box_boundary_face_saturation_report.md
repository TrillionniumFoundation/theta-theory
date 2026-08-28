# CM2 Round258 — Whole-Box Boundary-Face Saturation

## Result

- Reconstructed all `27,288` distinct-component, same-chart, same-key positive-area box-face candidates from the complete Round256 occurrence frontier.
- Full ten-field return-signature comparison rejects `12,548` candidates with zero glue credit.
- Exact upstream geometry classification leaves `904` candidates whose two occurrence regions each fill their entire strict-open box. Every accepted face has an identity chart transition, exact positive common area, equal ten-field signature, and explicit positive-volume corridors on both sides.
- The accepted faces cover `852` distinct Round257 component pairs: `468` are rank reducing and `384` are redundant independently certified connectivity.
- The unified quotient drops from `74,012` to `73,544` components while remaining memberwise exact-key pure.
- Accepted-axis census is `296` x-faces, `384` y-faces, and `224` z-faces. The exact accepted face-area sum is `4699647/81920000`; total two-sided corridor volume is `521900961/3355443200000`.
- The remaining `13,836` candidates have equal complete signatures but at least one curved-region occurrence lacks certified positive-area occupancy of the candidate box face. They remain fail-closed with zero glue credit.

## Independent Verification

- The verifier does not import or execute the producer.
- It independently rebuilds all `53,968` occurrence geometries and signatures, enumerates all `27,288` faces, checks every accepted/rejected/deferred row, reruns the DSU, and verifies the complete component, occurrence, and key frontiers.
- Independent status: `PASS_INDEPENDENT_ROUND258`.
- Hash seeds `258071` and `258929` reproduce byte-identical producer and verifier JSON outputs.

## Strict Boundary

- Box-face contact and exact-key equality alone never receive glue credit.
- All `12,548` complete-signature mismatches are strictly rejected.
- The `13,836` curved-region rows are not promoted until exact face occupancy and strict two-sided corridors are materialized.
- Round258 adds known physical connectivity but does not prove any component maximal.
- Maximal physical-component assignments remain `0 / 53,968`; exhausted exact-key fibres remain `0 / 116`; global dispositions remain `0 / 224,580`.
- Gate5 remains `10 / 18`; CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

Materialize exact face occupancy for the `13,836` same-signature curved-region candidates using their Round204 target graphs and Round208 factor-region geometry. Accept only positive-area common refinements with strict two-sided corridors, then rebuild the quotient before starting the pinned cross-chart transition audit.
