# Response to the R10 external referee report

Report fixed at `6f3ca64beec4b054dba8cb5def1a6c69fbc46d52`, report blob `3b60c8fd6bd915dc8585c029478e83180f18a67e`. We thank the referee for identifying overlapping-noise adaptive sensing as the central remaining mathematical challenge rather than requesting another separated digit example.

## Main mathematical response

The new article develops causal posterior pooling. Its controller stores only a phase-labelled cell and a read-only posterior barycenter computed under that controller's actual law. It selects the full Bellman-optimal action at that true conditional belief. The excess risk is exactly an acquired Jensen sum. A proved integrated curvature bound handles nonsmooth concave values, including action switches. Uniform actual posterior smoothing supplies a hard memory converse for *every* full-history policy. Thus overlapping-noise adaptive acquisition and finite-state prediction now have matching exponents at every fixed horizon, with the explicit complete-state upper and its n dependence preserved.

Raw positive finite-state sensor kernels verify the hypothesis. In two states, a genuinely noisy first reading determines which asymmetric sensor is best next; a strict advantage over all fixed two-sensor schedules is proved. A physical validation channel gives atomic/continuous acquired rank changes and verifies the stratified extension.

This addresses the requested noisy adaptive direction, but does not assert a universal intrinsic classification or horizon-uniform joint matching. Such a claim would exceed the proof. The old stronger horizon-uniform separated theorem remains complete and unchanged in Supplement T.

## Major issues 13.1–13.8

| Issue | Revision / proof location |
|---|---|
| Active-sensing and decision-tree comparison | New Section 6 compares objective, policy, noise, stopping, total state and planning against all five requested routes; corrected adaptive-submodularity version used |
| Strong separation structural | Introduction separates support gaps from informative noise. Positive-noise sensor realizes completion with overlapping hidden support after every finite report |
| Natural noisy adaptive application | General pooling theorem plus raw finite-state controlled sensor theorem and strict two-call switching proposition inside its proof; not another Cantor digit example |
| Randomized-policy reduction | Standalone lem:seeds with fixed-policy projection first and explicit autonomous-purification warning |
| Programme vs state | Main theorem and resource section explicitly allow abstract known real/Borel constants; prop:digitalpool gives separately certified finite execution |
| Planning existence vs complexity | Visible adjacent to theorem; no polynomial synthesis assertion; gamma comparison error charged separately |
| Duplicate native/supplement text | Fresh concentrated native article; complete old R10 supplied as integral T rather than reprinted among the new arguments. Complete S retained |
| Title/umbrella | Original title retained; General Theta defined as the experiment-to-risk programme on declared classes, not universal regularity |

## Technical comments 1–32

Comments 1,4–11,13–19 concern the preserved separated-refinement and graph-directed proof. Those proofs are not deleted or re-stated with different quantifiers: Supplement T retains positive branches, essential carriers, deterministic tie choices, filtered depth pruning, total 2m-1 states, one doubling, known calibration kernels and compulsory early-channel order. The new native proof avoids dependence on that tree mechanism. Fixed/stated adaptive comparisons now appear adjacently for the new noisy sensors. Safe channel status counts remain explicitly nonminimal.

Comments 2,3,12: deterministic checkpoint convention, fixed-policy projection, measurable least-index ties, and the independent-seed reduction are in Section 1. Time-indexed randomized autonomous policies are not purified without accounting for their tape.

Comments 20,21: Section 5 separates comparison, coefficient/report/arithmetic and output precisions. It distinguishes planning/integration from sequential execution and charges tables/scratch. Programmes can be large.

Comments 22–30: the complete continuation, conditional-cut, rank, filtering, stopped and morphism text remains in T/S with its original assumptions. The new quotient appendix repeats the task-state/full-experiment distinction; new morphism statement identifies the exact target and reverse source strategy classes and includes actions, reports, costs and audit. No lower-bound side information is a free upper register.

Comments 31,32: all build/regression/provenance claims remain outside mathematical novelty arguments. Ledgers and receipts are repository evidence only.

## Assessment requested next

The next external review should scrutinize the integrated Jensen lemma, all-incoming posterior calibration, the optimal-action telescope, last-action-uniform density lower, total phase state count and finite precision first-mismatch proof. It should assess the significance and priority of that combination independently. We do not claim that the prior top-four recommendation has already changed or that every proposed major direction is now closed.
