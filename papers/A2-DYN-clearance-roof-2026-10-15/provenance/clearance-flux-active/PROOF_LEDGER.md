# A2-DYN author proof/dependency ledger — clearance-flux revision

## Controlling identities

Complete active author: `45015de51c652bcdaca13123bf65627bf199b2ab`, repository tree `f377dc19c5df4be7c620e0bbed2caabf3b28042d`, original directory `papers/A2-DYN-v112-referee-response`.
Controlling review: `d7fd0b24314d7341f9a611130bb650371d2d5ef2`, report blob `0ad9f500c92db32ea4fc9f6d9ee28630b4484699`.
The paper's title, section, radius interval, physical collision clock and exact four-coordinate target remain unchanged. The word “low” denotes low **incidence** load.

## Status vocabulary

**Direct proof**: a complete written proof from the stated physical geometry and elementary measure calculus, not an independent expert or formal certificate.
**Conditional retained-input theorem**: complete deduction, with a named uniform dynamical input not independently reconstructed here.
**Retained**: unchanged active proof body, with its existing qualifications. No new credit is claimed.
**Open**: no proof supplied and no subtraction from the source authorized.

## New statements

| Anchor / source | Claim | Dependencies | Status |
|---|---|---|---|
| `lem:cf-foot`, 270 | A third-disk near-miss foot lies inside the actual segment, distance at least `g*-delta` from both endpoints; finite one-flight center set | original lattice spacing, disk radii, finite horizon | Direct proof |
| `thm:cf-flux`, 270 | Exact marked-flight disintegration and `integral N_delta dnu=delta/R` | foot lemma; actual backward collision reconstruction; Jacobian magnitude `R`; monotone chart exhaustion | Direct proof |
| `cor:cf-depth-mass`, 270 | All-depth clearance mass bound with exactly one `c*^-1` | invariant collision measure; flux theorem; two-end depth sum | Direct proof; integrated, not pointwise |
| `thm:cf-transverse`, 271 | Increasing-curve forward clearance and decreasing-curve past clearance length `<=Cgeo delta`, uniform at grazing | foot lemma; signed derivative; monotone argument; physical time reversal | Direct proof |
| `cor:cf-multiplier`, 271 | Bounded observable multiplier on stable tests | transverse theorem; pointwise bounded representative | Direct proof; no general distribution multiplier claim |
| `thm:cf-transfer`, 272 | Arbitrary-future-collision `S_a` gain `<=H(Cg Cgeo delta)^(1-a)` | transverse theorem; **Input `input:cf-growth`**; real unit-modulus record twist | Conditional retained-input theorem |
| `cor:cf-all-depth-tests`, 272 | All actual depths, all collision counts, real twists: `O(epsilon^(1-a))` | transfer theorem; exact insertion at `j+1`; positive union domination | Conditional retained-input theorem; no roof norm transfer |
| `thm:cf-record`, 273 | Exact original joint-record roof disintegration | flux theorem; invariance; actual inverse iterates; unchanged Pi | Direct proof |
| `prop:cf-bridge`, 273 | Normalization calculation for a sufficient conditional roof kernel estimate | explicitly **unproved** condition `eq:cf-bridge-input` | Conditional implication only; not a closure theorem |

The first two mechanisms do not use module 241's pressure theorem, the incidence MGF, or the desired LLT to establish their premises. The arbitrary-time bound uses only the separately stated short-stable-curve growth interface, not the stronger whole-cell pressure conclusion.

## Retained active chain

Modules 260–269 are byte-for-byte unchanged in the active manuscript. They retain: optical continuants and Jacobi bounds; visited-grazing trace/capacity payment; positive variation payment; persistent guard support; simultaneous endpoint/cofactor audit; global roof-angle uniqueness and monotone exhaustion; complete target-roof marked incidence pressure relative to its geometric inputs; deep/numerous incidence payments; joint-load MGF and quadratic count tail; the exact low-incidence-load source identity and remaining shortage.

`model.tex`, `inputs.tex`, and `comparison-scope.tex` are also unchanged. Their historical physical pairing, regular variation, averaged spectral and scalar-reduction interfaces are not independently reproved by the clearance extension.

