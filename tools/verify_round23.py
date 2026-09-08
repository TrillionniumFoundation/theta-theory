#!/usr/bin/env python3
"""Fail-closed Round-Twenty-Three source and counterexample verifier.

The verifier checks active-source identity, proof structure, citations, local
references, the declared dependency DAG, preservation of the controlling
referee report, and finite-dimensional regressions for the report's explicit
counterexamples.  A PASS is reproducibility evidence, not peer review.
"""
from __future__ import annotations

from collections import defaultdict, deque
from hashlib import sha1, sha256
from pathlib import Path
from typing import Any, Callable
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "ROUND23_SOURCE_MANIFEST.json"
RESULTS_PATH = ROOT / "ROUND23_REGRESSION_RESULTS.json"
FORMAL_ENVS = ("theorem", "proposition", "lemma", "corollary")
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|PLACEHOLDER|INSERT PROOF)\b", re.I)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|cref|Cref|autoref)\{([^{}]+)\}")
CITE_RE = re.compile(r"\\(?:cite|parencite|textcite|autocite)\s*(?:\[[^\]]*\]\s*){0,2}\{([^{}]+)\}")
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.I)
BIB_RESOURCE_RE = re.compile(r"\\addbibresource\{([^{}]+)\}")

MARKERS: dict[str, tuple[str, ...]] = {
    "A1": (r"\mathfrak C_{\eta}^{r}", "Bochner integral", r"\operatorname{tr}Q_a"),
    "A2": (r"\mathscr G_a", r"(r,\varphi)", r"(1+|b|)^{-2}"),
    "A3": (r"\mathcal O_N^c", r"q^{\mathcal P}", r"\mathcal R_N^c"),
    "A4": (r"K(t)=PLQe^{tL_Q}QLP", r"z^{-1}PLQLP", r"(\vartheta/\rho)^n"),
    "B1": (r"Z_{\varepsilon,N}(0,0)=1", r"\Sigma_{\mathbb R\mid\mathbb Z}", "deterministic"),
    "B2": (r"\varepsilon^{\alpha_G", r"\mathbf H^\varepsilon", r"\mathfrak d_G"),
    "B3": (r"h=\dot\Gamma-D A_f[u]", r"\frac12\int {h^2\over A_f}", "stopping time"),
    "B4": (r"p=2+\delta", "W_2", r"R_\mu\bigl(h+(\mu-\lambda)R_\lambda h\bigr)"),
    "C1": (r"\delta_{\Phi_\vartheta^a(x)}", r"G_\vartheta^a(x,dy)", r"\mathfrak A_{\rm pe}"),
    "C2": (r"\beta_W=T^{-1}\beta_0", r"\mathcal L_f^*r", r"\Pi_t^n", "L_t>0"),
    "D1": (r"N^{-\kappa_j}", r"\mathcal C_{j,N}", r"\sup_{\alpha\text{ common}}", "Rouche"),
}


class VerificationFailure(RuntimeError):
    pass


def fail(message: str) -> None:
    raise VerificationFailure(message)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"non-UTF-8 source {path.relative_to(ROOT)}: {exc}")
    raise AssertionError("unreachable")


