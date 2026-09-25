# Response to the complete A2 revision 157 referee report

## Review object and revision

Controlling report: `reviews/a2-v157-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`, commit `b81ba4a2fac700f17b26163079bd17ef54947509`.
Reviewed complete predecessor: `a6d34cd2bb2075c64015f3667dbf3f391665cefd`; its mathematical source commit was `b1cde8e304c0572bdb436d8484f1c9b70333fd77`.
New branch: `revision/a2-v158-intrinsic-boundary-singular-pencils-2026-09-25`.

The two reading submissions are Paper I, *Finite failure schemes and the reconstruction of quadratic pencils*, and Paper II, *Intrinsic power geometry and singular quadratic pencils*. The paired preservation master is not a third submission. All 352 predecessor labels and all 236 predecessor mathematical environment blocks are preserved. Front matter is rewritten and its predecessor archived. No old theorem is discarded or weakened to dispose of an objection.

## The three principal mathematical changes

**Intrinsic source, rather than a selected auxiliary subspace.** The new theorem `thm:intrinsic-envelope-v158` works on the groupoid of sharp failure algebras with arbitrary ungraded isomorphisms. From the first relation it extracts the determinant support, its rank-one Fano rulings, and the source ruling oriented by coefficient-support asymmetry. This precedes recovery of the pencil Pluecker line. On that intrinsic source it constructs the algebra bundle

`B_(A,h) = direct sum_p B_h(V)_p tensor O_{P(V)}(2p)`.

A scalar has weight `2p` on the first factor and `-2p` on the second, so the entire algebra and its multiplication descend through `PGL(V)`. The projective coefficient spaces and power maps descend as well. The associated construction works after fppf descent of a projective-source bundle, including nonreduced bases; no unproved commutation of reduction or restricted graph closures with base change is used. This is a choice-free functorial envelope, not a claimed preferred subquotient of the original finite algebra or an untwisted linear representation at a point. Its native dimension is `n`. It never selects an `n`-plane inside the separate `n^2-1` dimensional reciprocal-fibre complement.

**Every normal rank and every symmetric pencil.** The new theorem `thm:all-rank-graph-v158` retains the last nonzero power `A^(hr)`. That power recovers the image `r`-plane by its degree-`2h` Pluecker embedding. The whole graph, not merely its normalization, is relative complete quadrics over `Gr(r,V)`. The theorem `thm:singular-complete-data-v158` combines its contact divisors with finitely many kernel maps `C_j`: second differences of their nullities recover Kronecker minimal indices. Supported contact orders recover elementary divisors. The proof gives the conservation law

`sum_(i<r) (r-i) deg D_i + 2 deg(Λ -> Gr(r,V)) = r`,

with Grassmannian degree equal to the sum of minimal indices. The canonical congruence classification itself is credited to classical theory. The examples `S_0 + S_2` and `S_1 + S_1` show exactly why power contacts without the kernel maps cannot detect the singular invariant.

**A computed Hilbert boundary, selected by multiplication.** The new theorem `thm:hilbert-tail-v158` treats the transverse corank-two family `diag(s,s+τt,t-a_3s,...,t-a_ns)` for every `n>=3`. Its total graph is the blow-up of `(s/t,τ)`. Its special Hilbert fibre is a reduced nodal main component plus an exceptional projective line, with no embedded components. Every exterior-power multidegree and every resolved multiplication map on that line are determined; the latter are complete Veronese systems with degree `min(b,2h-b)`. A single exact power ideal, `J_(h(n-2)+1)=(s/t,τ)`, creates the tail. The old finite failure algebra does pull back constantly to the exceptional component; that automatic fact is not counted as the new interaction. The new interaction is the functorially recovered source envelope whose actual family ideal chooses the centre and whose other powers prescribe the tail's linear systems.

## Responses to the 24 specific requests

1. **Intrinsic status of `B_(n,h)`.** Paper I, `thm:intrinsic-envelope-v158` and `rem:envelope-status-v158`, provide the source-normalized algebra bundle and its canonical projective diagram. Paper II's independent coefficient section remains explicitly relative to its chosen splitting. There is no asserted canonical quotient of the full reciprocal fibre or of the original failure algebra.

2. **Dimension mismatch.** Both introductions and the intrinsic theorem distinguish native `V`, of dimension `n`, from the divisor complement of dimension `n^2-1`. The new construction uses the oriented rank-one ruling of the original first relation. The auxiliary complement is not used to construct the native graph.

3. **Opening claim.** The opening now states the proved functorial construction, including its algebra-bundle category and scalar cancellation. It neither repeats the unproved subquotient suggestion nor abandons the native boundary goal. Source extraction precedes the final pencil coefficient recovery.

4. **Coefficient map, duals and determinant twists.** `prop:coefficient-conventions-v158` identifies the coefficient span as the dual of quotient multiplication, fixes `A -> gAg^t`, proves the socle character `(det V)^(2h)` and the dual perfect-pairing twist, and records all line and projective twists.

5. **Invariant-ideal comparison.** The new foundations section compares the argument with Henriques–Varbaro §2.4, Theorems 2.6–2.8, which explicitly recall Abeasis's symmetric invariant-ideal results. It distinguishes the ordinary ideal identified by the apolar coefficient map from the broader classical classification and integral-closure theory. It makes no exhaustive historical nonanticipation claim. `LITERATURE_AUDIT_V158.md` records the precise checked scope.

