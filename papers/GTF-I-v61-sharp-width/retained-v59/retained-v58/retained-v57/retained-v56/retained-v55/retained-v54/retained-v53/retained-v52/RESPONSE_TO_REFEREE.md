# Response to report r33 — General Theta Foundations I, Revision 52

**Controlling review:** `review/general-theta-foundations-i-v51-compatible-lifts-harsh-top4-r33-2026-09-27`, commit `9d2f516b4113016f57fc8193c24ba192f8f782d5`.  
**Reviewed publication:** v51, commit `6363748923a5623801a53cfdb507a776aad414c3`.  
**New revision:** v52, `papers/GTF-I-v52-quantitative-lifts`.  
**Policy:** retain the established statements and proofs, answer mathematical objections by additional arguments, and distinguish a theorem from an executed computation or an editorial judgment.

The referee correctly identified the conceptual center of v51 and the limitations of its quantitative and noisy consequences. The new revision addresses those limitations rather than treating correct compilation or the prior report's favorable correctness assessment as sufficient. The central theorem now treats fixed positive error at arbitrary width. A rational-height rate and an explicit one-surplus multiplier replace two formerly qualitative consequences. The complete earlier mathematics remains available in the same manuscript; the main argument is reorganized rather than pruned.

All labels below are stable source labels, with final theorem numbers and page numbers supplied by `evidence/THEOREM_LOCATIONS.json`. A successful build is evidence of source consistency and reproducibility, not an independent mathematical referee decision.

## 1. The main new theorem: positive-error rigidity at arbitrary width

**Report §§5.2, 9.4.** The earlier robust theorem required rank-tight cuts, whereas the arbitrary-width theorem was exact. The referee asked for an appropriate approximate object and a theorem beyond minimum rank.

**Response.** Theorem `thm:noisy-finitegroup52` proves the following unrestricted-width statement under the original numerical interface:

> For a finite orthogonal alphabet containing the identity, signed coordinate seeds, and all coordinate queries, fix `0 <= epsilon < rho/(2D)`. Uniform boundedness over the horizon of nonuniform clocked stochastic width is equivalent to finiteness of the generated group, and hence to existence of one finite exact stationary permutation realization.

The wordwise error is total variation, so its coordinate-mean version is `delta = 2 epsilon`. No uniform reachable-rank, minimum-state-probability, or basis-conditioning assumption occurs in this theorem.

There is a genuine obstruction to applying the old word-distortion theorem directly: an infinite group can fix an axis, on which the full-space distortion is zero. Lemma `lem:finite-orbit52` removes the entire finite-orbit subspace `F`, not just common fixed vectors. Its orthogonal complement `E` is invariant and every nonzero vector of `E` has infinite orbit. Haar full support and compactness yield a positive distortion minimum there. Lemma `lem:haar-word52` realizes a positive fraction of that minimum by a finite distribution on actual positive command words, padded with identities to equal length.

Theorem `thm:noisy-budget52` then applies the inherited packet-centroid contraction to actual endpoint kernels, with no projection of hidden basis states. Its final calibration is

`q_N >= rho s_*/sqrt(D) - 2 epsilon`,

where `s_* = max_i ||P_E e_i|| >= 1/sqrt(D)`. A fixed finite width imposes a positive contraction on each selected word block, contradicting this calibration at long horizons. This also gives an occupation bound with arbitrary wider registers between selected endpoints. The proof repeats the complete conditional-expectation calculation in the main text.

The sufficient error interval is not claimed sharp. At `epsilon >= rho/2`, one label with a fair binary answer always suffices. The intermediate tolerance regime is not classified. This is a precise scope boundary, not a weakening of the original exact theorem.

## 2. An effective rate from intrinsic arithmetic data

**Report §§5.1, 9.3.** The multiplier `gamma_A(V,rho)>1` did not quantify width growth for an infinite group. A useful rate should depend on properties of the action rather than an unevaluated compactness minimum.

**Response.** Theorem `thm:height52` gives such a rate for every planar rational rotation of infinite order. Suppose its eigenvalue is `(a+ib)/c`, where `a^2+b^2=c^2`, with `c >= 2`. The alphabet may contain arbitrary additional orthogonal commands, including noncommuting reflections. No Diophantine exponent or spectral mixing assumption is used. With `kappa = rho/sqrt(2) - 2 epsilon > 0`, any feasible peak `K` satisfies

