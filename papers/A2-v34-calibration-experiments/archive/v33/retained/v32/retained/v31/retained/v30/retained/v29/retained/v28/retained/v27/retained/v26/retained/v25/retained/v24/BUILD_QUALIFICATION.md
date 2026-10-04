# Exact-source qualification and preserved layout evidence

The mathematical checkpoint is `b656134c592e10c3f2a1a686be59ef0794a10cef`. Its run `37106889506` completed with **failure**, not success. The new 2,530-check suite, the selected retained v23/v22 suites, and the first six declared documents passed. The final 133-page Supplement S compiled with exit zero but had underfull vertical and bibliography boxes, correctly failing the strict diagnostics gate. Its artifact is `11268640461`.

The revised driver changes no mathematical source or retained repository path. It first checks the exact source pins and retained Git trees. All adjustments occur only in an output staging directory.

For historical v18, it archives the raw PDF and log (including the 1.88753pt overfull vertical box). It then inserts `\addtolength{\textheight}{8pt}` and `\raggedbottom` before the document body. The checkpoint run already demonstrated that this produces a 35-page document without final TeX diagnostics.

For Supplement S, it first builds the unchanged cross-referenced documents twice and archives the raw S PDF and log. It inserts `\raggedbottom` before the document body and `\raggedright` immediately after the bibliography environment begins. No bibliography text is removed. Programmatic reversibility checks ensure that deleting these exact insertions restores each original source, and both original and staged SHA-256 hashes are recorded. The reflowed document must pass the unchanged strict diagnostics gate; no `hbadness`/`vbadness` relaxation or warning filter is used.

Every delivered PDF, including the primary and all six declared companions, must have no final TeX warnings, unresolved references or overfull/underfull boxes. The raw historical PDFs/logs are separately labelled evidence, not warning-free delivered copies. A pass requires current-source equality after validation and the actual checked-out SHA matching the workflow trigger.

`verification/checkpoint-local` retains the initial source-content receipt. `verification/local` records the actual new primary-only run after the validator repair. Neither local receipt asserts authenticated checkout or hosted all-volume success. The final exact-SHA workflow must establish its own outcome, with actual logs and PDFs uploaded even on failure. Previous failed runs are not relabelled or erased. Finite arithmetic tests and compilation are not mathematical proof certification.
