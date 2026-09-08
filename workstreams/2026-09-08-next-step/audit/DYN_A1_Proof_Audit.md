# DYN-A1: proof audit and disposition

**Date:** September 8, 2026.  
**Object:** Qian Qi, *Response and fluctuations of moving-cut hyperbolic path ensembles*, September 6, 2026.  
**Controlling source:** `A1_Response_Fluctuations_2026-09-06.tex`, SHA-256 `1f4734e1c9341664c1784f15f58f3136344ba9f301167a8808ab55076ee93161` (124,795 bytes).  
**Separate object:** This is not statistical A1 v36 and does not inherit its referee recommendation.

## Disposition

Retain the three principal statements as the basis of this dynamical manuscript, within their printed balanced moving-cut/Markov geometry. This pass did not establish a fatal counterexample or missing analytic implication in the examined main proof chain. The conclusion is bounded: it is not formal proof verification, a commissioned journal report, or a claim that all relevant prior work has been ruled out. No top-four acceptance recommendation is issued by this audit. The contribution comparison remains a separate publication task.

The full 1,615-line single-file source was read, including the geometric construction, coding derivatives, correlations, martingale argument, clock change, Fourier conditioning, examples, fixed-support extension, and both collision appendices. Independent finite diagnostics were written separately from the author's existing tests. Execution receipts distinguish new diagnostics from replayed author checks. Compilation and finite checks are not the reason for retaining the analytical statements.

## 1. The geometric origin of the law

The physical branch has horizontal derivative `pi_j/w_ij` and vertical derivative `w_ij/pi_j`. Their product is one; target strips partition each cell by the column balance. The finite word area is `pi_(i_-m) product P_(i_k,i_(k+1))`. The reverse-width formula telescopes correctly. This proves the stationary Markov coding from the specified geometry. It does not assume the symbols are independent.

The most recent past contraction is outermost in the backward coordinate. Reversing this composition order would break the conjugacy; the printed order is correct. Positive weights on a compact parameter set give uniform contraction of both one-sided coordinates. The piecewise exact-symplectic statement is local to each branch. The manuscript correctly does not call this a globally smooth autonomous Hamiltonian time-one map.

**Status:** no defect identified in Propositions 2.1/2.3 and Lemma 2.2 within their stated model. This is a multibaker realization; it is not a proof of generic specular billiard coding.

## 2. Derived shells and parameter derivatives

The affine coding expansion is a sum of `b_(e_k) product_(h<k) r_(e_h)`. At derivative order j, at most j contraction factors are differentiated. The undifferentiated factors give exponential decay and the derivative placements give a polynomial in depth. Summation gives the printed uniform coding-jet tail.

For a Dirac report on a D-dimensional torus, the squared H^(-s) norm of a j-th spatial derivative is bounded by `C sum_m (1+|m|^2)^(-s)|m|^(2j)`. The condition `s>D/2+j` is sufficient. The additional spatial order in the main hypothesis gives the Lipschitz control needed to compare coding jets at nearby points. Thus the physical orbit-window Dirac report has a telescoping exponentially local approximation. The shell coefficient is an approximation error, not an artificial weighting of the original physical current.

Finite word derivatives use the sum of logarithmic transition derivatives. Their L1 total is polynomial in word length because the probabilities sum to one. The proof does not differentiate a density between two infinite Markov path laws.

**Status:** the dependence on r, report length and Sobolev loss must remain visible. This is not an analytic all-order estimate in one fixed reporting space.

## 3. The Markov bridge and trace covariance

For windows separated by g transitions, the exact remaining dependence is `P_a^g-Pi_a`. Differentiating the whole tensor factorization retains derivatives of both window weights and this bridge. The numerical and exact two-state tests in the accompanying program are designed to detect the false replacement of this bridge by zero.

The double-shell proof splits at `n+m=k/2`. In the large-depth sector, coding tails dominate every polynomial in the lag. In the small-depth sector, the bridge length exceeds k/2 and supplies its own exponential bound. All derivatives through the prescribed finite order have a summable majorant in trace norm. Rank-one operator norms are products of Hilbert norms, so the same argument applies to cross covariances.

The finite-time Green--Kubo identity then gives an O(1/n) bound for covariance derivatives. This last rate follows directly from the proved weighted correlation sum; it should not be advertised as a separate independent breakthrough. The hard analytic step within this model is the common derivative bound before taking the limit.

**Status:** Theorem 1.1 is supported by the printed chain under its compact positive-flux hypotheses. No transfer to arbitrary moving-scatterer histories is obtained.

## 4. Martingale approximation and triangular parameters

The negative-lag projection vanishes for a suitable truncated past-measurable block. The positive-lag estimate is not a vanishing claim: it uses the forward Markov bridge and a geometric truncation error. The projection expansion is uniformly absolutely convergent because conditioning far into the future recovers the observable and conditioning far into the past tends uniformly to the centered mean.

For `D_0=sum_k P_0Y_k`, the difference of the two partial-sum arrays consists only of pairs with exactly one index inside the time interval. At a fixed displacement v there are O(|v|) such pairs. Exponential projection decay therefore supplies a deterministic bounded remainder. The exact two-state check has

`D_k=(epsilon_k-lambda epsilon_(k-1))/(1-lambda)`