6. **Exact complete-quadric reference.** The foundations section identifies Vainsencher Theorem 6.3, as presented with the graph description in Massarenti Remark 2.5 and Construction 2.6. The singular rank variant is compared with Casarotti–Corniani–Massarenti Definition 2.5, Remark 2.6 and Theorem 2.14. These are the load-bearing classical constructions.

7. **Simultaneous graph hypotheses.** `lem:simultaneous-graph-v158` assumes an integral noetherian complex scheme and nonzero coherent section systems, defines the common dense open, includes the line-bundle twists and proves that the graph lies scheme-theoretically in the Segre variety. The proof uses the Rees algebra as a subalgebra of the function-field polynomial ring.

8. **Projective twists.** The coefficient proposition gives the section of `B_p tensor O(p)` and the ideal map `B_p^* tensor O(-p) -> O`. The graph lemma treats invertible twists and positive powers of the product ideal. The determinant's invertible ideal may be omitted for blowing up but not from its contact divisor.

9. **Symmetric DVR congruence.** `lem:symmetric-dvr-v158` supplies a complete local proof, including an off-diagonal pivot via `e_i+c e_j`, symmetric elimination, a zero kernel block, and square roots of units. Ordinary left-right Smith equivalence is not substituted for congruence.

10. **Full Segre datum.** `thm:singular-complete-data-v158` explicitly retains both the supported projective spectral points and their positive local partitions, modulo projective reparametrization of the pencil line. Together with the minimal indices these are the complex congruence data.

11. **Singular pencils.** The new theorem treats every normal rank, including all singular pencils, rather than removing the old regularity warning. The earlier regular-pencil theorem remains correct as its special case. The new finite syzygy maps supply the information absent from the power-contact divisors.

12. **Classical orbit stratification.** It is identified as recalled interpretation of complete quadrics, not counted among the new classification results. The old corollary and proof remain preserved.

13. **Compactification property.** `prop:flattening-property-v158` states the precise normal dominant embedded-flat-closure universal property, including its dominance and fixed Hilbert-polynomial hypotheses. It is acknowledged as standard. The following theorem supplies the substantive explicit boundary calculation.

14. **More than algebra pullback.** `rem:tail-integration-v158` states that the original algebra is constant on the exceptional tail and does not claim otherwise. The genuinely computed interaction is the exact envelope power ideal selecting the blow-up centre and the complete power linear systems on the exceptional component. The total family, not its closed point alone, is used.

15. **Nontrivial limiting Hilbert fibre.** `thm:hilbert-tail-v158` gives the complete reduced two-component fibre, both affine blow-up charts, transversality, absence of embedded points, multidegrees, Hilbert polynomial, boundary intersection points and every power map on the tail. It applies to all dimensions at least three and all exponents `h>=1`.

16. **Multiplier-ideal attribution.** The foundations section states exactly that the old multiplier formula is a substitution of the universal exponents in Henriques–Varbaro Theorem 4.8. It is retained as a corollary and is not an independent originality pillar.

17. **Root review entry.** The branch-specific publication procedure updates `CURRENT_REVIEW_ENTRY.md` to v158, not v155 or v157. The final immutable source and materialization commits are separately identified there.

18. **Two pinned reading objects.** The root entry and directory README name Paper I and Paper II separately, with their complete PDF/source pairs and build receipt. The unified master is clearly marked as a preservation object only.

19. **Source versus materialization.** The build receipt records the mathematical source commit through the actual checked-out GitHub SHA. The materialization commit writes the compiled outputs. The final root entry pins that output commit without a self-referential hash claim.

20. **Finite checks.** `check_v158.py` performs exact rational tests, not a certification of the general arguments. It reruns the v157 suite, including the inherited v155/v154/v153 checks that those scripts actually invoke. The distinct historical 28-check suite is still not claimed as rerun.

21. **Ballico limitation.** Both submitted introductions retain the full-text limitation, in addition to the inherited literature discussion. Neither the wording nor the repository metadata asserts nonanticipation from an unavailable source.

22. **Paper I scope and retention.** The principal reading path is explicitly limited to first relations, source rulings, coefficient extraction, sharpness and the local inverse; the envelope is a stated application. The covering, stack and spectral extensions remain in the appendices and are not premises of the sharp theorem. They are retained rather than deleted. Further editorial separation may be considered by the referee, but no mathematical content is silently removed.

23. **Logical dependencies.** Both introductions now distinguish independent cores from linked applications. The sharp inverse does not use the power graph. The universal ideal, rank graph, given-pencil contact/syzygy and Hilbert-tail theorems do not use the inverse. Their interpretation for abstract failure algebras uses the source theorem. Identifying the intrinsic envelope's graph uses the companion's algebraic graph theorem. This is explicit logical dependence, not merely independent compilation.

24. **Canonicity with choices.** The source-normalized envelope is functorial by scalar-trivial descent, with a full cocycle argument. The chosen reciprocal-fibre section is still not called canonical under arbitrary changes of splitting. The distinction between an associated ambient graph and a restricted family's graph closure is preserved.

## Scope of the next evaluation

The new assertions needing mathematical scrutiny are the scalar-trivial source-envelope descent, the rank-stratified graph identification through its highest power, the combined contact/syzygy recovery and degree law, and the scheme-theoretic tail calculation with its complete linear systems. We do not claim a new classical Kronecker normal form, a new complete-quadric variety, a classification of every Hilbert boundary fibre, a proper quotient-stack compactification, or a canonical untwisted algebra at a point. The latter is not silently substituted for the proved algebra-bundle construction. No journal outcome or formal proof certification is asserted.
