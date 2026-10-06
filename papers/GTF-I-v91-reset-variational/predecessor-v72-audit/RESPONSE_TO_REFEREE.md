# Response to the v71/r46 reports — Revision 72

**Quantitative manuscript:** Observable Readout Geometry and Reusable Instrument Descriptions.
**Companion:** Finite Physical Actions and a Strong Converse for Repeatable Observations.

**Controlling report:** `b78c1dddd41de645edf207bc415406b3fc1b5e83`, reviewing v71 final head `8c053f4820da3abcbb04daab628aa94379fd01e3`.
**Companion audit:** `43e6713de2aa65f65e649df7cd90e2a95fc83a06`.

The reports found no fatal defect in the inspected v70/v71 proof chains and identified the varying-readout boundary and direct environment-state antecedents as substantive issues. We respond by proving an additional mixed-scale law, giving a direct exact rational codec, and stating a family-covering consequence of uniform environment seizing. The general-journal mathematical objective is unchanged. No old theorem is weakened or deleted to obtain a more favorable claim.

## Principal mathematical response

The new family measures an ordered rank-one projective readout and emits its label together with a conditional prepared state. The rank bounds allow singular states, zero blocks and changing output supports. With flag dimension b=d^2-d and conditional rank dimension V=sum_x(sum_y r_xy(2n-r_xy)-1), Section 47 proves

    log2 covering number = (b+V/2)log2 N + (b+V)log2(1/delta) + O(1)

uniformly over N>=1 and 0<delta<=1/32 at fixed dimensions and ranks. Arbitrary legal memoryless centres are permitted in the lower bound. Readout observability is stated in the abstract, theorem and implementation schema, not supplied implicitly by the proof. Fixed orthogonal output supports provide a second observable interface. For arbitrary unlabelled overlapping rows, an exact equal-row example shows that all basis parameters can disappear; no unsupported exponent is assigned there.

The readout scale comes from the established multiple-query projective measurement theorem, explicitly imported and cited. The conditional scale comes from the retained row-state product argument. The Cartesian packing is justified by two cases: different bases remain distinguishable after conditional outputs are discarded; equal bases with different rows are distinguished by a row-selecting input. This is not an addition of tangent dimensions without identifiability.

The upper construction selects a bounded chart by partial-pivot LU of unnormalized rational projection columns. A permutation and d(d-1) real coordinates suffice. Unnormalized Gram–Schmidt decodes legal rational projectors exactly, including rational projections with no rational normalized eigenvector. The proof gives an explicit stability constant and finite expanded bit bounds. It replaces the unfinished local v72 proposal's exhaustive flag search with a direct rational construction; the inherited v70 Givens unitary atlas is not removed.

Section 48 formulates the common seizer and processor on the whole ambient programme state space. Their composition retracts arbitrary legal memoryless centres, and the N-copy state covering number equals the instrument-family covering number at exactly the same radius. The state/channel equivalence is a credited antecedent. The contribution here is its explicit family-centre consequence, with the inherited rank-state coding law and a rational Pauli/Bell example. The transfer retains the full fixed error cap below two because it is an exact state-family identification, not an extrapolation of a coherent packing argument.

## Sixteen required revisions

