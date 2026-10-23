# General Theta Foundations I: complete controller-rigidity publication

This is the actual publication child of source `36f579de5aed425f238c2844fe86a8b230d45140`, not a build of the publication child itself. The source continues the unchanged complete R80 publication `304357fcada3771a5d01a29cdd93b4f42434cb7d`. All repository writes used the connected GitHub plugin; no prior author source, report or unrelated paper was overwritten.

## Read the complete current manuscript

- [Full main article, 75 pages](General_Theta_Foundations_I_Controller_Rigidity.pdf)
- [Current technical supplement, 196 pages](General_Theta_Foundations_I_Controller_Rigidity_Supplement.pdf)
- [Independent retained R58 companion, 37 pages](General_Theta_Foundations_I_Retained_Companion_R58.pdf)
- [Complete native source and build entry](../r80-controller-rigidity-addendum/README.md)
- [Item-wise author response](../r80-controller-rigidity-addendum/RESPONSE_TO_REFEREE.md)
- [Proof dependencies](../r80-controller-rigidity-addendum/THEOREM_DEPENDENCIES.json)
- [Exact content preservation map](../r80-controller-rigidity-addendum/PRESERVATION_MAP.md)
- [Current open research conditions](../r80-controller-rigidity-addendum/RESEARCH_STATUS.md)

The new result is Theorem 6.1 on pages 26--28. Within the fully specified two-model, two-label, six-parameter scalar family, a controller family's excess cost is o(sqrt(epsilon)) if and only if its five stated first-order coordinate asymptotics hold. Arbitrary discontinuous selections are allowed; xi is free. Leakage gamma must be o(epsilon), not merely O(epsilon). The converse establishes actual properness and both model costs. This is not a general-instrument theorem or an exact finite-epsilon optimizer formula.

The 267 R80 declarations, exact sharp value asymptotic and finite-search saturation classification are inherited. The current index has 268 declarations. The actual strict source run executed 33 diagnostic suites in ordinary and optimized Python, with identical paired outputs and 432064 finite checks, and compiled every current document natively. This evidence does not replace the written proofs. No new external referee verdict, human specialist priority certificate or editorial acceptance is claimed.

## Reproduction and identity

Checkout source SHA `36f579de5aed425f238c2844fe86a8b230d45140`, materialize both the addendum and its pinned R80 sibling, and run `python3 -B build.py --source-commit 36f579de5aed425f238c2844fe86a8b230d45140 --out /tmp/theta-rigidity-reproduction` from the addendum directory. It verifies the inherited tree, full source seal, preserved wrapper inputs, all theorem locators, diagnostics and native logs. A fresh output directory is required.

The companion is also directly compiled by changing to the pinned sibling's `companion-r58/` directory and running native LaTeX there. The convenience `companion.tex` wrapper requires that companion directory in TEXINPUTS for its nested section inputs; the supplied build script sets the correct source search paths and compiles it in its own directory.

`PUBLICATION_RECEIPT.json` gives the exact source and artifact hashes. `REMOTE_SOURCE_READBACK.json` distinguishes the local authoring commit from the connector-created remote source carrier, whose complete repository tree is identical. The actual remote-source run was performed after fetching that carrier. The hosted-run query returned zero runs for this source; no hosted CI success is invented. `VALIDATION_LOGS.tar.gz` retains actual diagnostics and native logs. Run `python3 -B verify_publication.py` to verify every deposited artifact hash.
