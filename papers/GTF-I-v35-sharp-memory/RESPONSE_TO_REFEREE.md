# Response to the nineteenth pipeline-aware referee report

**General Theta Foundations I — Revision 35**  
**Sharp Width of Hidden Rotation Experiments**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v34-compatible-dynamics-pipeline-harsh-top4-r19-2026-09-25/REFEREE_REPORT.md`, frozen at `6016075083626f7c94cfb07912c49fa256fcf9e0`. Reviewed v34 publication: `47bc47e5995e4b1b99a18aaa472a1309f1668f40`; native source: `5d773fb7dddb007887119b35cc29e0b3bae7406f`.

The report correctly identifies the hidden fifth-root/cube-root gap as the central mathematical question. This revision closes that gap for every badly approximable angle, in the original fixed-alphabet model, against arbitrary hidden stochastic states and at every fixed uniform row error below 1/20. It also proves a representation-valued compression theorem and a matched higher-dimensional result in a separately specified compact-command model. The new proof does not sharpen the fair-bit Fourier kernel; it changes the external test distribution to independent packets with correlated commands inside each packet.

Stable labels refer to the native LaTeX. `evidence/THEOREM_LOCATIONS.json` gives the actual compiled theorem numbers and pages. Analytic proofs are in the focused article; neither finite checks nor the number of previous revisions is external validation.

## 12.4 / Sections 4 and 13 — the hidden exponent gap

**Resolved, at the stated badly approximable angles and fixed signal/error.**

`thm:main` proves `W_(N,epsilon)(alpha) = Theta_(alpha,epsilon)(N^(1/3))` for every badly approximable alpha and fixed `0 <= epsilon < 1/20`. All stochastic rows may vary with time, all hidden directions are allowed, and the machine may be redesigned at every horizon. The matching upper construction is inherited and reproduced in full. Consequently hidden, vector-state and fixed-length common-command-row exact widths have the same order (`cor:common-row`). This is not a statement about one unchanged decoder correct at all stopping lengths.

The proof of `lem:packet` considers the norm of a conditional past-orbit mean. A fresh packet product is independent of the earlier process. After integrating out the entire computation within the packet, its endpoint has a common stochastic kernel from the starting state and packet word. Its at-most-k conditional centroid directions form a quantizer. Maximizing over its actual assignment, then over arbitrary assignments, bounds the surviving amplitude by one minus the orbit quantization loss. No observable-state or simplex-projection assumption is introduced.

For the circle, a length `B=2k-1` packet is `1^J 0^(B-J)` with J uniform on `0,...,B`. It consists of B actual commands, not one free enlarged input. Its 2k phase increments are separated by `s_B=min_(1<=l<=B)||l alpha||`. Any k centroid directions leave at least half the increments at circular distance at least `s_B/2`, giving relative loss at least `s_B^2`. Distinct packets are independent; commands inside one packet are not. We use the conditional-mean identity only at packet boundaries, not a false single-step independence assertion inside them.

For peak K, terminal correlation `kappa=1/10-2 epsilon` therefore forces

```
floor(N/(2K-1))*s_(2K-1)^2 <= log(1/kappa),
N < (2K-1)+(2K-1)^3*b_alpha^(-2)*log(1/kappa).
```

At the golden angle the exact lower bound is `W > (N/168)^(1/3)`, as well as `W>=3`. The constants are not optimized and no exact integer optimum or leading asymptotic constant is claimed.

`thm:occupation` also gives `#{1<=t<=N:K_t<=k} <= 2k-2+8 b_alpha^(-2) k^3 log(1/kappa)` without bounding any other cut. It selects disjoint test packets using the available profile, never by inspecting actual private states. Thus the original occupation objective is strengthened rather than discarded. An available-label bound always holds; positive-mass endpoint counts can be used only under the particular test law being analyzed.

