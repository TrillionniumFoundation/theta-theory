# A2-DYN: endpoint kernels and exact physical-interval inversion

**Author revision, 23 October 2026.** This is a continuation of the complete localized-clearance manuscript, not a new referee report. The paper remains *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The original triangular lattice, circular scatterers with radius (R\in[9/20,47/100]), all actual first collisions, unit-speed physical time, prescribed section and return events, exact displacement and occupation labels, and normalization (c_*=91/(10000\pi)) are unchanged. All 73 inherited core proof files 260–332 and the model/input files are byte-identical to the frozen predecessor. The native manuscript builds from `main.tex` without a generated replacement text.

## Mathematical additions

1. **A selected endpoint kernel including the first flight.** Native 335 retains the exact length of the first physical image of a clearance-selected horizontal source. The inherited length-sensitive renewal estimate and genuine time reversal give

   \[
   D_{m,R;j,\delta}(a,v)\le C_{\rm end}
     \bigl(\delta+\theta_{\rm r}^{\max(j,m-1-j)}\bigr),
   \]

   uniformly for every actual collision count, radius, flight index and pair of regular endpoint momenta. All real words and unvisited-disk witnesses are summed before the bound. No independence assumption is used. The interior-flight bound and longer-side argument are inherited deductions; the weighted first-image estimate completes both endpoint indices. Native 322 already pays the zero-clearance stratum at the original normalization. The new positive-width critical-sector consequence controls the complete leading coefficient by

   \[
   C_{\rm crit}\left(
      \frac{4\varepsilon(B)}{1-q_0^{1/4}}+
      m\theta_{\rm r}^{(m-1)/2}\right).
   \]

   This is a new unscaled endpoint/critical estimate. It is not an (m^{-2}) roof-height bound.

2. **Absolute inversion of the unchanged roof-interval event.** Native 334 uses the interval's own Fourier transform and the inherited exact-label BV theorem. For a union of at most (J) bounded intervals and roof-frequency cutoff (S), the exact inversion has tail at most (2JD/(\pi S)). The theorem keeps the full three-torus of integer labels and proves a summed-label bound without multiplying by the number of attainable labels. Conditional estimates use the actual event denominator and give the sharp-frequency variant of the certificate already present in native 331. Historical 64, 67 and 93 already contain other exact-inversion and tail certificates; the present direct interval proof uses only first-order all-label BV, without germ subtraction or a surviving smoothing kernel. The ordered raw bridge inherits the fixed-window evaluation from native 87 and isolates the remaining local derivative charge.

3. **Quantitative reconstruction of the section interface.** Native 333 checks the actual moving root, (q'_R<3), (|\theta'_R|<6), the section cap (|p|<5/6), coordinate side speeds, and the exact external multiplier assumptions. Historical native 72, 77 and 84 already proved the multiplier mechanism, entire occupation phase and moving-section strong-to-weak continuity. Those are inherited results, not claimed as discoveries here. The reference-measure convention is explicit: the function (1) represents (d\nu).

## Current theorem status

**The original full raw pointwise local limit theorem and the full four-coordinate inverse theorem are not completed by this revision.** The governing objective is unchanged. Under the retained scalar reduction and its actual hypotheses, the remaining same-roof positive-source condition is exactly native 329, `eq:lc-final-shortage`, with the full original comparison pool and the original order

\[
\lim_{B\to\infty}\limsup_{m\to\infty}\sup_{R,n,k}
m^2\operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}.
\]

The new endpoint estimate does not make this expression vanish. The retained native 87 fixed-window theorem evaluates the scalar interval-comparison term of the new bridge; its finite peak data also pay the reference modulus. On that route the remaining sufficient condition is the complete normalized local roof-variation charge. A new strong-operator theorem on growing frequency bands is a possible alternative method, not an additional prerequisite for this fixed-window implication. These are alternative routes to the original objective, not modifications of that objective. Conditioning and local inversion retain the exact denominator, arithmetic support and Jacobian hypotheses appropriate to their observations.

The historical full fixed-band spectral/arithmetic proofs and the weighted momentum-capacity theorem are retained. The latter is different from abundance of the actual same-roof comparison pool. No older solved condition is reintroduced as an open problem. Author proof bodies, auxiliary checks and independent expert reconstruction are different evidence levels; this package does not claim external expert certification or journal acceptance.

## Reading and reproduction

| File | Purpose |
| --- | --- |
| `main.tex`, `core/260_*.tex`–`core/335_*.tex` | Complete native active manuscript and proof bodies |
| `RESPONSE_TO_REFEREE.md` | Individually located replies to the controlling report and applicable historical concerns |
| `PROOF_DEPENDENCY_LEDGER.md` | Proven, inherited, conditional and unclosed dependencies |
| `SOURCE_PROVENANCE.md`, `SOURCE_MANIFEST.json` | Frozen commits, source trees, file identities and active source hash |
| `HISTORY_PRESERVATION_AUDIT.md`, `history/` | Original material and deduplicated historical native source preservation |
| `LITERATURE_HYPOTHESIS_AUDIT.md` | Exact primary-source versions and actual external hypotheses |
| `NEW_MATHEMATICAL_CHECKS.md`, `audit/` | Inequality, Jacobian, normalization, singularity and limit-order audits |
| `VALIDATION_REPORT.md`, `PUBLICATION_STATUS.json`, `evidence/` | Actual executions and precisely qualified publication status |

Install the dependencies in `requirements.txt`, a working `pdflatex` installation with the listed AMS/Latin Modern packages, and Poppler. Then run:

```bash
python3 -m pip install -r requirements.txt
bash build.sh
```

The validator checks the complete native input graph, byte identities of all inherited active proofs, all 660 preserved historical native objects, the exact controlling report, and all new mathematical verification programs. It invokes `pdflatex` three times, checks actual recorder inputs, unresolved references, missing characters and overfull boxes, and writes the PDF and receipts under `build/current/`. Run Python without `-O`; finite scripts deliberately retain their assertions. A successful build does not prove the continuous dynamical inputs or close the raw theorem.

The initial predecessor reconstruction passed 74 mathematical-program executions and compiled its 255-page manuscript. Its full source hash and the actual earlier GitHub run identifiers are recorded separately from this revision's checks. Failed integration attempts and their corrected causes are retained. The newly scoped workflow runs only for this revision branch and directory; no existing workflow is edited.
