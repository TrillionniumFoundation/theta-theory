# Author presentation precision corrections

These are the actual delegated final author edits to `main.tex`,
`revision-introduction.tex` and `RESPONSE_TO_REFEREE.md` on 19 October 2026.
They are not new theorem bodies, a new referee report, or a claim that the
full raw local limit theorem has been completed. The three files were
copied into `before/` before any edit. `BEFORE_IDENTITIES.json` and
`AUTHOR_PRECISION_CORRECTION_RECEIPT.json` record their original and final
byte lengths and SHA256 identities. `AUTHOR_PRECISION_CORRECTIONS.patch`
is the complete unified diff against those actual copies.

| Location | Correction and its mathematical reason | Native authority |
|---|---|---|
| Abstract | State the proved moment orders `1 <= gamma < 2`; remove the assertion that the actual marked-source threshold is sharp. The moment proof supplies upper bounds; it does not supply a lower density or a critical divergence theorem for that source. | `cor:nm-moments` |
| Abstract | Specify the complete covered sum over marks of proportional endpoint depth before asserting decay after collision normalization. A fixed shallow mark is not paid by multiplying a depth bound by `m^2`. | `thm:zf-flux`, `eq:zf-deep` |
| Introductory kernel argument | Treat `l=1` directly and use exactly `l-2` propagated genuine collisions only for `l>=2`. Name the additional Borel selector `0<=h<=1`. | `thm:nm-kernel`, `cor:nm-joint` |
| Critical reference | Distinguish the closed physical configuration `Q_*` from its endpoint-angle pair `q_*`; specify its actual regular-word limiting origin, zero endpoint momenta and original endpoint cap. | Setup preceding `lem:zf-formal` |
| Covered actual source | Require all `m+1` actual contacts to agree with the designated inverse branch, with original physical cuts retained. Agreement of only one contact or two endpoint angles is insufficient. | Covered-point definition preceding `thm:zf-flux` |
| Gradient-coordinate formula | Define `mathcal B(g)=B(q(g))`; retain `K_{B,g}` and the exact Euler remainder with weight `s`. Endpoint derivatives of `B(q)` and gradient-coordinate derivatives of the composition must not be conflated. | `eq:zf-Bg`, `eq:zf-euler` |
| Clearance levels and sides | At zero level use the physical `u>0` side. At positive levels charge one specified incident side, and add the two charges if both sides are included. The deep sum may specify one level `u_j` for each flight. | `thm:zf-flux`, `eq:zf-deep` and its incident-side conventions |
| Actual cross-curve comparison | Use the native `C_\times` and `mathcal J_m(x,xi)`, explicitly quantifying arbitrary nonzero vectors with slopes in `[100/47,170/9]` and the Euclidean norm in physical `(s,phi)` coordinates. Specify the closure-valid interior strip matching and retain the exact endpoint factors. | `thm:xd-cross-distortion`, `cor:xd-normalized-cocycles` |
| Response trace table | The tangency mark creates no collision at the marked foot; a later actual hit of that disk remains an ordinary collision. The former phrase “remains unvisited” could incorrectly exclude those later physical trajectories. | `thm:nm-trace` |
| Response joint inequality | Explicitly quantify every Borel selector `0<=h<=1` in the response itself. An unrestricted multiplier would not obey the displayed fixed constant. | `cor:nm-joint` |

The exact 316–318 proof bodies were rehashed after these edits and match
their three fixed preinterruption SHA256 values. No proof body, checker,
navigation generator, or historical navigation file was modified by the
agent making these three document edits. The principal author separately
handles navigation preservation and execution.

No compilation was invoked in this correction step. Earlier successful
builds concern their recorded source fingerprints. A new actual build and
regenerated navigation are required for the corrected main and introduction;
the old PDF is not silently relabelled as the corrected article.
