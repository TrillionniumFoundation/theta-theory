# Response to the v14 referee report

**Manuscript:** Qian Qi, *Nonlinear boundary laws and asymmetric two-contact rigidity in dispersing billiards* (A2 v15).

**Frozen report:** `reviews/a2-v14-external-harsh-top4-rereview-2026-09-28/REFEREE_REPORT.md` at commit `a8e432bd27c21485a4babc268006314a5c7186c5`. The reviewed v14 author commit is `65b7286080ffae0c4bf8e5d5112fe42f08d82f21`.

We thank the referee for distinguishing the corrected mathematics from the remaining significance and presentation objections. This revision addresses those objections with a new asymmetric inverse and a theorem-led article. The prior mathematical scope and complete proofs remain available in the accompanying volume; no earlier result has been discarded to make the new article shorter. Editorial significance remains a matter for renewed independent assessment, not a field that a verification script can mark as passed.

## 1. A broader geometric conclusion (report §§5.2 and 6.5)

The new main Theorem 1.1 removes individual evenness for the contact inverse by adding an explicitly defined, orientation-sensitive observation. For each of the two three-impact itineraries, the exact data are the event probability and the unconditional signed first moment of the sum of the two transverse endpoint coordinates. Thus four scalar germs, not the full boundary graph or a marked length spectrum, are supplied.

Proposition 3.1 proves an affine highest-jet block at every degree, not just a linearization at symmetric contacts. Probability coefficients recover successive even derivatives after lower jets are known; signed moment coefficients recover the intervening odd derivatives. With `z=c0*c1-1>0`, the determinant of the symmetric odd block satisfies

```
(c0*c1)*(1+2*z)^(2*m) - (1+2*m*z)^2
    >= z*(1+2*m*z)^2 > 0,    m >= 1.
```

The proof includes the mixed-twist variation of the opposite contact, the exact quadratic ellipse moments, the fixed Morse-domain justification of finite-jet dependence, and the recursive inverse in degree order. No curvature-separation denominator occurs. In particular the first cubic block is nonzero at equal curvatures. Analytic continuation then determines the two participating connected analytic boundary images in the supplied frames.

This is a genuine enlargement of the inverse target, but not a change of information set hidden in notation. The final remark of §3 proves that simultaneous transverse reflection preserves both count germs and reverses the signed moment germs. Removing evenness from the old count-only statement would therefore not establish the new oriented conclusion. Labels, signed transverse axis, gap and separate curvatures remain supplied. The theorem does not determine unvisited obstacles or infer a smooth germ from all its jets.

## 2. Physical realization and observation, not merely a formal inverse (§§5.2–5.3)

Proposition 4.1 extends the support-function construction to every degree from 3 through a fixed K. It checks the left-contact sign convention for odd powers, the all-degree triangular support-to-graph Jacobian, positivity of curvature and first-hit clearance, and the nonzero area derivative. This gives actual analytic periodic tables with independent asymmetric jets, at fixed area or with area free. The selected leading hierarchy stays fixed on the fixed-area slices.

Proposition 4.2 proves positive-window observation on these physical families: 2K-4 scalar means with fixed area and 2K-3 with free area. Separate count and moment polynomial blocks, and the shared count intercept when area is unknown, yield an invertible finite-window Jacobian. No unknown area is inserted into the row normalization and no derivative or zero-offset value is measured.

Theorem 4.3 supplies the regular statistical consequence without treating it as the central novelty. For the lower bound it specifies a binary compression of the signed physical mark. The compression seed and the original endpoint mark are not returned. The adaptive entropy argument is for these Bernoulli channels, not for a moving-support, uncompressed endpoint experiment. The complete volume retains the full smooth-profile upper preparation bound and does not relabel it a matching infinite-dimensional minimax theorem.

## 3. The analytic forward comparator (§§5.1 and 6.2)

