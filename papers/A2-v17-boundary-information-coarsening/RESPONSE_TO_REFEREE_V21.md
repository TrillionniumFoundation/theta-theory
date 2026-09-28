# Response to the independent A2 v20 referee report — v21 revision

**Revision branch:** `revision/a2-v21-nondominated-lan-registered-transfer-2026-09-11`  
**Controlling report:** `reviews/a2-v20-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Reviewed v20 manuscript head:** `f3839d34fcc045da47f257fbbf61fb1699adc76e`  
**Review-branch head from which v21 was forked:** `a0dfdc85ba8fa6a0908a5b167deb563a085042e4`

## Revision principle

The v20 report correctly identifies that the previous revision repaired much
of the v19 experiment architecture but exposed a new mathematical problem in
the promoted vector theorem: a moving-support alternative need not be
absolutely continuous with respect to the null, so the displayed global
Radon--Nikodym likelihood was not defined in outward-moving directions.  The
report also asks that the spatial registration model, the abstract-to-billiard
transfer, the tangent-level design argument, and the all-order signed jet
calculation be made theorem-level rather than left to prose or nonlinear
injectivity.

V21 responds by rebuilding those interfaces.  It does **not** retreat to a
known-gap problem, delete the signed inverse, replace the statistical theorem
by a no-go statement, or weaken the all-order contact conclusion.  The active
theorem chain remains

`relative nonlinear boundary law -> signed all-order labelled rigidity -> fixed-window physical endpoint-output Gaussian experiment`.

The main changes are:

1. the original moving-support family is treated as genuinely non-dominated;
2. a dominated common-collar representative is constructed and proved
   asymptotically equivalent to it;
3. the physical statistical family is defined as an explicit anchored graph
   family in one fixed laboratory chart;
4. exact and ideal billiard endpoint laws are compared quantitatively at the
   critical Hellinger scale;
5. the signed all-order inverse is reproved from the weighted stationary
   equations, and its finite-jet differential is shown directly to be an
   isomorphism;
6. the LAN/minimax statement is attached to the endpoint-output experiment,
   while the complete stopped transcript is retained for finite-to-boundary
   transfer and cost accounting;
7. a new exact-head native-build workflow is included for the final v21
   source.

No historical mathematical source has been deleted.  The active `main.tex`
now selects the v21 controlling modules; earlier v19/v20 files remain as
provenance.

---

## R20-1 / C20-M1 — rebuild the vector moving-support theorem in the non-dominated setting

### Referee objection

The v20 theorem wrote

`log dP_{n,h}^{\otimes n} / dP_{n,0}^{\otimes n}`

for the full moving-support family.  This quantity need not exist when the
alternative support extends outside the null support.  A high-probability
common-support event can justify an asymptotic likelihood calculation, but it
cannot create a finite-sample Radon--Nikodym derivative which does not exist.

### V21 repair

New active source:

- `article/18a_vector_boundary_information_v21.tex`

The original local family remains

`P_{n,h} = (1-p_n) delta_dagger + p_n f_{delta_n h}(x) dx`

and is explicitly declared non-dominated in general.

#### 1. Exact support decomposition

`Lemma (Lebesgue decomposition and support-exclusive mass)` proves, uniformly
for `h` in each compact set,

`P_{n,h}^{perp 0}(Omega) <= C_K p_n delta_n^2`

and

`P_{n,0}{f_{delta_n h}=0<f_0} <= C_K p_n delta_n^2`.

At the critical scale

`n p_n delta_n^2 log(1/delta_n) -> 1`,

both product support-exclusive probabilities are therefore
`O(n p_n delta_n^2)=o(1)`.

#### 2. A genuinely dominated representative

V21 sets

`L_n=(log(1/delta_n))^(1/4)`, `q_n=delta_n L_n`,

keeps observations in `C_n={w_0>=q_n}`, and sends successful observations in
the discarded collar to a second cemetery atom `partial`.  The resulting law
`overline P_{n,h}` is dominated by `overline P_{n,0}` on every compact local
parameter set for all large `n`.

`Lemma (Common-collar asymptotic equivalence)` proves

`Delta_LeCam({P_{n,h}^{\otimes n}}, {overline P_{n,h}^{\otimes n}})
 <= C_K n p_n q_n^2
 = O((log(1/delta_n))^(-1/2)) -> 0`.

Thus the revision no longer treats a nonexistent likelihood as though it were
defined; it replaces the original family by a nearby dominated experiment by
an explicit pair of Markov kernels.

#### 3. LAN is stated only where the likelihood exists

`Lemma (Uniform LAN for the dominated representative)` proves

`log d overline P_{n,h}^{\otimes n}/d overline P_{n,0}^{\otimes n}
 = h^T Delta_n - 1/2 h^T Q_n h + o_P(1)`

uniformly on compact local sets, with

`Delta_n => N(0,J_Sigma)` and `Q_n -> J_Sigma`.

The theorem then states that the **original non-dominated experiment** is
asymptotically equivalent to this uniformly LAN representative and hence
converges to the same Gaussian shift.  It does not retroactively assign a
finite-sample RN derivative to the original family.

#### 4. Contiguity, local alternatives and quadratic risk

Compact-uniform contiguity is established after the dominated LAN expansion
and then transferred by experiment equivalence.  The local central sequence
under alternatives is obtained from the dominated representative by Le Cam's
third lemma.  V21 also proves a compact-uniform fourth-moment bound under
local alternatives and uses it for uniform integrability of the quadratic
risk before passing from truncated quadratic loss to the unbounded quadratic
loss.

This closes both the major non-dominance objection and smaller comments 2--4
of the report.

---

## R20-2 / C20-M2 — define one physical common-coordinate family

### Referee objection

The previous phrase “registered endpoint coordinates” did not by itself prove
that all parameters were observed through one parameter-independent map.  The
report requested either an explicit anchored fixed-chart submodel or a full
laboratory-space treatment with moving contact/frame nuisance variables.

### V21 repair: explicit anchored registered submodel

New active source:

- `article/18b_raw_physical_multirate_v21.tex`

The statistical theorem now begins with one Euclidean laboratory chart
`(x,y)` and the literal family

`Gamma_{0,vartheta} = {(-psi_{0,vartheta}(u),u)}`,

`Gamma_{1,g,vartheta} = {(g+psi_{1,vartheta}(v),v)}`,

with

`psi_{b,vartheta}(0)=psi'_{b,vartheta}(0)=0`

