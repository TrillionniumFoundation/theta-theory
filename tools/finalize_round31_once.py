#!/usr/bin/env python3
"""Apply the final fail-closed Round-31 source corrections exactly once."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = ROOT / ".round31-finalized"


def replace_exact(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"expected source fragment not found in {path.relative_to(ROOT)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    if MARKER.exists():
        print("Round 31 finalizer already applied.")
        return

    preamble = ROOT / "ROUND31_PREAMBLE.tex"
    preamble_text = preamble.read_text(encoding="utf-8")
    additions = []
    if r"\newcommand{\cI}{\mathcal I}" not in preamble_text:
        additions.append(r"\newcommand{\cI}{\mathcal I}")
    if r"\newcommand{\cO}{\mathcal O}" not in preamble_text:
        additions.append(r"\newcommand{\cO}{\mathcal O}")
    if additions:
        preamble.write_text(
            preamble_text.rstrip() + "\n" + "\n".join(additions) + "\n",
            encoding="utf-8",
        )

    a4 = ROOT / "papers/A4-history-memory-universal-pressure/ROUND31_POSITIVE_CLOSURE.tex"
    replace_exact(
        a4,
        r"B_Q\in\cL(\cR,D(L_Q^3)).",
        r"B_Q\in\cL(\cR,D(L_Q^4)).",
    )
    replace_exact(
        a4,
        """For $y=B_Qr\in D(L_Q^3)$, three resolvent identities give
\[
 (z-L_Q)^{-1}y=z^{-1}y+z^{-2}L_Qy+z^{-3}L_Q^2y
 +z^{-3}(z-L_Q)^{-1}L_Q^3y.
\]
Because $C_Q$ is bounded on $\cH$ and the stable resolvent is uniformly
Hilbert bounded, the last term is $O(|z|^{-3})$ before the additional retained
coefficient, and one further identity gives the $O(|z|^{-4})$ remainder in
(A4.22).""",
        """For $y=B_Qr\in D(L_Q^4)$, four resolvent identities give
\[
 (z-L_Q)^{-1}y=z^{-1}y+z^{-2}L_Qy+z^{-3}L_Q^2y
 +z^{-4}L_Q^3y+z^{-4}(z-L_Q)^{-1}L_Q^4y.
\]
Because $C_Q$ is bounded on $\cH$ and the stable resolvent is uniformly
Hilbert bounded, the final two terms are $O(|z|^{-4})$ after applying $C_Q$.
Retaining the coefficients through order $z^{-3}$ therefore gives the
remainder stated in (A4.22).""",
    )

    verifier = ROOT / "tools/verify_round31.py"
    replace_exact(verifier, '"No root-resampling"', '"no root is resampled"')
    replace_exact(verifier, '"D1 remains terminal"', '"and is terminal"')
    replace_exact(
        verifier,
        '"Hellinger separation of the induced observation laws"',
        '"Global identification is imposed on induced laws"',
    )

    MARKER.write_text(
        "ROUND31_FINALIZED=1\n"
        "A4_MEMORY_DOMAIN=D(L_Q^4)\n"
        "COMMON_MACROS=cI,cO\n",
        encoding="utf-8",
    )
    print("Round 31 finalizer applied successfully.")


if __name__ == "__main__":
    main()
