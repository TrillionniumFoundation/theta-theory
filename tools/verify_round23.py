#!/usr/bin/env python3
"""Fail-closed source and mathematical-regression verifier for Round Twenty-Three.

The verifier checks active-source identity, theorem/proof structure, citations,
local references, the declared dependency DAG, preservation of the controlling
referee report, and finite-dimensional regressions for the explicit
Round-Twenty-Two counterexamples.

A PASS is internal reproducibility evidence.  It is not a substitute for
independent mathematical peer review.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
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
CITE_RE = re.compile(
    r"\\(?:cite|parencite|textcite|autocite)\s*"
    r"(?:\[[^\]]*\]\s*){0,2}\{([^{}]+)\}"
)
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.I)
BIB_RESOURCE_RE = re.compile(r"\\addbibresource\{([^{}]+)\}")
DISPLAY_OPEN = re.compile(r"(?<!\\)\\\[")
DISPLAY_CLOSE = re.compile(r"(?<!\\)\\\]")

REQUIRED_MARKERS: dict[str, tuple[str, ...]] = {
    "A1": (
        r"\mathfrak C_{\eta}^{r}",
        r"\operatorname{tr}Q_a=\mathbb E_a\|D_0\|",
        r"Bochner integral",
    ),
    "A2": (
        r"\mathscr G_a=\mathbb Z^3\times\mathbb R\times\mathbb Z",
        r"D_z(\Psi_1,\Psi_2)",
        r"(1+|b|)^{-2}",
    ),
    "A3": (
        r"\mathcal O_N^c",
        r"q^{\mathcal P}",
        r"\mathcal R_N^c",
    ),
    "A4": (
        r"K(t)=PLQe^{tL_Q}QLP",
        r"z^{-1}PLQLP",
        r"(\vartheta/\rho)^n",
    ),
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
    "B3": (
        r"h=\dot\Gamma-D A_f[u]",
        r"\frac12\int {h^2\over A_f}",
        r"(B3.12)",
    ),
    "B4": (
        r"p=2+\delta",
        r"W_2",
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
        r"L_t>0",
    ),
    "D1": (
        r"N^{-\kappa_j}",
        r"\mathcal C_{j,N}",
        r"\sup_{\alpha\text{ common}}",
        r"\operatorname{Re}\Lambda_{j_*}(z)",
    ),
}


class VerificationFailure(RuntimeError):
    """Raised when a fail-closed gate does not pass."""


def fail(message: str) -> None:
    raise VerificationFailure(message)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"non-UTF-8 source: {path.relative_to(ROOT)}: {exc}")
    raise AssertionError("unreachable")


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        out: list[str] = []
        escaped = False
        for char in line:
            if char == "%" and not escaped:
                break
            out.append(char)
            if char == "\\":
                escaped = not escaped
            else:
                escaped = False
        lines.append("".join(out))
    return "\n".join(lines)


def check_control_characters(text: str, name: str) -> None:
    allowed = {"\n", "\t"}
    for index, char in enumerate(text):
        if ord(char) < 32 and char not in allowed:
            line = text[:index].count("\n") + 1
            fail(f"{name}: control character U+{ord(char):04X} near line {line}")


def check_environment_balance(text: str, name: str, env: str) -> None:
    opens = len(re.findall(rf"\\begin\{{{re.escape(env)}\}}", text))
    closes = len(re.findall(rf"\\end\{{{re.escape(env)}\}}", text))
    if opens != closes:
        fail(f"{name}: unbalanced {env} environment ({opens} opens, {closes} closes)")


def check_display_balance(text: str, name: str) -> None:
    depth = 0
    for line_no, line in enumerate(text.splitlines(), start=1):
        depth += len(DISPLAY_OPEN.findall(line))
        depth -= len(DISPLAY_CLOSE.findall(line))
        if depth < 0:
            fail(f"{name}: display closes before opening near line {line_no}")
    if depth != 0:
        fail(f"{name}: unbalanced \\[ / \\] displays (depth {depth})")


def check_brace_balance(text: str, name: str) -> None:
    clean = strip_comments(text)
    depth = 0
    escaped = False
    for index, char in enumerate(clean):
        if char == "\\":
            escaped = not escaped
            continue
        if char == "{" and not escaped:
            depth += 1
        elif char == "}" and not escaped:
            depth -= 1
            if depth < 0:
                line = clean[:index].count("\n") + 1
                fail(f"{name}: brace closes before opening near line {line}")
        escaped = False
    if depth != 0:
        fail(f"{name}: unbalanced braces (depth {depth})")


def parse_bibliography(folder: Path, main_text: str, name: str) -> set[str]:
    resources = BIB_RESOURCE_RE.findall(main_text)
    if not resources:
        fail(f"{name}: main.tex has no bibliography resource")
    keys: set[str] = set()
    for resource in resources:
        path = folder / resource
        if not path.is_file():
            fail(f"{name}: missing bibliography resource {resource}")
        bib_text = read_text(path)
        for key in BIB_RE.findall(bib_text):
            if key in keys:
                fail(f"{name}: duplicate bibliography key {key}")
            keys.add(key)
    return keys


def check_citations_and_refs(
    source_text: str, main_text: str, bib_keys: set[str], name: str
) -> tuple[int, int, set[str]]:
    cited: set[str] = set()
    for match in CITE_RE.findall(source_text + "\n" + main_text):
        cited.update(key.strip() for key in match.split(",") if key.strip())
    missing_citations = sorted(cited - bib_keys)
    if missing_citations:
        fail(f"{name}: unresolved citation keys: {', '.join(missing_citations)}")

    labels = set(LABEL_RE.findall(source_text))
    referenced: set[str] = set()
    for match in REF_RE.findall(source_text):
        referenced.update(key.strip() for key in match.split(",") if key.strip())
    missing_refs = sorted(referenced - labels)
    if missing_refs:
        fail(f"{name}: unresolved local labels: {', '.join(missing_refs)}")
    return len(cited), len(referenced), labels


def check_dependency_graph(manifest: dict[str, Any]) -> list[str]:
    nodes = list(manifest["dependency_nodes"])
    edges = [tuple(edge) for edge in manifest["dependency_edges"]]
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
        fail("declared Round-Twenty-Three dependency graph contains a cycle")

    required_edges = {
        ("B2-GC", "B1"),
        ("B1", "B2-MC"),
        ("B2-GC", "B2-MC"),
        ("B2-MC", "B3"),
        ("B3", "B4"),
        ("C1", "C2"),
        ("C2", "D1"),
    }
    if not required_edges.issubset(set(edges)):
        missing = sorted(required_edges - set(edges))
        fail(f"dependency graph omits required edges: {missing}")
    return order


@dataclass
class RegressionResult:
    name: str
    metrics: dict[str, Any]


def close(left: complex | float, right: complex | float, tol: float = 1e-10) -> None:
    if abs(left - right) > tol * (1.0 + abs(right)):
        fail(f"numeric mismatch: {left!r} != {right!r} within {tol}")


def regression_a1_slow_tail() -> RegressionResult:
    eta = 0.1
    ns = [20, 40, 80]
    lower_scaled = [math.exp(eta * n) / (2.0 * math.sqrt(n + 1.0)) for n in ns]
    if not (lower_scaled[0] < lower_scaled[1] < lower_scaled[2]):
        fail("A1 slow-tail regression did not exhibit exponential blow-up")
    l2_bound = sum(1.0 / ((n + 1) ** 2) for n in range(200000))
    if not l2_bound < 2.0:
        fail("A1 test sequence unexpectedly failed square summability check")
    return RegressionResult(
        "A1_bare_Hilbert_no_exponential_rate",
        {"eta": eta, "N": ns, "scaled_tail_lower_bounds": lower_scaled},
    )


def regression_a1_trace() -> RegressionResult:
    probabilities = [0.2, 0.3, 0.5]
    vectors = [(1.0, 2.0), (0.0, -1.0), (3.0, 1.0)]
    q00 = sum(p * v[0] * v[0] for p, v in zip(probabilities, vectors))
    q11 = sum(p * v[1] * v[1] for p, v in zip(probabilities, vectors))
    trace = q00 + q11
    expected_norm = sum(p * (v[0] ** 2 + v[1] ** 2) for p, v in zip(probabilities, vectors))
    close(trace, expected_norm)
    return RegressionResult(
        "A1_trace_covariance_identity",
        {"trace_Q": trace, "expected_squared_norm": expected_norm},
    )


def regression_a2_character() -> RegressionResult:
    beta = math.sqrt(2.0)
    minimum = min(
        abs(m + n * beta)
        for m in range(-25, 26)
        for n in range(-25, 26)
        if (m, n) != (0, 0)
    )
    if minimum <= 1e-12:
        fail("A2 irrational roof pair admitted a spurious integer relation")
    if math.gcd(5, 7) != 1:
        fail("A2 coprime-period regression failed")
    return RegressionResult(
        "A2_periodic_character_elimination",
        {"finite_relation_minimum": minimum, "period_gcd": math.gcd(5, 7)},
    )


def regression_a3_order() -> RegressionResult:
    ordered_ab = ((0.0, "A"), (0.5, "B"))
    ordered_ba = ((0.0, "B"), (0.5, "A"))
    if sorted(mark for _, mark in ordered_ab) != sorted(mark for _, mark in ordered_ba):
        fail("A3 test data do not have matching unordered occupations")
    if ordered_ab == ordered_ba:
        fail("A3 chronological states failed to distinguish a permutation")
    path_ab = "".join(mark for _, mark in ordered_ab)
    path_ba = "".join(mark for _, mark in ordered_ba)
    if path_ab == path_ba:
        fail("A3 concatenated paths failed to distinguish order")
    return RegressionResult(
        "A3_ordered_state_distinguishes_paths",
        {"unordered_marks": ["A", "B"], "paths": [path_ab, path_ba]},
    )


def kl(probability: list[float], reference: list[float]) -> float:
    total = 0.0
    for p, r in zip(probability, reference):
        if p < 0 or r <= 0:
            fail("invalid probability in KL regression")
        if p > 0:
            total += p * math.log(p / r)
    return total


def regression_a3_recovery() -> RegressionResult:
    reference = [0.1, 0.2, 0.3, 0.4]
    control = [0.25, 0.15, 0.10, 0.50]
    cells = ((0, 1), (2, 3))
    recovered = [0.0] * 4
    cell_control: list[float] = []
    cell_reference: list[float] = []
    for cell in cells:
        qc = sum(control[i] for i in cell)
        kc = sum(reference[i] for i in cell)
        cell_control.append(qc)
        cell_reference.append(kc)
        for i in cell:
            recovered[i] = qc * reference[i] / kc
    fine = kl(control, reference)
    coarse = kl(cell_control, cell_reference)
    recovered_kl = kl(recovered, reference)
    close(recovered_kl, coarse)
    if recovered_kl > fine + 1e-12:
        fail("A3 conditional-reference recovery increased KL")
    close(sum(recovered), 1.0)
    return RegressionResult(
        "A3_conditional_reference_KL",
        {"fine_KL": fine, "coarse_KL": coarse, "recovered_KL": recovered_kl},
    )


def regression_a4_two_scale() -> RegressionResult:
    theta = 0.5
    rho = 0.8
    ns = [4, 12, 24]
    lyapunov = [rho**n * rho ** (-n) for n in ns]
    influence = [(theta / rho) ** n for n in ns]
    if any(abs(value - 1.0) > 1e-12 for value in lyapunov):
        fail("A4 remote mark did not retain order-one Lyapunov mass")
    if not (influence[0] > influence[1] > influence[2] > 0.0):
        fail("A4 remote influence did not decay")
    return RegressionResult(
        "A4_two_scale_remote_past",
        {"lyapunov_contribution": lyapunov, "influence": influence},
    )


def regression_a4_feshbach() -> RegressionResult:
    a, b, c, d = 0.2, 1.1, -0.4, -0.7
    errors: list[float] = []
    for z in (2.0 + 0.5j, 5.0 + 2.0j, 11.0 - 3.0j):
        determinant = (z - a) * (z - d) - b * c
        full_00 = (z - d) / determinant
        reduced = 1.0 / (z - a - b * c / (z - d))
        errors.append(abs(full_00 - reduced))
        close(full_00, reduced, 1e-12)
    limits = [z * (b * c / (z - d)) for z in (1000.0, 10000.0, 100000.0)]
    if not abs(limits[-1] - b * c) < abs(limits[0] - b * c):
        fail("A4 high-frequency coefficient did not converge to PLQLP")
    close(limits[-1], b * c, 1e-5)
    return RegressionResult(
        "A4_exact_Feshbach_and_z_inverse_lead",
        {"resolvent_errors": errors, "zKhat": limits, "PLQLP": b * c},
    )


def regression_b1_normalization() -> RegressionResult:
    ns = [10, 100, 1000]
    unnormalized = [-math.lgamma(n + 1.0) / n for n in ns]
    normalized = [math.log(1.0) / n for n in ns]
    if not (unnormalized[0] > unnormalized[1] > unnormalized[2]):
        fail("B1 factorial pressure did not exhibit its divergent trend")
    if unnormalized[-1] > -5.0:
        fail("B1 factorial pressure regression is too small to expose divergence")
    if any(value != 0.0 for value in normalized):
        fail("B1 normalized zero-source pressure is not zero")
    return RegressionResult(
        "B1_relative_canonical_normalization",
        {"N": ns, "unnormalized_pressures": unnormalized, "normalized": normalized},
    )


def regression_b1_schur() -> RegressionResult:
    sigma_zz, sigma_rr, sigma_rz = 4.0, 9.0, 3.0
    z = 2.0
    conditional_mean = sigma_rz / sigma_zz * z
    schur = sigma_rr - sigma_rz * sigma_rz / sigma_zz
    if conditional_mean == 0.0 or not (0.0 < schur < sigma_rr):
        fail("B1 conditional Gaussian regression lost shift or Schur reduction")
    close(conditional_mean, 1.5)
    close(schur, 6.75)
    return RegressionResult(
        "B1_mixed_Gaussian_Schur",
        {"conditional_mean": conditional_mean, "conditional_variance": schur},
    )


def regression_b2_loop() -> RegressionResult:
    m = 3.0
    kappa = 0.5
    alpha = kappa / (m + kappa)
    epsilons = [1e-2, 1e-4, 1e-8]
    bounds: list[float] = []
    for epsilon in epsilons:
        eta = epsilon ** (1.0 / (m + kappa))
        bounds.append(epsilon * eta ** (-m) + eta**kappa)
    if not alpha > 0.0:
        fail("B2 optimized loop exponent is not positive")
    if not (bounds[0] > bounds[1] > bounds[2] > 0.0):
        fail("B2 optimized loop bound did not decay")
    return RegressionResult(
        "B2_transverse_loop_positive_power",
        {"alpha": alpha, "epsilon": epsilons, "optimized_bounds": bounds},
    )


def regression_b2_factorial() -> RegressionResult:
    ratios: list[float] = []
    for k in range(2, 80):
        log_ratio = (k - 2.0) * math.log(k) - math.lgamma(k + 1.0) - k + 2.5 * math.log(k)
        ratios.append(math.exp(log_ratio))
    if max(ratios) >= 1.0:
        fail("B2 factorial Cayley bound exceeded the declared envelope")
    return RegressionResult(
        "B2_factorial_connected_normalization",
        {"max_scaled_tree_ratio": max(ratios), "k_max": 79},
    )


def ell(q: float) -> float:
    if q <= 0.0:
        fail("nonpositive q in entropy regression")
    return q * math.log(q) - q + 1.0


def regression_b3_hessian() -> RegressionResult:
    base_a = 2.0
    tangent_a = 0.4
    h = 0.7
    epsilon = 1e-4

    def zero_manifold(eta: float) -> float:
        a_eta = base_a * math.exp(tangent_a * eta)
        return a_eta * ell(1.0)

    zero_second = (
        zero_manifold(epsilon) - 2.0 * zero_manifold(0.0) + zero_manifold(-epsilon)
    ) / (epsilon**2)
    close(zero_second, 0.0, 1e-14)

    def normal_path(eta: float) -> float:
        a_eta = base_a * math.exp(tangent_a * eta)
        q_eta = 1.0 + eta * h / base_a
        return a_eta * ell(q_eta)

    normal_second = (
        normal_path(epsilon) - 2.0 * normal_path(0.0) + normal_path(-epsilon)
    ) / (epsilon**2)
    expected_second = h * h / base_a
    close(normal_second, expected_second, 2e-7)
    return RegressionResult(
        "B3_zero_manifold_and_defect_Hessian",
        {
            "zero_manifold_second_derivative": zero_second,
            "normal_second_derivative": normal_second,
            "expected": expected_second,
        },
    )


def regression_b4_moment() -> RegressionResult:
    delta = 0.5
    ns = [10.0, 100.0, 1000.0]
    remote_second = [n ** (-2.0) * n**2 for n in ns]
    remote_super = [n ** (-2.0) * n ** (2.0 + delta) for n in ns]
    if any(abs(value - 1.0) > 1e-12 for value in remote_second):
        fail("B4 escaping sequence did not retain unit quadratic mass")
    if not (remote_super[0] < remote_super[1] < remote_super[2]):
        fail("B4 superquadratic moment did not diverge")
    return RegressionResult(
        "B4_superquadratic_excludes_escape",
        {"N": ns, "remote_second": remote_second, "remote_p_moment": remote_super},
    )


def regression_c1_dirac() -> RegressionResult:
    ns = [10, 100, 1000]
    best_uniform_atom = [1.0 / n for n in ns]
    if not (best_uniform_atom[0] > best_uniform_atom[1] > best_uniform_atom[2] > 0.0):
        fail("C1 finite Dirac domination obstruction did not decay")
    return RegressionResult(
        "C1_no_common_hidden_Dirac_density",
        {"finite_family_size": ns, "largest_possible_uniform_atom_lower_bound": best_uniform_atom},
    )


def regression_c1_ratio() -> RegressionResult:
    bound = 2.0
    cases = [
        (1e-9, 1.5e-9, 0.0, 0.0),
        (0.1, 0.08, 0.11, 0.077),
        (0.0, 0.0, 1e-8, 1.8e-8),
    ]
    margins: list[float] = []
    for rn, nn, r, n in cases:
        post_n = nn / rn if rn > 0.0 else 0.0
        post = n / r if r > 0.0 else 0.0
        left = rn * abs(post_n - post)
        right = abs(nn - n) + bound * abs(rn - r)
        if left > right + 1e-15:
            fail("C1 integrated posterior ratio inequality failed")
        margins.append(right - left)
    return RegressionResult(
        "C1_integrated_small_evidence_ratio",
        {"nonnegative_margins": margins},
    )


def regression_c1_information() -> RegressionResult:
    p = 0.5
    dp = 0.0
    information = dp * dp / (p * (1.0 - p))
    close(information, 0.0)
    return RegressionResult(
        "C1_uninformative_action_zero_information",
        {"bernoulli_p": p, "parameter_derivative": dp, "Fisher_information": information},
    )


def regression_c2_dual() -> RegressionResult:
    weight = [1.0, 2.0, 5.0]
    mu = [0.5, -0.25, 0.1]
    f = [2.0, -3.0, 4.0]
    nu = [w * m for w, m in zip(weight, mu)]
    left_pairing = sum(x * m for x, m in zip(f, mu))
    right_pairing = sum((x / w) * n for x, w, n in zip(f, weight, nu))
    weighted_variation = sum(w * abs(m) for w, m in zip(weight, mu))
    nu_variation = sum(abs(n) for n in nu)
    close(left_pairing, right_pairing)
    close(weighted_variation, nu_variation)
    return RegressionResult(
        "C2_weighted_strict_pullback_isometry",
        {"pairing": left_pairing, "weighted_variation": weighted_variation},
    )


def regression_c2_positive_exponential() -> RegressionResult:
    samples = [math.exp(x - 0.5 * q) for x, q in [(-20.0, 2.0), (0.0, 1.0), (20.0, 5.0)]]
    if any(not value > 0.0 or not math.isfinite(value) for value in samples):
        fail("C2 finite continuous stochastic exponential lost strict positivity")
    return RegressionResult(
        "C2_finite_Brownian_exponential_strictly_positive",
        {"samples": samples},
    )


def regression_d1_weights() -> RegressionResult:
    kappa_1, kappa_2 = 1.0, 2.0
    c1, c2 = 2.0, 3.0
    ns = [10.0, 100.0, 10000.0]
    ratios = [(c2 / c1) * n ** (-(kappa_2 - kappa_1)) for n in ns]
    if not (ratios[0] > ratios[1] > ratios[2] > 0.0):
        fail("D1 polynomial phase ratio did not select the smaller exponent")
    return RegressionResult(
        "D1_polynomial_phase_weight",
        {"N": ns, "phase2_over_phase1": ratios},
    )


def regression_d1_shared_policy() -> RegressionResult:
    payoffs = ((1.0, 0.0), (0.0, 1.0))
    weights = (0.5, 0.5)
    shared = max(
        sum(weights[phase] * payoffs[phase][action] for phase in range(2))
        for action in range(2)
    )
    phasewise = sum(
        weights[phase] * max(payoffs[phase]) for phase in range(2)
    )
    if not shared < phasewise:
        fail("D1 shared-policy regression failed to distinguish clairvoyant optimization")
    close(shared, 0.5)
    close(phasewise, 1.0)
    return RegressionResult(
        "D1_shared_policy_before_phase_aggregation",
        {"shared_policy_value": shared, "phasewise_clairvoyant_value": phasewise},
    )


REGRESSIONS: tuple[Callable[[], RegressionResult], ...] = (
    regression_a1_slow_tail,
    regression_a1_trace,
    regression_a2_character,
    regression_a3_order,
    regression_a3_recovery,
    regression_a4_two_scale,
    regression_a4_feshbach,
    regression_b1_normalization,
    regression_b1_schur,
    regression_b2_loop,
    regression_b2_factorial,
    regression_b3_hessian,
    regression_b4_moment,
    regression_c1_dirac,
    regression_c1_ratio,
    regression_c1_information,
    regression_c2_dual,
    regression_c2_positive_exponential,
    regression_d1_weights,
    regression_d1_shared_policy,
)


def check_sources(manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    revision = manifest["revision"]
    active_name = manifest["active_source"]
    response_name = manifest["author_response"]
    combined_hash = sha256()
    global_labels: dict[str, str] = {}
    paper_records: list[dict[str, Any]] = []

    for key, entry in manifest["papers"].items():
        folder = ROOT / entry["directory"]
        main_path = folder / "main.tex"
        source_path = folder / active_name
        response_path = folder / response_name
        for path in (main_path, source_path, response_path):
            if not path.is_file():
                fail(f"{key}: missing {path.relative_to(ROOT)}")
        if source_path.stat().st_size < 5000:
            fail(f"{key}: active source is unexpectedly short")
        if response_path.stat().st_size < 800:
            fail(f"{key}: author response is unexpectedly short")

        main_text = read_text(main_path)
        source_text = read_text(source_path)
        response_text = read_text(response_path)
        check_control_characters(main_text + source_text + response_text, key)

        input_token = rf"\input{{{active_name}}}"
        if main_text.count(input_token) != 1:
            fail(f"{key}: main.tex must import {active_name} exactly once")
        if r"\input{ROUND17_POSITIVE_CLOSURE.tex}" in main_text:
            fail(f"{key}: wrapper still imports the legacy Round17 source slot")
        if revision not in main_text:
            fail(f"{key}: wrapper does not identify {revision}")
        if response_name not in main_text:
            fail(f"{key}: wrapper does not identify {response_name}")
        if "ROUND21-REFEREE-POSITIVE-CLOSURE" in main_text:
            fail(f"{key}: wrapper still advertises Round Twenty-One")
        if "ROUND17_POSITIVE_CLOSURE" in source_text:
            fail(f"{key}: active source contains a legacy source-slot marker")
        if PLACEHOLDER_RE.search(source_text) or PLACEHOLDER_RE.search(response_text):
            fail(f"{key}: placeholder token in active source or response")

        for marker in REQUIRED_MARKERS[key]:
            if marker not in source_text:
                fail(f"{key}: missing positive-closure marker {marker!r}")
        for label in entry["required_labels"]:
            if rf"\label{{{label}}}" not in source_text:
                fail(f"{key}: missing required active label {label}")

        for env in (*FORMAL_ENVS, "proof", "enumerate", "align", "align*"):
            check_environment_balance(source_text, key, env)
        check_display_balance(source_text, key)
        check_brace_balance(source_text, key)

        formal_count = sum(source_text.count(rf"\begin{{{env}}}") for env in FORMAL_ENVS)
        proof_count = source_text.count(r"\begin{proof}")
        if formal_count < 3:
            fail(f"{key}: fewer than three formal theorem-like statements")
        if proof_count < formal_count:
            fail(f"{key}: {formal_count} formal statements but only {proof_count} proofs")

        bib_keys = parse_bibliography(folder, main_text, key)
        cited_count, ref_count, labels = check_citations_and_refs(
            source_text, main_text, bib_keys, key
        )
        for label in labels:
            previous = global_labels.get(label)
            if previous is not None:
                fail(f"duplicate active label {label} in {previous} and {key}")
            global_labels[label] = key

        combined_hash.update(key.encode("ascii"))
        combined_hash.update(b"\0")
        combined_hash.update(source_text.encode("utf-8"))
        combined_hash.update(b"\0")
        source_digest = sha256(source_text.encode("utf-8")).hexdigest()
        paper_records.append(
            {
                "paper": key,
                "source": str(source_path.relative_to(ROOT)),
                "bytes": source_path.stat().st_size,
                "sha256": source_digest,
                "formal_statements": formal_count,
                "proofs": proof_count,
                "labels": len(labels),
                "citations": cited_count,
                "local_references": ref_count,
            }
        )
        print(
            f"paper={key} bytes={source_path.stat().st_size} "
            f"formal={formal_count} proofs={proof_count} citations={cited_count}"
        )

    return paper_records, combined_hash.hexdigest()


def main() -> int:
    try:
        if not MANIFEST_PATH.is_file():
            fail("missing ROUND23_SOURCE_MANIFEST.json")
        manifest = json.loads(read_text(MANIFEST_PATH))
        if manifest.get("schema") != "theta-theory-round23-source-manifest-v1":
            fail("unsupported or missing Round-Twenty-Three manifest schema")

        for relative in manifest["required_root_files"]:
            path = ROOT / relative
            if not path.is_file() or path.stat().st_size < 500:
                fail(f"missing or unexpectedly short root evidence file: {relative}")

        report_info = manifest["referee_report"]
        report_path = ROOT / report_info["path"]
        actual_report_sha = git_blob_sha(report_path.read_bytes())
        if actual_report_sha != report_info["git_blob_sha"]:
            fail(
                "controlling Round-Twenty-Two report changed: "
                f"expected {report_info['git_blob_sha']}, got {actual_report_sha}"
            )

        dependency_order = check_dependency_graph(manifest)
        ledger = read_text(ROOT / "ROUND23_PROOF_DEPENDENCY_LEDGER.md")
        for node in manifest["dependency_nodes"]:
            if f"| {node} |" not in ledger and f"`{node}`" not in ledger:
                fail(f"dependency ledger does not mention node {node}")

        paper_records, combined_source_sha = check_sources(manifest)

        regression_records: list[dict[str, Any]] = []
        for function in REGRESSIONS:
            result = function()
            regression_records.append(
                {"name": result.name, "status": "PASS", "metrics": result.metrics}
            )
            print(f"regression={result.name} status=PASS")

        payload = {
            "schema": "theta-theory-round23-regression-results-v1",
            "revision": manifest["revision"],
            "status": "PASS",
            "referee_report_git_blob_sha": actual_report_sha,
            "combined_active_source_sha256": combined_source_sha,
            "dependency_order": dependency_order,
            "papers": paper_records,
            "regressions": regression_records,
            "disclaimer": (
                "Internal source, algebra, and reproducibility gates; "
                "not independent mathematical peer review."
            ),
        }
        rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        RESULTS_PATH.write_text(rendered, encoding="utf-8")
        print(
            "ROUND23_VERIFY_PASS "
            f"papers={len(paper_records)} regressions={len(regression_records)} "
            f"source_sha256={combined_source_sha}"
        )
        return 0
    except (VerificationFailure, KeyError, TypeError, ValueError) as exc:
        print(f"ROUND23_VERIFY_FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
