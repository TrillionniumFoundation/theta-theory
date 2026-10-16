# Response to the v111 referee report

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revision:** A2-DYN 112, 14 October 2026  
**Controlling report:** `ddd59615ed6e7073f9cc85bf76ab269cf0b3889a`, report blob `a9173eb21f73bedd968ccfadfb3ee87215db7a20`  
**Reviewed author source:** `8c617cafa5e5493e26817401e866b2415522f7c0`

We retain the original exact-label raw pointwise assertion and its full
physical source. This revision develops the incidence part of the
referee's Route B without converting the problem into a specialist-only
replacement theorem, deleting an arithmetic class, or identifying
clearance with a visited incidence. All prior active mathematical modules
remain in the article; the entire previous source packet is also archived
byte-for-byte.

## 1. Principal objection: the localized shortage was not proved small

We agree that the unscaled bound `C epsilon` cannot be multiplied by
`m^2` at a fixed outer stage and declared negligible. The new proofs supply
an actual collision-dependent gain on additional positive submeasures.
They do not claim that the complete remaining shortage has vanished.

### 1.1 Joint depth and severity, not just the existence of a witness

Module 268, Theorem `thm:v112-load`, defines on the original trajectory

\[
\mathscr L_\varepsilon
=\sum_{i:\ c_i<2\varepsilon q_0^{d_i/4}}
                      \log(2\varepsilon/c_i).
\]

Every summand is nonnegative. It contains the depth contribution
`|log q_0| d_i/4` plus the amount by which the incidence lies below the
original threshold. For `alpha=|log q_0|/4`, the complete physical sum gives

\[
\|D[e^{\lambda\mathscr L_\varepsilon}]\|_\infty
\le C_\star\exp\{4K_\star\varepsilon/
                            (e^{\alpha(1-\lambda)}-1)\},\quad 0<\lambda<1.
\]

The proof is a positive product majorization followed by the retained
marked-pressure theorem. It assumes neither independent collisions nor
an exact-label mixing estimate. Optimizing at finite count gives

\[
\|D[\mathscr L_\varepsilon\ge u]\|_\infty
\le C_\star\exp[-u+2\sqrt{b_\varepsilon u}],
\qquad b_\varepsilon=4K_\star\varepsilon/\alpha,
\]

for `u>b_epsilon`, with an additional minimum against `C_star`.
At `u=(2+eta) log(m+1)` this is an actual normalized payment of rate
`m^{-eta+o_B(1)}`. It includes a single sufficiently severe shallow
incidence, which the v111 depth/count classification did not pay.
No claim is made that an arbitrary synthetic incidence pattern is
realized by a billiard trajectory.

### 1.2 The actual two-end depth geometry improves the count threshold

The same module proves

\[
r^{\lfloor(s+1)^2/4\rfloor}
\le e_s((r^{d_i})_{1\le i<m})
\le (s+1)r^{\lfloor(s+1)^2/4\rfloor}/(r;r)_\infty^2,
\quad r=q_0^{1/4},\quad m\ge s+1.
\]

The upper bound comes from the coefficient of
`prod_{d>=1}(1+z r^d)^2`; the proof of its coefficient formula is included.
The lower bound uses the balanced two-end depth set. This lower bound
concerns the deterministic polynomial only, **not** the physical density.
Combined with the unrelaxed elementary-symmetric witness bound, it gives
a quadratic count tail and a normalized payment at a count of order
`sqrt(log m)`. This is a strictly smaller asymptotic order than the previous
`log m/log log m` schedule. Both schedules remain available; no uniform
finite-count numerical improvement is claimed.

### 1.3 Exact source preservation and the honest endpoint

Module 269 proves, before and after the original roof pushforward,

\[
\mathsf U_B^{per}=\mathsf U_B^{exc}
                  +\mathsf U_B^{load}+\mathsf U_B^{low},
\qquad \mathcal H_M(\mathsf U_B^{load})=0.
\]

The full original nongrazing capacity is used on both sides of the
residual comparison; it is not spent twice or restricted to convenient
source points. All outer windows and costs remain fixed before the
physical sum, exact-label/radius/roof suprema and collision limsup.
The Chernoff parameter is optimized only inside a finite-count inequality
valid at every parameter value, not inside a fixed-width spectral theorem.

