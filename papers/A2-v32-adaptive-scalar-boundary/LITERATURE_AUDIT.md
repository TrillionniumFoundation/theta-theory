# A2 v32 literature audit — active binary boundary estimation

Primary sources were checked on 4 October 2026. This is a focused comparison requested by the v31 report, not an exhaustive priority search. The new lower-bound proof is self-contained and does not import a classification theorem with a different loss.

## Castro and Nowak

R. M. Castro and R. D. Nowak, *Minimax Bounds for Active Learning*, IEEE Transactions on Information Theory 54(5) (2008), 2339–2353; DOI 10.1109/TIT.2008.920189.

Author-hosted journal draft, 5 November 2007: https://rmcastro.win.tue.nl/publications/castro_IT_minimax.pdf

The formulation in Section II specifies an adaptive feature query and a binary class label, with risk measured by excess classification error. Boundary-fragment smoothness and regression-noise conditions determine the rates. Our collision bit does not directly label membership; the new local reduction provides that information at an explicitly charged cost. Our target is C2 geometry and primitive periodic recognition, with known smoothness and calibration, not their excess-risk problem. No exponent is transplanted between these losses.

The authors' correction to Theorem 3 of the COLT 2007 version was also checked: https://rmcastro.win.tue.nl/publications/errata.pdf . It identifies excess generality of that statement and supplies a corrected lower-bound formulation. Our elementary binary-leaf proof does not depend on that statement. The existence of an erratum is not treated as invalidating their research program.

## Locatelli, Carpentier and Kpotufe

A. Locatelli, A. Carpentier and S. Kpotufe, *An Adaptive Strategy for Active Learning with Smooth Decision Boundary*, PMLR 83 (ALT 2018), 547–571.

Official proceedings page: https://proceedings.mlr.press/v83/locatelli18a.html
Official primary PDF: https://proceedings.mlr.press/v83/locatelli18a/locatelli18a.pdf

Sections 2–3 define the membership-query classification model, smooth boundary fragment and noise assumptions. The line-search/interpolation strategy and adaptation to unknown smoothness/noise are the relevant comparison. Our adaptive choices concern spatial positions with known s; no adaptation-to-unknown-smoothness claim is made. The point of comparison is the observation reduction and C2 physical loss, not a claim that line search or polynomial interpolation is new.

## Classical inverse and geometric mechanisms

Lawler–Limic's *Random Walk: A Modern Introduction* (2010), retained in v31, is credited for stopped martingales and killed Green methods. The new proof supplies its bounded-stop calculation directly. The v31 references and theorem-level active-probing, hit-functional and periodic-recognition comparisons are retained unchanged in Supplement R. The manuscript does not claim to establish a new abstract potential-theory, dynamic-programming, entropy or interpolation principle.

Each comparison in the primary is limited to the stated information model, smoothness assumptions, loss and scope. No publication acceptance, exhaustive novelty search or equivalence to passive billiard spectra is inferred.
