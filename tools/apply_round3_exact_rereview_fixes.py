#!/usr/bin/env python3
"""Install the exact-commit round-three hostile-rereview replacements.

The replacement text lives in ``revision/round3-rereview`` so that this driver
contains only deterministic region operations.  It is idempotent, validates
labels after every operation, and never silently accepts an unmatched source
region.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
FRAG = ROOT / "revision" / "round3-rereview"
BS = chr(92)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def replace_region(
    path: Path,
    start: str,
    end: str,
    replacement: str,
    installed_marker: str,
) -> int:
    text = read(path)
    if installed_marker in text:
        return 0
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"{path}: start marker not found: {start!r}")
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"{path}: end marker not found: {end!r}")
    text = text[:i] + replacement.rstrip() + "\n\n" + text[j:]
    if installed_marker not in text:
        raise SystemExit(f"{path}: replacement marker absent: {installed_marker!r}")
    write(path, text)
    return 1


def insert_before(
    path: Path,
    marker: str,
    addition: str,
    installed_marker: str,
) -> int:
    text = read(path)
    if installed_marker in text:
        return 0
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"{path}: insertion marker count={count}: {marker!r}")
    text = text.replace(marker, addition.rstrip() + "\n\n" + marker, 1)
    if installed_marker not in text:
        raise SystemExit(f"{path}: inserted marker absent: {installed_marker!r}")
    write(path, text)
    return 1


def replace_once(path: Path, old: str, new: str, marker: str | None = None) -> int:
    text = read(path)
    if marker is not None and marker in text:
        return 0
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: replacement count={count}: {old[:100]!r}")
    text = text.replace(old, new, 1)
    if marker is not None and marker not in text:
        raise SystemExit(f"{path}: replacement marker absent: {marker!r}")
    write(path, text)
    return 1


def subsection(title: str) -> str:
    return BS + "subsection{" + title + "}"


def begin_theorem(title: str) -> str:
    return BS + "begin{theorem}[" + title + "]"


def validate_tex(path: Path) -> None:
    text = read(path)
    controls = sorted({ord(ch) for ch in text if ord(ch) < 32 and ch != "\n"})
    if controls:
        raise SystemExit(f"{path}: ASCII control bytes {controls}")
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    duplicates = sorted({x for x in labels if labels.count(x) > 1})
    if duplicates:
        raise SystemExit(f"{path}: duplicate labels {duplicates}")


def fix_a2() -> int:
    path = PAPERS / "A2-sinai-homological-pressure" / "ROUND3_POSITIVE_CLOSURE.tex"
    changes = 0
    geometry = read(FRAG / "A2_UNIFORM_GEOMETRY.tex")
    changes += replace_region(
        path,
        subsection("Uniform geometry and the moving-cut bundle"),
        "Let " + BS + "(\\mathcal W_R^s\\) be stable curves",
        geometry,
        "For a primitive lattice direction",
    )

    temporal = read(FRAG / "A2_TEMPORAL_PACKET.tex")
    changes += replace_region(
        path,
        subsection("A concrete temporal non-integrability rectangle"),
        subsection("Joint lattice--nonlattice local limit theorem"),
        temporal,
        "Certified temporal non-integrability on the induced quotient",
    )

    text = read(path)
    old = (
        "Let " + BS + "(K_n=S_n\\kappa_R\\), "
        + BS + "(T_n=S_n\\tau_R\\), and let\n"
        + BS + "((a,b)=\\nabla P_R(\\xi,s)\\) on a real simple branch.  Write"
    )
    new = (
        "Let " + BS + "(K_n=S_n\\kappa_R\\), "
        + BS + "(T_n=S_n\\tau_R\\), and put\n"
        + BS + "[\n a=\\partial_\\xi P_R(\\xi,s),\\qquad\n "
        + BS + "bar\\tau=-\\partial_sP_R(\\xi,s)>0.\n"
        + BS + "]\nWrite"
    )
    if old in text:
        text = text.replace(old, new, 1)
        changes += 1
    elif "bar\\tau=-\\partial_sP_R" not in text:
        raise SystemExit("A2 mean-coordinate sign block not found")

    old_condition = (
        BS + "(k_n-na=O(\\sqrt n)\\), and for intervals\n"
        + BS + "(J_n=[t_n-b_n,t_n+b_n]\\) with"
    )
    new_condition = (
        BS + "(k_n-na=O(\\sqrt n)\\), "
        + BS + "(t_n-n\\bar\\tau=O(\\sqrt n)\\), and for intervals\n"
        + BS + "(J_n=[t_n-b_n,t_n+b_n]\\) with"
    )
    if old_condition in text:
        text = text.replace(old_condition, new_condition, 1)
        changes += 1
    elif "t_n-n\\bar\\tau" not in text:
        raise SystemExit("A2 local-limit mean condition not found")

    old_expansion = (
        "=i" + BS + "langle(u,t),(a,b)\\rangle\n"
        " -\\tfrac12\\langle(u,t),\\Sigma_{R,\\xi,s}(u,t)\\rangle"
    )
    new_expansion = (
        "=i\\langle u,a\\rangle-it\\bar\\tau\n"
        " -\\tfrac12\\langle(u,-t),\\Sigma_{R,\\xi,s}(u,-t)\\rangle"
    )
    if old_expansion in text:
        text = text.replace(old_expansion, new_expansion, 1)
        changes += 1
    elif "-it\\bar\\tau" not in text:
        raise SystemExit("A2 pressure expansion sign block not found")

    text = text.replace(
        "identities and Lemma~" + BS + "ref{thm:r3-a2-high}",
        "identities and Theorem~" + BS + "ref{thm:r3-a2-high}",
    )
    write(path, text)
    validate_tex(path)
    return changes


def fix_a3() -> int:
    path = PAPERS / "A3-full-empirical-path-ldp" / "ROUND3_POSITIVE_CLOSURE.tex"
    fragment = read(FRAG / "A3_DIRECT_PATH_LDP.tex")
    changes = replace_region(
        path,
        "For a return branch " + BS + "(a\\), let " + BS + "(h(a)\\) be the largest",
        subsection("Finite-rate support and preparation"),
        fragment,
        "Defect-completed inducing and direct collision pressure",
    )
    text = read(path)
    text = text.replace(BS + "mathcal I^c", BS + "mathcal I_R^c")
    text = text.replace(BS + "mathcal I^p", BS + "mathcal I_R^p")
    write(path, text)
    validate_tex(path)
    return changes


def fix_a4() -> int:
    path = PAPERS / "A4-history-memory-universal-pressure" / "ROUND3_POSITIVE_CLOSURE.tex"
    fragment = read(FRAG / "A4_RAY_FELLER.tex")
    changes = replace_region(
        path,
        subsection("The weighted history Feller space"),
        subsection("An exact memory kernel without orthogonal dynamics"),
        fragment,
        "Strict-Ray history theorem",
    )
    validate_tex(path)
    return changes


def fix_b1_b3() -> int:
    packet = read(FRAG / "B1_B3_NULLSPACE_PACKET.tex")
    b1_text, b3_text = packet.split("% B3 insertion", 1)
    b1_text = b1_text.replace("% B1 insertion", "", 1).strip()
    b3_text = b3_text.strip()
    changes = 0
    b1 = PAPERS / "B1-microcanonical-preparation" / "ROUND3_POSITIVE_CLOSURE.tex"
    changes += insert_before(
        b1,
        BS + "begin{lemma}[Uniform characteristic-function gap]",
        b1_text,
        "Span-one particle-number gap",
    )
    b3 = PAPERS / "B3-hamilton-boltzmann-cotangents" / "ROUND3_POSITIVE_CLOSURE.tex"
    changes += insert_before(
        b3,
        BS + "begin{lemma}[Positive quotient covariance]",
        b3_text,
        "Density of local balanced variations",
    )
    validate_tex(b1)
    validate_tex(b3)
    return changes


def fix_b2() -> int:
    path = PAPERS / "B2-collision-clusters-dynamic-ldp" / "ROUND3_POSITIVE_CLOSURE.tex"
    fragment = read(FRAG / "B2_GLOBAL_SOURCE_LDP.tex")
    split_marker = subsection("Full grand-canonical density--actual-collision LDP")
    if split_marker not in fragment:
        raise SystemExit("B2 rereview fragment split marker missing")
    continuation, full_ldp = fragment.split(split_marker, 1)
    full_ldp = split_marker + full_ldp
    changes = 0
    changes += insert_before(
        path,
        subsection("Grand-canonical joint LDP"),
        continuation,
        "Bounded real-source continuation",
    )
    changes += replace_region(
        path,
        begin_theorem("Grand-canonical density--actual-collision LDP"),
        begin_theorem("Round-three B2 closure"),
        full_ldp,
        "Balance-preserving regularization of finite-action pairs",
    )
    validate_tex(path)
    return changes


def fix_c1() -> int:
    path = PAPERS / "C1-information-risk-sensitive-saddles" / "ROUND3_POSITIVE_CLOSURE.tex"
    fragment = read(FRAG / "C1_BLOCK_NORMALIZED_CONTROL.tex")
    fragment = fragment.replace("\\left[\n \n exp\\left", "\\left[\n \\exp\\left")
    if "\n exp" in fragment:
        fragment = fragment.replace("\n exp", "\n " + BS + "exp")
    changes = replace_region(
        path,
        subsection("Game III: canonical adaptive law control"),
        subsection("Smooth saddle envelopes and discrete envelopes"),
        fragment,
        "block-normalized canonical law control",
    )
    validate_tex(path)
    return changes


def fix_c2() -> int:
    path = PAPERS / "C2-cotangent-rigidity-tangent-representations" / "ROUND3_POSITIVE_CLOSURE.tex"
    fragment = read(FRAG / "C2_STRICT_MEMORY.tex")
    split_marker = subsection("Linearized history pressure and compressed memory")
    if split_marker not in fragment:
        raise SystemExit("C2 rereview fragment split marker missing")
    strict_part, memory_part = fragment.split(split_marker, 1)
    memory_part = split_marker + memory_part
    changes = 0
    changes += replace_region(
        path,
        subsection("A strict path-potential topology"),
        subsection("The closed coboundary quotient"),
        strict_part,
        "weighted bounded-strict path-potential topology",
    )
    changes += replace_region(
        path,
        subsection("A commutative memory--pressure identity"),
        begin_theorem("Round-three C2 closure"),
        memory_part,
        "Memory is the Laplace transform of the pressure tangent",
    )
    validate_tex(path)
    return changes


def main() -> None:
    changes = 0
    changes += fix_a2()
    changes += fix_a3()
    changes += fix_a4()
    changes += fix_b1_b3()
    changes += fix_b2()
    changes += fix_c1()
    changes += fix_c2()
    print(f"ROUND3_EXACT_REREVIEW_FIXES_PASS changes={changes}")


if __name__ == "__main__":
    main()
