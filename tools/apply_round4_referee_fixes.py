#!/usr/bin/env python3
"""Install round-four referee fixes in all eleven controlling manuscripts.

This driver runs after the exact round-three rereview materializer.  Every
operation is region-delimited, idempotent, and fail-closed.  Replacement text
is stored under revision/round4-referee so the mathematical packets remain
reviewable independently of the installer.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
FRAG = ROOT / "revision" / "round4-referee"
BS = chr(92)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def split_fragment(path: Path, marker: str, next_marker: str | None = None) -> str:
    text = read(path)
    start = "% " + marker
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"{path}: fragment marker missing: {marker}")
    i = text.find("\n", i) + 1
    if next_marker is None:
        return text[i:].strip()
    end = text.find("% " + next_marker, i)
    if end < 0:
        raise SystemExit(f"{path}: next fragment marker missing: {next_marker}")
    return text[i:end].strip()


def replace_region(path: Path, start: str, end: str, replacement: str,
                   installed: str) -> int:
    text = read(path)
    if installed in text:
        return 0
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"{path}: start marker missing: {start!r}")
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"{path}: end marker missing: {end!r}")
    text = text[:i] + replacement.rstrip() + "\n\n" + text[j:]
    if installed not in text:
        raise SystemExit(f"{path}: installed marker absent: {installed!r}")
    write(path, text)
    return 1


def insert_before(path: Path, marker: str, addition: str, installed: str) -> int:
    text = read(path)
    if installed in text:
        return 0
    if text.count(marker) != 1:
        raise SystemExit(f"{path}: insertion marker count={text.count(marker)}")
    text = text.replace(marker, addition.rstrip() + "\n\n" + marker, 1)
    if installed not in text:
        raise SystemExit(f"{path}: inserted marker absent: {installed!r}")
    write(path, text)
    return 1


def normalize_title(path: Path) -> int:
    text = read(path)
    old = "Round-three positive closure"
    if old not in text:
        return 0
    text = text.replace(old, "Round-four referee closure", 1)
    write(path, text)
    return 1


def validate(path: Path) -> None:
    text = read(path)
    controls = sorted({ord(c) for c in text if ord(c) < 32 and c != "\n"})
    if controls:
        raise SystemExit(f"{path}: ASCII control bytes {controls}")
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    duplicates = sorted({x for x in labels if labels.count(x) > 1})
    if duplicates:
        raise SystemExit(f"{path}: duplicate labels {duplicates}")
    if text.count("\\begin{proof}") != text.count("\\end{proof}"):
        raise SystemExit(f"{path}: unmatched proof environments")
    if text.count("\\begin{theorem}") != text.count("\\end{theorem}"):
        raise SystemExit(f"{path}: unmatched theorem environments")
    if text.count("\\begin{lemma}") != text.count("\\end{lemma}"):
        raise SystemExit(f"{path}: unmatched lemma environments")


def fix_a1() -> int:
    path = PAPERS / "A1-exact-benchmarks" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "A1_PORT_SUSPENSION.tex"
    standing = split_fragment(f, "A1_STANDING", "A1_MECHANICAL")
    mechanical = split_fragment(f, "A1_MECHANICAL", "A1_CALIBRATION")
    calibration = split_fragment(f, "A1_CALIBRATION")
    mechanical = mechanical.replace("thm:r4-a1-suspension", "thm:r3-a1-impact")
    calibration = calibration.replace("thm:r4-a1-calibration", "thm:r3-a1-calibration")
    changes = 0
    changes += insert_before(
        path,
        BS + "subsection{One common path space}",
        standing,
        "Standing model and notation",
    )
    changes += replace_region(
        path,
        BS + "subsection{Autonomous Hamiltonian impact network}",
        BS + "subsection{Random-root process conditioning}",
        mechanical,
        "Cut-port Hamiltonian suspension",
    )
    changes += replace_region(
        path,
        BS + "subsection{Mechanical canonical cocycles and the coefficient}",
        BS + "subsection{Defined all-order response arrays}",
        calibration,
        "Conditional Kolmogorov--Nagumo classification",
    )
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_a2() -> int:
    path = PAPERS / "A2-sinai-homological-pressure" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "A2_CURRENT_BUNDLE_LLT.tex"
    bundle = split_fragment(f, "A2_BUNDLE", "A2_DOLGOPYAT")
    dolgopyat = split_fragment(f, "A2_DOLGOPYAT", "A2_LLT")
    llt = split_fragment(f, "A2_LLT")
    changes = 0
    changes += replace_region(
        path,
        "Use common angular coordinates",
        BS + "subsection{Uniform twisted spectrum}",
        bundle,
        "Current-augmented moving-cut bundle",
    )
    changes += replace_region(
        path,
        BS + "begin{theorem}[Joint aperiodicity and high-frequency contraction]",
        BS + "subsection{Joint lattice--nonlattice local limit theorem}",
        dolgopyat,
        "Frequency-adapted Dolgopyat contraction",
    )
    changes += replace_region(
        path,
        BS + "subsection{Joint lattice--nonlattice local limit theorem}",
        BS + "subsection{Physical pressure root}",
        llt,
        "Uniform Liv\\v{s}ic alternative and covariance",
    )
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_a3() -> int:
    path = PAPERS / "A3-full-empirical-path-ldp" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "A3_ESCAPE_STRICT.tex"
    direct = split_fragment(f, "A3_DIRECT", "A3_COTANGENT")
    cotangent = split_fragment(f, "A3_COTANGENT")
    changes = 0
    changes += replace_region(
        path,
        BS + "subsection{Defect-completed inducing and direct collision pressure}",
        BS + "subsection{Singularity exclusion and continuous graph factors}",
        direct,
        "Survivor pressure limit",
    )
    changes += replace_region(
        path,
        BS + "subsection{The closed path cotangent quotient}",
        BS + "begin{theorem}[Round-three A3 closure]",
        cotangent,
        "Radon annihilator and Hausdorff cotangent",
    )
    text = read(path).replace("Round-three A3 closure", "Round-four A3 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_a4() -> int:
    path = PAPERS / "A4-history-memory-universal-pressure" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "A4_DOOB_VOLTERRA.tex"
    memory = split_fragment(f, "A4_MEMORY", "A4_REALIZATION")
    realization = split_fragment(f, "A4_REALIZATION", "A4_NONLINEAR")
    nonlinear = split_fragment(f, "A4_NONLINEAR", "A4_TANGENT")
    tangent = split_fragment(f, "A4_TANGENT")
    changes = 0
    changes += replace_region(
        path,
        BS + "subsection{An exact memory kernel without orthogonal dynamics}",
        BS + "subsection{Spectral regularity of the memory transform}",
        memory,
        "Volterra construction of the exact memory",
    )
    changes += replace_region(
        path,
        BS + "subsection{Spectral regularity of the memory transform}",
        BS + "subsection{Nonlinear history pressure}",
        realization,
        "Minimal realization of the pole part",
    )
    changes += replace_region(
        path,
        BS + "subsection{Nonlinear history pressure}",
        BS + "subsection{Short-memory tangent}",
        nonlinear,
        "Exact nonlinear Doob tower",
    )
    changes += replace_region(
        path,
        BS + "subsection{Short-memory tangent}",
        BS + "begin{theorem}[Round-three A4 closure]",
        tangent,
        "Prepared rough diffusion with resolved memory",
    )
    text = read(path).replace("Round-three A4 closure", "Round-four A4 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_b1() -> int:
    path = PAPERS / "B1-microcanonical-preparation" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "B1_SINGLETON_COEFFICIENT.tex"
    convex = split_fragment(f, "B1_CONVEX", "B1_COEFF")
    coeff = split_fragment(f, "B1_COEFF")
    changes = 0
    changes += replace_region(
        path,
        BS + "begin{lemma}[Uniform strict constraint convexity]",
        BS + "begin{corollary}[The source-dependent saddle]",
        convex,
        "Separate the connected logarithm into its one-label sector",
    )
    changes += replace_region(
        path,
        BS + "subsection{A joint lattice--continuous coefficient estimate}",
        BS + "subsection{The constrained pressure formula}",
        coeff,
        "Singleton-dominated mixed lattice--continuous coefficient",
    )
    text = read(path).replace("Round-three B1 closure", "Round-four B1 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_b2() -> int:
    path = PAPERS / "B2-collision-clusters-dynamic-ldp" / "ROUND3_POSITIVE_CLOSURE.tex"
    fragment = read(FRAG / "B2_ANCESTRAL_GRAPH_SURGERY.tex").strip()
    changes = replace_region(
        path,
        BS + "subsection{The marked trajectory norm}",
        BS + "subsection{The marked Hamilton--Jacobi equation}",
        fragment,
        "Ancestral contact ledger",
    )
    text = read(path).replace("Round-three B2 closure", "Round-four B2 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_b3() -> int:
    path = PAPERS / "B3-hamilton-boltzmann-cotangents" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "B3_RADON_GAUSSIAN.tex"
    dual = split_fragment(f, "B3_DUAL", "B3_GAUSSIAN")
    gaussian = split_fragment(f, "B3_GAUSSIAN")
    changes = 0
    changes += replace_region(
        path,
        BS + "subsection{Weighted primal spaces}",
        BS + "begin{lemma}[Positive quotient covariance]",
        dual,
        "Radon path-space Fenchel duality",
    )
    changes += replace_region(
        path,
        BS + "subsection{The joint density--collision Gaussian tangent}",
        BS + "begin{theorem}[Round-three B3 closure]",
        gaussian,
        "Nuclear-space joint density--collision Gaussian tangent",
    )
    text = read(path).replace("Round-three B3 closure", "Round-four B3 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_b4() -> int:
    path = PAPERS / "B4-nonlinear-kinetic-semigroups" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "B4_ENERGY_HIERARCHY.tex"
    hierarchy = split_fragment(f, "B4_HIERARCHY", "B4_ENERGY")
    energy = split_fragment(f, "B4_ENERGY", "B4_MICRO")
    micro = split_fragment(f, "B4_MICRO")
    changes = 0
    changes += replace_region(
        path,
        BS + "subsection{The exact correlation state}",
        BS + "subsection{The weighted density state and containment}",
        hierarchy,
        "Backward connected Duhamel correctors",
    )
    changes += replace_region(
        path,
        BS + "subsection{The weighted density state and containment}",
        BS + "subsection{Microscopic semigroup convergence}",
        energy,
        "Energy compactness and exponential containment",
    )
    changes += replace_region(
        path,
        BS + "subsection{Microcanonical preparation as a lifted static saddle}",
        BS + "subsection{Calibrated rays and the Gaussian tangent}",
        micro,
        "Microcanonical dynamics on the conserved constraint surface",
    )
    text = read(path).replace("Round-three B4 closure", "Round-four B4 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_c1() -> int:
    path = PAPERS / "C1-information-risk-sensitive-saddles" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "C1_TESTING_LAN.tex"
    control = split_fragment(f, "C1_CONTROL", "C1_FILTER")
    filtering = split_fragment(f, "C1_FILTER")
    changes = 0
    changes += replace_region(
        path,
        BS + "subsection{Game III: block-normalized canonical law control}",
        BS + "subsection{Smooth saddle envelopes and discrete envelopes}",
        control,
        "Uniform conditional source chart",
    )
    changes += replace_region(
        path,
        BS + "subsection{Information reduction and phase filtering}",
        BS + "begin{theorem}[Round-three C1 closure]",
        filtering,
        "Almost-sure odds and expected posterior selection",
    )
    text = read(path).replace("Round-three C1 closure", "Round-four C1 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_c2() -> int:
    path = PAPERS / "C2-cotangent-rigidity-tangent-representations" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "C2_FILTRATION_STRICT.tex"
    maps = split_fragment(f, "C2_MAPS", "C2_STRICT")
    strict = split_fragment(f, "C2_STRICT", "C2_LIKELIHOOD")
    likelihood = split_fragment(f, "C2_LIKELIHOOD")
    changes = 0
    changes += replace_region(
        path,
        BS + "subsection{Mechanical maps on the Sinai component}",
        BS + "subsection{The weighted bounded-strict path-potential topology}",
        maps,
        "Direct-pressure continuity ledger",
    )
    changes += replace_region(
        path,
        BS + "subsection{The weighted bounded-strict path-potential topology}",
        BS + "subsection{The closed coboundary quotient}",
        strict,
        "Coercive strict dual and phase compactness",
    )
    changes += replace_region(
        path,
        BS + "subsection{Likelihood ratios through the proved Sinai diffusion tangent}",
        BS + "subsection{Linearized history pressure and compressed memory}",
        likelihood,
        "Stable resolved filtrations and deterministic-to-diffusion likelihoods",
    )
    text = read(path).replace("Round-three C2 closure", "Round-four C2 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def fix_d1() -> int:
    path = PAPERS / "D1-deterministic-theta-contractions" / "ROUND3_POSITIVE_CLOSURE.tex"
    f = FRAG / "D1_FINITE_MEAN_COMMUTATION.tex"
    commutation = split_fragment(f, "D1_COMMUTATION", "D1_LIKELIHOOD")
    likelihood = split_fragment(f, "D1_LIKELIHOOD")
    changes = 0
    changes += replace_region(
        path,
        BS + "begin{theorem}[Analytic--convex commutation theorem]",
        BS + "subsection{Central limits and canonical likelihood ratios}",
        commutation,
        "Normalized analytic--convex commutation theorem",
    )
    changes += replace_region(
        path,
        BS + "subsection{Central limits and canonical likelihood ratios}",
        BS + "subsection{Dynamic action, Hessian, and semigroup in one diagram}",
        likelihood,
        "Finite-mean Gaussian tangents and exact local likelihoods",
    )
    text = read(path).replace("Round-three D1 closure", "Round-four D1 closure")
    write(path, text)
    changes += normalize_title(path)
    validate(path)
    return changes


def main() -> None:
    changes = 0
    for fn in (
        fix_a1, fix_a2, fix_a3, fix_a4, fix_b1, fix_b2,
        fix_b3, fix_b4, fix_c1, fix_c2, fix_d1,
    ):
        changes += fn()
    print(f"ROUND4_REFEREE_FIXES_PASS changes={changes}")


if __name__ == "__main__":
    main()