`N < 2K [1 + 16 c^(4K) log(1/kappa)]`.

Hence `W_(N,epsilon) >= [log N - O(log log N)]/(4 log c)`. The proof uses the `2K` actual products `I,R,...,R^(2K-1)`. A nonzero Gaussian integer gives their separation at least `c^(-2K)`; the inherited spherical-cap argument then gives finite-word distortion at least `c^(-4K)/16`. The endpoint proof turns this directly into a hidden-label lower bound. It does not pay an exponential loss through the projected vertex count `V_K`.

This answers the quantitative request by a directly calibrated word multiplier and a width-growth law. It is not described as a sharp closed formula for the one-step polytope multiplier `gamma_A(V,rho)`. The general exact variational theorem remains intact, and the stronger specialized arithmetic results in the appendices are not discarded.

## 3. Explicit one-surplus expansion and a numerical six-state horizon

**Report §§5.3, 9.5.** The old `beta_3(rho)>1` was obtained by compactness and supplied no numerical horizon.

**Response.** Lemma `lem:trace52` proves a quantitative asymmetry bound. If a full-dimensional polytope containing the origin has at most `k` vertices or facets, with `D+1 <= k < 2D`, then

`s_0(P) >= D/(k-D)`.

For the vertex case, an inclusion `-P subset lambda P` supplies a stochastic matrix with eigenvalue `1` and at least `D` eigenvalues `-1/lambda`. Nonnegative trace and the unit spectral disk imply the inequality. Polarity proves the facet case. Lemma `lem:cap-volume52` converts the resulting support displacement into a disjoint cone of added volume.

Theorem `thm:beta52` obtains an explicit formula in every dimension `D >= 3` and, in particular,

`beta_3(rho) >= 1 + rho^3/1024`.

For the dimension-three signed-permutation experiment with `I,-I`, this gives

`(1 + rho^3/1024)^N > 6 rho^(-3)  =>  W_(N,0)=6`.

At `rho=1/10`, the sufficient integer horizon `N=9,216,009` is verified by exact rational arithmetic using `log(1+x) >= x/(1+x)` and a degree-20 Taylor lower bound for `exp(9)`. We do not label this sufficient horizon optimal or compute an enormous integer power as a substitute for proof.

## 4. Approximate physical sections and two distinct noisy six-state results

**Report §§9.4–9.5.** Beyond the unconditional theorem in §1 above, Theorem `thm:conditioned52` formulates the approximate positive-section object explicitly. For a supplied independent reachable basis `E_t`, define

`A_t = max { ||alpha||_1 : alpha E_t in rowspan(E_t) intersect Delta }`.

This quantity is finite at a fixed cut, but a horizon-uniform bound is not automatic. If selected cuts satisfy `A_t <= A`, then the actual section images obey

`U_w S_s subset S_t + h[-1,1]^D subset Lambda S_t`,

where `h=A(1+sqrt(D)) delta`, `b=rho-D delta`, and `Lambda=1+Dh/b`. The proof controls the complete suffix once, rather than accumulating one-step error. It yields an arbitrary-width occupation inequality with `gamma_A(V_K,b)/Lambda^D` and a one-surplus version with `beta_D(b)/Lambda^D`.

Corollary `cor:conditioned-six52` consequently gives an **explicit** positive-error interval `epsilon <= rho^4/(2^23 A)` and a sufficient horizon inequality for six-state optimality in the stated conditioned class.

Theorem `thm:computable-six52` gives an **unconditional** six-state interval for algebraic input. At the now explicit exact-separation horizon, compactness makes the optimum five-state error strictly positive. A finite common-row prefix formula is decidable by real-algebraic elimination; successively testing dyadic tolerances therefore terminates with a positive interval. Identity truncation propagates it to all longer horizons.

These two conclusions are deliberately distinguished. The terminating algebraic search has **not been executed** at the illustrative horizon of 9,216,009. No numerical unconditional six-state tolerance is reported, and no conditioning assumption is silently imported into the unrestricted theorem.

## 5. The complete local system and a global certificate hierarchy

