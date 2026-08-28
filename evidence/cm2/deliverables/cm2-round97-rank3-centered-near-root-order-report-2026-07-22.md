# CM2 Round 97 — centered near-root ordering frontier

Date: 2026-07-22 (Asia/Shanghai)

Round 97 tests the shortest apparent repair of the Round96 third-competitor
residual: form the candidate discriminant in the same centered `q` arithmetic,
take its square root when positive, and compare the candidate near root against
the designated tangent flight.

The full depth-zero replay is stable but adds no certified gaps:

```text
input base gaps:                    10,205
first+second owner certified:       10,180
third-competitor certified:          1,552
third-competitor residual:           8,628
representation residual:                25
```

Independent 640-bit replay preserves this exact signature.  Thus the remaining
problem is not numerical precision and is not repaired by appending a scalar
square root to the mean form.  Adaptive subdivision with this same formula
wraps at discriminant tangencies and grows exponentially.

The next lawful method is an event-oriented implicit branch certificate:

1. isolate each candidate discriminant-zero parameter by interval Newton or
   Krawczyk;
2. continue the real near-root branch on each side by IFT;
3. compare `tau_near(q)-tau_tangent(q)` with a centered derivative bound;
4. cut only at genuine zero-order events.

Round 97 is a negative frontier certificate; it does not promote the face
quotient or any global gate.

