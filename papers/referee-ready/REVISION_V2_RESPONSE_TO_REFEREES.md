# Consolidated response to the harsh referee reports — revision v2

**Revision branch:** `theta-referee-revision-v2-2026-08-28`  
**Report branch:** `review/top4-harsh-referee-reports-2026-08-28`  
**Report snapshot reviewed by the referees:** `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`  
**Revision base:** `theta-referee-manuscripts-2026-08-28`  
**Scope:** θ-Theory only.

## 1. Status of the reports

The five reports concern the pre-split monograph, the old response manuscript,
the version-50 CM2 working note, the old HJB manuscript, and the old
representation note.  They do not review the later five-paper `referee-ready`
snapshot.  Nevertheless, every mathematical objection has been applied to the
five-paper series.  An objection is treated as closed only in one of the
following ways:

1. **proof closure:** the missing estimate or implication is proved in the
   revised manuscript;
2. **actualization closure:** a completely specified model is supplied and all
   hypotheses used by the stated theorem are checked in that model;
3. **scope closure:** a false or unsupported assertion is deleted and replaced
   by the strongest true statement, together with a no-go or an explicit
   additional hypothesis.

No archive, hash, compilation result, or internal proof audit is counted as
mathematical evidence.

## 2. Global objections and dispositions

| ID | Referee objection | Revision-v2 disposition |
|---|---|---|
| G1 | A1--A5 merely rename the desired theorem | The monograph theorem is not used.  Each revised paper states a finite theorem with either a proof or an actual model. |
| G2 | no nontrivial actual instantiation | Papers I--IV use one explicit moving-cut four-branch system and its deterministic product-shift realization.  Papers I and II also state exactly scoped radial/specular and similarity-flow results. |
| G3 | contradictory companion imports | All imports are replaced by theorem-numbered companion statements; conditional specular claims are never imported by the actual four-branch chain. |
| G4 | inconsistent HJB time sign | Every revised PDE uses the terminal convention `-u_t-\mathcal L u-H=0`; the sign is propagated through DPP, short-time expansion, Itô, BSDE and PPDE formulas. |
| G5 | one-sided Green--Kubo is not symmetric PSD | Paper II defines covariance by the symmetrized correlation series and proves equality with a variance limit, pressure Hessian and martingale bracket. |
| G6 | anisotropic pairing does not imply pointwise viscosity convergence | The revised actual HJB theorem uses a pointwise monotone dynamic-programming scheme.  No paired-to-Dirac or paired-to-a.e. upgrade is claimed. |
| G7 | nonconvexity was inserted by hand | The former polynomial port is deleted.  Paper IV derives a concave/nonconvex Isaacs Hamiltonian from an explicit strong concave--convex two-player energy game. |
| G8 | triangular Lorentz finite-horizon interval was wrong | The triangular-cell example is deleted from the controlling manuscripts.  No conclusion depends on that geometry. |
| G9 | representation calculus contained false implications | Paper V proves terminal-map differentiability under explicit uniformly parabolic hypotheses, deletes generic regularization passage and nonlinear `Z\mapsto p` inversion, and proves a genuine Novikov/Girsanov theorem. |
| G10 | manuscript was a ledger rather than a paper | The controlling objects are five standalone `main-v2.tex` manuscripts.  Internal status language is excluded from their mathematical narrative. |

## 3. Paper-I / response objections

| ID | Objection | Disposition |
|---|---|---|
| R1 | title stronger than unconditional theorem | Revised title and abstract concern moving-cut systems; the specular statement is explicitly source-specific. |
| R2 | radial example is differentiated invariance | Retained only as an invariant-projector theorem.  A separate exact cohomological-correlation susceptibility theorem records its genuine but restricted content. |
| R3 | assembly-first reset does not prove historical closure | Historical reset is absent from the revised theorem.  The actual four-branch model is closed directly on a fixed graded scale. |
| R4 | S1--S3 certificates equal the missing theorem | They are not used.  The actual product tail is proved from explicit operator formulas. |
| R5 | primitive trace domain was not transfer invariant | The actual model uses periodic Sobolev/BV levels preserved by the centered transfer operator. |
| R6 | genericity only in a custom topology | The revised maximality theorem names the exact sequence-space topology and makes no Baire claim in the full `C^r` observable space. |
| R7 | fixed-table spectral theorem was not uniformized | Uniform contraction for the actual family is calculated directly from the branch widths. |
| R8 | a second-order criterion assumed its main remainder | The criterion is removed from the main line; finite-DQ follows from an explicit fourth derivative and Taylor remainder. |
| R9 | exact conjugacy is not moving-face cancellation | It is not used as nonvacuity. |
| R10 | continuous-time response missing | Paper II supplies a separate actual moving-cut suspension theorem. |
| R11 | overgrown structure | The revised paper has one abstract mechanism, one full actual model, one restricted specular corollary, and one maximality section. |