The result need not hold under the old fair-command law by itself. A wordwise simulator has to work under all chosen input laws, which licenses the packet law. No claim about average-case fairness is silently strengthened. General irrational angles retain a separation-function bound, and the rational-entry irrational rotation retains an explicit logarithmic consequence; it is not asserted badly approximable.

## 12.5 / Section 10 — compact-group scope

**Addressed by a general packet theorem and a separate matched noncommuting example.**

`thm:group-budget` holds for any finite-dimensional orthogonal or unitary representation of a compact group. It defines an intrinsic orbit distortion `Gamma_k(mu)`, and proves `sum_i Gamma_(k_i)(mu_i) <= log(1/kappa)` for independent packets and a nonzero terminal correlation. The packets need not commute. An invariant direction can make Gamma zero, so a positive lower bound is proved from orbit geometry rather than assumed for all representations.

`prop:small-ball` supplies a reusable criterion in terms of orbital ball masses. `cor:characters` embeds the binary-circle lower theorem in compact-group characters, including characters of higher tori. It does not turn several marginal correlations into a free joint-output product claim.

`thm:sphere` treats the explicitly different interface in which every element of SO(d) is an exact atomic command and the final task is one coordinate of its action on a unit seed. Haar orbit cap bounds give `Gamma_k >= c_d*k^(-2/(d-1))`, and a spherical-net stochastic construction matches the lower bound. Thus its exact and sufficiently accurate hidden widths are `Theta_(d,epsilon)(N^((d-1)/2))`. Its rows are Borel functions of the compact input; they can be chosen independent of time, with a horizon-dependent final decoder. For d>=3 this is a noncommuting model. It is not a theorem giving that exponent for every finite generating alphabet or a free finite-bit representation of a real matrix.

The sphere covering and cap estimates are classical geometric tools and are proved as needed. The sequential conditional-centroid contraction is the common mathematical step connecting them with causal width.

## 12.2 / Section 5 — branching-program comparison

**A dedicated model and theorem comparison is in the main article.**

The article now identifies the clocked transducer as a probabilistic ordered read-once layered program with arbitrary stochastic rows and a real terminal readout. It separates maximum layer width from total size and uniform description complexity. Appending a Bernoulli acceptance row converts a selected real decoder into randomized Boolean acceptance without increasing width beyond two. The two coordinate means combine into a complex readout on the same state alphabet, without demanding two independent answers.

The article explicitly writes its standard Boolean-input matrix Fourier coefficient. That coefficient differs from a harmonic of a conditional phase measure; our new packet proof needs neither a Boolean Fourier-growth estimate nor the original fair-bit harmonic potential.

Reingold–Steinke–Vadhan (2013), Steinke–Vadhan–Wan (2017), and Lee–Pyne–Vadhan (2022) are compared at the model and stated-theorem level. The inspected regular/permutation results have their hypotheses; arbitrary row stochasticity does not preserve a uniform state law, as the reset matrix demonstrates. We also point out that some unrestricted deterministic Fourier bounds extend by convexity to randomized tables, so randomness is not used as a blanket novelty argument. None of the cited stated theorems supplies the packet orbit-distortion inequality or the nonuniform width/correlation product asserted here. The research claim is this explicit mathematical statement, not an exhaustive independent priority certification.

## 12.3 / Section 6 — circle walks and arithmetic

**The missing primary comparison is supplied.**

Berkes–Borda, *Random walks on the circle and Diophantine approximation*, is cited in the article and audit. The exposition distinguishes the known harmonic multipliers of the uncompressed walk from loss caused by compression into a hidden register. For a biased Bernoulli test the multiplier is `1-p+p exp(2*pi*i*l*alpha)` and its squared modulus is `1-4p(1-p) sin^2(pi*l*alpha)`. The new packet law is separately defined and does not purport to be that independent-bit walk. Badly approximable means bounded continued-fraction type, defined once. The rational-entry rotation still has irrational angle.

## 12.6 / 3.3 / specific point 8 — the angular estimate

