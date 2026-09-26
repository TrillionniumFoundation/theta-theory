# Response to the independent referee report on A2 v170

The controlling report is `reviews/a2-v170-independent-harsh-top4-2026-09-27/REFEREE_REPORT.md`, commit `35b33cd5b0eda133137c9baa7e2a1ef0591dc58b`, blob `94fe39b7a97b20324ac45aa6b38b43297e87ca01`. It reviews the complete v170 tip `b8c3c1d7e59591b4e402272773d9bed5ae7c88ba`. We have not relabelled an older report as a review of a later mathematical object.

## The changed mathematical route

The revised Paper II begins with an actual-ideal conductor identity for an arbitrary normal proper birational model of a smooth coefficient space, under an arbitrary finite flat dominant smooth coefficient cover, in any dimension. Its proof is classical trace duality applied to this geometric problem, with full prime tracking and no hidden codimension-two extension. A normalization-defect cycle and an associative conductor-divisor formula for towers follow.

The application is no longer limited to diagonal monomial coefficient covers. For `b=u^r, c=u+v^s`, all contact orders and all `r,s>=2` have explicit conductor coefficients and generic defects. For the square-tangency cover we compute the complete normal surface and scheme fibre in every contact order, starting with three exhaustive normalization charts and continuing by ordinary blow-ups of specified smooth points. Two divisors have the same values on `u,v` and different values on `u+v^2`; their separation depends on cancellation, not on a fan of the original monomial weights. Two normalization lifts of the same embedded Hilbert limit can have different local singularity types. Both are realized by actual projective coefficient arcs.

The diagonal full-fibre calculation is retained and rewritten as a self-contained application with expanded local proofs. The unramified chain, including the determinant row factorization, is proved within the new paper. The complete mathematical body of the preceding Paper II is in a fully typeset technical supplement. All 487 preceding mathematical blocks are retained in the archive, and Paper I's complete proofbody is unchanged. This reorganization preserves the research programme without asking the new central theorem to carry every historical development as a prerequisite.

The general conductor identity is not advertised as a new duality formalism. Its classical trace/different inputs are identified explicitly. The new detailed applications and their exact scope are separated from those inputs. Neither a publication strategy nor journal acceptance is inferred from compilation or from the calculations below.

## Detailed requests

### 1. Lock and state the exact object

The review entry identifies the controlling report and immutable predecessor. `BUILD_RECEIPT_V171.json` pins every final manuscript source and PDF by SHA-256, while the separate read-only qualification receipt binds the exact submitted `GITHUB_SHA`. Commit identifiers and build machinery are not part of the mathematical exposition. The archive master is not a third submission.

### 2. Make the chain model self-contained

`thm:chain-v171` and `prop:chain-factorization-v171` prove the marked Hilbert graph directly. The proof supplies the Hilbert polynomial, the regularity degree, the row ideals, their factorization, removal of principal content, the normal Rees argument and the exhaustive chain charts. It does not invoke a historical version label as an unpublished theorem. The earlier argument remains intact in the technical supplement.

### 3. Prove the raw-chart cover

`eq:chain-charts-v171` and `eq:chain-overlaps-v171` are derived from the actual blow-up fan. `eq:raw-first-v171`, `eq:raw-middle-v171` and `eq:raw-last-v171` are their finite-flat base changes, hence cover the whole diagonal pullback. `thm:square-tangency-v171` derives the three tangent raw rings from the same exhaustive cover before normalizing them. No merely birational replacement is being substituted for the graph.

### 4. Rewrite integrality

`thm:duality-conductor-v171` proves that every finite locally free pullback algebra injects into its generic algebra, the single field `k(X)`. This excludes vertical and embedded structure, rather than relying on the existence of a dense torus. The local complete-intersection and S2 assertions are proved separately by the finite flat complete-intersection base change and the depth formula.

### 5. State the precise semigroup and grading

`eq:semigroup-facets-v171` specifies the affine semigroup generators, all coordinate and degree inequalities and all compact-facet inequalities. Its group is proved to be the full three-dimensional lattice. `eq:normal-rees-all-degrees-v171` then identifies integral closure with cone saturation, preserving the degree coordinate. Clearing denominators is used to prove an integral monomial equation, not to identify saturation with membership in the original fixed-degree semigroup.

### 6. Separate the graph from the Rees presentation

`prop:chain-factorization-v171` distinguishes the raw Fitting ideal, its principal content and the content-free ideal. The maps `fQ^n -> b^(nC)fQ^n` and its diagonal counterpart are explicit graded isomorphisms, including their fraction-field interpretation. The exponents depend on Hilbert degree; the graph does not. The raw Smith length has not been reintroduced as an intrinsic graph invariant.