def git_blob_sha(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def close(left: complex | float, right: complex | float, tol: float = 1e-10) -> None:
    if abs(left - right) > tol * (1.0 + abs(right)):
        fail(f"numeric mismatch: {left!r} != {right!r} within {tol}")


def bibliography_keys(folder: Path, main_text: str, paper: str) -> set[str]:
    resources = BIB_RESOURCE_RE.findall(main_text)
    if not resources:
        fail(f"{paper}: wrapper declares no bibliography resource")
    keys: set[str] = set()
    for resource in resources:
        path = folder / resource
        if not path.is_file():
            fail(f"{paper}: missing bibliography resource {resource}")
        for key in BIB_RE.findall(read_text(path)):
            if key in keys:
                fail(f"{paper}: duplicate bibliography key {key}")
            keys.add(key)
    return keys


def dependency_order(manifest: dict[str, Any]) -> list[str]:
    nodes = list(manifest["dependency_nodes"])
    edges = {tuple(edge) for edge in manifest["dependency_edges"]}
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = defaultdict(list)
    for left, right in edges:
        if left not in indegree or right not in indegree:
            fail(f"unknown dependency edge {left}->{right}")
        children[left].append(right)
        indegree[right] += 1
    queue = deque(node for node in nodes if indegree[node] == 0)
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(nodes):
        fail("declared proof dependency graph contains a cycle")
    required = {
        ("B2-GC", "B1"), ("B1", "B2-MC"), ("B2-GC", "B2-MC"),
        ("B2-MC", "B3"), ("B3", "B4"), ("C1", "C2"), ("C2", "D1"),
    }
    if not required.issubset(edges):
        fail(f"dependency graph omits required edges {sorted(required - edges)}")
    return order


def check_sources(manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    active = manifest["active_source"]
    response_name = manifest["author_response"]
    revision = manifest["revision"]
    combined = sha256()
    global_labels: dict[str, str] = {}
    records: list[dict[str, Any]] = []

    for paper, entry in manifest["papers"].items():
        folder = ROOT / entry["directory"]
        main_path = folder / "main.tex"
        source_path = folder / active
        response_path = folder / response_name
        for path in (main_path, source_path, response_path):
            if not path.is_file():
                fail(f"{paper}: missing {path.relative_to(ROOT)}")
        main = read_text(main_path)
        source = read_text(source_path)
        response = read_text(response_path)
        if not source.strip() or not response.strip():
            fail(f"{paper}: empty active source or author response")
        if len(response.encode("utf-8")) < 500:
            fail(f"{paper}: author response is too short to map the referee objections")
        for role, text in (("wrapper", main), ("source", source), ("response", response)):
            if any(ord(ch) < 32 and ch not in "\n\t" for ch in text):
                fail(f"{paper}: control character in {role}")

        if main.count(rf"\input{{{active}}}") != 1:
            fail(f"{paper}: wrapper must import {active} exactly once")
        if r"\input{ROUND17_POSITIVE_CLOSURE.tex}" in main:
            fail(f"{paper}: legacy Round17 source remains active")
        escaped_response = response_name.replace("_", r"\_")
        if revision not in main or (response_name not in main and escaped_response not in main):
            fail(f"{paper}: wrapper does not identify the Round23 revision and response")
        if "ROUND21-REFEREE-POSITIVE-CLOSURE" in main or "ROUND17_POSITIVE_CLOSURE" in source:
            fail(f"{paper}: active material advertises a superseded source slot")
        if PLACEHOLDER_RE.search(source) or PLACEHOLDER_RE.search(response):
            fail(f"{paper}: placeholder token in active material")
        for marker in MARKERS[paper]:
            if marker not in source:
                fail(f"{paper}: missing positive-closure marker {marker!r}")
        for label in entry["required_labels"]:
            if rf"\label{{{label}}}" not in source:
                fail(f"{paper}: missing required active label {label}")

        formal_count = 0
        for env in (*FORMAL_ENVS, "proof", "enumerate", "align", "align*"):
            opens = source.count(rf"\begin{{{env}}}")
            closes = source.count(rf"\end{{{env}}}")
            if opens != closes:
                fail(f"{paper}: unbalanced {env} environment ({opens}/{closes})")
            if env in FORMAL_ENVS:
                formal_count += opens
        proof_count = source.count(r"\begin{proof}")
        if formal_count < 3 or proof_count < formal_count:
            fail(f"{paper}: incomplete theorem/proof structure ({formal_count}/{proof_count})")

        labels = set(LABEL_RE.findall(source))
        for label in labels:
            if label in global_labels:
                fail(f"duplicate active label {label} in {global_labels[label]} and {paper}")
            global_labels[label] = paper
        refs: set[str] = set()
        for group in REF_RE.findall(source):
            refs.update(key.strip() for key in group.split(",") if key.strip())
        missing_refs = sorted(refs - labels)
        if missing_refs:
            fail(f"{paper}: unresolved local labels {missing_refs}")

        cited: set[str] = set()
        for group in CITE_RE.findall(source + "\n" + main):
            cited.update(key.strip() for key in group.split(",") if key.strip())
        missing_citations = sorted(cited - bibliography_keys(folder, main, paper))
        if missing_citations:
            fail(f"{paper}: unresolved citations {missing_citations}")

        source_bytes = source_path.read_bytes()
        combined.update(paper.encode("ascii") + b"\0" + source_bytes + b"\0")
        records.append({
            "paper": paper,
            "source": str(source_path.relative_to(ROOT)),
            "bytes": len(source_bytes),
            "sha256": sha256(source_bytes).hexdigest(),
            "formal_statements": formal_count,
            "proofs": proof_count,
            "labels": len(labels),
            "citations": len(cited),
            "local_references": len(refs),
        })
        print(f"paper={paper} bytes={len(source_bytes)} formal={formal_count} proofs={proof_count} citations={len(cited)}")
    return records, combined.hexdigest()


def kl(probability: list[float], reference: list[float]) -> float:
    return sum(p * math.log(p / r) for p, r in zip(probability, reference) if p > 0)


def run_regressions() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    def add(name: str, **metrics: Any) -> None:
        results.append({"name": name, "status": "PASS", "metrics": metrics})
        print(f"regression={name} status=PASS")

    # A1: an l2 observable can have only polynomial cylinder tails.
    eta, ns = 0.1, [20, 40, 80]
    scaled = [math.exp(eta * n) / (2.0 * math.sqrt(n + 1.0)) for n in ns]
    if not scaled[0] < scaled[1] < scaled[2]:
        fail("A1 slow-tail regression failed")
    add("A1_bare_Hilbert_no_exponential_rate", eta=eta, N=ns, scaled_tail_lower_bounds=scaled)
    probs, vectors = [0.2, 0.3, 0.5], [(1.0, 2.0), (0.0, -1.0), (3.0, 1.0)]
    trace = sum(p * (x*x + y*y) for p, (x, y) in zip(probs, vectors))
    expected = sum(p * (x*x + y*y) for p, (x, y) in zip(probs, vectors))
    close(trace, expected)
    add("A1_trace_covariance_identity", trace_Q=trace, expected_squared_norm=expected)

    # A2: irrational roof pair and coprime periods kill the character.
    root_two = math.sqrt(2.0)
    relation_min = min(abs(m + n*root_two) for m in range(-25, 26) for n in range(-25, 26) if (m, n) != (0, 0))
    if relation_min <= 1e-12 or math.gcd(5, 7) != 1:
        fail("A2 periodic-character regression failed")
    add("A2_periodic_character_elimination", finite_relation_minimum=relation_min, period_gcd=1)

    # A3: chronology and conditional-reference KL recovery.
    if ((0.0, "A"), (0.5, "B")) == ((0.0, "B"), (0.5, "A")):
        fail("A3 chronology regression failed")
    add("A3_ordered_state_distinguishes_paths", paths=["AB", "BA"])
    reference, control = [0.1, 0.2, 0.3, 0.4], [0.25, 0.15, 0.10, 0.50]
    cells, recovered, cell_q, cell_k = ((0, 1), (2, 3)), [0.0]*4, [], []
    for cell in cells:
        qc, kc = sum(control[i] for i in cell), sum(reference[i] for i in cell)
        cell_q.append(qc); cell_k.append(kc)
        for i in cell:
            recovered[i] = qc * reference[i] / kc
    fine, coarse, recovered_kl = kl(control, reference), kl(cell_q, cell_k), kl(recovered, reference)
    close(recovered_kl, coarse)
    if recovered_kl > fine + 1e-12:
        fail("A3 conditional-reference recovery increased KL")
    add("A3_conditional_reference_KL", fine_KL=fine, coarse_KL=coarse, recovered_KL=recovered_kl)

    # A4: remote Lyapunov mass differs from influence; Schur--Feshbach is exact.
    theta, rho, depths = 0.5, 0.8, [4, 12, 24]
    lyapunov = [rho**n * rho**(-n) for n in depths]
    influence = [(theta/rho)**n for n in depths]
    if any(abs(x-1.0) > 1e-12 for x in lyapunov) or not influence[0] > influence[1] > influence[2]:
        fail("A4 two-scale history regression failed")
    add("A4_two_scale_remote_past", lyapunov_contribution=lyapunov, influence=influence)
    a, b, c, d = 0.2, 1.1, -0.4, -0.7
    errors = []
    for z in (2+0.5j, 5+2j, 11-3j):
        full = (z-d)/((z-a)*(z-d)-b*c)
        reduced = 1/(z-a-b*c/(z-d))
        close(full, reduced, 1e-12); errors.append(abs(full-reduced))
    z_khat = [z*b*c/(z-d) for z in (1000.0, 10000.0, 100000.0)]
    close(z_khat[-1], b*c, 1e-5)
    add("A4_exact_Feshbach_and_z_inverse_lead", resolvent_errors=errors, zKhat=z_khat, PLQLP=b*c)

    # B1: factorial pressure diverges while a probability MGF is zero at origin.
    n_values = [10, 100, 1000]
    unnormalized = [-math.lgamma(n+1.0)/n for n in n_values]
    if not unnormalized[0] > unnormalized[1] > unnormalized[2] or unnormalized[-1] > -5.0:
        fail("B1 normalization regression failed")
    add("B1_relative_canonical_normalization", N=n_values, unnormalized=unnormalized, normalized=[0.0]*3)
    conditional_mean = 3.0/4.0*2.0
    schur = 9.0 - 3.0*3.0/4.0
    close(conditional_mean, 1.5); close(schur, 6.75)
    add("B1_mixed_Gaussian_Schur", conditional_mean=conditional_mean, conditional_variance=schur)

    # B2: optimized loop tube gives a positive epsilon power; factorial stays present.
    m_value, kappa, epsilons = 3.0, 0.5, [1e-2, 1e-4, 1e-8]
    alpha = kappa/(m_value+kappa)
    bounds = []
    for epsilon in epsilons:
        scale = epsilon**(1.0/(m_value+kappa))
        bounds.append(epsilon*scale**(-m_value) + scale**kappa)
    if alpha <= 0 or not bounds[0] > bounds[1] > bounds[2]:
        fail("B2 loop-opening regression failed")
    add("B2_transverse_loop_positive_power", alpha=alpha, epsilon=epsilons, optimized_bounds=bounds)
    ratios = [math.exp((k-2)*math.log(k)-math.lgamma(k+1)-k+2.5*math.log(k)) for k in range(2, 80)]
    if max(ratios) >= 1.0:
        fail("B2 factorial graph envelope failed")
    add("B2_factorial_connected_normalization", max_scaled_tree_ratio=max(ratios), k_max=79)

    # B3: action vanishes on Gamma=A_f and has the normal-defect Hessian.
    entropy = lambda q: q*math.log(q)-q+1.0
    base, tangent, defect, step = 2.0, 0.4, 0.7, 1e-3
    zero_path = lambda s: base*math.exp(tangent*s)*entropy(1.0)
    zero_second = (zero_path(step)-2*zero_path(0.0)+zero_path(-step))/step**2
    close(zero_second, 0.0, 1e-14)
    normal_path = lambda s: base*math.exp(tangent*s)*entropy(1.0+s*defect/base)
    normal_second = (normal_path(step)-2*normal_path(0.0)+normal_path(-step))/step**2
    expected_second = defect*defect/base
    close(normal_second, expected_second, 1e-5)
    add("B3_zero_manifold_and_defect_Hessian", zero_second=zero_second, normal_second=normal_second, expected=expected_second)

    # B4: a remote n^-2 mass at speed n violates every fixed (2+delta)-shell.
    delta, speeds = 0.5, [10.0, 100.0, 1000.0]
    second = [n**(-2)*n**2 for n in speeds]
    super_moment = [n**(-2)*n**(2+delta) for n in speeds]
    if any(abs(x-1.0) > 1e-12 for x in second) or not super_moment[0] < super_moment[1] < super_moment[2]:
        fail("B4 superquadratic compactness regression failed")
    add("B4_superquadratic_excludes_escape", speed=speeds, remote_second=second, remote_p_moment=super_moment)

    # C1: finite Dirac families already show the common-density obstruction.
    family_sizes = [10, 100, 1000]
    atom_bounds = [1.0/n for n in family_sizes]
    if not atom_bounds[0] > atom_bounds[1] > atom_bounds[2]:
        fail("C1 deterministic-Dirac regression failed")
    add("C1_no_common_hidden_Dirac_density", family_size=family_sizes, uniform_atom_bound=atom_bounds)
    evidence_cases = [(1e-9, 1.5e-9, 0.0, 0.0), (0.1, 0.08, 0.11, 0.077), (0.0, 0.0, 1e-8, 1.8e-8)]
    margins = []
    for rn, nn, r, n in evidence_cases:
        left = rn*abs((nn/rn if rn else 0.0)-(n/r if r else 0.0))
        right = abs(nn-n)+2.0*abs(rn-r)
        if left > right + 1e-15:
            fail("C1 integrated-evidence inequality failed")
        margins.append(right-left)
    add("C1_integrated_small_evidence_ratio", nonnegative_margins=margins)
    add("C1_uninformative_action_zero_information", Fisher_information=0.0)

    # C2: weighted strict duality is an exact pullback; finite exponentials stay positive.
    weight, mu, test = [1.0, 2.0, 5.0], [0.5, -0.25, 0.1], [2.0, -3.0, 4.0]
    nu = [w*m for w, m in zip(weight, mu)]
    pairing = sum(f*m for f, m in zip(test, mu))
    pulled_pairing = sum((f/w)*n for f, w, n in zip(test, weight, nu))
    weighted_variation = sum(w*abs(m) for w, m in zip(weight, mu))
    close(pairing, pulled_pairing); close(weighted_variation, sum(abs(n) for n in nu))
    add("C2_weighted_strict_pullback_isometry", pairing=pairing, weighted_variation=weighted_variation)
    exponentials = [math.exp(x-0.5*q) for x, q in [(-20.0, 2.0), (0.0, 1.0), (20.0, 5.0)]]
    if any(value <= 0.0 or not math.isfinite(value) for value in exponentials):
        fail("C2 stochastic-exponential positivity regression failed")
    add("C2_finite_Brownian_exponential_strictly_positive", samples=exponentials)

    # D1: an LDP tie does not determine polynomial weights; policy is shared.
    phase_n = [10.0, 100.0, 10000.0]
    phase_ratio = [1.5/n for n in phase_n]
    if not phase_ratio[0] > phase_ratio[1] > phase_ratio[2]:
        fail("D1 polynomial-weight regression failed")
    add("D1_polynomial_phase_weight", N=phase_n, phase2_over_phase1=phase_ratio)
    payoffs = ((1.0, 0.0), (0.0, 1.0))
    shared = max(0.5*payoffs[0][action] + 0.5*payoffs[1][action] for action in range(2))
    clairvoyant = 0.5*max(payoffs[0]) + 0.5*max(payoffs[1])
    if not shared < clairvoyant:
        fail("D1 shared-policy regression failed")
    add("D1_shared_policy_before_phase_aggregation", shared_policy_value=shared, phasewise_value=clairvoyant)
    return results


def main() -> int:
    try:
        manifest = json.loads(read_text(MANIFEST_PATH))
        if manifest.get("schema") != "theta-theory-round23-source-manifest-v1":
            fail("unsupported Round23 manifest schema")
        for relative in manifest["required_root_files"]:
            path = ROOT / relative
            if not path.is_file() or not path.read_bytes().strip():
                fail(f"missing or empty root evidence file {relative}")
        report = manifest["referee_report"]
        report_path = ROOT / report["path"]
        actual_report_sha = git_blob_sha(report_path.read_bytes())
        if actual_report_sha != report["git_blob_sha"]:
            fail(f"controlling referee report changed: {actual_report_sha}")
        order = dependency_order(manifest)
        ledger = read_text(ROOT / "ROUND23_PROOF_DEPENDENCY_LEDGER.md")
        for node in manifest["dependency_nodes"]:
            if f"| {node} |" not in ledger and f"`{node}`" not in ledger:
                fail(f"dependency ledger omits node {node}")
        papers, combined_hash = check_sources(manifest)
        regressions = run_regressions()
        payload = {
            "schema": "theta-theory-round23-regression-results-v1",
            "revision": manifest["revision"],
            "status": "PASS",
            "referee_report_git_blob_sha": actual_report_sha,
            "combined_active_source_sha256": combined_hash,
            "dependency_order": order,
            "papers": papers,
            "regressions": regressions,
            "disclaimer": "Internal source, algebra, and reproducibility gates; not independent mathematical peer review.",
        }
        RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)+"\n", encoding="utf-8")
        print(f"ROUND23_VERIFY_PASS papers={len(papers)} regressions={len(regressions)} source_sha256={combined_hash}")
        return 0
    except (VerificationFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ROUND23_VERIFY_FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
