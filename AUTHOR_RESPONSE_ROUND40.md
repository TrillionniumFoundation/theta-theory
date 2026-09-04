# Author response to Round 40

**Controlling report:** `REFEREE_REPORT_ROUND40_GPT56_PRO_HARSH.md`  
**Reviewed head:** `1144f2c08a9dee66b6cc12b3bcc35252a054160b`  
**Revision entry point:** `ROUND41_REVISION.tex`

The revision strengthens the two response-identification theorems while
preserving their full positive claims.  The finite model now has a genuinely
uniform horizon-dependent policy class; the infinite model now has a valid
compact-class likelihood proof and a quantitative posterior rate theorem.

| Referee item | Revision | Mathematical closure |
|---|---|---|
| R40-M1/M2 | `round41/lattice.tex`, Lemma `lem:prefix-window-count` and Proposition `prop:balanced-contrast` | Replaces asymptotic density by `N_cal(m) >= rho m-C_cal` for every prefix; proves `W_n >= rho n/6-C_win` and carries the constant through the predictable contrast and Azuma/net argument. |
| R40-M3 | `round41/lattice.tex` | Declares one common exploitation force bound `U` and uses `max(a,U)` in all Duhamel derivative bounds. |
| R40-M4/M9 | `round41/lattice.tex`, `round41/filter_memory.tex` | Declares common `tau_min,tau_max`; sets `underline tau=min(tau,tau_min)` and proves `t_i >= i underline tau` in nuisance and filter estimates. |
| R40-M5 | `round41/lattice.tex` | Makes the duration `F_{i-1}`-measurable before the fresh sign and conditions the sign-square identity on `F_{i-1}`. |
| R40-M6 | `round41/infinite_jacobi.tex` | Declares the compact box `0<c_-<c_+`, `0<a_-<a_+`, `2a_+<b_-<b_+`. |
| R40-M7/M8 | `round41/appendix_uniformity.tex`, Lemma `lem:supnorm-response-slln` | Replaces the invalid `L^2`-net/uncountable-Doob step by a finite `C([0,T])` sup-norm net.  One empirical first moment `n^{-1} sum |xi_i|` controls every member of a net ball; the square field uses `|f^2-g^2| <= 2B||f-g||_infty`. |
| R40-M10 | `round41/filter_memory.tex`, Lemma `lem:strong-pushforward` | Introduces deterministic separable jet-dual spaces `E_j^0`, proves Bochner measurability there, uses a fixed countable dense parameter set for suprema, and displays the polynomial dependence on `L^1`/TV derivative norms. |
| Significance | `round41/introduction.tex`; Proposition `prop:jacobi-response-geometry`; Theorem `thm:jacobi-rate` | Unifies both models through response geometry and strengthens infinite-Jacobi consistency to a full posterior large-deviation principle with matching open/closed bounds, plus true-value-uniform finite-cylinder stability through `kappa_J(delta)` and `Omega_J(r)`.  Adds Vollmer (2013) and de Hoop et al. (2023). |
| Article focus | `round41/preparations.tex` and wrapper | Removes repository manifests, CI descriptions, SHA records, and review-governance prose from the mathematical article; they remain only in this reviewer packet. |

## New positive theorem

Let `I_beta0(beta)=(a^2/(2 sigma^2))D(beta,beta0)`.  For every Borel set
`A` in the complete compact Jacobi product, the exact posterior satisfies

`-inf_{A interior} I_beta0 <= liminf n^{-1} log Pi_n(A)`

and

`limsup n^{-1} log Pi_n(A) <= -inf_{closure A} I_beta0`

almost surely.  The denominator is proved to have exact exponential rate
zero, so the open lower and closed upper bounds match.  The pairwise modulus
`kappa_J(delta)` is now minimized over all parameter pairs in the compact box,
not only around one fixed truth, and `Omega_J(r) -> 0` gives an explicit
variational inverse-stability inequality.  Strong product-topology consistency
is a strict corollary of this full large-deviation theorem.

## Verification boundary

The executable checks cover source invariants, exact finite jet algebra, the
Vandermonde determinant, the finite Schur identity, source hashes, and the
LaTeX build.  The new martingale and Banach-space arguments are mathematical
proofs in the article, not claims of proof-assistant verification.
