# Specialist audit map: revision 51

## New, self-contained real analysis

Check `lem:v51-local-convolution-height`: the sum of cell suprema is bounded by `||K||_1/h+||K'||_1`; the limit in h is after the collision limsup and K remains fixed. Check `prop:v51-positive-principle`: the error identity is exact, the kernel may have either sign, and only the remainder must be nonnegative. Check that the positive-part map is 1-Lipschitz in the new positive criterion. Check the normalization factor in `thm:v51-conditional-minorization` and the direction of the reverse likelihood inequality.

## Inherited continuum inputs

The proof still depends on the physical thin-layer multiplier (module 105), full occupation-torus power bounds and moving peaks (84--87), all-depth decision bound (103), physical-only source partition (104), protected pointwise correction (99), and full fixed-band arithmetic inverse (93). These are not certified by the new elementary lemmas. The inherited source files are unchanged.

| Multiplier hypothesis / issue | Exact manuscript check | External input / remaining audit |
|---|---|---|
| Fixed number of regularity cells per homogeneity strip | `lem:v49-physical-envelope`, bounded trigonometric degree and finite center list | DPZ arXiv:1902.06850v1, Lemma 3.3(b); verify complete list and strip cuts |
| Bounded intersections and boundary-neighborhood length | Positive clearance slope versus negative stable slope, formula `eq:v49-transverse-derivatives` | Verify uniform cone and graph matching constants |
| Coalescing parallel boundaries | Whole thin interval charged if width is below graph distance | No inverse-width norm may be introduced |
| Grazing horizontal thresholds | At most two new cuts; angle coordinates retained through homogeneity strips | Check the actual homogeneity convention and stable-length normalization |
| Piecewise Holder and norm exponents | Constant indicator on each cell; `eq:v35-exponent-choice` | Pinned DPZ numbering; no endpoint Holder exponent |
| Physical multiplication on completion | `prop:v49-physical-multiplier` | Check agreement with limits of actual smooth densities |
| Previous incident disk | A physical hitting line has distance <= R; envelope requires >= R | Intersection is tangential/null, not a thick added region |
| Mark and source normalization | Clearance j is marked at j+1; occupation ends at m-1; source nu/c | Check once, without adding another 1/c in module 108 |

No independent human audit has occurred. The new analysis neither transports through a physical singular seam nor proves the missing positive-height bound.
