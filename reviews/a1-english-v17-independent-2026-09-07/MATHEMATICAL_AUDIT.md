# Mathematical audit accompanying the A1 v17 referee report

**Pinned submission:** `1f3838d89a5820b853d1e4b78194293b23e70bd2`.  
**Date:** 7 September 2026.  
This note supplies independent calculations behind the report. Boundary examples are expressly separated from counterexamples to the manuscript. Source paths and theorem labels refer to the pinned v17 directory; see [SOURCE_INDEX.md](SOURCE_INDEX.md). No formal verification is claimed.

## A. Exact continuous-envelope identity

Let `s_1>=...>=s_p>=0`, put `V_0=1`, `V_j=prod_{i<=j}s_i`, and define

$$
e(b)=\max_{1\leq j\leq p}(V_j/b)^{1/j},\qquad b\geq1.
$$

For every l and b, the l-th term gives `b e(b)^l>=V_l`. Suppose first that `s_l>0` and set `b_l=V_l/s_l^l`. Since each of the first l scales is at least `s_l`, this budget is at least one.

For `j<l`,

$$
\frac{V_j}{b_\ell}
=\frac{s_\ell^\ell}{s_{j+1}\cdots s_\ell}
\leq s_\ell^j.
$$

For `j>l`,

$$
\frac{V_j}{b_\ell}
=s_\ell^\ell s_{\ell+1}\cdots s_j
\leq s_\ell^j.
$$

The l-th expression equals `s_l^l`. Thus `e(b_l)=s_l` and `b_l e(b_l)^l=V_l`. This proves the continuous identity without a differentiability or strictly-separated-scales assumption. Several products may share one supporting budget.

Let r be the number of positive scales. If `r=0`, the envelope is identically zero. If `0<r<l`, put `b_r=V_r/s_r^r`. For `j<r`, comparison of the j-th and r-th branches reduces to

$$
b^{r-j}\geq V_j^r/V_r^j.
$$

This holds at `b_r` by the preceding support calculation and persists as b increases. Consequently the r-th branch dominates for all `b>=b_r`, and

$$
b e(b)^\ell=V_r^{\ell/r}b^{1-\ell/r}\longrightarrow0.
$$

This proves the zero-product cases. It does not claim the infimum is attained at a finite b. The manuscript's separate treatment of zero rank is essential and correct.

**Disposition:** `lem:integer-envelope-duality`, continuous component, passes this audit.

## B. Integer budgets: valid sandwich, generally not equality

For positive `s_l`, let `M_l=ceil(b_l)`. Monotonicity of e and `b_l>=1` yield

$$
V_\ell\leq\inf_{M\in\mathbb N,\ M\geq1}M e(M)^\ell
\leq M_\ell e(M_\ell)^\ell
\leq M_\ell s_\ell^\ell
\leq2V_\ell.
$$

If the relevant product vanishes, restricting the large-budget argument in A to integers still gives infimum zero. This validates the integer result, including its endpoints.

The following independent calculation explains why the inequality should not be silently strengthened. Take

$$
s=(1,2/3,2/3),\qquad V_2=2/3,\qquad V_3=4/9.
$$

For `l=2`, the real supporting budget is `b_2=3/2`. At `M=1`, `M e(M)^2=1`. For every integer `M>=2`, the third branch dominates, and

$$
M e(M)^2=(4/9)^{2/3}M^{1/3}.
$$

This is increasing in M. Therefore

$$
\inf_{M\geq1,\ M\in\mathbb N}M e(M)^2
=(32/81)^{1/3}>2/3.
$$

The cube of its ratio to `V_2` is `4/3`. This is a witness for the necessity of integer slack, not a counterexample to the stated factor-two bound. No optimality of the universal constant two is asserted here.

## C. Passing from envelope bounds to optimal-risk invariants

Suppose, with constants independent of every parameter being compared,

$$
c e_s(M)^2\leq R_s(M)\leq C e_s(M)^2.
$$

For each fixed l, the map `x -> x^(l/2)` is increasing on nonnegative x. Multiplying the resulting inequalities by M and taking infima gives

