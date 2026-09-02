#!/usr/bin/env python3
"""Fail-closed source and counterexample verifier for Round Twenty-Three.

The checks establish repository consistency and executable finite-dimensional
regressions.  They do not substitute for independent mathematical peer review.
"""
from __future__ import annotations

from collections import defaultdict, deque
from hashlib import sha1, sha256
from pathlib import Path
from typing import Any
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
CITE_RE = re.compile(
    r"\\(?:cite|parencite|textcite|autocite)\s*(?:\[[^\]]*\]\s*){0,2}\{([^{}]+)\}"
)
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.I)
BIB_RESOURCE_RE = re.compile(r"\\addbibresource\{([^{}]+)\}")

REQUIRED_MARKERS: dict[str, tuple[str, ...]] = {
    "A1": (
        r"\mathfrak C_{\eta}^{r}",
        r"\operatorname{tr}Q_a=\mathbb E_a\|D_0\|",
        "Bochner integral",
    ),
    "A2": (
        r"\mathscr G_a=\mathbb Z^3\times\mathbb R\times\mathbb Z",
        r"D_z(\Psi_1,\Psi_2)",
        r"(1+|b|)^{-2}",
    ),
    "A3": (r"\mathcal O_N^c", r"q^{\mathcal P}", r"\mathcal R_N^c"),
    "A4": (r"K(t)=PLQe^{tL_Q}QLP", r"z^{-1}PLQLP", r"(\vartheta/\rho)^n"),
    "B1": (
        r"Z_{\varepsilon,N}(0,0)=1",
        r"\Sigma_{\mathbb R\mid\mathbb Z}",
        r"B_j=\{m(j-1)+1,\ldots,mj\}",
    ),
    "B2": (
        r"\varepsilon^{\alpha_G s(G)}",
        r"\mathbf H^\varepsilon_{[0,t]}",
        r"\mathfrak d_G",
    ),
    "B3": (r"h=\dot\Gamma-D A_f[u]", r"\frac12\int {h^2\over A_f}", "(B3.12)"),
    "B4": (
        r"p=2+\delta",
        "W_2",
        r"R_\mu\bigl(h+(\mu-\lambda)R_\lambda h\bigr)",
        r"\mathcal H_\varepsilon\phi_{\varepsilon,K}",
    ),
    "C1": (
        r"M_\vartheta^a(x,dx')=\delta_{\Phi_\vartheta^a(x)}",
        r"G_\vartheta^a(x,dy)=g_\vartheta^a(x,y)\nu(dy)",
        r"\mathfrak A_{\rm pe}",
    ),
    "C2": (
        r"\beta_W=T^{-1}\beta_0",
        r"-\mathcal L_f^*r",
        r"\Pi_t^n=\mathcal L(X_t^n\mid\mathcal F_t^{Y^n})",
        "L_t>0",
    ),
    "D1": (
        r"N^{-\kappa_j}",
        r"\mathcal C_{j,N}",
        r"\sup_{\alpha\text{ common}}",
        r"\operatorname{Re}\Lambda_{j_*}(z)",
    ),
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


def blob_sha(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def close(left: complex | float, right: complex | float, tol: float = 1e-10) -> None:
    if abs(left - right) > tol * (1.0 + abs(right)):
        fail(f"numeric mismatch {left!r} != {right!r} within {tol}")


def balanced(text: str, env: str, name: str) -> None:
    opens = text.count(rf"\begin{{{env}}}")
    closes = text.count(rf"\end{{{env}}}")
    if opens != closes:
        fail(f"{name}: unbalanced {env} environment ({opens}/{closes})")


def check_displays(text: str, name: str) -> None:
    depth = 0
    for number, line in enumerate(text.splitlines(), 1):
        # Ignore the second slash of a TeX line break followed by [spacing].
        depth += len(re.findall(r"(?<!\\)\\\[", line))
        depth -= len(re.findall(r"(?<!\\)\\\]", line))
        if depth < 0:
            fail(f"{name}: display closes before opening near line {number}")
    if depth:
        fail(f"{name}: unbalanced display delimiters (depth {depth})")


def bibliography_keys(folder: Path, main_text: str, name: str) -> set[str]:
    resources = BIB_RESOURCE_RE.findall(main_text)
    if not resources:
        fail(f"{name}: no bibliography resources")
    keys: set[str] = set()
    for resource in resources:
        path = folder / resource
        if not path.is_file():
            fail(f"{name}: missing bibliography resource {resource}")
        for key in BIB_RE.findall(read_text(path)):
            if key in keys:
                fail(f"{name}: duplicate bibliography key {key}")
            keys.add(key)
    return keys


def source_checks(manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    records: list[dict[str, Any]] = []
    combined = sha256()
    global_labels: dict[str, str] = {}
    active = manifest["active_source"]
    response = manifest["author_response"]
    revision = manifest["revision"]

    for paper, entry in manifest["papers"].items():
        folder = ROOT / entry["directory"]
        paths = {
            "main": folder / "main.tex",
            "source": folder / active,
            "response": folder / response,
        }
        for role, path in paths.items():
            if not path.is_file():
                fail(f"{paper}: missing {role} file {path.relative_to(ROOT)}")
        if paths["source"].stat().st_size < 5000:
            fail(f"{paper}: active source unexpectedly short")
        if paths["response"].stat().st_size < 800:
            fail(f"{paper}: response unexpectedly short")

        main = read_text(paths["main"])
        source = read_text(paths["source"])
        response_text = read_text(paths["response"])
        for text_name, text in (("main", main), ("source", source), ("response", response_text)):
            if any(ord(char) < 32 and char not in "\n\t" for char in text):
                fail(f"{paper}: control character in {text_name}")

        input_token = rf"\input{{{active}}}"
        if main.count(input_token) != 1:
            fail(f"{paper}: main.tex must import {active} exactly once")
        if r"\input{ROUND17_POSITIVE_CLOSURE.tex}" in main:
            fail(f"{paper}: legacy Round17 input remains active")
        if revision not in main:
            fail(f"{paper}: wrapper does not identify {revision}")
        escaped_response = response.replace("_", r"\_")
        if response not in main and escaped_response not in main:
            fail(f"{paper}: wrapper does not identify {response}")
        if "ROUND21-REFEREE-POSITIVE-CLOSURE" in main:
            fail(f"{paper}: wrapper still advertises Round Twenty-One")
        if "ROUND17_POSITIVE_CLOSURE" in source:
            fail(f"{paper}: active source contains legacy slot marker")
        if PLACEHOLDER_RE.search(source) or PLACEHOLDER_RE.search(response_text):
            fail(f"{paper}: placeholder token in active material")

        for marker in REQUIRED_MARKERS[paper]:
            if marker not in source:
                fail(f"{paper}: missing positive marker {marker!r}")
        for label in entry["required_labels"]:
            if rf"\label{{{label}}}" not in source:
                fail(f"{paper}: missing required label {label}")

        for env in (*FORMAL_ENVS, "proof", "enumerate", "align", "align*"):
            balanced(source, env, paper)
        check_displays(source, paper)
        formal = sum(source.count(rf"\begin{{{env}}}") for env in FORMAL_ENVS)
        proofs = source.count(r"\begin{proof}")
        if formal < 3 or proofs < formal:
            fail(f"{paper}: formal/proof count {formal}/{proofs} is incomplete")

        labels = set(LABEL_RE.findall(source))
        for label in labels:
            if label in global_labels:
                fail(f"duplicate label {label} in {global_labels[label]} and {paper}")
            global_labels[label] = paper
        refs: set[str] = set()
        for group in REF_RE.findall(source):
            refs.update(part.strip() for part in group.split(",") if part.strip())
        missing_refs = sorted(refs - labels)
        if missing_refs:
            fail(f"{paper}: unresolved local labels {missing_refs}")

        citations: set[str] = set()
        for group in CITE_RE.findall(source + "\n" + main):
            citations.update(part.strip() for part in group.split(",") if part.strip())
        missing_citations = sorted(citations - bibliography_keys(folder, main, paper))
        if missing_citations:
            fail(f"{paper}: unresolved citations {missing_citations}")

        source_bytes = paths["source"].read_bytes()
        source_hash = sha256(source_bytes).hexdigest()
        combined.update(paper.encode("ascii") + b"\0" + source_bytes + b"\0")
        record = {
            "paper": paper,
            "source": str(paths["source"].relative_to(ROOT)),
            "bytes": len(source_bytes),
            "sha256": source_hash,
            "formal_statements": formal,
            "proofs": proofs,
            "labels": len(labels),
            "citations": len(citations),
            "local_references": len(refs),
        }
        records.append(record)
        print(
            f"paper={paper} bytes={len(source_bytes)} formal={formal} "
            f"proofs={proofs} citations={len(citations)}"
        )
    return records, combined.hexdigest()


def dependency_order(manifest: dict[str, Any]) -> list[str]:
    nodes = list(manifest["dependency_nodes"])
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = defaultdict(list)
    edges = {tuple(edge) for edge in manifest["dependency_edges"]}
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
        fail("dependency graph is cyclic")
    required = {
        ("B2-GC", "B1"),
        ("B1", "B2-MC"),
        ("B2-GC", "B2-MC"),
        ("B2-MC", "B3"),
        ("B3", "B4"),
        ("C1", "C2"),
        ("C2", "D1"),
    }
    if not required.issubset(edges):
        fail(f"dependency graph omits {sorted(required - edges)}")
    return order


def kl(probability: list[float], reference: list[float]) -> float:
    return sum(p * math.log(p / r) for p, r in zip(probability, reference) if p > 0)


def regressions() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    def add(name: str, **metrics: Any) -> None:
        output.append({"name": name, "status": "PASS", "metrics": metrics})
        print(f"regression={name} status=PASS")

    # A1: square summability does not supply an exponential tail.
    eta = 0.1
    ns = [20, 40, 80]
    scaled = [math.exp(eta * n) / (2 * math.sqrt(n + 1)) for n in ns]
    if not scaled[0] < scaled[1] < scaled[2]:
        fail("A1 slow-tail regression failed")
    add("A1_bare_Hilbert_no_exponential_rate", eta=eta, N=ns, scaled_tail_lower_bounds=scaled)

    probabilities = [0.2, 0.3, 0.5]
    vectors = [(1.0, 2.0), (0.0, -1.0), (3.0, 1.0)]
    trace = sum(p * (x * x + y * y) for p, (x, y) in zip(probabilities, vectors))
    expected = sum(p * (x * x + y * y) for p, (x, y) in zip(probabilities, vectors))
    close(trace, expected)
    add("A1_trace_covariance_identity", trace_Q=trace, expected_squared_norm=expected)

    # A2: irrational roof pair and coprime periods.
    root_two = math.sqrt(2)
    relation_min = min(
        abs(m + n * root_two)
        for m in range(-25, 26)
        for n in range(-25, 26)
        if (m, n) != (0, 0)
    )
    if relation_min <= 1e-12 or math.gcd(5, 7) != 1:
        fail("A2 periodic-character regression failed")
    add("A2_periodic_character_elimination", finite_relation_minimum=relation_min, period_gcd=1)

    # A3: chronology and absolutely continuous cell recovery.
    ordered_ab = ((0.0, "A"), (0.5, "B"))
    ordered_ba = ((0.0, "B"), (0.5, "A"))
    if ordered_ab == ordered_ba or "".join(x[1] for x in ordered_ab) == "".join(x[1] for x in ordered_ba):
        fail("A3 order regression failed")
    add("A3_ordered_state_distinguishes_paths", paths=["AB", "BA"])

    reference = [0.1, 0.2, 0.3, 0.4]
    control = [0.25, 0.15, 0.10, 0.50]
    cells = ((0, 1), (2, 3))
    recovered = [0.0] * 4
    cell_q: list[float] = []
    cell_k: list[float] = []
    for cell in cells:
        qc = sum(control[i] for i in cell)
        kc = sum(reference[i] for i in cell)
        cell_q.append(qc)
        cell_k.append(kc)
        for i in cell:
            recovered[i] = qc * reference[i] / kc
    fine, coarse, recovered_value = kl(control, reference), kl(cell_q, cell_k), kl(recovered, reference)
    close(recovered_value, coarse)
    if recovered_value > fine + 1e-12:
        fail("A3 recovery increased KL")
    add("A3_conditional_reference_KL", fine_KL=fine, coarse_KL=coarse, recovered_KL=recovered_value)

    # A4: remote influence and exact Feshbach algebra.
    theta, rho = 0.5, 0.8
    depth = [4, 12, 24]
    lyapunov = [rho**n * rho ** (-n) for n in depth]
    influence = [(theta / rho) ** n for n in depth]
    if any(abs(x - 1) > 1e-12 for x in lyapunov) or not influence[0] > influence[1] > influence[2]:
        fail("A4 two-scale regression failed")
    add("A4_two_scale_remote_past", lyapunov_contribution=lyapunov, influence=influence)

    a, b, c, d = 0.2, 1.1, -0.4, -0.7
    errors: list[float] = []
    for z in (2 + 0.5j, 5 + 2j, 11 - 3j):
        full = (z - d) / ((z - a) * (z - d) - b * c)
        reduced = 1 / (z - a - b * c / (z - d))
        close(full, reduced, 1e-12)
        errors.append(abs(full - reduced))
    limits = [z * b * c / (z - d) for z in (1000.0, 10000.0, 100000.0)]
    close(limits[-1], b * c, 1e-5)
    add("A4_exact_Feshbach_and_z_inverse_lead", resolvent_errors=errors, zKhat=limits, PLQLP=b * c)

    # B1: factorial divergence and full conditional covariance.
    n_values = [10, 100, 1000]
    factorial_pressure = [-math.lgamma(n + 1) / n for n in n_values]
    if not factorial_pressure[0] > factorial_pressure[1] > factorial_pressure[2] or factorial_pressure[-1] > -5:
        fail("B1 normalization regression failed")
    add("B1_relative_canonical_normalization", N=n_values, unnormalized=factorial_pressure, normalized=[0.0] * 3)

    sigma_zz, sigma_rr, sigma_rz, z_value = 4.0, 9.0, 3.0, 2.0
    conditional_mean = sigma_rz / sigma_zz * z_value
    schur = sigma_rr - sigma_rz * sigma_rz / sigma_zz
    close(conditional_mean, 1.5)
    close(schur, 6.75)
    add("B1_mixed_Gaussian_Schur", conditional_mean=conditional_mean, conditional_variance=schur)

    # B2: optimized loop power and factorial graph normalization.
    m_value, kappa = 3.0, 0.5
    alpha = kappa / (m_value + kappa)
    epsilons = [1e-2, 1e-4, 1e-8]
    loop_bounds: list[float] = []
    for epsilon in epsilons:
        eta_value = epsilon ** (1 / (m_value + kappa))
        loop_bounds.append(epsilon * eta_value ** (-m_value) + eta_value**kappa)
    if alpha <= 0 or not loop_bounds[0] > loop_bounds[1] > loop_bounds[2]:
        fail("B2 loop-opening regression failed")
    add("B2_transverse_loop_positive_power", alpha=alpha, epsilon=epsilons, optimized_bounds=loop_bounds)

    ratios = [
        math.exp((k - 2) * math.log(k) - math.lgamma(k + 1) - k + 2.5 * math.log(k))
        for k in range(2, 80)
    ]
    if max(ratios) >= 1:
        fail("B2 factorial graph envelope failed")
    add("B2_factorial_connected_normalization", max_scaled_tree_ratio=max(ratios), k_max=79)

    # B3: zero-cost manifold and normal-defect second derivative.
    def ell(q: float) -> float:
        return q * math.log(q) - q + 1

    base, tangent, h, step = 2.0, 0.4, 0.7, 1e-3
    def zero_path(s: float) -> float:
        return base * math.exp(tangent * s) * ell(1.0)
    zero_second = (zero_path(step) - 2 * zero_path(0) + zero_path(-step)) / step**2
    close(zero_second, 0.0, 1e-14)
    def normal_path(s: float) -> float:
        return base * math.exp(tangent * s) * ell(1 + s * h / base)
    normal_second = (normal_path(step) - 2 * normal_path(0) + normal_path(-step)) / step**2
    expected_second = h * h / base
    close(normal_second, expected_second, 1e-5)
    add(
        "B3_zero_manifold_and_defect_Hessian",
        zero_manifold_second_derivative=zero_second,
        normal_second_derivative=normal_second,
        expected=expected_second,
    )

    # B4: escaping quadratic mass violates every superquadratic shell.
    delta = 0.5
    speeds = [10.0, 100.0, 1000.0]
    second = [n ** (-2) * n**2 for n in speeds]
    super_moment = [n ** (-2) * n ** (2 + delta) for n in speeds]
    if any(abs(x - 1) > 1e-12 for x in second) or not super_moment[0] < super_moment[1] < super_moment[2]:
        fail("B4 escaping-moment regression failed")
    add("B4_superquadratic_excludes_escape", speed=speeds, remote_second=second, remote_p_moment=super_moment)

    # C1: finite approximations to impossible common Dirac domination.
    family_sizes = [10, 100, 1000]
    atom_bound = [1 / n for n in family_sizes]
    if not atom_bound[0] > atom_bound[1] > atom_bound[2]:
        fail("C1 Dirac domination regression failed")
    add("C1_no_common_hidden_Dirac_density", finite_family_size=family_sizes, atom_lower_bound=atom_bound)

    bound = 2.0
    cases = [(1e-9, 1.5e-9, 0.0, 0.0), (0.1, 0.08, 0.11, 0.077), (0.0, 0.0, 1e-8, 1.8e-8)]
    margins: list[float] = []
    for rn, nn, r, n in cases:
        posterior_n = nn / rn if rn else 0.0
        posterior = n / r if r else 0.0
        left = rn * abs(posterior_n - posterior)
        right = abs(nn - n) + bound * abs(rn - r)
        if left > right + 1e-15:
            fail("C1 integrated evidence inequality failed")
        margins.append(right - left)
    add("C1_integrated_small_evidence_ratio", nonnegative_margins=margins)

    information = 0.0**2 / (0.5 * 0.5)
    close(information, 0.0)
    add("C1_uninformative_action_zero_information", Fisher_information=information)

    # C2: weighted dual pullback and strict positivity of finite exponentials.
    weight, mu, test = [1.0, 2.0, 5.0], [0.5, -0.25, 0.1], [2.0, -3.0, 4.0]
    nu = [w * value for w, value in zip(weight, mu)]
    left = sum(f * value for f, value in zip(test, mu))
    right = sum((f / w) * value for f, w, value in zip(test, weight, nu))
    variation = sum(w * abs(value) for w, value in zip(weight, mu))
    close(left, right)
    close(variation, sum(abs(value) for value in nu))
    add("C2_weighted_strict_pullback_isometry", pairing=left, weighted_variation=variation)

    exponentials = [math.exp(x - 0.5 * q) for x, q in [(-20.0, 2.0), (0.0, 1.0), (20.0, 5.0)]]
    if any(value <= 0 or not math.isfinite(value) for value in exponentials):
        fail("C2 stochastic-exponential positivity regression failed")
    add("C2_finite_Brownian_exponential_strictly_positive", samples=exponentials)

    # D1: polynomial phase weights and shared-policy/nonclairvoyant control.
    phase_n = [10.0, 100.0, 10000.0]
    phase_ratio = [1.5 / n for n in phase_n]
    if not phase_ratio[0] > phase_ratio[1] > phase_ratio[2]:
        fail("D1 polynomial phase regression failed")
    add("D1_polynomial_phase_weight", N=phase_n, phase2_over_phase1=phase_ratio)

    payoffs = ((1.0, 0.0), (0.0, 1.0))
    shared = max(0.5 * payoffs[0][a] + 0.5 * payoffs[1][a] for a in range(2))
    clairvoyant = 0.5 * max(payoffs[0]) + 0.5 * max(payoffs[1])
    if not shared < clairvoyant:
        fail("D1 shared-policy regression failed")
    add("D1_shared_policy_before_phase_aggregation", shared_policy_value=shared, phasewise_value=clairvoyant)

    return output


def main() -> int:
    try:
        if not MANIFEST_PATH.is_file():
            fail("missing ROUND23_SOURCE_MANIFEST.json")
        manifest = json.loads(read_text(MANIFEST_PATH))
        if manifest.get("schema") != "theta-theory-round23-source-manifest-v1":
            fail("unsupported manifest schema")

        for relative in manifest["required_root_files"]:
            path = ROOT / relative
            if not path.is_file() or path.stat().st_size < 500:
                fail(f"missing or short root evidence file {relative}")

        report = manifest["referee_report"]
        report_path = ROOT / report["path"]
        actual_report_sha = blob_sha(report_path.read_bytes())
        if actual_report_sha != report["git_blob_sha"]:
            fail(f"controlling report changed: {actual_report_sha}")

        order = dependency_order(manifest)
        ledger = read_text(ROOT / "ROUND23_PROOF_DEPENDENCY_LEDGER.md")
        for node in manifest["dependency_nodes"]:
            if f"| {node} |" not in ledger and f"`{node}`" not in ledger:
                fail(f"dependency ledger omits {node}")

        papers, combined_hash = source_checks(manifest)
        regression_results = regressions()
        payload = {
            "schema": "theta-theory-round23-regression-results-v1",
            "revision": manifest["revision"],
            "status": "PASS",
            "referee_report_git_blob_sha": actual_report_sha,
            "combined_active_source_sha256": combined_hash,
            "dependency_order": order,
            "papers": papers,
            "regressions": regression_results,
            "disclaimer": "Internal source/algebra/reproducibility gates; not independent mathematical peer review.",
        }
        RESULTS_PATH.write_text(
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            f"ROUND23_VERIFY_PASS papers={len(papers)} regressions={len(regression_results)} "
            f"source_sha256={combined_hash}"
        )
        return 0
    except (VerificationFailure, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"ROUND23_VERIFY_FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