### 7. Promote the coordinate-ideal lemma

`lem:coordinate-ideal-v171` is now a standalone proof. It specifies the character lattice, the meaning of negative exponents, the two same-side cases, and the crossing-diagonal case with the separate low/high-ray inequalities. It identifies the actual coordinate ideal with a symbolic valuation-ideal intersection, proves reflexivity and applies the exact depth sequence to exclude zero-dimensional associated primes. The scheme fibre conclusion is not based on a cycle computation.

### 8. Write the local node ring

The fibre proof in `thm:diagonal-v171` uses exactness of cyclic invariants and the explicit invariant ring `k[x^Delta,y^Delta]/(x^Delta y^Delta)`, equivalently the fibre product of two polynomial rings over `k`. It obtains the completed ring `k[[X,Y]]/(XY)`. For the nonmonomial square-tangency family the ring is obtained directly as `B_1/(u,v)=k[e,z]/(ez)` in `eq:square-full-fibre-v171`.

### 9. Ordinary versus reflexive powers

The convention is stated at the beginning of `sec:duality-base-change-v171`. In the diagonal nilpotence proof, ordinary products satisfy the valuation inequalities; only an inclusion in the fibre ideal is used. Nonvanishing is checked at a component of maximal generic length. The tower theorem explicitly uses reflexive products and does not claim equality of ordinary tensor products.

### 10. Expand the conductor-depth lemma

Two proofs now serve different purposes. `lem:trace-lattice-v171` identifies the ordinary conductor as an actual submodule of the fraction field using the trace adjunction. `lem:normal-complementary-v171` tracks height-one primes through the finite map, using every maximal ideal of the semilocal DVR normalization. Separately, `lem:conductor-depth-v171` proves the S2 intersection statement using the exact sequence `0 -> A -> A+Az -> M -> 0` and the explicit depth inequality. No height-one prime downstairs is conflated with a branch upstairs.

### 11. Residue degree versus closed lifts

`thm:tangent-conductor-v171` proves there is exactly one divisor above each old exceptional divisor. An irreducible residue polynomial over `k(w)` and the fundamental equality `sum ef=rs` establish this, rather than assuming it. The text then distinguishes its residue field degree from the number of general closed lifts over an algebraically closed field. The same distinction is explicit in the diagonal application. Special closed residues are treated by actual charts, not by a generic root count.

### 12. Explain the asymmetric normality criterion

After `lem:conductor-depth-v171` the proof shows why all diagonal conductor coefficients vanish for `rho=1` and why the last is positive for `rho>1`. The asymmetry is attributed to the orientation of the marked ideal system `prod(b,c^j)`. It is not a symmetric assertion about arbitrary monomial covers of the plane.

### 13. Equal-power conductor overlaps

The last part of the diagonal conductor calculation states the first/intermediate generator `u^(d-1)` and the last generator `v^(a(d-1))`. On the last overlap their ratio is the unit `zeta^(d-1)` from `u=v^a zeta`; interior overlaps use the same character. The new square-tangency conductors are additionally computed as finite free sublattice conductors, with overlap ratio `c/e=z^2`, in `eq:square-chart-conductors-v171`.

### 14. Specify quotient types

The diagonal quotient convention orders the adjacent rays counterclockwise, extends the first to an oriented lattice basis and writes the second as `p r_1 + Delta t`. The type is `1/Delta(-p,1)`, with the basis and coordinate-exchange ambiguities explained. `ex:unequal-cover-v171` gives the concrete type `1/3(1,1)` and its cubic Veronese ring. `thm:square-tangency-v171` computes the two A1 completed local rings directly.

### 15. State the terminal category

`prop:chain-category-v171` specifies integral locally Noetherian tests, the dense inverse image of the coefficient torus, invertibility as nonzero fractional ideals, and all structural morphisms. The induced generic maps are retained, not replaced by an inappropriate identification of each test with the torus. On normal tests the lift to normalization is proved by a finite birational generic-section closure.

### 16. Proportional logarithmic claims

The diagonal logarithmic paragraph states why `K+boundary` is Cartier, why invariant divisors on the simplicial surface are Q-Cartier and how a toric resolution verifies log canonicity. It states expressly that this is a parameter-space assertion, not stable or semistable reduction of embedded curves. The new conductor theorem and its tower law do not rely on logarithmic terminology.

### 17. Strengthen arc realization

