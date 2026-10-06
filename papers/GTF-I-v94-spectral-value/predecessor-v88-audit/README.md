# General Theta Foundations I — Revision 88

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

This revision responds to both R57 reports on the exact v87 publication `aab076189b7276f6a0b4113b472ea09a7ac640cc`. Both reports are frozen verbatim and identified in `CONTROLLING_REPORTS.json`. The general mathematics journal objective and the paper's subject are unchanged. All previous mathematical sections remain byte-identical and active.

## New result: classical feedback and coherent reset width

The new acquisition class permits classical feedback between fresh blocks, arbitrary adaptive quantum control inside each block, and arbitrary joint receiver instruments with retained quantum memory. Conditional on the classical history, however, the complete fresh probe-reference system must be the same under both hypotheses and independent of the receiver's entire previous quantum memory. No old quantum system is fed coherently into a later acquisition. Reserved block budgets are at most `b`, and their sum is at most `N` on every record.

For fixed `E`, nonzero one-sided PSD tangent `H`, and quadratic allowance `Lambda`, every legal tuple with `sum_j ||F_j-E_j-sH_j||op <= Lambda s²` satisfies the three sharp local orders

| Tangent | Reset-width-b separation |
|---|---|
| `H in Ran(C_E)` | `min(1,sqrt(N)s)` |
| all missing-support blocks vanish and `Gamma_E(H) not in W_E` | `min(1,sqrt(Nb)s)` |
| some missing-support block is nonzero | `min(1,Ns)` |

The constants and sufficiently small interval depend on `E,H,Lambda`, but are uniform in every integer `1<=b<=N`, `N`, and the unknown allowed remainder. The lower designs are inherited parallel GHZ blocks or product witnesses and do not depend on that remainder. At `b=1`, classical feedback and receiver quantum memory do not improve the coherent tangent's square-root order; at `b=N` the reset class is the unrestricted adaptive class. These are local order statements, not equality of exact distances between arbitrary fixed pairs.

The proof uses conditional root fidelity on subnormalized receiver states. For nodewise fidelity deficits `a_h`, a pathwise total at most `A` yields final fidelity at least `(1-A)_+`. This does not assume unconditional independence of feedback-generated outputs. A fresh n-call adaptive block satisfies `d_B <= s(alpha*n+sqrt(r*n))`, retaining its full `n*r*s²` channel remainder. If `Q=max_paths sum n(h)²`, the resulting policy-sensitive trace bound is `min(2,2(alpha+sqrt(r))*s*sqrt(Q))`, with `Q<=bN`.

## Entry points

| File | Purpose |
|---|---|
| `quantitative.tex` / `paper.pdf` | Focused discrimination article and new reset-width proof |
| `supplement.tex` / `BINARY_SUPPLEMENT.pdf` | Complete current binary proof dependency package |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Independent, unchanged structural article |
| `main.tex` / `COMPLETE_REVISION.pdf` | Entire retained mathematical development |
| `sections/79-classical-feedback-reset-width.tex` | Precise protocol, conditional fidelity, adaptive-block estimate, sharp reset-width orders |
| `RESPONSE_TO_REFEREE.md` | All 15 required revisions, 20 comments, 21 release gates, and 16 risks |
| `PROOF_AUDIT.md` | Complete proof and quantifier audit of the new section |
| `FEEDBACK_SCHEMA.md` | Finite policy-budget certificate and its conditional interpretation |
| `editions/current-comparison88.tex` / `LITERATURE_AUDIT.md` | Theorem-level HMNW/Yuan–Fung and GHPS comparisons |
| `evidence/BUILD_RECEIPT.json` | Native source, four PDFs, regressions and reconstruction identities |
| `evidence/JOURNAL_PACKAGE.zip` | Reconstructible linked quantitative/supplement and independent structural objects |

```sh
python build_revision.py --check-source
python feedback_check.py
python feedback_budget.py examples/feedback-policy.json > policy-certificate.json
python feedback_budget.py examples/feedback-policy.json --verify policy-certificate.json
python build_revision.py --preflight        # local check, not source qualification
python build_revision.py --isolated         # at the committed native source
python build_revision.py --verify-published # read-only at publication/final review head
```

All 25 inherited regression suites run anew together with the new suite, under ordinary and optimized Python. The new suite has 8430 positive checks and 18 negative controls, including 180 complete finite quantum receiver-memory experiments on 45 public policies. It tests conditional fidelity and arithmetic; it does not prove the continuum theorem, certify a physical reset, execute an unknown measurement learner, or synthesize a recovery.

The v87 source baseline has 632 native files, 962 complete-edition labels, 475 quantitative/supplement labels jointly, and 116 structural labels. Changed entry, audit, and build files retain exact originals under `predecessor-v87-audit/`. Previous revision directories and review branches are unchanged.

Independent specialist priority clearance is not supplied by this revision. Arbitrary-pair full-boundary equivalence and entropy, growing-outcome minimax learning, general control/dictionary synthesis, unrestricted higher jets, and quantum-correlated imports across nominal reset blocks remain separate questions. The independent A/B/C/D aggregate flags remain false. Source identity and finite tests do not establish human authorship signatures or external referee approval.
