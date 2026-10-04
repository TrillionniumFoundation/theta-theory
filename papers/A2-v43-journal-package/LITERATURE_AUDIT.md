# Literature audit — A2 v43

**Manuscript:** *Scalar collision laws and recognition of periodic dispersing billiards*.
**Audit date:** October 4, 2026. **Scope:** current theorem-level comparisons and
version-sensitive primary-source checks, not an exhaustive priority search.
The v41/v42 research notes are retained as provenance, not current front matter.

## Current comparison map

The primary comparison is `core/28_theorem_comparison.tex`. The bibliography
in `references.tex` supplies the following precise sources and locators.

| Comparison | Source and locator | Role in the present argument |
|---|---|---|
| Planar covariogram uniqueness | Averkov--Bianchi, JEMS 2009, Theorem 1.1; doi:10.4171/JEMS/179 | Classical recovery modulo translation/reflection from a different exact datum. |
| Two-body factorization | Bianchi, Adv. Appl. Math. 2009, Theorem 1.1; PLMS 2016, Theorem 6.3; doi:10.1016/j.aam.2008.10.002 and doi:10.1112/plms/pdw020 | Polygon exceptions, smooth factor classes and reflected interchange differ from the ordered collision datum. |
| Noisy geometric data | Bianchi--Gardner--Kiderlen, JAMS 2011, Theorems 4.10 and 6.4; doi:10.1090/S0894-0347-2010-00683-2 | Covariogram observations are not free collision observations. |
| Unknown probe | Villarrubia, J. Res. NIST 1997, Sections 5.1 and 7.3.3; doi:10.6028/jres.102.030 | Maximal consistent probe versus exact factor separation from the matched support identity. |
| Signed support measures | Martinez-Maure, Definition 4.4 and Theorem 4.6, as cited in `references.tex` | Classical signed length measures; separating the two summands here uses nonatomic obstacle mass versus chord atoms. |
| Compact deconvolution | Meister, Theorem 1, and Delaigle--Meister, Theorem 4.1, as cited in `references.tex` | Fourier zeros do not invalidate exact uniqueness; finite collision estimates instead use explicit moments. |
| Moments and transportation | Rigollet--Weed, Section 2.3, Theorem 4 and Corollary 1, as cited in `references.tex` | Classical moment comparison; the present bivariate positive-factor proof and collision acquisition are internal. |

These comparisons and locators are retained from the reviewed manuscript.
This round rechecked the version-sensitive unknown-noise items below, rather
than claiming a fresh exhaustive audit of every source in the table.

## Unknown-noise identification and the erratum

Gassiat--Le Corff--Lehericy, *Deconvolution with unknown noise distribution is
possible for multivariate signals*, Ann. Statist. 50 (2022), 303--323,
doi:10.1214/21-AOS2106, Theorem 2.1, is the exact identification comparator.
Its independent noise-coordinate blocks and entire-transform dependence
condition are substantive. The compact planar launch law in A2 need not have
independent coordinates; the collision-support identity supplies the extra
information instead. This exact comparison is not a borrowed statistical rate.

The authors' erratum was checked at
https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/erratum.pdf
(HAL record https://hal.science/hal-04928354). Pages 1--2 identify an error in
the quantitative contrast argument for Proposition A.2; Sections 1--3 give
replacement conditions for rate arguments. Page 4 distinguishes these from
unchanged consistency. The exact identification theorem is still used in the
erratum. A2 neither imports that contrast bound nor depends on its statistical
rate proof. The primary and bibliography now cite this scope explicitly.

## The accepted Bernoulli version and numbering

The Bernoulli journal's papers page links the accepted manuscript at
https://www.e-publications.org/ims/submission/BEJ/user/submissionFile/68730?confirm=a078ae36 .
It was reopened successfully in this round. For Capitao-Miniconi--Gassiat--Lehericy,
*Support and Distribution Inference from Noisy Data*, the relevant locators are
Corollary 2.5 (printed p. 6, followed by the strict-convex illustration),
Theorem 5.1 (printed p. 17), and assumption (Amin) (printed p. 10).
The compact-signal Wasserstein upper bound is of order `log log n/log n` on
its stated class. Quantitative contrast is distinct from exact dependence.

The author's 51-page version at
https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/support.pdf
uses Corollary 2 and Theorem 6 for the corresponding statements. The journal
comparison consistently uses the accepted 30-page numbering, not a mixture of
the two versions. Bernoulli lists the paper among its forthcoming papers and
the author publication list also marks it forthcoming; no invented volume or
page numbers have been added. Neither these passive additive samples nor their
rates are used as observations or costs of the collision experiment.

## Attribution boundary

The endpoint identity, matched support cancellation and signed two-bit
acquisition are identified with their A2 derivation history. Support-function
calculus, Fourier uniqueness, positive finite fitting, polynomial approximation,
concentration and transportation duality are not represented as newly invented
background theorems. No exhaustive novelty or journal-acceptance claim is made.
