#!/usr/bin/env python3
"""Arb certificate for the common center-cocycle cone subgate.

This imports, but does not modify, the frozen v52 period-eight certificate.
It proves a necessary center-derivative statement only.  It does not certify
full-cross strips, a Markov rectangle, or singularity margins on a strip.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


FROZEN_CERT = Path(__file__).with_name(
    "cm2_fixed_section_common_vertex_cert.py"
)


def load_frozen_certificate():
    spec = importlib.util.spec_from_file_location("cm2_v52_common_vertex", FROZEN_CERT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen certificate {FROZEN_CERT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def certify_positive_cone(module, name, matrix, expansion_threshold):
    arb = module.arb
    lower_slope = arb(13) / 2
    upper_slope = arb(7)

    if not matrix.det() > arb(999) / 1000:
        raise RuntimeError(f"{name}: determinant is not positive with margin")

    lower_margins = (
        matrix[1, 0] - lower_slope * matrix[0, 0],
        matrix[1, 1] - lower_slope * matrix[0, 1],
    )
    upper_margins = (
        upper_slope * matrix[0, 0] - matrix[1, 0],
        upper_slope * matrix[0, 1] - matrix[1, 1],
    )
    if not all(margin > 0 for margin in lower_margins + upper_margins):
        raise RuntimeError(f"{name}: positive cone is not mapped into [13/2,7]")

    inverse_lower_margins = (
        matrix[1, 0] - lower_slope * matrix[1, 1],
        matrix[0, 0] - lower_slope * matrix[0, 1],
    )
    inverse_upper_margins = (
        upper_slope * matrix[1, 1] - matrix[1, 0],
        upper_slope * matrix[0, 1] - matrix[0, 0],
    )
    if not all(
        margin > 0 for margin in inverse_lower_margins + inverse_upper_margins
    ):
        raise RuntimeError(
            f"{name}: inverse negative cone is not mapped into [-7,-13/2]"
        )

    forward_column_sums = (
        matrix[0, 0] + matrix[1, 0],
        matrix[0, 1] + matrix[1, 1],
    )
    if not all(value > expansion_threshold for value in forward_column_sums):
        raise RuntimeError(f"{name}: forward l1 expansion threshold fails")

    determinant = matrix.det()
    inverse_absolute_column_sums = (
        (matrix[1, 1] + matrix[1, 0]) / determinant,
        (matrix[0, 1] + matrix[0, 0]) / determinant,
    )
    if not all(
        value > expansion_threshold for value in inverse_absolute_column_sums
    ):
        raise RuntimeError(f"{name}: inverse stable-cone expansion threshold fails")

    print(f"{name}_CENTER_CONES: CERTIFIED")
    print("  C_plus={(x,y): x>0, y>0}")
    print("  M(C_plus) subset {(x,y): x>0, 13/2<y/x<7}")
    print("  C_minus={(x,y): x>0, y<0}")
    print("  M^{-1}(C_minus) subset {(x,y): x>0, -7<y/x<-13/2}")
    print(f"  forward_lower_slope_margins={lower_margins}")
    print(f"  forward_upper_slope_margins={upper_margins}")
    print(f"  inverse_lower_slope_margins={inverse_lower_margins}")
    print(f"  inverse_upper_slope_margins={inverse_upper_margins}")
    print(f"  forward_l1_column_sums={forward_column_sums}")
    print(f"  inverse_l1_column_sums={inverse_absolute_column_sums}")


def main():
    module = load_frozen_certificate()
    root = module.certify_orbit_root()
    matrix_b, angle_residual, momentum_residual = module.connector_derivative(
        root.boxes[0]
    )
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("period-eight center residual does not contain zero")

    sqrt_two = module.arb(2).sqrt()
    alpha = (module.arb(661) - 325 * sqrt_two) / 36
    beta = (module.arb(859) - 550 * sqrt_two) / 100
    gamma = module.arb(625) * (25 - 4 * sqrt_two) / 324
    matrix_a = module.arb_mat([[alpha, beta], [gamma, alpha]])

    certify_positive_cone(module, "QNL_PERIOD2", matrix_a, module.arb(6))
    certify_positive_cone(module, "CONNECTOR_PERIOD8", matrix_b, module.arb(6))
    print("COMMON_CENTER_CONE: CERTIFIED")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  missing=full-cross strips and strip-uniform singularity/cone margins")


if __name__ == "__main__":
    main()
