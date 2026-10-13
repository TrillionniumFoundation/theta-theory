# A2-DYN, revision 60

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. It retains the original Lorentz record and all previous mathematics. It responds to the frozen v59 report at `546a82be685897355e4918598f2d06847aa9f69c`.

The new proof route is `core/128_positive_coarea_criterion.tex`, `core/129_perturbed_markov_density.tex`, and `core/130_perturbed_heights_and_contact.tex`. It gives an exact-label positive coarea criterion, a parameter-uniform perturbed Markov roof density, three positive source heights, and a critical endpoint profile whose damping equals that of the moving pressure peak. The unweighted normalized density error is `C log(2+m)^(3/2)/sqrt(m)`. Weighted endpoints retain an explicit arithmetic profile.

All 127 inherited core files and 171 inherited Python files are unchanged. All old compiled appendices and labels remain. The complete Lorentz pointwise incidence and clearance heights are not claimed by the Markov application. See `RESPONSE_TO_REFEREE.md` for the exact item-by-item status.

Build from a checkout with `bash papers/A2-DYN-v60-referee-response/build.sh`. The workflow qualifies the exact ordinary source tree, frozen report, normal/optimized finite checks and native typesetting. Dynamic receipts, not advance claims in prose, identify the run SHA and PDF hash. This is not a formal proof certificate or an independent human review.
