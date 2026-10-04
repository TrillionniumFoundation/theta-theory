# Rational enclosure example

Run `python3 tools/reciprocal_intervals.py examples/compass-two-by-two.json` from the paper root. This is a synthetic killed two-by-two lattice occupation of value one, not physical measured data. Half of the compass steps leave this state set, so the exact tail after two steps is 1/4. The exact iterate is 3/4 and the conditional occupation enclosure is [3/4,1] at every node.

For real data the forcing intervals must incorporate all simultaneous confidence and calibration allowances. A survival bound must follow from the physical component/step bounds and the protected-aperture argument. The example does not provide or verify those inputs for a physical apparatus.
