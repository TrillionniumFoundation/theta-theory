# Referee report — A1, English revision 13

**Manuscript:** *Sparse observation algebras and certified memory across exponent collisions*  
**Author named in the manuscript:** Qian Qi  
**Review date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation: REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted independent referee-style assessment. It was not commissioned by any of the four named journals. The recommendation below is an editorial assessment of this submission, not a claim that its principal theorem is false or that the research program cannot succeed.

## 1. Submission, evidence, and scope

```text
repository:          TrillionniumFoundation/theta-theory
revision branch:     revision/a1-english-v13-referee-response-2026-09-06
submission commit:   fc6465b86fbc7ee6a4e8f3ccfb54ea32a64dc8b6
submission tree:     4577957f28244cae85e5e2c09e1157a39d1b8140
submission time:     2026-09-06T12:12:55Z
principal directory: papers/A1-english-v13/
controlling review:  f2638b4910ee6245e9df4f641a2ed861bc4960b7
new review branch:   review/a1-english-v13-harsh-referee-2026-09-06
```

The report concerns this immutable submission, not subsequent changes to its branch. I examined the new common-moment theorem and its proofs, the request-conformance proposition and implementation, the prior-envelope and numerical-stability arguments, and the principal inherited collision-geometry dependencies. In particular, I reconstructed the normalized transversality argument, the distinction between local attainment and global covering, the causal recurrence, and the new overlapping-history two-point lower bound. `SOURCE_INDEX.md` records the sources and limits; `MATHEMATICAL_AUDIT.md` records the substantive calculations. [S0–S9]

The complete v13 workflow artifact was downloaded through the repository connection. Its archive hash, the Git blob of its source manifest, and all 62 manifest-listed source hashes were checked. I reran the four author suites: 7,904, 8,207, 26,158, and 12,944 assertions respectively, totaling 55,213. These are independent executions of author-written tests, not 55,213 independently designed checks. A separately written probe, importing no author test helper, executed another 4,909 assertions, rejected ten precision/horizon fault injections, and exercised a physical common-name program stopping on its advice floor. [X]

A separate three-pass LaTeX rebuild produced 68 pages, with no undefined-reference or overfull warnings reported by the build checker. Its extracted text agrees page by page with the submitted PDF. I visually inspected manuscript pages 38 and 42, not every page. The preservation checker confirms 68 retained v12 proof blocks and 71 retained named results against its supplied manifests; the present expanded manuscript has 74 proof blocks and 77 named results. These are source-structure observations, not mathematical certificates. [X]

I did not execute the whole `validate.py` pipeline, since the downloaded artifact omits the adjacent historical directories and the original prior-referee script required by its historical reproductions. The present review does not pretend to have rerun those historical scripts, checked every retained appendix independently, or exhaustively cleared the literature for priority. The new fault probes and all four present author suites were actually executed.

## 2. Overall judgment

Revision 13 makes a real advance over revision 12. The precision and horizon faults are repaired at the correct architectural boundary: the construction is checked against a request fixed before synthesis, rather than against metadata chosen by the returned program. The common-input physical diagnostic is now present. More importantly, the manuscript no longer offers only a rank-two example for its uncertainty lower term. It proves a lower bound uniformly at every calibration in the compact chamber, including additive collisions and their intersections, under explicit interior-prior and numerical-name slack assumptions. These are substantive responses and must receive credit. [S1, S4–S8]

**I found no blocking counterexample or essential unfilled step in the principal mathematical chain examined under its printed hypotheses. I also found no new blocking implementation defect in the tested request-conformance layer.** This statement is deliberately narrower than a certification of every assertion in the manuscript. It is nevertheless incompatible with recycling the v12 defects as reasons to reject v13.

My recommendation remains negative at the requested journal level for a different reason: the manuscript has not established a sufficiently compelling case for the exceptional mathematical significance of the complete contribution. Its central achievement is the collision-uniform attainable exterior-volume profile. The new uncertainty theorem is a correct and useful consequence, but the proof shows a largely separable combination of that inherited geometry, finite-dimensional stability, and a uniformly visible prior-tilt direction. The additional saturation formulas invert the existing profile. The implementation repairs make the constructive claim credible; they do not, by themselves, increase the mathematical depth of the classification.

This is not a disguised false-theorem objection. Nor is it a finding that an identical theorem exists elsewhere. It is a judgment about the strength, reach, and presentation of the demonstrated contribution. The remainder of the report explains that judgment and identifies exactly which previous objections are closed.

