#!/usr/bin/env python3
"""Materialize the round-five referee repairs into the eleven controlling papers."""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
FRAG = ROOT / "revision" / "round5-referee"

PAPER_DATA = {
    "A1-exact-benchmarks": {
        "code": "A1",
        "fragment": "A1_RECUT_COCYCLE_RESPONSE.tex",
        "labels": ["lem:r5-a1-recut", "thm:r5-a1-return", "prop:r5-a1-work", "thm:r5-a1-response"],
        "repairs": [
            "recut incoming/outgoing ports onto one exact symplectic section",
            "construct a single-valued autonomous first-return suspension",
            "replace the non-descending one-form by an exact-symplectic work cocycle",
            "type all response operators on one conjugated Banach fibre",
        ],
    },
    "A2-sinai-homological-pressure": {
        "code": "A2",
        "fragment": "A2_UNIFORM_PACKET_LLT.tex",
        "labels": ["prop:r5-a2-bundle", "lem:r5-a2-certificate", "thm:r5-a2-spectrum", "thm:r5-a2-llt"],
        "repairs": [
            "construct a finite moving-cut Banach bundle with uniform Lasota--Yorke bounds",
            "supply a joint homology--roof non-arithmeticity/UNI certificate",
            "prove compact- and high-frequency twisted spectral estimates",
            "replace the false wide-window LLT by local, central, and saturated regimes",
        ],
    },
    "A3-full-empirical-path-ldp": {
        "code": "A3",
        "fragment": "A3_SURVIVOR_ENTROPY_LDP.tex",
        "labels": ["thm:r5-a3-pressure", "lem:r5-a3-entropy", "thm:r5-a3-induced", "thm:r5-a3-two-clock"],
        "repairs": [
            "retain escape as a cemetery-state pressure branch",
            "replace periodic-orbit recovery by entropy-preserving Markov recovery",
            "prove the direct induced level-three lower bound",
            "construct bounded terminal surgery for collision and physical clocks",
        ],
    },
    "A4-history-memory-universal-pressure": {
        "code": "A4",
        "fragment": "A4_HISTORY_DOOB_MEMORY_ROUGH.tex",
        "labels": ["thm:r5-a4-history", "prop:r5-a4-doob", "thm:r5-a4-memory", "thm:r5-a4-rough"],
        "repairs": [
            "type the exact state on complete history",
            "replace fixed-denominator normalization by a space-time harmonic Doob cocycle",
            "derive the time-domain Volterra kernel from the corrected A2 spectral packet",
            "include the deterministic rough area anomaly and its bracket drift",
        ],
    },
    "B1-microcanonical-preparation": {
        "code": "B1",
        "fragment": "B1_FINITE_SADDLE_COEFFICIENT.tex",
        "labels": ["lem:r5-b1-convex", "thm:r5-b1-saddle", "thm:r5-b1-coefficient", "thm:r5-b1-transfer"],
        "repairs": [
            "fix the singleton activity/speed normalization",
            "center Fourier inversion at the exact finite-volume saddle",
            "prove compact minor-arc and global continuous-frequency estimates",
            "derive the source-uniform mixed shell coefficient and Schur complement",
        ],
    },
    "B2-collision-clusters-dynamic-ldp": {
        "code": "B2",
        "fragment": "B2_CONTACT_STRATA_CONTINUATION.tex",
        "labels": ["lem:r5-b2-atlas", "thm:r5-b2-pivot", "thm:r5-b2-cumulant", "thm:r5-b2-continuation", "thm:r5-b2-ldp"],
        "repairs": [
            "stratify actual deterministic contact-coordinate charts",
            "obtain one first-surplus tube gain without deleting any collision",
            "sum all later actual contacts by an ordered factorial recursion",
            "continue finite source balls by exact hierarchy blocks and prove full recovery",
        ],
    },
    "B3-hamilton-boltzmann-cotangents": {
        "code": "B3",
        "fragment": "B3_WEIGHTED_GAUGE_GAUSSIAN.tex",
        "labels": ["thm:r5-b3-right-inverse", "thm:r5-b3-gauge", "thm:r5-b3-duality", "thm:r5-b3-gaussian"],
        "repairs": [
            "move the gauge complex to a quadratic weighted exponential Orlicz heart",
            "construct a quantitative balance right inverse",
            "exclude singular/finitely-additive dual functionals",
            "correct the collision bracket and prove nuclear-space process tightness",
        ],
    },
    "B4-nonlinear-kinetic-semigroups": {
        "code": "B4",
        "fragment": "B4_HIERARCHY_HAMILTONIAN_DOMAIN.tex",
        "labels": ["lem:r5-b4-algebra", "thm:r5-b4-exact", "thm:r5-b4-correctors", "thm:r5-b4-comparison"],
        "repairs": [
            "define a genuine convolution algebra of hierarchy observables",
            "keep the exact intermediate state in the complete deterministic hierarchy",
            "prove convergence of the infinite connected-corrector series",
            "place the exponential Hamiltonian on a Maxwellian exponential-moment domain",
        ],
    },
    "C1-information-risk-sensitive-saddles": {
        "code": "C1",
        "fragment": "C1_STRATEGY_DPP_LAN.tex",
        "labels": ["thm:r5-c1-law", "thm:r5-c1-dpp", "prop:r5-c1-sufficiency", "thm:r5-c1-testing", "thm:r5-c1-lan"],
        "repairs": [
            "construct opponent-dependent strategy laws by Ionescu--Tulcea recursion",
            "prove compact relaxed controls, lower semicontinuity, and the complete-history DPP",
            "type the sufficient information state",
            "derive the testing exponent and finite-volume-centered projective LAN",
        ],
    },
    "C2-cotangent-rigidity-tangent-representations": {
        "code": "C2",
        "fragment": "C2_TYPED_HISTORY_COMMUTATION.tex",
        "labels": ["thm:r5-c2-sum", "thm:r5-c2-contraction", "thm:r5-c2-likelihood", "thm:r5-c2-memory"],
        "repairs": [
            "define the countable locally convex platform direct sum and product dual",
            "prove coercive strict phase compactness and typed contractions",
            "put finite likelihood martingales on complete-history filtrations",
            "derive optional-projection, memory, diffusion, and BSDE commutation",
        ],
    },
    "D1-deterministic-theta-contractions": {
        "code": "D1",
        "fragment": "D1_PROJECTIVE_COMMUTATION.tex",
        "labels": ["thm:r5-d1-global", "thm:r5-d1-conditioning", "thm:r5-d1-interchange", "thm:r5-d1-lan", "thm:r5-d1-triangle"],
        "repairs": [
            "replace one local pressure by a compatible projective family of finite-source balls",
            "retain lower-semicontinuous closure in conditioning/contraction interchange",
            "use exact finite-volume centering in Gaussian likelihoods",
            "prove the dynamic triangle and independent canonical-cocycle calibration",
        ],
    },
}