for every parameter.  The obstacle labels, transverse origin `y=0`, and
tangent direction are fixed throughout the statistical family.  Varying the
gap translates the second graph only in the normal `x` direction.

The raw endpoint map is printed explicitly:

- on success it returns the laboratory `y` coordinates of the first and last
  physical collision points;
- otherwise it returns a common failure symbol.

The fixed patches are selected by the same labels and the same inequalities
`|y|<u_*` at every parameter.  Hence both the raw record space and endpoint
observation map are parameter independent.

The deterministic signed-rigidity theorem remains broader.  The anchored
hypothesis is stated only for the physical statistical family; it is not
silently imposed on the preceding geometric inverse theorem.

### Generic nearby tables are not hidden inside the anchored formula

The final subsection of `18b_raw_physical_multirate_v21.tex` explains the
laboratory-space extension.  If `chi_{b,eta}` maps laboratory transverse
coordinates to moving contact-centered coordinates, then the observed action
is

`mathscr S_{b,eta}(y)=S_{b,eta}(chi_{b,eta}(y))`

and its first variation contains

`D_eta mathscr S_b[h]
 = D_eta S_b[h] + S'_b D_eta chi_b[h]`.

Thus contact translation/frame rotation contributes explicitly to the support
velocity and is not erased by the word “registered.”  The abstract
non-dominated theorem applies once these nuisance coordinates are included.
V21 does not claim that the anchored information matrix is unchanged after
silently adding them.  A charged registration pilot is negligible at the
same boundary Hellinger scale

`k_n epsilon_n^2 log(1/epsilon_n) -> 0`.

This chooses the report's Route A for the main theorem while making the Route B
velocity correction explicit enough to prevent scope ambiguity.

---

## R20-3 / C20-M3 — quantitative abstract-to-billiard experiment transfer

### Referee objection