**Report §§5.4, 9.6–9.7.** We have corrected Proposition `prop:dual51` to enumerate all three blocks of `B vec(T)=b`: row sums, projector-range invariance, and observable intertwining. For a `k`-by-`ell` transition,

`B` has `(k + k ell + kD)` rows and `k ell` columns,

with redundancy allowed. The witness has the same number of coordinates as the rows and may be normalized by `b^T y=-1`. The exact regression suite contains a swap matrix accepted after dropping invariance and rejected by the complete system.

Proposition `prop:counts52` gives separate scalar-variable, equality, and inequality counts, specifies the coefficient representation, and distinguishes polynomial description size from elimination time. Projector rank is not constrained to the minimal reachable rank. Algebraic inputs and outputs are represented by defining polynomials with isolating intervals.

Theorem `thm:sos52` supplies a global alternative over the previously unknown geometric variables. Let `h` be the complete equality list and `q=sum h_i^2` on the compact variable box. A redundant ball inequality makes the quadratic module Archimedean. The Putinar–Lasserre hierarchy for `min q` converges to zero precisely in the feasible case; in the infeasible case some finite-degree identity has a strictly positive lower bound. Exact verification uses coefficient identities and positive-semidefinite Gram matrices, not a floating-point solver's success flag.

The positivity theorem and convergence mechanism are explicitly credited as classical. This is a global certificate construction for the specified realization system, not a claim of a new Positivstellensatz or a practical polynomial-time optimizer. `certificate_verifier.py` implements verification of supplied rational identities of bounded Gram order; `check_revision.py` tests its positive and negative cases. A general SOS search engine and a large unknown-section optimization instance are not presented as having been run.

## 6. Resources and horizon-uniform realization

**Report §§5.8, 9.9.** The resource table now appears in the introduction before memory interpretations. It separates label width, row description, sampling bits, working storage, and time/nonuniformity.

Theorem `thm:uniform52` supplies a positive companion theorem rather than simply repeating the limitations. With a finite group of rational orthogonal matrices and rational signal level, the signed-seed orbit gives one horizon-independent permutation transducer. Its deterministic transition tables, rational query probabilities, and exact Bernoulli sampler have explicit separate size and expected-random-bit bounds. Rejection sampling is exact and has an unbounded worst-case running time; this is stated. Orbit enumeration is guaranteed to terminate under the finite-group hypothesis, not offered as an unrestricted group-finiteness algorithm.

## 7. Organization, literature, and the analytic pipeline

**Report §§9.1–9.2, 9.8, 9.10.** The title, abstract, introduction, and main proof chain now center on quantitative and noisy finite-group rigidity. The complete inherited tensor, simplex, arithmetic, and finite-bit theory remains loaded in explicitly marked appendices. The accompanying core PDF is only a reading excerpt. This meets the request for a focused theorem chain without deleting the prior mathematical content. The preservation manifest verifies all 201 loaded v51 labels; final numbering and locations are generated from the compiled source.

The main text now includes the requested theorem-by-theorem comparison table: current statement, published antecedent, shared mechanism, additional hypotheses, and additional conclusion. It treats positive realization, nonnegative intertwining, static extended formulations, invariant polytopes, probabilistic and weighted automata, difference bodies, and global polynomial positivity. An independent exhaustive priority judgment is not manufactured from a targeted literature search. See `LITERATURE_AUDIT.md` for the primary sources actually checked and the limits of that comparison.

The inherited word-profile and packet-contraction line is used substantively in the new proof, with the finite-orbit reduction and arithmetic calibration supplied here. In contrast, the repository's analytic A/B/C/D gates require different model-specific theorems. We have checked the Round-Seventeen dependency ledger and retain its separation. This revision does not claim raw Fourier/local-limit estimates, stopped LDPs, nonlinear resolvents, filtering QMD, or downstream labelled contraction merely because finite stochastic realization has advanced. `PIPELINE_STATUS.json` records precisely this boundary.

## 8. Point-by-point disposition of the 35 local comments

