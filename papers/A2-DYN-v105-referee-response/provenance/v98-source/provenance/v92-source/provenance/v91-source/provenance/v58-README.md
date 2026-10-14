# A2-DYN revision 58

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The author baseline is v57 at `8dbfac97a74e2b498c77d1afd663dd1e7db18c91`; the controlling external review is `4ffcf6bea86fabad719e8d893e4ae43bbb56da26`, report blob `8293a37ac814e4028d0af8e831102d77d245c69e`. Both new branches start from that review commit.

The new modules are `123_flat_pressure_contact.tex` and `124_common_gaussian_arithmetic_law.tex`. All 122 old core files, 163 inherited Python files, old compiled appendices and the bibliography are byte-identical. The prior front matter remains compiled under `appendices/v57_frontmatter.tex`; its full main source and eleven supporting files remain under provenance.

## New mathematics

The positive pressure and a visible branch have the same Hessian at zero damping. Keeping this contact gives `|mu_j-mu_R|^2=o(kappa_j)`, with an explicit bound in the Hessian mismatch and a cubic remainder. Thus peaks surviving at `m*kappa_j=O(1)` do not keep separate Gaussian centers. The complete transition kernel has one physical-mean Gaussian shape uniformly through arithmetic changes, while every finite phase, damping and residue stays in its scalar coefficient.

The original untruncated fixed-return law is then asymptotic in total variation to `n^(-2) alpha_{m,R}(k,n,u) g_{D_R}(V)`, uniformly in the radius. This is the physical return covariance, not a moving complex covariance. The positive-part normalized reference carries the same graph-coupled bridges and exact full-output selection theorem. A three-strip deterministic baker map provides a separately verified singular-hyperbolic realization of the scalar contact theorem; no continuous density theorem is asserted for its finite-support observable.

## Verification

Run `bash papers/A2-DYN-v58-referee-response/build.sh` in a complete checkout. The workflow `.github/workflows/a2-dyn-v58-qualification.yml` checks the exact source tree and report hashes, compares normal and optimized diagnostics, compiles the entire article, renders theorem pages and emits a dynamic exact-SHA receipt. The source archive includes the frozen baselines and controlling report.

The original incidence and clearance essential-height estimates, unrestricted two-sided pointwise law, unrestricted same-roof bridge and independent human specialist review are not claimed complete. The reference simplification does not remove a positive physical boundary source.