| Item | Response |
|---|---|
| 1. Focused quantitative object | The focused quantitative paper contains every proof dependency of Sections 47–48, alongside the retained preliminary theorems. The complete research edition remains an archival object, not a third journal submission. The structural companion is separately complete. |
| 2. Separate v70 and v71 novelty | The introduction and proof inventory explicitly distinguish v70 coherent/preparation results, v71 fixed-readout/full-error results, and the present observable varying-readout and covering-transfer results. The r46 review is not presented as reviewing v72. |
| 3. Direct environment antecedents | The focused comparison and bibliography now include Das–Wilde Definition 3/Proposition 2, Wilde–Berta–Hirche–Kaur Definition 36/Theorem 37, and Wang–Wilde Section III.A. Their programme/seizing principles are credited before the new covering consequence is stated. |
| 4. Fixed readout in earlier headlines | The retained v71 theorem and its summaries remain fixed-readout. The new theorem explicitly changes that hypothesis to observable varying ordered projections and proves the different basis coefficient. It is not advertised as an unrestricted instrument-boundary classification. |
| 5. Fixed-dimensional convention | Page one and the resource ledger state the public dimensions, labelled outcomes, rank bounds, horizon, tolerance and cap. Chart permutations, pivot masks, anchors and integer bodies are charged. Constants need not be uniform in growing dimensions. |
| 6. Unhalved norm | The metric is defined before its first use; its range is [0,2], and probability changes are at most half the displayed norm. The old multiplicity proof retains that factor. |
| 7. Retraction versus ranks | The new uniform-seizing retraction, like the inherited dephasing/preparation retractions, can increase Choi rank. The Pauli example demonstrates rank one becoming rank four. Only target encoding preserves the specified ranks and zeros. |
| 8. Sandwich versus equality | The v71 all-row comparison remains a sandwich. Equality is not asserted for general N in that family. Exact equality is separately proved under the stronger uniform seizing premise in Section 48. |
| 9. Separate error ranges | The new mixed readout and old coherent tensor laws use delta<=1/32. Interior, preparation, fixed-readout and uniformly seizable rank-state laws have each fixed cap delta_*<2. No coherent full-error extension is inferred. |
| 10. Programme hardware | The description specifies a quantum operation. The proof processor is quantum and its Hilbert-space dimension is not the reusable bit payload. |
| 11. Learning | All targets are supplied matrix data. No query/sample complexity or unknown-device identification claim is made. |
| 12. Real and rational targets | The general real-family cover uses exact-real selection and rounding to rational centres. The actual CLI processes rational projector/row inputs with exact rational/integer arithmetic. It does not claim finite access to arbitrary unspecified reals. |
| 13. Legal codebook | Every valid chart word yields a flag, and every valid factor word yields positive normalized rows. The decoder validates headers and bodies; target binding additionally requires complete canonical replay. Invalid transport objects are not certified codewords. |
| 14. Exact final head | A dedicated contents-read-only workflow is included, with source identity, immutable predecessor files, page/raster reconstruction and independent minimal-package rebuild. Its actual run and commit are reported after execution, not presumed here. No signature is manufactured. |
| 15. Independent priority | A targeted independent-review brief and primary comparison are provided. No independent human/expert report has been obtained or represented as obtained. Author-side proof work, CI and the historical referee reports cannot certify absence of equivalent formulations. |
| 16. Independent analytic graph | The frozen A/B/C/D graph is preserved. No local instrument code discharges its raw local-limit, stopped-path, past-kernel, Mosco, Nisio, filtering or response obligations; all aggregate flags remain false. |

## Twenty-six detailed comments