| r33 item | Change and location |
|---|---|
| 1 | `thm:section51` proof gives the coefficient-sum reason for the affine hull of reachable rows. |
| 2 | `r_t=dim R_t` precedes the vertex bound; new summaries also state its meaning. |
| 3 | Permanently zero coordinates are expressly redundant restrictions, not a failure of the active-set argument. |
| 4 | The first independent active subset in lexicographic order is chosen, making the vertex-to-subset assignment definite and injective. |
| 5 | The proof writes the projected body as the convex hull of the images of section vertices. |
| 6 | `cor:surplus51` counts independent active `D`-subsets of at most `D+2` facets. |
| 7 | Reachability rank is consistently the ordinary dimension of the actual reachable linear span. |
| 8 | `thm:local51` expressly leaves projection rank unconstrained and allows protected unreachable directions. |
| 9 | `prop:counts52` lists scalar equalities and inequalities in addition to variables. |
| 10 | Defining polynomials and rational isolating intervals are specified next to effective algebraic assertions. |
| 11 | `prop:dual51` and `prop:counts52` explicitly include both range and observable equations in `B`. |
| 12 | The negative Farkas witness is normalized by `b^T y=-1`. |
| 13 | The definition of `gamma_A(V,rho)` expressly inherits `I in A`. |
| 14 | The multiplier is written with its action, vertex budget, and inner radius; the noisy geometric theorem uses `gamma_A(V_K,b)`. |
| 15 | The compactness proof explicitly uses Hausdorff continuity of finite unions followed by convex hull. |
| 16 | Equality of a full-dimensional containing body and its equal-volume subset is justified. |
| 17 | Exact clocked bound `K` and derived stationary bound `V_K` are kept distinct. The noisy theorem asserts existence, not that same stationary size bound from an approximate machine. |
| 18 | The factorial group-size estimate is labeled extremely coarse. |
| 19 | Truncation uses the decoder `T_(N+1,I)d_j` explicitly, also at positive error. |
| 20 | The rational rotation's trace is explicitly the eigenvalue sum, a rational algebraic integer under the torsion assumption. |
| 21 | The polarity argument notes `0 in int S`, since `C_rho subset S`. |
| 22 | Continuity of the symmetrized hull and its volume is stated before minimizing. |
| 23 | The old sufficient variational horizon is retained and now strengthened by `thm:beta52`. |
| 24 | The averaged anchor has error at most `delta` because it is a convex average of two error vectors. |
| 25 | The induced infinity norm is defined before inverse estimates. |
| 26 | Entrywise maximum and maximum absolute row sum are distinguished. |
| 27 | The approximate-containment arguments identify the whole selected suffix followed by identity padding. |
| 28 | Mean tolerance is explicitly `delta=2 epsilon` wherever TV tolerance enters the new corollaries. |
| 29 | The error interval is independent of the horizon; the sufficient horizon condition remains a separate requirement. |
| 30 | The retained exact four-label machine is an all-horizon upper bound; it is not used as evidence for a new lower bound. |
| 31 | The resource table is moved to the introduction. |
| 32 | The section is called a finite projector characterization; degree three describes its equations, not analytic locality. |
| 33 | Description length, coefficient encoding, and elimination complexity are explicitly separated. |
| 34 | A focused main argument and core excerpt are supplied; all inherited mathematical modules remain in the complete article and prior versions remain untouched. |
| 35 | The conclusion identifies the remaining sharp-rate, larger-noise, computational, and partial-interface questions without presenting them as solved. |

## 9. Evidence and remaining review questions

The v52 exact suite checks the rational one-surplus/horizon constants, the trace mechanism, 372 rational orbit-separation comparisons, finite-orbit projection in the fixed-axis example, the complete local linear system, supplied SOS identities, and 2016 exact rational-sampling cases. Eighteen named negative controls execute both normally and with Python optimization. The inherited v51, v50, v49, v47, and v44 checks are rerun rather than copied as historical passes. Build receipts and an isolated-source rebuild identify the tested source.

These finite tests do not prove the universal Haar/compactness arguments by sampling. The next referee should in particular examine the finite-orbit reduction, the complete-word endpoint conditioning identity, the support-displacement cone bound, and the separation of the unconditional and conditioned noise statements. The unrestricted sharp noise boundary, sharp general one-step `gamma` rates, practical global optimization, and exhaustive priority remain substantive questions. They are not asserted closed by this revision.
