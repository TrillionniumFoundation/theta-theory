# Response to v73/r47 — Revision 74

**Quantitative manuscript:** *Coupled Boundary Geometry and Reusable Measurement Descriptions*.

**Companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*.

**Controlling report:** `fa857238020a0b5f2befd936b39820a9b426390a`; **proof/pipeline audit:** `62ffc56f0911b939f3e6b79ae0a5e38563e5a988`. Both review v73. **Base:** completed v73 final head `ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f`.

We thank the referee for distinguishing correctness from significance and for identifying the appropriate next mathematical question: a geometric criterion accounting for coupled perturbations, identifiability and boundary support change. We retain the general-journal objective and the previous conclusions. The response is a new theorem chain, not a change of journal target, a numerical extrapolation or an unsupported assertion of broader applicability.

## Principal mathematical changes

The new section studies the entire unbiased binary qubit measurement ball E_x^±=(I±x·sigma)/2. Visibility |x| is no longer public. For s=min(|x|,|y|), the finite-use metric is comparable with absolute constants to min(1,sqrt(N/(1-s²+1/N))|x-y|), at every horizon and separation, including erasure and projective effects. The exact one-use distance is |x-y|.

The radial direction is treated by an exact Bernoulli-programme equality. A finite block argument supplies the support cutoff without a Gaussian or Fisher-information approximation. Crucially, a binomial monotonicity argument shows that the radial distance is bounded by the actual unequal-direction distance; triangle inequality then controls the same-radius angular distance. This prevents cancellation between radial and angular perturbations. The inherited v73 angular modulus is credited and retained, not presented as a new result.

The metric comparison yields a structural criterion on every compact k-Ahlfors-regular identifiable subset X of this ball. Its small-error covering number, even with arbitrary legal memoryless lower centres, is comparable to

    delta^(-k) integral_X [N/(1-|x|²+1/N)]^(k/2) dmu.

The criterion depends on local geometric measure and depth distribution, not a redundant parameter chart. If mu{1-|x|²<=t} has order t^alpha, the horizon factor is N^(k/2), N^(k/2)log(N+2), or N^(k-alpha), according as alpha is above, at, or below k/2. Positive mass on the projective boundary gives N^k. In particular, the jointly encoded disk has order N log(N+2)/delta² and the ball N²/delta³. The critical disk logarithm is absent from the fixed-public-visibility circle problem.

An exact rational codec realizes the disk/ball upper laws. It accepts rational Cartesian Bloch vectors with possibly irrational norm. Rational radial layers and signed-axis charts, chosen by sign-before-square comparisons, avoid irrational normalization. One index encodes both radial and angular digits. Every codeword is a legal rational centre; canonical target replay is distinct from decoder legality.

The criterion covers regular identifiable subsets of the unbiased binary qubit measurement ball. It does not purport to classify arbitrary biased POVMs, nonobservable readout or general disturbing instruments. Such an extension would require additional mathematics; it is not inferred by renaming the present interface.

## Seventeen required revisions

