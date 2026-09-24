# Response to the eighteenth pipeline-aware referee report

**General Theta Foundations I — Revision 34**  
**Fourier Budgets for Hidden Causal Memory**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v33-compatible-lifts-pipeline-harsh-top4-r18-2026-09-25/REFEREE_REPORT.md`, frozen at `ee524c3e210ede7d6ff927c2bd2a2a1a104cb28c`. Reviewed v33 publication: `aab96108125317342e51e6a946efc4d778429338`; native v33 source: `243e670a5be8628b9f4eaf60338348032357bcab`.

The report identifies a precise mathematical obstacle: the general hidden-state lower bound passes through an exponentially large projected polygon, whereas the cube-root theorem applies only to vector states. It explicitly asks for a superlogarithmic lower bound for arbitrary hidden lifts as one route to a material advance. This revision supplies such a bound, for the same fixed-alphabet, uniformly positive rotation experiment, and for arbitrary cut-dependent stochastic rows. It does not relabel the vector-state theorem as an unrestricted theorem. A separate deficiency argument turns the new bound into a quantitative obstruction for every proposed small stochastic diagram of that experiment.

The broad program title is retained. Its role is not evidence for significance, and no journal outcome is asserted. All prior mathematical results remain in their unchanged repository paths and archival volumes. The focused article contains the new proofs independently of those archives. Stable labels below are resolved to actual theorem numbers and pages in `evidence/THEOREM_LOCATIONS.json`.

## Sections 4, 8.1 and 12.4 — the unrestricted hidden-lift gap

**A polynomial all-hidden-state lower bound replaces the logarithmic lower bound.**

`thm:fourier34` proves a general spectral occupation inequality. Drive any finite, time-dependent stochastic transducer by independent fair external command bits, write `L_t` for their sum, and put

```
z_t(s) = E[zeta^(-L_t) | S_t=s],
q_t = sum_s Pr(S_t=s) |z_t(s)|.
```

These conditional past-phase moments are proof objects. No hidden basis state is assigned a statewise-intertwining future vector, and no extra posterior is supplied to the executing machine. Their number is bounded by the actual hidden register size, regardless of how many vertices a projected simplex section has.

The amplitude q_t decreases under stochastic compression. The total decrease is at most one. The angular function `f_l(re^(i theta))=r e^(i l theta)` has an averaging error bounded by `(l^2+1)` times this same amplitude loss. This is proved directly, including averages at zero. Under a fresh fair command, its moment contracts by `(1+zeta^(-l))/2` up to that error. A positive Fejer kernel detects every positive phase measure with at most k atoms. Combining the squared moment recursions and summing through time gives

```
#{0 <= t < N: K_t <= k} * beta_(2k)(alpha) <= 18*k^3/kappa^2,
beta_m(alpha) = min_(1 <= l <= m) sin^2(pi*l*alpha),
q_N >= kappa > 0.
```

There is no cap on the widths at other epochs. This is an occupation bound, not just a peak estimate. The process need not be stationary and may use a different machine for each horizon.

`prop:terminal34` uses only the two terminal coordinate laws at the single prescribed length N. For row-TV error epsilon below 1/20 it gives `q_N >= 1/10-2*epsilon`. Therefore, with `b_alpha=inf_l l ||l alpha|| > 0`,

```
W_(N,epsilon)(alpha) >= [b_alpha^2*(1/10-2*epsilon)^2*N/18]^(1/5).
```

At the golden angle and zero error the explicit result is

```
max(3,(N/16200)^(1/5)) <= W_N < 2*max(5,(40*N)^(1/3)).
```

The upper side is the inherited resonant exact construction, reproduced with its proof. Thus arbitrary hidden lifts cannot achieve logarithmic width for bounded-type angles. The remaining gap is between powers 1/5 and 1/3, not between logarithmic and cube-root growth. We do not claim that the new lower exponent is sharp or that the hidden and vector-state optima coincide.

## Sections 8.3 and 13.14–15 — rational rotation

**The unrestricted rational-angle lower bound improves from doubly logarithmic to logarithmic.**

For `zeta=(3+4i)/5`, the nonzero Gaussian integer `(3+4i)^l-5^l` gives `sin^2(pi*l*alpha) >= 25^(-l)/4`. The same hidden-state occupation theorem, without any bounded-type assumption, implies

```
N <= 7200*W_N^3*25^(2*W_N),
W_N >= max(3,log_(5000)(N/7200)).
```

The old exact rational counter still supplies at most `3*(N+1)` states. The arithmetic upper/lower orders are not declared matched. No unproved bounded-partial-quotient property of this rational matrix angle is used.

## Sections 5, 12.2 and 13.1–3 — Blackwell comparison and deficiency

**The direct statistical-experiment lineage is restored in the article.**

`prop:blackwell34` states the finite one-sided deficiency

```
delta(E,F) = min_(T stochastic) max_h TV((E*T)_h,F_h)
```

and proves its dual with total row-oscillation budget one. At zero defect this is the classical finite Blackwell garbling problem, not a new one-step theorem. Blackwell (1953), Torgersen (1991) and the modern Blackwell–Sherman–Stein treatment of Fritz–Gonda–Perrone–Rischel are cited. The proof fixes the direction of simulation and the factor of two in binary TV. The inherited 1/4 example is treated in the regression record as a small deficiency calculation, not as the main-family obstruction or a novelty claim.

## Sections 7, 12.5 and 12.7 — approximate compatibility in the main family

**A quantitative defect is proved for every proposed finite diagram of the rotation experiment.**

For a fixed diagram of proposed state distributions E_t indexed by all input prefixes, `thm:diagram34` minimizes a common stochastic post-processing at each command and at the terminal decoder. Let D(E) be the sum of the maximum command defects and the terminal defect. The chosen stochastic rows form an actual machine with that same register profile and uniform output error at most `min(1,D(E))`. The proof is a wordwise telescoping argument, not a history-dependent choice of rows.

If all widths are at most K, the Fourier converse yields

```
D(E) >= (1/2)*[1/10 - sqrt(18*K^3/(N*beta_(2K)(alpha)))]_+.
```

At bounded type this is at least

```
(1/2)*[1/10 - sqrt(18*K^5/(b_alpha^2*N))]_+.
```

For K=o(N^(1/5)) the total certified defect is therefore bounded away from zero. This applies to any candidate sequence of hidden distributions, not to one hand-selected section or one four-point example. In particular, an O(log N)-coordinate static polygon extension cannot provide a vanishing-defect stochastic diagram for the original task at that width, once initialization and a bounded decoder are included.

D(E) is an additive executable error certificate, not asserted to equal the minimum final output error for that diagram: intermediate errors may cancel. The fixed-diagram linear programs do not search globally over unknown sections. The lower bound ranges over all diagrams because the machine converse does, not because those programs solve the global search problem.

## Sections 6, 12.3 and 13.4–6 — symmetric and equivariant lifts

**The omitted primary comparisons are included with their exact quantifiers.**

The article discusses the symmetric slack-factorization theorem of Gouveia–Parrilo–Thomas, the symmetry-size phenomenon of Kaibel–Pashkovich–Theis, and the regular-polygon equivariant LP/PSD results of Fawzi–Saunderson–Parrilo. It distinguishes a group action on one extension from noninvertible stochastic maps between changing sections. The known linear equivariant LP lower bounds are not directly applied to an arbitrary time-dependent hidden machine.

`prop:cyclic34` gives an elementary spectral comparison for an exact cyclic stochastic lift with a common matrix, including its last-to-first closure. Its proof and m-state equality construction are supplied, and it is explicitly classified as a classical spectral consequence. The new finite Fourier budget requires neither cyclic closure nor a common matrix, so it is not a disguised application of that proposition. The literature record specifies inspected texts and inherited background rather than claiming exhaustive independent originality clearance.

## Sections 9, 12.6 and 13.16–18 — fixed-length and anytime autonomy

**The two tasks now have separate definitions and bounds.**

`A_N^fix` uses a common state set and common command matrices with a horizon-specific decoder correct only at length N. It is a subclass of the clocked machines. The new unrestricted lower bound applies to it, and the inherited resonant construction already uses epoch-independent command matrices. Consequently it lies between the same N^(1/5) and N^(1/3) orders at bounded-type angles.

`A_N^any` requires one decoder correct at every length 0 through N. The inherited Cayley–Hamilton proof gives at least N+1 internal states, and a triangle-label/counter gives at most 3(N+1). Two retained absorbing answer labels can be charged separately. The proof is restated to show exactly why all intermediate lengths are essential. It is not presented as a linear lower bound for the fixed-length autonomous task.

## Machine model and editorial comments

The formal definition retains finite alphabets, full external words, a specified horizon, row-stochastic updates, all persistent randomization in the register, available-label counting, normalized unreachable rows, and atomic final queries. An external epoch, exact atomic real sampling and read-only row descriptions remain part of the mathematical model. The rational and irrational constructions do not silently share a fair-bit implementation claim.

The abstract and headline theorem lead with the new unrestricted lower bound. Vector-state, stationary, anytime, and fixed-length quantities are not conflated. The proof potential appears as an independent probabilistic theorem before its rotation application. A contribution table distinguishes the new Fourier argument and main-family defect from the inherited upper construction and classical comparison/spectral ingredients.

## Pipeline and preservation

The frozen Round-Seventeen proof-dependency ledger and relevant v31–v33 derivations were read. The previous GTF path through causal experiments, hidden sections, geometric growth and continued-fraction synthesis is retained. The new proof changes the lower-bound mechanism rather than discarding those results. The separate analytic A2/A3/A4/C2/D1 and hard-sphere B2/B1/B3/B4/C1/C2/D1 gates retain their own hypotheses and proof obligations. No fully adaptive collision optimum, noisy-tag theorem, sharp hidden exponent, or aggregate closure is inferred.

The work branch was created remotely from r18 before publication. Only a new v34 package, a branch-specific workflow and a root review entry are added. The v33 article remains byte-identical as supporting-results.pdf. Both v33 cumulative volumes are appended unchanged after the current article and a divider. The compact referee package excludes the large archives and includes independently buildable core sources. Preservation and tests are delivery evidence, not proof of significance.

## Status for the next referee

The main new claims have full proofs: the homogeneous angular averaging bound, common-amplitude Fourier recursion, finite-atom Fejer witness, all-hidden occupation theorem, robust polynomial width, rational logarithmic width, and the main-family diagram-defect bound. Finite rational identities and separately labelled high-precision diagnostics exercise these arguments and implementations; they are not independent proof certification or a test of all hidden realizations. The sharp hidden exponent and general optimal-lift synthesis remain genuine quantitative questions, not claims hidden by the new lower bound.
