# A2-DYN, revision 18

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The immediate author baseline is revision 17 at `253f7c56de1f198ff9bd5e13fa2009baf4551495`. The latest located referee report is the substantive v16 report at `b0b7ddfcd90f493e02254742b33174e9108fc5a7`, blob `805f04cd60d144bc6321ce3f4304ebe1cda34999`. The current revision continues that response; it does not invent a separate review of v17.

## New theorem and its place in the original problem

Theorem I establishes complete raw edge extraction for every finite physical-count restriction of the actual return law. Integrating the whole finite collision graph gives constructible time densities, including all critical and singular itinerary boundary effects. Convergent one-sided rational-power/logarithm germs are extracted through exponent one. The exact residual belongs to `W^{2,1}` in each of finitely many lattice components. Its Fourier transform is integrable, with an explicit far-roof bound in terms of the actual summed second-derivative norm.

The observed collision count makes a linear count restriction exact on the original central window. The new inversion identity uses that support property, with a rapidly decaying high-count convolution correction. It is an identity for the unmodified raw law, not an LLT for a smoothed or conditioned substitute. The scalar physical kernel cutoff is `2 n^(-99/200)`, or `2 n^(1/200)` in rescaled frequency.

The existence of the finite extraction is now proved. Quantitative control of its norms as the return count grows, uniform control of the local edge correction, the complete complementary integral, and the exact weighted-event comparison remain separate estimates. The article retains their full original endpoint.

## Files

`core/40_finite_count_edge_extraction.tex` proves the density structure, complete power-log extraction, trace cancellation and Fourier bounds. `core/41_count_localized_raw_inversion.tex` proves exact support agreement, the central inversion identity and the resulting raw error budget. `RAW_EXTRACTION_INPUT_MAP.md` identifies the added Cluckers--Miller input and its precise scope. `RESPONSE_TO_REFEREE.md` answers the controlling report item by item.

All 39 inherited core files and all 28 inherited Python files are byte-identical. All 459 inherited mathematical labels and all 14 old bibliography entries remain. Six exact introduction/bibliography edits are replayed from `INHERITED_EDITS.json`; no inherited theorem is deleted.

Run `bash papers/A2-DYN-v18-referee-response/build.sh` in a checkout. The read-only qualification workflow checks the event source, executes normal and optimized finite diagnostics, and typesets the full article. Its dynamic receipt identifies the exact SHA, run, and PDF hash. These checks are not continuum proof certification or journal acceptance.
