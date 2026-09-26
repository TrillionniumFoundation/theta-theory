# Response to the twenty-ninth referee report

**General Theta Foundations I — Revision 44**  
**Hankel Compatibility, Distortion Rates, and Finite-Bit Memory**  
26 September 2026

Controlling report: `reviews/general-theta-foundations-i-v43-word-profiles-arithmetic-fluctuations-harsh-top4-r29-2026-09-26/REFEREE_REPORT.md`, frozen at `6e8a9504a1a0820e6195317df885d99aed06c878`. Reviewed v43 publication: `153830f5dc8d13358f9103c307c619076c5ec80c`; native source: `92722c0c14d1897740344a53e3e017258bec040e`.

The report asks for a realization-theoretic account of the resource, a relation between the two finite profiles, and a substantial advance beyond changing the presentation. This revision supplies a universal distortion–dilation inequality, an explicit controlled Hankel formulation, and a separate table-free finite-bit implementation with a charged computational resource. All v43 substantive mathematical arguments are retained, rather than replaced by those additions. The existing v44 work branch is untouched; the new branch starts directly from the controlling report.

Stable labels below refer to native LaTeX. The build resolves them to theorem numbers and pages in `evidence/THEOREM_LOCATIONS.json`.

## 11.1 and Section 4 — the minimum in the minimal-type proof

The displayed estimate now retains `min{1/2,r(1+h)/(2r+1+h)}`. The proof also says explicitly that `0<h<1/(2r-1)` selects the second branch before `h` tends to zero. Thus the stronger finite-type implication is fully visible.

One logical point merits clarification. The original line was a weaker upper bound, not a false inference: `L <= min{a,b}` always implies `L <= b`, including when b>a. At r=1,h=2 the valid upper bound 1/2 does imply the displayed weaker upper bound 3/5. No counterexample or invalid limit argument follows from that example. We have nevertheless adopted the sharper display and small-h explanation, which removes the ambiguity identified by the referee. The new regression checks both the branch cutoff and the valid direction of this implication. It is an exposition repair, not a retraction of the minimal-type theorem.

## 11.2 / Section 5 — positive realization and finite-horizon Hankel arrays

**Addressed in `prop:hankel-form`, `prop:hankel-dual`, `prop:rank-three44`, and the comparison section.**

The paper defines the full probability array `H_t[(x,u),(v,j,b)]`, with prefix length t and suffix length N-t. Every suffix/query pair is a normalized binary response. We distinguish ordinary rank, nonnegative rank, normalized stochastic factor rank and the width of a compatible chain. Separate seed rows and query columns are part of that definition; they are not omitted from a homogeneous scalar sequence.

The exact profile is equivalent to polytopes in the full future-response cube, with at most K_t generators and a common positive suffix-restriction map for each command. Approximate realization is the minimum entrywise distance to a whole response table admitting such a chain. This keeps all hidden continuation coordinates and does not project an arbitrary hidden machine into the observed plane. The per-row extension problem has an explicit l-infinity/l-one separation dual; its accumulated certificate is an upper bound, not the actual error when cancellations are possible.

These formulations are explicitly classical normalizations, not a new cone-realization theory. Benvenuti–Farina's stationary invariant-cone theorems and irrational-rotation example are compared directly. The v33 compatible-lift formulation in this repository already treated positivity extension and hidden states; that ancestry is made explicit. The current result concerns prescribed finite lengths, permits unrelated cut-dependent matrices, and allows redesign at every horizon. A stationary infinite-word impossibility argument is not used in place of the finite lower bound.

For the planar numerical experiment all three separate factor ranks equal three at every cut. A rank-three affine submatrix gives the lower bound; a legal triangle of continuations gives the matching normalized factorization. A factorization can be embedded in a whole machine with unrestricted registers elsewhere. This proves exactly why separate ranks do not detect the already established growth, without claiming that signed/positive order separation was previously unknown.

The comparison treats Balle–Panangaden–Precup's Hankel-rank and l2-approximation setting, Finesso–Grassi–Spreij's approximate stationary HMM NMF objective and common-update recovery, and Ohta's reachable/null reductions and tensor realization. Their stochastic output-law and weighted-series norms are not relabeled as worst-word conditional binary-TV error. Benvenuti's 2022 survey is included at bibliographic/abstract level only: its full text was not obtained in this audit, so no theorem number is invented.

## Section 6 and direction 12.1 — relating the finite profiles

**The new `thm:rate44` is a universal comparison, not another matching-hypotheses corollary.**

For every finite orthogonal alphabet and every feasible common k-vertex enclosure with inradius a, it proves

```
sup_(B>=1) [-log(1-Gamma_A(k,B))]/B <= log lambda_A(k,a).
```

To prove it, run the enclosure machine without imposing a final decoder. At length n its represented mean is `a lambda^(-n) U_wu`; pairing with its unit-bounded state vectors forces conditional-orbit amplitude at least `a lambda^(-n)` under every word law. Repeat an optimizing B-word packet independently m times. The same amplitude is at most `(1-Gamma_A(k,B))^m`. Taking mth roots and letting m grow removes a. This yields a per-command obstruction to every common enclosure, including noncommutative alphabets, without any gap or Diophantine hypothesis.

`cor:chain44` supplies the cut-dependent statement `I_N(K) <= log(1/a)+sum log lambda_t`. It prices a whole enclosure chain against the optimized interval certificate. These are actual inequalities between the quantities, rather than an assumption that their powers happen to match.