The introduction discusses the local analytic normal form before the global inverse comparison. Main §5 proves the mixed-boundary implicit equation and normalized derivative estimate, followed by the exact physical Jacobian formula on a common physical box. The analytic relative product is expressly not claimed as the new phenomenon. Its relation to the geometric smooth determinant construction remains visible, while the new inverse is carried by the signed all-degree moment blocks.

The smooth law still has its original full strength in the companion: common nonshrinking physical collars, fixed mixed parameter derivatives, both parities, first-hit localization and residual-time integration. Volterra uniqueness still concerns entire symmetrized energy profiles rather than formal Taylor series. These results are not replaced by an assumed analytic chart or a qualitative citation.

## 4. A single dominant theorem and preservation (§§5.4–5.5 and 6.1–6.3, 6.6)

The primary article is organized around Theorem 1.1. Its local physical law, all-degree inverse, physical image and finite observation consequences are proved in sequence. The other mathematical project is available as a separately readable complete proof volume, with a contents page and its own references. The article is no longer a chronological account of successive referee rounds.

The byte-level source check confirms that all 312 native v14 files remain available. In the active complete volume, only three files change: its main front matter, the same-section convention, and the probability-margin paragraph. All 54 historical top-level TeX inputs remain in order; there are 116 retained proof environments. The original native tree, earlier derivations and old acknowledgment text are preserved exactly. A concise main-article disclosure identifies the locations of the new AI-assisted ideas; detailed chronology and attribution belong to `PROVENANCE.md` and the frozen historical records.

## 5. Specific technical comments (§4)

**4.1, same-section convention.** Main §5.2 and the direct source `complete/article/16_normal_form_comparison.tex` now specify the same stable–unstable coordinate order and physical momentum/transverse conventions. Consequently `V_t(0)=U_p(0)` and `V_q(0)=U_s(0)`. The general determinant remains primary whenever a chart is reversed or its variables interchanged.

**4.2, fixed orders.** The abstract, Theorem 1.1, Proposition 4.2 and the complete-volume abstract explicitly fix the jet or derivative order before choosing constants. No conditioning bound uniform in growing order is claimed.

**4.3, probability margins.** The actual paragraph in `complete/article/31_regular_observability.tex` has been corrected. Nodes are first fixed inside a common physical collar; positivity and the strict upper bound then give uniform margins by continuity on the fixed compact parameter ball. The new observation proof uses the same order of choices.

**4.4, minimality.** The 2M-1 count in the retained even family and the 2K-4/2K-3 counts in the new asymmetric families refer only to differentiable locally bi-Lipschitz scalar-mean coordinate maps. The corresponding dimension argument is stated, and no minimum over arbitrary experiments is claimed.

**4.5, build evidence.** All three complete v15 documents have now been built locally, with 13, 133 and 7 pages respectively, using the recorded direct sources. Final logs have no undefined references or citations, multiply defined labels, overfull boxes or LaTeX warnings. The read-only validation records source hashes, executable commands and exit codes. The independent new diagnostics pass in normal and optimized Python with identical output; the retained 1,588 finite algebraic checks also pass in both modes.

A chronological correction is also necessary: the v14 CI run 36379170430 was queued when the report was finalized, but subsequently completed successfully at 05:37:46 UTC on 28 September 2026. Its artifact 10953112488 was downloaded and its SHA-256 and native source tree verified. We do not retroactively treat that later result as evidence available to the referee, nor use the old build as a substitute for the new local builds. Current v15 hosted CI status is reported separately from local source-content qualification.

## 6. Requested renewed assessment

The new result to assess is the asymmetric all-degree inverse from the explicitly enriched two-flight data, including its physical realization, not a renewed assertion that a local analytic relative product or a parametric risk rate is exceptional by itself. The full proof of that inverse is in the primary article, and the older smooth invariant and acquisition theory remain intact in the companion. We retain the requested four-journal benchmark without asserting that source tests or this response settle the editorial judgment.
