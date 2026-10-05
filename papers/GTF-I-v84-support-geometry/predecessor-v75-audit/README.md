# General Theta Foundations I — Revision 75

**Focused quantitative article:** *Finite-Use Geometry of Binary Qubit Measurements* (`quantitative.tex`, `paper.pdf`).

**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* (`structural.tex`, `STRUCTURAL_PAPER.pdf`). Its mathematics is inherited, with its fresh classical nondisturbing-probe hypotheses.

**Complete research edition:** *General Theta Foundations I: Stochastic Realization and Finite-Use Measurement Geometry* (`main.tex`, `COMPLETE_REVISION.pdf`). It retains every one of the 522 v74 complete-edition labels and the full active proof chain. The long former quantitative overview is retained in this edition while the focused article opens with the new theorems.

## New theorem chain

The target is the full body of ordered binary qubit measurements

    E+ = ((1+b) I + x.sigma)/2,   E- = I-E+,   |b|+|x| <= 1.

For eigenvalues `0 <= q <= p <= 1`, define

    T_N(s,t) = |s-t| sqrt(N / (max{s(1-s),t(1-t)} + 1/N)),
    K_N(p,q) = (p-q) sqrt(N / (p(1-p)+q(1-q) + 1/N)).

For a pair of effects let `H` be the sum of the two spectral `T_N` terms and `min(K,K')` times the angle; when either effect is scalar the angular term is zero. Theorem `thm:biasedmetric75` proves, for every integer `N >= 1`,

    (1/8192) min(1,H) <= d_N <= min(2,3H).

The metric is the unhalved final-state trace norm over all common reference-assisted adaptive testers, including feedback and bounded public stopping. The exact one-use identity is `d_1=|b-b'|+|x-x'|`.

The angular proof uses an explicit scalar-overlap measurement dilation and two complementary lower witnesses. Spectral endpoint tests prevent angular changes from hiding either eigenvalue. This resolves the single-rank-face regime separately from the projective edge.

Theorem `thm:biasedcover75` proves the full-body small-error law

    C_N(delta) ~ N^2 log(N+2) delta^(-4).

The constants are absolute and uniform in `N >= 1` and `0 < delta <= delta_0` for an absolute sufficiently small cap. Lower centres may be any legal memoryless device of the same binary interface. The proof combines dyadic projective-corner packing with a matching finite rational lattice count; it makes no regularity assumption on redundant spectral charts at scalar effects.

Theorem `thm:biasedcodec75` attains the order with one index charging both eigenvalues and all identifiable direction data. Its optimal payload is

    2 log2 N + log2 log(N+2) + 4 log2(1/delta) + O(1).

The inherited unbiased-ball metric, regular-family weighted covering criterion, contact trichotomy, and exact visibility/direction code remain active. They have their own target and small-error conventions.

## Exact implementation

`biased_codec.py` accepts rational bias and Cartesian Bloch coordinates, including vectors of irrational norm. Every sign comparison, layer choice, index and decoded matrix entry is exact. Every in-range word decodes to a legal rational measurement; target replay checks the stricter canonical encoding relation.

```bash
python biased_codec.py encode --input inputs/biased-measurement-3.json --horizon 1 --error 1/4
python check_biased_geometry.py
```

The reference encoder enumerates an ordered spectral-pair table. Its arithmetic-operation count is quadratic in the numerical spectral grid size and its stored row-count table is linear in that size. Payload, encoder workspace, expanded matrices, syntax and physical quantum hardware are distinct resources. The stored `delta/2` certificate is a proved construction budget, not a computation of the optimum adaptive distance. See `BIASED_CODEC_SCHEMA.md` and `RESOURCE_LEDGER.md`.

## Reproduction and review

Install the Python versions in `requirements.txt`, together with pdfLaTeX, AMS, Latin Modern and the usual LaTeX packages. Then run:

```bash
python build_revision.py --isolated
```

The builder runs the new exact suite and all eleven inherited suites in normal and optimized Python modes; typesets all three manuscripts; rejects unresolved references, citations and overfull/underfull boxes; checks every prior proof label; and rebuilds the native archive in an empty directory. Actual counts, PDF hashes, page checks and source identity are in `evidence/BUILD_RECEIPT.json` and its associated inventories.

The focused `evidence/JOURNAL_PACKAGE.zip` contains the quantitative and structural articles, PDFs, active sources, comparison/response material and an independent verifier. It compiles without historical PDFs. The `evidence/RESEARCH_PACKAGE.zip` includes the complete research edition and exact tools.

After publication, `python build_revision.py --verify-published` reconstructs the committed PDFs and finite evidence without altering the submitted source. The dedicated v75 GitHub workflow verifies the actual pushed SHA. Its external run record is distinct from the source-build receipt and from any independent mathematical or authorship certification.

## Sources and branches

Completed predecessor: v74 final head `8477a4c44cbed327068ab895c244f2ddfa86e27a`.

Inherited v75 work anchor: `d9ed8e4422fccd7e849ba5e72dc0df447b9d2470`.

Controlling external report r48: `0fd7db3c634b85ad93a4d205b95bf04b6cb7e476`.

Controlling proof/pipeline audit r48: `53371065e8684e33bd3f04748dbea652011c5a7e`.

Work branch: `revision/general-theta-foundations-i-v75-full-measurement-body-2026-10-04`.

Referee branch: `revision/general-theta-foundations-i-v75-referee-ready-2026-10-04`.

The response addresses all twenty required revisions and thirty-six detailed comments. `CONTROLLING_REPORTS.json` fixes the source identities, `HISTORY_AND_PIPELINE_AUDIT.md` traces the entire development, and `PRESERVATION_MANIFEST.json` records all 238 predecessor native files. Forty-nine inherited section files are byte-identical; section 50 receives the requested explanatory additions, and section 44 adds the verified literature citation. Prior files in every earlier directory remain unchanged.

Fiurasek–Micuda (2009) is now directly compared with the 2014, 2018 and 2021 measurement-discrimination results. A theorem-specific independent review brief is supplied. No independent human priority opinion, human signature, or journal acceptance is asserted. The general-journal objective and the distinct historical analytic-pipeline status are retained.