and

`sum_(k=0)^(N-1) Y_k - sum_(k=0)^(N-1) D_k = lambda/(1-lambda)(epsilon_-1-epsilon_(N-1))`.

This confirms the endpoint sign and the need for a boundary correction, without proving the Hilbert theorem by an example.

Finite-past approximants of D have a joint compact range over the compact parameter interval. They give uniform Hilbert projection tails. Their predictable scalar covariances have uniformly summable correlations; hence triangular bracket averages have variance O(1/n). A finite time mesh and boundedness yield uniform-in-time bracket convergence. These are the missing ingredients that would not follow from a fixed-parameter scalar CLT alone, and they are present in the manuscript.

The direct characteristic-function martingale has a bounded reciprocal product because its conditional factors equal 1+O(1/n). The covariance limit is deterministic, so convergence of that product may be taken through the bounded martingale. The fourth-moment argument and Hilbert projection estimate supply path tightness. The local alternative drift follows from the already established strong mean derivative, not from differentiation of weak convergence.

**Status:** no fatal gap identified in the examined proof of Theorem 1.2. The covariance identification is a trace-norm limit; nonlinear prelimit path statistics are not differentiated by this argument.

## 5. Canonical endpoints, arithmetic, and conditioning

The finite Perron--Doob path identity retains both eigenvector endpoints and the initial stationary law. Its leading amplitude is `(pi r)(l^T 1)`, not automatically one. The inserted interior block is flanked by two long powers. At zero Fourier frequency its amplitude is that same positive endpoint factor times the stationary tilted block expectation. It therefore cancels only after the correct ratio is formed.

Equality in the Fourier spectral-radius bound is exactly the edge phase/coboundary condition. Compactness away from zero provides a strict Fourier gap. Near zero, the uniform variance lower bound and cubic Taylor error give an absolute integral error O(1/n), hence the stated relative O(n^(-1/2)) local estimate. Fixed block length is essential to the printed constant.

The physical-window conclusion uses a pointwise geometric truncation followed by the fixed-word estimate. The source takes first the long-path limit and then the truncation limit; it does not claim a uniform rate for growing inserted blocks.

**Status:** retain Theorem 1.3 with its arithmetic condition, fixed interior word window, and separate physical-decoding statement. Do not convert it into a complete empirical-path LDP.

## 6. The actual return clock and preparation

The centered current is `G=kappa-v tau`, with `v=E kappa/E tau`. The covariance is `Sigma_G/E tau`. Positivity and boundedness of the roof control the inverse clock and the unfinished reward. The length-biased base law of stationary suspension is explicitly included. Finite-cylinder approximation and uniform positive-chain coupling transfer the limit to that preparation.

The pressure root also has an independent verification: a positive Perron martingale stopped at the first roof sum exceeding physical time. Overshoot and endpoint factors are bounded. This establishes its exponential growth rate without replacing the roof by an untilted average.

**Status:** the specified suspension clock is legitimate. It is not identified with a Lorentz free-flight roof, and its physical interpretation must retain that distinction.

## 7. What is not established by this audit

There is no new line-by-line priority comparison with every multibaker, parameter-response or martingale theorem. The primary abstracts for Altaner--Vollmer, existing CLT variance-response work, and Lorentz perturbations were consulted to avoid a false novelty baseline. A specialist comparison should isolate the distribution-valued physical report, trace response, and common parameter/long-time estimates from classical ingredients.

The original unconstructed descendant seam current is not automatically the new mass-one orbit-window measure. The manuscript's change map correctly makes this distinction. Nor does its Lorentz appendix prove arbitrary many-collision response. It establishes a whole-preparation zero-or-one-event identity and finite-order distributional response only in that window.

**Next writing decision:** do not expand the setup or merge this text into statistical A1 v36. Preserve this dynamical source as a separate review object. The concrete mechanical continuation delivered with this audit is a two-collision count-response note; it does not pretend to close the remaining full-path or long-time estimates.

## 8. Evidence and reproducibility

`evidence/DYN_AUTHOR_REPLAY.json` and its log report the current replay of the original author's 35 test cases. `evidence/NEW_DIAGNOSTICS.json` reports the separate 17 test cases authored in this execution, including exact rational/symbolic checks and explicitly floating Lorentz quadrature. Optimized and ordinary executions are compared. Build receipts record what was actually compiled now; historical receipts are not counted as current executions. Every technical PDF has its own source and hash in the package manifest.

The unmodified inherited native builder was also executed in an isolated extracted copy: both complete forms compiled in three passes, producing 35 pages each with all page rasters identical at 100 dpi. The regenerated single source matches the controlling source hash. This repeated the same 35 author tests; it is not 35 additional independent cases. The original author deliverables were not changed.

Primary literature used for scope, not as an unexplained proof substitute:
- Altaner--Vollmer, arXiv:1212.4728, network multibaker context.
- Gordin--Peligrad, DOI 10.3150/10-BEJ276, martingale approximation.
- Cuny--Merlevede, DOI 10.1214/13-AOP856, martingale/WIP methods.
- Demers--Zhang, arXiv:1210.1261, Lorentz perturbation theory.
- Marklof, arXiv:1605.02715, stationary/Palm interpretation of flow entry times.
