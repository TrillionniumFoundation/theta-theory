# Response to the external referee: A2-DYN revision 56

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v55-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `38cfd6796d9146b9dcf30fb2f614731801edb53c` / `304f5b638c0cb2d61d934bbb864d48ea43039f90`.  
**Reviewed author commit:** `32866de446dd83c3036c04544ce4da66b019a990`.  
**Frozen complete author paper tree:** `752682f2cc874aafa60c2e59581cc0e29ddccd89`.  
**New article:** `papers/A2-DYN-v56-referee-response/main.tex`.

We thank the referee for the detailed audit of the cap-free endpoint argument and for insisting on the distinction between finite integral norms and essential height. This revision keeps the original physical record, exact indices, title, arithmetic transition kernel and full two-sided pointwise endpoint. It adds a maximal localization theorem for the same two positive physical sources, followed by raw and conditional laws uniform over every interval containing the same good roof. It does not label the remaining unrestricted height estimate as proved.

## 1. Positive incidence height

New module `119_maximal_physical_layers.tex` proves a finite-count estimate for the uncentered roof maximal function of the original positive physical remainder. For any fixed mother window of length h, the bad set has length at most

`C(1+h) min{epsilon^(1/16)/lambda, lambda^(-145/144)}`.

Outside this one open set, the incidence density is at most lambda almost everywhere and its average over **every** positive-length subinterval containing a good anchor is at most lambda. This is simultaneous over arbitrary bounded source insertions by the original disintegration and positive domination. The set is not chosen separately for an insertion or interval.

The actual normalized source mass of the set is at most

`C(1+h) min{1,(epsilon^(1/16)/lambda)^(1/145)}`

at every finite count. The proof uses the weak endpoint only for this source-weight conversion. The maximal covering lemma itself is proved in full, so no new dynamical multiplier or source regularity assumption is imported.

This gives essential-height control off a quantitatively localized set. It does not control the height inside that set. The referee's unrestricted incidence-height requirement is therefore advanced in localization, but not completely discharged.

## 2. Positive clearance height

The same set is built from the **sum** of the two positive components and therefore controls clearance as well as incidence, including simultaneous arbitrary source insertions. It uses the unchanged first-physical-defect decomposition, not cancellation between two signed corrections. The clearance of flight j stays at collision j+1. No orbit is continued through a competing-hit seam.

The maximal Lq estimate also retains the exact finite-count exponent `9(145/144-q)` for `1<q<145/144`. Its new feature is that it controls the supremum over a continuum of interval resolutions, not just each fixed window separately. The unrestricted clearance essential height remains a separate geometric requirement.

## 3. Two-sided arithmetic raw theorem

The exact positive raw-error identity gives a sharper consequence than the finite-count weak-endpoint conversion. At fixed reconstruction band B, take `epsilon(B)=A0 B^(-1/12)` and density threshold `lambda_B=B^(-1/384)`. The open exceptional set has length `O(B^(-1/384))` uniformly in every finite collision count. After the collision limsup, its **original source mass** has that same exponent, not the weaker exponent supplied by weak integrability alone. This uses `P=G+V_B+e_B` and the bounded controlled part `G+e_B` explicitly.

On the complement, all anchored interval averages of `|P-G|` and the almost-everywhere pointwise error are `O(B^(-1/384))` in the ordered limit. The interval lengths have no lower bound and may depend on the collision count. No fixed-window theorem is differentiated after an asymptotic substitution: the maximal inequality is finite before the count limit.

The complete two-sided pointwise theorem on **all** central roofs is not declared proved. The open set may contain a thin positive spike. Its possible nonemptiness is precisely the remaining distinction from the full positive-height criterion. The proof and finite negative controls explicitly retain that distinction.

## 4. Same-roof bridges and arbitrary interval resolution

New module `120_resolution_uniform_roof_laws.tex` applies the same physical envelope to the common positive path-valued remainder. The existing bounded-Lipschitz-dual positive-error representation gives one set, independent of all path tests, on whose complement the collision-path raw law holds uniformly over every anchored interval. At good roofs with a positive pointwise arithmetic floor, the same-roof collision bridge is uniformly close to its Gaussian reference.

For an anchored interval J with average positive reference at least d, the original conditional denominator is at least `(d-r)|J|`, where r is the raw maximal error. The probability total-variation roof error is at most `r/(d-r)` and the joint roof/path-test and conditional-mean path errors are at most `2r/(d-r)`. These hold for arbitrarily short J, without a prescribed slow resolution. The source is the complete original exact-label source.

