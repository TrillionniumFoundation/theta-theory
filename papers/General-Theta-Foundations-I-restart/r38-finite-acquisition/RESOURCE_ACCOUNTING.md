# Resource accounting

| Resource | Native model / certificate | Not free |
|---|---|---|
| Raw calls | core hidden uniform audit: pathwise maximum N=n+2; mean report count (n+1)/2 | preparation and final audit counted |
| Extended calls | post-control bit extension: N=n+3 | bit prepared only after all core controls stop, paid hold/audit interface |
| Persistent observer state | at most M labels, one table; no separate erasure label, phase counter or posterior register | retained randomness/auxiliary dynamic state would enlarge M |
| Persistent label bits | ceil(log2 M) | not equal to total implementation bits |
| Read-only program | O(M d log(1/sigma)+M |A| log Q+M d p_out), plus primitive/grid code | mathematical real constants not finite bit strings |
| Workspace | W_primitive(p)+O(d p+log M+|A| log Q) for declared interpreter | offline integration/enumeration and report evaluation have separate work costs |
| Calibration/readout precision | weighted squared error delta_out^2 under actual invariant label masses | tiny masses are handled by mass-weighted allowance before division |
| Numerical per-call discrepancy | b tau/gamma in joint ensemble, gamma independent M | requires positive mass-preserving executed maps and same physical task |
| External clock | hidden T uniform 1..n, separate ceil(log2 n) counter and sampling resources | not available to observer, no exact internal stopping theorem implied |
| Physical time | sum of primitive calls, report processing, observer steps and task hold/audit | neither n nor M alone measures it |
| Simulator | R internal labels with target M -> at most R M; calls/time compose | one-way simulator has no reverse lower implication |
| Extended bit task | running m core labels plus three response copies, <=4m+2 labels | sufficient construction, no minimal-state claim |
| Marked acquired strata | finite visible mark incorporated into labels, per-stratum grids | true w_j and any rare access word probability retained |

The new uniform gap removes the extra erasure-induced amplification: to preserve M^(-2/d) risk, ensemble tolerance of order M^(-2/d) suffices, with certificate-dependent constants. The theorem does not give matching lower bounds on program size, workspace, clock hardware, synthesis time or minimal simulator states.