$$
c^{\ell/2} V_\ell
\leq\mathcal I_\ell(R_s)
\leq 2C^{\ell/2}V_\ell.
$$

No minimizer of the optimal coding problem is required for this step. No exchange of a supremum over histories with an infimum over budgets occurs. The assumption is already a two-sided statement about the optimal curve.

If two such curves are uniformly comparable, their transforms, hence their products, are uniformly comparable. Conversely, suppose corresponding products in a fixed padded dimension satisfy `A^(-1)V_l<=W_l<=A V_l`. Their squared-envelope terms differ by factors between `A^(-2/l)` and `A^(2/l)`. Taking a maximum gives a uniform comparison, and the forward constants transfer it to the risk curves. Matching zero sets are necessary; otherwise no positive two-sided comparison exists.

For a fixed positive rank r, the eventual envelope is `(V_r/M)^(1/r)`. Hence

$$
\lim_{M\to\infty}\frac{\log R_s(M)}{\log M}=-2/r.
$$

The all-zero risk curve requires a separate convention; taking the logarithm of zero is not part of this argument. Ratios of positive consecutive transforms recover each individual scale only up to constants. They do not recover an exact singular vector, a particular latent parameter, or the leading constant of optimal quantization.

**Disposition:** `thm:operational-reconstruction` passes under its stated fixed-dimension, uniform-comparison hypotheses.

## D. Why the monomial substitution is legitimate

The determinant volumes themselves are defined by a maximum over subsets. An inverse formula for an arbitrary list of coefficients would be false. The needed additional fact is the ordered Leja representation in `lem:leja-scales`.

With normalized nodes in `[0,1]`, adding a selected node multiplies each candidate product by a gap at most one. The maximum defining the next pivot cannot increase. Thus `d_1=1>=d_2>=...>=0`. Exact repeated nodes produce zero pivots rather than an instruction to invert them.

For each l, the product of the first l pivots is the Vandermonde product of that greedy subset, hence is at most the maximum volume. Conversely, the monic Newton polynomials on the first l selected nodes have maximal absolute values bounded by those pivots on the finite node set. The determinant expansion on any l nodes gives

$$
\prod_{j\leq\ell}d_j\leq\mathcal V_{m,\ell}
\leq\ell!\prod_{j\leq\ell}d_j.
$$

This comparison is gap-independent at fixed dimension, and remains meaningful when a product is zero. It is the justification for applying C, not a claim that the raw volume coefficients satisfy an unproved exact envelope identity.

At checkpoint `(n,m)`, truncate the ordered list after `p_{n,m}` and pad further indices with zeros. If there are fewer distinct positive future exponents, some pivots vanish even before that truncation. Thus a zero recovered product can mean either past limitation or physical collision. The inverse does not distinguish those causes without the known model data. The manuscript's “past-attainable” formulation is the correct one.

The strongest part of the monomial theorem remains the forward link from this list to actual histories. The binomial tangent has separated exponent support even when the future sums collide. Complete divided-difference prefixes span complete Hermite blocks; selecting isolated derivatives from incomplete blocks would not justify the Chebyshev pairing. The inspected proof uses complete prefixes, accounts for exactly one normalization direction, and augments the command map by kernel coordinates before deriving a measure minorization.

**Disposition:** `cor:monomial-operational-recovery` is supported by the actual ordered scales available in the inherited theorem.

## E. Circular paired scales and odd products

For `k=min(n,m)`, the real scale list is

$$
s_{2j-1}=s_{2j}=\tau^{2j},\qquad1\leq j\leq k.
$$

Counting the exponents gives

$$
V_{2j-1}=\tau^{2j^2},\qquad
V_{2j}=\tau^{2j(j+1)}.
$$

For even index `l=2j`, the squared-envelope term is

$$
(V_{2j}/M)^{1/j}=\tau^{2(j+1)}M^{-1/j}.
$$

The first odd term is no larger than the `l=2` term for `M>=1`. For `j>=2`, the logarithm of the `l=2j-1` term is a convex combination of the neighboring even logarithms, with weights

$$
\frac{j-1}{2j-1}\quad\hbox{and}\quad\frac{j}{2j-1}.
$$