The actual-return bridge is handled separately. Its already proved integrated clock-transfer error produces a common maximal exceptional set for both bridges, with an explicit modulus in that error but no asserted count rate. We do not assign the collision-envelope band exponent to a return-clock estimate which has no such rate.

The simultaneous family of deterministic conditional laws is not misidentified with conditioning on the output of an adaptive interval-selection procedure. Such a procedure can carry an additional selection event. Likewise, bounded-Lipschitz path tests are not path-space total variation.

## 5. Arithmetic endpoint

The full transition kernel remains in every main term through parameter transitions; the fixed-radius factor is not replaced by one. Conditional roof references use `G_+` with a positive integrated denominator. A forward likelihood is used only under a pointwise floor `G>=d`; its essential bound in this revision is restricted to the same good roofs, not the entire window. Zero arithmetic classes are not assigned a likelihood.

## 6. Independent specialist verification

No independent human specialist audit has been obtained. The new interval-covering, source-weight and normalization arguments are self-contained and author-checked. Their billiard application still depends on the frozen continuum inputs identified in `SPECIALIST_AUDIT_MAP.md`: the exact guard decomposition, local finite-count physical mass, protected geometry, occupation spectrum, arithmetic kernel and common path disintegration. Source hashes, finite models and typesetting are not certificates for those inputs.

## 7. Generality

The two real-variable lemmas are stated independently of billiards and have complete proofs. The added conclusion is a maximal, resolution-uniform consequence of the existing physical source estimates. It is not claimed as a newly discovered maximal inequality, a second singular-hyperbolic realization or a proof of broad dynamical universality. The original concrete problem remains unchanged.

## 8. Manuscript architecture and preservation

The two new modules sit immediately after the cap-free and endpoint-modular pair. They form a short direct route: finite positive mass -> one maximal roof envelope -> original-source exceptional mass -> all-resolution raw/path laws -> exact normalization. The first principal theorem is extended rather than adding another leading theorem hierarchy. All 118 inherited core modules, 155 inherited Python scripts, bibliography and compiled appendices remain byte-identical. All inherited mathematical labels remain. The former main source and metadata are archived under `provenance/v55-*`.

The article retains the full original raw-return program and does not replace it with a different paper or discard valid derivations. The burden of closing height inside the exceptional sets remains stated explicitly.

## 9. Prior-art comparison

The maximal interval argument is classical real-variable analysis, proved here to expose constants and quantifiers. It is not advertised as a new spectral method. The Lorentz-process LLT of Szasz--Varju, the endpoint local limits for deformed billiards of Demers--Pene--Zhang, and the suspension-flow LLT of Dolgopyat--Nandori remain the comparison theorems. Their role is recorded in the retained literature section. The new consequence uses the particular exact-label positive remainder and arithmetic transition kernel already constructed here; no existing interval theorem is differentiated into an unproved raw density height estimate.

The difference from the earlier almost-full roof-set corollary is exact: that corollary controls the conditional kernel at most roofs, whereas the new good anchor simultaneously controls all surrounding intervals of arbitrarily small length. This distinction is demonstrated by the finite interval tests and does not constitute a claim of historical priority.

## Technical comments 1--20

The auxiliary spectral band, reconstruction band, protection width, density threshold and interval length remain separate. Every maximal mass inequality is finite in m; the sharper original-source estimate explicitly uses a collision limsup at fixed B. Exact-label disjointness and the factor 1/c remain in the inherited source proof. The half-open occupation and next-collision clearance conventions are restated. The exponent 145/144 remains weak, q is strictly subcritical, and beta>1 remains in the inherited endpoint modular. No essential-height conclusion is inferred from modular convergence.

The mother window is fixed, but the new subinterval theorem genuinely takes a simultaneous supremum over all positive lengths on the same good set. No count rate is assigned to the qualitative diagonal. Constants depend on h, q or the arithmetic floor where stated. Path dual norm, path variation, roof variation mass and probability TV are distinguished. The positive-part reference handles signed finite-count G for interval posteriors; forward likelihood requires a pointwise floor. All source qualification and finite checks retain their non-certification status.

## Qualification

The frozen v55 response run is `37893598233`, artifact `11599656339`, archive SHA-256 `d5b739ab291f47c0cc66801e7db86bbd7cba4fe9648f72299bd34be1db67466c`. This identifies the baseline, not the new run. Revision 56 has its own read-only exact-SHA workflow, ordinary-source Merkle checks, normal/optimized finite diagnostics, complete native TeX build and theorem-label-based renders. Successful new execution is recorded only in the observed run and its dynamic receipt.
