# General Theta Foundations I — R73 author revision

**General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, by Qian Qi.

This is the complete author-revision packet. The central new proof classifies the exact stochastic memory of compactly reversible controlled responses. The original causal, predictive, finite-resource, quantum measurement, reset, discrimination, variational, dual and geometric developments remain in the current paired documents or their explicitly preserved independent sources. The Annals / Acta / Inventiones / JAMS research objective is retained.

## Immutable source and delivered documents

The mathematical source is commit **[`e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b`](https://github.com/TrillionniumFoundation/theta-theory/tree/e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b/papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form)**, paper tree **`0507d04ad0bebd20cb0ce609ab94f7cc67d11f56`**. The publication is a later child commit containing this entry and the actual artifacts. For an immutable publication URL, use the full containing commit SHA rather than the moving branch name.

| Document | Native PDF | Pages | SHA-256 |
|---|---|---:|---|
| manuscript | [General_Theta_Foundations_I_R73.pdf](General_Theta_Foundations_I_R73.pdf) | 26 | `718e9f5b6f30883ab8faa9380c23d92aa5a4d00e593805f371d01bdb84bc27eb` |
| supplement | [General_Theta_Foundations_I_R73_Supplement.pdf](General_Theta_Foundations_I_R73_Supplement.pdf) | 143 | `2c21d462cdd9bc4b7d273e8741405454f630ad9b2fac819540a175e467e5d4fb` |
| companion | [General_Theta_Foundations_I_R73_Retained_Companion_R58.pdf](General_Theta_Foundations_I_R73_Retained_Companion_R58.pdf) | 37 | `5bdbe05bcb4955fc4dca36265457675fb94ef86c0ae5c54fd711548f5758c3a3` |

Keep the main and supplement filenames together to preserve their cross-document links.

The [complete native source archive](General_Theta_Foundations_I_R73_Source.zip) includes all 156 current source files and an external archive-provenance record. [RESPONSE_TO_REFEREE.md](RESPONSE_TO_REFEREE.md) is the complete 10-major-request and 40-technical-comment response. The unchanged original predecessor source is commit `5463d93f0f22a7459efba8c44af1f8b326d92c34`; the latest applicable substantive report is commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`. R65 assessed R65, and no endorsement of R66–R73 is inferred.

## Mathematical reading path

Begin with the main article's definitions and inherited finite-realizability criterion. Then read the following current statements and their full proofs. Page numbers below are from the actual final native main PDF.

| Stable label | Current statement number | Main page |
|---|---:|---:|
| `thm:r73-normal-form` | 4.1 | 8 |
| `thm:r73-memory-formula` | 4.2 | 10 |
| `cor:r73-group-bound` | 4.3 | 10 |
| `cor:r73-rank-rigidity` | 4.4 | 10 |
| `prop:r73-symmetric-family` | 4.5 | 11 |
| `prop:r73-decoder-obstruction` | 4.6 | 11 |
| `thm:r73-algebraic-synthesis` | 5.2 | 14 |
| `thm:r73-finite-tests` | 6.1 | 16 |
| `thm:r73-memory-plateau` | 6.2 | 17 |
| `prop:r73-period-four` | 6.3 | 18 |

The key formula is $m(b)=\min\{N_b,1+\kappa_G(b)\}$, where the preparation is a prescribed pure live label and $\kappa_G(b)$ retains bounded probability decoders. The symmetric-group family gives exact $k+1$ stochastic versus $k!$ deterministic-transition labels. The strict $S_3$ example shows why group, rank and permutation-module data alone are insufficient. Algebraic synthesis and finite separation then give a matched stable-memory interval for a specified common background.

The companion technical lemma in the current supplement proves the finite-chain projection directly. The supplement retains the full periodic, arithmetic, leakage, stopping, risk, rank and geometric bodies with their original hypotheses. The original actual-history comparison remains proved in the main article. See the source [theorem map](../r73-reversible-normal-form/THEOREM_MAP.md), [preservation map](../r73-reversible-normal-form/PRESERVATION_MAP.md), [priority record](../r73-reversible-normal-form/LITERATURE_AND_PRIORITY.md) and [research status](../r73-reversible-normal-form/RESEARCH_STATUS.md) for their distinct roles.

## Actual validation and its limits

[BUILD_RECEIPT.json](BUILD_RECEIPT.json) records a **strict local PASS at `e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b`**. It checked the actual HEAD, exact paper tree, unchanged R72 tree and inherited diagnostic identities; executed all 14 suites in ordinary and optimized Python with identical output; and rebuilt all three PDFs with three native LaTeX passes each. It reports **28,933 finite checks: 16,900 exact and 12,033 floating**, and the actual **185-entry statement index, including all 171 inherited labels**. Final logs contain no undefined or multiply defined labels or overfull boxes.

[PDF_VISUAL_QA.json](PDF_VISUAL_QA.json) separately records all-page rendering, actual visual inspection and final-PDF identity comparison. [HANDOFF_AUDIT.json](HANDOFF_AUDIT.json) is a bounded AI handoff audit. [NATIVE_AND_DIAGNOSTIC_LOGS.tar.gz](NATIVE_AND_DIAGNOSTIC_LOGS.tar.gz) retains native logs, recorder/auxiliary files and every executed diagnostic output. The source [proof audit](../r73-reversible-normal-form/PROOF_AUDIT.md) identifies the separately challenged proof inputs and their exact hashes.

These are distinct forms of evidence. No formal proof-assistant check, independent human referee approval, journal submission or editorial decision is claimed. [SOURCE_REMOTE_READBACK.json](SOURCE_REMOTE_READBACK.json) records the actual matching-SHA hosted-run query; the historical R65 success is never reported as R73 CI. The general fixed-memory squared-sign risk frontier, unrestricted controlled boundary optimization, sharp plateau endpoints and independent A1/A2/Theta obligations remain explicitly open.

## Reproduce this edition

Use Python 3 with the source's exact `requirements.txt` versions and a working native `pdflatex` installation. In a Git checkout of this repository:

```bash
git checkout e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b
cd papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form
python3 verify.py --source-commit e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b --out /tmp/general-theta-r73-verified
```

The output directory must be fresh and outside the source. In the standalone archive, `python3 verify.py --draft --out /tmp/general-theta-r73-draft` builds a readable packet but deliberately does not authenticate a Git source SHA or issue a strict PASS.

[DELIVERY_RECORD.json](DELIVERY_RECORD.json) fixes the source, artifact and execution relationship. [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json) hashes every publication file except itself. No predecessor paper or historical branch is overwritten by this independent revision branch.
