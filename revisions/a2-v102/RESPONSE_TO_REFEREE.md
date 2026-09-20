# A2 revision 102 — response to the v101 referee report

**Controlling report:** `reviews/a2-v101-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md` at `9e7caa42cce40587828f7e8357c119e127a56805`.

**Reviewed source:** `d1654974140410eb356240d3121c5f36267a89d2`.

**Revision branch:** `revision/a2-v102-intrinsic-metric-contact-walls-2026-09-20`.

**New principal:** *Intrinsic metric data and cancellation laws for polynomial observations*, `papers/A2-v17-boundary-information-coarsening/article/v102/paper.tex`.

The referee identified a substantive gap between a finite representation of an already known quadratic form and an intrinsic information theorem, and asked for a family-level consequence of the contact construction. This revision supplies a canonical metric invariant, an exact probe-family theorem with a stated query model, an endpoint quotient classification, and a cancellation-uniform polynomial wall theorem. The old theorems and all their proofs are retained in the supporting and archival source graph. No acceptance or universal correctness verdict is inferred from the changes or from the diagnostic computations.

## R101.1 — what the scalar values actually are

Section 3.1 defines the retained quantities on the **observable model image**, using the coefficient inverse and analytic cluster factors. The central multiplicity and endpoint pattern is recovered from the exact centre law, up to the model's component permutation. The first two cluster coefficients determine sums and centered variances even when individual roots are not differentiable.

Equation (3.2) defines a model-dependent **variational oracle** over nearby observable laws. It is explicitly not an empirical scalar statistic, a physical intervention, or a sample-complexity claim. Proposition 3.2 proves equality with the retained/free quotient using actual feasible root alternatives and a whole-model localization argument. This law-space identification is not itself advertised as compression: the principal contribution addressing finite information is Theorem 3.3 and the quotient theorem below.

The preceding constrained-cost theorem remains available, with its original feasible alternatives and uniform error estimates; nothing is removed or reinterpreted as an operational measurement.

## R101.2 — exact sufficiency, necessity, and the invisible endpoint quotient

**Theorem 3.3:** for an arbitrary admissible matrix family Q, a ray family is sufficient exactly when the sampling kernel meets its secant set only at zero. For the full positive-definite class this is equivalent to the rank-one probe tensors spanning the symmetric matrices. The proof includes necessity, not only polarization sufficiency.

The theorem proves a worst-case lower bound of k(k+1)/2 exact ray values, including deterministic adaptive queries: a nonzero symmetric perturbation orthogonal to the actual queried directions preserves the entire adaptive transcript. It also proves realizability of every positive-definite quotient by changing the ambient observation tangent metric while keeping the binary model germ fixed.

The scope is deliberate and proved. The universal lower bound is for this variable-metric class, **not** asserted for the smaller fixed-Hellinger family. For the latter the exact secant-kernel criterion remains valid. On endpoint-free patterns the leading root fibre determines the quotient form through its radial gauge, so the lower bound concerns recovery of the actual fibre and not merely a chosen matrix representation. Corollary 3.4 gives stability for any sufficient family, in terms of its least singular value.

**Theorem 3.5:** with repeated interior roots and invisible endpoint sums, the intrinsic spectral datum is G_Q(x)=min_{z>=0}(x,z)^T Q(x,z), not Q. The theorem gives its finite active-face Schur-complement description and proves that equality of these functions is equivalent to equality of the decoded leading fibres. Example 3.6 exhibits distinct positive-definite matrices with the same fibre. This explicitly closes the injectivity issue noted in the report rather than concealing it in a lower-bound argument.

## R101.3 — classical order theory versus the added metric information

The introduction and Appendix A identify integral closure, normalized blow-ups, divisorial order tests, and real arc orders as the classical mechanism for the exponent. The cited Lejeune-Jalabert–Teissier text includes Risler's real-analytic treatment; the revision does not rename that machinery as a new valuative criterion.

**Theorem 2.2** defines the leading residual set E_rho in the original feasible real observation coordinates and proves that every positive-definite norm has the same entrance order. Its coefficient is the minimum of y^T H y over E_rho. The closed convex upward envelope of residual tensors is reconstructed exactly from all these coefficients by positive-definite separating functionals. It is thus a complete invariant of the leading coefficient as the observation metric varies, not an unspecified metric unit attached to a chosen resolution.

The proof treats unbounded residual sets, attainment of each metric minimum, separation by semidefinite functionals and approximation by definite ones, covariance under invertible residual changes, and local Lipschitz continuity in H. It neither asserts that this convex envelope recovers all nonconvex residual geometry nor claims that integral closure preserves it. Proposition 2.4 states the intrinsic real-arc order formula separately.

## R101.4 — canonical data, not a canonical divisor list

The invariant is the pair (rho,C_rho), defined before a resolution is chosen. Appendix A specifies a finite proper, surjective real monomial presentation, its compact corner sectors, the positive-time closure, nonvanishing units, and transverse real accessibility. Proposition A.1 shows that any such presentation computes the same exponent and all metric support values, hence the same envelope.