**The proof gap is repaired, and the universal coefficient is sharpened and shown optimal.**

Appendix `lem:angular` proves

```
|E f_l(Z)-f_l(EZ)| <= (l^2-1)*(E|Z|-|EZ|).
```

The case l=1 is linear. For l>=2, retain `l(l-1)` in the Taylor remainder and add `l-1`, giving `l^2-1`; the zero-mean case is handled directly. Symmetric two-point distributions approaching one direction prove this coefficient cannot be improved uniformly over all complex mixtures. Thus the quadratic order is genuinely present in the general averaging lemma. The new cube-root result bypasses the harmonic summation instead of claiming an unjustified linear angular bound. The original published PDF and its theorem are retained; the improved proof is in the current article.

## 12.7 / Section 7 — actual error versus accumulated local deficiency

**The new lower bound is first proved for actual terminal error.**

`thm:final-error` defines the compact finite-dimensional optimum `E_N(profile)` over all legal machines and the maximum actual terminal row-TV error. A finite interval budget, computable from the width profile and the separation numbers, gives

```
E_N(profile) >= [1/10-exp(-B_alpha(profile))]_+/2.
```

This inequality holds whether intermediate modeling errors cancel or not. For badly approximable alpha and peak `o(N^(1/3))`, the liminf of the actual error is at least 1/20. The lower constant is not claimed optimal, nor is the inequality an exact formula for every finite profile.

Only afterwards does `cor:diagram` apply the executable common-row composition argument to the accumulated local certificate `D(E)`. It keeps the classical Blackwell/deficiency attribution, and explicitly says D(E) may overestimate final error because of cancellation. It does not minimize all diagrams or identify the local sum with the intrinsic optimum. This answers the semantic concern without deleting the earlier operational statement.

## 12.1, 12.8–12.10 and model/editorial points

The General Theta Foundations I program prefix is retained, with a precise subject subtitle. The abstract leads with the resolved width law and states the clocked atomic-row convention and the separate compact-input extension. A contribution paragraph distinguishes new, inherited and classical material. The final mathematical conclusion does not require knowledge of internal A2/B4/C2 labels.

The resource definition counts available persistent labels. Epoch, horizon, row tables, arithmetic and exact real sampling remain free in this positive-realization width model; this is not ordinary uniform computational space. Exact irrational rows are not claimed finite fair-bit algorithms. The fixed-length common-row upper theorem displays its N-dependent decoder in the statement. The inherited anytime theorem is not used or claimed new. The compact-command model cannot be confused with the fixed binary-command theorem.

## Historical pipeline and preservation

The frozen Round-Seventeen proof ledger and the relevant v32–v34 mathematical sources were consulted. The new result closes the previously recorded sharp-hidden-rotation-width objective for badly approximable angles and fixed positive signal. It does not discharge independent branchwise Fourier/LLT, stopped-LDP, nonlinear-semigroup, operator-domain or optional-projection gates in other manuscripts. Those claims are not inferred from the use of Fourier or stochastic kernels here. Fully adaptive collision validation, noisy-tag composition, and unrestricted analytic aggregate closure remain distinct.

The entire v34 article is byte-identical in `supporting-results.pdf`. Its cumulative mathematical and development volumes are appended unchanged after the current complete article and a divider. The small referee package contains only the current article, response, audit and standalone core reproduction files; large archives are optional repository records. All older repository paths remain unchanged. No theorem is replaced by a build receipt or by a no-go conclusion.

## Disposition for the next referee

The main quantitative request is answered by a matched cube-root theorem for arbitrary hidden states, with a nonuniform occupation bound and fixed-error robustness. The generalization request is answered by the representation-valued packet budget and the distinct sharp SO(d) command theorem. The direct literature omissions and angular proof issue are repaired. Exact finite-width constants, all irrational arithmetic classes, a uniform bit implementation of real commands, and unrelated program-wide analytic closure are not claimed. Independent scrutiny of the new proofs and priority boundary remains necessary.
