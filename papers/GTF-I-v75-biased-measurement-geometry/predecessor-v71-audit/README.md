# General Theta Foundations I — Revision 71

## Manuscripts and new results

**Quantitative:** *Input-Dependent Boundary Coding and the Full Error Range* (`quantitative.tex`, `paper.pdf`).

**Structural:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* (`structural.tex`, `STRUCTURAL_PAPER.pdf`).

**Complete research edition:** `main.tex`, `COMPLETE_REVISION.pdf`. All v70 active mathematical labels remain typeset; no predecessor path is overwritten.

For the fixed-readout family Phi_sigma,y(X)=sum_x <e_x,X e_x> sigma_xy, each input row has total trace one. With fixed public conditional output-rank bounds r_xy, put V=sum_x(sum_y r_xy(2n-r_xy)-1). The new theorem proves

    log2 M_N(delta) = (V/2) log2 N + V log2(1/delta) + O(1)

for N>=1 and every 0<delta<=delta_*<2, with fixed dimensions, ranks and cap. The metric is the unhalved final-state trace distance over common bounded adaptive quantum testers, including references, memory, feedback and stopping. Outcomes can depend on the input. No positive eigenvalue margin is required. The measured input basis is fixed; this is not a classification of all disturbing instruments.

An idempotent-input retraction shows that arbitrary legal memoryless centres give the same covering number as fixed-readout centres, at every radius. Centre ranks may increase under retraction. The separate rational upper code does preserve zero conditional blocks and never increases conditional ranks.

A common estimator with an explicit mean-square bound, followed by a bound on covering-centre multiplicity, extends the inherited general positive-margin and preparation-family laws to the whole fixed submaximal error range. It avoids the invalid inference that one centre can cover only one packing point at error greater than one. Constants need not remain bounded as delta_* approaches two. The coherent/preparation mixed law remains inherited with its own delta<=1/32 range.

## Exact reference implementation

    python conditional_codec.py encode --input inputs/conditional-boundary.json --horizon 100 --error 1/1000 --ranks '[[1,1,0],[0,1,2]]' > code.json
    python conditional_codec.py decode --input code.json > decoded.json
    python conditional_codec.py verify --input inputs/conditional-boundary.json --certificate code.json
    python conditional_codec.py retract --input decoded.json
    python check_conditional.py

The encoder is given rational Choi data. It rejects off-diagonal input coherences rather than silently deleting them, applies the inherited factor codec separately to the input rows, and joins rational decoded blocks with an exact marginal. Expanded storage and encoder workspace are not the compressed payload. A decoded quantum operation is not a physical classical simulation on unknown entangled inputs. Bare decode checks legality; verification binds the certificate to its supplied target by canonical replay.

## Reproduction and ancestry

    python build_revision.py --isolated

The build executes the new exact regression and all seven inherited suites in ordinary and optimized modes, retains prior labels, compiles all three manuscripts, and reconstructs the native archive in an empty directory. The minimal journal package rebuilds without historical PDFs. Actual receipts and page counts, not this README, record completed tests and builds.

Base: completed v70 exact head `a5cd3bb0ea9c29f680381230c603e54354866376`. Controlling reports remain v68/r45 at `e862e5c963ef36b9caa3b1b814b495ae4428a088` and `a3fd5b80549a855c46151fd7183b3fc7139abac7`; no v70-specific report was found in the opening survey. V69 is only a continuation anchor. V70's coherent-boundary theorem and literature corrections are inherited, not advertised as new here.

Work branch: `revision/general-theta-foundations-i-v71-input-dependent-boundary-2026-10-03`.
Referee branch, after exact-head reconstruction: `revision/general-theta-foundations-i-v71-referee-ready-2026-10-03`.

The response addresses all 14 required and 24 detailed r45 comments. The mathematical journal objective is unchanged. Neither finite regression nor CI claims independent priority clearance, authorship signatures, acceptance, universal formal verification or A/B/C/D analytic closure.
