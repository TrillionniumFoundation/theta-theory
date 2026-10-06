# Response to v74/r48 — Revision 75

**Paper:** General Theta Foundations I, quantitative manuscript on the finite-use geometry of ordered binary qubit measurements.

**Controlling external report:** `GENERAL_THETA_FOUNDATIONS_I_V74_REFEREE_REPORT_R48.md`, commit `0fd7db3c634b85ad93a4d205b95bf04b6cb7e476`.

**Controlling proof/pipeline audit:** `GENERAL_THETA_FOUNDATIONS_I_V74_PROOF_PIPELINE_AUDIT_R48.md`, commit `53371065e8684e33bd3f04748dbea652011c5a7e`.

**Completed predecessor:** Revision 74, exact head `8477a4c44cbed327068ab895c244f2ddfa86e27a`. The v75 work anchor `d9ed8e4422fccd7e849ba5e72dc0df447b9d2470` records the intended extension and is not treated as a completed proof or build.

We thank the referee for the detailed assessment of the finite-use comparison, its geometric consequences, and the exact construction. The report distinguishes the correctness of the v74 theorem chain from the question of mathematical breadth. Revision 75 addresses that question by treating the full body of ordered binary qubit measurements, including bias and both spectral boundary faces. The general-journal objective is retained. The new conclusions are stated and proved for their precise interface, and all inherited mathematics is preserved.

## Principal mathematical changes

Write a positive-outcome effect as

\[
 E=qI+(p-q)P_u=\tfrac12(aI+x\cdot\sigma),\qquad
 0\le q\le p\le1,\quad a=p+q,\quad x=(p-q)u.
\]

The other effect is `I-E`. The outcomes are ordered and there is no residual quantum output. The parameter is the effect itself: at `p=q`, every direction gives the same scalar effect. Bias `a-1`, the spectral gap, and the direction are all target data. They are charged in the new code.

Theorem `thm:biasedangular75` proves a finite-distance angular comparison uniform in both eigenvalues and in the horizon. Its scale is

\[
 K_N(p,q)=(p-q)\sqrt{\frac{N}{p(1-p)+q(1-q)+N^{-1}}}.
\]

The upper proof constructs a common Stinespring gauge with scalar overlap. If `h` is the angle, put

\[
 A=\sqrt{p(1-p)}+\sqrt{q(1-q)},\qquad r=p-q.
\]

For `A>0`, the chosen dilations have squared overlap

\[
 c^2=\frac{A^2}{A^2+r^2\sin^2(h/2)}.
\]

Because the overlap is a scalar multiple of the input identity, it multiplies under arbitrary common adaptive use. Together with the hybrid estimate, this gives the finite upper bound in `eq:biasedfiniteupper75`. Publicly stopped testers are padded by ignored dummy calls. The lower proof combines an ordinary rare-Bernoulli witness with a common preprocessing that removes bias and reduces the pair to the inherited unbiased angular theorem. In particular, a one-sided singular face `q=0, p<1` has a square-root horizon scale at fixed `p`; it is not assigned the projective scale merely because one effect has rank one.

Theorem `thm:biasedmetric75` couples spectral and angular changes. Each difference of maximal eigenvalues, and each difference of minimal eigenvalues, is bounded below by an eigenstate test of the actual pair. Binomial stochastic ordering prevents cancellation. An aligned spectral comparison then uses the two classical row programmes, and triangle inequality controls a fixed-spectrum angular comparison. The resulting all-pair metric is equivalent to the sum of the two finite-use Bernoulli spectral scales and the angular scale at the less distinguishable endpoint, truncated at a constant. It includes scalar effects, deterministic outcomes, one-sided singular effects, and projective measurements. Equation `eq:biasedoneuse75` gives the exact normalization

\[
 d_1(E,F)=2\lVert E-F\rVert_{\mathrm{op}}
         =|a-a'|+|x-x'|.
\]

Theorem `thm:biasedcover75` determines the covering number of this entire four-dimensional effect body. Uniformly for `N>=1` and an absolute sufficiently small positive error,

\[
 \mathcal C_N(\delta)\asymp
 N^2\log(N+2)\,\delta^{-4}.
\]

The lower proof uses separated spectral boxes at dyadic distances from the projective corner. Each scale contributes order `N^2 delta^-4`, and order `log(N+2)` scales contribute. Any legal memoryless centre of the same interface is allowed; the centre need not lie in a chosen box or fixed-spectrum slice. The upper proof counts one exact rational code for the full body. It does not assume Ahlfors regularity of a redundant spectral parameter space at scalar effects.

