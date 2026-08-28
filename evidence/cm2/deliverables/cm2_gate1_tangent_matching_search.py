#!/usr/bin/env python3
"""Exploratory search for QNL/connector tangent-line matching words.

This file is intentionally a *non-rigorous search utility*: it uses binary64
arithmetic only to discover candidate solid-collision words which can later be
replayed with Arb.  It never prints a certification label.

Coordinates are the outward normal angle ``theta`` and outgoing tangential
momentum ``p`` on either the gray or white circular obstacle of the centered
two-disk torus billiard.  The universal-cover first-hit search is exhaustive
on a radius-four lattice window; the caller rejects any orbit which leaves
the central search window.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np


RADIUS = {"G": 9.0 / 25.0, "W": 4.0 / 25.0}
BASE_CENTER = {"G": np.array([0.0, 0.0]), "W": np.array([0.5, 0.5])}
CONNECTOR_THETA = float(
    "0.78409255751959244111062347294760048351680250557700470160436187178052747618097046"
)
QNL_THETA = math.pi / 4.0


@dataclass(frozen=True)
class State:
    kind: str
    theta: float
    p: float


@dataclass(frozen=True)
class Step:
    state: State
    lift: tuple[int, int]
    flight: float
    incidence: float
    gap: float


def wrap_angle(theta: float) -> float:
    return (theta + math.pi) % (2.0 * math.pi) - math.pi


def phase_point(state: State) -> tuple[np.ndarray, np.ndarray]:
    normal = np.array([math.cos(state.theta), math.sin(state.theta)])
    tangent = np.array([-normal[1], normal[0]])
    if abs(state.p) >= 1.0:
        raise ValueError("nonphysical momentum")
    velocity = math.sqrt(1.0 - state.p * state.p) * normal + state.p * tangent
    position = BASE_CENTER[state.kind] + RADIUS[state.kind] * normal
    return position, velocity


def forward(state: State, lattice_radius: int = 4) -> Step:
    position, velocity = phase_point(state)
    candidates: list[tuple[float, str, int, int, np.ndarray]] = []
    for kind in ("G", "W"):
        base = BASE_CENTER[kind]
        radius = RADIUS[kind]
        for i in range(-lattice_radius, lattice_radius + 1):
            for j in range(-lattice_radius, lattice_radius + 1):
                center = base + np.array([float(i), float(j)])
                displacement = position - center
                linear = float(np.dot(displacement, velocity))
                offset = float(np.dot(displacement, displacement) - radius * radius)
                discriminant = linear * linear - offset
                if discriminant <= 0.0:
                    continue
                root = math.sqrt(discriminant)
                for flight in (-linear - root, -linear + root):
                    if flight > 1.0e-10:
                        candidates.append((flight, kind, i, j, center))
                        break
    if not candidates:
        raise RuntimeError("no forward collision in lattice window")
    candidates.sort(key=lambda item: item[0])
    flight, kind, i, j, center = candidates[0]
    second_flight = candidates[1][0] if len(candidates) > 1 else math.inf
    impact = position + flight * velocity
    normal = (impact - center) / RADIUS[kind]
    normal /= np.linalg.norm(normal)
    incoming = -float(np.dot(velocity, normal))
    if incoming <= 0.0:
        raise RuntimeError("selected root is not incoming")
    reflected = velocity + 2.0 * incoming * normal
    tangent = np.array([-normal[1], normal[0]])
    momentum = float(np.dot(reflected, tangent))
    theta = math.atan2(float(normal[1]), float(normal[0]))
    return Step(
        State(kind, theta, momentum),
        (i, j),
        flight,
        incoming,
        second_flight - flight,
    )


def reverse(state: State, lattice_radius: int = 4) -> Step:
    reversed_state = State(state.kind, state.theta, -state.p)
    step = forward(reversed_state, lattice_radius=lattice_radius)
    return Step(
        State(step.state.kind, step.state.theta, -step.state.p),
        step.lift,
        step.flight,
        step.incidence,
        step.gap,
    )


def iterate(state: State, count: int, backward: bool = False) -> tuple[State, tuple[str, ...]]:
    word = [state.kind]
    current = state
    for _ in range(count):
        step = reverse(current) if backward else forward(current)
        current = step.state
        word.append(current.kind)
    return current, tuple(word)


def trace_iterate(state: State, count: int, backward: bool = False) -> tuple[State, tuple[tuple[str, int, int], ...]]:
    trace = [(state.kind, 0, 0)]
    current = state
    for _ in range(count):
        step = reverse(current) if backward else forward(current)
        current = step.state
        trace.append((current.kind, step.lift[0], step.lift[1]))
    return current, tuple(trace)


def eigenslopes() -> tuple[float, float]:
    sqrt_two = math.sqrt(2.0)
    beta_a = (859.0 - 550.0 * sqrt_two) / 100.0
    gamma_a = 625.0 * (25.0 - 4.0 * sqrt_two) / 324.0
    slope_a = math.sqrt(gamma_a / beta_a)

    # Midpoints of the frozen Arb enclosure suffice for search seeding.
    slope_b = math.sqrt(364_394_817.0 / 7_928_333.0)
    return slope_a, slope_b


def perturb(base: State, scalar: float, slope: float, stable: bool) -> State:
    sign = -1.0 if stable else 1.0
    ds = scalar
    dp = sign * slope * scalar
    return State(base.kind, wrap_angle(base.theta + ds / RADIUS[base.kind]), base.p + dp)


def verify_periodic_words() -> None:
    qnl = State("G", QNL_THETA, 0.0)
    qnl_final, qnl_word = iterate(qnl, 2)
    connector = State("G", CONNECTOR_THETA, 0.0)
    connector_final, connector_word = iterate(connector, 14)
    expected_connector = tuple("GWGWGWGGGWGWGWG")
    print("binary64 periodic-word diagnostics")
    print(f"  qnl_word={''.join(qnl_word)}")
    print(
        "  qnl_residual="
        f"({wrap_angle(qnl_final.theta-QNL_THETA):.3e},{qnl_final.p:.3e})"
    )
    print(f"  connector_word={''.join(connector_word)}")
    print(
        "  connector_residual="
        f"({wrap_angle(connector_final.theta-CONNECTOR_THETA):.3e},{connector_final.p:.3e})"
    )
    if qnl_word != ("G", "W", "G"):
        raise RuntimeError("QNL binary64 word mismatch")
    if connector_word != expected_connector:
        raise RuntimeError("connector binary64 word mismatch")


def sample_curve(
    base: State,
    slope: float,
    stable: bool,
    backward: bool,
    iterate_count: int,
    half_width: float,
    sample_count: int,
) -> list[tuple[float, State, tuple[str, ...]]]:
    result = []
    for scalar in np.linspace(-half_width, half_width, sample_count):
        try:
            start = perturb(base, float(scalar), slope, stable=stable)
            finish, word = iterate(start, iterate_count, backward=backward)
        except (RuntimeError, ValueError, OverflowError):
            continue
        result.append((float(scalar), finish, word))
    return result


def unwrap_pair(left: float, right: float) -> tuple[float, float]:
    delta = wrap_angle(right - left)
    return left, left + delta


def segment_intersection(a0, a1, b0, b1):
    matrix = np.column_stack((a1 - a0, -(b1 - b0)))
    determinant = float(np.linalg.det(matrix))
    if abs(determinant) < 1.0e-13:
        return None
    rhs = b0 - a0
    parameters = np.linalg.solve(matrix, rhs)
    if -1.0e-12 <= parameters[0] <= 1.0 + 1.0e-12 and -1.0e-12 <= parameters[1] <= 1.0 + 1.0e-12:
        point = a0 + parameters[0] * (a1 - a0)
        return float(parameters[0]), float(parameters[1]), point, determinant
    return None


def contiguous_segments(samples):
    for left, right in zip(samples, samples[1:]):
        if left[2] != right[2] or left[1].kind != right[1].kind:
            continue
        theta_left, theta_right = unwrap_pair(left[1].theta, right[1].theta)
        if abs(theta_right - theta_left) > 0.25 or abs(right[1].p - left[1].p) > 0.25:
            continue
        yield left, right, np.array([theta_left, left[1].p]), np.array([theta_right, right[1].p])


def search(args) -> None:
    slope_a, slope_b = eigenslopes()
    qnl = State("G", QNL_THETA, 0.0)
    connector = State("G", CONNECTOR_THETA, 0.0)
    print(f"QNL eigen-slope={slope_a:.16g}")
    print(f"connector eigen-slope={slope_b:.16g}")
    unstable_curves = []
    for n_a in range(args.min_qnl_steps, args.max_qnl_steps + 1):
        unstable_curves.append(sample_curve(
            qnl,
            slope_a,
            stable=False,
            backward=False,
            iterate_count=n_a,
            half_width=args.qnl_width,
            sample_count=args.samples,
        ))
    stable_curves = []
    for m_b in range(args.min_connector_steps, args.max_connector_steps + 1):
        stable_curves.append(sample_curve(
                connector,
                slope_b,
                stable=True,
                backward=True,
                iterate_count=m_b,
                half_width=args.connector_width,
                sample_count=args.samples,
            ))

    total = 0
    for n_offset, unstable in enumerate(unstable_curves):
        n_a = args.min_qnl_steps + n_offset
        u_segments = list(contiguous_segments(unstable))
        for m_offset, stable in enumerate(stable_curves):
            m_b = args.min_connector_steps + m_offset
            s_segments = list(contiguous_segments(stable))
            for u_left, u_right, u0, u1 in u_segments:
                for s_left, s_right, s0, s1 in s_segments:
                    if u_left[1].kind != s_left[1].kind:
                        continue
                    # Put the second segment in the same angle lift as the first.
                    shift = round((u0[0] - s0[0]) / (2.0 * math.pi)) * 2.0 * math.pi
                    s0_shifted = s0.copy()
                    s1_shifted = s1.copy()
                    s0_shifted[0] += shift
                    s1_shifted[0] += shift
                    hit = segment_intersection(u0, u1, s0_shifted, s1_shifted)
                    if hit is None:
                        continue
                    alpha, beta, point, determinant = hit
                    scalar_u = u_left[0] + alpha * (u_right[0] - u_left[0])
                    scalar_s = s_left[0] + beta * (s_right[0] - s_left[0])
                    print("CANDIDATE (binary64 only; not certified)")
                    print(f"  forward_qnl_steps={n_a}, reverse_connector_steps={m_b}")
                    print(f"  section={u_left[1].kind}, point_theta_p=({point[0]:.17g},{point[1]:.17g})")
                    print(f"  qnl_local_scalar={scalar_u:.17g}")
                    print(f"  connector_local_scalar={scalar_s:.17g}")
                    print(f"  polyline_transversality_det={determinant:.9e}")
                    print(f"  qnl_word={''.join(u_left[2])}")
                    print(f"  reverse_connector_word={''.join(s_left[2])}")
                    _, qnl_trace = trace_iterate(
                        perturb(qnl, scalar_u, slope_a, stable=False), n_a, backward=False
                    )
                    _, connector_trace = trace_iterate(
                        perturb(connector, scalar_s, slope_b, stable=True), m_b, backward=True
                    )
                    print(f"  qnl_lift_trace={qnl_trace}")
                    print(f"  reverse_connector_lift_trace={connector_trace}")
                    total += 1
                    if total >= args.max_results:
                        return
    if total == 0:
        print("no binary64 candidate found in declared search window")
    else:
        print(f"binary64_candidates_reported={total}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-qnl-steps", type=int, default=0)
    parser.add_argument("--max-qnl-steps", type=int, default=20)
    parser.add_argument("--min-connector-steps", type=int, default=0)
    parser.add_argument("--max-connector-steps", type=int, default=20)
    parser.add_argument("--qnl-width", type=float, default=1.0e-8)
    parser.add_argument("--connector-width", type=float, default=1.0e-12)
    parser.add_argument("--samples", type=int, default=401)
    parser.add_argument("--max-results", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    verify_periodic_words()
    search(args)


if __name__ == "__main__":
    main()
