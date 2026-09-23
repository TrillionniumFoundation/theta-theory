# Independent harsh referee report — A2 revision 140

## Manuscript and review scope

**Manuscript:** *Intrinsic reconstruction from nonreduced failure schemes*  
**Author:** Qian Qi  
**Reviewed revision branch:** `revision/a2-v140-intrinsic-pencil-moduli-2026-09-23`  
**Exact reviewed branch head:** `6bac73f9ebcaadcfa135e4960de19c93323bbfd7`  
**Immediate predecessor:** `revision/a2-v139-natural-moduli-referee-closure-2026-09-23`, commit `4ebf4fbf7c07b72d80429aa23d38b290ac731150`  
**Controlling earlier independent report:** `reviews/a2-v137-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`  
**Review standard:** external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested, AI-assisted independent referee-style report, not a journal-commissioned editorial decision.

I reviewed the current principal article, the inherited web and all-pencil reconstruction architecture relevant to the new claims, the v139 sharp finite-neighbourhood theorem, the v140 spectral-torsion and rank-preserving-specialization section, the responses to the v137 report, the v139/v140 literature audits, the source/provenance manifests, the exact symbolic checks, and the current GitHub Actions state.

There is an unusual source-state qualification. At the exact reviewed head, the branch does **not** contain the fully materialized native `v140` manuscript tree. It contains a checksum-bound transport plus workflows intended to reconstruct `v138 -> v139 -> v140`. The source-audit run `35856728237` succeeded, but the three `A2 v140 spectral revision` materialization runs `35858667472`, `35858772847`, and `35859428260` all failed. The latest failed run stops before the fifteen mathematical/build checks. I therefore independently reconstructed the intended source from the pinned v138 referee artifact and the checksum-bound v139/v140 transports:

- v138 referee artifact: run `35847505538`, artifact `10743339474`, archive SHA-256 `bd68ac83a841259a4f2b39fa803bd48e8d43b4b508ea2b8a4a3e44168d48d665`;
- v140 incoming transport artifact: run `35859428260`, artifact `10749355942`;
- transport SHA-256 before the recorded three edits: `543d5d6e0adc4eaf5c84b9039a2a00400b9eaaa31ccc2653bf30e60ede794bb9`;
- transport SHA-256 after those edits: `0ecc40af06906aa9d203e5716988031c588e4bd250a6d24134442c346ef82f72`;
- decoded v140 source-package SHA-256: `63bd8efa21ea56aa8cb6a2337e81233f2ba093b7eb321cef6e2c84a59a4deff2`.

On that independently reconstructed source, the complete v140 build passes: all fifteen exact/symbolic scripts execute successfully; the source-integrity and label checks pass; the principal article is 49 pages, the supplement 66 pages, and the complete compilation 112 pages; 326 inherited labels and 338 current labels are recorded; and the resulting `BUILD_RECEIPT_V140.json` has `ok=true` with no failed checks. I treat these facts as reproducibility and regression evidence only. They do not formally verify the global proofs or settle historical novelty.

For the two most relevant external comparisons, I also checked the public record for Fevola--Mandelshtam--Sturmfels, *Pencils of quadrics: old and new*, *Le Matematiche* 76 (2021), 319--335, DOI 10.4418/2021.76.2.2, and the publisher record for Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Math. Nachr.* 163 (1993), 5--13, DOI 10.1002/mana.19931630102. The former treats Segre-symbol classification and reciprocal curves as established pencil geometry. The latter publisher page exposes bibliographic material and a first-page route, but I did not obtain theorem text sufficient to perform the six-axis comparison demanded by the earlier report.

## Recommendation

**Reject in the present form at a general top-four mathematics journal.**

This is a materially more positive mathematical assessment than the v137 report. The authors have done real work since v137: the deliberately engineered polar example is no longer carrying the generality claim; the paper now contains a natural all-pencil multiplication-failure family, a scheme-theoretic parameter embedding, a sharp finite-neighbourhood result, and an explicit classical spectral/reciprocal-geometric consequence. I did not find a new fatal defect in the v140 spectral theorem or in the displayed rank-preserving specialization.

