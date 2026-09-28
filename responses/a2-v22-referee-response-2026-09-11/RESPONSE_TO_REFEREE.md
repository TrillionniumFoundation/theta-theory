# Response to the A2 v21 independent referee report

**Revision:** A2 v22  
**Revision branch:** `revision/a2-v22-allorder-multichannel-top4-2026-09-11`  
**Report answered:** `reviews/a2-v21-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Report branch head used as revision base:** `0d94442420c5b2117246962cd984c7795caa8738`  
**Canonical v22 manuscript-source commit:** `82a19b18f35fee63819bcc99d530f52adf56c384`  
**Active entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`

We thank the referee for distinguishing the repairs already achieved in v21 from the remaining issues.  The v22 revision does not reduce the theorem package in response to the report.  It instead expands the proof of the all-order inverse, fixes the physical/statistical formulation at theorem level, and adds a finite-channel analytic table-rigidity theorem so that the determinant-one local mechanism has a global geometric consequence.

## R21-1. Fully close the all-order signed-jet calculus

**Addressed in:** `article/23a_signed_endpoint_rigidity_v22.tex`.

The v21 proof compressed the step from weighted stationary equations to arbitrary-order action-jet dependence.  The referee correctly observed that differentiating a stationarity equation \(k\) times may expose a graph derivative of order \(k+1\); therefore the sentence asserting graph order at most \(k\) at the equation level was not a valid proof of the action filtration.

V22 replaces that shortcut by the following self-contained package.

1. **Quantitative weighted inverse.**  The half-line Green kernel is estimated directly on \(X_\rho\).  Along the nonlinear stationary orbit we prove
   
   `||H_b(u,q)-H_b^0(q)||_{X_rho -> X_rho} <= C |u|`
   
   and, after shrinking the common endpoint box,
   
   `||H_b(u,q)^{-1}|| <= 2 C_0`.
   
   This is an explicit Neumann-series estimate, uniform on compact positive geometric sets.

2. **Correct derivative-order bookkeeping.**  V22 explicitly states that orbit derivatives can see one higher graph derivative.  The order of the *action* is proved separately from the exact first variation rather than inferred from the differentiated stationarity equations.

3. **Differentiated infinite action.**  The infinite stationary action and every fixed finite family of mixed derivatives are shown to converge absolutely from the weighted orbit estimates.

4. **Finite-truncation envelope identity.**  The action is first truncated.  Interior orbit-variation terms cancel by stationarity.  The sole remaining right boundary term obeys a uniform estimate of the form
   
   `|partial_u^k R_N| <= C_k rho^(2N)`,
   
   so the half-line envelope identity follows by an actual tail limit.

5. **Homogeneous-degree isolation.**  For a variation of the \(m\)-th graph jet,
   
   `partial_{q_{r,m}} S_b(u) = O(u^m)`.
   
   Hence a graph jet of order \(m>n\) cannot enter \(S_b^{(n)}(0)\).  At \(m=n\), the degree-\(n\) coefficient is obtained from the linear half-line orbit alone; nonlinear orbit corrections increase the degree.

6. **Geometric sums and signs.**  The own-contact and opposite-contact sums are displayed with boundary/interior multiplicities.  They yield
   
   `coth(n gamma)` and `r_b^n csch(n gamma)`
   
   and therefore the determinant-one block exactly as in v21.

7. **Quantitative finite-jet inverse.**  The finite signed-jet map is proved \(C^1\), block lower triangular, and invertible at every strictly convex labelled jet.  Its least singular value has a positive minimum on every compact positive finite-jet set.

Thus the determinant-one theorem is retained at *all* finite orders; no truncation to a low-order reconstruction has been made.

## R21-2. Fix the physical itinerary/parity

**Addressed in:** `article/18b_raw_physical_multirate_v22.tex`, the v22 introduction, and the abstract.

Every same-type physical design now explicitly uses

`j_n in 2 N,  j_n -> infinity`.

The text states near the first definition of a `bb` design that an odd flight number terminates at the opposite contact and would require the mixed action \(S_b\oplus S_{1-b}\).  All same-type support, information and batch formulas are therefore attached to an itinerary which actually realizes the stated law.

## R21-3. Fix the cap quantifiers

**Addressed in:** Lemma `Reference-based cap` in `article/18b_raw_physical_multirate_v22.tex`.

The experiment is now defined before any compact local set is quantified over.  For each design we choose the single deterministic cap

`N_{n,l} = ceil(4 k_{n,l} / p^partial_{n,l}(0))`.

Under `j_n delta_n -> 0`, smooth dependence of the success prefactor and hyperbolic exponent gives, for every fixed compact \(K\),

`sup_{z in K} |p^partial_{n,l}(z)/p^partial_{n,l}(0)-1| -> 0`.

Consequently, for every fixed \(K\), the same cap sequence satisfies

`inf_{z in K} N_{n,l} p^partial_{n,l}(z) >= 2 k_{n,l}`

for all sufficiently large \(n\), and the cap-failure probability is exponentially small.  The compact set no longer changes the experiment.  This is the quantifier order used by the Gaussian and local minimax statements.

## R21-4. Define the observation sigma-field exactly

**Addressed in:** `article/18b_raw_physical_multirate_v22.tex`, `article/01b_observation_hierarchy.tex`, the abstract and introduction.

V22 separates four objects.

