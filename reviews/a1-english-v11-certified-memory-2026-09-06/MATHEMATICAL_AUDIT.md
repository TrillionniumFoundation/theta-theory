# Mathematical audit of the A1 v11 principal chain

**Pinned submission:** `f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0`.  
**Scope:** the main collision-classification and finite-compilation chain, including selected critical inherited arguments. This is a referee's proof audit, not formal certification of every appendix. Source keys are defined in [SOURCE_INDEX.md](SOURCE_INDEX.md).

## 1. Experiment and nontrivial attainment

The likelihood of a history is the product of its accepted and rejected report factors, normalized by its prior integral. Every factor is bounded below by a positive constant. Commands are available only when received; a future-only continuation cannot inspect a discarded prefix. The fixed finite product-probe menu is physically executable and spans the formal homogeneous future moment coordinates. This is a prediction problem for one shared hidden parameter, not one in which that parameter is resampled at each step. These operational quantifiers are necessary to the stated memory problem and remain explicit. [S2]

At the common interior binomial tuple, write the factors as \(1+c_i z\), with \(z=t^D\), ignoring harmless constants. For distinct nonzero \(c_i\), the polynomials \(P_i(z)=\prod_{j\ne i}(1+c_jz)\) form a basis through degree n−1: evaluation at \(-1/c_i\) proves independence. Their products with each one-step monomial give precisely

\[
 \{jD:0\le j\le n\}\ \cup\
 \{a_i+jD:1\le i\le r-2,\ 0\le j<n\}.
\]

The supports are disjoint because the interior exponents lie strictly between 0 and D. Hence the product tangent has dimension \(n(r-1)+1\). It contains the product itself. The normalized differential is the linear moment pairing followed by \(v\mapsto v-p e_0v\), with \(e_0p=1\); its kernel on the pairing image is exactly the constant normalization direction. Exactly one rank, rather than an uncontrolled number of directions, is lost. [S3]

Strict mixed-moment positivity follows from the determinant integration identity and positivity of generalized Vandermonde determinants on ordered positive points. Full support supplies positive measure to a product of separated subintervals; no prior density is required. The confluent version uses complete exponential-polynomial blocks. The logarithmic functions extend boundedly to zero because their positive exponents stay away from zero; the constant zero-exponent block has multiplicity one. The stated Rolle argument and determinant sign yield the required full-rank pairing. [S3, S5]

## 2. Collision uniformity is not just a spectral calculation

For finite Leja pivots \(d_j\), the active triangular block of the Newton evaluation matrix has uniformly bounded entries and inverse. The inactive tail multiplies zero pivots. Thus no reciprocal of a vanishing gap is used in the metric comparison. Evaluating monic Newton polynomials on any selected node set gives

\[
 \prod_{j\le\ell}d_j\le\mathcal V_{m,\ell}
       \le\ell!\prod_{j\le\ell}d_j.
\]

The auxiliary exterior singular-value formulation follows by bounded changes of basis, including at rank loss. It is correctly distinguished from statistical attainment. [S4, S6]

An arbitrary prefix of divided differences spans all Hermite data for its multiset, not isolated highest derivatives. This remains true for nonadjacent repeated nodes. Applied to \(t^{Hz}\), it gives complete logarithmic blocks. Their pairing with the actual product tangent yields a surjective normalized differential onto the first \(p_{n,m}\) desingularized coordinates. Uniform continuity of \(t^c\log^j t\), finitely many formal orderings, and compactness of K then provide a uniform least row singular value. The local inverse argument retains the all-failure likelihood before integrating complementary command coordinates. This supports an unconditional minorization rather than a probability-zero chosen-history lower bound. [S3–S6]

The whole reachable image is a different matter. At fixed calibration and report word, its coordinates are ratios of command polynomials with positive evidence. Real prior moments are coefficients of a bounded-format formula; they need not vary semialgebraically with calibration. Normalizing individual factors bounds the image dimension by n(r−1), and the future ambient dimension gives the other truncation. The thin-rectangle lemma uses bounded affine-section component counts and the real entropy inequality. Projection volumes of the containing rectangle are bounded by products of its largest widths, and variations above the set's dimension vanish. Its final budget inversion explicitly handles small M and recentres on reachable points. No local chart is being substituted for this global cover. [S5–S6]

For the lower law, the minorized cube scaled by \(d_1,\ldots,d_\ell\) has mass outside M sufficiently small balls. The physical/raw linear maps and active Newton inverse have uniformly bounded norms. Randomized label assignments cannot beat nearest-centre error; independent coding randomness can be fixed and averaged. Every checkpoint uses a prefix of the same exploration law, so taking their maximum is justified. [S6]

## 3. Finite compilation has the necessary feasible-state discipline

Let e_n(M) be the unrestricted M-centre covering radius of S_n. A finite command h-net gives an A_n h-net of reachable histories. Approximate farthest-first selection, with evaluation error at most tau, produces true reachable representatives with radius

\[
 R_n\le2e_n(M)+A_nh+4\tau.
\]

Each transition target is evaluated by appending a command and report to an actual representative history. An arbitrary perturbed vector is never supplied to a posterior update. The approximation comparison adds a further 4 tau, giving

\[
 E_{n+1}\le L_nE_n+G_nh+2e_{n+1}(M)+A_{n+1}h+8\tau.
\]

Fixed horizon and the query Lipschitz constants yield the stated all-history bound. Offline histories are not runtime memory: the running `Machine` retains only an index, with stage and program supplied separately. The command-coding rule must be memoryless for the converse; otherwise it could transmit history. This restriction is explicit. [S7, S10]

