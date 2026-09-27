# General Theta Foundations I — Revision 49

**Sign and Magnitude Duality for Numerical Word Realizations**  
Qian Qi · 27 September 2026

Controlling latest located report: r30, `6ecf57a2d7ce804352f85daead8ec38e56377631`, reviewing v46. This revision starts from the completed v47 publication `98b59f3f45f63dacd8dba8cf132d23e54e7596e8`, whose source is `d0c5c82103f7f15ebc9351000c3914c78e1e35fe`. The report and source genealogy are distinct: no report on v47 is invented. The existing v48 branch had transport parts but no native paper at the surveyed commit; it is not overwritten or counted as verified mathematics.

Work branch: `revision/general-theta-foundations-i-v49-robust-duality-2026-09-27`. The separate referee-ready branch is published only after exact-source validation and isolated core rebuilding.

[Article](paper.pdf) · [Native source](main.tex) · [Response to r30](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Build receipt](evidence/BUILD_RECEIPT.json)

[Compact referee package](evidence/REFEREE_PACKAGE.zip) · [Standalone core](evidence/CORE_SOURCES.zip)

## Mathematical result

For arbitrary finite antisymmetric binary targets at a prescribed all-two-label profile, threshold-active entries fix the essential nonzero coordinates. Sign equations and a logarithmic linear system per chamber give a complete feasibility alternative, including zero entries and thresholds. Nonexistence has integer multiplicative certificates, with at most v+1 inequalities per chamber. Univariate algebraic threshold strata determine the optimum and an algebraic minimizing machine. There is no free persistent mixing selector.

The numerical example has one actual command epoch, two distinct commands, two positive seeds and their negatives, and two queries. At unit signal its exact optimal binary-TV error is t/2, where 500t^3-375t^2+540t-124=0 and 0.260362898747<t<0.260362898748. A five-entry identity proves the lower bound; explicit algebraic stochastic rows attain it. No rational machine with that profile attains the optimum. A separate rational orthogonal example gives exact error rho/20 at every positive horizon, even with unrestricted widths between two two-label cuts.

The scalar normal form and quarter-turn compatibility frontier are inherited from v47 and reproduced unchanged. Matrix fixed-sign Chebyshev feasibility, monomial logarithms and Farkas alternatives are explicitly credited. The new conclusion completes the controlled multilinear two-state problem, not arbitrary higher-width positive realization.

## Rebuild and exact checker

Use Python 3.12, SymPy 1.14.0, PyMuPDF 1.26.7, and AMS-compatible LaTeX with Latin Modern, mathrsfs, microtype, geometry, mathtools and booktabs. No font files are distributed.

```sh
python check_duality.py
python -O check_duality.py
python build.py --core-only
python build.py
```

The core ZIP contains one directory and is independently rebuildable. The archival build reads the sibling `GTF-I-v47-compatible-certificates` PDFs, or `GTF_V47_INPUT`. The full source archive contains those pinned inputs.

For a complete rational tensor, supply JSON fields `dims` and lexicographic `values`. Run `python dual_certificate.py input.json --delta 1/10`, where delta is mean tolerance (twice binary TV), or `--bisect 12`. Exact rational products determine every sign; no floating LP tolerance is used. The checker returns algebraic factor descriptions or input-bound sign/multiplicative rejection certificates. It enumerates sign chambers and can be exponential. A resource limit returns undetermined, never infeasible. The elimination checker need not return a support-minimal dual. The general symbolic univariate root algorithm is proved; the supplied software implements rational threshold decisions and certified bisection, plus the exact cubic worked certificate.

## Preservation and scope

[Unchanged v47 article](supporting-v47.pdf) · [Mathematical archive](complete-manuscript.pdf) · [Development archive](complete-development.pdf) · [Full rebuilding sources](evidence/SUBMISSION_SOURCES.zip)

All original paths, review branches and other work branches are unchanged. The entire v47 article and cumulative volumes are retained. Its mathematical modules remain in the current article; the finite-certificate copy has the explicitly registered corrections and new height lemma. Both earlier introductions remain as source files. Large archives are optional provenance, not the compact referee submission.

The primary resource is nonuniform clocked atomic-row label width. The global finite-table algorithm is distinct from polynomial displayed-candidate Gram verification, and from succinct-horizon or fixed-dimensional orthogonal complexity. Complete higher-width certification, unrelated A2/B4/C2 analytic gates and independent priority/proof assessment are not asserted. Build results establish reproducibility, not journal acceptance.