V20 used an `o(delta_n)` support perturbation and an `O(delta_n)` amplitude
perturbation and then asserted that the abstract likelihood proof was uniform
under them.  At a linearly vanishing boundary the support scale is
`epsilon^2 log(1/epsilon)`, so this step required an explicit experiment
comparison.

### V21 repair

Two new statements close this interface.

#### 1. General moving-hypersurface stability

`Lemma (Quantitative stability of a linearly vanishing support)` in
`18a_vector_boundary_information_v21.tex` proves that for two normalized
linearly vanishing densities on a common tubular family,

`H^2(f, f_tilde)
 <= C { epsilon^2 log(e/epsilon) + eta^2 }`,

where `epsilon` controls the `C^1` support-defining-function error and `eta`
controls the regular amplitude error.

The proof separates the `O(epsilon^2)` boundary-strip mass from the common
support, where the square-root density difference has the integrable envelope
`eta^2 s + epsilon^2/s`.

#### 2. Exact billiard endpoint law versus ideal vector family

`Proposition (Quantitative fixed-window reduction)` in
`18b_raw_physical_multirate_v21.tex` proves, uniformly on compact local
parameter sets,

`|| w^{ex}_{n,z} - (w_{b,d} - delta_n U_b z) ||_{C^2}
 <= C_K r_n`,

with

`r_n = delta_n^2 + delta_n/j_n`,

and

`|| A^{ex}_{n,z} - A_{b,d} ||_{C^1} <= C_K delta_n`.

The ideal density is explicitly normalized.  The stability lemma gives

`H^2(f^{ex}_{n,z}, f_tilde_{n,z})
 <= C_K { r_n^2 log(e/r_n) + delta_n^2 }`.

At

`k_n delta_n^2 log(1/delta_n) -> 1`

and `j_n -> infinity`, the proof checks in two cases (`j_n^{-1} <= delta_n`
and `j_n^{-1} > delta_n`) that

`k_n r_n^2 log(e/r_n) -> 0`,

while `k_n delta_n^2 -> 0`.  Hence the exact and ideal endpoint product
experiments are at `o(1)` Le Cam distance.

The physical Gaussian theorem is now obtained by composition of two actual
experiment comparisons:

`exact billiard endpoint experiment`

`~ ideal linear moving-support experiment`

`~ dominated common-collar ULAN representative`.

There is no longer an informal appeal to “uniformity of the likelihood
proof.”

---

## R20-4 / C20-M4 — finite-design nonsingularity at the tangent level

### Referee objection

The v20 proof inferred tangent injectivity from the nonlinear signed inverse.
Nonlinear injectivity alone does not imply injectivity of the differential.

### V21 repair

New active source:

- `article/23a_signed_endpoint_rigidity_v21.tex`

`Proposition (Tangent injectivity of the finite signed-jet map)` defines, at
fixed positive gap and for each finite order `M`,

`A_M:(kappa_0,kappa_1,q_3,...,q_M) -> (s_2,s_3,...,s_M)`.

The leading map `(kappa_0,kappa_1)->(a_0,a_1)` has the explicit smooth inverse
printed in the theorem, so its differential is invertible.  At every degree
`n>=3`, the new jet pair enters through

`M_n = [[coth(n gamma), r_0^n csch(n gamma)],
        [r_1^n csch(n gamma), coth(n gamma)]]`

with `det M_n=1`.  Dependence on lower jets lies strictly below the diagonal.
Thus `D A_M` is block lower triangular with invertible diagonal blocks and is
an isomorphism.  Compactness gives the quantitative bound

`||D A_M[h]|| >= c_M ||h||`.

`Lemma (Finite positive-offset design)` in
`18b_raw_physical_multirate_v21.tex` now uses this differential statement
directly.  A common information-kernel vector first has zero gap component,
then zero variations of both action germs, and finally zero finite jet vector
by the tangent isomorphism.  Compactness of the finite-dimensional unit sphere
selects finitely many positive windows.

The theorem now explicitly states that this finite design may depend on the
chosen finite jet order `M`.  No universal finite window set for the full
infinite jet is claimed.

---

## R20-5 — standalone all-order signed jet proof

### Referee objection

The determinant-one matrix was promising but its derivation was too compressed
for a theorem carrying much of the paper's originality.

