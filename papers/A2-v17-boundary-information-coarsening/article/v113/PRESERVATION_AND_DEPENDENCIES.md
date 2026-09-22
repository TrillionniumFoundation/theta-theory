# Preservation and proof dependencies — A2 v113

## Immutable baseline

Controlling review and branch base: `66220b85960a5a50db15342ccfacfbf1395bca88`.
Reviewed v112 mathematical source: `0c696736e6ec22259c730672f61ebd8ef0d95460`.
Reviewed v112 head: `e8eb87d4b22e341295175e2c3223fd21c68f41df`.

No inherited file is modified or deleted. New material is confined to `papers/A2-v17-boundary-information-coarsening/article/v113/`, `A2_REVISION_V113_INDEX.md`, and `.github/workflows/a2-v113-referee.yml` on the new revision branch.

## Exact retained parts

| Part | Baseline Git blob |
|---|---|
| 01-contact-native.tex | ea55d5e3b0f1d2316baaf88eaaf7c66b2e7074aa |
| 02-global-geometry.tex | f33676a3564e092f9e8bb6d2b7d7e504b9e7935b |
| 02b-component-structure.tex | d728969ccc2898ee8b29344a4383110ce0a97ced |
| 03-realization-stability.tex | 1410da1834f5d0f144f312bfc1766b9381e1447c |
| 04-statistical-experiments.tex | e52ed7b8d75f840e73bed815ca0441dc21a886c3 |
| 05-complements.tex | 6d605bd740e5ca4a5f02b9faa661c24dca7004e6 |

These are copies by Git blob identity, not summaries. The stable component proof and statistical parts move to the appendix through the master file's input order. Existing theorem hypotheses and conclusions are not weakened. The new bibliography retains every inherited key and adds Ballico 1993 and the Stacks reducedness criterion.

## Acyclic proof order

1. Retained classical Hankel strata and isotropic dimension formulas prove the retained full-range codimension theorem.
2. Direct differentiation and dual frames prove the all-rank residual tangent sequence; Schur elimination proves the all-corank local presentation.
3. Explicit affine fibres prove residual-plane dominance. Finite stratification gives incidence-to-component control. Expected grade gives purity independently of the new component list.
4. Analytic rank equality analysis gives exactly five exceptions. Orientation monodromy and nonsecant points identify the incidences. The explicit `(5,7,1)` product example supplies its excess component.
5. Dimension of the open projective annihilator fibre gives generic corank one. The residual tangent theorem gives generic smoothness. Purity plus generic reducedness gives the whole expected-codimension scheme theorem. When `k=c+1`, residual planes are the entire residual binary space; this case is treated separately rather than invoking a strict-subseries theorem outside its hypotheses.
6. The smaller square residual map is now covered by the already proved all-dimension theorem. Its determinant divisor, affine residual morphism and lift variation give the nonempty corank-one wall divisor. Normal-derivative factorization and the analytic implicit function theorem give the node; no induction on the node theorem is used.
7. The node gives the logarithmic local singular-value law. Phase factorization and dihedral monodromy give the higher-product sector theorem independently of a global higher-product dimension claim.
8. The earlier statistical proofs are unchanged. Explicit Poisson constants and the nuisance invariant clarify their uniformity and observation category.

## Scope boundaries retained explicitly

The all-dimension component theorem does not classify every smaller excess component or every global excess associated prime. The wall node theorem does not classify higher-corank, nonsplit, or colliding-support germs. Same-annihilator signed intersections are not substituted for every projected intersection. The higher-product theorem classifies two-point sectors, not the full higher-product failure scheme. The Ballico 1993 full-text priority comparison is not certified.

Finite checks are stress tests of formulas and examples. They are not proofs of universal statements, normality, reducedness, or publication-level novelty.