It introduces no additional maximum branch. Nevertheless its continuous supporting budget exists: both products at `2j-1` and `2j` are supported at

$$
b=\tau^{-2j(j-1)}.
$$

Thus absence of a separately dominant odd branch does not make that odd product unrecoverable. Ordered-product structure, rather than a list of distinct visible phases, is doing the work. At zero contrast all physical scales vanish; normalized auxiliary coefficients need not vanish and are not themselves an observed information state.

For an additional independent check of the physical normalization, write posterior Fourier coefficients as `c_j=p_j/p_0`, and `Y_j=tau^j c_j`. Direct multiplication by `1+tau(z w+conj(z) w^(-1))` gives

$$
Y'_j=\frac{Y_j+\tau^2 zY_{j-1}+\overline zY_{j+1}}
 {1+z\overline{Y_1}+\overline zY_1}.
$$

The denominator is the posterior expectation of the positive normalized factor and is at least `1-tau`. The update therefore does not pay an inverse-contrast factor. This calculation agrees with the manuscript and with the independently implemented Laurent multiplication tests. The tests do not determine how large the theorem's uniform small-contrast interval may be; that interval comes from the quantitative submersion argument.

**Disposition:** `cor:circular-operational-recovery` and the inspected physical update and metric identities pass this audit.

## F. Boundary examples: none contradicts the printed theorem

### F1. Finite-budget observation cannot determine the last nonzero scale

Fix a finite integer B and `0<epsilon<=1/B`. Compare the ordered lists `(1,epsilon)` and `(1,0)`. Their squared envelopes are

$$
\max\{M^{-2},\epsilon/M\}\quad\hbox{and}\quad M^{-2}.
$$

They agree for every integer `1<=M<=B`. Their second products are respectively epsilon and zero, and their eventual slopes differ. The code checks finite instances; the inequality `epsilon M<=1` proves the assertion for every B. This is an exact envelope example, not an identification of two experimental optimal risks. It illustrates the exclusion already made in the new section.

### F2. Arbitrary coefficients really can be hidden

Take coefficients `(A_1,A_2,A_3)=(1,a,1)` with `0<a<1`. For every `b>=1`,

$$
\max\{b^{-1},(a/b)^{1/2},b^{-1/3}\}=b^{-1/3}.
$$

The transformed second coefficient is then `inf_{b>=1} b^(1/3)=1`, not a. The implied consecutive scales `(1,a,1/a)` are not nonincreasing. This example shows why the ordered-product premise is substantive. It is outside the premise and cannot be used as a defect in the manuscript.

### F3. A positive error floor destroys the zero-product interpretation

If `R(M)>=delta^2>0` for every positive integer budget, then

$$
\mathcal I_\ell(R)\geq\delta^\ell>0
$$

for every positive l, regardless of how many nonzero coding scales there are. This is why the common-name law cannot be fed into the known-prior rank interpretation. The manuscript expressly separates these statements.

### F4. The causal maximum loses checkpoint attribution

If two checkpoints have ordered-scale envelopes, their maximum records which envelope is largest at each budget, not which checkpoint generated it. Inserting or changing a checkpoint curve that remains everywhere below the maximum leaves that maximum unchanged. Thus a converse for a single maximum cannot in general recover all the individual checkpoint profiles. The paper declines that extension; no counterexample to its stated checkpoint result is being alleged.

## G. Global geometry and causal lower bounds: dependency check

For `lem:tame-rectangle`, bounded-format section complexity bounds the number of components of almost every affine slice uniformly in the coefficients. Sections of codimension larger than the dimension of the set are generically empty. For smaller codimension j, the translation parameters of nonempty slices lie in a projected rectangle. Its j-volume is bounded by a dimension constant times `a_1...a_j`, by the zonotope projection formula. Substitution in the classical real entropy inequality gives the dimension-truncated sum. This is a global argument; the local minorization is not used as an upper-bound proof.

At fixed calibration the rational posterior moment image has bounded format because its numerator and evidence denominator are polynomials of bounded degree in the commands. The coefficients may be arbitrary real prior integrals. This verifies the correct kind of uniformity; one does not need a definable family of priors or a semialgebraic dependence on calibration. Positive denominators and a finite number of report words give compact images.

