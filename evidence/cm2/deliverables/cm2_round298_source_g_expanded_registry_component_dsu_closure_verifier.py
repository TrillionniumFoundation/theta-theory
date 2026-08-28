#!/usr/bin/env python3
"""Independent fail-closed bootstrap for Round298 verification.

The final verifier must rebuild all 564,492 assignments and every accepted
edge channel without importing or executing the producer.  The previously
computed 140,836 components and 379,168 ordered edge applications are only the
ordinary-plus-true-seam prefix, not final Round298 counts.  Until both pending
upstream package digests are sealed and lower-stratum physical incidence is
proved to imply component connectivity, this module refuses to inspect a
Round298 candidate.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
R295C_MANIFEST = (
    "cm2_round295c_source_g_all_stratum_scope_composition_closure_"
    "manifest.sha256"
)
R296_MANIFEST = (
    "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
    "manifest.sha256"
)
R297_MANIFEST = (
    "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
    "manifest.sha256"
)

PACKAGE_MANIFEST_PINS = {
    R295C_MANIFEST:
        "a9499856148480b9ddd5b0dd9ea8de28b989b592477c9a3b7ea43541772180c1",
    R296_MANIFEST:
        "f7786b9cdec45cb381ec46489eb44b0365b8ee43d81ae9a9611cb2dcdee7fb59",
    R297_MANIFEST:
        "1feecefa897c5320eadc006509ba6bde84cdbf692dfaddd024472b93c13c38c0",
}

SEALED_PREFIX_EXPECTED = {
    "member_assignment_row_count": 564_492,
    "ordinary_plus_true_seam_prefix_component_count": 140_836,
    "ordinary_plus_true_seam_prefix_edge_application_count": 379_168,
    "ordinary_plus_true_seam_prefix_rank_reducing_edge_count": 227_128,
    "ordinary_plus_true_seam_prefix_redundant_edge_count": 152_040,
    "inherited_Round266_rank_reduction": 196_528,
    "ordinary_plus_true_seam_prefix_cumulative_rank_reduction": 423_656,
}

LOWER_STRATUM_CHANNEL_STATUS = (
    "PENDING_FAIL_CLOSED__PHYSICAL_INCIDENCE_IS_NOT_YET_PROVED_"
    "COMPONENT_CONNECTIVITY"
)
FINAL_EDGE_APPLICATION_COUNT = None
FINAL_RANK_REDUCTION = None
FINAL_COMPONENT_COUNT = None

PIN_RE = re.compile(r"^[0-9a-f]{64}$")


class VerificationError(RuntimeError):
    """Fail-closed independent Round298 verification error."""


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def verify_manifest_boundary() -> None:
    for filename, expected in PACKAGE_MANIFEST_PINS.items():
        if PIN_RE.fullmatch(expected) is None:
            raise VerificationError(
                "UNSEALED_PACKAGE_MANIFEST_PIN:" + filename
            )
        path = HERE / filename
        if (
            path.parent != HERE
            or not path.is_file()
            or path.is_symlink()
            or file_sha256(path) != expected
        ):
            raise VerificationError(
                "PACKAGE_MANIFEST_PIN_MISMATCH:" + filename
            )
    if LOWER_STRATUM_CHANNEL_STATUS.startswith("PENDING_"):
        raise VerificationError(LOWER_STRATUM_CHANNEL_STATUS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=298_101)
    parser.parse_args()
    verify_manifest_boundary()
    raise VerificationError("ROUND298_INDEPENDENT_RECONSTRUCTION_NOT_INSTALLED")


if __name__ == "__main__":
    main()
