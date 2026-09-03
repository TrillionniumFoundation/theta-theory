# Round 33 — point-by-point proof ledger

Review: `e037717914a34fe7c0636743b3f5c645969bcb20`, Round 32, section 4.

`core_repaired` means a proved lemma or exact construction on its stated domain. It does not certify the original mechanical application. `application_open` is not a no-go result: it identifies the next mathematical obligation while preserving the research objective.

## Source integrity

All mathematical corrections are in committed source, not deferred to a finalizer. The verifier is read-only with respect to that source. It writes build outputs and evidence under `build/`. A source manifest binds the active graph to bytes. Local results and remote CI status are separate facts. No prior Round 31 verification declaration is adopted.

## A1

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-A1-01 | Top-order jet uses an undeclared derivative | Jet identities are explicitly limited to j<r; finite shells are C^r. | `core_repaired` |
| R32-A1-02 | Boundary-shell derivatives lack compatibility | Boundary shells are actual derivatives of one shell family, not unrelated arrays. | `core_repaired` |
| R32-A1-03 | Weak bounds are promoted to strong C^r | Uniform shell derivatives and the Banach fundamental theorem of calculus prove norm differentiability. | `core_repaired` |
| R32-A1-04 | Raw seam current receives an unjustified probability weight | A declared depth-weighted current example is constructed; the original unweighted seam estimate remains open. | `application_open` |
| R32-A1-05 | Ancestry projection estimate is asserted | The finite-cylinder interval [q-n,q+n] gives the exact vanishing of P_0 outside abs(q)<=n. | `core_repaired` |
| R32-A1-06 | Projection and covariance derivative sums are unproved | Finite product differentiation and a double trace-norm majorant are proved for the shell class. | `core_repaired` |

## A2

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-A2-01 | Impossible Diophantine lower bound near zero | A concrete algebraic-norm proof gives a bound only for abs(b)>=1. | `core_repaired` |
| R32-A2-02 | Three scalar parameters prescribe six targets | The dimensional requirement is identified; no concrete billiard rank-six realization is claimed. | `application_open` |
| R32-A2-03 | Automaton and UNI geometry not constructed | No verified billiard grammar is declared; the actual construction remains an application obligation. | `application_open` |
| R32-A2-04 | Bad-word terminal transversality unproved | This remains an explicit spectral/geometric input rather than a certificate declared verified. | `application_open` |
| R32-A2-05 | Anisotropic intermediate contraction compressed into a paragraph | The downstream Fourier integral is proved conditionally; the full anisotropic estimate remains open. | `application_open` |
| R32-A2-06 | High-order singular spectral calculus missing | The necessary central L1 remainder and source derivatives are stated; an iid benchmark is verified. | `application_open` |

## A3

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-A3-01 | Stopping count and occupation both named nu_N | Separate ell_N, eta_N, Q_N, L_N, J_N are defined. | `core_repaired` |
| R32-A3-02 | Head/tail indices are off by one | Edges carry exactly h_(k-1) and h_k; the endpoint identity is proved without error. | `core_repaired` |
| R32-A3-03 | div_U current has no mark coordinate | J_N lives on time, tail history, and mark; its divergence is explicitly defined. | `core_repaired` |
| R32-A3-04 | Mesoscopic H^-1 tightness has no cancellation estimate | A determined divergence defect has a proved test-dual bound; no unsupported H^-1 compactness is asserted. | `application_open` |
| R32-A3-05 | Arbitrary current recovery unproved | Exact binary renewal recovery is proved; full legal-current recovery remains open. | `application_open` |
| R32-A3-06 | Complete-past fractional moment not exported by A2 | It remains a separately required mechanical input. | `application_open` |
| R32-A3-07 | Source-dependent terminal amplitudes declared to cancel | Their ratio is retained; only separately subexponential logarithms disappear at speed N. | `core_repaired` |

## A4

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-A4-01 | Relative generator lacks a generation theorem | Relative bound, shifted dissipativity, and a real range condition give Lumer--Phillips generation. | `core_repaired` |
| R32-A4-02 | D(L_Q^3) used for O(z^-4) remainder | The source uses D(L_Q^4), four resolvent identities, and Hilbert-bounded observation. | `core_repaired` |
| R32-A4-03 | Concrete perturbation hypotheses not verified | A direct domain-safe compression theorem is proved; concrete mechanical coercivity is still required. | `application_open` |
| R32-A4-04 | Graph-angle isomorphism merely assumed | Finite orthogonal projections with basis in D(L) intersect D(L*) give a bounded off-diagonal construction. | `core_repaired` |
| R32-A4-05 | Capped Wasserstein gap transferred to unrelated norm | The transfer is proved for the same distance and explicit weighted integrability; the mechanical norm estimate remains open. | `application_open` |
| R32-A4-06 | Spectral bridges contain the desired conclusion | Finite-memory iid primitive-matrix examples are given; actual billiard exposing bridges remain open. | `application_open` |
| R32-A4-07 | Renewal maps lack continuation bounds | The concrete suspension strip bounds remain an explicit application obligation. | `application_open` |

