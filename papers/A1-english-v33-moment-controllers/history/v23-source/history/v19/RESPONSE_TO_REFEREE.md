# Response to the v18 referee — A1 English v19

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.
**Controlling report:** `reviews/a1-english-v18-independent-2026-09-07/REFEREE_REPORT.md`, commit `e5fff530c95a4f3aa1163a2087838ff2795f052b`.
**Reviewed manuscript:** `papers/A1-english-v18`, commit `be8effe038608bef255fa97318a9ee3b4434af2d`.
**Revision:** `papers/A1-english-v19`, on a new revision branch. Stable theorem labels below refer to this manuscript.

We thank the referee for distinguishing inspected correctness, attribution, and significance. We accept the specific attribution correction and address the significance assessment by adding a structural extension and a realizability theorem with a full degeneration law. We do not treat the editorial assessment as a theorem, claim that a checklist guarantees acceptance, or respond by reducing the physical model. All eleven v18 results remain with their complete proofs; so do the complete inherited collision, circular, causal, inverse, uncertainty, and numerical-resource arguments.

## E18.1 — the finite square-pairing predecessor

The report identifies a precise omitted predecessor. The revised introduction, the rectangular section, `sections/pairing_comparison.tex`, and the bibliography now cite Banaji and Pantea, *SIAM Journal on Applied Dynamical Systems* 15 (2016), 807–869, Definition 2.24 and Lemma 2.36. We checked these passages in arXiv:1309.6771v6, including the convention that a strict compound sign means weak common sign with a nonzero entry.

For finite X, let A and B be the two d-by-m evaluation matrices. The pairing determinant is det(A diag(w) B^t). In their rank criterion, D2 A is onto, so rank(A D1 B^t D2 A)=d if and only if det(A D1 B^t) is nonzero. Normalizing positive weights gives positive probability weights. Thus the finite square necessity-and-sufficiency core is attributed to this existing strong-compatibility result. The manuscript no longer leaves attribution of Andréief's identity to carry the novelty accounting for necessity.

The compact-space/full-support formulation, posterior normalization of an augmented tangent, and unconditional history-mass consequence are distinguished from that inherited finite algebraic core. The theorem and its proof were not removed or weakened. The added rectangular formulation also makes a proactive comparison with Müller–Feliu–Regensburger–Conradi–Shiu–Dickenstein, Lemma 2.1, rather than presenting its finite sign-vector specialization as a new theorem.

## E18.2 — mathematical response to the significance assessment

The report correctly distinguishes the general fixed-prior dimension theorem from an anisotropic classification and credits the existing collision chain. We retain that distinction. The new response comprises the following results, with full proofs in the main text.

### 1. Rectangular universal attainment, not an assumed square reduction

`thm:v19-rectangular` treats arbitrary finite-dimensional spaces E,F of continuous functions on a compact metric space, with dim F <= dim E. Their moment pairing has full column rank under every full-support probability if and only if every nonzero f in F has a multiplier g in E with fg nonnegative and nonzero somewhere. The proof passes through the exact full-support moment image, not a limiting positive-density assertion or a square determinant selected in advance.

`thm:v19-rank-alternative` gives more than a full-rank yes/no criterion: for every subspace U of F, the possibility of U lying in a pairing kernel is exactly the condition that zero belongs to the relative interior of the convex hull of the product-evaluation vectors (u_i e_a). It follows that the minimum pairing rank over all full-support priors is k minus the maximum permitted kernel dimension. Each permitted kernel is realized by an actual full-support mixture with at most jd+1 added atoms. The mixture weight is not claimed uniform.

`prop:v19-dominated-margin` gives an exact distance formula for the least singular value over priors dominating c times a fixed full-support probability. `cor:v19-rectangular-history` converts rectangular pairing rank to normalized rank by subtracting exactly one evidence direction and proves unconditional mass by integration in all unused command coordinates. It does not assume that the radial direction is a physical command derivative.

`prop:v19-pentagon` realizes a genuinely rectangular experiment with positive affine likelihoods and a physical query. The augmented tangent has dimension three and the test space dimension two. Pairing rank is two for every full-support prior, but no fixed two-dimensional tangent subspace containing evidence works universally. Four explicit separators prove the rectangular property; four consecutive-difference inequalities prove the square-subspace assertion. The qualifier “containing evidence” is essential and is printed in the theorem.

These statements extend the attainment mechanism beyond the square regime rather than claim newness for finite sign-vector linear algebra. They provide actual priors, rank alternatives, and physical histories in that extension.

### 2. Arbitrary covariance germs inside one fixed physical experiment

`thm:v19-covariance-realization` fixes a latent sign cube, likelihoods bounded below by 1/4, and a uniform menu of binary queries with probabilities in [1/4,3/4]. For every small q-by-b matrix A, the prior density is

    d mu_A / d mu_0 = 1 + sum_{j,i} A_{ji} xi_i zeta_j.

