# Response to the two independent A2 v7 referee reports

**Revision:** A2 v8, September 9, 2026.  
**Article:** *Relative boundary laws and inverse experiments in dispersing billiards*.  
**Canonical branch:** `revision/a2-v8-relative-boundary-fixed-offset-2026-09-09`.

We respond jointly to the latest sharp-physical report, commit `861a1465ad332652e83dd118c9061d79062a5511`, and the critical-boundary report, commit `3af77abc50561c99c42c2a10ee2a8221dfad06da`. Their author sources are respectively `e3f5cba851f6216e879d1effa13fa171d92861b7` and `fc2f0599f5b6d905859722891265232dc7ef3c5b`. The later timestamp of the sharp source concerns documentation; the critical source has the complementary later mathematical extensions. The new manuscript takes the latter as its preserved source spine and incorporates the stronger sharp-v7 conclusions.

Both reports distinguish their significance and organization objections from a newly demonstrated fatal proof defect. We have not treated the previously repaired v6 issues as still-open objections. Nor have we removed their mathematical scope to obtain a simpler claim. All 130 formal statement/proof environments in the critical v7 active manuscript remain byte-identical and active; the substantive changes add results, reorganize their exposition, and resolve the requested experiment comparison.

## S-R1 and C-R1: the fixed-offset exact-model benchmark

**Response: incorporated as a full theorem, then extended to a joint-loss comparison.**

Section 13 gives the referee's four-window construction with all required analytic and statistical steps. Lemma 13.1 proves analyticity of the exact normalized finite-offset probabilities on a common complex neighborhood by analytic stationary action, the constructive Morse change of coordinates, fixed-disk integration, and cancellation of odd powers. The full lattice rotation/reflection group makes these probabilities symmetric in all three radius increments. Local root branches followed by bounded removable extension across the discriminant give analytic functions in the symmetric coefficients even at a triple root. We do not infer this coefficient differentiability merely from smoothness in labelled roots.

Theorem 13.2 uses the four physical windows `(1,g_c+a)`, `(1,g_c+2a)`, `(2,2g_c+a)`, `(3,3g_c+a)`, with a single fixed positive `a` independent of requested accuracy. The gap is unknown. After a row difference and scaling the gap column, the exact Jacobian converges to a block matrix whose determinant is `C_1 det D`, where the nonzero physical three-amplitude determinant is derived in full in Section 12. The inverse is obtained in a full coefficient neighborhood before restricting to real-rooted physical parameters.

Corollary 13.3 estimates the four means with deterministic-budget independent Bernoulli preparations. A compact Borel minimum-discrepancy fit controls gap, area, and symmetric coefficients linearly and the unordered curvature triple with exponent one third. This proves the requested curvature-only `epsilon^-6 log(1/eta)` upper bound without knowing the gap, area, channel labels, or positions. The construction is attributed to the referee comparison in the article and in the source pins. It is not presented as an independently originated author construction.

**The finer gap target is now compared by a new physical lower bound.** Section 14 defines an all-history bounded-flight Bernoulli class on a fixed collar and permits adaptive selection and stopping. Lemma 14.1 compares two circular physical tables with gaps `g_c` and `g_c+Delta`. The entropy is taken in the higher-gap to lower-gap direction, so the moving onset support causes no false absolute continuity assertion. The elementary physical estimates `|p_Delta-p_0| <= C d Delta` and `p_0 >= c d^2` give a per-query divergence at most `C Delta^2`, uniformly down to onset. The stopped chain rule gives the same bound times expected preparation count.

Combining this timing pair with the preserved physical curvature-splitting pair yields Theorem 14.2:

`N_K(epsilon,delta,eta) asymp (epsilon^-6 + delta^-2) log(1/eta)`.

The upper bound is the exact four-window fit; the lower bound allows random stopping and adaptive queries. In particular, the older simultaneous target `delta = epsilon^(3+3/m)` has optimal preparation power `6+6/m` in this wider fixed-collar class. Curvature loss alone has power six. This is a positive mathematical resolution of the distinction raised by the referee, rather than a repetition of the narrower shrinking-design lower bound.

Corollary 14.3 also imports the sharp branch's confidence logarithm for all-history shrinking designs, with a complete binary testing argument. The supplied-bracket upper and lower orders then agree at each fixed extrapolation order. This does not turn unrestricted collision observations into Bernoulli data, and does not take an uncontrolled limit in the extrapolation order.

**The unknown-remainder alternative is explicit, not rhetorical.** Section 15 defines an observation envelope with positive unknown `C^m` functions `H_j`, known common derivative bounds, and only `H_j(0)=C_j(g,e)` supplied by the physical leading model. Theorem 15.1 proves count-only recovery uniformly over this envelope. It acquires the initial bracket from a fixed interval, estimates the square-root onset zero using fixed-budget pilot samples, performs extrapolation with the timing normalization error included, and fits the leading data measurably. The preparation bound holds on every history, including a failed search, without a waiting-time assumption. The gap, coefficient/area, and curvature errors are respectively `h^(m+1)`, `h^m`, and `h^(m/3)`. No exact higher-order probability formula is supplied. We explicitly do not assert that every arbitrary nuisance triple is geometrically realizable, or claim a curvature-only minimax theorem for this larger envelope.

## S-R2 and C-R2: identify the independent nonlinear contribution