## 3. Disposition of the controlling v12 report

| V12 item | What v13 supplies and what was checked | Disposition |
|---|---|---|
| P12.1: wrong precision can produce an accepted false bracket | `ConstructionRequest` fixes the precision and error budget before compilation. Both adaptive routines use it; the checker compares metadata and reconstructs numerical entries. Independently injected coarse precision and misleading precision metadata are rejected in both routines for M=1 and M=2. | **Closed for the identified fault class.** |
| P12.2: a two-stage request can return an accepted one-stage program | The requested horizon and complete stage/query schema are bound independently of returned table lengths. Two independently injected shortened-horizon cases are rejected. | **Closed.** |
| P12.3: no one-name physical end-to-end diagnostic | The rerun v13 suite constructs one program per budget from one fixed moment table and tests four compatible models, including an exact additive collision and both sides of it. The independent probe additionally exercises the floor-only stopping regime with M=64. | **Closed at the explicitly finite-domain evidence level requested.** |
| E12.2: the lower witness is only rank two and does not give a uniform noisy-collision law | Theorem `thm:sharp-common-moments`, Lemma `lem:uniform-collision-ambiguity`, and the intersecting-strata corollary supply the missing uniform statement, with interior and slack hypotheses stated openly. | **Mathematical limitation addressed.** It must not be restated as an unresolved absence of a collision-stratum lower bound. |
| E12.1/E12.3: significance of the whole submission | A stronger consequence, repaired construction boundary, and integrated evidence have been added. | **Substantive response, but not sufficient for a positive four-journal recommendation.** See Section 6. |

Earlier issues about unjustified oracle access, omitted history probability, ambient rather than attainable dimension, exact-zero pivots, or the corrected discounted-control citation are not reopened without new evidence. The selected checks did not supply such evidence. [R, S2–S8, L1–L4]

## 4. Mathematical assessment of the new theorem

### 4.1 The hypotheses do meaningful work

Theorem `thm:sharp-common-moments` fixes a full-support reference probability, a dominated prior envelope, an interior measure margin, and a compact strictly ordered one-step exponent chamber. A rational moment name is required to lie within half the prescribed error tolerance of an interior center. The consistency class uses the full tolerance and includes all compatible calibrations and priors in the envelope. The common program receives the numerical name and fixed task data, not that center. [S5]

These distinctions prevent three possible but invalid objections. Uniformity over this dominated envelope is not uniformity over all full-support priors. A boundary name need not admit the two alternatives used in the converse. And a lower bound arising from uncertainty in the prior is not a calibration-only lower bound with an exactly known prior. The manuscript states these limitations; they are not concealed assumptions discovered by this review.

### 4.2 The uniform lower bound is valid in the examined argument

Write z(t)=t^{a_1}, f=z−μ(z), and ε=δ/2. The perturbed priors are

\[
 d\mu_\pm=(1\pm\varepsilon f)\,d\mu.
\]

Their total mass is one and their density factors remain positive. The interior measure margin keeps them in the declared envelope for sufficiently small δ. Every formal monomial is bounded by one, so each supplied moment changes by at most ε. The unused half of the name's error budget makes both perturbed models compatible with the same name. No exponent equality is decided. [S5; A2]

For any history with likelihood L and posterior ν under the center, direct subtraction gives

\[
 \nu_+(q)-\nu_-(q)
 =\frac{2\varepsilon\operatorname{Cov}_\nu(q,f)}
        {1-\varepsilon^2(\nu f)^2}.
\]

The relevant fixed physical query is an affine multiple of z, obtained by multiplying one nonconstant failure probe by constant failure probes. Positivity of every report likelihood and the lower prior envelope give a uniform positive lower bound on its posterior variance at every fixed-horizon history. Compactness inside the strictly ordered chamber prevents the first positive exponent from disappearing. Thus the query separation is of order δ, uniformly in the additive collision pattern.

Crucially, the proof does not say that the two history distributions are equal. It uses the common domination P±≥(1−ε)P0. The same prediction kernel conditional on the observed history, together with the elementary two-point squared-loss identity, then gives an unconditional lower bound of order δ². The argument applies even to a rule retaining the entire history. The audit gives the constants and quantifiers. I found no gap at this step. [A2]

### 4.3 The joint law follows without selecting the unknown center

The inherited intrinsic lower theorem applies to the center, which belongs to the consistency class. It gives the independent Ξ lower bound even when the encoder is allowed more model knowledge than the common program. Combining the two lower bounds gives a constant multiple of Ξ+δ². For the upper bound, paired-history stability and the prior-envelope version of the covering theorem compare all models compatible with the same name; the robust compiler itself does not inspect the center. This is not circular use of a desired profile to certify the program. [S4–S6; A3]