for paper, data in PAPER_DATA.items():
    src = FRAG / data["fragment"]
    dst = PAPERS / paper / "ROUND5_POSITIVE_CLOSURE.tex"
    if not src.is_file():
        raise SystemExit(f"missing fragment: {src}")
    text = src.read_text(encoding="utf-8")
    dst.write_text("% ROUND5-REFEREE-POSITIVE-CLOSURE\n" + text, encoding="utf-8")

    main = PAPERS / paper / "main.tex"
    m = main.read_text(encoding="utf-8")
    m = re.sub(r"\\date\{[^}]*\}", r"\\date{August 31, 2026}", m, count=1)
    m = re.sub(
        r"\\noindent\\textbf\{Controlling revision:\}\s*\\texttt\{[^}]+\}\.",
        r"\\noindent\\textbf{Controlling revision:} \\texttt{ROUND5-REFEREE-POSITIVE-CLOSURE}.",
        m,
        count=1,
    )
    m = re.sub(
        r"\\input\{ROUND[0-9]+_POSITIVE_CLOSURE\.tex\}",
        r"\\input{ROUND5_POSITIVE_CLOSURE.tex}",
        m,
        count=1,
    )
    m = m.replace("round-three dependency", "round-five dependency")
    main.write_text(m, encoding="utf-8")

    response = PAPERS / paper / "AUTHOR_RESPONSE_ROUND5.md"
    lines = [
        f"# {data['code']} author response to round-four harsh rereview",
        "",
        "The report was treated as a new mathematical review of the materialized round-four tree.",
        "The former controlling module is retained only for provenance; `main.tex` now loads",
        "`ROUND5_POSITIVE_CLOSURE.tex`.",
        "",
        "## Positive repairs",
        "",
    ]
    lines.extend(f"- {item}." for item in data["repairs"])
    lines += ["", "## Controlling proof labels", ""]
    lines.extend(f"- `{label}`" for label in data["labels"])
    lines += [
        "",
        "No headline theorem was replaced by a no-go statement or by a weaker negative result.",
        "The declared domains were made explicit where the former statement was ill typed.",
        "",
    ]
    response.write_text("\n".join(lines), encoding="utf-8")