**Response: the relative boundary theorem now organizes the article.**

The opening pages formulate a relative approximation problem whose flux scale decays exponentially although the endpoint Hessian remains positive. Theorem 1.1 states the common-box, common-collar, differentiated nonlinear result before the statistical applications. The full proof is still supplied: finite bridge localization and cofactors, trace-norm control of tridiagonal perturbations, two separated determinant blocks and their half-line limits, differentiation with one trace-class factor, and physical residual-time integration on a common Morse domain. No absolute action error is divided by an exponentially small twist.

Section 7 remains in the main body as a concrete nonlinearity test. Its quartic variation and exact-area realization show information beyond the leading selected-channel hierarchy; the text expressly retains that selected-channel scope. All finite-jet realizations, the identical-even triangular inverse, the one-flight comparison, and coefficient sensitivity proofs remain in full in the appendices. Neither the general smooth theorem nor its derivative quantifiers are reduced to that special inverse family.

The introduction and Section 16 compare the target estimate with Hill identities, localized wave-trace geometry, marked-length reconstruction, and Prony conditioning. The paper does not claim that exponential endpoint localization or the disk-ellipse overlap is a new general principle. Nor does it use a contact-germ theorem to claim global table rigidity. Primary author/publisher records were checked for the cited comparison papers; the manuscript does not claim an exhaustive priority search.

The asymptotically tangent testing result is now explicitly separated from the genuinely nonlinear fixed-offset result. At fixed positive offset the latter remains Theorems 1.1/6.3 and the experiment-transfer theorem. The sharp support profile is an additional physical joint limit, not evidence that the fixed-offset nonlinear rate is optimal. Whether this strengthened result and its presentation merit the requested journal remains an independent editorial judgment; the response does not self-certify that judgment.

## S-R3 and C-R3: replace revision accumulation with one article

**Response: one introduction and a proof-oriented structure.**

The active source no longer inputs the consecutive v6/v7 introductions. Its single introduction specifies the geometry, the principal relative theorem, the two observation problems, and the route to their proofs. The main order is geometric construction, physical integration, nonlinear boundary separation, nonlinear information, endpoint experiments, physical count invariants, exact fixed-window inversion, joint-loss acquisition, smooth-remainder reconstruction, and literature comparison.

Complete secondary proofs are organized in appendices rather than removed. The marked-source statement is relocated without changing its mathematical content. The circular specialization, its original action construction, finite collision records, conditional-position inverse, supplied-bracket pilot, fixed-bracket cap construction, and previous coalescence statements all remain active. The original active main file is retained as `history/main-v7.tex`, and unchanged version directories are reused by Git object identity. Version chronology, source pins, diagnostic records, and this letter remain outside the article's mathematical narrative.

The clean article is 79 pages, and the unchanged companion is 7 pages. Length is not offered as evidence of significance; the retention check is evidence that the reorganization did not silently discard proofs.

## S-R4 and C-R4: reconcile the sibling versions and supply exact build evidence

**Response: one canonical successor, with complementary conclusions preserved.**

The critical branch's unequal-contact/common-whitening calculation, both parities, heterogeneous product overlaps, reverse erasure kernels, common-space tangent estimates, and fixed-initial-bracket acquisition remain active without alteration. Theorem 9.4 adds the sharp branch's stronger projection argument and makes it uniform over varying geometries in a fixed compact family. The single-observation condition is `omega(d_j)/q_j -> 0`, with `omega(d)=sqrt(d)` generally and `omega(d)=d` for even graphs. It covers zero, finite, and infinite effective sample limits, and characterizes when total variation vanishes. In the supercritical case it projects to a fixed critical subsample rather than requiring the entire sample's approximation error to vanish.

The sharp branch's explicit high-confidence stopped-design result is integrated in Section 14; the critical branch's expected-risk and weighted-exposure results are preserved in Appendix I. The complete original sharp chapters are pinned and retained separately. We have combined mathematical statements, not pretended that the two original builds or CI records were the same.

A new auxiliary-free local build compiles the exact revised article and its companion, with all references resolved and no overfull boxes. The actual log records one underfull vertical-box notice in the article and ordinary font-expansion notices; these are disclosed rather than relabelled as zero diagnostics. All pages were rasterized and visually checked in page-contact sheets, with detailed inspection of the new theorem pages. The source, build, and diagnostic manifests separate source identity, exact algebra, ordinary floating-point tests, and written proof.

The new finite diagnostic suite passes 249 checks: 86 exact-algebra checks, 31 ordinary floating-point checks, and 132 source-integrity checks. The inherited critical-v7 suite passes its 134 checks. Normal and `python -O` runs agree within each suite. These are not interval enclosures, an exact nonlinear probability solver, or formal proof certification. Remote CI success is not claimed.

## Suggested focus of the next independent review

The new analytic and statistical statements should be scrutinized in their own right: analytic descent across the discriminant in Lemma 13.1; the exact unknown-gap Jacobian in Theorem 13.2; the entropy direction at the moving onset in Lemma 14.1; the all-history design and joint-loss quantifiers in Theorem 14.2; and the unknown-remainder information model and failure-history cost in Theorem 15.1. The nonlinear significance case is the common-collar relative determinant and differentiated physical integral, with its retained constructive proofs, rather than the elementary tangent overlap alone.
