# Dependency ledger, A2 revision 66

The current entry theorem is `thm:v66-main` in `article/00g_contact_synthesis_v66.tex`. It is a summary, not an additional proof claim. Both `rigidity.tex` and `main.tex` include the complete proofs.

| Conclusion | Proof | Inputs | Observation/quantitative boundary |
|---|---|---|---|
| Actual quadratic Schur identity and converse | `lem:v66-riccati` | v65 signed Jacobi coordinates, positive half-line construction | Fixed polygon; positive curvature; actual decaying solution |
| Global curvature inverse, image, iteration, data-dependent stability | `thm:v66-curvature` | Schur identity, positive-orthant contraction | Fixed positive flight coefficients; image is not the whole positive orthant; no grazing uniformity |
| Exact finite-jet and analytic-germ identification without nearby candidates | `thm:v66-global-rigidity` | Global curvature inverse; v65 actual smooth-jet factorization and signed recursion; two-offset extraction | Marks and shared two-offset amplitudes supplied; smooth jets are not smooth germs |
| Exact entire labelled obstacle images | Same theorem | Analytic germ identity and continuation | Fixed lattice and placement; connected closed embedded analytic boundaries; every labelled obstacle visited |
| Fixed-order finite-flight inverse | `prop:v66-finite-flight` | v64 relative physical law, stable extraction, global quadratic inverse and finite recursion | Compact positive classes, fixed order, density error; no sampling budget |
| Complete analytic norm inverse | Retained `thm:v65-analytic-inverse` | Actual holomorphic graph half-lines; finite low-degree system and contracted tail | Local neighborhood and small fixed analytic disc; not implied by global coefficient uniqueness |
| Conditional real-law stability | Retained `thm:v65-real-stability` | Larger-disc analytic prior, real-to-disc estimate, smaller-disc complete inverse | Local prior and radius loss remain |
| Weaker-data alternating, unknown-lattice, nuisance and preparation results | All existing active sections and v65 ledger | Unchanged proofs and model-specific assumptions | No implication from the supplied-polygon model erases their separate hypotheses |

Historical local exact uniqueness clauses remain true, and the new global theorem explicitly strengthens them. Their local norm estimates are not restated as global. All 131 inherited active inputs remain; three new common inputs give 134 distinct paths (123 full, 55 principal, one companion).