`cor:tangent-lost-labels-v171` gives two explicit arcs and verifies the defining equations. Generic base-point-freeness is checked on both source charts: when `s_0` is nonzero the second coordinate is nonzero; at `s_0=0` the first coordinate is nonzero. The regular and singular normalization lifts therefore correspond to genuine projective graph families, including source infinity.

### 18. Unequal-cover worked chart

`ex:unequal-cover-v171` works out `(a,rho,sigma)=(3,2,3)` at the first crossing. It gives the raw ring, the finite birational cubic Veronese normalization, all three relations, the extra integral generator, conductor `(u,v)B`, and complete fibre `k[w,theta]/(w^2)`. The full fibre has no embedded point at the quotient singularity. The generic fibre lengths are explicitly distinguished from the conductor orders.

### 19. Novelty comparison

The new introduction and `LITERATURE_AUDIT_V171.md` distinguish the complementary-module identity and the complete-intersection different theorem from their geometric application. They compare the semigroup/complete-ideal inputs with the specified portions of Huneke–Swanson and identify the relation to Jacobian containment in the conductor literature. The square-tangency model is compared by its actual nonmonomial rings and cancellation valuations, not by vocabulary. No new general duality formalism, exhaustive priority search or theorem-level Ballico 1993 comparison is claimed.

### 20. Proof versus tests

No count of checked parameter tuples is used as a proof in either publication paper. The exact script and receipts are auxiliary files. They test trace Gram matrices, resultant discriminants, chart overlaps, fibre quotients, conductor lattices and actual arcs. The general statements are supported by the written proofs and the attributed classical theorems; neither finite tests nor compilation certify those proofs.

### 21. Read-only qualification on the exact submitted SHA

The publication workflow and the final read-only submission workflow have different roles. The former materializes and publishes complete manuscripts. The latter is triggered on the actual submitted tip after publication, uses `contents: read`, copies the source tree to a temporary build directory, verifies the submitted source/PDF hashes, reruns the entire inherited chain and the new checks, and recompiles every paper and the archive. It compares regenerated standalone sources and extracted PDF text with the committed objects and publishes a receipt bearing the exact SHA without committing anything. The checkout is required to remain unchanged. A workflow check is not represented as an administratively enforced branch-protection rule; enforcement is not inferred from the API permissions or the check's name.

### 22. Keep the preservation master archival

The review entry presents two publication papers first. The preservation master is clearly marked as an optional repository archive, not a third submission or an object whose length is evidence for the main theorem. Every old mathematical block remains available. The technical supplement has a distinct role: it is the complete earlier development available for targeted verification, not a dependency of the new Paper II.

### 23. Historical front matter

The preceding front matters and disclosures are saved in separate archival source files. Paper I's introductory sequence of revision-by-revision boundary summaries is replaced by one invariant proof roadmap, a statement of characteristic hypotheses and logical independence, and a precise literature/audit limitation. Its 161 theorem/statement/proof blocks are unchanged. Paper II has fresh publication front matter and no commit identifiers or response scripts in its mathematical text.

### 24. Rebuild the active Paper II around one route

The active Paper II now runs from the conductor identity to the self-contained chain, the tangent-cover theorem, the complete square-tangency model, and the diagonal scheme-fibre proof. The previous 326 mathematical blocks are typeset intact in the technical supplement rather than silently omitted. This yields a substantially shorter independently readable main paper while preserving the full mathematical programme and every predecessor proof.

### 25. Response completeness is not theorem completeness

The 25-item response is an index, not a proof or a significance certificate. The general coefficient-change theorem is stated on all normal models under its hypotheses. The complete nonmonomial surface classification concerns the square-tangency family in all contact orders, not the entire B_a fibre. Higher-corank and singular-pencil full Hilbert classifications, an external independent audit of Paper I, and the missing complete Ballico comparison are not represented as accomplished by answering the report. The manuscript offers the new general identity and detailed nonmonomial theorems for substantive rereview.

## Additional editorial observations

The inverse theorem remains a logically separate assertion. Its main proof does not use the conductor theorem, and the conductor theorem does not use the inverse. The two papers therefore have separately readable introductions and separate proof routes. The status of the external independent Paper I audit is unchanged: it has not been obtained. The new front matter is a better audit entry, not a substitute for that audit.

The preceding scope has not been erased. It is retained in the technical supplement and master, while the new main theorem operates on arbitrary normal birational coefficient models and the new examples include tangent, rather than only transverse monomial, boundary divisors. The resulting increase in scope is identified exactly; no claim about all quadratic-pencil degenerations is inferred from a complete calculation of one family.
