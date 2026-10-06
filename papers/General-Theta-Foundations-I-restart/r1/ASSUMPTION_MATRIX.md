# Experiment-level assumption matrix

| Certificate | General theorem requires | Binary filter verification | Singular sensor verification |
|---|---|---|---|
| Preparation/kernels | normalized nonnegative Borel kernels, genuine costs | flip transition, density (1+a(2x-1)y)/2 | prepared box mixture, failure/success coin, absorbing hold |
| Executable tests | determining future tests, legal terminal probes | future filter words + terminal hidden bit | future attempts + terminal flag/Bernoulli coordinate probes |
| Quotient Q | compact realization or explicit compatible versions proved from tests | posterior p; denominator >=1-a_+ | unresolved point plus glued absorbed Z; latent mark eliminated |
| Fixed exploration | chosen before encoder; no free optimal control | constant command gives controller D=1; bounds also for declared rules | single attempt action, controller D=1 |
| Actual mass G | raw conditional densities bounded relative to chart volume | derivative dF/dy bounded below, then mixture of actual densities | success mass 1-(1-s)^N and original conditional uniform charts |
| Global valid cover | whole valid envelope, not only a local patch | one invariant interval | union of all physical chart images plus unresolved point |
| Predictive separation | score lower bound on each chart | scalar p is exact probe mean | physical z maps, flag distinguishes unresolved mode |
| Intersections | separated all budgets; intersections m>=2J | single component | mixed line/rectangle/atom, no separation required above threshold |
| Update I | pathwise error insertion recorded only when executed | rho=1-2q_0 on every update | A=1,B=0 on holds; A=0,B_j=1 on reveal |
| Weighted moment T | E(sum Z_j r_j)^2 <= Gamma sum w_j r_j^2 | Gamma <=(2q_0)^-2 | Gamma=1 exactly by disjoint indicators |
| Report continuity C | actual report/terminal-kernel TV Lipschitz on valid interfaces | TV=a rho |p-p'|/2; terminal TV=|p-p'| | absorbed attempt laws identical; mode separated by flag; Bernoulli probes Lipschitz |
| Effective computation | finite descriptions, precision inputs, certified allocation | rational grids/updates, interval arithmetic | algebraic width/weight allocation, approximated physical-distance comparisons |
| Calibration | paid pilot or deterministic certificate, no oracle learning | known calibration; perturbations enter u and zeta | known acquisition/map calibration; successful input error enters once |
| Uniformity | constants independent only of stated variables | N,m, fixed command rule; not q_0->0 | N,s,widths,intersections; fixed finite chart constants |

The raw kernel does not automatically imply these certificates for every possible
experiment. Each additional model must supply the missing proof, not relabel a
formal parameter domain as an acquired chart.
