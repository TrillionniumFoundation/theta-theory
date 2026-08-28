# Referee guide — Paper I

## Central claim

The paper proves that two crossed one-sided graph-current estimates imply an
absolutely summable two-time product tail whenever the strict logarithmic rate
condition `A0 B0 > C0 D0` holds.  It then proves that the same complete topology
supports finite difference quotients and a directed third-source totalization,
producing a continuous third spectral jet on a graded Banach scale.

## Suggested audit order

1. Check the interpolation calculation in Theorem 3.1 and the necessity of the
   strict rate window.
2. Check that the finite-DQ theorem is stated in the complete `l1(N^2)`
   topology rather than pointwise in the time indices.
3. Check the common-refinement cancellation and tail estimate in the
   CM2-to-U3 theorem.
4. Check the regularity typing of the third-order contour-resolvent words.
5. Audit the exact derivative formula and spectral contraction for the
   four-branch family.
6. Audit the nonzero seam-current argument.
7. For the specular radial theorem, distinguish invariant-projector/source U3
   from arbitrary noncoboundary reduced-resolvent response.
8. Check the unique-shortest-period-two hypothesis used in the nonconjugacy
   argument.

## Principal theorem dependencies

The abstract theorem assumes a simple isolated invariant eigenvalue and a
level-preserving reduced resolvent.  These are standard spectral hypotheses,
not conclusions of local moving-face geometry.  The actual four-branch family
verifies them directly.  The radial Sinai application uses the established
fixed-table spectral gap for finite-horizon dispersing billiards.

## Permanent scope boundary

The paper does **not** prove that every finite-horizon specular deformation has
third response for every noncoboundary twist.  The positive specular result is
an invariant-projector/source assembly theorem and an exact cohomological-twist
theorem.  A generic noncoboundary application must verify the bilateral
third-source packet.

## Items external review should verify especially carefully

- completeness of the chosen graph-current source module in any intended
  billiard application;
- compatibility of common-refinement UIDs with the physical collision atlas;
- the local right-inverse hypothesis in the geometric maximality theorem;
- all bibliography metadata and novelty comparisons.
