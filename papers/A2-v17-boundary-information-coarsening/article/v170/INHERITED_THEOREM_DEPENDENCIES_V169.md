# A2 v169 — proof dependencies

## Main reading route in Paper II

1. `prop:incidence-content-v169` and the preserved `thm:determinantal-v167`: the natural evaluation map, its fixed-degree Hilbert immersion, and the classical Rees graph lemma identify the retained-coefficient graph. The new content lemma distinguishes an invertible divisorial factor from a projective graph point. These are infrastructure, not the main new geometric classification.
2. `thm:chain-model-v169`: the one-entry-per-column structure gives the row-ideal product and its all-order factorization. `prop:rees-v169` proves the integral semigroup inequalities, normality of every Rees degree, and the exceptional valuation rays. It implies the smooth chain model and its independence of Hilbert embedding degree on this marked family.
3. `prop:curve-charts-v169`: explicit low-degree equations, monic Buchberger reductions, source-infinity checks, and fixed-target overlaps give the flat universal curve. This does not depend on numerical experiments or an assumed classification of the full B_a fibre.
4. `thm:arc-table-v169`: substitute the chart limits of a DVR arc to obtain all 2a+1 wall/chamber families. The order of b plus one gives the sharp family coefficient-jet bound. Residue parameters are retained.
5. The associated-point calculation and `thm:genus-correction-v169`: dehomogenize on F, G, R, remove only the punctual torsion when explicitly discussing the pure curve, and identify the torsion module of the full Hilbert limit. The full ideal is never replaced by its radical. The last wall produces the cuspidal tail and the nilradical power formula. The a=3 specialization gives seven complete embedded curves and a length-one punctual contribution in the last three cases.
6. `thm:global-gluing-v169`: actual source changes, pivot normalization, and target undo matrices glue A^2 x Gamma_a charts of the fixed-degree projective coefficient graph. The proof is independent of the chain's choice of coordinates and retains the chosen fixed-degree problem. It does not glue different generic Hilbert-polynomial functors into an asserted all-pencil moduli space.
7. The fixed-source Quot comparison contracts the marked exceptional chain; the Hilbert graph separates it. The unbounded punctual-nilpotence consequence is an application to Hilbert limits of smooth rational curves independent of Paper I.
8. Only the final effective-family application invokes Paper I and the inherited fixed-target contact comparison. No earlier result in this reading route requires reconstructing a failure algebra.

Consult `THEOREM_INDEX_V169.json` for exact compiled labels/numbers/pages and `REFEREE_CROSSWALK_V169.md` for locators for both sets of 66 requests. The index is generated from the actual compiled auxiliary files; prose locators are not a replacement for that index.

## Preservation and publication units

Paper I retains its full sharp-inverse mathematical body. It is a logically separate reconstruction paper, not an appendix needed to prove the rational-curve results above. Paper II presents the new chain/content/genus/gluing route first. Its former main sections and former appendices follow intact as supporting appendices. The preservation master contains both paper bodies exactly once and is an audit object, not a third submission.

All 423 predecessor mathematical blocks and 625 predecessor master labels are checked. The check uses complete theorem/lemma/proposition/corollary/remark/example/definition/proof environments, not only environment counts. Complete predecessor source hashes are locked. Mathematical validity still requires reading the written proofs; byte retention and test success do not establish it.

## Explicit nondependencies / uncompleted classifications

No proof assumes a complete component, normalization, or associated-prime classification of the full fibre of Gamma_a over B_a for a >= 3. No proof assumes an all-higher-corank or all-Kronecker Hilbert-boundary theorem, an internal boundary operation on an isolated raw algebra, a globally minimal fan for arbitrary coefficient presentations, or an external proof audit of the sharp inverse. These are distinguished in both referee responses rather than silently promoted to hypotheses already discharged.
