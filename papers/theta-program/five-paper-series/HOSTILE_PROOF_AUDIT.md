# Hostile proof audit of the θ-Theory five-paper series

**Date:** 2026-08-28  
**Scope:** internal proof and dependency audit; θ-Theory only  
**External peer review:** not performed

## Audit rule

The audit asks whether a conclusion follows from the hypotheses actually stated
in the same paper or a named upstream interface.  A stronger result outside the
stated theorem scope is not treated as a missing lemma.  Conversely, a
conditional interface is not promoted to an actual system theorem.

## Round 1: dependency and scope

### Finding A1: stale blanket response imports

The older HJB draft imported moving-flow and regularity-budget labels that the
latest response audit did not export unconditionally.

**Repair:** the five-paper series uses only the P1--P5 interfaces in
`THEOREM_INTERFACE_MANIFEST.yaml`.  The old blanket label is forbidden by the
verifier.

### Finding A2: K2 and K3 were conflated

The old organization made filtering/game assumptions appear necessary for the
basic one-player HJB.

**Repair:** Paper III proves the K2-to-HJB/theta branch.  Paper IV is an
optional typed fan-out for filtering and games.

### Finding A3: stochastic representations were over-unified

A classical FBSDE, a controlled BSDE, a 2BSDE, and a PPDE were treated too
nearly as interchangeable outputs.

**Repair:** Paper V routes equations by generator type and forbids reverse use
of representation results.

## Round 2: mathematical typing and limiting arguments

### Finding B1: third-order response words lost regularity

Writing `RG1RG1RG1R` on one untyped space concealed three source losses.

**Repair:** Paper I now uses the explicit ladder

```text
X4 -> X3 -> X2 -> X1
```

for third-order words and `X5` for fourth-order Taylor remainders needed by
finite-DQ through third order.  Every reduced resolvent preserves its ladder
level.

### Finding B2: square roots of a partition of unity need not be smooth

The first common-space construction used `sqrt(chi_alpha)` without a
zero-order hypothesis.

**Repair:** Paper II uses a globally smooth quadratic partition

\[
\sum_\alpha\psi_\alpha^2=1
\]

and defines `J_a,R_a` with `psi_alpha`; hence `R_aJ_a=I` by an exact smooth
identity.

### Finding B3: qualitative uniform WIP was used as a full-scale rate

A qualitative frozen convergence theorem does not control the sum of errors
over a diverging number of blocks.

**Repair:** Paper III distinguishes:

```text
compatible WIP modulus or direct triangular characteristics -> full scale
qualitative uniform WIP only                                -> cofinal diagonal
```

The actual four-branch model uses bounded martingale triangular-array
characteristics, not an asserted rough Berry--Esseen exponent.

### Finding B4: filter Lipschitz continuity did not imply value collapse

A bound by `sum q^k` is finite but does not remove the initial reward's
dependence on the prior.

**Repair:** Paper IV requires a fast initial layer with a diverging number of
filter updates and vanishing slow duration.  The value difference is bounded by

\[
C_Tq^{\ell_\varepsilon}\|\nu-\nu'\|
+C\delta_\varepsilon^{\rm init}
+\operatorname{Err}_\varepsilon.
\]

The actual hidden-symbol model has exact one-step prediction forgetting and one
fast step has vanishing slow duration.

### Finding B5: calibrated diffusion sign depended on PDE convention

Taking `F_X` as a diffusion matrix is wrong if the upstream equation is written
with negative Hessian orientation.

**Repair:** Paper V fixes generator orientation before calibration, then sets

\[
\sigma^u(\sigma^u)^T=2F_X.
\]

The Paper-III convention `A=Sigma/2` is explicitly translated to
`sigma sigma^T=Sigma`.

## Round 3: formulas and exact interfaces

### Finding C1: suspension entry and exit transforms were oversimplified

The two incomplete roof segments generally give different entry and exit
operators.

**Repair:** `paper-II-pressure-diffusion/TECHNICAL_NOTE_RENEWAL.md` gives the
normative formula

\[
\widehat C
=H^{\rm cell}
+\mathcal O_{a,z}F
[(I-L_{a,z})^{-1}\mathcal I_{a,z}G].
\]

Only the reduced low-frequency resolvent is exported.

### Formula checks

The following algebraic checks were repeated independently inside the audit:

1. crossed-envelope interpolation gives
   \[
   \lambda_*=(B+D)/(A+B+C+D),\qquad
   \log\rho_*=(CD-AB)/(A+B+C+D);
   \]
2. for affine branch weights and inverse branches,
   \[
   \partial_a^kL_ah
   =\sum_i[kv_ir_i^{k-1}h^{(k-1)}(\psi_i)
          +w_ir_i^kh^{(k)}(\psi_i)];
   \]
3. implicit pressure differentiation gives
   \[
   \partial_a\Sigma_{ij}
   =\mathscr P_{a q_iq_j}/\bar\tau
    -\mathscr P_{q_iq_j}\partial_a\bar\tau/\bar\tau^2;
   \]
4. for Paper III's explicit port and `p=q=pi/2`,
   \[
   H(p+q)-H(p)-H(q)=4\delta>0;
   \]
5. the Bayes update satisfies the stated conservative bound
   `C_B=2g_+/g_-` in the declared TV convention;
6. the pure-saddle inequalities have the correct max--min orientation;
7. the calibrated Feynman--Kac source has the positive integral sign for the
   PDE `u_t+Lu+cu+r=0`.

## Structural verifier

`tools/verify_theta_five_paper_series.py` checks:

- all five manuscript, interface, and blocker files;
- 34 unique named exports and 20 named imports;
- producer uniqueness and acyclicity;
- forbidden old theorem labels;
- convention anchors and review boundaries;
- SHA-256 hashes for the inspected checkout.

The exact script bytes were reconstructed locally and passed Python byte-code
compilation.  At the time of this audit, the private branch was not exposed as
a complete local checkout to the execution container, so a full script run
against the Git tree is not claimed in this document.  A checkout or available
runner should execute the command before merge.

## Audit verdict

```yaml
internal_named_dependency_gaps: 0
known_circular_dependencies: 0
known_stale_blanket_imports_in_new_series: 0
hostile_findings_repaired: 6
actual_scoped_end_to_end_model: four_branch_moving_seam_symbolic_port
unrestricted_universal_CM2: REFUTED_NOT_REVIVED
external_peer_review: NOT_PERFORMED
mathematical_proof_certified: false
formal_credit: 0
```

The last three fields are deliberate.  This audit improves and checks the
internal proof draft; it is not an external correctness certificate.
