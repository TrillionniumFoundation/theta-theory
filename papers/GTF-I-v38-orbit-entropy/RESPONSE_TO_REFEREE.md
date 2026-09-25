# Response to the twenty-second pipeline-aware referee report

**General Theta Foundations I — Revision 38**  
**Orbit Geometry and Entropy Budgets for Finite Memory**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v37-spectral-memory-pipeline-harsh-top4-r22-2026-09-25/REFEREE_REPORT.md`, frozen at `c630ea23b8a27c959466a389da5d3de49a020bd6`. Reviewed publication: `c5b8015887f83833832e393db69380afeb5a9a3b`; native v37 source: `946db04e25c075427a3f6c09054b61fef14adea9`. The new work branch was created remotely from this report before source publication. No previous manuscript or review branch is changed.

The report accepts the spherical matched-order theorem but asks for a representation-level mechanism, a quantitatively effective example, and a direct causal-coding/conditional-entropy comparison. We pursue these routes through an orbital occupation theorem, an all-spectra conjugation estimate, and a projective synthesis theorem. This is not the substitution of an ambient dimension into the previous sphere result: that substitution would give the wrong upper exponent.

Stable labels below are resolved to numbers and pages in `evidence/THEOREM_LOCATIONS.json`. The proofs are in the article. Finite checks do not establish the universal statements or certify priority.

## 16.6 / Sections 8 and 12 — beyond the spherical class

**A general representation-level occupation theorem and a matched higher-dimensional family are proved.**

Theorem `thm:occupation` concerns any orthogonal representation of a compact group with a norm gap away from its Haar-invariant functions and a uniform orbital ball bound of exponent s. Invariant functions need not be radial. The bound is

```
sum_{0<=t<N: K_t<=k} g_t
 <= 2048 D (16 A)^(2/s) kappa^(-3-2/s) k^(2/s).
```

The new sparse obstruction averages a cone over the compact group, not over the entire ambient sphere. Its hypothesis is imposed on all unit directions in the representation. This distinction is essential: hidden conditional means of initial orbit points generally leave the initial orbit. The statement permits arbitrary hidden labels and cut-dependent stochastic rows. It does not assume that an internal basis state is a geometric orbit point.

For SU(q) conjugation on traceless Hermitian matrices, Theorem `thm:all-spectra` proves the uniform small-ball bound with exponent `2(q-1)` for every norm-one spectrum, including repeated eigenvalues. A unit trace-zero matrix has at least one uniformly separated spectral cut. Small conjugation displacement then controls its rank-k spectral projector. The Grassmann graph-chart calculation bounds the probability of that projector event by an explicit constant times `r^(2k(q-k))`. Minimizing this exponent over k gives `2(q-1)`. The proof never imposes a simple spectrum or pretends a mixed centroid is pure.

Theorem `thm:projective-upper` constructs a compatible machine using a finite net of pure-state projectors. A net of sine radius h loses at most `q h^2` in every support direction of the centered density-matrix body. Choosing `h` of order `N^(-1/2)` gives `O_q(N^(q-1))` labels with exact conditional probabilities. Command rows can be the same at all epochs; the final decoder is horizon-dependent. Each row has at most q^2 successors. A real-valued centroid matrix is only a mathematical description of a label, not an extra register.

Combining these facts yields Theorem `thm:main`:

```
W_(N,epsilon) = Theta_(q,rho,epsilon,mu)(N^(q-1))
```

for every fixed q, fixed positive signal, fixed error below `rho/(2 sqrt(q^2-1))`, and the stated full group-gap hypothesis. The alphabet and quantum dimension are fixed as N grows. Adjacent algebraic SU(2) generators give an explicit finite alphabet for each q through the external Benoist–de Saxcé/Bourgain–Gamburd theorem. Its gap remains qualitative in general dimension.

A gap only on the pure-state quotient is not silently substituted for the full group hypothesis: mixed-centroid orbit directions require the latter transfer. The theorem is not a classification of every representation or every dense finite alphabet.

## 16.5 / Section 9 — an effective arithmetic example

**A separate six-command example has an analytic numerical gap certificate. The old five-command gap is not falsely declared evaluated.**

The six commands are rotations about the three axes with cosine `-3/5` and sine `4/5`, together with their inverses. They are the adjoint images of the standard norm-five quaternion representatives `1 +/- 2 i`, `1 +/- 2 j`, `1 +/- 2 k`, divided by sqrt(5). The classical LPS spherical Hecke bound gives unnormalized norm at most `2 sqrt(5)`, hence normalized norm at most `sqrt(5)/3` and squared gap at least `4/9`. Proposition `prop:LPS` states the convention and the source of the full-spectrum inequality. Finite harmonic diagonalization is not used as certification.

Theorem `thm:effective` then gives, for every N>=1,

```
[(1/(10 sqrt(3))-2 epsilon)^4 / 221184] N
 <= W_(N,epsilon) <= W_(N,0) < 150 N.
