# Response to the complete-materialized A2 v153 report — revision 157

## Review object and revision basis

The controlling report is `reviews/a2-v153-materialized-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md` at `52ebb8183433ad398f61958219b2af809f721824`. It evaluates the complete 80-page v153 article, not the earlier incomplete source-lock shell. We use the complete, reproducible v155 manuscript at `54b3a37bb8349fbba089dd0b7cdaa2ba0aa74414`, whose master-source SHA-256 is `7169ee083430fab37e6ed353a18a499e38dc6c79cee164d89cb5c50936a98af7`, and retain all intervening proof repairs and mathematical extensions.

The new branch is `revision/a2-v157-universal-power-ideals-2026-09-25`. It descends from `07309cd8061a9dd48e98267477f482709e87db62`, preserving the v156 source-lock files as well. The two encoded v156 source parts at that commit fail strict base64 decoding: their concatenation has 35441 data characters, which is 1 modulo 4. No mathematical claim in this revision is inferred from the undecoded package. The complete v155 sources, rather than an unavailable v156 manuscript, are the locked mathematical input. This provenance issue is recorded here, not used as a significance argument.

We thank the referee for asking for a global connection between the divisor-fibre algebra and the native geometry of pencils. Revision 157 supplies a universal coefficient-ideal theorem, an identification of the entire simultaneous power graph with complete quadrics, and boundary-contact and resolved-pencil consequences. The general statements have written proofs; they are not extrapolated from exact examples.

## 1. A universal equality of ideals, before restriction to a pencil

**Location:** Paper II Section 3, Theorem 3.1 and Lemma 3.2. Stable labels: `thm:universal-power-v157`, `lem:bounded-row-v157`.

Let `B_(n,h)` be the determinant-power apolar algebra which is the entire quadratic coefficient section of the reciprocal normalization fibre. For a symmetric matrix A over any commutative complex algebra T, let `J_p(A)` be the ideal of the pth power of its degree-one element. We prove

`J_p(A) = I_q(A)^(h-s) I_(q+1)(A)^s`, where `p = hq+s`, `0 <= s < h`.

The equality holds for every `0 <= p <= nh`, with `I_0=T` and the second factor omitted when `s=0`. It holds on nonreduced and non-Noetherian bases, commutes with arbitrary base change, and glues for symmetric bundle maps with a line twist. In particular `J_(h(n-j)) = Fitt_j(coker A)^h` over every such base. This is not an equality only after taking radicals or integral closures.

The v155 proof established the Fitting equality along a pencil by discrete-valuation calculations. We do not extend that conclusion by testing geometric fibres. Instead, over the universal polynomial ring, the power coefficient span is the dual of the apolar degree-p quotient. Its multiplicity-free decomposition consists of even-row representations indexed by partitions of width at most h. The degree-p span of the balanced minor product has exactly these representations: a torus-weight bound gives one inclusion, and a principal-minor highest-weight vector together with determinantal balancing gives the other. The ideals are generated in degree p, so equality of these subspaces proves the polynomial identity, after which arbitrary substitution is legitimate.

The balancing lemma is explicitly attributed to Bruns–Conca, Lemma 2.5, and its classical De Concini–Eisenbud–Procesi context. The apolar character is attributed to Nagaoka–Wachi. The symmetric Cauchy decomposition is a classical input, not a newly claimed result. A nonreduced example over `C[e]/(e^3)` distinguishes the ideal theorem from a closed-point assertion. Another example explains why one cannot take unique ideal roots for `h>1`.

## 2. The whole power graph is a classical native compactification

**Location:** Paper II Section 4, Theorem 4.1 and Corollary 4.2. Labels: `thm:power-graph-v157`, `cor:native-strata-v157`.

Take the simultaneous graph closure of all powers `[ell_A^p]`, `1 <= p < nh`, over the nondegenerate open of `P(Sym^2 V)`. We prove that this graph is canonically isomorphic, as a scheme over that projective space, to the space of complete quadrics. No normalization has to be added to the graph. It is independent of h.

The scheme-level proof uses the Rees algebra of the product of base ideals. The universal ideal formula shows that this product is, up to an invertible ideal, `(I_2 ... I_(n-1))^(h^2)`. Its blow-up is the classical exterior-power graph. Thus the identification follows before any pointwise description. The smoothness, simple-normal-crossing boundary, flag description and congruence-orbit stratification are classical complete-quadric results, attributed to Vainsencher and Massarenti. Our assertion is their recovery from reciprocal multiplication, not a claim to have discovered those properties of complete quadrics.

For boundary divisors E_r of rank break r, the exact transform is