1. The **full raw collision history** of a preparation.
2. The **per-preparation endpoint/residual-time coarsening plus failure**, which is the record compared by the historical v6 transfer theorem.
3. The **complete stopped acquisition transcript at that declared coarsened record level**, retaining all designs, success/failure records and the stopping time; this is the object compared by the adaptive v16 theorem.
4. The **endpoint-output experiment**, a further Markov coarsening to which the Gaussian information/minimax theorem is attached.

V22 no longer calls item 2 or 3 the complete raw collision history.  The finite-to-boundary theorem explicitly says that no total-variation comparison of the full growing collision array is asserted.

## R21-5. Separate LAN, equivalence, experiment convergence and minimax

**Addressed in:** `article/18a_vector_boundary_information_v22.tex`.

The abstract boundary theorem is reorganized as follows.

- A Hellinger convention is fixed explicitly.
- The original moving-support family remains non-dominated at finite \(n\).
- A parameter-independent common-collar map produces the dominated representative.
- The null censoring atom is explicitly shown to have positive mass.
- Both the forward and reverse comparison kernels are explicitly parameter independent.
- Uniform LAN is asserted only for the dominated representative.
- Asymptotic equivalence transfers local conclusions to the original experiment.
- A separate bounded-sequence lemma proves mutual contiguity.
- Finite local subexperiments are stated to converge in Le Cam distance to the Gaussian shift; this is not rhetorically identified with a separate global deficiency theorem for an uncountable compact parameter set.
- If the information matrix is singular, the Gaussian experiment is formulated on
  
  `H = Ran(J_Sigma)`
  
  with the Moore--Penrose inverse/projection used for estimation and the minimax theorem stated on the identifiable space.
- The central-sequence estimator is explicitly described as a local reference-model statistic.

This keeps the non-dominated finite-sample structure and all local Gaussian conclusions simultaneously explicit.

## R21-6. Strengthen the conceptual consequence at the top-four target

**Addressed by a new theorem:** `article/23b_multichannel_rigidity_v22.tex`.

V22 adds **Finite-channel analytic table rigidity**.  For a periodic table with finitely many labelled connected real-analytic strictly convex obstacle boundaries, take a finite registered channel cover meeting every obstacle label.  If the onset and the two same-type signed endpoint-law germs agree for every channel in that cover, then the complete labelled obstacle boundary images agree in the fixed fundamental cell; hence the two labelled tables are identical.  Without an absolute laboratory placement, fixing one initial oriented contact frame leaves one common Euclidean motion.

The proof uses the v22 all-order signed inverse at each measured channel, analytic continuation of the recovered boundary germ along the connected analytic obstacle, uniqueness of the planar Frenet equations, and the spanning property of the channel cover.  This is a table-level geometric consequence, not a restatement of local jet recovery.

The manuscript continues to distinguish this data set from marked/enriched length spectra.  No dominance relation between the observation schemes is claimed.

## R21-7. Produce a real canonical build

**Workflow added:** `.github/workflows/a2-v22-native-build.yml`.

A native-build workflow is attached to the exact v22 revision branch and checks out the exact head, installs a native TeX toolchain, runs the repository submission builder and boundary diagnostics, rejects unresolved references/fatal TeX diagnostics, and records source/PDF hashes on success.

For the canonical manuscript-source commit `82a19b18f35fee63819bcc99d530f52adf56c384`, GitHub created workflow run `34595965653`.  The automatic attempt failed before any runner step was executed: job `103251658435` returned `failure` with `steps = null`.  We explicitly reran the job.  The second job `103251787513` again returned `failure` with `steps = null`.  Thus there is still **no native-build certificate**, but equally there is no executed LaTeX failure to report.  V22 records this limitation exactly rather than treating a zero-step infrastructure failure as either a pass or a manuscript error.

## Smaller comments

The revision also implements the smaller points that affect the active theorem chain.

- The parity convention appears at the first same-type physical design.
- The Hellinger convention is fixed.
- Positivity of the null censoring atom and parameter-independence of the reverse kernel are explicit.
- Bounded local contiguity has its own lemma.
- Singular information uses the identifiable subspace and pseudoinverse.
- Fixed laboratory-time differentiation is separated from channel-centered action differentiation; the residual gap dependence of \(S_b\) is displayed as an \(O(\delta_n/j_n)\) support remainder.
- The finite positive design is stated to depend in general on the finite jet order and reference geometry.
- The anchored realization chooses the statistical patch strictly inside the plateau where the cutoff equals one.
- If two contact perturbations lie on the same connected obstacle, global embeddedness is explicitly preserved after shrinking the parameter ball.
- Analytic continuation is stated as equality of registered boundary images, not as noisy global stability.
- The active introduction and main source identify the logical theorem chain directly, without requiring version manifests to infer which results are active.

## Summary of the new architecture

The v22 manuscript retains the v21 non-dominated statistical repair and registered fixed-window model, but strengthens the paper in two directions.  First, the determinant-one all-order inverse now has a full weighted-operator/envelope/homogeneous-degree proof rather than a compressed induction.  Second, the local analytic inverse is assembled into a finite-channel table-rigidity theorem.  The physical theorem simultaneously fixes itinerary parity, cap quantifiers, observation sigma-fields and the hierarchy of LAN/Le Cam/minimax statements.

No substantive v21 theorem has been removed merely to obtain a favorable report.  The remaining submission-readiness blocker is external to the executed mathematics: the repository's GitHub Actions runner has still not executed a single step of the exact-head native-build job.