Theorem `thm:biasedcodec75` constructs rational spectral levels and rational sphere charts. A single union index includes the two spectral indices and all direction data. When the two spectral levels coincide, the code has one scalar word and assigns no direction. Every in-range word decodes to a legal ordered measurement, and the encoder accepts rational Cartesian effect data even when its eigenvalues are irrational. The optimal reusable payload is therefore

\[
 2\log_2N+\log_2\log(N+2)+4\log_2(1/\delta)+O(1)
\]

on the same small-error range. The new logarithm is associated with simultaneous approach of the two eigenvalues to the projective corner. The inherited unbiased disk logarithm and unbiased ball law remain with their original statements and proofs.

## Twenty required revisions

The identifiers below reproduce the order of section 7 of the controlling report. The complete-edition theorem labels are stable audit anchors; `evidence/THEOREM_LOCATIONS.json` records their compiled locations when the native build is performed.

| Item | Response and location |
|---|---|
| R01. Fiurášek–Mičuda (2009) | The focused bibliography and comparison include *Optimal two-copy discrimination of quantum measurements*, Physical Review A 80 (2009), 042312, arXiv:0909.2940. The comparison distinguishes its projective two-use adaptive, entangled and feed-forward strategies from the uniform finite-use metric, full biased-body cover, and supplied-description code proved here. See `LITERATURE_AUDIT.md` and `editions/coding-comparison.tex`. |
| R02. Independent priority review | The theorem-specific `INDEPENDENT_REVIEW_BRIEF.md` and literature audit identify the exact assertions requiring specialist comparison. No independent human priority opinion has been obtained or represented as obtained. This external review remains distinct from the author-side mathematical and source audits. |
| R03. Independent focused article | The quantitative article and its source package have their own active inputs and bibliography. The complete research edition retains the full historical theorem graph. Predecessor manuscripts and native files remain available at their original paths; selecting a focused article does not delete inherited mathematics. |
| R04. Target class in headlines | The new target is explicitly the full body of ordered binary qubit measurements, including bias. The inherited section 50 continues to name the unbiased binary qubit measurement ball. The word “full” refers to this precise binary-qubit interface. |
| R05. Small-error cap | The abstract, introduction, `thm:biasedcover75`, and payload consequence state the sufficiently small-error range. The inherited family-dependent cap in `thm:weightedcover74` retains its dependence on regularity data. |
| R06. Metric versus cover | `thm:biasedmetric75` is an all-pair, all-horizon comparison; `thm:biasedcover75` is a small-error covering theorem with its own proof. Neither conclusion is substituted for the other. |
| R07. Identifiable image | The model is defined by the effect matrix before dimensions are counted. At equal eigenvalues the direction is absent. Section 52 counts scalar words once; the inherited Ahlfors theorem remains a theorem on the identifiable Bloch image. |
| R08. Operational proof before geometric interpretation | Section 51 proves finite-distance upper and lower bounds, including the exact dilation overlap and support cutoffs. Section 52 derives the cover directly. No general Fisher-volume principle is assumed. |
| R09. Arbitrary legal centres | The lower proof uses strictly separated target packings. It permits every legal memoryless centre of the same binary interface, without restricting centres to the spectral boxes or slices used to construct the packing. The inherited arbitrary-centre theorem is retained. |
| R10. Pair-dependent witnesses | The witness quantifier is explicit. The known pair may determine the input eigenvector, rotation, phase or block size, while the test is common to the two hypotheses. Packing requires this pairwise separation; a common family estimator is a separate question. |
| R11. Visibility charged | The new union index charges both eigenvalues and the direction, hence bias and visibility. The old v73 circle keeps its separate public-visibility convention. Neither target eigenvalue is an uncharged header in the new interface. |
| R12. Exact algorithm complexity | The reference code is finite and exact and may enumerate a spectral-level table. The implementation and resource ledger make no polynomial-time assertion in the binary lengths of all numerical parameters. |
| R13. Resource accounting | Reusable payload means index capacity. Input bit length, public dimension/horizon/error, syntax, grid tables, encoder workspace, expanded Choi matrices, and physical hardware are separately accounted for in `RESOURCE_LEDGER.md` and the codec schema. |
| R14. Ordered outcomes | The positive and negative labels remain fixed. Swapping outcomes changes the target unless the effects themselves coincide. The common outcome swap in the bias-removing lower witness is an explicitly described operation of a tester, not a quotient of the target space. |
| R15. Disk logarithm | Section 50 retains the self-contained calculation: the disk has `k=2`, depth exponent `alpha=1`, and weighted volume of order `N integral_0^1 (t+N^-1)^-1 dt`, comparable to `N log(N+2)`. Chart overlap only changes constants. The new four-dimensional logarithm is proved independently by the dyadic spectral boxes and matching lattice sum. |
| R16. Inherited structural contribution | The structural companion remains inherited in v75. Its finite-action and fresh nondisturbing classical-probe results are retained and are not counted as a new contribution of the biased-measurement theorem. |
| R17. Final-source reproducibility | The build records source hashes, theorem locations, exact finite regression results and page checks. Final-head reconstruction must verify the actual published object; source-parent evidence is not treated as evidence for an unchecked successor. The recorded receipt and external reconstruction evidence specify what was actually rebuilt. These are reproducibility checks, not proof certification. |
| R18. Human authorship signature | No human author signing credential has been used, and no human signature or signed release is asserted. Native source hashes and a reconstruction artifact establish byte identity, not human authorship. |
| R19. Analytic pipeline separation | `HISTORY_AND_PIPELINE_AUDIT.md` retains the independent A/B/C/D obligations and false aggregate completion flags. The present finite-use metric and code do not by themselves close a raw local limit, stopped-path LDP, past kernel, shell conditioning, Mosco/Nisio, filtering/LAN, changing-filtration response or posterior-contraction gate. |
| R20. Significance of the proved extension | The principal new conclusions are a scalar-overlap adaptive upper mechanism, cancellation-free full spectral/angular comparison, the full ordered binary qubit body law `N^2 log(N+2) delta^-4`, and an exact rational code charging every target coordinate. This is a new theorem chain extending the v74 object; the general-journal objective is unchanged. |

