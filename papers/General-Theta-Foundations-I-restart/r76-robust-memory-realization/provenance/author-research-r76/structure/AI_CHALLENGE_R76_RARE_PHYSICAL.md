# R76 author-team AI challenge: rare excursions and physical dictionaries

**Classification:** independent author-team AI proof challenge, performed by the
structural-mathematics agent. This is not an external referee report, human expert
review, formal proof verification, or editorial assessment. It supplies no
independent priority guarantee. The challenge examines the written mathematical
arguments and their quantifiers, not merely a finite numerical sample.

**Recorded:** 2026-10-21 13:27:27 UTC.

## Reviewed source identities

| Source | SHA256 |
| --- | --- |
| `conditional/46-rare-branch-approximation.tex` | `29eb545ff00792e776d872d49addd93f4bca633085ccbae76d139d451ec73780` |
| `conditional/47-physical-approximation-lower.tex` | `5a8ad91ae3e177bbe6d8587bec1ed8be7705358e050a8bccd51b058057d96fa5` |
| Inherited R75 `sections/44-noisy-instruments.tex` | `90e1c00160d5e62b6cc476e0176f03064185ba55e1145a838873494568e6f898` |

The first two paths are relative to `r76-research/`. The inherited path is
relative to `theta-r76-work/papers/General-Theta-Foundations-I-restart/`
`r75-nonabelian-stationary-memory/`. These are source-text bindings; this note
does not by itself assert a Git commit identity or a successful compilation.

## Conclusion

No mathematical gap was found in the three statements in file 46 or in the
physical-dictionary matching theorem in file 47, at the source hashes above.
The lower bound requires fixed density-matrix terminal decoders and fixed causal
report transition tables. The text states both restrictions explicitly.
The logarithmic leading constant is proved for each fixed positive budget and a
fixed phase with the supplied Diophantine separation constant. It is not a lower
bound for unrestricted classical decoder tables, nor for the separate original
algebraic phase without an additional Diophantine argument.

## Challenge of the sharp excursion bound

1. For `u(k)=(r^(-k)-1)/(1-r)`, direct subtraction gives
   `r*u(k+1)-u(k)=1`. Since `u(k+1)>=0`, replacing `r` by any conditional
   continuation probability `p<=r` only decreases this drift. Stopping before
   the first completed run and including the indicator that the next call is
   actually made gives the claimed expectation inequality for randomized,
   adaptive policies, including zero-call stopping.
2. On the event of a completed run before stopping, the absorbed potential is
   exactly `u(L)`; on every other event it is nonnegative. The finite-horizon
   inequality therefore bounds the event probability without a tail assumption
   beyond the target budget. Taking the increasing union over horizons is
   legitimate.
3. For independent Bernoulli continuation, disjoint blocks establish finite
   expected waiting time. The drift becomes equality; bounded convergence of
   the potential and monotone convergence of the stopping time give
   `E eta_L=u(L)`. Mixing the run-until-success policy with zero-call stopping
   attains `min(1,B/u(L))` for every budget. Thus the sharpness statement is
   correctly about the exceptional-run probability, not a universal simulation
   error lower bound.

## Challenge of the finite return-polytope theorem

4. The invariant set hypothesis includes the seeds and every positive normalized
   branch of every seed image. Consequently the continuation probability bound
   remains valid after conditioning on the virtual hidden seed choices. This is
   stronger than a bound only on the visible posterior and is the hypothesis
   actually available here.
5. The countable exact refinement is a valid proof device: every returning
   branch has a seed decomposition, every continuing branch has its exact
   normalized image, and linearity preserves every subnormalized word state.
   It is not counted as a finite implementation.
6. In the finite model, the first modified successor requires at least `L`
   consecutive continuing reports. A return re-enters the original seeds, and
   every shorter continuation word is present. Identifying equal physical
   states cannot create an earlier overflow, because successor states depend
   only on the current density matrix and the requested command/report.
7. The common-path coupling gives a common positive contribution to the stopped
   classical-quantum law. Trace distance of the unmatched portions is at most
   their common missing mass. Arbitrary causal terminal POVMs then contract
   that distance. No external entangled register is included, as stipulated.
8. For unbounded stopping, the finite stopped blocks increase to all stopped
   blocks; the unfinished scalar masses decrease to the nontermination masses.
   Passing to the limit preserves the uniform bound. The approximate process
   need not share the target's expected duration, and the text does not claim
   that it does.
9. The extra initializer uses the initial mixture only on the first actual
   command and has the correct zero-call decoder. It is counted and is not
   re-entered. The theorem asserts an upper of `G(L)+1`, not necessity.
10. The commuting-map count is the number of nonnegative multi-indices with
    total degree below `L`, namely `binom(L+b-1,b)`. Subnormalization and
    deletion of zero images cannot increase that count. The polynomial orbit
    conclusion fixes `r` and takes `B/delta` to infinity, as required.

## Challenge of the explicit qubit construction

11. Inherited R75 gives report-zero probability `1/8`, reset-to-tau report one,
    and a normalized report-two Bloch radius at most `5/11`. The real Bloch
    plane is invariant. The equilateral triangle has inradius `1/2`, so the
    return hypothesis holds at every represented input and supplied angle.