### V21 repair

The v21 signed section has been rewritten around three standalone
propositions.

### A. Weighted stationary equations

For the half-line starting at contact type `b`, V21 writes the stationary
system

`F_{b,i}(x,u;q)
 = partial_2 ell_{b+i-1}(x_{i-1},x_i)
 + partial_1 ell_{b+i}(x_i,x_{i+1}) = 0`

in the weighted space

`X_rho={x: sup_i rho^{-i}|x_i|<infinity}`

with `e^{-gamma}<rho<1`.

`Proposition (All-order stationary-sequence calculus)` recalls the explicit
positive half-line Jacobi Green kernel from the nonlinear boundary-layer
proof, proves the bounded inverse on `X_rho`, and differentiates the
stationary system inductively.  At each order the highest orbit derivative is
multiplied by the same uniformly invertible operator; every other term uses
only lower orbit derivatives and graph jets.

### B. Envelope isolation of the highest new homogeneous degree

For variation of only `q_{r,n}`, V21 writes the stationary-action envelope
identity.  Interior stationary-orbit variations cancel, the tail boundary
term vanishes, and the first degree in which the varied graph jet can occur is
obtained by substituting the **linear** half-line orbit.  Hence lower nonlinear
orbit terms cannot contaminate the degree-`n` coefficient.

### C. Both geometric sums and determinant

For an orbit starting at type `b`,

`t_i^(b)=rho0^i` on even sites and
`r_b rho0^i` on odd sites, with `rho0=e^{-gamma}`.

The boundary site is counted once and every interior site twice.  V21 then
computes

`partial_{q_{b,n}} S_b^(n)(0)
 = 1 + 2 sum_{k>=1} e^{-2 n gamma k}
 = coth(n gamma)`

and

`partial_{q_{1-b,n}} S_b^(n)(0)
 = 2 r_b^n sum_{k>=0} e^{-n gamma(2k+1)}
 = r_b^n csch(n gamma)`.

Reversing the labels gives the second row.  Since `r_0 r_1=1`,

`det M_n = coth^2(n gamma)-csch^2(n gamma)=1`.

The inverse block is printed, the recursion is explicit, and finite-order
quantitative local inverse bounds follow on compact positive geometric sets.
The section also states precisely that odd graph jets are fixed-frame
coordinates: reversing an oriented transverse frame changes their signs.

The result is therefore not weakened; the mechanism supporting the original
all-order claim is now exposed in the controlling paper.

---

## R20-6 — separate endpoint-output information from the complete transcript

### Referee objection

Preparation cost was correctly charged in v20, but the complete stopped
transcript is statistically richer than the successful endpoint coarsening.
The reported `K_design` is not an efficiency bound for every procedure using
waiting counts and stopping information.

### V21 repair

The abstract, introduction and physical theorem now use the phrase
**endpoint-output Gaussian experiment** for the LAN/minimax conclusion.

`Theorem (Uniform stopped finite-to-boundary transfer)` compares the complete
actual and boundary stopped transcripts in total variation while retaining:

- failures,
- successes,
- design labels,
- raw endpoint records,
- stopping times.

Every common Markov coarsening inherits the transfer.  The endpoint-output
coarsening is then the experiment to which the Gaussian information and
local minimax theorem are attached.

`Remark (Endpoint information is not complete-transcript efficiency)` states
explicitly that waiting counts can carry additional, possibly faster,
information through the `sinh(j gamma)^{-1}` success factor.  Charging all
preparations is not equated with statistical equivalence of the richer
transcript.

This is now also reflected in the abstract: the complete transcript is used
for physical transfer and cost, while the Gaussian/minimax statement is for
the endpoint-output experiment.

---

## Pilot sigma-field clarification

The new

`Corollary (Pilot-centered endpoint-output equivalence)`

states exactly what is compared.  The pilot is used operationally, its cost is
charged, and its estimate determines the subsequent physical windows.  The
Le Cam comparison is made on the **post-pilot endpoint-output sigma-field**:
the retained selected endpoints plus the cap cemetery symbol.  The pilot
transcript and numerical realized design times are not included in that
comparison experiment.

