# Common actual platform - `OB3-PE-v1`

For `rho in [-1/20,1/20]`, use three circular obstacles

```text
K1(rho) = B((0,0),1+rho),  K2 = B((6,0),1),  K3 = B((0,9),1)
```

with unit-speed free flight and Euclidean specular reflection. Uniform no-eclipse margins give the fixed code shift with no consecutive repeated obstacle.

The actual free-flight roof is `tau_rho`. The base path preparation is the Bowen-Margulis equilibrium state of the suspension potential `-h_rho tau_rho`, where `P(-h_rho tau_rho)=0`. The mechanical macro observable is the fraction of collisions on obstacle 1.

A prepared impact frequency `r in (0,1/2)` selects `theta_rho(r)` through the pressure derivative. The tilted equilibrium state remains an invariant preparation of the same deterministic billiard.

The centered impact fluctuation has collision variance `Lambda_rho''(theta)` and physical variance obtained by division by the mean actual roof. Papers I-III use only this platform.
