# Inputs to the damped-unsmoothing proof

This revision adds no external continuum theorem. It uses the existing primary-source collision-space framework through the exact statements already printed in the paper.

`core/22_collision_covariance.tex`: mean-preserving BV smoothing, supremum contraction, `L1` approximation, uniform BV of the bounded collision compensation and its residual. The fine smoothed residual is used only as a multiplier; it is never the observable defining a new twisted operator.

`core/46_finite_order_damping.tex`: fixed-order product decoupling, finite partition cumulants and anchored sums; the real-frequency power bound with its original coarse-scale analytic-disk and Taylor-remainder restrictions. The clock uses cumulants only through fixed order twenty, while the spectral polynomial still has degree nineteen. The moment--cumulant identity is derived by finite generating-polynomial algebra in the new proof. Döring--Jansen--Schubert, Probability Surveys 19 (2022), 185--270, DOI 10.1214/22-PS7, remains a background reference; no new all-order hypothesis from that survey is assumed.

`core/28_marked_return_band.tex` and `core/30_unsmoothed_moments.tex`: the actual two-sided recentering, forward/backward visit conventions, fixed collision windows, bounded section-density domination and exact marked measure. The new higher-moment proof improves only the characteristic stopping rate, and does not silently change the old `L2` stopping result.

`core/40_finite_count_edge_extraction.tex` and `core/41_count_localized_raw_inversion.tex`: complete finite-packet extraction for finite-record subanalytic weights, `W^(2,1)` residual inverse, observed count-coordinate support and Schwartz tail. The new raw identity requires their weight class in addition to BV. No long-time derivative bound is imported from constructible finiteness.

The fine-scale third-degree correction has at most four multipliers, including the actual-return mark. Every intervening power uses the same coarse-scale operator; its nonnegative lengths sum to the entire deterministic interval. Repeated times introduce only zero powers. This is the exact reason the polynomial correction retains damping and the fine smoothing scale does not alter the spectral domain.
