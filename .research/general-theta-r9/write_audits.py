from pathlib import Path
p=Path('papers/General-Theta-Foundations-I-restart/r9-continuation-completion')
old=Path('papers/General-Theta-Foundations-I-restart/r8-continuation-geometry')
new={
'README.md':'''# General Theta Foundations I — restart R9

**Acquired Geometry and Causal Resource Transfer** — Qian Qi.

This is a new foundations revision responding to the R7 external report. The canonical start remains `18000b21e4bfd89180ccb069e46ac0f21621f34d`. The pre-existing unreviewed R8 source at `3c9b212f8673c95e3a28fd83811b8a4f3bacc431` is credited and preserved, not relabeled as newly discovered work.

## Manuscript and submitted supplement
`main.tex` is the complete native article. Its principal theorem is `thm:serial`: the online resource exponent is the largest acquired continuation exponent across all cuts under explicit raw-verifiable recursion, global covering and positive-mass observability certificates. Checkpoint and online excess match exactly when that largest exponent equals the terminal exponent. The finite horizon, fixed physical exploration and candidate-domain assumptions are part of the theorem.

`thm:ranknoisy` derives all-cut certificates and a rank-sensitive noisy law; `thm:singularserial` proves a singular-acquisition law with a potentially geometry-expanding terminal query. All R8 substantive sections remain active, including two-sided/conditional cuts, a sequential-chart construction, the full-rank noisy model, acquisition, Gaussian filtering, stopping and morphisms.

Supplement S is part of this same submission, not an external publication. `build.py` supplies its complete retained technical text with a cover explaining its status. No theorem is justified by an unpublished, unavailable self-citation.

## Reproduction
Run `python3 refresh_manifest.py` only while authoring. It is not a build step.
Run `python3 verify.py` and then:
```
python3 build.py --source-sha <immutable-source-commit> --expected-tree <native-source-tree> --output <outside-source-output-dir> --receipt <outside-source-receipt.json>
```
The builder never regenerates the source manifest. It runs ordinary and optimized regressions, checks active inputs, builds the native article twice in isolated copies, rebuilds the complete pinned supplement twice, and verifies unchanged source bytes. The mathematical proofs, not the test counts, establish continuum claims.

The final source, artifact and read-only verification SHAs are recorded under `evidence/` after the corresponding operations actually succeed. This document does not predeclare success or journal acceptance.
''',
'RESEARCH_CONTRACT.md':'''# Research contract — restart R9

The branch was created directly at canonical restart `18000b21e4bfd89180ccb069e46ac0f21621f34d`. R7 review `f04b0c0c967a75dfa2f09cbfb3d38e54cef639d2` is the latest referee input found. R8 research `3c9b212f8673c95e3a28fd83811b8a4f3bacc431` already contains continuation-chart and noisy-regression mathematics and is an explicitly attributed source dependency.

Do not change the General Theta topic, use old v97 numbering, overwrite a review/realization/archive ref, or count repository organization as mathematics. The new source remains in the restart family. Preserve every substantive predecessor result in active source or the supplied complete supplement and immutable sibling trees.

The new objective is a class-level necessary-and-sufficient compatibility criterion, with an actual serial construction, all-cut lower certificates, changing observable rank and singular acquisition. Its stated assumptions are not hidden conclusions. Universal width-only duality, unknown-model adaptive acquisition and a fully matched computational resource region are not claimed without proof.
''',
'PINNED_INPUTS.md':'''# Immutable inputs

| Input | Commit / object |
|---|---|
| Canonical restart | 18000b21e4bfd89180ccb069e46ac0f21621f34d |
| Latest R7 report | f04b0c0c967a75dfa2f09cbfb3d38e54cef639d2 |
| Report blob | 637f674f3e074c9f9d82f1d0e7ac61bb7aab3f5d |
| Reviewed R7 head | 627ea5c950c5030ecebf9a1dca70c2b169ad23b5 |
| Inherited, previously unreviewed R8 research | 3c9b212f8673c95e3a28fd83811b8a4f3bacc431 |
| R8 whole manuscript subtree | 057f318118224e615ea812214608eb3c79ab98ae |
| R4 preserved subtree | 39efc9cf1199031fd6cce40690c1eb617e80af4c |
| R5 preserved subtree | 44fff54beca2eca58133d67a21306822b26bc887 |
| R6 preserved subtree | e449fa84cb6a83589e8b20831230825c19c2e050 |
| R7 preserved subtree | b39a6d0b4704bba93d75176280e936cba6282dcb |
| Supplement immutable source commit | 86472b72b62184ac542e7ea82c354b2c293ef59e |
| Supplement native source tree | 0b3839c841b02a173745d6d4fb3d997712ea9fe0 |

The four canonical controls remain unchanged. The R8 technical results are inherited research, not an independent referee endorsement. Actual write, build and verification objects are recorded only after execution.
''',
'THEOREM_MAP.md':'''# Theorem dependency graph

```
prepared standard-Borel kernels + legal fixed exploration + one scored task
    -> future-test evaluation quotient (prop:quotient; full domain assumptions)
    -> full-history Bayes projection (eq:task)
        -> checkpoint q_M identity
        -> complete-prefix/suffix cut lower (lem:cut)
            -> conditional/two-sided common-channel comparison (thm:cutduality)
            -> raw density / joint regeneration certificates (lem:minorization)

raw serial task realization + global inward covers + candidate Lyapunov drift
    -> code-independent candidate moments
    -> one M-label recursion after every report
    -> accumulated task-root error upper
actual cut submeasures + observable small-ball exponent at EACH active cut
    -> matching cut lower
both branches -> thm:serial (central acquired-dimension compatibility theorem)
    -> cor:serialerrors (same-metric approximation and causal risk transfer)
    -> lem:serialcompander (changing-rank unbounded candidate domains)
    -> thm:ranknoisy (all prefix ranks and terminal scalar exponent)
    -> thm:singularserial (all singular prefix exponents and terminal expansion)
```

No realization theorem is used to prove `thm:serial`. The `eq:compandpoint` scalar construction in the independently proved chart theorem supplies the Euclidean quantizer; that chart theorem does not rely on the serial theorem. The new Gaussian proof inherits square-completion identities from `thm:noisy`, not its full-rank conclusion. All-cut lower/upper constants are reverified at reduced rank.

Parallel retained mechanisms: `thm:transfer` supplies uniform-time block control; `thm:adaptive`, `thm:joint`, `thm:digital` supply matched paid acquisition / label / calibration / attained-defect and finite-bit feasibility; `thm:brier` is ordinary filtering; bounded stopping and typed morphisms have separate hypotheses. Supplement S contains the full nonreset singular dynamics and typed transcript proofs.
''',
'PROOF_LEDGER.md':'''# Proof ledger — new central layer

| Statement | Proof mechanism | Quantifiers / scope |
|---|---|---|
| thm:serial lower | A Hilbert r-ball pulls back into a state ball of radius 2r/ell; M balls cover at most half actual mass; fixed-seed cut lemma transfers distortion | Every M; every online randomized predictor; one encoder-independent experiment; no normalized rare-event mass |
| thm:serial upper | Inward Q + candidate Lyapunov inequality gives A_t before error analysis; e_t <= L_t e_(t-1)+a_t A_t M^(-1/s_t) | Global candidate domains, every admitted report; finite T; independent reports not assumed |
| thm:serial compatibility | Choose maximum exponent for lower, sum insertion gains for upper; terminal cut supplies separate checkpoint exponent | Necessary and sufficient within this certificate class only; constants retain T and gains |
| lem:serialcompander | Inward scalar power compander, product cardinality <=M, polynomial moment envelope | Changing Euclidean dimensions, unbounded correlated reports, finite (2+zeta) moments |
| cor:serialerrors | Same recursion plus all-candidate root perturbation; bounded common-law TV | Error budgets are upper certificates, not lower-risk floors; full resource tuple multiplies |
| thm:ranknoisy | Derived A, partial column spans, rank-state recursion; compact conditional Gaussian minorization; projected Gaussian density; query-frame lower | Fixed known G,tau,sigma,a,L,lambda; noises positive; rank can change across prefix cuts; no exact prefix stored |
| thm:singularserial | Actual Cantor cylinder mass and global product covers; noisy suffix minorization; sphere frame; scalar posterior subdensity | Exact analog raw reports with finite retained labels, fixed ratios in (0,1/2); D need not be integer; terminal cut retained |

Every statement above has a full native proof. The finite suite checks algebraic witnesses and catches implementation drift; it cannot certify these continuous-parameter arguments. Correctness, originality and journal significance remain subject to external review.

## Inherited dependency ledger (not new R9 claims)
'''+(old/'PROOF_LEDGER.md').read_text(),
'ASSUMPTION_MATRIX.md':'''# Assumption matrix — central theorem and raw realizations

| Requirement | General serial certificate | Noisy rank family | Singular acquisition family |
|---|---|---|---|
| Actual preparation | Given normalized kernels, not reachable-set measure | Theta prior and all positive normal noises | Fair Cantor digits, exact coordinate-report kernel |
| Legal exploration | Fixed encoder-independent finite protocol | d scalar reports then one noisy query packet | d analog coordinate reports then one noisy query packet |
| Task realization | Borel recursion sufficient for the single conditional mean | Successive partial ranks of J^T A; posterior response after packet | Reported candidate prefix, then psi(B dot X) |
| Full predictive quotient | Separately validated if needed for all future laws | Rank task factor need NOT determine nuisance suffix law | Prefix is sufficient for remaining independent preparation and noisy suffix |
| Global cover | M-value inward weighted radius M^(-1/s_t) | Euclidean compander on every partial-rank candidate space | Full compact product cylinders, including all rounded candidates |
| Update stability | Global pair modulus and Lyapunov bound, no independence | Partial-span operators norm <=1; Gaussian report moments | Append operator norm1; V=1; bounded sigmoid derivative |
| Actual mass | Unnormalized product sublaw at every active cut | Compact prefix event, bounded projected Gaussian density | Full Cantor product law times actual positive noise-minorization mass |
| Observable lower | Co-Lipschitz future-response map in L2 of common suffix | Positive smoothed-sigmoid derivative and frame on L | Positive sigmoid derivative and sphere frame |
| Terminal geometry | Positive mass of exponent s_T | Scalar forecast density submeasure, exponent1 | Continuous query yields scalar density submeasure, exponent1 |
| Report continuity | Used separately for implementation/morphisms | Conditional normal translation bound on full actual prefix | Shared remaining coordinates and translated V density |
| Resource budget | Entire data-dependent tuple <=M at every cut | Known coefficient description, phase, scratch separately charged | Exact Borel analog model; finite precision requires new interface certificate |

No unobserved preparation variable, rereadable report tape, exact real posterior or forgotten controller state is included in the online upper for free. The lower may relax computation but not the M-valued object crossing its cut.
''',
'COUNTEREXAMPLE_LEDGER.md':'''# Counterexample ledger

1. **Dropping earlier cuts.** Positive-noise rank-r regression has terminal exponent1 but online exponent r. For r>1, scalar terminal quantization cannot describe online memory.
2. **Dropping the final cut.** Singular prefix dimension D<1 does not give M^(-2/D) online error: a continuous query creates terminal exponent1. The correct maximum is max(D,1).
3. **Using hidden ambient dimension.** The same d-dimensional noisy hidden variable with queries spanning only L of rank r<d has exponent r, not d.
4. **Calling a task factor a full predictive quotient.** Discarded directions in the noisy model may affect V's conditional law while leaving the scored response sufficient through the low-rank factor. A simulator using only that factor is not certified.
5. **Free exact whitening.** Quantizing A H only after storing every H_j violates the earlier-cut memory model. The proof uses partial-span updates and rounds at each actual report.
6. **Hypotheses only on true states.** A true-trajectory moment bound does not control representatives after repeated approximation. The global candidate Lyapunov inequality is imposed before code selection.
7. **Zero global product.** A continuously reissued W produces diagonal support; global product domination can vanish. The conditional-cut theorem uses genuine side information or a stated relaxation, not an uncharged retained register.
8. **Small-ball normalization.** Normalizing away alpha p removes a real loss factor and changes the experiment. Every q_M of a finite measure scales with its mass.
9. **Atomic terminal distribution.** A finite atomic task does not satisfy a positive power small-ball bound at every radius. Such tasks remain covered by the exact cut identity and the retained finite/progressive results, not by a falsely applied serial power-law specialization.
10. **Analog versus digit acquisition.** A single declared analog report and an entire progressive digit stream are different raw interfaces. Singular analog results do not imply a free infinite-bit progressive acquisition theorem.
11. **Stable finite horizon versus uniform time.** The serial constant contains products of L_t. Letting T grow can destroy uniformity. The separate block theorem must be invoked with its own raw hypotheses.
12. **An allowed defect is not a risk floor.** Adding TV tolerance epsilon to a model class does not force risk epsilon. The inherited early-erasure construction supplies an actually attained lower in one scored task.

The examples determine correct hypotheses; they do not replace the intended general theory with a no-go conclusion.
''',
'PIPELINE_DERIVATION.md':'''# Pipeline derivation — acquired continuation completion

1. Preserve the original A0--A5 object and G1/G3 task. Start from the canonical preparation and normalized causal kernels; define actual exploration, complete interfaces, executable future tests and one scored terminal outcome.
2. Retain the full predictive quotient theorem. When a smaller serial statistic is used, prove only its actual task sufficiency and explicitly withhold full report-law simulation unless separately established.
3. At each information cut derive the complete prefix/suffix law. Produce positive product sublaws by conditional density or joint regeneration; push their unnormalized mass through future-response functions. Conditional localization handles genuine shared interfaces.
4. Verify global candidate spaces, legal update maps and a selectable finite cover. Prove a candidate Lyapunov bound for all inputs before selecting the actual code. This extends the original T08 propagation to unbounded domains without granting a free exact state.
5. Construct the single finite-state machine. Induct on its candidate moments and on its mean-square distance from the true task state. The only retained object is a finite index after every actual report.
6. Apply the same-task cut lower at every active stage. Observable small-ball exponents produce explicit constants retaining mass. Compare the largest cut exponent with the terminal one; this proves the compatibility criterion within the declared certificate class.
7. Derive all-cut ranks from Gaussian raw likelihoods and the executable query frame. Quantize successive partial-rank coordinates, not an inaccessible exact transformed prefix. Verify compact common channels and projected acquired densities at every cut.
8. Derive singular exponents from actual Cantor masses and product coverings. The noisy suffix gives an actual common channel. The continuous query produces a terminal scalar density, explaining the max(D,1) law rather than silently using ambient dimension.
9. Compose calibration and numerical root error in the same task state norm, then complete-law TV in common absolute risk. Multiply actual retained predictor/controller/simulator/phase counts. Keep code description, temporary workspace, output precision and time distinct.
10. Preserve uniform-block filtering and the full nonreset singular supplement; preserve the exact progressive acquisition/minimax theorem and finite-bit feasible implementation. Their special hypotheses do not redefine the general foundations theorem.

The finite-horizon serial lower/upper pairing is new in this revision relative to the pinned R8 source. Basic projection, quantization packing and telescoping are inherited or standard tools. Provenance and successful build operations are not mathematical novelty.
''',
'PROOF_AUDIT.md':'''# Proof audit — restart R9

## Central argument
The lower and upper use the same fixed physical exploration and Bayes baseline. A suffix code is obtained after fixing every independent algorithm coin; it is not allowed to choose a different physical policy. The upper's finite index is defined after every raw call. Its global cover maps back into the same candidate domain. The actual report law, not a candidate-generated law, controls moments. Minkowski needs no independence. At the final task state, orthogonal projection identifies squared state error with excess.

The lower uses arbitrary Hilbert centers, not just centers in the image. A ball intersecting the image pulls back into a state ball of twice the radius divided by the response modulus. The half-mass argument retains p_t and yields the displayed p_t^(1+2/s_t) constant. The criterion compares actual exponents supplied by independently checked covers and submeasures; it does not infer an implementable cover from optimal q_M alone.

## Rank-sensitive verification
A=DC_H is invertible by raw Gaussian square completion. Its query-projected partial column ranks may change. Their coordinates update linearly with norm <=1, so the Euclidean compander is applied online. Conditional remaining reports have a positive definite Gaussian covariance even with correlated prefixes. Compact conditioning bounds the density below. The projected acquired statistic has full covariance on its rank space and hence a bounded density. Restriction only decreases that measure. Query-frame and derivative lower hold on a compact range including line segments. The terminal scalar density argument is unchanged and uses I-Sigma positive definite. The low-rank statistic is not asserted sufficient for the entire report kernel.

## Singular verification
Cylinder lengths and masses are computed from the preparation. Strong separation supplies uniform finite overlap at each fixed ratio. Weighted allocations of binary depths give <=M centers and M^(-1/D_i) radii. Rounding after each append never leaves the compact candidate domain. The entire conditional suffix includes the remaining Cantor variables, noisy V, B, phase and costs. Its product minorization retains alpha. The response lower is an integral against the actual query frame. The terminal scalar lower is separately proved from a sphere slice density on an interior interval; this is why D<1 cannot bypass terminal quantization.

## Not yet proved
Universal causal-width-only sufficiency; all natural kernels admitting a global inward cover; unknown-kernel/value-dependent adaptive design; optimal program/workspace/time bounds; parameter-uniform behavior as noise, frame or gap constants degenerate; unlimited stopping and infinite-horizon rate equality. These are genuine remaining mathematical tasks, not reasons to abandon the mother problem.

This is an author-side proof audit, not a commissioned external referee report or a machine-checked proof certificate.
''',
'NOTATION_AUDIT.md':'''# Notation audit

- H_t is the complete prefix (public coins/actions/costs included); U_t is all genuine post-cut information available before prediction. O_t is one complete raw report in the serial theorem.
- P_T and B_T always refer to the same terminal task and physical law within a theorem. A different experiment is compared by absolute risk unless a common baseline is explicitly transported.
- S_t,Z_t in the serial theorem are task-realization spaces/states; they may be proper factors of the full future-test quotient.
- s_t is a cut exponent, s_* its maximum; s_T is terminal. r_j in the Gaussian rank subsection is an integer partial rank, while r_j in the separately introduced Cantor subsection is a contraction ratio. They are not used in the same statement. Cantor dimensions are d_j and cumulative D_i.
- rho_t is an acquired finite submeasure; p_t is its actual mass. xi_t is its Hilbert response image. No normalization is implicit.
- eta_t is a suffix probability in the central theorem. Numerical errors in cor:serialerrors are u_t, not eta_t.
- A_t in the central theorem is a scalar moment envelope; A=DC_H in the Gaussian subsection is an explicitly reintroduced matrix. The two are locally scoped.
- M is the entire data-dependent retained label tuple at each cut. Q is a separately stored deterministic phase count. Scratch, description, numerical precision and physical time are never equated with log2 M.
- Fixed raw report count T excludes separately charged preparation/audit. The new model examples explicitly have N=d+3.
- All native labels, references, active inputs and bibliography keys are checked against the manifest. Supplement S has its own section numbering and is supplied in full.
''',
'SCOPE_AUDIT.md':'''# Scope audit

## Established with native proofs
A finite-horizon general serial transfer theorem pairs actual continuation submeasure lower bounds with a single recursively implementable global-cover upper. Under matching observable cut exponents, online error is governed by the largest exponent and checkpoint error by the terminal exponent. Their constant-factor equivalence is characterized within that class. Changing-rank noisy correlated Gaussian observation and a singular analog observation class each verify all hypotheses from raw kernels. The latter includes the D<=1 to D>1 transition caused by a continuous future query.

## Retained and expressly credited
R8 already established exact/two-sided/conditional functional-cut comparison, raw minorization, sequential-chart equivalence and full-rank noisy regression. R7 supplied the dominated cut, optimized independent-tail progressive acquisition, attained early-erasure defect, standard filtering task and finite-bit feasibility. R4--R6 supplied the candidate/block and singular/stopping/morphism mechanisms. Their substantive sources remain supplied, not deleted or rebranded as R9 discoveries.

## F1--F4
F1: all-cut matching and a class compatibility criterion, together with retained uniform-block results. The new serial constants are finite-horizon, not uniform in time without extra stability.
F2: same-metric numerical/calibration composition and typed causal transfer; matched N,M,delta,attained-epsilon remain proved for the specified progressive class. No universal joint rate for all experiments is claimed.
F3: genuinely singular acquired laws and changing observable ranks have full native verification. The full nonreset, nonuniform activity singular dynamics remain in Supplement S.
F4: noisy Gaussian regression and singular geometric observation both instantiate the new central theorem. Sparse Gaussian filtering and nonreset Cantor transport remain distinct block realizations.

## Genuine remaining proof tasks
Global necessity of the candidate-cover hypotheses; width-only recursive duality outside the certificate class; arbitrary correlated/value-dependent adaptive experimental design and unknown-kernel calibration; a matching optimal region for program, scratch, simulator/controller state, phase and time; uniform constants at singular parameter boundaries; unrestricted/infinite stopping. No TV-to-LDP, fixed-to-stopping substitution or unbounded-operator closure claim is made.

The exact Borel analog upper is not a free finite-precision computer. Finite description and arithmetic feasibility need the separately stated input and numerical certificates. The previous progressive finite-bit theorem is preserved without being exported to arbitrary coefficients.
''',
'RESOURCE_ACCOUNTING.md':'''# Resource accounting

| Resource | New serial theorem | Noisy rank / singular examples | Matched status |
|---|---|---|---|
| Raw acquisitions N | Fixed T report protocol plus preparation/audit, all failures/costs included | d+3 actual calls; suffix is one declared packet | General constants may depend on N; independent-tail progressive theorem has separately matched N-law |
| Data-dependent persistent alphabet M | Entire tuple <=M after EVERY call | Partial-rank quantizer / recursively quantized singular prefix; scalar final label | Matching exponent, with actual all-cut lower |
| Deterministic stored phase Q | <=T+1 predecision values, multiplicative if stored | Known schedule only, no encoded observation | Feasible multiplier; no universal phase-minimality claim |
| Simulator/controller state | Must be included if later consulted | No extra predictor-dependent exploration in the two new models | Product upper; reverse lower needs reverse certificate |
| Calibration / numerical precision | Same-state-metric root insertions u_t, weighted by later gains | Separate finite report/computation error certificate required | General upper, not unavoidable lower; attained progressive calibration remains matched |
| Complete causal deficiency epsilon | L_max epsilon in common absolute risk | Full typed interface and strategy lift required | General upper; inherited early-erasure pair attains matching defect in its task |
| Program description | Cover, thresholds, known kernel/schedule/coefficients described separately | Exact Borel theorem alone need not provide finite descriptions of arbitrary real data | Finite-bit feasible region proved for progressive family only |
| Temporary workspace | Current report/readout workspace erased at next cut | No retained exact H, posterior, or old query packet | No general optimal scratch lower |
| Output | Final finite task label; any streamed vector is write-only | Bounded scalar forecast | Output-grid cost explicit where applicable |
| Computational / physical time | Separate from labels; finite T gains explicit | No unit-cost arbitrary real arithmetic assertion | Feasible accounts where certified, not a general optimal region |

At every fixed cut the phase is known or separately counted. A data-dependent controller cannot hide in Q. A physical suffix packet is available only on its paid call and cannot be divided into free rereadable calls. A relaxed lower can give the decoder the whole suffix without making that memory free in the upper.
''',
'HISTORY_COVERAGE.md':'''# History and actual review coverage

The four canonical control files were read, with particular attention to A0--A5, T02/T03/T07/T08 and G1/G3 in the original v0.1 outline. The canonical archived v1 index was fetched; it identifies the original source and receipt objects. The latest R7 report was fetched in full and used as the current referee input. R4--R8 pipeline derivations and the directly used R8 general-cut/chart/noisy/regression/resource dependencies were inspected. All R8 substantive native sections remain active in this new article. The full R6 technical text is supplied and rebuilt as Supplement S.

The branch first starts at the canonical commit. Exact R4, R5, R6, R7 and R8 sibling trees are preserved when connecting these dependencies. The old review branches, all listed realization branches and frozen archive are not written. Their original content remains available independently. The ordered-measurement, finite-action, streaming-space and quantum-discrimination programs are not premises for the serial theorem and remain separate research lines.

Preservation is not fresh mathematical certification. This revision does not assert that every theorem in all v1--v96 manuscripts, every old referee report, or every independent realization has been re-proved or exhaustively re-reviewed during this run. No conclusion requires that assertion. The dependence on the original elementary propagation and projection tools is explicit; they are not renamed as new discoveries.

R8 was already present on the remote when this task started. Its conditional/two-sided-cut theorem, raw common-channel lemma, chart construction, noisy regression result and expanded coding comparisons are inherited research, not newly attributed to R9. The new native addition is the all-stage exponent/compatibility theorem, its candidate-moment composition, and its all-cut changing-rank/singular verifications.
'''
}
for name,text in new.items(): (p/name).write_text(text)
pre='''# R9 response and provenance of the R7 corrections

This revision responds to the same latest R7 external report pinned below. Its detailed 16.1--16.8 and all thirty Section17 responses were already drafted in the remotely present R8 research source. They are retained in full below and credited as inherited corrections, not newly claimed R9 work.

## Additional mathematical response in R9

`thm:serial` makes the maximum of actual continuation exponents sufficient as well as necessary within a global-cover/Lyapunov certificate class. It builds a single online machine across changing state spaces, rather than only the sequential-coordinate chart. The explicit root-error profile and actual lower constants retain raw horizon/gains/mass. The checkpoint/online criterion is `max_t s_t = s_T` and the ratio otherwise is `M^(2/s_T-2/max_t s_t)`.

`thm:ranknoisy` verifies all active cuts, with partial observable ranks rather than the hidden ambient dimension. Its rounded partial-span recursion never stores the exact prefix. `thm:singularserial` verifies noninteger acquired exponents directly from Cantor preparation kernels and proves that a continuously sampled future query can raise the terminal exponent, giving `M^(-2/max(D,1))`. Both derive hypotheses of the general theorem; neither replaces it.

This further addresses Section18.1 (a class compatibility criterion) and 18.3 (noisy continuation is quantitatively essential) and strengthens F3. Bare-width universal duality, unrestricted observation-dependent acquisition and a fully matched computational-vector region are still open within this manuscript, not silently claimed complete. The title and mother problem are unchanged.

## Retained complete point-by-point response from the R8 research input

'''
(p/'REFEREE_RESPONSE.md').write_text(pre+(old/'REFEREE_RESPONSE.md').read_text())
lit='''# Literature comparison and attribution — R9

The theorem-level comparison below is inherited from R8. New R9 claims are narrower than a claim of discovering functional coding, companding, small-ball lower bounds or recursive error propagation. The original foundations outline already contains the elementary T07 projection and T08 telescoping mechanism. The new serial theorem pairs those mechanisms with actual conditional-response submeasures at every cut, uses a code-independent candidate-moment envelope on global domains, and proves the resulting class compatibility criterion. Rank-sensitive noisy and singular final-query verifications establish its meaning beyond terminal geometry.

Primary online verification in this run included the original Wyner--Ziv IEEE record; the IBM Research Equitz--Cover author record; the NeurIPS 2025 original Anjarlekar/Etesami/Srikant record; PMLR 300:1423--1431 Zhu/Lu; and the Hudak et al. arXiv:2602.08734 author version. The latter is cited as the verified accepted author version rather than relying on an unverified page range. The one-cut/source-coding and allocation comparisons remain explicit and are not priority certificates.

'''
(p/'LITERATURE_COMPARISON.md').write_text(lit+(old/'LITERATURE_COMPARISON.md').read_text())