12. With `h=1/8+r_1/16`, the third report has mass `p2=7/8-h` and
    subnormalized Bloch vector `u2=-R_theta*r/8-h*v0`. The proposed weights
    `(p2+2*v_j dot u2)/3` sum to `p2` and reproduce `u2`, using
    `sum v_j=0` and `sum v_j*v_j^T=(3/2)I`. Their margin is
    `p2/33 >= (11/16)/33 = 1/48`. This verifies positivity and normalization
    of the full report table, not just the continuation branch.
13. Keeping multi-index labels even at coincident physical states is permitted.
    At depth `L-1`, modifying the next zero report still waits until `L`
    consecutive zeroes. Substituting `r=1/8` gives exactly
    `7B/[8*(8^L-1)]`, and the stated ceiling makes it at most `delta`.
    The algebraic-state and algebraic-transition assertion follows from the
    finite rotation products and explicit return weights.

## Challenge of the physical-dictionary lower and upper

14. **Causal terminal choice and budget.** Fixing `n` before the experiment is a
    valid policy. The effect `rho_n` is requested only after the visible prefix
    `1 0^n` completes; it does not affect previous report transitions. Report
    one from `I/2` and each subsequent zero have probability `1/8`. Including
    the initial coin gives prefix mass `p_n=zeta*8^(-(n+1))` and expected call
    count `zeta*sum_{j=0}^n 8^(-j) <= zeta*8/7 <= B`. The geometric cost,
    rather than a deterministic horizon cost, is essential and is correct.
15. **Joint events, not rare conditioning.** For the subnormalized simulator
    state `A_n`, the event of prefix completion gives `|tr A_n-p_n|<=delta`.
    The joint event of prefix completion and the complementary terminal
    outcome has zero target probability and gives
    `tr[(I-rho_n)A_n]<=delta`. Positivity and `p_n>delta` therefore force one
    positive-weight dictionary state to have fidelity at least
    `1-delta/(p_n-delta)`. No conditional-TV estimate is smuggled into this
    deduction. The randomized initial coin may be included in the common
    policy history; the successful nonempty report prefix itself already
    distinguishes the begun test from zero-call stopping.
16. **Packing constants.** For `0<=n<J`, the displayed condition on `delta`
    implies `delta/(p_n-delta)<=c^2/J^2`. A mixed Bloch vector within this
    fidelity deficit is within Euclidean distance `2c/J` of `v_n`. The
    Diophantine inequality and `sin(pi*x)>=2*x` on `[0,1/2]` imply pairwise
    orbit distances at least `4c/(n-m)>4c/J`. Strict separation excludes one
    physical dictionary label serving two of the `J` witnesses.
17. **Counted pure-start extra label.** Zero-call binary POVMs force the
    initializer's Bloch length to be at most `2delta`; hence its fidelity
    with every pure state is at most `1/2+delta`. The lower-bound condition
    with `J>=2`, `c<=1/2` gives `delta<1/4` and witness fidelity at least
    `15/16`. Thus the initializer cannot be any of those `J` labels. This
    argument uses the physical decoder restriction even at zero calls.
18. **Finite orbit-prefix upper.** Irrationality supplies a nonzero multiple
    distance `d<1/4`. The points with indices `0,q,...,floor(1/d)*q` have
    circular gaps at most `d`, in either orientation, so a sufficiently long
    ordinary orbit prefix has all central gaps below `pi/2`. Its polygon
    contains the radius-`5/11` disk. With `K` seeds, continuation images at
    depth below `L` lie among precisely the first `K+L-1` orbit points. Even
    the last seed needs at least `L` successive zeroes before it can exit
    this dictionary. Returning decompositions stay in the original seeds.
19. **Leading constant.** For fixed `B>0`, the upper is
    `log_8(1/delta)+O_B(1)`. Setting
    `J=log_8(1/delta)-2*log_8(log_8(1/delta))+O_{B,c}(1)` with a sufficiently
    negative constant satisfies the lower condition. Both counts therefore
    have the stated ratio limit of one. No uniform joint limit in `B,delta`
    follows or is asserted.
20. **Golden phase.** The conjugate product is the nonzero integer
    `p^2+p*q-q^2`; the other factor has absolute value at most
    `sqrt(5)*q+1/2 < 3*q`. Thus `c=1/3` is valid for every positive integer
    `q`. The sorted first five phases have gaps `2*omega-1` and
    `2-3*omega`; `3/5<omega<5/8` makes the larger gap less than `1/4`.
    This verifies `K=5` without numerically sampling phase gaps.
21. **Original rational rotation upper.** For `cos(theta)=3/5` and
    `sin(theta)=4/5`, the seven listed points are in circular order.
    Their consecutive-edge distances are `cos(theta/2)=2/sqrt(5)`;
    the closing-edge distance is `-cos(3*theta)=117/125`. Both exceed
    `5/11`. The orbit coordinates and polygon barycentric linear systems
    are rational, so the proposed transition tables can be rational.
    This upper neither proves nor presupposes a badly-approximable
    certificate for `theta/(2*pi)`.

## Scope and retained open points

- The two files correctly distinguish general return-geometry uppers from
  the special instrument's explicit construction and the still narrower
  physical-dictionary lower.
- The source now explicitly restricts transition tables to causal tables
  fixed independently of later terminal measurement requests.
- The source now states that a matching lower for arbitrary classical
  terminal decoder tables remains open. The previously potentially
  ambiguous general sentence about no matching lower is absent from the
  checked text.
- No new theorem was proposed or added in this challenge. The note does
  not increase the count of numerical diagnostics performed elsewhere.
- Compile status, complete manuscript integration, bibliographic priority,
  and journal-level significance remain outside this focused audit.