Nevertheless, the manuscript still does not clear the bar required for a positive recommendation to a general top-four venue. Two novelty questions are expressly unresolved by the manuscript itself, the closest historical failure-locus source remains unread at theorem level, and the new spectral section--although mathematically coherent and useful--does not yet turn the paper into the solution of a recognized external problem of commensurate significance. In addition, the current revision branch is not presently a self-contained green submission object: its canonical materialization fails before the advertised build/audit stage.

I would support a genuinely fresh referee round after these issues are closed. I would not describe the remaining work as cosmetic.

## 1. What revisions 138--140 have genuinely fixed

### 1.1 B137.2 is substantially improved: there is now a natural second family

The v137 report objected that the polar-Fitting family encoded the hidden coefficient space too directly. That criticism no longer describes the paper's strongest second family.

Section `sec:natural-pencils` starts from the original multiplication map of the cube-zero algebra `A_R = C + V + (Sym^2 V/R)` and its genuine multiplication-failure scheme. No auxiliary coefficient-evaluation block is inserted. The factorization

`I_{\widehat D_R} = (det M) I_p(\gamma Sym^2 M)`

comes from the actual maximal minors of the multiplication matrix. For pencils, the exterior representation is irreducible and the residual coefficient module recovers the entire Plücker line.

This is qualitatively stronger than the v137 polar construction. The paper should say plainly that this natural pencil family, not the polar example, is now the principal answer to the former conceptual objection.

### 1.2 B137.3 is also substantially improved: the criterion now has an automatic family theorem behind it

Theorem `thm:automatic-quadratic-coefficients` proves the required coefficient extraction for a full Grassmannian range of quadratic relation spaces, rather than assuming the key coefficient decomposition as part of a criterion. Theorem `thm:finite-parameter-immersion` then proves a closed immersion of the full pencil parameter scheme into the Grassmannian of first relation spaces, with arbitrary complex base change in fixed tensor coordinates.

The factorization through the Plücker embedding, the line-to-subspace embedding, and a fixed linear representation inclusion is conceptually clean. In my reading, this is a genuine response to the v137 complaint that the "principle" was then little more than a restatement of its hypotheses.

### 1.3 The v139 finite-neighbourhood theorem is the strongest new structural result since v137

Theorem `thm:sharp-finite-pencil` is clear and auditable. The ideal in the graph neighbourhood has no relations below degree `d = n + 2(N-2) = n^2 + 2n - 4`, so every lower ideal-adic neighbourhood is independent of the pencil. At order `d`, the nilradical multiplication recovers the first relation space `K_R = ker(Sym^d(n/n^2) -> n^d/n^(d+1))`, and because the normal-cone ideal is generated in that one degree, this relation space recovers the whole graded normal cone. The prior intrinsic reconstruction then recovers the pencil.

I did not find an off-by-one error in the convention: `Z_R^[k]` uses the quotient by the `(k+1)`-st power, so a relation of degree `d` first becomes visible at `k=d`.

The sharpness asserted is correctly **uniform sharpness**: every lower order fails to classify all pencils, while order `d` classifies all of them. The manuscript should preserve this wording and avoid suggesting that every individual pencil necessarily has pointwise minimal separating order exactly `d` against every other pencil.

### 1.4 The new v140 spectral statement is mathematically coherent

Theorem `thm:spectral-finite-torelli` identifies, for regular pencils, the data recovered at the sharp finite order with the classical spectral torsion sheaf on the parameter line. The proof that an unpaired torsion sheaf suffices over C is short but meaningful.

After choosing an affine coordinate away from the spectral support, the torsion sheaf gives the similarity class of `C=A^{-1}B`. If two nondegenerate symmetric forms `A,A'` make the same `C` self-adjoint, then `K=A^{-1}A'` commutes with `C` and is self-adjoint for `A`. Since `K` is invertible over C, a polynomial square root `H=h(K)` exists modulo the minimal polynomial. Then `H` commutes with `C`, is self-adjoint for `A`, and gives `H^t A H = A'` and `H^t B H = B'`.

I see no immediate defect in this argument.

### 1.5 The v140 specialization is a real, exact example rather than a slogan

For the four-dimensional block, the identities `C_t^2 = [[0,tN_0],[0,0]]` and `C_t^3=0`, together with `rank C_t=2` for all `t` and `rank C_t^2=1` exactly for `t != 0`, give partitions `(3,1)` and `(2,2)` while the determinant stays `s^4`. The spectator extension preserves the advertised simple roots.