For a lower bound, project prediction centers onto the physical query span, pass through uniformly bounded active inverses, and then project onto the first l positive attainable coordinates. On a minorized rectangle of side-product comparable to `V_l`, the union of M radius-b balls has probability at most a constant times `M b^l/V_l`. Taking b as a small multiple of `(V_l/M)^(1/l)` leaves a fixed positive mass. This argument works even when the chosen radius exceeds a small individual side, because the ball-volume bound is an upper bound on its intersection with the rectangle. The preceding active-coordinate restriction is essential at exact collisions.

Conditional averaging makes randomized decoder outputs no better under squared loss. Random assignment to centers cannot beat their pointwise nearest-center distance. Independent public coding randomness can be fixed and averaged without modifying the acquisition experiment. These steps do not cover an uncharged shared memory used to generate the command history, which is expressly excluded.

For the upper causal bound, the representative state is an actually reachable state. Applying the next admitted likelihood keeps it reachable. Positive evidence controls the quotient update on segments of reachable moment vectors. Therefore the one-step estimate has the form `e_(n+1)<=L_n e_n+r_(n+1)`, with constants independent of collision gaps or contrast in the relevant model. Finite iteration is sufficient at the fixed horizon. It would not, without additional estimates, produce a horizon-uniform theorem. The manuscript makes only the former assertion.

## H. A retained normalization and uncertainty check

Let `nu=ell mu/(mu ell)` be the reference posterior and let a bounded f satisfy `nu f=0`. In general `mu f` is not zero. Define

$$
d\mu' =\frac{1+t f}{1+t\mu f}\,d\mu.
$$

This prior has mass one. Updating by the same likelihood gives exactly

$$
d\nu'=(1+t f)\,d\nu.
$$

The denominator in the prior cannot be omitted. The formula in `prop:ambiguity-ellipsoid` includes it. The independent finite two-atom calculation checks this algebra in a case with `mu f` nonzero; it is not offered as an instance of the full-support interval theorem.

For the common-name lower bound, the manuscript instead uses a fixed pair `mu_+=(1+epsilon f)mu`, `mu_-=(1-epsilon f)mu` with `mu f=0`. The two posterior query means satisfy

$$
\nu_+q-\nu_-q=
\frac{2\epsilon\operatorname{Cov}_\nu(q,f)}
 {1-\epsilon^2(\nu f)^2}.
$$

The history distributions need not be identical; each dominates `(1-epsilon)` times the reference history law. A common prediction kernel and the squared-loss midpoint identity give the stated two-point lower bound after integration. The interior margin in the consistency class keeps both priors admissible under one moment name. This is not a claim about an arbitrary boundary name, which might identify a singleton.

These are favorable checks of the displayed algebra and quantifiers. The compiler and the complete common-program synthesis theorem are not newly certified by this note.

## I. Execution record and interpretation

Run from this directory:

```sh
python verify_review.py --output EXECUTION_REPORT.json
```

The recorded Python 3.13.5 run passed. Exact group counts were: envelope 16,500; zero-rank 2,220; Leja 126; paired products 100; scope examples 218; tilt normalization 2. The floating Laurent group contained 520 checks. The total was 19,686. The script SHA-256 is

```text
76aa34b11e13d43b193b356af031e11e7c117bd85c3e9471333069c2738ac8b5
```

The exact calculations use `Fraction` and integer powers. They avoid comparing irrational roots with floating tolerances. The Laurent regression uses complex floating arithmetic and is reported separately. Its recorded scaled residual is `1.1102230246251565e-16`, below `3e-12`. Since many tests are related instances of the same identity, the count must not be interpreted as thousands of independently established results.

No author code is imported, no network is used by the program, and no earlier referee's results are imported into this count. Neither finite diagnostics nor preserved Git objects prove a compact-family theorem. The analytic arguments in A--H and the cited manuscript proofs carry that burden.

**Overall audit conclusion:** the new inverse results withstand the checks made here. The boundary examples explain necessary premises already present in the manuscript. The publication-negative finding in the accompanying report is an editorial significance judgment, not a mathematical counterexample supplied by this audit.