Important direct dependencies retained from earlier sources:
- module 238 stable optical comparison: blob `c79fb9d660ab90370700c4fbfe4d4311175ac60f`;
- module 239 physical-word domination: blob `fc76d61faeb70c0eeca6217c2c09daea4c3b2bde`;
- module 241 uniform geometric pressure: blob `fa0f71468d1f304da492687d949ad00c953402e7`.
All three are present under provenance. The full recursive archive is separately pinned, not represented as locally reconstructed.

## Key analytic audit

1. The line-coordinate Jacobian is `R` in `(alpha,p)`, and `R cos(phi)` in `(alpha,phi)`. Thus the mark flux is `4 pi delta`, divided by `4 pi R`. The exact-record formula adds exactly one factor `1/c*`.
2. Clearance is the minimum over the real segment. The gap proof excludes endpoint minima without ignoring them; the incident disks remain excluded exactly as in the original model.
3. The derivative is `b'=-cos(phi)-t_z(1/R+phi')`. Its lower magnitude uses physical `t_z>=g*-delta`, not an assumed incidence cap. `g*-delta*=9/200`, `a0=9/94`, argument monotonicity margin `600/2491`.
4. A short increasing graph has at most one positive-foot interval per center, and two signed bands. Arbitrarily many physical continuity cuts cannot increase monotone impact multiplicity. The constant counts finitely many one-flight centers only.
5. Time reversal is used in the correct orientation. A mark on flight `j` becomes a past-flight indicator at actual collision `j+1`; the remaining iterate is `m-j-1`, including zero.
6. The absolute stable-test bound uses pointwise bounded representatives, not essential bounds on arbitrary distributions restricted to curves. Multiplication of general anisotropic distributions is not asserted.
7. `a<1` is essential. At `a=1` the geometric-series denominator degenerates; no endpoint claim is made. Real-frequency modulus control is not high-frequency decay.
8. Null collision-area singular sets may be assigned zero for area disintegration. This does not annihilate positive paired endpoint traces, critical entrances, or section cuts.
9. No conditional angular roof density is assumed in `thm:cf-record`. Its kernel is first a measure. The optional bridge condition rules out singular conditional mass and supplies the missing normalization only if separately proved.
10. All core source restrictions and comparisons retain fixed outer widths. None of the new stable-test bounds is inserted as if it were an `m^2 L-infinity` roof bound.

## Still open, with a precise closure interface

- **Clearance target-roof gain.** Derive a uniform estimate for the exact marked-record kernels in the physical roof topology. Equation `eq:cf-bridge-input` is one stronger sufficient condition, not claimed necessary or true; a suitably integrated-in-clearance kernel estimate allowing angular folds, or a valid capacity comparison, would suffice instead. An appropriate summed bound must pay `m^-2` before the collision supremum/limsup. No arbitrary interchange of fixed-clearance disintegration, roof supremum and limits is permitted.
- **Low-severity shallow incidence.** Supply a collision-normalized source bound or sufficient physical comparison capacity. The new clearance results do not cover incidence-only states by analogy.
- **Full nongrazing capacity.** Prove abundance for the unchanged pool or directly pay every source state outside it. No source-selected pool is substituted.
- **Positive boundary sources.** Complete the inherited physical pairing/coarea interfaces at critical entrances, section cuts, singular paired endpoints and all relevant seams. Area-nullness alone is not a payment of their boundary coefficients.
- **Core independent reconstruction.** Uniform pressure, stable optical comparison, full physical multiplicity, spectral/arithmetic data and the historical inversion chain still require the same source-specific expert reconstruction; new finite tests do not do this.
- **Final theorem.** `eq:v112-remaining` and hence the complete original raw pointwise LLT are still open in this packet. The four-coordinate inverse objective is retained, not declared complete.

## No duplicate contribution

The retained low-load support already satisfies `alpha f(N)<u_m`, hence the square-root-logarithmic count restriction. We retain the independent count theorem but do not claim its bound as an extra new payment of that same retained source. No new residual symbol is introduced to suggest closure.
