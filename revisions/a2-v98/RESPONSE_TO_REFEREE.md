# A2 revision 98 — response to the v97 referee report

## Controlling sources and revision destination

The controlling report is `reviews/a2-v97-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`, on `review/a2-v97-independent-harsh-top4-2026-09-20`, at review commit **3b1f657871936a8807f0b3a3b6e86fd75851c9f8**. Its report blob is `56e59974b88339f2e5754510fe550c5860c56ba0`. The reviewed manuscript commit is **5c8b57c655aaec0df76dc3178554de2d1736b076**, not a moving branch tip.

The new branch is **revision/a2-v98-relative-spectral-atlas-proof-2026-09-20**, created from that review commit. The manuscript source commit is **b5691d8d3cc6a62295bfb8b2578be024b5e0c423**. The accompanying validation commit adds this response, scripts, exact records and a branch-scoped workflow without changing that manuscript source.

The principal article is *Projective polynomial observations: joint spectral atlases and a weight-wall transition*. Its entrypoint is `papers/A2-v17-boundary-information-coarsening/rigidity_v98.tex`. The standalone article has 26 pages in the local native build. The discussion below identifies source labels as well as the current numbering, so its references survive pagination changes.

## Route and mathematical changes

We take the report's **Route A**: retain the general finite real spectral atlas and supply its relative and uniform arguments as separate theorem-level statements. The full-rank multiplicity theorem is not substituted for the general theorem, and the cubic calculation is not substituted for the relative construction.

The principal dependency graph is now:

finite generic algebraic certificate -> relative real proper cover -> scalar orders -> fibrewise joint initial set -> semialgebraic Hausdorff error -> compact-uniform power law.

The explicit experiment then supplies the independent quantitative graph:

normalizer recovery -> approximate affine pencil -> robust cubic isolation -> coefficient and stochastic inverse -> complete local Fisher fibre -> exact remote corner -> positive constrained entrance distance.

The remote corner yields a genuine strengthening: the entrance law is now

`d_rem(delta) = mu_E delta + O(delta^2)`, with `mu_E > 0`.

The earlier `O(delta^(3/2))` conclusion follows from this stronger estimate. The improvement is specific to the simple/double cluster pattern at the remote point. It is not asserted for the base triple-root coefficient expansion or for arbitrary singularities.

## Point-by-point response

“Supplied” below means that the stated argument is in the revision for independent scrutiny. It does not mean that a referee or proof assistant has certified the theorem.

