# A2-DYN revision 59

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision begins from the latest v58 review at `94c9ef54bd84d9eb04fbd3b4d3431776beab64de`, whose reviewed author source is `b9c8e1f15b65e4843d1321f23ed5b816378b855c`. It does not restart from the older v36 branch scaffolds.

All 124 inherited core modules and all 167 inherited Python scripts remain byte-identical. All inherited mathematical labels and compiled appendices remain. Three modules are added: physical root-taking and accretive Gaussian details; a correlated Markov-baker realization with a continuous roof; and a direct pointwise density/coarea theorem including positive boundary heights in that model. The original four-coordinate Lorentz record, signed arithmetic coefficient, graph coupling, exact source and pointwise target are unchanged.

The Markov roof theorem is a true essential-supremum estimate, at rate `log(2+m)/sqrt(m)`, derived from exact stable coarea and finite-cylinder bounds. Its perturbed pressure branch has damping `12*pi^2*epsilon^2/119+O(epsilon^3)` and centered drift `-3456*pi^2*epsilon^2/99127+O(epsilon^3)`. The density theorem is stated at epsilon zero; no uniform perturbed-roof density theorem is asserted. These results do not supply the two still-missing Lorentz incidence/clearance heights.

`RESPONSE_TO_REFEREE.md` maps the latest report items to the new proofs and states the unresolved obligations without changing their scope. `JOURNAL_ROUTE.md` gives a short referee reading route. Run `bash papers/A2-DYN-v59-referee-response/build.sh` on the exact source checkout. The read-only qualification workflow binds the source, finite checks, native PDF and rendered proof pages to the event SHA. Successful typesetting is not mathematical certification.