The independent symbolic audit verifies the determinant, ranks, determinantal divisors, inverse formula, and spectator extensions in exact arithmetic. I also checked the algebraic argument in the manuscript rather than relying on the script. It is sound as written.

The qualifier **reduced** in "fixed reduced rank loci" is essential. The manuscript correctly retains it: the gcd of the three-row minors changes from a unit times `z` to a unit times `z^2` at the multiple root. Thus the example does **not** say that all full determinantal/Fitting data remain fixed; it says precisely that the reduced rank loci and the full determinant remain fixed while higher spectral/Fitting information changes. This distinction must not be weakened in future revisions.

## 2. Major blocker B140.1: the current v140 branch is not a self-contained submission object

This is not a theorem-level objection, but at present it is a real submission blocker.

At commit `6bac73f9...` the native directory `papers/A2-v17-boundary-information-coarsening/article/v140/` is absent. The branch depends on Actions to recover the predecessor artifact, reconstruct v139, apply v140, run all checks, compile three PDFs, and then commit the native sources and evidence back to the branch.

That workflow has failed three times. The latest run `35859428260` successfully checks out, records and decodes the transport, downloads the authentic v138 artifact, and then fails in "Restore and verify the complete predecessor source." The subsequent dependency installation, fifteen audits, PDF compilation, publication commit, and referee-bundle upload are skipped.

The failure is reproducible from the workflow logic. The restored v138 files are present in the working tree but are not tracked in the v140 branch index. The v139 assembler then invokes a Git comparison against the v138 pin over the predecessor source path. Git therefore reports the predecessor tree as deleted relative to the pin even though artifact bytes have been restored into the working tree, and the assembler exits before mathematical checks begin.

I was able to reconstruct and build the package independently, so this failure is **not evidence that the mathematics or symbolic checks fail**. It is evidence that the current canonical publication route is broken.

For an actual submission, a referee should not have to reverse-engineer a transport chain and Actions artifact lineage to obtain the article. Required action:

1. materialize the complete v140 native source tree and PDFs on the reviewed revision branch;
2. make the workflow green on that exact source commit;
3. preserve a source-bound receipt whose commit SHA is the commit actually containing the reviewed manuscript;
4. ensure the predecessor verification compares artifact bytes/provenance manifests rather than relying on index membership that the workflow itself intentionally omits.

Until this is done, the repository does not yet present a stable, independently reviewable "revision 140" in the ordinary sense.

## 3. Major blocker B140.2: the Ballico 1993 theorem-level comparison remains open

This blocker survives unchanged in substance from v137, and the v140 literature audit explicitly admits it.

The closest historical item is still E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* 163 (1993), 5--13. The title and surrounding literature are close enough to the manuscript's central vocabulary--failure loci, higher-order properties, degeneracy phenomena--that a general top-four referee cannot responsibly certify conceptual novelty without reading the theorem statements and proofs.

The current audit has bibliographic verification but not the demanded six-axis theorem comparison:

1. parameter spaces;
2. reduced versus scheme-theoretic failure loci;
3. the varied multiplication or higher-order map;
4. nilpotent, infinitesimal, colon, or normal-cone structure;
5. relative/base-change statements;
6. inverse/reconstruction conclusions.

The authors are commendably explicit that this remains unverified. But an honest open blocker is still an open blocker.

**Required action:** obtain the complete article through a lawful library/interlibrary route and perform a theorem-level comparison. The final paper should then state exactly what Ballico proves, what it does not prove, and where the present reconstruction mechanism first departs from that framework.

At this stage I would not accept "we do not claim exhaustive priority" as sufficient for a top-four submission whose central conceptual claim is a new use of nonreduced failure schemes. The burden is not to prove that no related paper exists anywhere; it is to close the closest known comparison that has already been identified.

## 4. Major blocker B140.3: the exact novelty of the all-dimensional contraction theorem is still not cleared

The inherited all-dimensional theorem remains one of the manuscript's most ambitious claims. It computes the rank-dependent kernel of the specific contraction `iota_q o j_n : det(V) tensor Sym^n(V) -> wedge^(n-1) Sym^2(V)`, including singular ranks and the even-dimensional nondegenerate exception. The paper then converts this to an exterior-support gap and a uniform recombination theorem.