The conclusion is deliberately one-sided. We do not assert equality, characterize every hidden optimum by observed-state polytopes, or turn the inherited packing–dilation meta-corollary into an all-alphabet classification. The exact full-Hankel normal form and the smaller observed-space enclosure class remain distinct.

## Direction 12.5 / resource objections — a uniform finite-bit theorem

**Addressed in `lem:round44`, `thm:uniform44`, `cor:space44`, and executable `finite_bit.py`.**

The new computational model has a fixed program, a one-way command stream, finite work tape and fresh fair bits. Horizon, command counter, current label, parameters, arithmetic scratch space and the current random integer are all charged. There is no N-dependent advice or stored per-label row table. Exact arbitrary-real atomic rows elsewhere in the paper remain a different resource.

Angles must have fixed linear-space, polynomial-time digit procedures; this explicit hypothesis rules out a free oracle. The program obtains dyadic angle approximations, certifies a denominator by integer inequalities, and uses a regular q-gon plus one central state. Its reference rows have two adjacent vertices and the center as successors. Outward fixed-point sine/cosine intervals produce dyadic lower probabilities; all leftover mass goes to the center, preserving positivity and row sums exactly. The bounded terminal decoder is rounded independently.

With `b=ceil(log2(16(N+2)/epsilon))`, the program uses exactly `(N+2)b` fair bits, including dummy draws on deterministic central rows. Initialization, N commands, final rounding and angle perturbations are all included in the uniform error estimate. Every deterministic word meets the requested positive error. The program stores O(r) offsets/weights, not a table of q rows; all arithmetic registers have O(log N+log(1/epsilon)) bits. Its search and fixed-point evaluation have polynomial total time in N+log(1/epsilon), for fixed digit procedures. The reference implementation uses integer interval arithmetic, not a floating-point assertion of stochasticity.

The clean stochastic register has q+1 labels, q=O(sqrt N). Whenever the arithmetic supplies a better denominator at the stated safety constant, the search returns no larger q. Thus the minimal-type and badly-approximable clean-label exponents survive the finite-bit compilation. The full tape/configuration count is not assigned that exponent: scratch and parameters are charged separately.

For the explicit algebraic-angle alphabets the all-hidden atomic lower bound implies `s(N) >= r/(2r+1) log2 N-O(log log N)` for any fixed finite-bit program; the polynomial work-head factor is included when counting configurations. The compiler supplies O(log N), so the work order is Theta(log N). The algebraic digit hypothesis is proved by bisection and the classical norm argument is reproduced. Importantly, the O(log N) upper order alone is already obtainable by storing the r command counts. It is not presented as a new ordinary-space upper bound. The contribution here is the compatible positive implementation retaining the arithmetic clean register, with a fixed number of random bits and no hidden real table. No exact finite-bit simulation of transcendental probabilities, leading optimal space coefficient or optimal total program-size theorem is asserted.

## 11.3–11.6 and minor points — precision of statements

The abstract and introduction name the atomic positive-realization resource and separately identify the computational theorem. The series prefix is retained with a mathematical subtitle; editorial ambition is not used as proof of significance.

All constants in the almost-everywhere theorem now explicitly depend on the fixed alphabet, delta, dimension, signal and tolerance. There is no growing-r or uniform-near-relations assertion. The ordinary dual exponent is connected to Bugeaud–Laurent's Definition 1, distinguishing ordinary, uniform and simultaneous notions. The rational-s to real-s step chooses `1<s0<s` explicitly. Natural logarithms are declared.

The unit-circle constraint on quantizer centers is repeated inside its proof; the exponential cone-program size remains adjacent to the complexity discussion. Gamma=1 is interpreted as destruction of positive terminal calibration. Finite rational extensions now show `max(2,hq)`, and the held two-label cut is stated at first use. Exact real rows are not confused with the positive-tolerance compiler. All inherited Diophantine/Liouville conclusions remain unchanged in strength.

## 11.7 and historical pipeline

The complete r29 report and the frozen Round-Seventeen dependency ledger were read. The published v43 native files used here were checked against their source hashes; the v33 README was consulted to prevent duplicating an inherited lift formulation as new. The arithmetic, packet and interval proofs from v43 are present in the current article. Earlier calibration, spectral and representation results are retained at their original paths and in the unchanged supporting/cumulative volumes.

The independent A2/A3/A4/C2/D1 and hard-sphere B2/B1/B3/B4/C1/C2/D1 analysis gates are not discharged by these local finite-state results. No global kernel, LLT, stopped LDP, nonlinear semigroup, graph-core, filtering or optional-projection proof is manufactured by a dependency label. The exact finite width problem, nonminimal multidimensional arithmetic classification, precise Liouville limsup, original-page LPS audit and independent expert review remain separate obligations. This does not withdraw any theorem proved at its actual hypotheses.

## Delivery and next review

The full v43 article is byte-identical in `supporting-results.pdf`; its cumulative volumes follow the new article and a divider without alteration. The compact referee package excludes those large archives. All pre-existing repository paths and the other v44 branch remain unchanged. The workflow publishes native source first, builds that commit, independently rebuilds the core source archive and then pushes the final package without force.

The next referee can inspect the distortion-rate inequality, the normalized Hankel compatibility quantifiers, and every work/error/random-bit claim in the uniform compiler. Exact finite regressions and deliberately broken controls support implementation integrity, not universal mathematical proof or independent priority certification.
