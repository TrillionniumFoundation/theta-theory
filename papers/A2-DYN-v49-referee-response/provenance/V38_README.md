# A2-DYN, revision 38

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Active source: `main.tex`. The controlling external report is v37 at `08562f799dd967056c81324c55ddcd9b91d79c14`; the exact author baseline is `d039c92d9f957ee180b74c0f3cf4c8bf52b9547c`.

## New theorem-bearing revision

Modules `80_four_dimensional_concentration.tex` and `81_return_resolution_and_complement.tex` prove a four-dimensional fixed-strip estimate, an all-target single-return concentration bound `C(1+|J|)m^(-2)`, and a local theorem for every diverging block of actual return indices. For `H -> infinity`, `H=o(sqrt(m))`, the original event has probability `c |J| H m^(-2) g_Omega(z,y) + o(Hm^(-2))`. The proof uses moving Fourier tests and a correct two-envelope lower bound, not weak convergence on fixed diffusive windows. A separate exact torus formula isolates the still-unproved single-index cancellation.

Theorem 4 is the synopsis. The probability upper bound concerns one index; the Gaussian asymptotic concerns a diverging block. Roof time is in a fixed unscaled interval, not a pointwise density. No polynomial convergence rate is asserted. The complete raw-return endpoint, pointwise correction and full complement remain the original research objective.

All 79 inherited core modules and 87 inherited Python scripts, the bibliography and the compiled A--X synopsis are unchanged. All inherited mathematical labels remain. `provenance/V37_main.tex` preserves the previous main file. No other paper directory is modified.

Build: `bash papers/A2-DYN-v38-referee-response/build.sh`. The v38 read-only workflow verifies the exact event source, runs normal/optimized finite checks, compiles the full article and renders proof pages. Its dynamic receipt binds the PDF to the event SHA and run. See `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, `SPECIALIST_AUDIT_MAP.md` and `VALIDATION.md`. No source build is an independent specialist proof certificate.