The exact profile threshold is also correct:

\[
 \Xi_N(M,a)\le\delta^2
 \quad\Longleftrightarrow\quad
 M\ge\max_{n,\ell}\mathcal V_{N-n,\ell}(a)\delta^{-\ell}.
\]

The corresponding statement about minimax risk is a comparison-order saturation statement, not an exact risk constant. The manuscript maintains that distinction. Its noisy five-trial example retains the three previously established geometric terms and appends the uncertainty floor. [S5; A4]

## 5. Construction and reproducibility

### 5.1 The new boundary addresses the actual fault

The bound request fixes horizon, ordered alphabets, state and query dimensions, label budget, output precision, raw numerical error allowance, and total error allowance. The numerical name is frozen before the compiler is called. The checker subsequently compares the returned object with that specification and independently reconstructs the required farthest-first choices, transitions, and clipped rounded outputs. It no longer lets a returned program choose which precision or how many stages are to be certified. [S7]

The contract remains conditional on the supplied raw numerical accuracy and command-net hypotheses. Its digest proves identity of a supplied finite name, not truth of an arbitrary moment oracle. That is the correct boundary. A demand that this finite checker establish the accuracy of an unconstrained external oracle would be a different problem, not a repair to P12.1.

The independent probe uses the scalar system U=[1/4,3/4], s0=1/2, T(s,u)=(s+u)/2, Q(s)=s. Its one-step exact M-center radius is 1/(8M). Four unmodified controls satisfy the returned brackets. Eight wrong/misleading-precision mutations and two shortened-horizon mutations are rejected with `ContractError`. These are fault-injection checks of what the acceptance layer excludes, not allegations that the unmodified compiler naturally produces those faults. [X]

### 5.2 The common physical test is now integrated

The author's physical experiment has N=3, two acquisition commands, four reports, and exponents (0,1,2+gap). A single rational moment table is used against four compatible models: two opposite prior tilts at exact collision, and two uniform-prior calibrations on opposite sides of that collision. I reran that diagnostic rather than relying on its committed success receipt. It supports the claimed finite-domain integration. It does not purport to enumerate the continuum command cube. [S8, X]

My additional probe changes the budget to M=64 while retaining a fixed finite physical experiment and a common moment name. All candidate histories can then be represented, so the exact finite-domain covering radius is zero. The robust routine stops on its advice floor, not its positive-radius condition. The returned stage counts are (1,8,64), the selected b is 11, output precision is 13, and the mesh is 1/2048. One unchanged program is evaluated against all four compatible models. All prefix state recurrences and all requested query errors satisfy the checked bounds; the largest observed query discrepancy is about 6.046×10⁻⁵. Exact fractions are in `INDEPENDENT_PROBES.json`. [X]

This is a useful positive control of the other stopping mechanism, not an additional condition imposed retroactively on the author. It is not a numerical verification of the five-trial phase theorem, a universal performance guarantee inferred from samples, or a measurement of the theorem's optimal constants.

## 6. Why I still do not recommend the submission at the requested level

### E13.1 — A uniform noisy law need not introduce new collision geometry

The new lower theorem genuinely holds on collision strata. However, its uncertainty direction is the first positive one-step monomial, and the two competing priors can have exactly the same calibration. The proof deliberately chooses a direction whose variance remains bounded below uniformly over the entire chamber. It does not resolve how an uncertain numerical name behaves along each vanishing exterior direction. Its δ² lower term is therefore largely independent of the difficult collision scales. This is an observation about the proof's mechanism, not a claim that the printed theorem should have a different scope.

An abstract dependency calculation makes the point precise. Once one has (i) a memory lower profile at a center, (ii) a common-name upper construction controlled by the center's covering radius plus δ, (iii) stability of that profile over the consistency class, and (iv) one uniformly visible two-point uncertainty direction, the sum law follows by taking a maximum for the lower bound and squaring a sum for the upper bound. Section A3 supplies that reduction explicitly. The special work added in v13 is checking the alternatives and uniform variance within the physical model. That work is correct, but it is a short robust-statistical addition to the geometric classification, not a second comparably substantial geometric theorem.

This assessment does **not** reopen E12.2. The requested uniform converse has been supplied. Nor does it demand a calibration-only theorem, a boundary-name theorem, or an infinite-horizon result as a hidden condition for correctness. It explains why satisfying the previous mathematical request does not automatically settle the editorial question.

