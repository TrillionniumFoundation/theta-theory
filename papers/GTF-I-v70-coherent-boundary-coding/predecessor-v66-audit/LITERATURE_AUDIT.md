# Primary-source comparison — Revision 66

Checked 29 September 2026. This is an author-side comparison, not independent priority clearance. Exact predecessor comparisons, including theorem numbers for automata, positive realization, spectral inputs and the earlier entropy chain, remain in `predecessor-v65-audit/LITERATURE_AUDIT.md` and the older preserved audit directories.

## Quantum trajectories and filtering

**P. Rouchon and J. F. Ralph, Efficient Quantum Filtering for Quantum Feedback Control, Physical Review A 91 (2015), 012118.** Primary version: arXiv:1410.5345v2, 6 January 2015, https://arxiv.org/html/1410.5345v2. DOI: 10.1103/PhysRevA.91.012118.

Section II, especially equations (10)–(13), gives normalized positive updates for diffusive stochastic-master-equation filtering and measurement-based feedback. This is a close antecedent for positivity-preserving numerical trajectories. The present integer precision budget concerns discrete instrument calls, exact rational branch masses and subnormalized full-history error; it does not replace their time-discretization analysis or claim priority for positive quantum filtering as a general idea.

## Choi correction and projected process estimation

**T. Surawy-Stepney, J. Kahn, R. Kueng and M. Guţă, Projected Least-Squares Quantum Process Tomography, Quantum 6 (2022), 844.** Primary version: arXiv:2107.01060v2, 18 October 2022, https://arxiv.org/html/2107.01060v2. DOI: 10.22331/q-2022-10-20-844.

Section 4, equation (15), explicitly mixes a nearly positive TP estimate with the maximally mixed Choi state to preserve the partial trace while repairing positivity. Section 13 supplies CP/TP projection formulas; Theorem 1 concerns statistical error bounds. Identity mixing after TP correction is therefore not claimed as a new principle here. Their Choi normalization has trace one, whereas ours is input-first and unnormalized. The new theorem specifies a direct integer grid correction with an explicit common denominator and deterministic diamond bound from certified coordinate errors. It is not a nearest-point projection, a rank-optimal estimator, or a statistical sample-complexity theorem.

## Complete norms and adaptive networks

**J. Watrous, The Theory of Quantum Information, Cambridge University Press, 2018.** Primary author chapters: https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf and https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf.

Theorems 2.22 and 2.26 give the Choi positivity and partial-trace criteria. Section 3.3, printed page 179, equation (3.306), states additive accumulation of completely bounded trace-norm errors in channel networks, derived from Proposition 3.48 and Corollary 3.47. These are classical premises; the new manuscript supplies a direct proof for its tensor convention and stopped classical command port. The dimension-independent reference guarantee does not imply a classical physical realization on unknown quantum input.

**G. Gutoski, On a measure of distance for quantum strategies, Journal of Mathematical Physics 53 (2012), 032202.** Primary version: arXiv:1008.4636v4, 14 March 2012, https://arxiv.org/html/1008.4636v4. DOI: 10.1063/1.3693621.

The operational strategy norm and Theorem 3's unit-ball/duality characterization provide the proper neighboring language for arbitrary interactive quantum testers. We do not introduce a new strategy norm or claim that the hybrid comparison is new. Our finite-description result concerns rational instrument blocks whose replacement error is uniform for every common tester and bounded public stopping rule.

## Version-sensitive automata comparison retained

The current arXiv histories were rechecked: the April Chen–Wu paper is **arXiv:2604.07058v2**, 27 August 2026, *The State Cost of Classical Simulation of One-Way General Quantum Finite Automata*; the May paper is **arXiv:2605.10682v1**, 11 May 2026, *On the Simulation Cost of Quantum Finite Automata*. Primary version URLs are https://arxiv.org/html/2604.07058v2 and https://arxiv.org/html/2605.10682v1.

The predecessor comparison retains Definition 2.1, Theorem 3.2, Theorem 4.4 and Corollary 4.5 for the April strict-cutpoint model, and Theorems 11 and 14 with Corollary 15 for the May models. Section 35 retains the elementary attenuation and effect-margin separator. No calibrated numerical or whole-history claim is attributed to a sign-preserving language theorem. Neither the new compiler nor the earlier matrix-space lower bound is advertised as solving the distinct strict-cutpoint cost question.

## What this comparison establishes

The exact integer formula, variable-description recurrence, and their stated operational interfaces have written proofs and reference code. Their ingredients include classical Choi criteria, identity buffering, rational matrix arithmetic, rejection sampling, trace-norm contraction, hybrid comparison and a posterior normalization inequality. The paper does not claim those general ingredients as inventions. It also does not claim absence of equivalent formulations across all numerical trajectory, filtering, automata, positive-realization or streaming literature.

A further independent expert assessment of theorem-level priority was requested in r42. No independent human report has been obtained or fabricated during this revision. Preserved external r42 reports assess v65 only, not the newly written v66 results. Compilation, regression, source attestation and author-side literature comparison remain separate evidence classes.