`J_p O_CQ = O_CQ(- sum_(r=1)^(n-1) max(p-hr,0) E_r)`.

The proof supplies Gaussian charts and checks every minor ideal on them. Division by these common factors extends every normalized power map. The relative associated-bundle construction works for arbitrary complex bases. We distinguish it from the graph closure of an individual restricted family, whose formation need not commute with nonflat base change.

The congruence orbits in this graph are indexed by subsets of `{1,...,n-1}`. Their codimensions, closures and flag data are described. This is a meaningful complete orbit stratification of the identified power graph under the native group. It is not advertised as a classification of all full cotangent `GL(E)` first-relation orbit closures.

## 3. Boundary contacts recover the spectral degeneration data

**Location:** Paper II Section 5, Theorem 5.1 and Example 5.2. Labels: `thm:contact-Segre-v157`, `ex:contact-profile-v157`.

Every regular pencil line lifts uniquely to complete quadrics. If D_r is its contact divisor with E_r and `0=e_1 <= ... <= e_n` are its local Smith exponents, then

`mult_x D_r = e_(r+1) - e_r`.

The supported contact divisors recover the whole Segre symbol. Conversely the power-zero lengths recover the contacts by the explicit second difference

`mult_x D_r = (v_(h(r+1)) - 2 v_(hr) + v_(h(r-1)))/h`.

This is a boundary-detection theorem for native pencil data, not the existence of a single common extreme limit. The proof uses the principalization formula, symmetric elimination over the completed local ring, and faithful flatness. A pair of germs reaching the same complete-flag point but with different contact orders makes the distinction between a boundary point and an arc explicit.

For singular pencils the universal theorem still detects normal rank and all Fitting schemes. It does not assert that Fitting ideals alone recover Kronecker minimal indices. The sharp unmarked inverse for every pencil, including singular pencils, remains unchanged in Paper I. The inherited fixed-spectrum full-orthogonal closure theorem is also retained, with its expression through power-zero divisors; it is not claimed again as a new orbit classification.

## 4. A projective parameter space carrying the actual failure family

**Location:** Paper II Section 6, Proposition 6.1. Label: `prop:pencil-compactification-v157`.

Over the open set of regular pencils avoiding the corank-at-least-two locus, the lifted pencil curves in complete quadrics have Hilbert polynomial `binom(n,2)m+1` for the exterior-power polarization. We take the normalized graph closure of this family in the pencil Grassmannian times the corresponding projective Hilbert scheme. The result is a normal projective native-equivariant parameter space, birational over the Grassmannian and unchanged on that open.

The universal Hilbert family is flat and remains scheme-theoretically incident with the underlying pencil. The proof of incidence uses flatness over the integral graph normalization, not only closed-point containment. All normalized power maps restrict to the family, for every h. Pulling back the already constructed finite locally free failure algebra preserves its original multiplication. Thus the compactification carries actual failure algebras and resolved member curves together.

This is an equivariant incidence compactification, not a proper quotient stack or a universal ordinary algebra on a coarse quotient. We do not classify every extra or nonreduced component in a limiting Hilbert fibre. Those assertions are not needed for the stated construction.

## 5. Further uniform singularity invariants

**Location:** Paper II Section 7, Corollary 7.1. Label: `cor:power-multiplier-v157`.

The affine complete-quadric resolution gives explicit multiplier ideals and log canonical thresholds of all universal power-zero ideals. With `w_r=max(p-hr,0)` and `c_r=binom(n-r+1,2)`, the multiplier ideal is the intersection of `I_(r+1)` symbolic powers of exponent `max(0,floor(b w_r)+1-c_r)`, and the threshold is the minimum of `c_r/w_r` over positive w_r. We spell out the discrepancy and valuation calculation and credit the classical symmetric-determinantal theory of Henriques–Varbaro.

These are invariants of the whole universal power-zero scheme. They are not mislabeled as the conductor or the Hilbert function of every full reciprocal normalization fibre. The v155 complete-section character, length, socle, Lefschetz and nilpotence results and the v154 small-fibre full resolution remain with their exact scopes.

## 6. Response to the 24 specific requests