The v138 operator-comparison section is useful: it distinguishes harmonic decomposition, transvectants, apolar differential operators, exterior contraction, Piola-type identities, and skew-flattening support. But v140 itself concedes that the broader expert comparison requested in B137.5 has not been completed. The local build receipt also lists an "exhaustive priority assessment for the contraction theorem" as documentary-open.

That is unacceptable if this theorem is to carry general significance in a top-four paper. It is not enough to show that surrounding ingredients are classical while the exact formula was not encountered in a small set of sources. The authors need a map-specific comparison with classical invariant theory and the literature on symmetric/exterior plethysm, transvectants/contractions, orthogonal branching, Jacobian/polarization embeddings, and known kernel formulas for the same or equivalent equivariant map.

I do not have evidence that the theorem is anticipated. I also do not have enough evidence to certify that it is new. The manuscript currently asks the reader to accept a major novelty claim while explicitly recording that its exact novelty audit is unfinished.

## 5. Major blocker B140.4: the top-four significance case is better, but still not closed

This is now the decisive mathematical/editorial issue.

Revision 140 has finally produced a natural external geometric consequence: the finite multiplication-failure neighbourhood recovers the classical spectral torsion module of a pencil, and an explicit flat family has fixed discriminant and fixed reduced rank loci while the spectral partition changes; in dimension four the reciprocal curve changes from a conic to a line.

This is a substantial improvement over the v137 polar example. It is natural pencil geometry, and Fevola--Mandelshtam--Sturmfels independently study Segre strata and reciprocal curves.

However, the new section still does not establish a top-four-level external significance theorem.

### 5.1 The spectral theorem is largely a composition of the new internal reconstruction with classical pencil classification

The implication `Z_R^[d] isomorphic to Z_R'^[d] <=> R and R' projectively equivalent` is the v139 theorem. The equivalence between a regular symmetric pencil and its root-labelled elementary-divisor/spectral-torsion data is classical. The new proof of the unpaired-sheaf sufficiency is elegant, but it is not itself a deep new classification theorem.

Thus `thm:spectral-finite-torelli` primarily identifies what the paper's internal invariant is remembering in classical language. That is valuable exposition and interpretation. It is not, by itself, the external breakthrough the earlier report asked for.

### 5.2 The rank-preserving specialization is explicit and correct, but elementary

The family is a carefully chosen nilpotent four-by-four block, with spectator eigenvalues in higher dimension. The distinction between `(3,1)` and `(2,2)` is read from `rank C_t^2`. The conic-to-line reciprocal change follows directly from `(sI+uC_t)^(-1) = s^(-1)I - u s^(-2) C_t + u^2 s^(-3) C_t^2`.

This is a good example. It demonstrates that the failure neighbourhood detects strictly more than the determinant plus reduced rank loci. But it does not resolve a previously recognized open problem, classify a difficult moduli fibre, or produce an unexpected theorem about reciprocal curves beyond the explicit block family.

### 5.3 The sharp finite order is mathematically precise but internally generated

The number `d=n^2+2n-4` is the degree at which the first homogeneous relation appears: degree `n` from `det T` plus degree `2(N-2)` from the maximal minors. Once the single-degree generation and prior normal-cone reconstruction are known, the "all lower orders are constant / order d recovers the pencil" conclusion is structurally natural.

Again, this is a strong theorem about the paper's invariant. But the manuscript has not yet shown why this exact high infinitesimal order answers a question that the surrounding community was already trying to understand.

### 5.4 What would close the significance gap

The paper needs one external theorem that experts in algebraic geometry/invariant theory would recognize without first buying into the paper's bespoke failure-scheme construction. Plausible routes include, for example:

- classify or geometrically describe a fixed-discriminant/fixed-rank stratum of pencils and prove that the finite failure neighbourhood provides its normalization, a canonical finite cover, or a complete modular refinement;
- prove a theorem about the fibres/monodromy of a previously studied web--K3--Reye--Enriques moduli map, and show that the nonreduced failure scheme resolves a genuine pre-existing ambiguity;
- identify the recovered first-relation module with a standard moduli-theoretic or syzygetic object and prove a new theorem about that object independent of the reconstruction packaging;
- turn the one-parameter spectral example into a classification theorem for which partitions can specialize with fixed determinant and fixed reduced rank loci, and prove that the failure-neighbourhood invariant is the minimal natural refinement detecting those strata.