| Referee request | Revised location | Response |
|---|---|---|
| 1. A theorem-level relative principalization/spreading argument | Lemma 3.3 `lem:spread`, Theorem 3.4 `lem:relative`, pp. 5–8 | The generic certificate, finite closed chain, spread inverse isomorphisms, relative smooth centres and divisor intersections, unit identities and zero flags are specified. Associated-graded generic freeness is used before asserting blow-up base change. Bad images are constructible and their closures are removed. The proof then recurses on exceptional and vertical base components with strict dimension descent. |
| 2. Separate relative orders, fibrewise joint sets, and uniform asymptotics | Theorems 3.4, 4.1, 4.3 and Proposition 4.2; `eq:closure-formula`, pp. 7–11 | The parameter is a free variable held fixed inside every closure quantifier. Labelled-root matching gives a first-order Hausdorff-distance formula. Finitely many polynomial supports give finitely many candidate positive decay orders. A positive continuous threshold selection supplies compact-uniformity. Hardt triviality supplies topological types only. |
| 3. Update the comparison to current Hà and include Theorem 9.9 | Introduction, Table 1 and bibliography, pp. 2–3 | The reference is arXiv:2602.18410v2, March 14, 2026. Theorems 5.8, 9.9 and 12.3 are distinguished by their actual hypotheses. Theorem 9.9 is acknowledged as a non-toric finite-candidate chamber principle. |
| 4. Delimit the additional invariant after granting scalar predecessors | Introduction and Theorem 4.4 `thm:atlas` | Scalar finite-max and chamber results are granted. The retained output is the simultaneous real coefficient relation, its root-multiset image and exact bottleneck diameter, with normalization, stochastic inequalities and remote-fibre entry accounted for. |
| 5. Quantitative cross-rank inverse, especially the second marginal and pencil reduction | Proposition 7.2 `prop:affine`, Lemmas 7.3 and 7.4, pp. 17–19 | The proof gives `W0 = 2 Kd/(pi beta0)`, an explicit approximate-pencil error, coefficient-neighbourhood radii, discriminant Lipschitz bounds and a depressed-cubic absorption threshold. The final coefficient-dual inversion recovers weights and channels. No lower margin for `abs(det U)`, `-B` or `-E` is used. |
| 6. Both directions of the remote tangent cone and uniform realizing arcs | Proposition 8.1 `prop:remote-cone`, Lemmas 8.2–8.3, pp. 22–24 | The feasible set itself is locally a Nash image of four nonnegative and seven free coordinates. Every normalized secant is accounted for, every cone vector has a feasible arc, both stochastic simplices and the active weight floor are included, and the component permutation introduces no extra directions. Exact cubic product identities give uniform second-order remainders. The cone is established before the inverse, avoiding circularity. |
| 7. Preserve the full multiplicity theorem with explicit scope | Theorem 6.2 `thm:mult-atlas`, pp. 13–16 | The complete v97 multiplicity module is byte-identical. The scope remains fixed degree, coprime components, strictly positive invertible channels, strict weights, at least `2d+1` exterior clocks, every endpoint/interior multiplicity pattern, and all closed-model competitors. |
| 8. Separate existence, effectiveness and executable evidence | Theorem 5.1 `thm:effective`, pp. 11–12; new exact script and record | The geometric construction and a direct elimination route are specified separately. The latter constructs the compact coefficient maximum by a quantified formula, isolates its algebraic branch, selects rational orders by finite tests, and then eliminates the joint/root/diameter formulas. No universal resolution or elimination implementation is claimed to have been run. The executable script checks finite identities and specified Fisher programs only. |
| 9. Exact-head principal/archive/complete build evidence | `scripts/audit_a2_v98.py`, `.github/workflows/a2-v98.yml`, `LOCAL_VALIDATION.json` | The principal native PDF is locally compiled and inspected. The workflow checks out the actual PR head rather than a synthetic merge, verifies source hashes and addition-only ancestry, builds the historical and new products, and binds PDF hashes and recorded TeX input graphs to that head. A workflow definition is not a successful run; a remote full-volume success claim requires its completed runtime receipt. |

## Details of the relative construction

The source graph is retained with all inequalities. On each basic closed piece, an inequality is lifted as `p = s^2`; its real projection is exactly that piece. Properness over compact parameter sets follows from the compact graph and bounded slack coordinates. Resolving only the largest algebraic component would be insufficient for some isolated real singular points. The construction therefore also resolves the successively singular closed loci and spreads their regular-locus inverse maps. Each retained real point lies in one of these regular differences and has a real lift. Subsequent smooth-centre blow-ups have nonempty real projective fibres.

The spreading lemma does not infer arbitrary-fibre compatibility from smooth functoriality. It spreads finitely many equations and identities, arranges flatness of the ambient and associated-graded algebras, and then obtains base change for all powers of the centre ideal and the Rees algebra. Smoothness, relative normal crossings, chart coverage and invertible units are separately retained after deleting constructible bad images. Zero-function and vertical phenomena on the deleted loci are recomputed, not assigned the generic flags. Finite algebraic label covers are restricted to their selected real Nash branches before descent and real-accessibility tests.

For uniform asymptotics, pointwise convergence is first proved for the entire rescaled observation ball by semialgebraic monotonicity and finite nets. The error function is then defined using all labelled root arrays and finite permutation matching. Its graph involves finitely many polynomial supports. Any nonzero vanishing algebraic branch has an order arising from a tie between two monomials, giving a finite positive candidate list. Choosing a smaller rational power and a continuous positive threshold gives the compact-uniform bound. The proof does not infer a power rate, an order list, or Nash regularity from topological homeomorphism type.

## Details of the inverse and the stronger wall law

The second-marginal coefficient matrix has a positive smallest nonzero singular value uniformly on a compact centre set. Its closeness forces every nearby competitor's second channel to be invertible with a specified bound. Monicity then converts the bounded linear-span representation into an affine-pencil representation with a degree-below-three error. Near the first pencil endpoint, root nonnegativity and the discriminant give opposite one-sided bounds. Near the triple-root endpoint, the perturbed cubic is depressed using its own quadratic coefficient; the real-rootedness inequality absorbs the apparent nonlinear displacement. Coefficient functionals dual to the two base polynomials complete the parameter inverse without using the first channel's determinant.

