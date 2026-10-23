#!/usr/bin/env python3
"""Exact auxiliary checks for native338, not a continuous-geometry proof.

Uses only the Python standard library. Runs against the inherited complete
author source and checks rational constants, original moving section levels,
the exact two-sided determinant polynomial, index exponents, normalization,
and the necessity of the new simultaneous-root matching step. It also searches
all 660 preserved native-source blobs for the closest prior mechanisms.

Neither a finite script nor the historical text search certifies the actual
billiard curve-growth inputs or the full pointwise local limit theorem.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re
import tarfile


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def qtext(x: Q) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# Sparse exact polynomials in R,c,Xminus,Yminus,Xplus,Yplus.
ZERO_EXP = (0,) * 6


def var(index: int):
    e = [0] * 6
    e[index] = 1
    return {tuple(e): Q(1)}


def add(*items):
    out = {}
    for item in items:
        for e, value in item.items():
            out[e] = out.get(e, Q(0)) + value
    return {e: a for e, a in out.items() if a}


def mul(*items):
    out = {ZERO_EXP: Q(1)}
    for item in items:
        new = {}
        for e, a in out.items():
            for f, b in item.items():
                ef = tuple(x + y for x, y in zip(e, f))
                new[ef] = new.get(ef, Q(0)) + a * b
        out = {e: a for e, a in new.items() if a}
    return out


def scale(a, item):
    return {e: a * v for e, v in item.items() if a * v}


def run(source: Path, draft: Path):
    Rmin, Rmax, tau, h0 = Q(9, 20), Q(47, 100), Q(3, 50), Q(1, 200)
    sigma = 1 / (1 + 2 * tau / Rmax)
    E = Rmax / tau
    C0 = (tau + Rmax) / (2 * tau)
    U = 1 / Rmin + 1 / tau
    U2 = 1 / Rmin + 2 / tau
    assert sigma == Q(47, 59)
    assert E == Q(47, 6)
    assert C0 == Q(53, 12)
    assert U == Q(170, 9)
    assert U2 == Q(320, 9)
    assert U / 2 == Q(85, 9)
    # c*=91/(10000*pi): C_J/pi is rational and contains c* exactly once.
    cstar_over_pi_inverse = Q(91, 10000)
    CJ_over_pi = U / (2 * cstar_over_pi_inverse)
    assert CJ_over_pi == Q(850000, 819)
    dmin = tau / (tau + Rmax)
    assert dmin == Q(6, 53)
    assert 1 / (2 * dmin) == C0

    qlo, qhi = Q(49, 100), Q(53, 100)
    sintheta = lambda q: 2 * q / (1 + q*q)
    # The derivative 2(1-q^2)/(1+q^2)^2 is positive throughout this interval.
    assert 1 - qhi*qhi > 0
    moving_lower = sintheta(qlo) - h0
    moving_upper = sintheta(qhi) + h0
    assert moving_lower > h0
    assert moving_upper < Q(5, 6)
    constant_horizontal_levels = [-h0, h0, -Q(1, 2)-h0,
                                  -Q(1, 2)+h0, -Q(3, 20), Q(3, 20)]
    assert min(abs(b) for b in constant_horizontal_levels) == h0
    assert all(b != 0 for b in constant_horizontal_levels)
    # Four squares and one rectangle, two side occurrences of each orientation.
    horizontal_side_occurrences = vertical_side_occurrences = 2 * (4 + 1)
    assert horizontal_side_occurrences == 10
    assert 2 * vertical_side_occurrences == 20

    R, c, Xm, Ym, Xp, Yp = [var(i) for i in range(6)]
    Am = add(mul(R, c, Xm), Ym)
    Ap = add(mul(R, c, Xp), Yp)
    # Determinant of rows (Am,-Ym),(Ap,Yp).
    determinant = add(mul(Am, Yp), mul(Ym, Ap))
    horizontal_denominator = add(mul(Am, Yp), mul(Ym, Ap))
    vertical_denominator = add(scale(Q(2), mul(Ym, Yp)),
                               mul(R, c, Xm, Yp), mul(R, c, Xp, Ym))
    assert determinant == horizontal_denominator == vertical_denominator
    assert len(determinant) == 3
    # Therefore u=c/det = c/[Am Ap (Ym/Am+Yp/Ap)]
    #                      = c/[Ym Yp (2+Rc Xm/Ym+Rc Xp/Yp)].
    # Exactly one collision-area c, no extra R or probability factor.

    exact_sums = {}
    checked_index_pairs = 0
    geom_coefficient = (1 + sigma) / (1 - sigma)
    assert geom_coefficient == Q(53, 6)
    for m in range(2, 257):
        s = Q(0)
        for i in range(1, m):
            a, b = i - 1, m - i - 1
            assert a >= 0 and b >= 0
            assert 2 * max(a, b) >= m - 2
            assert min(sigma**a, sigma**b) == sigma**max(a, b)
            s += sigma**max(a, b)
            checked_index_pairs += 1
        # Squaring avoids all floating square roots in the half-integer bound.
        assert s*s <= (m-1)**2 * sigma**(m-2)
        assert s*s <= geom_coefficient**2 * sigma**(m-2)
        k = m - 2
        if k % 2 == 0:
            r = k // 2
            closed = sigma**r * (1 + 2*sigma*(1-sigma**r)/(1-sigma))
        else:
            r = (k - 1) // 2
            closed = 2*sigma**(r+1)*(1-sigma**(r+1))/(1-sigma)
        assert s == closed
        if m <= 8:
            exact_sums[str(m)] = qtext(s)
    # Endpoint m=1 contains no interior source; no accidental sigma^-1/2 term.
    interior_term_at_m1 = Q(0)
    endpoint_term_at_m1 = 2 * vertical_side_occurrences
    assert interior_term_at_m1 == 0 and endpoint_term_at_m1 == 20

    # Countercheck: generic interval overlays do NOT permit the new longer-half
    # bound. One left interval overlaps all 16 disjoint right intervals.
    H = Q(1)
    A, B = Q(1, 4), Q(1, 16)
    overlay_total = sum((A*B for _ in range(16)), Q(0))
    false_matching_bound = min(A, B)*H
    assert A <= H and 16*B <= H
    assert overlay_total == Q(1, 4) > false_matching_bound == Q(1, 16)
    # Native338 obtains a matching because each endpoint momentum tends to the
    # same exact normal value; it never applies this false overlay inequality.

    files = {
        "hessian": "core/285_complete_critical_sector_sum.tex",
        "zero_clearance": "core/322_positive_critical_marked_source.tex",
        "canonical_sources": "core/324_canonical_collision_boundary_budgets.tex",
        "enlarged_class": "core/284_physical_momentum_fibres.tex",
        "growth": "core/283_admissible_growth_and_clearance_consequences.tex",
        "word_pressure_not_used": "core/326_physical_boundary_stopping_pressure.tex",
        "source_remainder_not_used": "core/263_persistent_guard_and_nongrazing_shortage.tex",
    }
    identities = {}
    for role, rel in files.items():
        raw = (source/rel).read_bytes()
        identities[role] = {"path": rel, "git_blob": git_blob_sha(raw),
                            "sha256": hashlib.sha256(raw).hexdigest()}
    draft_raw = draft.read_bytes()

    archive = source/"history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz"
    archive_raw = archive.read_bytes()
    archive_hits = []
    full_blobs = {}
    critical_section = re.compile(
        r"section[- /](?:only|critical|side|cut|record)",
        re.I)
    with tarfile.open(archive, "r:gz") as tf:
        for member in tf:
            if not member.isfile() or not member.name.endswith(".tex"):
                continue
            raw = tf.extractfile(member).read()
            txt = raw.decode("utf-8", "replace")
            full_blobs[git_blob_sha(raw)] = (member.name, txt)
            if ("critical" in txt.lower()
                and critical_section.search(txt)
                and ("sigma" in txt or "exponential" in txt.lower())):
                title = re.search(r"\\section(?:\[[^\]]*\])?\{([^}]+)", txt)
                phrase_hits = []
                for match in critical_section.finditer(txt):
                    if any(w in txt[max(0,match.start()-150):match.end()+150].lower()
                           for w in ("critical", "punctur", "separate")):
                        context = txt[max(0,match.start()-100):match.end()+180]
                        phrase_hits.append(re.sub(r"\s+", " ", context).strip())
                        if len(phrase_hits) == 5:
                            break
                archive_hits.append({
                    "archive_member": member.name, "git_blob": git_blob_sha(raw),
                    "title": title.group(1) if title else None,
                    "nearby_contexts": phrase_hits,
                })
    assert len(full_blobs) == 660, len(full_blobs)
    prior_alternate = "cc6ceae6e0e12bd9206c0bfe8dcb85e6a281bc55"
    assert prior_alternate in full_blobs
    prior_text = full_blobs[prior_alternate][1]
    assert "section-only" in prior_text
    pos = prior_text.index("section-only")
    prior_scope = re.sub(r"\s+", " ", prior_text[max(0,pos-130):pos+220]).strip()
    native322_sha = identities["zero_clearance"]["git_blob"]
    assert native322_sha in full_blobs
    native324_sha = identities["canonical_sources"]["git_blob"]
    assert native324_sha in {hit["git_blob"] for hit in archive_hits}

    return {
        "status": "PASS",
        "proof_status": "auxiliary exact checks; continuous geometry and inherited dynamical proof are not certified by this script",
        "source": str(source),
        "draft": {"path": str(draft), "git_blob": git_blob_sha(draft_raw),
                  "sha256": hashlib.sha256(draft_raw).hexdigest()},
        "exact_constants": {
            "radius_min": qtext(Rmin), "radius_max": qtext(Rmax),
            "tau_min": qtext(tau), "sigma": qtext(sigma), "E": qtext(E),
            "C0": qtext(C0), "U_determinant": qtext(U),
            "U2_eigenvalue_not_used": qtext(U2), "CJ_times_cstar": qtext(U/2),
            "CJ_divided_by_pi": qtext(CJ_over_pi),
            "d_lower": qtext(dmin), "exact_geometric_sum_coefficient": qtext(geom_coefficient),
        },
        "original_section": {
            "horizontal_side_occurrences": horizontal_side_occurrences,
            "vertical_side_occurrences": vertical_side_occurrences,
            "vertical_endpoint_occurrences": 2*vertical_side_occurrences,
            "minimum_absolute_endpoint_horizontal_level": qtext(h0),
            "moving_lower_level_bound": qtext(moving_lower),
            "moving_upper_level_bound": qtext(moving_upper),
            "positive_gap_below_5_over_6": qtext(Q(5,6)-moving_upper),
            "moving_level_monotonicity_certificate": "1-(53/100)^2 > 0",
        },
        "determinant": {
            "identity": "D=(RcXminus+Yminus)Yplus+Yminus(RcXplus+Yplus)=2YminusYplus+Rc(XminusYplus+XplusYminus)",
            "sparse_polynomial_terms": len(determinant),
            "collision_area_factor": "c; no additional R",
        },
        "index_checks": {
            "m_range": [2,256], "checked_pairs": checked_index_pairs,
            "exact_small_count_sums": exact_sums,
            "closed_formula_checked": True,
            "squared_half_integer_bound_checked": True,
            "m1_interior_term": 0, "m1_endpoint_occurrences": endpoint_term_at_m1,
            "analytic_limit": "For each fixed q, (q+1)log m - ((m-2)/2)log(59/47) tends to -infinity; q log m -(m-1)log(59/47) also does.",
        },
        "necessary_matching_negative_control": {
            "left_intervals": 1, "right_intervals": 16,
            "overlay_sum": qtext(overlay_total),
            "false_longer_half_bound": qtext(false_matching_bound),
            "outcome": "generic overlap violates the proposed bound by factor 4; normal-root matching is essential",
        },
        "inherited_source_identities": identities,
        "novelty_search": {
            "archive": str(archive),
            "archive_sha256": hashlib.sha256(archive_raw).hexdigest(),
            "distinct_native_tex_blobs": len(full_blobs),
            "criteria": "critical plus original section-side/cut or section-only terms plus sigma or exponential; close prior mechanisms read in full",
            "hits": archive_hits,
            "closest_predecessor_native322": native322_sha,
            "closest_alternate_predecessor": prior_alternate,
            "alternate_explicit_scope": prior_scope,
            "classification": "native322 pays zero-clearance critical fans; native324 pays regular punctured side fluxes but not critical fans; native338 newly pays physically regular original-section critical fans by normal-root matching",
            "limitation": "This reproducible text audit is evidence of source novelty, not a formal proof that no semantically equivalent theorem exists elsewhere.",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(
        "/workspace/scratch/52177605cd92/a2-work/papers/A2-DYN-physical-roof-jump-spectrum-author-revision"))
    parser.add_argument("--draft", type=Path, default=Path(__file__).with_name(
        "338_original_section_critical_fan_payment.tex"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name(
        "338_EXACT_CHECKS_AND_NOVELTY.json"))
    args = parser.parse_args()
    report = run(args.source.resolve(), args.draft.resolve())
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({
        "status": report["status"], "output": str(args.output),
        "native_archive_blobs": report["novelty_search"]["distinct_native_tex_blobs"],
        "novelty_candidate_hits": len(report["novelty_search"]["hits"]),
        "index_pairs_checked": report["index_checks"]["checked_pairs"],
        "scope": report["proof_status"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