inventory = {
    "schema": "theta-theory-round5-referee-inventory-v1",
    "report_branch": "review/round4-gpt56-pro-harsh-11paper-2026-08-31",
    "reviewed_commit": "cbee394d6ee33db471b63420131314bd05909a0f",
    "revision_branch": "revision/round5-referee-positive-closure-11paper-2026-08-31",
    "papers": {
        paper: {
            "report": f"papers/{paper}/REFEREE_REPORT_ROUND4_GPT56_PRO.md",
            "fragment": f"revision/round5-referee/{data['fragment']}",
            "controlling_module": f"papers/{paper}/ROUND5_POSITIVE_CLOSURE.tex",
            "labels": data["labels"],
        }
        for paper, data in PAPER_DATA.items()
    },
}
(ROOT / "ROUND5_REFEREE_INVENTORY.json").write_text(
    json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

audit = """# Round-five historical derivation audit

The round-four harsh reports were checked against the archived recursive/CM2
corpus, the round-three rereview fragments, and the materialized round-four
proof packets.  Historical status words were not counted as proof.

| Chain | Reusable prior material | New defect exposed by the reports | Round-five resolution |
|---|---|---|---|
| A1 | exact-symplectic branch maps, common symbolic paths, saltation calculus | incompatible port faces; work primitive did not descend; response spaces were undefined | common recut section, autonomous exact first return, endpoint-corrected work cocycle, one Banach response fibre |
| A2 | finite-horizon geometry, finite-iterate growth, candidate UNI words | false wide-window LLT and incomplete moving-cut/high-frequency packet | finite moving-cut bundle, joint periodic certificate, complete frequency partition, three disjoint window regimes |
| A3 | escape-branch insight and finite-cut operators | zero-entropy periodic recovery could not preserve a positive-entropy rate | cemetery compactification, entropy-preserving Markov recovery, direct survivor/escape lower bound |
| A4 | Ray realization and compressed-resolvent algebra | fixed normalization did not form a nonlinear tower; area anomaly omitted | space-time harmonic Doob cocycle, history kernel, Volterra decay, anomalous rough lift |
| B1 | source-dependent limiting saddle and Schur complement | Fourier coefficient centered at the wrong finite mean | exact finite-volume saddle and mixed finite-saddle local limit |
| B2 | actual-contact orientation, short local cluster estimates | collision deletion changed the deterministic future; global sources absent | unchanged-trajectory contact strata, pivotal tube estimate, ordered factorial recursion, hierarchy block continuation |
| B3 | balance gauge idea and Radon current topology | gauge maps were not typed and the jump bracket was overcounted | weighted Orlicz heart, right inverse, no singular dual, one-increment bracket |
| B4 | BBGKY hierarchy and entropy action | hierarchy functionals were not an algebra; energy did not control the exponential Hamiltonian | convolution algebra, convergent correctors, Maxwellian exponential domain |
| C1 | block normalizers and game timing split | strategy-dependent conditional laws and LAN centre were missing | canonical Ionescu--Tulcea laws, relaxed DPP, sufficient state, finite-centred projective LAN |
| C2 | platform labels and strict component duals | direct-sum topology and finite history likelihoods were not constructed | locally convex direct sum/product dual, history Doob martingales, optional-projection/memory commutation |
| D1 | finite normalization and Schur-complement identities | local pressure was used as a global dual | compatible finite-source pressure family, closed global dual, closure-qualified interchange |

The recursive corpus supplies useful abstract templates but no direct proof of
the new model-specific gates above.  Those gates are therefore materialized as
new proof modules rather than promoted from status language.
"""
(ROOT / "ROUND5_HISTORICAL_DERIVATION_AUDIT.md").write_text(audit, encoding="utf-8")

ledger = """# Round-five proof dependency ledger

The controlling dependency graph is acyclic:

```text
A1

A2 -> A3 -> A4 -> C2
                 \\-> D1

B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1
                              \\       \\-> D1
                               \\-> C2 ----/
```

`B2-GC` denotes the finite-source grand-canonical contact expansion.
`B2-MC` denotes its conditioning after the exact finite-volume B1 saddle.
C1 and C2 retain the complete-history/hierarchy state at finite scale.
D1 uses only the union of source balls established in B2 and the exact
conditioning supplied by B1.
"""
(ROOT / "ROUND5_PROOF_DEPENDENCY_LEDGER.md").write_text(ledger, encoding="utf-8")

response = """# Series response to the round-four harsh referee reports

All eleven reports on
`review/round4-gpt56-pro-harsh-11paper-2026-08-31` were treated as new
mathematical reports, not as a request for editorial wording changes.

The revision first audited the recursive/CM2 corpus and prior repair packets.
Useful constructions were retained, but status labels and conditional
blueprints were not promoted to theorem credit.  Eleven new controlling
modules were then written.  The decisive counterexamples are addressed
directly:

- A2 separates local, central, and saturated roof-window regimes.
- A3 uses entropy-preserving Markov recovery rather than periodic measures.
- B1 conditions at the exact finite-volume saddle.
- B2 never deletes a deterministic collision from the future trajectory.
- B3 types quadratic collision increments in a weighted exponential heart and
  uses one jump increment in the bracket.
- B4 requires the velocity-tail domain that makes the exponential Hamiltonian
  finite.
- C1/C2 retain complete history and hierarchy states at finite scale.
- D1 takes a closed projective dual over the proved union of finite source
  balls.

No principal statement is replaced by a no-go theorem.  Domain corrections
are positive typing repairs required to make the announced operators finite
and composable.
"""
(ROOT / "REFEREE_ROUND5_RESPONSE.md").write_text(response, encoding="utf-8")

print(f"ROUND5_MATERIALIZED papers={len(PAPER_DATA)}")