The density stays between 1/2 and 3/2, and the weighted covariance is exactly A/(8 b sqrt(q)). The prior map is affine and injective. Thus an arbitrary scaled real analytic matrix germ, including all its determinantal rank loci, is realized while the physical experiment, query weights and prior domination remain fixed. This is not a spectrum postulated after assuming a risk envelope, and it is not another scalar cancellation example.

### 3. A complete analytic-arc memory law and all permitted phase orders

`lem:v19-analytic-orders` supplies the classical one-variable analytic Smith argument in the rectangular, possibly rank-deficient case. It identifies the least vanishing order A_l of l-minors with sums of ordered invariant orders. The classical matrix result and its singular-value interpretation are attributed to Kaveh–Makhnatch; neither is counted as an independent novelty claim.

`thm:v19-analytic-memory` then proves, for the entire positive affine class along an analytic covariance arc, the simultaneous law

    R_{M,1}(t) comparable to max_l t^(2 A_l/l) M^(-2/l),

uniformly for all integer M >= 1 and sufficiently small t >= 0, with the exact zero endpoint treated separately by the affine theorem. The constants belong to the fixed analytic germ, not an unrestricted collection of arcs.

`cor:v19-memory-phases` determines the phase exponent at M=ceil(t^(-gamma)) as min_l 2(A_l+gamma)/l, the ordered transition values l alpha_(l+1)-A_l, and the recovery of A_l from the full integer-budget checkpoint curve. Together with the realization theorem, every ordered nonnegative integral list of permitted length occurs under one fixed positive physical interface and one common density envelope. A displayed matrix has determinant order six and singular orders (1,5), producing the changeover M comparable to t^(-4).

The claims are arcwise and one-acquisition-step claims. No simultaneous multi-parameter Smith form, unbounded-horizon result, finite-data inversion, or covariance substitute for the multi-step theorem is asserted. This delineation does not withdraw any earlier result: the complete multi-step collision and circular classifications remain stronger in their own directions, with their independent causal constructions.

### 4. Contribution and journal standard

The revision locates the contribution in the experiment-level results: rectangular attainable histories with explicit prior alternatives; a fixed physical experiment realizing arbitrary small covariance germs; and a sharp, jointly uniform memory law with all permitted analytic-arc phases. The classical convex separation, positive diagonal criteria and Smith form remain explicitly attributed inputs. The collision-uniform acquisition/cover/update synthesis remains a principal result rather than being displaced by generic dimension language.

We submit these stronger statements for a new mathematical and editorial assessment. The receipt of a passing diagnostic or a correct proof is not represented as settling the referee's four-journal significance judgment. The manuscript has not been narrowed to an easier task or reformulated as a no-go result in response to that judgment.

## Standalone preservation observation in Section 8

We agree with the nonblocking engineering observation, including its qualification: the old full validator already checked the inherited inverse source against the original v17 manifest. The issue concerned the advertised standalone preparation mode, not a demonstrated hole in the full validator.

The new `build.py` calls `verify_history()` before any baseline copy. It checks the archived v18 manifest against its original Git blob `f4245151593153b5e8ec77e30449588cdd478dc4`, every archived source against that manifest, and all unchanged active mathematical/compiler/test files against the same independent baseline. It also pins the original v17 manifest blob `e8870117088145c9db0f71fc38e9be0ff0d27de2` and checks the current operational-inverse source against that earlier record.

The actual baseline is reconstructed from `history/v18`, not copied from the changing current mathematical sources. The original preparer runs unchanged there. Compiled proof/statement multisets and all previous labels must be contained in the new compilation with identical bytes.

`validate.py` mutates a proof in `sections/operational_reconstruction.tex`, invokes standalone `build.py --prepare-only`, requires a nonzero exit specifically identifying changed inherited source, restores the exact original bytes in a finally block, verifies the current manifest, and then builds the complete manuscript. Its executed result is recorded separately from the mathematical diagnostics.

## Preservation, checks, and scope

The prepared source contains 109 proof blocks and 112 theorem-class statements: the complete 99/102 v18 blocks plus ten new 1-to-1 statement/proof pairs. All previous labels survive. No existing proof is replaced by a reference to an older version. All prior material remains on the branch, and the original v18 directory and review reports are left unchanged.

The validator reruns eight inherited author suites (v10–v15, v17, v18), the new exact symbolic/rational suite, the standalone mutation check, and the full three-pass PDF build. The new suite checks full-support kernel witnesses, the rectangular physical example, weighted Walsh covariance identities, actual likelihood/density bounds, non-diagonal rectangular determinantal orders, zero endpoints, and all phase branches in finite exact families. It is not an exhaustive search over encoders or a proof of every universal quantifier by enumeration.

The original report's eleven inspected v18 results remain credited as having survived that report's stated checks. This revision does not turn that assessment, its own source-preservation checks, or a PDF build into a claim of independent formal verification of every inherited argument. The attached source and receipts permit the next referee to examine both the added mathematics and the retained material directly.
