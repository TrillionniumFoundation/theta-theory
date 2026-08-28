# Referee-response addendum — physical clock and roof-normalized coefficients

A final cross-paper audit after the initial v4 rewrite identified one interface
that required an explicit theorem rather than a convention: Paper II defines
physical covariance as collision covariance divided by the mean roof, whereas
Paper III's first slow recursion was indexed by collision count.

This interface is now closed by

```text
paper-III-rough-theta/physical-clock-appendix-v4.tex
```

## Added proof chain

1. For the same predictable moving collision process and the same branch roof
   used in Paper II, define
   
   ```text
   C^epsilon(s)=epsilon^2 sum_{k<s/epsilon^2} tau_{I_k}(A_k).
   ```

2. Exact predictable innovations give the martingale decomposition
   
   ```text
   C^epsilon(s)
    = epsilon^2 sum bar_tau(A_k) + N^epsilon(s),
   E sup |N^epsilon|^2 <= C epsilon^2.
   ```

3. The predictable clock converges uniformly to
   
   ```text
   C(s)=integral_0^s bar_tau(Theta(X_r)) dr.
   ```

4. Positivity of the roof makes the limiting clock bi-Lipschitz and gives
   uniform convergence of inverse clocks.

5. Time change of the collision-time diffusion produces
   
   ```text
   dX_t = [b/bar_tau] dt
          + [sigma_c/sqrt(bar_tau)] dW_t,
   ```
   hence covariance
   
   ```text
   Sigma_phys = C_coll/bar_tau,
   ```
   exactly as in Paper II's pressure-root theorem.

6. A branch-dependent semi-Markov one-step operator advances physical time by
   `h tau_i(a)`.  Its consistency equation is
   
   ```text
   bar_tau U_t + b.DU + (1/2) C_coll:D2U
   + (theta/2) DU^T C_coll DU = 0.
   ```

7. Division by the positive mean roof gives the physical-time HJB with the
   pressure-root covariance.

8. The same positive Diophantine roof vector can be used simultaneously for
   the full-frequency suspension theorem, the random clock, the physical-time
   rough limit, and the semi-Markov theta DPP.

## Status

```yaml
collision_count_to_physical_time: PROVED
inverse_clock_convergence: PROVED
rough_path_time_change: PROVED
pressure_covariance_match: PROVED
physical_time_microscopic_DPP: PROVED
constant_roof_shortcut_used: false
remaining_interface_gap: 0
```

This addendum is positive and theorem-level.  It does not remove the
full-frequency nonlattice roof or replace it by a constant-roof example.