The list of coordinate divisors is explicitly presentation-dependent. No minimal canonical list of accessible real Rees valuations is asserted for arbitrary inequality-constrained germs. This is not left implicit: the canonical replacement is the tensor envelope, whose exact reconstruction and covariance are proved in Theorem 2.2.

## R101.5 — a new family-level polynomial wall classification

**Theorem 4.1** treats g_a(x)=sum a_i x^{n_i} with m<n_1<...<n_s and residual (x^m-delta,g_a(x)). With z=delta^(1/m), it proves the uniform relative estimate

    d_H(a,delta) = kappa_H |C(a,z)| (1 + O(z^(n_1-m))),
    C(a,z) = sum a_i z^(n_i),
    kappa_H^2 = h_22 - h_12^2/h_11.

The statement is a two-sided inequality even on C=0. Its proof localizes minimizers using the actual trial x=z and uses the exact divided-difference identity g_a(x)=C+(x^m-z^m)B_a(x,z), with B_a=O(z^(n_1-m)). The error is relative to the canceled residual itself; it is not an absolute generic-stratum remainder that loses control near a wall.

Consequences proved in the principal:

- the exact wall is C=0;
- every bounded semialgebraic coefficient path is classified by its first nonzero term after substitution into this exact finite polynomial, or by exact vanishing;
- Corollary 4.2 computes the entire residual tensor envelope on an opening arc;
- Corollary 4.3 proves the locally uniform two-term crossover and arbitrarily higher moving-parameter cancellations;
- Corollary 4.4 shows exactly when weighted leading valuations suffice and how residue cancellation changes both the exponent and exact wall membership;
- Theorem 4.5 realizes the whole family by strictly positive polynomial probability observations with a two-point central exact fibre and distinct polynomial targets, and derives the sharp Fisher-normalized Hellinger coefficient.

This general polynomial probability family extends the monomial-contact realization in v100. It is not misidentified with the cubic binary subfamily. The original cubic rank-loss inverse and both order-one identification walls remain unchanged. Remark 4.6 also preserves the exact equality-shell qualification: equality of nonzero leading distance and threshold terms does not decide membership by itself.

## R101.6 — a theorem-driven principal and full preservation

The principal has four sections and two appendices. Its proof order is the canonical metric envelope, the binary local quotient and exact information criterion, and the cancellation-uniform polynomial wall family. All three arguments are presented with proofs. It is not a new introductory wrapper around the earlier long article.

The source entrypoints are:

| Volume | Entrypoint | Content |
|---|---|---|
| Principal | rigidity_v102.tex | New self-contained article |
| Supporting | rigidity_v102_supporting.tex | Complete reviewed v101 article, unchanged |
| Archive | rigidity_v102_archive.tex | Complete reviewed v101 article plus its complete historical archive |
| Complete | rigidity_v102_complete.tex | New principal followed by the entire archive |

The supporting volume is not added twice to the complete volume: it is already part of the archive. All prior mathematical files, review files, and derivations are inherited from the controlling review commit. The build script enforces an addition-only diff against that commit. No existing source or other manuscript branch is edited.

## R101.7 — executed evidence and the remaining native-build distinction

The new principal was compiled locally by the native pdfLaTeX/latexmk toolchain, both through its self-contained source and its repository wrapper. The final principal has 13 pages. Its final log has no undefined references, unresolved citations, multiply-defined labels, overfull boxes, or underfull boxes. The PDF was rendered and visually checked. The exact principal source blob was read back from GitHub and matched the locally compiled bytes.

`LOCAL_VALIDATION.json` records the source and PDF hashes and the exact scope. `EXACT_DIAGNOSTICS.json` records executed rational score/profile checks for simple, repeated-interior, and mixed-endpoint binary patterns; probe ranks for k=1,...,8; endpoint active-face identities; 24 divided-difference identities; a moving cancellation example; the oblique metric coefficient; probability positivity; and 80-digit numerical local stationary checks. These finite checks are not substitutes for the universal proofs or certified global numerical optimization.

`scripts/build_a2_v102.py` and the branch-scoped workflow rebuild the principal, supporting, archive, and complete targets through the inherited literal TeX/PDF dependency walker. Source bytes are compared with the triggering commit, binary-only dependencies are explicitly identified and hashed, and all native logs are checked. A successful source-bound receipt, PDFs, and logs are published and committed only after success. The evidence commit is allowed to follow documentation-only additions without falsely claiming that it compiled its own self-referential commit hash.

**At preparation of this response, the full archival source graph has not been executed locally and no v102 full-graph remote success is claimed.** The durable `native/RUNTIME_RECEIPT.json`, when present with `status=native_passed`, is the full-build evidence. A workflow definition, a queued run, or an older v98 artifact is not such evidence. This part of R101.7 must be judged from the actual runtime receipt rather than from this response.

## Reading sequence for the next referee

Read Theorems 2.2, 3.3, 3.5, 4.1 and 4.5 with their proofs, then Corollaries 4.2–4.4 and Appendix A. Use the supporting volume for the unchanged full multiplicity, cubic, weighted-atlas and critical-shell proofs. The scientific novelty and journal-level significance remain matters for independent review; neither the response matrix nor the diagnostic suite claims to settle them.
