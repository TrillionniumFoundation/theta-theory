# Execution Plan: Paper 3 representation calculus

- Created: 2026-07-07

## Phase 1: standalone article shell

- Build title, abstract, dependency statement, theorem map, and core theorem
  chain. `[done]`
- Compile standalone. `[done]`
- Keep the paper explicitly downstream of Paper 2. `[done]`

## Phase 2: theorem statement extraction

- Replace skeleton statements with polished statements from `main.tex`.
- Separate theorem assumptions by regime:
  - smooth nondegenerate;
  - degenerate viscosity regularization;
  - localized nondegenerate BSDE;
  - deterministic Hamiltonian shift.
- Current status: first interface cleanup done; `main.tex` now has a
  representation-window assumption and journal-facing theorem map.

## Phase 3: proof extraction

- Extract proofs for:
  - linearity obstruction;
  - first variation and calibrated generator;
  - BSDE Ito calculation;
  - Hamiltonian-shift identity.
- Keep proofs short in the main body.
- Move long deterministic calibration ledgers to appendix.
- Current status: short main-body proofs are in place for the listed items.

## Phase 4: appendix cleanup

- Extract only the appendix pieces needed for representation:
  - calibrated generator details;
  - gradient-vs-Z conversion;
  - sign convention;
  - post-derivation calibration guardrail.
- Remove duplicated singular-billiard proof ledgers that belong to Paper 1.
- Current status: gradient-vs-Z conversion and post-derivation calibration are
  now in the main text; the terminal-value sign convention and parabolic
  orientation ledger has also been added.

## Phase 5: journal-facing polish

- Choose primary target framing:
  - SPA/AAP/EJP for stochastic-analysis representation;
  - SICON for control/PDE representation.
- Add an optional robust-pricing example if targeting Finance and Stochastics.
  `[done: short stress-test illustration added]`
- Run full LaTeX compile and log hygiene. `[done for current draft]`
- Produce submission package checklist, referee-risk memo, and retained
  submission PDF. `[done]`
