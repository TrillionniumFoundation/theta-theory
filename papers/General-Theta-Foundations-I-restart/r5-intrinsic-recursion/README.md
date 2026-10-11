# General Theta Foundations I — restart r5

The new main manuscript is `main.tex`, with seven native sections and `references.tex`. It is self-contained: it does not import an old manuscript to supply an omitted main proof. The unchanged sibling `../r4-causal-resolvent/` is the complementary mathematical supplement, preserving all 38 predecessor formal statements and their hypotheses.

The center is Theorem `thm:inward`: construct a recursive finite-label encoder from a static inward cover, a true-report-law pair moment inequality, and an envelope drift. The new construction removes the supplied recursive-machine premise and the terminal occupation/reference premise for this sufficient class. It is not a necessity theorem for every experiment.

Two verifications are Theorem `thm:filter` (arbitrary finite-dimensional, time-inhomogeneous intermittently mixing filters) and Theorem `thm:singular` (finite-read, nonreset, nonhomogeneous Cantor experiments with arbitrary initial mode law and time-varying mode masses). The general theorem precedes both. Resource composition and its limits are in Section 6 and `RESOURCE_ACCOUNTING.md`.

Reproduce: `python3 build.py --source-sha COMMIT --source-tree NATIVE_TREE`. The second argument is the exact native paper-subtree SHA. The builder checks native manifest/labels/references, runs regressions in ordinary and optimized Python, and typesets in two separate temporary source directories. It never pushes, installs dependencies, runs shell-escape TeX, or modifies a GitHub workflow. A local build is not a hosted-CI claim. Finite tests do not prove continuum theorems.

Read `REFEREE_RESPONSE.md`, `PROOF_LEDGER.md`, `THEOREM_MAP.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `PIPELINE_DERIVATION.md`, and the scope/literature/notation audits before interpreting any closure claim. The full optimal workspace/program/time/simulator-deficiency region, unknown-kernel adaptive acquisition, and a necessary-and-sufficient classification remain genuine research obligations.