## B1

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-B1-01 | Anchor positions incorrectly called conditionally independent | Only equilibrium velocities factor independently of all positions; a full Gaussian calculation is used. | `core_repaired` |
| R32-B1-02 | Fixed m_0 conflicts with arbitrary smoothing order | An explicit m>2(d+s+1)/d budget fixes anchor size after derivative order. | `core_repaired` |
| R32-B1-03 | Uniform exterior clearance and stationary phase missing | Equilibrium velocity smoothing avoids position charts; trajectory-tilted exterior estimates remain open. | `application_open` |
| R32-B1-04 | Maxwellian truncation tail lacks Edgeworth control | The equilibrium Gaussian integral is exact and untruncated; dynamic differentiated tails remain open. | `application_open` |
| R32-B1-05 | Event independence survives exact energy conditioning only by assertion | Event measurability and independence are used before momentum-energy disintegration, not after it. | `core_repaired` |
| R32-B1-06 | Saddle/pressure input from B2 unavailable | General dynamic-source saddle and Edgeworth claims remain application obligations. | `application_open` |

## B2

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-B2-01 | Endpoint radius hypothesis is a_0>a_0 | a_* is independent; q=eMT/(a_0-a_*)<1 and optional a_*<a_0-Lambda T. | `core_repaired` |
| R32-B2-02 | Volterra kernel and time-simplex allocation diverge | Equal radius gaps are chosen before integrating times, giving n^n/n! (Mt/Delta)^n. | `core_repaired` |
| R32-B2-03 | Endpoint norm degenerates at T | The fixed E_(a_*) norm has bound 1/(1-q) through T, including a strict intermediate radius. | `core_repaired` |
| R32-B2-04 | Tree inverse does not preserve surplus lower bound | A stacked-rank equivalence and counterexample show the missing condition; all-graph rank remains open. | `application_open` |
| R32-B2-05 | Conormal classification omits dependencies | Repeated labels and all dependencies must be checked; no complete singular classification is claimed. | `application_open` |
| R32-B2-06 | Velocity cutoff grows with uncontrolled constants | An iterated fixed-cutoff convergence lemma is proved; no quantitative epsilon power is inferred. | `core_repaired` |
| R32-B2-07 | Noncommuting pivot flows assigned a rectangle | No simultaneous flow chart is asserted without construction; this remains open. | `application_open` |
| R32-B2-08 | Time-composition logarithm declared connected cluster log | Kernel composition and disjoint-union cumulants are separated; the actual cluster identification remains open. | `application_open` |
| R32-B2-09 | Local pressure promoted to full projective LDP | Uniform scale stability is proved, but full mechanical exponential tightness and recovery remain open. | `application_open` |

## B3

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-B3-01 | Fixed Hilbert gap two not Hilbert--Schmidt | The mode-count criterion 2s>D and Minkowski summation are explicit. | `core_repaired` |
| R32-B3-02 | Microscopic remainder summed through infinitely many grids | The finite terminal sum includes its exact r_epsilon^p delta_epsilon^(-1-p gamma) budget. | `core_repaired` |
| R32-B3-03 | Maximum jump substituted for within-cell oscillation | A separate within-cell input is required and a continuous-spike counterexample is recorded. | `application_open` |
| R32-B3-04 | Free transport absent from interval moment argument | A separate drift moment bound in the same final Hilbert space is stated. | `application_open` |
| R32-B3-05 | Drift and martingale estimates use inconsistent spaces | All increments in the grid theorem and drift example use one Hilbert space. | `core_repaired` |
| R32-B3-06 | Dynamic CLT and Mosco promoted without inputs | The static entropy Mosco theorem is proved; full kinetic process and moving-reference recovery remain open. | `application_open` |
| R32-B3-07 | Hypocoercive graph domains and weights unverified | The concrete kinetic graph inverse remains an application obligation. | `application_open` |

## B4

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-B4-01 | Fast collisions change boundary direction instantly | Only scalar total-energy kinematic closure is proved; dynamics uses an explicit genuine tail gate. | `application_open` |
| R32-B4-02 | Positive probability mass at infinity admitted | The exact attainable narrow-total-energy closure is proved by a recovery mixture; mass at infinity is excluded. | `core_repaired` |
| R32-B4-03 | Boundary generator not defined | No semigroup is asserted on the kinematic closure; construction of boundary dynamics remains open. | `application_open` |
| R32-B4-04 | Second moment does not control fast collision tests | A path compactness theorem uses superlinear tail control and spatial density control as explicit additional inputs. | `application_open` |
| R32-B4-05 | Contact boundary cost missing | Finite-velocity contact compactness is not claimed to identify the missing boundary action. | `application_open` |
| R32-B4-06 | Arbitrary-boundary microscopic realization unproved | Kinematic recovery is explicit; hard-core exact-saddle realization remains open. | `application_open` |
| R32-B4-07 | Comparison Hamiltonian discontinuity at boundary | No global comparison theorem is inferred; additional spatial compactness is required; weighted strong convergence is proved sufficient for collision products. | `application_open` |