### E13.2 — The main contribution must carry the submission, rather than the number of consequences

The nontrivial core is the simultaneous attainment of the collision-normalized flag by actual positive histories, with a common exploration law and a separate matching global cover. This is more than a Vandermonde determinant estimate. It deserves to be assessed as the central contribution, not dismissed as a spectral identity. [S2–S3]

At the same time, the proof uses a particularly rigid fixed-format setting: the sparse monomial algebra, binomial history factors with separated tangent exponents, complete confluent Chebyshev systems, coefficient-independent semialgebraic complexity, and a fixed finite horizon. Once the normalized flag is attained, the lower bound is a volume argument, the causal realization is a finite Lipschitz recurrence, and the numerical scale is selected by a farthest-first radius bracket. The collision-tree allocation and saturation thresholds then describe the consequences of the finite exterior profile. The audit separates these steps rather than calling the whole result routine. [A1, A3–A4]

My reservation is that the submission does not yet demonstrate why this specialized classification, with these fixed-format constants, constitutes an advance of exceptional general-mathematical importance. The examples exhibit the predicted phases within the model, but are largely evaluations or inversions of the same determinant formula. The new common-name consequence extends the useful interpretation of that formula without substantially changing the source of its mathematical force.

Fixed horizon, classical tools, or specialization alone are not disqualifying. Equally, correctness, completeness, and a larger collection of formally named consequences are not sufficient grounds for acceptance in the four named journals. The present paper has not persuaded me on the latter question. This is a judgment about this manuscript, not a purported universal rule about what those journals publish.

### E13.3 — Presentation still gives too much weight to the revision apparatus

The current manuscript is more coherent than a stack of response letters, and the historical proofs have genuinely been preserved. Nevertheless, the principal narrative gives substantial space and theorem-level visibility to finite-data interfaces, sufficient precision, residual checking, request conformance, workspace bookkeeping, and separate versions of closely related realizations. The reader must continually distinguish intrinsic classification from numerical construction and implementation acceptance. [S0, S4, S6–S7, S9]

For a further submission, I would ask for one explicit theorem hierarchy: the geometric classification; the common-name minimax consequence; and the finite implementation theorem under its numerical interface. The central proof and its conceptual obstruction should dominate the exposition. Supporting contracts and historical specializations can remain complete in appendices or retained supplements. This is an organizational request, not an instruction to delete proofs or weaken the theorem.

The author already distinguishes persistent labels, numerical advice, and read-only program length, and does not claim universal optimality of all three. That distinction should become more prominent in the theorem hierarchy. Likewise, the uniform noisy theorem should consistently be read as joint prior-and-calibration uncertainty for interior names, not as identification of calibration from moments alone. These are priorities for presentation, not new false-statement findings.

## 7. Literature and limits of the novelty assessment

I checked selected external inputs rather than treating the repository's literature log as independent verification. Zhang–Kileel's version 4, Lemma 2.18, supplies the relevant bounded-format semialgebraic regularity statement. The real entropy inequality recalled in the introduction of Comte–Halupczok supports the thin-rectangle argument; its new motivic theorem is not being substituted for a real theorem. De Boor's divided-difference account supports the confluent integral formula. Saldi–Yüksel–Linder version 3 does identify Theorem 5.2 with the discounted-cost comparison, so the earlier version/number issue remains closed. [L1–L4]

These sources support specific inputs and distinctions. None, on the material checked, supplies an identical positive-history collision law; none is cited here as a priority refutation. The targeted search is not an exhaustive novelty clearance. A negative significance recommendation must not be inflated into an unsupported assertion of nonoriginality.

## 8. Recommendation and disposition

I do not recommend acceptance, or a minor revision, at the requested four-journal level. **The basis is insufficiently demonstrated significance and an overextended hierarchy of consequences, not a remaining version of the repaired precision/horizon defects and not a discovered counterexample to the new common-moment theorem.**

There are no newly asserted blocking mathematical or implementation errors in this report. P12.1–P12.3 are closed in the stated scope, and the uniformity limitation behind E12.2 has been addressed. The outstanding editorial reservations are E13.1–E13.3. A further response should address the mathematical importance of the central classification and the organization of the complete argument, rather than merely adding assertion counts or another contract lemma. No particular unproved extension is prescribed as an acceptance checklist.

The accompanying audit, source index, execution receipt, exact probe output, and reproducible script make the scope of this judgment inspectable. The revision and all earlier material are left unchanged.
