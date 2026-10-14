# Response to the external report on A2-DYN revision 98

**Author:** Qian Qi. **Revision:** 100, uniform-capacity revision, 13 October 2026.

**Controlling report:** `reviews/a2-dyn-v98-external-top4-review-2026-10-13/REFEREE_REPORT.md`, commit `357e47da83265ac52bbc65b524aecccc6100508b`, blob `041bdf3eb46f24c09dbc1a469a5e728713c4d900`.

**Immediate author baseline:** v99, commit `09685ba342a68d8551c87587540ff5a17c09726e`, paper tree `864bea62f1a63c5ec07e765cf4f720aaba0ebbe4`. Both baseline runs `38343313528` and `38343321404` succeeded. Those runs qualify v99 only. At initialization the latest visible external report was v98; the present revision continues v99's response instead of presenting the prior fixed-radius result as new. The distinct uniform-capacity branch names avoid overwriting an existing plain-v100 placeholder.

We thank the referee for separating the actual weighted momentum capacity from the positive short-trace source. This revision discharges the **family-uniform spectral-capacity condition**, by a geometric pressure proof which has no table-dependent mixing time, and then derives the original family-wide uncut and critical-height conclusions. The positive nongrazing paired-trace height is still not proved. The original title, model, exact labels, guard, normalization, arithmetic reference and uniform pointwise objective are unchanged.

## 1. Capacity and the required actual-fiber estimate — request 12.1

The v99 momentum uniqueness and marked comparison are retained, not repeated as this revision's new result. Module 241 supplies the missing uniform pressure control. The published long-cell reduction is audited at potential parameter one using common geometric constants. A finite grid of homogeneous short stable tests meets every long backward cell, uniformly in radius and count. Whole-cell distortion compares its stable weight to a homogeneous inverse piece of one test. Dropping the final stable factor leaves only a uniformly bounded number of true one-step physical cuts; it does not introduce an infinite count of homogeneity strips. Distinct backward cells assigned to one test give distinct inverse pieces. The uniform curve-growth estimate then bounds the complete pressure sum.

The parameter audit is explicit: curvature, flight bounds, cone angles, homogeneous tail, finite-step branch moduli and finite displacement count are common over the prescribed compact circular family. Long-cell constants are selected using those finite choices and geometric series. No radius-uniform conclusion is inferred merely from compactness and pointwise-in-radius convergence. The proof avoids the fixed-table mixing/Cantor-rectangle argument used in the older pressure deduction.

Module 242 inserts that uniform pressure bound into the *actual* marked optical comparison, obtaining `K_m <= K_*` uniformly in radius and collision count. It follows that `m^6 K_m theta_Bstar^(2m)` tends to zero at every fixed admissible band. The earlier finite-block strict margin is also certified analytically by choosing a fixed block larger than `log(max(1,Q_*))/(-2 log theta_Bstar)`; this is not a claimed numerical optimization or a band growing with collision count. The condition (SC) is no longer a new unproved hypothesis.

## 2. Complete error before cutoff removal

The same module proves the actual insertion `I_m z^-p 1_{0<z<b}` for every `1<=p<129/128`. Its theorem displays both finite-count caps and the complete resulting error. The quadratic cap is uniform before any collision limit. Positive layer cake extends to zero gradient first. At a fixed band the remaining error has exponential rate `theta_Bstar^(m(4-2p)/3)`, times the displayed fixed constants and `m^2`. Only afterwards are the collision and auxiliary-band limits taken.

The exponent is on the endpoint gradient, not on `I_m`; no result for `(I_m/z)^p` or a bounded strong-space singular multiplier is asserted. At `p=1` this gives the full radius-uniform uncut inverse-gradient concentration required by the critical certificate and trace comparison.

## 3. Positive paired short trace — request 12.2

Theorem `thm:v100-recovery` now controls the entire grazing-ended short source and the complete short-trace comparison error uniformly in the radius, with cost `C(1+epsilon^-1)delta` and no capacity premise. The long critical residual has height `C(qr)^(257/256)` on the retained schedule. These are family-wide results; v99 had removed the premise only at a fixed radius.

The positive minimum of two nonzero endpoint traces is still a separate source. Neither a small outgoing-minus-incoming difference nor a bounded pressure sum forces that minimum to be small. The theorem therefore retains `H_M(T_S^epsilon)` explicitly. Backward critical traces are not erased merely because the critical set has zero original area. The full positive nongrazing paired-height claim remains false, and request 12.2 is not marked closed.

## 4. Separate obligations and the original scalar schedule — requests 12.3–12.4

The family-uniform capacity obligation has been discharged. The remaining scalar inequality is the original one with the same source and target, now without an additional (SC) or finite-block premise. With `q=1/8`, `r=c epsilon(B)^4`, `a=sqrt(qr)` and `delta=6qr`, its explicit critical and comparison terms have orders `epsilon^(257/64)` and `epsilon^3`. The only unestimated term in this retained reduction is the positive paired short-trace height.

All physical sums, marked insertions, test assignments and zero-gradient integrations precede the collision limit. The auxiliary band is fixed first and enlarged only afterwards, and B is last. The original full pointwise theorem is not replaced by fixed-radius recovery, a weak local norm or a windowed event.

## 5. Downstream laws — request 12.5

No unrestricted denominator, posterior, likelihood, relative entropy, path total variation or same-roof ratio is promoted. The retained lower pointwise and finite-roof-norm conclusions remain intact. The full upper half still needs positive paired-trace decay. Zero arithmetic classes remain in the unnormalized theorem and are never divided by.

## 6. Specialist verification — request 12.6

The new audit map specifies the uniform long-cell choice, finite stable testing, bounded last physical split, whole-cell rather than same-curve distortion, and multiplicity-one assignment to inverse components. These are load-bearing continuum checks. The inherited Cartesian uniqueness, optical/stable normalization, actual marked-fiber bridge, coarea kernels and four-record spectral remainder remain identified inputs. No independent human specialist approval or formal proof certification is claimed.

The primary sources were read directly: Baladi–Demers arXiv:2009.10936v3, especially Lemmas 2.2, 3.3, 3.5 and 3.6; Demers–Zhang arXiv:1210.1261v1, Theorem 2.5, Remark 2.7 and Lemma 3.2(b). The finite testing step is proved in the new manuscript, not attributed to a uniform mixing theorem in those references.

## 7. Exposition, preservation and qualification

Every prior core file, Python source, appendix, bibliography and provenance file is retained byte-for-byte with its mode. The full v99 article is in the archive and every v99 top-level file is additionally snapshotted. Both v88 variants and every frozen review remain untouched. Current claims are stated in the active abstract, theorems, response and ledger; historical conditional statements are not rewritten retroactively.

The new workflow pins the v99 source tree, controlling report and both v88 variants; it checks preservation, two explicitly justified capacity/margin status supersessions, normal/optimized finite fixtures, native article and complete archive, all 243 recorder modules and page geometry. Its result must be read at the new final SHA. Source qualification does not certify the new geometric proof or the unproved positive paired-trace theorem.
