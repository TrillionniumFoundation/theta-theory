# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/A1_MAPPING_TORUS_ONE_SIDED_RESPONSE.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| False bilateral directional Lasota--Yorke inequality | Replace the bilateral inverse-shift estimate by two one-sided Ruelle operators on future and past tails; the translated-cylinder counterexample is included as a regression test. | `lem:r10-a1-one-sided; cor:r10-a1-resolvent` |
| Physical section confused with symbolic natural extension | Keep the square as the Liouville section and the two-sided shift only as a measurable coding extension. | `thm:r10-a1-factor` |
| Hybrid reset called one autonomous Hamiltonian | Use the exact symplectic mapping torus; the global autonomous Hamiltonian is H=E on the quotient, so no external reset is applied. | `thm:r10-a1-suspension` |
| Undefined products of seam currents | Use typed Hadamard cut derivatives between graded trace spaces; intersections are represented by ordered traces, never by multiplying distributions. | `lem:r10-a1-currents` |
| Physical and symbolic response mixed | Transport observables through the coding maps and differentiate the commutative physical/symbolic diagram. | `thm:r10-a1-response` |
| Mechanical valuation overclaim | Retain the identification only under equality of canonical likelihood cocycles. | `thm:r10-a1-work` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