| Item | Treatment |
|---|---|
| 1. Definition of d_N | The focused introduction defines the metric before any displayed covering law, including references, feedback and bounded public stopping. |
| 2. Choi normalization | The retained normalized testing input uses J/d. The supplied/decoded Choi representation remains input-first unnormalized; the new formula uses P_x transpose tensor sigma_xy. |
| 3. Common event space | The full-error multiplicity proof retains one common tester and its common output sigma-algebra. New pairwise readout packing is not mislabeled as that common-estimator argument. |
| 4. Error-cap dependence | Uniformity is only at fixed cap below two. Neither Section 48 nor the old full-error law asserts a uniform constant as the cap tends to two. |
| 5. Estimator description | The retained witness is called informationally complete; it is not described as optimal tomography. |
| 6. Inverse Lipschitz chart | Compact row subpatches retain their quantitative inverse bounds. The new flag proof checks injectivity of the triangular-chart derivative and restricts to a compact subpatch. Its global upper atlas has a separate explicit singular-value bound. |
| 7. Row normalization | Each x row is separately trace normalized, accounting for the subtraction of one in each v_x. Global normalization would give the wrong dimension and is not used. |
| 8. Input versus output geometry | The old family remains fixed-basis, allowing noncommuting and singular rows. The new flag coordinate has its own proof and observable interface. |
| 9. Composition side | The old retraction is right composition on the input. The new A B construction is separately defined as a one-use superchannel with an explicitly held outer input. |
| 10. Memoryless centres | All unrestricted centre claims here concern legal memoryless instruments. No retraction of arbitrary memoryful processes is inferred. |
| 11. All-row programme | One copy of every row per slot remains a proof overhead, not a hardware or sample-cost theorem. |
| 12. One-use equality | The old one-use maximum-row equality is retained separately. Section 48's stronger all-N equality has an explicitly stronger uniform seizing hypothesis. |
| 13. Pivot masks | All row masks are charged. The new flag permutation is additionally charged by ceil(log2 d!), and its signed coordinate digits are counted. Column phases are not payload. |
| 14. Exact zero blocks | Zero preservation is checked in factor encoding, not attributed to centre retraction. The flagged Kronecker Choi assembly preserves it. |
| 15. Expanded denominator | Gram inverses and lcm denominators are expanded decoded data. They have fixed-dimensional bit bounds but are not substituted for the fixed-length payload. |
| 16. Canonical JSON | The new target verifier compares the entire canonical encoding; extra fields, changed legal digits and altered certificates are negative controls. The earlier conditional verifier is unchanged. |
| 17. Global versus column phases | The old unitary coordinate still has dimension d^2-1. The ordered readout quotient has dimension d^2-d, removing every column phase while retaining outcome order. |
| 18. Atlas complexity | The old general unitary atlas remains a finite exhaustive construction. The new flag implementation selects its chart directly from rational projections; this does not retrospectively assign an efficiency result to the old atlas. |
| 19. Pair-dependent tests | Pair-dependent eigenvectors and query counts remain legitimate for the old coherent packing. The new measurement witness also uses a pairwise metric supremum, with its full theorem credited externally. |
| 20. Coherent transition | No full-error coherent/readout theorem is claimed from the half-dimensional common estimator. |
| 21. Structural probe model | The independent structural article still uses fresh repeatable nondisturbing classical probes, not repeated measurements on an unknown quantum system. |
| 22. Authorship | Exact-head reconstruction attests source and artifact consistency. It does not provide cryptographic authorship or an independent mathematical endorsement. |
| 23. Tests versus universal proof | The new suite checks exact examples and implementations, including two-query measurement discrimination. It does not prove the imported theorem, continuum packing or all adaptive testers. |
| 24. Pipeline flags | Every aggregate analytic completion flag remains explicitly false in PROOF_STATUS.json and the release documentation. |
| 25. Introduction | The introduction leads with the two new theorem packages and their mechanisms. The longer genealogy remains in HISTORY_AND_PIPELINE_AUDIT.md and predecessor records. |
| 26. Next boundary | The observable varying-readout case is now proved, with an orthogonal-recovery corollary. The next boundary is nonrecoverable overlapping rows or coupled coherent/support-changing directions without a common seizing map; the exact collapse example identifies an obstruction to naive parameter counting. |

## Preservation and reproducibility

The new work continues the already pushed v72 anchor; it does not fork a competing “current” revision. The partial earlier v72 transfer remains untouched as history and is not treated as a completed source. Every native v71 source path is retained unchanged in the Git ancestry, and all 460 previously active complete-edition labels must remain in the current complete proof graph. Source inventories and the actual build receipt verify these counts.

The minimal journal package has no predecessor-PDF dependency. The full research edition and exact code remain available separately. The source builder and read-only final-head verifier distinguish written proof, finite regression, artifact identity, independent priority and journal acceptance. The latter two are not certified by this release.