At the remote point, the exact polynomial chart is

`(z-u)((z-r-v_f/2)^2-x), (z-a-w)((z-b-v_h/2)^2-y)`.

Locally its active constraints are exactly `u,x,y,k >= 0`. The remaining root, channel and weight inequalities have strict margins. Putting all chart coordinates equal to `delta` times a bounded cone vector produces polynomial coefficients analytic in `delta`, even though the individual double-root splits are analytic in `sqrt(delta)`. Equations (8.7)–(8.8) display the quadratic and cubic terms explicitly. There is no order-`delta^(3/2)` coefficient term in this chart.

The direct positive-entrance argument evaluates a putative zero-score pencil motion at `0,r,b`. It forces the base pencil displacement to vanish and the remote displacement to be nonnegative. Differentiating the normalizer then demands `pi t_h + c_* k = -1`, which is impossible. The zero-score version gives cone coercivity. This establishes local inverse control and attainment of the entrance program without presupposing either one. The exact chart, not just its outer cone, supplies both bounds on `d_rem` with an `O(delta^2)` error.

The strict regimes below and above `lambda = mu_E`, the positive exact-fibre jump, the nonidentified-side square-root opening, and finiteness of the base local constant are retained. At the critical ray, the sign of the higher-order difference still decides membership; the closed ball includes equality. The geometric wall `B=0` has a different endpoint cone and is not relabelled as covered by the weight-wall theorem.

The centre-known risk corollary is also preserved under the original uniform condition `n_j/N -> w_j`. Its proof now uses the strict testing slack `2 c sqrt(2) <= 1/4`, rather than requiring an unassumed `O(1)` rounding rate for the sampling allocation. The stated risk constants and asymptotic remainder are unchanged.

## Historical derivations and preservation

The revision uses the complete v97 modules and the prior v96 normal-form derivation at commit `423a0e135c217d6dc42fc973d8da4ee13893e865`. In particular `article/v96/uniform_normal_form.tex` supplies the exact root-coordinate and radial-contraction argument for the whole-model leading set; `article/v96/paper.tex` records its dependence on the earlier finite-Newton, global normalization, clock, quotient and perturbation modules. The source-pinned v97 response was also read to retain the previous report dispositions and its explicit limitations on archive build evidence.

No historical source or report is edited or deleted. The new `model.tex`, `multiplicity.tex` and `preamble.tex` use the same Git blobs as v97. The new archival entrypoint imports the unchanged `rigidity_v97_complete.tex`, which includes the entire reviewed v97 article and its unchanged v96 historical volume. The new complete entrypoint prepends the v98 article to that archival volume. Thus preservation is not an assertion that obsolete statements have become active premises; it is an unchanged, inspectable historical companion.

## Validation and limits of the evidence

The local principal PDF was built with native latexmk/pdfLaTeX, with recorder output, at 26 pages. Its final log has no LaTeX warnings, undefined references or citations, or underfull/overfull box messages. All 26 pages were rendered; page montages and selected full-size theorem pages were inspected. This is layout inspection, not mathematical peer review.

The exact SymPy 1.14.0 script passed 11 named regression groups. These include the cubic discriminant, the remote factorization, the two exact second-order chart identities, depressed-cubic algebra, multiplicity witnesses and ordered-diameter inequalities for `m=2,...,12`, three base Fisher programs, and the remote 16-support calculation with a strictly positive exact squared entrance constant. All numerical interval assertions are rational power comparisons. The record is `EXACT_DIAGNOSTICS.json`.

The local working directory is a staging copy, not a full Git checkout. The unchanged historical source graph was not locally mounted, so the archival and complete PDFs have not been represented as locally compiled. `LOCAL_VALIDATION.json` records this distinction. The branch-scoped workflow builds those products from the actual repository and records the exact head, actual TeX input graphs and product hashes. Until a successful run and its receipt are inspected, no full-volume remote build success is claimed.

No proof assistant or universal symbolic elimination of the stochastic model was run. The general relative and uniform assertions are mathematical arguments supplied for the next independent referee. Finite exact checks support their specified examples and identities; they are not a certificate for the universal quantifiers.
