#!/usr/bin/env python3
"""Write exact-source author responses for all round-four revised papers."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"

RESPONSES = {
    "A1-exact-benchmarks": {
        "blockers": "The claimed torus Hamiltonian used a non-global coordinate and a branch map which is not a circle diffeomorphism; the entropic coefficient was assumed inside the calibration axioms.",
        "history": "No archived CM2 or round-three repair packet supplied a valid global mechanical realization.  Only the common-symbol and response-array calculations were retained.",
        "revision": "Replaced the torus construction by an exact symplectic cut-port map and its autonomous mapping-torus suspension; derived the exponential certainty equivalent from Kolmogorov--Nagumo/time-consistency axioms before matching the mechanical cocycle.",
        "markers": "Cut-port Hamiltonian suspension; Mechanical calibration of the exponential coefficient",
    },
    "A2-sinai-homological-pressure": {
        "blockers": "All-depth moving singularities, boundary-motion derivatives, quantitative Dolgopyat cancellation, covariance Livsic alternative, and the lattice--roof local-limit smoothing were incomplete.",
        "history": "A2_UNIFORM_GEOMETRY and A2_TEMPORAL_PACKET contained useful finite-horizon and polygon-UNI material, but they were orphaned and did not close the all-depth bundle or Fourier proof.",
        "revision": "Materialized the repair packets, added a current-augmented moving-cut Banach bundle, a frequency-adapted Dolgopyat block contraction, the induced-quotient Livsic theorem, and a four-region Fourier inversion with fixed-width smoothing and correct roof sign.",
        "markers": "Current-augmented moving-cut bundle; Uniform vector--clock local limit",
    },
    "A3-full-empirical-path-ldp": {
        "blockers": "A one-big-excursion event has ordinary exponential cost, invalidating the superexponential truncation of the empirical block proof; the cotangent annihilator used a non-Radon separator.",
        "history": "A3_DIRECT_PATH_LDP already suggested an induced/escape maximum, but did not fully construct survivor pressure and exposed zero-frequency phases.",
        "revision": "Constructed finite survivor operators and their monotone pressure, proved the max renewal/survivor formula, exposed-phase density and full direct LDP, and replaced the cotangent proof by a weighted bounded-strict Radon annihilator theorem.",
        "markers": "Defect-completed collision pressure; Radon annihilator and Hausdorff cotangent",
    },
    "A4-history-memory-universal-pressure": {
        "blockers": "General Ray processes are not norm-strong Feller; inverse-Laplace regularity and residue augmentation were unsupported; the normalized Feynman--Kac expression did not satisfy a tower.",
        "history": "A4_RAY_FELLER correctly separated bounded-strict and exposed-phase norm continuity, but the memory and nonlinear tower still needed reconstruction.",
        "revision": "Used a time-domain second-kind Volterra equation to construct the exact kernel, a minimal finite state-space realization of pole terms, a Doob-normalized Markov semigroup for the nonlinear tower, and an explicit rough/memory scaling theorem.",
        "markers": "Volterra construction of the exact memory; Exact nonlinear Doob tower",
    },
    "B1-microcanonical-preparation": {
        "blockers": "The safe boxes had volume of order epsilon cubed and could not have order-one activity, so the lattice minor-arc gap and shell coefficient were unproved.",
        "history": "The previous span-one packet repeated the same unsafe-box mechanism and was not retained.",
        "revision": "Separated the connected pressure into a strictly nondegenerate singleton sector and a short-time connected remainder; singleton domination now gives the uniform number-frequency gap, continuous-frequency decay, and mixed coefficient theorem.",
        "markers": "Singleton pressure gap; Source-uniform shell coefficient",
    },
    "B2-collision-clusters-dynamic-ldp": {
        "blockers": "A first-cycle estimate did not control all later recollisions, and later contacts were incorrectly assigned an independent time simplex; a local source ball was insufficient for the full entropy action.",
        "history": "B2_GLOBAL_SOURCE_LDP supplied useful real-source continuation and balance-preserving regularization, but the cyclic sector remained load-bearing.",
        "revision": "Added a first-cycle ancestral witness atlas, degenerate-stratum estimates, and forgetful graph surgery with an ancestral contact ledger; then materialized bounded real-source continuation, a positive collision right inverse, action-dense regularization, and full GC/MC joint LDPs.",
        "markers": "Ancestral contact ledger; Bounded real-source continuation",
    },
    "B3-hamilton-boltzmann-cotangents": {
        "blockers": "The Orlicz equivalence class could not detect singular collision measures; the full covariance nullspace and process-level Gaussian limit were not proved.",
        "history": "The old nullspace packet supplied a useful local-variation idea but inherited the wrong dual pair.",
        "revision": "Rebuilt the action dual on bounded-strict continuous collision works with Radon dual, proved singular-current separation by Urysohn tests and the exact graph gauge, then supplied local tangent density and a nuclear-space Mitoma/cumulant process CLT with typed collision response.",
        "markers": "Radon path-space Fenchel duality; Prepared joint fluctuating Boltzmann limit",
    },
    "B4-nonlinear-kinetic-semigroups": {
        "blockers": "The m-greater-than-six moment source was not Gaussian integrable, collisions did not conserve that weight, energy balls were not compact in the asserted topology, and the hierarchy correctors were only formal.",
        "history": "No archived derivation closed these points; the B2 tree and B3 fluctuation packets were reusable inputs.",
        "revision": "Introduced an energy-compact subquadratic topology, exact quadratic containment with zero collision Lyapunov cost, backward connected Duhamel correctors in a stable hierarchy functional algebra, energy-compatible comparison, and a one-time constrained semigroup on the conserved surface.",
        "markers": "Backward connected Duhamel correctors; Energy compactness and exponential containment",
    },
    "C1-information-risk-sensitive-saddles": {
        "blockers": "Deterministic contacts have no finite-volume Poisson compensator; the expected posterior error exponent was incorrectly identified with KL; posterior weights alone were not a sufficient dynamic state.",
        "history": "C1_BLOCK_NORMALIZED_CONTROL correctly proposed exact block normalizers but needed a uniform conditional source theorem and a corrected testing analysis.",
        "revision": "Proved conditional B2 source charts on complete correlation states, exact block-normalized DPP and Isaacs convergence, separated almost-sure KL odds from expected Chernoff error, and added finite-mean LAN/Bernstein--von Mises together with the correct posterior-plus-history state.",
        "markers": "Uniform conditional source chart; LAN and Bernstein--von Mises tangent",
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "blockers": "Strict-dual phase compactness lacked coercivity, the Sinai continuity ledger inherited the long-block error, optional projections on varying filtrations were unsupported, and the memory formula used the wrong generator/type.",
        "history": "C2_STRICT_MEMORY provided the correct Doob generator and compressed-memory tangent but was orphaned.",
        "revision": "Materialized that packet, added explicit weighted rate coercivity, rebuilt Sinai contractions from direct pressure, and proved uniform Doob-kernel convergence and optional-projection convergence on the resolved filtrations before passing likelihood, Girsanov, and BSDE diagrams.",
        "markers": "Coercive strict dual and phase compactness; Kernel and filtration convergence",
    },
    "D1-deterministic-theta-contractions": {
        "blockers": "The constrained contraction omitted its minimum constant; Gaussian fields and local likelihoods were centered at the limiting rather than finite-volume mean, so finite likelihoods were not exact densities.",
        "history": "No prior repair file addressed these algebraic errors.",
        "revision": "Normalized the constrained dual by subtracting the constrained minimum, restricted targets to a uniform interior gradient image, centered at DQ-epsilon, and proved exact mean-one local likelihoods without assuming a convergence rate for the means; process upgrades are tied to B3/C2 tightness.",
        "markers": "Normalized analytic--convex commutation theorem; Exact likelihood-ratio convergence",
    },
}


def render(name: str, d: dict[str, str]) -> str:
    return f"""# Author response to the round-three referee report