## 4. CM2-working-note objections

| ID | Objection | Disposition |
|---|---|---|
| C1 | version 50 was not controlling | Version 50 is not cited or used by the revised papers. |
| C2 | positive hypotheses were essentially CM2 | The actual family proves its two-time envelope from a regularity-loss estimate; no actual-SRB escape, cemetery or reverse-Hölder packet is assumed. |
| C3--C5 | physical escape, conditional moments and face product tail unproved | These interfaces are absent from the actual theorem.  They remain possible tools for other billiard classes, not imports. |
| C6--C7 | fixed-section and translation pilots did not pass their gates | Neither pilot is used as an actual theorem. |
| C8 | measure-trivializing gauge excluded many deformations | The actual model has a fixed reference Lebesgue probability and requires no component-mass gauge. |
| C9--C10 | growing-depth and jet-tail constants were not closed | The actual occurrence atlas is finite, so no growing-depth or Remez assumption is needed. |
| C11 | no identification from physical current to marked kernel | The actual derivative is computed as a concrete operator on the fixed graded scale. |
| C12 | universal posture contradicted later no-go | The revised theorem is packetized and nonuniversal; the no-go boundary is stated in the paper. |
| C13 | verifiers do not prove mathematics | Agreed and stated throughout the revision record. |
| C14 | working note unreadable | It is not a submission object. |

## 5. HJB objections

| ID | Objection | Disposition |
|---|---|---|
| H1 | false Paper-I interface | Paper III imports only the pressure/covariance fields actually proved in Paper II and separately proves the invariance principle used for homogenization. |
| H2 | parabolic sign error | Corrected globally. |
| H3 | false triangular-cell geometry | Example deleted. |
| H4 | prelimit value not defined | Paper III defines an explicit deterministic product-shift one-step evaluation and its finite-horizon recursion. |
| H5 | response does not imply homogenization | A separate martingale rough-path theorem and an actual triangular-array verification are given. |
| H6 | paired residual cannot yield pointwise contact inequality | Paired residuals are not used in the actual convergence proof.  Monotonicity and pointwise consistency yield the viscosity inequalities. |
| H7 | paired convergence cannot yield local uniform/a.e. state convergence | No such conclusion is stated. |
| H8 | comparison only on a compact gradient window | The actual entropic coefficients are global and uniformly elliptic; comparison follows from the Cole--Hopf transform.  The abstract theorem assumes global structural bounds. |
| H9 | Green--Kubo PSD not proved | Closed in Paper II. |
| H10 | `H(x,0)=0` unsupported | In the actual entropic port the normalization is explicit and follows from the log-moment generating function at zero. |
| H11 | nonconvexity was hand planted | Deleted from Paper III and replaced by the actual game-derived branch in Paper IV. |

## 6. Representation objections

| ID | Objection | Disposition |
|---|---|---|
| P1 | input sign inconsistent | Corrected terminal convention is used throughout. |
| P2 | differentiability was assumed | Paper V proves a Fréchet differentiability theorem by a difference-quotient Schauder estimate. |
| P3 | viscosity regularizations do not imply derivative convergence | The generic theorem is deleted.  A passage to a limit is stated only under explicit uniform tangent estimates. |
| P4 | `Z=\sigma(x,p)^Tp` was incorrectly inverted | No inversion is used.  The tangent coefficients depend on the already known decoupling field. |
| P5 | FBSDE was only an Itô identity | The paper distinguishes the tangent-law representation from an independently solvable semilinear FBSDE and states each with its own hypotheses. |
| P6--P7 | the alleged Girsanov result was algebraic and notationally inconsistent | The algebraic shift is removed.  A genuine stochastic exponential, Novikov condition, Radon--Nikodym density and changed drift are proved. |
| P8 | linear-law obstruction lacked support/domain hypotheses | The revised theorem states the initial-state and common-core hypotheses explicitly. |
| P9 | calibrated generator needed unavailable regularity | The tangent theorem is restricted to a nonempty uniformly parabolic classical window, and the Paper-III entropic model is given as an actual instance. |
| P10 | SDE well-posedness was hidden in “regular enough” | Bounded Lipschitz coefficients and uniform ellipticity are stated. |
| P11 | robust-pricing envelope had no DPP | The unsupported envelope is deleted; the volatility-control branch has an explicit stable control family and DPP. |
| P12 | insufficient originality | The revised mathematical contribution is the differentiable tangent-law bundle and its incompatibility with a universal payoff-independent law, plus exact pathwise entropic and nondominated branches.  Journal-level significance remains for the next external review to assess. |

## 7. Meaning of closure

`Known internal objection gaps = 0` will mean that every objection above has a
proof, an actual model, or an explicit scope deletion in the revised files.  It
does **not** mean that the external referees have accepted the revisions.  A
second formal review is required before any claim of external certification.
