# R74 structural-extension handoff

These files are author-revision source and author-team diagnostics. They are not an independent referee report, a proof-assistant certificate, a human expert endorsement, or an editorial decision. No repository branch or remote was modified by this subagent. The two native source files are frozen for parent integration.

## Deliverables and frozen hashes

| File | SHA256 |
|---|---|
| `37-contrast-memory.tex` | `cbd4fffa320472e1273cf570b6db008bfb849a256f0a638ef8ea6588b3daae17` |
| `38-quotient-memory.tex` | `092daa2329adafb71772fa0ae1bfbdfed99e5eaf88d725e5b5aa38c9cd5d4a17` |
| `diagnostics_r74_contrast.py` | `264925751ad2f16f0e403324c3cc934f055f9c9d111da8ab9995cdebfee3471e` |
| `CONTRAST_DIAGNOSTICS.json` | `a81b22a0bfcef68d123daa57ea33b89add3af31e154bdece31aa0887235fc534` |

`bibliography-r74-structural.tex` contains the four precise citation entries. `structural.md` is the earlier full mathematical development draft; the final native files add the explicit payoff witness, robust finite-table corollary, and complete S3 contrast theorem. The Markdown draft's KPT publication metadata were corrected during final primary-source verification. The native files cite only keys and were unaffected by that correction.

## Theorem map and scope

| Native label | Mathematical assertion | Essential dependencies and scope |
|---|---|---|
| `thm:r74-low-contrast` | For every finite observable group and every finite outcome set, sufficiently small positive terminal contrast attains the minimum permutation-module size exactly. | R73 probability-core normal form and module lower bound; elementary equivariant projection and explicit positive preparation/decoder. Zero-mean outputs are removed and restored; no extra strict-positivity hypothesis. |
| `thm:r74-contrast-thresholds` | Every memory budget gives an attained closed initial contrast interval; finitely many exact transitions; algebraic thresholds for algebraic data. | Compactness, finite group actions, decoder mixing; classical QE only as a proved finite procedure, not an execution claim. Rational thresholds require the normal-subgroup LP reduction. |
| `prop:r74-s3-contrast` | Retained prepared-qubit S3 example: core 3 then 6 at threshold 2/3; prescribed-start memory 4 then 6. | Faithful S3 sets of size at most five; four explicit matrices spanning all endomorphisms of its two-dimensional standard module; decoder bounds. |
| `lem:r74-normal-orbits` | Within-orbit preparation is absorbed into the decoder for normal stabilizers; repeated quotient types merge. | Normality, essential to the coset-invariance calculation. The diagnostic includes a nonnormal S3 negative control. |
| `thm:r74-quotient-lp` | Exact subgroup-family linear programs and same-field algebraic optimal controllers. | Every subgroup of G normal (finite Dedekind groups, including all finite abelian groups); no unrestricted nonabelian LP claim. Minimal observable G gives N=|G|. |
| `thm:r74-quotient-dual` | Explicit necessary and sufficient payoff inequalities, strict rational infeasibility witnesses, quantitative stability, and attained primal/dual contrast endpoint formula. | Compact quotient probability polytopes; direct closest-point separation proof; finite facets handle affine degeneracy. |
| `cor:r74-abelian-cover` | Exact character-cover formula for the permutation-module bound, attained at small contrast. | Finite abelian G; cyclic module multiplicity one; real conjugate pairs treated as two-dimensional real summands. |
| `prop:r74-circuit-transition` | C2^4 five-character circuit: fixed d=6, N=16, module bound 10; exact positive cores 10/12 and memory 11/13 at threshold 3/5. | All budget-at-most-eleven action families classified analytically; explicit rational Farkas witnesses; matching quotient constructions. This is a special exact family, not a formula for every response. |
| `cor:r74-circuit-robust` | On the same finite group/command quotient, sup-norm perturbations less than (5t-3)/18 retain core >=12 and memory >=13 for t>3/5. | Five active Fourier modes remain nonzero; explicit witness norm <=9/4. The radius is sufficient, not claimed sharp. Matching upper 13 is only proved on the exact contrast line. |

All sharp families charge the pure start through the inherited R73 theorem. At t=0 the observable group changes and memory is separately one. Terminal readout contrast is distinguished from command damping, strict positivity of a complete instrument, and general Theta pipeline assumptions.