- Controlling revision: `revision/round4-referee-positive-closure-11paper-2026-08-30`
- Referee source: `REFEREE_REPORT_ROUND3_GPT56_PRO.md`
- Policy: positive closure; no theorem downgrade; no no-go substitution.

## Referee blockers

{d['blockers']}

## Historical-derivation audit

{d['history']}

## Revision and proof closure

{d['revision']}

## Exact source markers

`{d['markers']}`

The repository build and structural gates verify materialization and local
reference closure.  They do not substitute for independent external journal
certification.
"""


def main() -> None:
    index = [
        "# Round-four referee response index",
        "",
        "The new report branch was audited against the archived recursive/CM2 derivations and the eight round-three repair packets.  Useful packets were incorporated, but status language or orphan files were never counted as theorem credit without materialization in the controlling paper.",
        "",
        "| Paper | Response | Required source markers |",
        "|---|---|---|",
    ]
    for name, d in RESPONSES.items():
        path = PAPERS / name / "AUTHOR_RESPONSE_ROUND4.md"
        path.write_text(render(name, d), encoding="utf-8")
        index.append(
            f"| `{name}` | `papers/{name}/AUTHOR_RESPONSE_ROUND4.md` | {d['markers']} |"
        )
    index.extend([
        "",
        "## Historical conclusion",
        "",
        "The prior derivation corpus partially solved A2, A3, A4, B2, C1, and C2, but those results were orphaned or incomplete.  It did not solve the A1 global symplectic obstruction, the B1 safe-volume scaling error, the B3 Radon dual/process tightness problem, the B4 energy-topology problem, or the D1 normalization/centering errors.  The round-four packets add new tools for those gaps.",
        "",
    ])
    (ROOT / "ROUND4_REFEREE_RESPONSE.md").write_text(
        "\n".join(index), encoding="utf-8"
    )
    print(f"ROUND4_AUTHOR_RESPONSES_WRITTEN papers={len(RESPONSES)}")


if __name__ == "__main__":
    main()