For monomial experiments, the formal moment quotient has denominator at least \(\kappa^n\). Keeping coincident formal labels does not require deciding equality. Perturbed entries need not themselves form a consistent positive moment sequence, because numerical vectors are used for offline selection and evaluations, not asserted to be exact reachable states. These are valid responses to common finite-precision pitfalls. [S7–S10]

## 4. Audit of the ten additional named results

### Separated floor and uniform resource bounds

With k=floor(N/2), m=N−k and d0=(r−1)k, the future chain has m(r−1)+1 distinct sites, adjacent gaps at least delta_K. It contains d0 positive sites. Their normalized Vandermonde product is at least

\[
 (\delta_K/H)^{d_0(d_0-1)/2}.
\]

Its term in the profile therefore gives

\[
 \Xi_N(M,a)\ge(\delta_K/H)^{d_0-1}M^{-2/d_0}.
\]

The argument includes r=2 and d0=1. Choosing h and tau of order \((M+1)^{-1/d_0}\) absorbs their squared errors in the **full** profile, not merely its floor. Counting command-grid entries then gives the sufficient program bound. The constants can depend on the fixed chamber and experiment; a smallest nonzero additive-gap estimate is not needed. The attribution to the preceding referee note is present. [S8]

### Observable radius and first-success selection

For a finite approximate history list and its actual greedy selection, the extra farthest point and the M selected points are r_n-separated. Covering the true set by M balls and transferring to the approximate samples gives

\[
 r_n\le2e_n(M)+2\tau.
\]

Moving a general reachable point to a grid history, its approximation, a selected approximation and finally its true representative gives

\[
 e_n(M)\le r_n+A_nh+2\tau.
\]

When tau=h and c=A+2, these inequalities imply

\[
 \max(0,r/2-h)\le e(M)\le r+ch.
\]

The stopping test r≥4ch eventually succeeds if e(M)>0: it is guaranteed once h≤e/(5c). At success, h≤r/8 since c≥2, so

\[
 3r/8\le e\le5r/4.
\]

For the first successful b>0, failure at b−1 and h_(b−1)=2h_b give e<10ch_b, while success and r≤2e+2h_b give h_b≤e/(2c−1). The initial b=0 case is bounded by the fixed state diameter. These are sufficient to prove the claimed scale and logarithmic refinement count; no monotonicity of the noisy radii across refinements is required. [S8]

The absolute-tolerance variant is also sound. If the radius test has not fired when h≤zeta, the previous failure and dyadic step imply h>zeta/2 unless b=0. Together with e<5ch, this gives the comparison with e+zeta. It does not decide whether a general compact set has zero covering radius. [S8]

### Residual and finite-input certificates

The transition residual includes two evaluation errors; the output residual includes one. Induction proves the displayed error bound for any supplied program. It does not assert that every program satisfying a large bound is good. This distinction is the source of the diagnostic issue in P11.1, not a defect of the proposition. [S8, S10]

For each report factor, entrywise coefficient error epsilon gives coefficient norm error at most Cf epsilon, Cf=Jr. Telescoping the product and then integrating the moment-table error gives

\[
 D_n=nC_f(B+1)^{n-1}+(B+1)^n.
\]

The numerator and evidence errors are at most epsilon D_n. If this is at most \(\kappa^n/2\), the computed denominator is positive. For a raw moment q=A/Z in [0,1], subtracting q from the approximate quotient yields

\[
 \left|\widetilde A/\widetilde Z-q\right|
 \le2\epsilon D_n/\widetilde Z.
\]

The exact-query coefficient norm changes the numerator constant as stated. Clipping does not increase probability error. Fixed finite degree and positive evidence therefore justify the input-accuracy transfer. They do not, by themselves, identify exact intermediate bit lengths with rounded working precision; P11.3 addresses that separate sentence. [S8–S10]

### Profile recovery, causal realization, and phases

The reverse inequality in `lem:cover-profile` uses an arbitrary M-centre raw cover to construct an admissible checkpoint code with a bounded linear physical decoder followed by clipping. Its worst squared error is at most C(e_n+epsilon)^2. The **already established** checkpoint converse bounds this below by c Psi. The forward inequality is the inherited raw reachable cover. Hence e_n^2 is comparable to Psi and e^2 to Xi without invoking the adaptive theorem's conclusion. [S6, S9]

The separated floor ensures e>0. Applying the adaptive theorem gives query error O(e), and squaring gives regret O(Xi). The raw states lie in a unit cube, and M^−2≤Xi≤1; the logarithmic precision statements and absorption of output bits into the transition-table bound follow. Read-only program size is a sufficient bound, and rational-operation counts exclude oracle time. Neither is advertised as a converse. [S7–S9]

In the stated four-cell, five-trial family, J=4 and the sufficient program factor is M F^−2. Substituting the three terms of F gives the three displayed minimum terms. This algebra is correct conditional on the inherited example's profile. The entire specialized two-parameter derivation was not independently reaudited here; nor were its phases tested numerically. They must not be presented as new lower bounds on program length. [S9]

## 5. Result of the audit

The strongest negative findings in this round concern the evidentiary force of the tests, a numerical-model sentence, and citation traceability, alongside the independent editorial judgment. No essential new gap was found in the examined main rate/compilation chain. Known calibration, fixed horizon, a fixed arbitrary full-support prior, certified offline input access, and memoryless command coding are real hypotheses, not oversights to be silently removed. Any future extension must re-establish the relevant bounds rather than transfer the current constants outside that scope.
