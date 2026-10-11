# Concordance for the 25 detailed comments

References below use stable native theorem labels; U denotes the complete unchanged R11 article. These clarifications are part of the referee packet, not retroactive edits to a frozen predecessor.

| Comment | Response / location |
|---|---|
| 1. Constants in checkpoint/autonomous inequalities | `thm:main` takes c smaller and C larger if necessary so that the same pair works in both inequalities; all dependence is listed there. |
| 2. Grid floors and small allocations | `lem:curvature` uses floor(L^(1/d)) >= L^(1/d)/2 for every L>=1 and includes L=1. No uncharged per-phase minimum L_0 is hidden. |
| 3. Centers and collar | The new proof replaces the compact-collar restriction by a global convex supporting-plane extension. Cell centers and enlarged balls can lie outside K without evaluating an illegal predictive state during execution. |
| 4. Submean and local curvature | `lem:curvature` displays normalized spherical averaging, radial monotonicity, w(R omega)<=R partial_r w and the divergence theorem, yielding h^(2-d) exactly. |
| 5. Cutoff integration by parts | The proof writes integral chi d(Delta f) = -integral grad chi dot grad f. Compact support removes the boundary term; global convex mollification supplies the nonsmooth limit. |
| 6. Bellman continuity | `lem:allocation` proves Lipschitz continuity directly by W1 and finite common actions. Raw Bayes normalization is continuous for each report with positive density. For U, its bound by a constant times sum_j f_j is integrable, so dominated convergence proves the older continuity statement as well. |
| 7. All incoming labels | `lem:telescope` explicitly integrates every incoming label and report assigned to a cell, and constructs each next mixture forward before using it. |
| 8. Full telescope | `eq:telescope` and its proof display R-B_n*=sum_t[E V_t(Q_t)-E V_t(W_t)], with E V_t(W_t)=E V_(t-1)(Q_(t-1)). Thus all intermediate E V_t(Q_t) cancel. |
| 9. Last-action density mixture | `lem:lower` conditions immediately before the final action/report, then mixes the uniform conditional bounds, allowing randomized policies. |
| 10. Optimal policy attainment | Continuation values are Lipschitz and a finite minimum admits the Borel least-index minimizing action. Iterating gives an attained full-history Bellman policy. |
| 11. Two affine-sensor likelihoods | In U's scalar plus sensor, f_0(y)=1/2 and f_1(y)=(1+lambda y)/2; in minus, f_0(y)=(1+lambda y)/2 and f_1(y)=1/2, on [-1,1]. This makes the parenthesized shorthand unambiguous. |
| 12. Affine-sensor Jacobian | U's determinant is lambda^d product_(j=0)^d q_j / D^(d+1)>0 throughout the cube. The explicit inverse is one-to-one; cube boundaries are null, so there is no multiplicity factor. The Gaussian and quantum native proofs separately state their corresponding invertibility/null-boundary conditions. |
| 13. Minimality and permutations | Choose the legal action whose known T^a is invertible. Undo its known report-coordinate and hidden-label permutations, recover q_j=3 E[y_j]/lambda for j>=1 and q_0 by normalization, then p=q(T^a)^(-1). Equal p fixes all future laws. This is the precise action used for U's separation argument. |
| 14. Strict feedback constant | The adjacent derivation below expands U's conservative bound. No numerical test replaces it, and no unproved Gaussian strict-feedback statement is added. |
| 15. Terminal stratum quantifier | `thm:strata` says immediately before the final action and report, uniformly over every incoming state/action; the proof then mixes over histories. |
| 16. Actual validation mass | `cor:validation` explicitly substitutes w=1-vartheta and rho_*=(1-vartheta)rho to get (1-vartheta)rho^(-2/r). |
| 17. Coordinate versus output errors | `prop:digital` uses b_t for coordinate sup error and u for task-output error, with an explicit loss modulus omega(u). |
| 18. Boundary slabs | The proof counts C/h_t hyperplanes in the fixed cube and their total slab volume C b_t/h_t. It uses the unconditional ideal acquired law. |
| 19. Conditional-mean readout | The digital discussion states that for Brier loss the label's actual conditional barycenter makes the extra readout risk exactly its squared norm error. General losses use omega(u), not an asserted quadratic identity. |
| 20. Independence in joint lower | `cor:joint` uses one product preparation and conditions on independent early-bit/offset variables when invoking the policy-uniform engine lower. No separate least-favorable laws are added illegitimately. |
| 21. TV convention | `prop:morphism` repeats TV=sup_B |P(B)-Q(B)|; loss in [0,H] gives H epsilon. The same convention is used in the exact erasure converse. |
| 22. Quotient factor range | `prop:quotient` types the unique map on the attained image of the sufficient statistic with its trace sigma field when Borelness of that image is not known. |
| 23. Modern comparisons | Formal references and `LITERATURE_COMPARISON.md` include the three specified papers with pinned versions and inspected theorem locations. |
| 24. Known kernels and finite actions | The first section, raw-kernel theorems and conclusion explicitly state this boundary; no unknown-kernel learning claim is made. |
| 25. Build limitations | README, native receipts, full-build receipts and history audit distinguish finite reproducibility from continuum proof and all-history certification. |

## Expanded affine-feedback inequality retained in U

In U's notation, I(q)=sum_(k>=0) lambda^(2k+2) q^(2k)/(2k+3). The k=1 term alone gives

```
|I(q)-I(1-q)| >= lambda^4 |2q-1|/5.
|b_-(q)-b_+(q)| >= 2 alpha^2(1-alpha)^2 lambda^4 |2q-1|/5.
```

On either half-interval with |y| in [1/2,1],

```
|2q(y)-1| >= (1-2alpha)lambda / [2(2+lambda)],
r_0(y) >= (1-lambda/2)/2,
```

and that half-interval has length 1/2. Integrating gives at least

```
alpha^2(1-alpha)^2(1-2alpha)lambda^5(1-lambda/2) / [20(2+lambda)]
```

for each of the two competing fixed second-sensor disadvantages. Their minimum is still bounded below by this positive number. Complementing the hidden state compares sequences starting with the other first sensor. This is an explanatory expansion of the unchanged U result, not a new native theorem or a claim that the threshold persists at every horizon.
