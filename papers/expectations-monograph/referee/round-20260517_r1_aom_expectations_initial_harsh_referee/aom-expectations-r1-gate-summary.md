# AoM expectations R1 gate summary

- Generated: 2026-05-17 Asia/Shanghai
- Manuscript: `main.tex`
- PDF: `main.pdf`
- Title: **A Unified First-Principles Theory of $\theta$-Expectations from Deterministic Billiards**
- Gate status: **FAIL**
- Recommendation: **Not submission ready; major structural rewrite required.**

## Compile QA

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: passed
- PDF pages: 243
- PDF SHA256: `f9c25c7e3455dd4cd85746352438125514936df8035d2d01d30dcc05c4c1004d`
- Undefined references/citations: 0
- Multiply defined labels: 0
- Overfull hboxes: 9
- Underfull hboxes/vboxes: 19 total
- LaTeX warnings: 1
- Package warnings: 1

## Blocking Checks

1. **Article-scope gate: fail.** The manuscript is 243 pages, with a 15,883-line source file and many theorem/appendix layers. It reads as a research monograph or programmatic proof ledger, not a submit-ready article.
2. **Core proof-audit gate: fail.** The paper claims to derive singular hyperbolicity, anisotropic transfer spaces, spectral gaps, suspension Dolgopyat resolvents, moving-singularity response, cell correctors, and viscosity homogenization from primitive billiard geometry. The local proof style is often a dependency ledger or high-level proof sketch rather than a fully checkable derivation at the claimed level.
3. **Primitive-input gate: fail.** The compact finite-response mechanical port is powerful enough to realize tailored cotangent feedback and potentials. This makes the non-convexity/subadditivity examples look engineered rather than forced by the billiard geometry.
4. **Representation-layer gate: fail.** The downstream nonlinear expectation, FBSDE, and Girsanov sections require extra smoothness, invertibility, and uniform ellipticity assumptions that are not integrated into the main degenerate HJB theorem.
5. **Presentation/package gate: fail.** The root `README.md` is still generic IMS/AOP template text, not a manuscript-specific build/readiness document. Log hygiene is not clean because of overfull/underfull boxes and warnings.

## Positive Checks

- Current source compiles locally.
- The title in the source and recompiled PDF now agree.
- The manuscript is explicit that probabilistic representations are downstream of the deterministic HJB derivation.
- The manuscript tries to avoid the common false shortcut of replacing a singular billiard by a smooth compact Anosov diffeomorphism.
- The theorem chain is at least internally labeled and has enough structure to support a targeted repair pass.

## Next Gate Conditions

The next revision should not aim merely to add more text. It should compress and refocus:

- choose one central theorem and one target venue;
- replace broad internal derivations with precise cited theorem inputs where possible;
- make every genuinely new singular-billiard/resolvent/response claim fully checkable;
- define the finite-response port as a concrete physical class rather than an all-purpose realization mechanism;
- add one worked billiard example where $D$ and $H$ can actually be inspected;
- clean compile layout and replace the generic template README with reproducibility instructions.

