# Technical note — the classical spectral content and phase structure of A1 v9

**Submission:** `e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5`  
**Principal source:** [`papers/A1-english-v9/sections/06b_collision_geometry.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/06b_collision_geometry.tex)  
**Status:** Independent referee analysis, not an author revision and not a claim of new priority.

The purpose of this note is to sharpen the comparison in the accompanying [referee report](REFEREE_REPORT.md). It identifies exactly what the intrinsic determinant formula adds to a classical finite evaluation matrix, verifies a nonaffine stress case, and derives an additional elementary consequence of the collision-tree recurrence. None of the propositions below refutes the submitted main theorem. None substitutes for its attainable-posterior or causal arguments.

## 1. Maximal Vandermonde products are exterior spectral scales

Fix q and a multiset x=(x_1,...,x_q) in [0,1]. Repeated labels are retained. Define

\[
 W(x)=(x_i^{j-1})_{1\le i,j\le q},\qquad
 \mathcal V_l(x)=\max_{|J|=l}\prod_{\{i,j\}\subset J}|x_i-x_j|,
 \qquad \mathcal V_1=1.
\]

Let sigma_1≥...≥sigma_q≥0 be the singular values of W. Constants with subscript q below are permitted to depend on q, but not on node separation.

### Proposition 1

Uniformly over x, including repeated nodes,

\[
 \mathcal V_l(x)\asymp_q\prod_{j=1}^l\sigma_j(W(x)),
 \qquad 1\le l\le q.
\]

Both sides vanish when l exceeds the number of distinct sites. The assertion is a comparison up to constants, not an equality of maximal minors and singular-value products.

### Proof

Order the nodes by the finite Leja procedure used in `lem:leja-scales`. Row permutation does not change singular values. Put

\[
 d_1=1,\qquad d_j=\prod_{i<j}|x_j-x_i|,\qquad
 P_{j-1}(z)=\prod_{i<j}(z-x_i).
\]

If s is the number of distinct sites, d_1≥...≥d_s>0 and d_j=0 for j>s. Write T for the coefficient matrix whose jth column is the monic polynomial P_(j−1) in the ordered power basis. It is upper triangular with diagonal one. Its entries are elementary symmetric polynomials in at most q−1 numbers in [0,1], so its norm is bounded in terms of q alone. Writing T=I+U with U strictly upper triangular gives

\[
 T^{-1}=\sum_{k=0}^{q-1}(-U)^k,
\]

hence the same kind of uniform bound for its inverse.

Evaluation gives W T=N, where N_(ij)=P_(j−1)(x_i). The Leja argument factors N=L D, with D=diag(d_j), bounded entries |L_(ij)|≤1 in active columns, and an active lower-triangular leading block with diagonal entries ±1. Every column j>s of N vanishes: its polynomial already has every distinct site as a root.

Extend L to an invertible matrix L_tilde by retaining the first s columns and replacing each remaining column j by the coordinate vector e_j. This is block lower triangular. The active diagonal block and its inverse are bounded in terms of q by the finite triangular recursion; the inactive diagonal block is the identity and the remaining block has bounded entries. Therefore both L_tilde and its inverse have q-dependent bounds. Because the corresponding diagonal entries of D vanish,

\[
 W=\widetilde L\,D\,T^{-1}
\]

still holds exactly. The singular-value inequalities for multiplication by invertible matrices yield

\[
 c_q d_j\le\sigma_j(W)\le C_q d_j
\]

for every j, including the zero tail.

Finally the manuscript's finite determinant argument gives

\[
 \prod_{j=1}^l d_j\le\mathcal V_l(x)
 \le l!\prod_{j=1}^l d_j.
\]

Combining these inequalities proves the proposition. No reciprocal exponent separation has occurred. ∎

### Consequence for the submitted rate

For each future label set, let W_m(a) be its square ordinary Vandermonde matrix. The submitted checkpoint profile can equivalently be written

\[
 \Psi_{n,m}(M,a)\asymp
 \max_{1\le l\le p_{n,m}}
 \left(\frac{\|\wedge^l W_m(a)\|}{M}\right)^{2/l},
\]

where the norm of the exterior operator is the product of the largest l singular values. The constants may depend on the fixed horizon through q_m. This is an interpretation of the intrinsic scales, not a stronger horizon-uniform estimate.

The proposition is **not** an application of a theorem about clustered Fourier matrices with identical hypotheses. W_m is an ordinary finite real evaluation matrix. The proof above is supplied in full precisely to avoid claiming that a nearby spectral paper already proves the Bayesian theorem. Batenkov–Diederichs–Goldman–Yomdin provide relevant clustered spectral context, but do not provide the attained history distribution or the streaming lower bound.

What remains to turn this finite-matrix profile into memory is substantial and model-specific: the initial resolved coordinates must be excited by actual histories; their exploration law must minorize volume with its acquisition evidence; the entire reachable image needs a dimension-truncated cover; and the transitions must preserve the rate under repeated compression. Proposition 1 proves none of those statements. The main report evaluates their proofs separately.

## 2. Why every initial Newton flag is a complete Hermite space

Let y_1,...,y_p be any ordered multiset of positive nodes, not necessarily grouped by their repeated values. Define the functionals

\[
 \lambda_j f=[y_1,\ldots,y_j]f,\qquad 1\le j\le p.
\]

Let H be the p-dimensional space of Hermite data consisting of f^(k)(y) for each distinct node y and 0≤k<mult(y).

### Proposition 2

The functionals lambda_1,...,lambda_p form a basis of H. Consequently, applied to z↦t^(Hz), their span consists of all functions t^(Hy)(log t)^k in the corresponding complete multiplicity blocks, with harmless nonzero normalization factors.

### Proof

Every prefix divided difference depends only on the Hermite data at that prefix, hence belongs to H. On the polynomial space of degree at most p−1, lambda_j annihilates degrees below j−1 and takes value one on z^(j−1). The matrix of these functionals on 1,z,...,z^(p−1) is triangular with diagonal one. They are therefore independent, and because dim H=p they span H. Substitution of t^(Hz) converts exponent derivatives into H^k t^(Hy)(log t)^k. ∎

This is the classical Newton–Hermite prefix principle; compare de Boor, *Divided Differences*, [Proposition 7, printed p. 48](https://arxiv.org/pdf/math/0502036). It is valid for nonadjacent repetitions. The argument explains why the manuscript may use strict confluent positivity after selecting an arbitrary Newton prefix, whereas a selection of isolated logarithmic jets with missing lower orders would not justify the same inference.

At the binomial product tuple, the tangent has n(r−1)+1 distinct monomials. Adjoin the constant to p≤n(r−1) such tests. The manuscript's strict mixed/confluent pairing is onto a (p+1)-dimensional space; normalization removes its one constant direction. This establishes the stated rank p before compactness is invoked. Uniformity then uses continuity over the compact calibration set and finitely many permutations, not continuity of the selected Leja ordering itself.

For an exact diagnostic with the uniform prior, integration reduces to

\[
 \int_0^1 t^b[y_1,\ldots,y_j](z\mapsto t^z)\,dt
 =\frac{(-1)^{j-1}}{\prod_{i=1}^{j}(b+y_i+1)}.
\]

The identity is the divided difference of 1/(b+z+1), and remains valid at repeated nodes. Our program uses this formula, its density-3t² analogue, and a half-uniform/half-point-mass prior to check ranks exactly. These three full-support priors are diagnostics, not verification for all full-support measures.

## 3. An automatic additional consequence: convex collision energies

Retain the submitted collision-tree hypotheses after identifying sums identical along the path. Let beta_l be the minimum total pair order of an l-element subset, and set beta_0=beta_1=0.

### Proposition 3

The finite sequence beta_0,...,beta_q is discretely convex:

\[
 \beta_{l+1}-\beta_l\ge\beta_l-\beta_{l-1},\qquad 1\le l<q.
\]

One can choose optimal subsets nested as l increases. These conclusions follow from the submitted laminar-tree energy and do not require an additional regularity hypothesis on the path beyond that energy representation.

### Proof

At a leaf the finite cost sequence is (0,0). At an internal cluster C the submitted recurrence has the form

\[
 F_C(k)=\Delta_C\binom{k}{2}
       +\min_{\sum k_i=k}\sum_i F_{C_i}(k_i),
 \qquad \Delta_C\ge0.
\]

Inductively suppose each child sequence is discretely convex over its feasible integer range. Its successive marginal costs are nondecreasing. The minimum convolution in the display has as its marginal sequence the sorted union of the child marginal sequences: selecting the k cheapest marginals is feasible because selecting a child marginal can be arranged to include its cheaper predecessors, with prefix-respecting tie breaking. This also gives a nested sequence of minimizing child allocations as k increases.

Adding Delta_C binomial(k,2) adds Delta_C(k−1) to the kth marginal. The resulting marginal sequence remains nondecreasing. Moreover this added term depends only on total k and does not change the minimizing child allocation. Induction therefore gives both convexity and nested optimal subsets at every cluster, hence at the root. ∎

This is an elementary consequence of finite convex allocation. It may simplify computation and exposition, but it should not be counted as an independent deep theorem without further consequences.

### Adjacent phase boundaries

For M of order theta^(−b), a fixed checkpoint's terms have exponents

\[
 \frac{2(\beta_l+b)}{l},\qquad 1\le l\le p,
\]

and the largest regret term is the one with the smallest exponent. The adjacent l and l+1 terms coincide at

\[
 b_l=l\beta_{l+1}-(l+1)\beta_l.
\]

The discrete convexity just proved gives

\[
 b_l-b_{l-1}
 =l(\beta_{l+1}-2\beta_l+\beta_{l-1})\ge0.
\]

Thus these adjacent boundaries are ordered. Repeated boundaries correspond to zero-length intermediate regimes, explaining why some displayed determinant terms are only geometric interpolations of others. Past limitation simply stops this list at the attainable cap p. These are asymptotic power boundaries, not exact finite-budget thresholds or leading distortion constants.

## 4. The two-parameter stress case

In the submitted four-cell family with N=5, the checkpoint n=3,m=2 has positive formal exponents

\[
 1;\quad 2,2+u;\quad 3+u,3+v;\quad
 4+2u,4+v;\quad 5+u+v;\quad 6+2v.
\]

There are six separated limiting groups. The three potentially small gaps are |u|, |v−u|, |v−2u|. With their decreasing rearrangement g_1≥g_2≥g_3, the signed relation (v−u)=u+(v−2u) gives g_1≤2g_2. Also g_1 is comparable to rho=max{|u|,|v|}; g_3=tau. Consequently the products for l=6,7,8,9 have orders 1,rho,rho²,rho²tau. This recovers the manuscript's three-term rate.

Along u=theta, v=theta+theta^k, k≥2,

\[
 (\beta_1,\ldots,\beta_9)=(0,0,0,0,0,0,1,2,k+2).
\]

The adjacent boundaries b_6=b_7=6 explain why dimension seven has no open intermediate power regime. The final boundary is b_8=8k−2. Explicitly,

\[
 R_M\asymp
 \begin{cases}
 M^{-1/3},&1\le M\lesssim\theta^{-6},\\
 \theta^{1/2}M^{-1/4},&\theta^{-6}\lesssim M\lesssim\theta^{-(8k-2)},\\
 \theta^{2(k+2)/9}M^{-2/9},&M\gtrsim\theta^{-(8k-2)}.
 \end{cases}
\]

Boundary constants depend on the fixed experiment and path. At the power boundaries the regret orders are theta² and theta^(2k). Exactly on a nonzero collision line the last term disappears and the peak dimension is eight; at the origin both weak contributions disappear and the peak dimension is six. These deductions confirm the printed formula; they are not corrections to it.

## 5. What was executed

The standalone standard-library program `referee_checks.py` ran successfully with seed 190906 under Python 3.13.5. Its receipt contains 3,821 passed assertions and zero failures. In particular it checked 27 finite matrix configurations, including all-equal sites and a gap of 10^(−12); 135 arbitrary-prefix pairing/normalization configurations; eight tree/subset comparisons; a signed 25-point calibration grid; five contact orders k=2,3,4,7,11; and 18 index-only fixtures with 450 exact raw-update vector comparisons.

The raw-update reference independently integrates products of actual positive report factors. The small codebooks are reachable codebooks generated from a finite command menu, and the mutable machine has only an index field. The reference prefix polynomial lives outside the implemented machine and is used solely for the audit. These fixtures test the arithmetic and storage discipline, not the existence or asymptotic optimality of the continuum covers.

Reproduction from this review directory:

```sh
python3 referee_checks.py --output fresh-diagnostics.json
```

The timestamp and Python version may differ on a fresh run. The author programs, manuscript PDF build, and standalone author archive were not executed by this command. Successful execution does not establish the continuum entropy theorem, exhaustive priority, or a journal acceptance recommendation.
