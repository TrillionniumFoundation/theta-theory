# Final author reconstruction of native 318

This is an internal reconstruction of the revised author proof, not an external referee report. It supplements the preserved independent reconstruction in `../source-audit/INDEPENDENT_CROSS_CURVE_RECONSTRUCTION.md`; that earlier reconstruction's source identity remains unchanged.

## Exact final files

| File | SHA256 |
|---|---|
| `full_word_cross_curve_distortion.tex` | `8bc8010010bb9c9a5f67c511689b89370166af17db6b37ed3771e8abd9a0afbc` |
| `check_cross_curve_distortion.py` | `0c4b0b981b9311f5b98239024a599e45e361255e5d4caf16a4152220663930c2` |

The native file is ready to be copied as `core/318_full_word_cross_curve_distortion.tex`. The checker resolves that exact suffix when installed under `tools/`. No existing article, inherited proof body, old execution record or remote reference was modified by this finalization.

## Homogeneity boundaries under reversal

The definition keeps the original fixed disjoint assignment of artificial strip boundaries. An arbitrary such assignment need not commute with the actual isometry `I(s,φ)=(s,-φ)`. The backward proof consequently uses only the assertion that the two reflected angles belong to the closure of one reflected strip.

Lemma `lem:xd-log-incidence` explicitly proves its estimate on each closed strip. Its grazing bound is valid up to both artificial endpoints because the lower cosine bound is `(2/π)(k+1)^{-2}>0`. The central estimate is likewise closure-valid. Reflection leaves the absolute angular difference and cosine unchanged. Therefore the stated correction requires no repartition, no boundary deletion, no altered index convention and no enlarged constant. True grazing still lies outside the regular derivative domain.

The forward endpoint cancellation uses precisely the interior indices `1,…,m−1`. The unweighted backward theorem uses times `−1,…,−m`; omitting its terminal homogeneous condition retains the ratio of the two true terminal backward incidences. These are the unchanged physical time indices, and neither original section membership nor a roof label is used to discard a terminal factor.

## The native one-flight endpoint-factor lemma

The final source contains `lem:xd-physical-terminal-limit` with its complete geometric proof. Its radius is `R=9/20`, its initial point is `(R,0)`, and its target center is `(1,0)`. The outgoing angle runs through `0≤θ<arcsin(9/11)`. Solving the actual ray-circle intersection gives

\[
c_1(\theta)=\sqrt{1-(11\sin\theta/9)^2},\qquad
\tau(\theta)=\frac{11}{20}\cos\theta-\frac9{20}c_1(\theta).
\]

The difference of the squared nonnegative terms in the latter formula is `1/10`, which proves that this first entry time is strictly positive. The ray leaves the initial disk since its squared distance to that center is `R²+2Rt cosθ+t²>R²` for every positive flight time.

The entire segment lies in `[9/20,1]×[0,11/40]`: its horizontal length is at most `(11/20)cos²θ`, and its height is at most `(11/20)sinθ cosθ≤11/40`. Every nonzero triangular lattice row is vertically separated from that rectangle by at least `√3/2−11/40>R`. Squaring the positive quantities `√3/2` and `29/40` leaves the exact positive remainder `359/1600`. Every other center on the zero row is at horizontal distance at least `1>R`. These estimates cover every lattice center and the complete open segment, not only the terminal contact.

The actual limits are

\[
c_0\longrightarrow \frac{2\sqrt{10}}{11},\qquad
\tau\longrightarrow\frac1{\sqrt{10}},\qquad
Q_1\longrightarrow\left(\frac{139}{220},\frac{9\sqrt{10}}{110}\right).
\]

For a local curve with initial slope `a=100/47` in the physical `(s,φ)` coordinates, the exact differential gives `v_1=κ+c_1(κ+a)/A_0`, where `A_0=τ(κ+a)+c_0` and `κ=20/9`. Thus `v_1→κ`, and

\[
c_1\mathcal J_1\longrightarrow
\left(\frac{\kappa+a}{\sqrt{10}}+\frac{2\sqrt{10}}{11}\right)
\frac{\sqrt{1+\kappa^2}}{\sqrt{1+a^2}}>0.
\]

All family members before the limiting angle are regular and have the same complete lifted one-flight word. There is no derivative at the singular limit. Comparing with the regular member at `θ=0` verifies the need for the actual terminal incidence factor when terminal homogeneity is unspecified. The lemma makes no claim against whole pressure, the raw local limit or the original inverse objective.

## Other constants and inherited inputs

The independent reconstruction already checks the common disk-product minimum and the complete endpoint deficit `E_R≤2R`; the fourth root and rounding constant `q_a^{-1/2}`; the two-sided contact and flight sums; the semicircle chord estimate without inverse incidence; the uniform logarithmic estimate with exponent `1/3`; all four slope-map derivatives and the exact `47/48` contraction; the denominator `2aτ_-`; the single telescoped Euclidean endpoint factor; and the one-time optical cost `30000²`. The final boundary wording and one-flight lemma leave every one of those constants unchanged.

The new theorem remains conditional only on the cited inherited native proofs, principally the geometric localization in 308 and the physical differential/optical comparison in 313. It supplies the uniform cross-curve comparison on every actual common word and its declared homogeneous indices. It does not prove the positive sum of all physical cell suprema. The physical continuation and refinement/renewal payment in the retained pressure route, together with the other original raw-limit dependencies, remains explicit.

## Actual paired executions

Both final executions are retained under `verification-cross-curve/20261019T113255105961Z/`. Normal Python and `python -O` each exited zero, emitted empty stderr, and passed every declared group. Their stdout and details files are pairwise byte-identical, with SHA256 `8e2de1872260c10d218e2fa688674848cf7a4ff0143821bbd3f0ffc5a7923558`. The native and program identities above were unchanged throughout both executions.

The checker has **nine** named groups. The inherited summary incorrectly said ten; the first final receipt wrapper repeated that count and therefore marked its own count validation failed even though both actual programs passed. That original receipt is preserved. `CORRECTED_EXECUTION_VALIDATION_RECEIPT.json` and the separate `validate_final_cross_curve_execution.py` record the correction by verifying all nine exact group names, every status, both real exit codes, both modes and every retained output hash. The earlier 11:09 output also reports nine groups. No mathematical failure has been concealed, and no additional execution is claimed by the correction.

These executions are auxiliary exact algebra and finite-index evidence. The complete continuum proof remains in the native manuscript. No current CI run, whole-pressure theorem, independent journal approval or completion of the original raw local limit is claimed by this receipt.