## C1

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-C1-01 | Literal control bytes in active source | Fresh printable source is checked byte by byte, including embedded carriage returns. | `source_repaired` |
| R32-C1-02 | Projective distribution bonding maps and completeness absent | Tensor Sobolev spaces, contraction bonding maps, closed projective limit, and measure embedding are proved. | `core_repaired` |
| R32-C1-03 | Weak cylinder difference quotients promoted to strong topology | Uniform finite-coordinate Taylor remainders are integrated, proving norm convergence at every seminorm. | `core_repaired` |
| R32-C1-04 | No nonempty inference example | An exact adaptive Gaussian calibration channel on an arbitrary parameter-free deterministic product hidden state is supplied. | `core_repaired` |
| R32-C1-05 | Fisher inequality promoted to Riccati filter contraction | No such implication is used; finite-horizon derivative filters and an exact posterior are proved separately. | `application_open` |
| R32-C1-06 | Incompatible diagnostic words have no schedule | Nonoverlapping fixed-length blocks with sum rho_j<=1 give a defined randomized schedule. | `core_repaired` |
| R32-C1-07 | General BvM inputs remain unproved | Uniform exact Gaussian posterior asymptotics are proved for the diagnostic example; mechanical identification remains open. | `application_open` |

## C2

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-C2-01 | Observable quotient continuity promoted to full linear filter bound | An explicit full-path likelihood L1 coupling bound replaces this inference. | `core_repaired` |
| R32-C2-02 | Second characteristics inferred from unrelated weak kernels | A truncation lemma requires actual second-moment uniform integrability and correctly typed kernels. | `core_repaired` |
| R32-C2-03 | Skorokhod cylinder uniform approximation unproved | A full-path coupling treats bounded continuous F directly; process tightness remains additional. | `application_open` |
| R32-C2-04 | Policy likelihood cancellation not stated | The same parameter-independent chronological policy is explicit; differing policies contribute RN factors. | `core_repaired` |
| R32-C2-05 | Rigidity bridges assume their conclusion | Finite graph coboundary criterion is proved; concrete singular pressure bridges remain open. | `application_open` |
| R32-C2-06 | BSDE stochastic bases underspecified | A fixed Brownian-Poisson basis with PRP, integrand norms, L2 errors, and an Ito-BDG proof is given. | `core_repaired` |
| R32-C2-07 | Imports from failed path/filter roots | No full mechanical optional-projection process theorem is imported without its inputs. | `application_open` |

## D1

| Report item | Objection | Replacement / next proof | Status |
|---|---|---|---|
| R32-D1-01 | Normalized continuous density omits positive N power | Raw-to-mean Jacobian N^d_R is derived and checked against Gaussian sample means. | `core_repaired` |
| R32-D1-02 | Labelled off-central density not exported upstream | The local-Laplace implication is proved conditionally; physical labels and off-central estimates remain open. | `application_open` |
| R32-D1-03 | Policy-dependent high-order phase jets unproved | Only leading conditional Laplace coefficients are concluded; higher mechanical expansions remain open. | `application_open` |
| R32-D1-04 | Finite-memory feedback identified with static source | Actual chronological conditional laws are used for comparison; augmented-kernel local theory remains required. | `application_open` |
| R32-D1-05 | Memory approximation and derivative budget assumed compatible | Explicit exponential memory and chart-growth powers are computed; no subpolynomial growth is silently assumed. | `core_repaired` |
| R32-D1-06 | Epi-development restates desired selection conclusion | A complete common-policy theorem is proved from power-drop and Holder exponent bounds. | `core_repaired` |
| R32-D1-07 | Complex phase and coexistence imports unavailable | No complex zero-free or full mechanical coexistence theorem is claimed without labelled local inputs. | `application_open` |

## Original targets still requiring proof

The original unweighted seam realization, concrete Sinai all-frequency/Edgeworth model, full chronological recovery and stopped local theorem, physical memory projection/pressure bridges, all-genealogy hard-sphere rank and joint LDP, dynamic exact conditioning, kinetic process tightness and graph inverse, full-action kinetic semigroup, mechanical filter/statistical identification, changing-filtration prediction limits, and labelled adaptive phase expansion remain application targets. No missing target is replaced by a fabricated proof certificate.