## Thirty-six detailed comments

These identifiers follow section 8 of r48, independently of the twenty required revisions above.

| Comment | Treatment |
|---|---|
| D01. Unhalved distance | The operational definitions and exact one-use formulas keep the unhalved trace norm. Classical transcript total variation is half this norm. |
| D02. Programme bits after stopping | The radial proof supplies `N` independent bits and discards the unused suffix. The biased spectral programme likewise discards unqueried row bits; the dilation proof pads stopped testers by ignored dummy calls. |
| D03. Radial zero-probability endpoint | In the ordered v74 radial variables, `q=(1-s)/2=0` forces `s=r=1`, so the pair is identical. The singular endpoint is separated before any division by a variance. |
| D04. No-success event | It is identified as the finite support-cutoff proof device. Exact radial distance is the product-Bernoulli distance; the block statistic is not claimed optimal. |
| D05. Binomial monotonicity | The self-contained monotone-likelihood-ratio event argument is retained. In v75 it is applied separately to maximal and minimal eigenvalues in `lem:spectralprojection75`. |
| D06. Chord and angle | The inherited chord identity and the explicit factor `pi/2` remain in the proof of `thm:ballmetric74`. The new angular proof likewise keeps `sin(h/2)` before converting to an angle comparison. |
| D07. Nonoptimal constants | The comparison constants, including the inherited `1/256`, are explicitly not optimized. Theorems state uniform comparison, not sharp constants. |
| D08. Reference-assisted one-use equality | The short operator-norm duality proof is retained. Equation `eq:biasedoneuse75` extends the normalization to arbitrary bias: `d_1=2||E-F||op=|a-a'|+|x-x'|`. |
| D09. Ahlfors after identification | The inherited regularity assumption applies to the image in the Bloch ball. The new full-body proof handles scalar spectral collisions directly rather than assigning them a direction. |
| D10. Family-dependent cap | `delta_X` retains its dependence on the fixed regularity data, including the local scale and measure constants. It is not described as a universal cap for all Ahlfors sets. |
| D11. Auxiliary measure | The weighted measure in section 50 is a geometric device. It is not a prior, a distribution of unknown targets, or hidden-register entropy. |
| D12. Strict packing separation | Target packings are separated strictly more than `2delta`; the inherited proof uses `3delta`. Triangle inequality then excludes two packed targets from any radius-`delta` ball. |
| D13. Boundary mass | `F(0)` refers to boundary mass under the specified target measure. It is not identified with the ambient surface measure of the projective sphere. |
| D14. Two-sided contact hypotheses | The transverse-volume and support-deficit comparisons remain two-sided. No general regularity assertion for every singular or semialgebraic set is added. |
| D15. Disk and ball exponents | The inherited disk is explicitly `(k,alpha)=(2,1)`, and the unbiased ball `(3,1)`. Their horizon factors remain `N log(N+2)` and `N^2`, respectively. |
| D16. Coordinate line | Its analytic law follows from the same weighted criterion. The inherited implemented Cartesian codec keeps its declared dimensions two and three. The new biased-body schema states its own supported input interface. |
| D17. Erased radial layer | The v74 radial grid retains both endpoints and one erased word at layer zero. The v75 spectral code has one word for each scalar spectral level; no direction is charged when the spectral gap is zero. |
| D18. Chart overlap | Signed-axis overlap and endpoint redundancy are included in exact capacity. They affect comparison constants and do not create the logarithmic factors. |
| D19. Canonical chart ties | The maximal-coordinate chart uses a deterministic axis and sign rule, retained in canonical replay. A tie is not resolved by floating-point perturbation. |
| D20. Sign before squaring | The schema and proof keep the sign test before squaring an algebraic comparison. This remains necessary for both irrational target normalization and spectral comparisons. |
| D21. Error certificate meaning | A stored adaptive-error upper value is a construction budget derived from separate approximation steps. It is not a numerical evaluation of the exact adaptive distance. The inherited `delta/4` certificate retains that meaning. |
| D22. Legality and replay | Every syntactically valid in-range word decodes legally. Target-bound canonical replay is a stricter check and is kept separate. |
| D23. Boolean cache keys | Validation precedes any cached grid lookup; Boolean values are rejected as integer horizons, including after a colliding integer key has been populated. The inherited negative control is retained. |
| D24. Scope of finite tests | Exact finite tests cover algebra, selected inequalities, legal decoding, indexing and defensive parsing. They do not quantify over all continuum targets or all adaptive testers, and are not substitutes for the written proofs. |
| D25. Actual reviewed SHA | The final reconstruction must use the submitted final head. The publication protocol and evidence distinguish a qualified native source, a publication object, and an exact-head read-only rebuild. |
| D26. Unsigned provenance | A workflow artifact is described as a reconstruction record. It is not called a human signed attestation. |
| D27. Structural probe interface | Fresh, classical, nondisturbing probes remain the hypothesis of the inherited structural companion. This is not reinterpreted as repeated quantum measurement of one system. |
| D28. Earlier width gap | The v63 exponential-width multiplicative gap remains separately recorded in the history audit. It is not removed by the new description-covering theorem. |
| D29. Mutable workspace | The payload law does not assert an optimal mutable-workspace lower bound for its encoder or a streaming implementation. The resource ledger preserves this distinction. |
| D30. Boundary terminology | Every full-body statement names the ordered binary qubit effect body. The inherited entire-ball wording remains qualified as unbiased. |
| D31. No retraction | The covering converse uses only target separation and triangle inequality. It does not produce a nearest-point retraction or convex projection. |
| D32. Equivalent regular measures | The inherited disk order is unchanged under equivalent Ahlfors measures; the comparison constants depend on the regularity data. |
| D33. Unbiased-ball boundary enhancement | The inherited `N^2 delta^-3` law is explicitly boundary dominated, rather than the interior `N^(3/2)` volume scale. Its contact calculation remains in section 50. |
| D34. Interior/projective crossover | The inherited cutoff `1/N` links square-root interior resolution to coherent projective resolution. The new angular theorem also resolves the one-sided singular face and scalar collapse, which require separate spectral information. |
| D35. Four direct antecedents | The focused comparison distinguishes Fiurášek–Mičuda 2009, Sedlák–Ziman 2014, the 2018 single-shot projective-distance paper, and the 2021 multiple-shot projective theorem. Their respective interfaces and roles are not conflated. |
| D36. Mechanisms and new conclusions | The comparison and independent review brief credit dilation/programme contraction, classical product testing, entangled probes, separated nets, summation and rational charts. Novelty is attached to the proved finite-use full-body comparison, its joint counting law and its exact charged construction, subject to independent priority review. |

## Preservation, evidence, and further review

The predecessor source remains unchanged at its original paths. The new complete edition retains the historical structural, spectral, positive-realization, streaming, instrument-description, preparation, coherent-readout, seizing, noisy-circle and unbiased-ball results, with their original hypotheses. The prior v74 author response and proof audit are copied to `predecessor-v74-audit/`. `PRESERVATION_MANIFEST.json` and the build's label comparison provide the file and theorem-graph accounting; numerical counts are taken from those generated records rather than guessed in this response.

`PROOF_AUDIT.md` separates the arguments for the biased metric, dyadic lower cover, exact rational upper cover and inherited results. Reproducibility evidence belongs to the emitted files under `evidence/`, including `SOURCE_HASHES.json`, `REGRESSION_RESULTS.json`, `PAGE_CHECKS.json`, `THEOREM_LOCATIONS.json` and `BUILD_RECEIPT.json`. A receipt supports only the source and checks it actually records. An external exact-head reconstruction supports only its recorded commit. Neither is an independent mathematical referee opinion or an authorship signature.

The submission therefore supplies concrete new mathematics and a complete itemized response for further referee assessment. Independent specialist priority clearance and human authorship signing are not supplied by this author-side revision. The journal's significance assessment remains the referee's and editor's judgment.