| Item | Response |
|---|---|
| 1. Focused quantitative article | The title, abstract and introduction centre the coupled metric and covering criterion. Both focused articles remain independently proof-complete. All prior active labels remain in their original focused graphs and in the complete edition; no mathematical section is arbitrarily deleted. Historical PDFs are absent from the minimum build dependencies. |
| 2. Sedlak–Ziman | Added to both active bibliographies, introduction, comparison and literature audit. Section VI, Example 4, equation (37), already permits different noise levels. We explicitly distinguish that single-shot state-discrimination reduction from our finite-use joint covering criterion. |
| 3. The 2018 distance paper | Added Puchala–Pawela–Krawiec–Kukulski, PRA 98 (2018), 042103, Theorem 1. Its one-shot diagonal-phase/unitary-channel optimization is distinguished from the 2021 multiple-shot projective theorem and from noisy-ball metric comparisons. |
| 4. Established mechanisms | Classical programmes, fidelity, coherent blocks, likelihood-ratio ordering, packing and rational charts are credited. The new conclusions are the joint finite-use comparison, weighted geometric criterion, contact trichotomy and charged exact joint code. |
| 5. Public visibility | The old theorem retains public visibility in its statement. The new theorem instead encodes visibility and direction jointly. No visibility or radius field is permitted as an uncharged target header in the new codec. |
| 6. Small-error cap | The metric theorem is finite-distance on the whole ball; the covering criterion is explicitly for delta<=delta_X, uniformly in N. We do not infer a full submaximal-error cover from pairwise tests. |
| 7. Ordered outcomes | Outcomes remain ordered. x and -x are different except at zero; no outcome-permutation quotient is taken. The exact one-use equality checks this convention. |
| 8. Programmes versus seizing | The v73 pair programme remains pair dependent. The radial equality has its own fixed-direction programme. Neither is described as a global ball seizer. The v72 ambient-domain seizing theorem remains separate. |
| 9. Pair tests versus estimators | Lower witnesses may depend on the known pair. Packing uses pair separation and triangle inequality only. No one common estimator or large-error multiplicity theorem is claimed for the ball. |
| 10. Centre classes | The lower criterion allows arbitrary legal memoryless centres of the same binary qubit interface; the upper centres lie in X. The rational disk/ball construction supplies legal rational family centres. No retraction is assumed. |
| 11. Rationality | The new geometric result is real-valued. Its algorithm takes rational Cartesian x and returns fully rational effects even when |x| is irrational; visibility is approximated and encoded rather than retained as an irrational public coefficient. The older rational-circle qualification for irrational public visibility remains unchanged. |
| 12. Payload and resources | The full layer-and-chart union has one integer payload. Codebook size, public parameters, JSON, input precision, radial table, workspace, expanded Choi matrices and proof programmes are distinguished in the new schema/resource ledger. |
| 13. Learning and physical simulation | The target is supplied. Encoding is neither unknown-measurement estimation nor a finite-classical-resource implementation acting on unknown quantum inputs. |
| 14. Imported v72 theorem | Its projective, ordered-outcome and multiple-shot hypotheses are retained. It is not used as an exact noisy-ball formula. The new proof instead uses the separately proved v73 noisy angular theorem. |
| 15. Independent priority | Direct missing antecedents are corrected and a theorem-specific independent review brief is supplied. No independent human opinion has been obtained or fabricated. This remains an external review request, not something source CI can certify. |
| 16. Signed release/tag | No human author signing credential has been used. Source hashes and exact-head reconstruction establish byte identity, not authorship. We therefore leave author signing explicitly unfulfilled rather than generate a misleading signature. |
| 17. A/B/C/D separation | All analytic aggregate flags remain false. The new finite-dimensional metric/covering theorem neither depends on nor closes the independent local-limit, LDP, kernel, filtering or response gates. |

## Thirty detailed comments

