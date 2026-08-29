# Theta-Theory v11 — deterministic hard-sphere kinetic cotangent candidate

The controlling source is stored as ordered base64 parts under `source/`.
Reconstruct it with:

```bash
cat source/part-*.b64 | base64 -d > theta_v11_hard_sphere_kinetic_source_only.tar.gz
sha256sum -c theta_v11_source_only.tar.gz.sha256
tar -xzf theta_v11_hard_sphere_kinetic_source_only.tar.gz
```

The extracted tree contains five manuscripts, status records, verifiers and a build workflow. The inherited v9 expanded `papers/` tree is provenance only and is not the controlling v11 source.

Platform: `HSBG-LIO-v1`. Scope: deterministic three-dimensional hard spheres, thin-shell microcanonical Liouville preparation, Boltzmann–Grad scaling, short kinetic time, bounded regular sources and regular biased trajectories. External line-by-line review is pending.