| Report item | Disposition in the complete revision |
|---|---|
| 1. Complete-local hypotheses | `lem:complete-local-v154` is retained, with locality, residue field, continuity, completeness and Noetherian hypotheses. |
| 2. Reduced completion | The excellent reduced local-ring argument and standard Stacks citations are retained. |
| 3. Miracle flatness | The named flatness input and hypotheses in `lem:residual-selection-v154` are retained. |
| 4. Residual selection and descent | The resultant-open cover, Artin cancellation and unique descent are retained. Universal power ideals now use polynomial base change, not descent from geometric fibres. |
| 5. Gradings | Ordinary coefficient degree, reciprocal weight and maximal-ideal filtration remain distinct. In the quadratic section the first two are one and two. |
| 6. Hensel product | `lem:hensel-products-v154` and its square-zero lifting proof are retained. |
| 7. Partition closures | The proper power-map argument and coincident-root comparisons are retained. The new native boundary closure order is separately attributed to complete quadrics. |
| 8. Conductor globalization | The coherent-ideal, stalkwise completion argument in `lem:equalizer-v154` is retained. |
| 9. Coordinate equalizer | The coefficient-by-monomial proof is retained with its coordinate hypotheses. |
| 10. Hochster citation | The Miller–Sturmfels attribution and full block Betti calculation are retained. |
| 11. Skeleton/transversal positioning | Classical monomial-ring properties are not relabeled as new; the geometric incidence identification is distinguished. |
| 12. Atlas versus classification | The introductions and conclusions consistently call it an exact completed incidence atlas. |
| 13. Branch finiteness | `prop:atlas-functor-v154` retains integral factor coefficients and monic-division quotient coefficients. |
| 14. Coordinate independence | The represented marked-divisor functor is retained. The new universal ideal and associated complete-quadric bundle are explicitly equivariant. |
| 15. Fitting equivariance | The simultaneous `GL_m` action in the double-root model is retained; the new universal proof specifies the full generating representation. |
| 16. Specialization lemma | The inherited variable-ideal-times-relation-ideal specialization argument is retained. |
| 17. Counts are not geometry | Equation and embedding-dimension counts remain correctly labeled. The graph, its boundary, contacts and flat resolved-pencil family are now global geometric consequences. |
| 18. Higher invariants | Full-section Hilbert functions, lengths and socles, small-fibre resolution and block Betti data are retained; all universal power-zero multiplier ideals are added. The whole fibre is not confused with a section. |
| 19. Acting groups | Native congruence, fixed-form full orthogonal and full cotangent-coordinate groups remain distinct. The new graph uses native congruence. |
| 20. Two-stage degeneration | The original two-stage proof is preserved; no universal one-parameter subgroup is asserted. |
| 21. Ballico comparison | Metadata are verified, but theorem and proof text remain unavailable. The article states this limitation and does not infer nonanticipation. |
| 22. Regression scope | The v155 suite is actually executed, including its inherited v154/v153 checks. The separate historical 28-check suite is explicitly not claimed as rerun. |
| 23. Infrastructure | Hashes, preservation manifests and compilation receipts are repository records, not arguments for mathematical significance. |
| 24. Separate papers | Two complete independent-compiling companion sources and PDFs are supplied. Paper II starts with the exact section, universal ideal and global boundary argument. The full master remains available without deleting inherited mathematics. |

## 7. Reading objects, preservation and verification

Paper I is **Finite failure schemes and the reconstruction of quadratic pencils** (`reconstruction.pdf`, 60 pages locally). Paper II is **Reciprocal power ideals, complete quadrics, and pencil degenerations** (`divisor-geometry.pdf`, 43 pages locally). The unified preservation master is `geometry.pdf` (98 pages locally). `BUILD_RECEIPT_V157.json` records the authoritative remote build counts and hashes. Both companion sources have stable embedded cross-reference maps and compile without an external companion auxiliary file.

All 322 v155 labels and all 219 theorem/lemma/proposition/corollary/definition/example/remark/proof environment blocks are retained byte-for-byte in the master. There are 352 labels and 236 such blocks in v157. Every mathematical body block is allocated exactly once across the two companion papers. The previous frontmatter is archived, and all predecessor branches and files remain untouched.

`check_v157.py` compares exact rational polynomial row spaces, not just their dimensions, for 34 power maps in seven dimension/exponent pairs. The two sides are computed independently from coefficients of `det(X+zA)^h` and balanced products of minors. It also checks the boundary and graph exponents in 40 parameter pairs, 375 local spectral profiles, and the explicit nonreduced-base example. It reruns the entire v155 finite check program and copies its new receipt into this revision. These finite checks do not certify the general proofs.

The new compactification and boundary-contact statements address the central missing bridge in the report. We do not claim a conductor formula for every collided multivariate image, a classification of every full `GL(E)` orbit closure, all Hilbert functions of all original reciprocal fibres, or an editorial acceptance decision. The manuscript states the exact new theorems at full strength and gives their proofs while preserving the sharp reconstruction program.
