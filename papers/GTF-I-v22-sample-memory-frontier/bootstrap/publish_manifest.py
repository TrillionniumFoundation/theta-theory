#!/usr/bin/env python3
"""Write the referee entry point from the executed receipt, not estimated counts."""
from __future__ import annotations
import json
from pathlib import Path
P = Path(__file__).resolve().parent.parent
R = json.loads((P / 'evidence/BUILD_RECEIPT.json').read_text())
D = 'papers/' + P.name
text = f'''# General Theta Foundations I — v22 referee package

**Causal Continuation and Statistical Resource Frontiers**

Source commit: `{R['source_commit']}`. Executed workflow run: `{R['workflow_run']}`.
Review baseline: `{R['review_commit']}`. Preserved v21 publication: `{R['base_commit']}`.

Canonical English article: **{R['canonical_pages']} pages**. Complete development: **{R['complete_pages']} pages**, including all **{R['predecessor_pages']} predecessor pages** with identical text and raster rendering.

## Referee entry points

- [Full English article]({D}/paper.pdf) and [LaTeX entry point]({D}/main.tex).
- [Point-by-point response]({D}/RESPONSE_TO_REFEREE.md).
- [Complete preserved development]({D}/complete-development.pdf).
- [Executed build receipt]({D}/evidence/BUILD_RECEIPT.json), [new theorem locations]({D}/evidence/THEOREM_LOCATIONS.json), and [portable source archive]({D}/evidence/SUBMISSION_SOURCES.zip).
- [Resource ledger]({D}/RESOURCE_LEDGER.md), [proof status]({D}/PROOF_STATUS.json), [pipeline status]({D}/PIPELINE_STATUS.json), [history audit]({D}/HISTORY_AUDIT.md), and [literature comparison]({D}/LITERATURE_CROSSWALK.md).

## Mathematical revision

The article retains the v20 and v21 theorem chains and adds an exact all-stochastic-machine Bayesian multicut theorem for erasure-revelation experiments with arbitrary fixed priors; explicit sample/width inversions; a polynomial-horizon bounded-state selection theorem; active-update transport; a third resource regime for the original positive-noise collision experiment; and bounded-state confidence amplification.

The physical constructions now exhibit preparation/peak-width points (399, 40,602), (320,000, 1,604), and (12,800 times 2^400, 12), in the declared externally clocked model. They have the same expected-score objective; none is misrepresented as the exact physical fixed-sample optimum. The exact revelation-family frontier is a separate statistical theorem, not a substituted physical lower bound.

Executed diagnostics: **{R['finite_diagnostic_checks']:,}**, including **{R['new_finite_diagnostic_checks']:,}** new checks and **{R['exhaustive_transition_tables_evaluated']:,}** small transition-table/reachable-law evaluations. All **{R['negative_control_executions']}** negative-control executions were detected, and normal/optimized Python outputs agree. The article has no undefined references or overfull boxes. All **{R['unchanged_math_modules_verified']}** unchanged inherited mathematical modules remain in the canonical article. The v21 organizing theorem and proof are preserved verbatim in the appendix.

## Scope and unresolved publication obligations

The original Norberg proof-level comparison remains incomplete: no original full proof text was obtained. Exact physical peak width and the optimal fixed-sample physical frontier are not asserted. A2 remains an independent primary chain; the historical B4 and broad C2 aggregates are not declared closed. Their targets and sources remain preserved.

These are supplied analytic proofs and executed reproducibility checks, not independent mathematical certification or a journal acceptance claim. No predecessor manuscript, review, or other historical repository path was modified or deleted.
'''
(P.parent.parent / 'GENERAL_THETA_FOUNDATIONS_I_V22_REVIEW_READY.md').write_text(text, encoding='utf-8')