The retained source has bounded total incidence depth, bounded total
logarithmic severity, and fewer than the displayed square-root-logarithmic
number of incidence witnesses. Its clearance witnesses can still occur
at arbitrary depth. In particular, a state with no incidence witness
and a clearance-only guard witness is not paid by the new theorem.
Critical entrances and section cuts are not removed merely by name.

Equation `eq:v112-remaining` remains unproved. The manuscript, response,
proof ledger and publication-status file state this consistently.
The principal referee request is therefore **advanced but not closed**.
The work has not been reframed as a no-go theorem or a different topic.

## 2. Explicit status at the beginning of the introduction

The opening paragraph lists the proved global uniqueness, marked-pressure
and normalized payment results, identifies their inherited inputs, and
states that the complete raw pointwise assertion is still the target.
The abstract makes the same distinction. The article does not present
source or software qualification as an LLT proof.

## 3. Explicit inherited pressure and optical input

Module 266 now has Input statement `input:v112-geometric-pressure`.
It specifies the circular family, finite-horizon and curvature bounds,
endpoint section cap, full-area two-sided regular set, stable Jacobian
in `(s,phi)` Euclidean arclength, its consistent block cocycle, the
original `(alpha,p)` endpoint derivative, and the precise uniform
inequalities with constants `Q_star,C_0,C_1`.
The original proofs in modules 238, 239 and 241 are copied and SHA-pinned.
They are retained inputs, not newly independently certified continuum
results. In particular, unconditioned physical pressure is not described
as twisted or exact-label pressure.

## 4. Unbounded weights and monotone exhaustion

Module 265 now includes Proposition `prop:v112-exhaustion`.
It chooses countably many relatively compact local diffeomorphism charts,
disjointizes their Borel source pieces, fixes angular seams, truncates the
weight and the number of charts together, tests against nonnegative Borel
functions, and only then passes by monotone convergence and Tonelli.
The pressure bound subsequently supplies finiteness. Null-set passage
from the two-sided regular set is made on the locally Lipschitz charts
at each fixed radius, followed by Fubini. No radius-independent exceptional
set or prior integrability of the unbounded marked weight is assumed.

## 5. Marked-step indexing

The block proof in module 266 now displays the exact indexing from steps
`0,...,m-1`, with marks in `1,...,m-1`. The example `m=7`, `S={1,2,6}`
leaves lengths `(1,0,3,0)` and three deleted physical symbols. Adjacent
marks, the final mark and `P_0=1` are explicit. Homogeneity strips are not
counted at a removed incidence.

## 6. Unscaled versus normalized bounds

Every pressure summary retains its unscaled scope. The new normalization
is obtained only after the exponential tail or quadratic depth exponent
is evaluated at the displayed finite-count threshold. The explicit
`m^{-eta+o_B(1)}` rate, and the fixed-outer-stage quantifiers, are proved
rather than inferred from the label tests on the left side of an upper sum.

## 7. Incidence and clearance notation

The new load uses only the original incidence witnesses. It contains no
third-disk clearance factor. The residual discussion explicitly includes
unvisited tangencies, clearance-only witnesses and arbitrary clearance
depth. The words 'localized' and 'low load' are immediately qualified as
incidence statements. No clearance theorem is claimed.

## 8. Prior workflow provenance

The two successful exact-SHA v111 runs, `38535355035` and `38535364837`,
were re-read through GitHub's Actions API and are recorded in
`provenance/v111-ci-observed-2026-10-14.json`. The v111 packet, including
its pre-run validation statement, remains byte-identical in its original
path and in `archive/v111`. It has not been retrospectively rewritten.

## 9. Validation and independent reconstruction

The new tests check the depth polynomial, balanced minimum, exact
fractional-power product majorization, Chernoff optimization, strict
threshold boundary, positive source identity and two negative controls.
Inherited optical and physical-trajectory diagnostics are retained.
Normal/optimized agreement and typesetting are recorded separately.
These checks do not establish physical realizability of synthetic test
patterns, the historical uniform pressure theorem, every original pairing
sheet, or the final shortage. The specialist reconstruction obligations
in section 20 of the report remain visible in `PROOF_LEDGER.md`.