The corollary explicitly makes no equivalence claim for a richer experiment
which retains those random coordinates.  This addresses smaller comment 6
without treating data-dependent times as literally identical to oracle times.

---

## R20-7 — canonical native build

A new workflow has been added:

- `.github/workflows/a2-v21-native-build.yml`

It is pinned to the v21 revision branch and triggers whenever the active A2
source or the workflow itself changes.  It:

1. records the exact Git head and preserves a source tarball;
2. installs the native TeX dependencies on an actual `ubuntu-latest` runner;
3. runs the repository's submission build driver on the exact checked-out
   source;
4. runs the boundary diagnostics in normal and `python -O` modes and compares
   the outputs;
5. rejects fatal TeX diagnostics and unresolved references/citations;
6. records PDF hashes on success and uploads the build directory on every
   conclusion.

The v20 failed-before-runner event is not represented as a TeX failure, but it
is also not represented as a successful certificate.  V21 requires an actual
runner-executed successful build before its verification record is marked
successful.

---

## Smaller comments

### 1. Ambiguous logarithm notation

The active vector theorem now writes exactly

`L_n=(log(1/delta_n))^(1/4)`.

### 2. Experiment convergence versus LAN

V21 reserves “uniform LAN expansion” for the dominated common-collar
representative.  The original moving-support experiment is described as
asymptotically equivalent to that representative and converging to the same
Gaussian shift.  These statements are distinguished explicitly.

### 3. Uniform estimator limits

The local central-sequence estimator is transferred only after compact-uniform
contiguity has been established for the dominated representative and then for
the original experiment.

### 4. Unbounded quadratic risk

A compact-uniform fourth-moment bound under local alternatives is proved, not
only under the null.  Uniform integrability is invoked before the passage from
bounded truncated losses to the unbounded quadratic risk.

### 5. Finite design scope

The finite positive-window design is indexed by the chosen finite jet order
`M`.  No universal finite design for the infinite jet is asserted.

### 6. Pilot output sigma-field

Handled as described above: the compared experiment is the post-pilot
endpoint-output sigma-field; richer pilot/time transcripts are not declared
equivalent.

### 7. Onset language

The deterministic inverse continues to use physical onset to identify the
gap.  The statistical theorem does not insert onset as an oracle observation:
the unknown gap is an actual local coordinate at rate `delta_n/j_n` in fixed
physical windows.  The separate onset pilot remains charged.

### 8. Proof dependency graph

The active main source now points to the v21 introduction, v21 signed inverse,
v21 non-dominated vector theorem and v21 physical experiment.  Earlier
versions remain as repository provenance rather than controlling theorem
sources.

### 9. Version-source friction

The repository retains its historical directory for compatibility, but v21
adds an explicit revision branch, v21 response, v21 source manifest and v21
build workflow.  The active `main.tex` selects only the v21 controlling
modules for the newly repaired interfaces.  Historical files are not deleted.

### 10. AI-assisted memoranda

The acknowledgment remains factual.  The manuscript does not use the
existence of those memoranda as evidence of correctness or editorial
acceptance.

---

## Strength retained and strengthened

The revision preserves all of the substantive v20 advances:

- a uniform nonlinear long-bridge relative boundary law on a fixed collar;
- fixed physical acquisition times rather than parameter-dependent centered
  time windows;
- the gap as an inferential coordinate at the faster `delta_n/j_n` scale;
- signed support recovery of the two unsymmetrized actions;
- recovery of both curvatures without supplying them;
- arbitrary odd and even labelled contact jets through determinant-one
  all-order blocks;
- analytic contact-germ determination;
- complete finite-to-boundary stopped-transcript transfer with failed
  preparations charged;
- explicit acknowledgement that waiting counts may carry additional
  information.

It strengthens the proof architecture by replacing the invalid dominated
likelihood with an experiment-equivalence argument, replacing nonlinear
inverse rhetoric with a differential isomorphism, and replacing qualitative
billiard-to-abstract stability with an explicit critical-scale
Hellinger/Le Cam theorem.

The requested top-four reassessment can therefore focus on the mathematical
and significance content of the repaired theorem package rather than on the
finite-sample domination, registration or transfer gaps identified in v20.