## Actual diagnostic executions

Both commands completed successfully:

```text
python3 diagnostics_r74_contrast.py --output CONTRAST_DIAGNOSTICS.json
python3 -O diagnostics_r74_contrast.py --output CONTRAST_DIAGNOSTICS_OPTIMIZED.json
```

The resulting JSON files are byte-identical. No Python `assert` gates the checks. Arithmetic is exact `fractions.Fraction`; there are 3,173 exact checks and zero floating checks:

| Group | Count |
|---|---:|
| Circuit observability and Fourier | 111 |
| Exact quotient controllers and initializer | 1,217 |
| Explicit Farkas witnesses | 1,793 |
| S3 coefficient injectivity and threshold | 52 |

The diagnostic checks the circuit and its six-dimensional observable span; exact decoder bounds and all group responses; group multiplication for both constructed actions; the charged pure initializer; all 26 singleton/pair witness partitions and their exact norm table; one interior perturbed table with an additional Fourier mode; the four explicit S3 matrices and their rank; the S3 decoder at and below the threshold; and a nonnormal-stabilizer counterexample to unrestricted absorption.

These are finite identity checks for the displayed constructions and certificates. The universal lower bounds, general finite-G saturation theorem, all contrast intervals, and subgroup LP duality rest on the written proofs. No general LP or QE solver was run by this diagnostic. The independent author-team challenge agent separately enumerated subgroup families; its record is distinct and must retain its own source identity and limitations.

No native LaTeX compilation is claimed by this subagent. Parent integration must compile the complete manuscript with its inherited macros, cross-references and bibliography.

## Primary literature and priority boundary

1. **GPT13:** J. Gouveia, P. A. Parrilo, R. R. Thomas, *Lifts of convex sets and cone factorizations*, Mathematics of Operations Research 38(2) (2013), 248–264, DOI `10.1287/moor.1120.0575`; https://arxiv.org/pdf/1111.3164 . Theorem 2.4 covers cone lifts and factorizations; Theorem 2.12 covers their symmetric version. A response probability table is not automatically a complete slack operator.
2. **KPT10:** V. Kaibel, K. Pashkovich, D. O. Theis, *Symmetry matters for sizes of extended formulations*, SIAM Journal on Discrete Mathematics 26(3) (2012), 1361–1382, DOI `10.1137/110839813`; https://arxiv.org/pdf/0911.3712 . Definition 11 and Lemma 12 concern coordinate-symmetric sections. The key `KPT10` is an integration identifier only: the full journal publication is **2012**. The preliminary IPCO version was 2010, LNCS 6080, 135–148. Publisher verification: https://epubs.siam.org/doi/10.1137/110839813 .
3. **GillisGlineur12:** N. Gillis, F. Glineur, *On the geometric interpretation of the nonnegative rank*, Linear Algebra and its Applications 437(11) (2012), 2685–2712, DOI `10.1016/j.laa.2012.06.038`; https://arxiv.org/pdf/1009.0880 . The restricted-rank geometry cautions against confining every hidden state to the target observable linear space.
4. **BocciCarliniRapallo11:** C. Bocci, E. Carlini, F. Rapallo, *Perturbation of matrices and nonnegative rank with a view toward statistical models*, SIAM Journal on Matrix Analysis and Applications 32(4) (2011), 1500–1512, DOI `10.1137/110825455`; https://arxiv.org/pdf/1010.3566 . Theorem 3.1 and Proposition 3.2 concern local nondecrease and barycentric perturbation of ordinary nonnegative rank.

All four full primary preprints were opened and relevant portions inspected. The final metadata recheck used author arXiv records and publisher/institution records. Do not claim invention of positive factorization, equivariance, convex separation, mixing-based positivity, or generic perturbation persistence. The proved consequences here concern the common group action for all command words, the exact permutation-module saturation value, normal-orbit absorption, charged prescribed start, and the exact threshold families.

A search also located a Gillis monograph statement about nonnegative rank under rank-one perturbations. The author-hosted large PDF could not be accessed (tool size limit, then HTTP 503). Its theorem was not inspected and is not used as a proof or claimed priority clearance. No exhaustive novelty clearance or specialist approval has been obtained.