| Comment | Treatment |
|---|---|
| 1. K definition/endpoints | The retained v73 theorem keeps its exact K definition and endpoint conventions. The new abstract uses one smooth finite-use cutoff and does not duplicate the old K expression. |
| 2. Meaning of noise uniformity | The new result is uniform over two independently supplied vectors, not robustness to unmodelled noise. It charges target visibility explicitly. The old convention remains public visibility. |
| 3. One-use normalization | The new metric theorem states d_1=|x-y|, reducing to 2lambda sin(h/2) at equal visibility. |
| 4. Pair-dependent endpoints | Their role stays a two-point bound, not a global programme alphabet. The actual codebook is the explicitly counted rational family-centre union. |
| 5. Finite fidelity expression | The original v73 fidelity expression is retained. The new radial proof also uses its exact product-programme fidelity before deriving the scale estimate. |
| 6. Nonadaptive lower design | Stated explicitly. Adaptive freedom is needed for the upper quantifier, not the construction of the lower witness. |
| 7. Common GHZ phase | The inherited proof retains a phase common to the two hypotheses, depending only on the known pair. |
| 8. Block-visibility range | The original correlation-scale restriction is unchanged. The new radial block size has its own support-cutoff restriction and explicit floor estimates. |
| 9. Nonzero large-angle block | The retained max{1,floor(1/h)} is unchanged. No new zero-length block is introduced. |
| 10. Erasure | x=0 is a unique identifiable instrument. The new union code has one erased word; the encoder does not retain a meaningless direction. Its fixed-length capacity still reflects the whole joint family. |
| 11. Off-family centres | The new converse uses a separated packing and triangle inequality. No centre retraction is asserted. |
| 12. Chart overlap | Signed-axis chart overlap is included in capacity as a bounded redundancy. Every overlap word remains legal. |
| 13. Rational-circle notation | The new code is rational in all coordinates. The prior rational-circle wording is clarified below without falsely promising rational matrices for irrational public visibility. |
| 14. Index versus string | The schema defines ceil(log2 L) index capacity. Hexadecimal omits padding; JSON size is separate. |
| 15. Conditional trace constraints | The v73 state dimension with one trace constraint per state is retained unchanged. No conditional-state dimension is added to the new ball theorem. |
| 16. Maximally mixed witness | The original proof explicitly uses trace-one binary effects. It is not promoted to an arbitrary noisy-POVM fact. |
| 17. Two row programmes | Their proof-only role remains. They are not payload or physical hardware resources. |
| 18. Rank nonincrease | The earlier state encoder's rank guarantee is retained. New arbitrary-centre covers claim no rank-preserving retraction. |
| 19. Flag dimension | The retained ordered flag dimension remains d²-d, distinct from projective-unitary dimension d²-1. |
| 20. Imported multiple-use formula | Remains visibly external and separate from the new finite comparison. |
| 21. Rational LU atlas | Its nested-subspace proof is preserved in the active source. No normalized irrational basis is introduced in either codec. |
| 22. Ambient seizer domain | The inherited left-inverse condition is retained on the full ambient programme space. The new covering proof requires no seizer. |
| 23. Pauli/Bell mechanism | Credited as a standard application, not added to v74 novelty. |
| 24. Source transfer | Packaging and Git genealogy are provenance only. No theorem premise is justified by a workflow step. |
| 25. Scope of assertions | New and inherited assertion counts are described as exact finite regression, never verification of the adaptive supremum or a continuum theorem. |
| 26. Exact reviewed SHA | A separate contents-read-only workflow reconstructs the final request head. Its external artifact is separate from the builder's in-tree receipt. |
| 27. Authorship | Unsigned provenance is not described as cryptographic author attestation. Item 16 remains explicit. |
| 28. Repeatable observations | The structural companion remains about fresh nondisturbing classical probes, not repeated measurement of one quantum system. |
| 29. Complete edition | Kept as archival mathematics. The journal-facing quantitative and structural packages each build without historical PDFs. |
| 30. Structural next problem | Addressed by the weighted-covering criterion on arbitrary regular identifiable subfamilies of the unbiased binary qubit ball. Coupled radial/angular changes, support cutoff, contact order and arbitrary lower centres are accounted for. General biased/disturbing instruments are not claimed to follow automatically. |

## What is inherited and what is new

The v73 circle theorem, v72 observable flag/seizing results, earlier rank preparation and intrinsic coding, and original finite-label/streaming theories remain with complete proofs. The structural article is inherited and is not counted as a new v74 contribution. The two missing direct citations are now in both active bibliographies.

All 222 predecessor native files remain unchanged at their repository paths. All 502 predecessor complete-edition labels remain in the new combined edition, and each focused graph retains its prior labels. Finite code tests, universal written proof, source reconstruction, independent priority and author signature are distinct assertions. The manuscript supplies the first three in their respective forms; it does not manufacture the latter two or editorial acceptance.