```

At exact output, the lower denominator is `19,906,560,000`; it exceeds the separate four-state minimum at `N=79,626,240,001`. The upper rows are rational, sparse and common across epochs, with an N-dependent decoder. The large constants are explicitly conservative, not optimized or a claim of practical efficiency.

This is an application of a known arithmetic theorem to a specified alphabet, not a new proof of Ramanujan expansion. The original five-gate experiment and its non-evaluated gap-dependent theorem remain intact in the preserved v37 article. The new six-symbol theorem is separately named throughout.

## 16.3 / Section 10 — causal coding, rate-distortion and aggregation

**The main article now compares objectives and theorem conclusions directly.**

The comparison uses the full Wood–Linder–Yüksel treatment: its formulations of the Witsenhausen and Walrand–Varaiya reductions (Theorems 1–2), stationary optimality (Theorem 3), and finite-memory periodic approximation (Theorem 4). These are source-law average-distortion theorems with ongoing messages and reproductions. The belief-state reduction is not a cardinality reduction to a finite register; the belief lives in a continuous simplex. Here the current orbit is not directly observed by the machine, only commands are received, no message transcript is free, and the final response is required for every word. Neither theorem is claimed to subsume the other task.

The nonanticipative rate-distortion comparison cites the finite-horizon analysis of He–Charalambous–Stavrou and identifies its directed-information objective and expected-distortion constraints. Those are not maximum persistent alphabet size. The Markov lumping comparison uses Geiger–Temmel's Theorem 9, which concerns a deterministic lumping and higher-order Markov behavior, whereas our updates are random, command-dependent and time-varying. No mere occurrence of a conditional expectation is treated as a proof-level equivalence.

These sources repair the omission without presenting the present theorem as a general solution of causal coding or state aggregation.

## 16.4 / Section 11 — Gaussian conditional-expectation entropy

**The direct conditional-mean entropy literature is compared, and the classical identity is not counted as new.**

The full Atalik–Köse–Gastpar text was inspected. Its Theorem 1 and vector Proposition 2 concern the differential entropy of the unsmoothed posterior mean under a Gaussian observation model. Its posterior-covariance identities also clarify the Hessian calculation used here. Our lemma instead allows an arbitrary finite conditioning variable and adds a fresh Gaussian after conditioning to both distributions. It bounds their entropy difference by the quadratic martingale-coupling cost. A discrete posterior mean is allowed, so its unsmoothed differential entropy need not be the object of interest.

The article does not claim priority for the Gaussian score identity, the Hessian lower bound, or a new estimation identity. The short semiconcavity proof is reproduced to keep the occupation proof self-contained. The new assertion is its use with group-invariant rather than radial functions, the all-spectra orbital sparsity estimate, and matching projective synthesis. Polyanskiy–Wu remains an explicitly different Wasserstein continuity comparison.

## 16.7 / Section 12 — resource models and branching programs

**A formal conversion is supplied, and implementation claims remain separate.**

Proposition `prop:program` identifies the atomic machine exactly with a nonuniform probabilistic ordered read-once layered program with real output columns. Appending one Bernoulli acceptance row gives Boolean acceptance probability `(1+m)/2` for a selected mean m and uses only a two-label final layer if that layer is charged. It changes no command-layer width. Several available query columns are not jointly independent outputs. The proposition separately names maximum width, total size and nonuniform row advice.

The quantum realization uses a q-dimensional density matrix, a fixed reset channel, fixed unitary commands and a single selected two-outcome measurement. The classical label-bit order is `(q-1) log_2 N+O(1)`, not linear classical bit space. Quantum memory advantages for stochastic and input-output processes are credited as prior phenomena; the contribution is the proved classical order for this numerical family.

The padded fair-bit compiler is preserved in v37. It is not said to preserve atomic labels or to implement arbitrary irrational rows exactly. Tables, arithmetic and table construction remain free in the present resource model. The theorem does not optimize autonomous stopping, total branching-program size, or uniform computational space.

## Editorial and mathematical conventions

The title retains the program identifier with a precise subject subtitle. The abstract states the group-gap and orbital hypotheses and says matched cardinality order, not exact finite complexity. A neutral contribution table distinguishes classical identities, external gaps, inherited ideas and new consequences. The operator convention is inverse pullback, its adjoint is specified, and group averaging is explicitly different from radial averaging. The general real theorem permits orientation-reversing orthogonal actions; the named examples lie in SU(q) and SO(3).

Available labels are counted. Conditional centroids and Gaussian densities are proof-side variables. Binary-TV factors of two are kept in all calibrations. The signal/error threshold is sufficient and is not claimed optimal; the stated growth is for fixed positive calibration. No log-Sobolev theorem, point-mass one-step mixing or efficient construction of huge tables is inferred from the entropy proof. Carathéodory sparsity counts successors, not arithmetic or description complexity.

## Pipeline and preservation

We read the frozen Round-Seventeen dependency ledger, the complete controlling report, the v37 entropy/sparse/width/rational/implementation arguments, and their history and status records. The new proof genuinely depends on the inherited conditional-centroid budget but replaces radial invariance by orbital invariance and proves the required geometry for all hidden spectra. This is a mathematical extension within the finite-register chain. It does not discharge branchwise Fourier/LLT, stopped-LDP, nonlinear-semigroup, domain, filtering or optional-projection obligations in A2/B4/C2 and their descendants. No documentary edge is presented as an analytic theorem.

The entire v37 article is copied without alteration to `supporting-results.pdf`. Its cumulative mathematical and development volumes are appended unchanged after the new article and a divider. Old sources remain at their original paths. The compact referee package excludes the large archives and contains the current proof, this response, the audit and standalone core sources. No old result is deleted or replaced by a no-go conclusion.

The new claims are supported by full proofs and explicit finite arithmetic witnesses. They remain subject to independent mathematical and originality review. Optimized constants, the original five-gate numerical gap, all-alphabet classification, vanishing-signal sharpness and unrelated analytic pipeline closure are not claimed.
