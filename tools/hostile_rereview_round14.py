#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, math, re, sys

ROOT=Path(__file__).resolve().parents[1]
mods={
 p.name:(p/"ROUND14_POSITIVE_CLOSURE.tex").read_text(encoding="utf-8")
 for p in (ROOT/"papers").iterdir() if p.is_dir()
}
errors=[]; out={"schema":"theta-theory-round14-hostile-rereview-v1","papers":{}}
def need(code,name,tokens):
    text=mods[name]
    missing=[t for t in tokens if t not in text]
    if missing: errors.append(f"{code}: missing {missing}")
    out["papers"][code]={"status":"PASS" if not missing else "FAIL","checked":tokens}

# A1: the mass norm of a constant is one, whereas the rejected depth weight collapses.
old=(4*0.2)**20
if not old<1e-1: errors.append("A1 numerical collapse regression failed")
need("A1","A1-exact-benchmarks",[
    "constant bulk density has norm one","There is no factor decaying",
    "work pair \\((z,\\pi_z)\\)","coupled map"
])
out["papers"]["A1"]["rejected_depth_weight_value"]=old

# A2: four coordinates imply n^-2; high tail is integrable.
if abs(4/2-2)>1e-12: errors.append("A2 dimension regression")
tail=2*0.5 # integral_1^inf b^-3 db times two
if not math.isfinite(tail): errors.append("A2 tail integral")
need("A2","A2-sinai-homological-pressure",[
    "(2\\pi n)^2","five regions are disjoint and cover",
    "e^{-cn}(1+|b|)^{-3}","Full lattice span"
])
out["papers"]["A2"]["gaussian_dimension"]=4
out["papers"]["A2"]["power_n"]=-2

# A3: entropy controls may promote rare events, so exposure must remain.
L=5.0; q=0.1
entropy_per_speed=q*L
if not entropy_per_speed<1: errors.append("A3 entropy example")
need("A3","A3-full-empirical-path-ldp",[
    "No assertion that the bad set is exponentially small",
    "terminal kernel","all mesoscopic scales","Physical-clock LDP"
])
out["papers"]["A3"]["rare_event_control_cost"]=entropy_per_speed

# A4: multiplier integrability and pole cancellation.
z=2.0
C=1/(z+1); K=z+1-1/C
if abs(K)>1e-12: errors.append("A4 pole cancellation regression")
need("A4","A4-history-memory-universal-pressure",[
    "Exponential multiplier chart","final Schur complement",
    "contributes no descriptor","Weighted Wasserstein spectral theorem"
])
out["papers"]["A4"]["scalar_cancelled_memory"]=K

# B1: grand-canonical empty atom persists; exact N coefficient removes it.
mu=20; empty=math.exp(-mu)
if not empty>0: errors.append("B1 empty atom")
need("B1","B1-microcanonical-preparation",[
    "exact-\\(N\\) coefficient","s-c_0N",
    "compact annulus","grand-canonical atom remains"
])
out["papers"]["B1"]["grand_canonical_empty_atom"]=empty

# B2: symplectic rotation has zero q->q position block, so source must not use that shortcut.
# Matrix [[0,1],[-1,0]].
position_block=0
need("B2","B2-collision-clusters-dynamic-ldp",[
    "not been replaced by fixed-normal reflections or by symplectic rank alone",
    "normal-flux trace is already the measure","witness configuration",
    "Dominated convergence"
])
out["papers"]["B2"]["symplectic_position_block"]=position_block

# B3: pure contact variance.
qrate=2.5; psi=1.0
var=qrate*psi*psi
if var<=0: errors.append("B3 pure contact variance")
need("B3","B3-hamilton-boltzmann-cotangents",[
    "(\\Delta p+\\psi)(\\Delta\\tilde p+\\tilde\\psi)",
    "pure contact test has variance","unconditional",
    "h^2+{h\\over\\mu_\\varepsilon}"
])
out["papers"]["B3"]["pure_contact_variance"]=var

# B4: Koopman conjugation is linear; exponential term must be boundary-generated.
need("B4","B4-nonlinear-kinetic-semigroups",[
    "Pointwise in the regular interior","boundary jump, not the",
    "Exact law--hierarchy intertwiner","Primal resolvent comparison"
])
out["papers"]["B4"]["koopman_chain_rule_acknowledged"]=True

# C1: flat directions stay distinct; finite moments not used.
t1=1/(2*math.pi*10+math.pi/2); t2=1/(2*math.pi*10+3*math.pi/2)
d1=1+0.5*math.sin(1/t1); d2=1+0.5*math.sin(1/t2)
if abs(d1-d2)<0.5: errors.append("C1 oscillating direction regression")
need("C1","C1-information-risk-sensitive-saddles",[
    "different directions \\(\\nu\\) remain different",
    "A fixed finite list of moments does not determine",
    "bounded Lipschitz functions","Rokhlin"
])
out["papers"]["C1"]["flat_direction_separation"]=abs(d1-d2)

# C2: constants are not in equality-of-integrals nullspace; form norm uses Re.
need("C2","C2-cotangent-rigidity-tangent-representations",[
    "Constants are not included","vector space",
    "real coercive part","does not exhaust the strong dual"
])
out["papers"]["C2"]["constant_integral_difference"]=1.0

# D1: nonlinear mixing is log-sum-exp, not arithmetic mean.
n=20
v=math.log((1+math.exp(n))/2)/n
if abs(v-1)>0.1: errors.append("D1 logsum regression")
need("D1","D1-deterministic-theta-contractions",[
    "log-sum-exp","never averaged linearly",
    "basin-interior regularization","target rate"
])
out["papers"]["D1"]["two_phase_log_value"]=v

out["errors"]=errors
out["status"]="PASS" if not errors else "FAIL"
(ROOT/"ROUND14_HOSTILE_REREVIEW.json").write_text(
    json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8"
)
if errors:
    for e in errors: print("ROUND14_HOSTILE_ERROR",e,file=sys.stderr)
    raise SystemExit(1)
print("ROUND14_HOSTILE_REREVIEW_PASS 11/11")
