# Submission map — A2 v33

Primary: `main.tex`, 21 pages in the local build. Read Theorem 1.3, Theorem 4.1, Section 7 and Section 8 for the additions; the six original v32 proof chapters remain active and complete.

Supplement R32: `retained/v32/main.tex`, with the entire reviewed native v32 source tree unchanged (`2a7d949f43dcb7b84d4a85ef8a4436349f615493`). It includes the fifteen declared documents and nested original submission maps. The included v31 volume remains Supplement R in the unchanged historical comparison.

The full current package has sixteen documents: the new primary plus the fifteen documents declared and qualified by the unchanged retained v32 validator. The v33 receipt embeds the complete retained receipt, with its relative paths, PDF hashes, page counts and historical layout disclosures. A flat source name such as `main.tex` in a nested receipt is interpreted relative to that receipt's own volume, not the new primary.

The full command is `python3 tools/validate_v33.py --all-volumes --require-checkout --expected-commit "$(git rev-parse HEAD)"`. It checks source pins, the retained native tree, the workflow digest and the actual checkout SHA, then reruns the whole validator chain. Preserved historical build wrappers, where required for old long volumes, operate only on staged layout copies and are disclosed in nested receipts; no retained mathematical source is edited.

`RESPONSE_TO_REFEREES.md` answers the five explicit v32 corrections and the broader resource objection. `PROOF_LEDGER.md` records assumptions and validation limits. The exact-source archive from the workflow is the complete distribution; a primary-only convenience ZIP is not a substitute for the retained-volume package.