I am not prescribing one of these exact projects. The point is that a top-four significance case requires more than an internally sharp invariant plus an explicit illustrating family.

## 6. Detailed audit of Theorem `thm:spectral-finite-torelli`

I found the proof credible, but I recommend two local improvements before another review.

### 6.1 Make the sheaf-to-similarity step explicit

The text says that, after choosing an affine coordinate avoiding the support, the torsion modules are the vector spaces on which the coordinate acts as `C=A^{-1}B`, so an isomorphism of sheaves gives similarity of `C` and `C'`.

This is correct, but in a theorem whose point is precisely the sufficiency of the unpaired torsion sheaf, it deserves a one-paragraph lemma. State explicitly that a finite-length coherent sheaf supported in the chosen affine line is equivalent to a finite-dimensional module over `C[z]`, and that the presentation sequence identifies multiplication by `z` with the stated matrix (up to the chosen sign convention). Then an `O`-module isomorphism is exactly a module isomorphism and hence a similarity.

### 6.2 Spell out the polynomial square-root argument at the right algebraic level

The square-root argument is correct over C, including nonsemisimple `K`, because `K` is invertible and one can solve `h(x)^2=x` in each local Artinian factor `C[x]/(x-lambda)^m` and combine by Chinese remainders.

Write it this way. The current phrase "prescribe a square-root Taylor expansion" is accurate but compressed. This point is what removes any need for an extra symmetric pairing on the torsion sheaf, so it should be maximally transparent.

These are not rejection-level proof gaps.

## 7. Detailed audit of Theorem `thm:rank-preserving-specialization`

I found no fatal error in the displayed family.

The four-dimensional block has the advertised ranks and nilpotent partitions. The determinant identity is immediate from nilpotence of `C_t`. With spectator blocks, the multiple root remains unique and every added root is simple. Therefore the corank function on the marked projective line is independent of `t`; over C the associated reduced determinantal subschemes are indeed determined by these closed-point sets.

The spectral length profiles `(3,1): (ell_1,ell_2,ell_3,...)=(2,3,4,...)` and `(2,2): (2,4,4,...)` correctly distinguish the special fibre from the punctured fibres.

The flatness argument is also plausible: two fixed linear functionals split off a fixed complement to every `R_t`; hence the quotient `S_{R_t}`, the socle Grassmannian, and its graph bundle are simultaneously trivialized over the parameter line. The degree-`d` relation spaces form a constant-rank subbundle by `thm:finite-parameter-immersion`, so the truncated algebra is locally free.

For auditability I would nevertheless extract the gluing argument into a short relative proposition. The manuscript moves quickly from the fixed-coordinate closed immersion `R -> K_R` to the tautological bundle over `B x A^1`. State explicitly that the local relation subbundles are equivariant under right frame changes of `U` and therefore glue to the structure sheaf of the **actual ideal-adic neighbourhood** `Z_{R_t}^{[d]}`, not merely to an abstract family of isomorphic coordinate quotient algebras. I believe this is what the proof is already using; it should be written as such.

Again, this is a clarity request, not a detected counterexample.

## 8. The reciprocal-curve corollary is clean but should not be oversold

For `t != 0`, `I,C_t,C_t^2` are linearly independent and the inverse pencil is the quadratic Veronese image in their projective span. At `t=0`, `C_0^2=0` and the image is a line. The corollary is correct.

Its role should be calibrated carefully. It proves that the paper's finite failure neighbourhood detects a change in an independently studied classical object. It does **not** prove a new classification of reciprocal curves, and the reciprocal curves themselves are explicitly not claimed to form a flat family. The current text respects these limits; future revisions should keep them.

## 9. The inherited web theorem is no longer the main correctness concern, but its significance narrative is still diffuse

The v137 report found that the earlier fatal-looking local proof issues--scheme-theoretic rank-one Fano recovery, common-coordinate descent, and full orthogonal harmonic irreducibility--had been credibly repaired. Those arguments are retained. Revisions 138--140 add rather than replace the main web theorem.

I found no new v140 change that reopens those repaired local points. The problem is now presentation and significance. The paper simultaneously asks the reader to regard as central:

- the four-dimensional web/K3 reconstruction theorem;
- the all-dimensional contraction/support theorem;
- the automatic coefficient-extraction family;
- all-pencil intrinsic reconstruction;
- sharp finite-neighbourhood order;
- hyperelliptic moduli;
- spectral torsion;
- reciprocal geometry;
- and the polar construction.

All are related, but a 49-page principal article cannot make all of them the primary significance story. At a general top-four journal, the introduction must tell the reader which theorem changes the subject and why the other results are necessary consequences or supporting structure.

My recommendation is not to delete mathematics arbitrarily. It is to impose hierarchy. The polar construction and some of the historical/technical comparisons can remain in the supplement if they are not required for the main theorem chain. The principal article should have one unmistakable spine.

## 10. Reproducibility evidence is strong once the source is reconstructed

The authors' regression discipline is unusually good. On the independently reconstructed source I obtained:

- fifteen executed exact/symbolic scripts;
- `REVISION140_EXACT.json` with all displayed v140 identities passing;
- 338 unique current mathematical labels with all 326 inherited labels retained;
- source-hash agreement against `PROVENANCE_MANIFEST_V140.json`;
- principal article: 49 pages;
- supplement: 66 pages;
- complete compilation: 112 pages;
- no failed checks in the final local receipt.

This evidence is worth preserving. But it should remain subordinate to mathematical proof and novelty. A build receipt cannot certify the all-dimensional theorems, historical exhaustiveness, or journal-level significance, and the v140 verifier itself correctly says so.

The immediate priority is to make the **remote canonical build** reproduce this successful state.

## 11. Required work before I would support a fresh top-four review

I would require all of the following.

1. **Repair and materialize the v140 submission branch.** Put the native manuscript source/PDF/evidence tree on an immutable reviewed commit and obtain a green source-bound workflow on that commit.
2. **Complete the Ballico 1993 six-axis theorem comparison.** This is the closest identified historical source and remains nonnegotiable for the central novelty narrative.
3. **Complete the map-specific novelty audit of the all-dimensional contraction theorem.** Compare the exact rank-dependent kernel formula and even-dimensional exception, not merely neighboring representation-theoretic ingredients.
4. **Prove one external significance theorem stronger than the current explicit specialization.** The spectral and reciprocal examples are good evidence of naturality; they are not yet enough to carry a general top-four paper.
5. **Clarify the relative gluing in the flat v140 family.** State explicitly why the frame-local degree-`d` relation subbundles glue to the actual ideal-adic neighbourhood family.
6. **Add the two short lemmas/paragraphs in the spectral theorem proof.** Make sheaf-isomorphism-to-similarity and the polynomial square-root argument completely explicit.
7. **Keep the distinction between reduced rank loci and full determinantal/Fitting data.** The example depends on this distinction; do not rhetorically strengthen it.
8. **Choose one primary narrative in the 49-page article.** Preserve the mathematics, but move secondary constructions/history to supporting material if they interrupt the main theorem chain.
9. **State the exact novelty boundary of the finite-order result.** Emphasize what is genuinely new--intrinsic recovery from the unmarked failure neighbourhood and the parameter-scheme embedding--and distinguish it from the formal consequence of knowing the first homogeneous relation degree.

## 12. Final assessment

Revision 140 is not an empty iteration. It contains substantial new mathematics beyond v137, and the most serious earlier conceptual objection--that the only generalization was an engineered coefficient block--has been addressed by the natural pencil family. The v139 sharp finite-neighbourhood theorem is a strong and clean result. The v140 spectral interpretation and rank-preserving specialization are mathematically coherent, and I found no new fatal defect in their displayed proofs. The independently reconstructed package also passes its full regression/build suite.

That is still not enough for a positive recommendation at a general top-four journal.

The closest historical failure-locus comparison remains open. The exact novelty audit of one of the paper's broadest representation-theoretic theorems remains open. Most importantly, the current external application demonstrates that the invariant sees classical data that reduced rank information misses, but it does not yet establish a field-level theorem whose importance is independent of the paper's own reconstruction framework. Finally, the exact reviewed branch does not presently contain a green, native, self-contained v140 submission tree.

Accordingly my recommendation is **reject in the present form**, with an invitation to return only after the priority, significance, and source-state blockers have been genuinely closed. If those are closed, the paper would merit a fresh top-four review on its mathematical merits rather than another incremental response round.
