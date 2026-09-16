#!/usr/bin/env python3
"""A2 v72 source preservation and finite algebra checks, not proof certification."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import sympy as sp
from source_provenance import INPUT, blob_id, require, safe_relative, strip_comments
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'history/v71-review-baseline'
EDITED = {'README.md', 'main.tex', 'rigidity.tex', 'article/00i_main_thesis_v70.tex'}
NEW_INPUTS = {'article/00l_one_law_overview_v72.tex',
              'article/00m_abstract_addition_v72.tex',
              'article/10g_uncalibrated_single_law_v72.tex'}
CORE = ('article/10a_periodic_itinerary_relative_v64.tex',
        'article/10b_periodic_contact_inverse_v65.tex',
        'article/10c_global_curvature_inverse_v66.tex',
        'article/10d_smooth_contact_rigidity_v68.tex',
        'article/10e_sampled_smooth_recovery_v69.tex',
        'article/10f_local_observation_comparison_v71.tex')
ENTRIES = ('main.tex', 'rigidity.tex', 'two_collision.tex')

def old_path(name: str) -> Path:
    return (BASE if name in EDITED else ROOT) / safe_relative(name)

def matches(data: bytes, record: dict) -> bool:
    return (len(data) == record['bytes'] and blob_id(data) == record['git_blob']
            and hashlib.sha256(data).hexdigest() == record['sha256'])

def active(name: str, old: bool = False, found: set[str] | None = None) -> set[str]:
    found = set() if found is None else found
    if name in found:
        return found
    found.add(name)
    p = old_path(name) if old else ROOT / safe_relative(name)
    require(p.is_file() and not p.is_symlink(), 'Missing input: ' + name)
    for child in INPUT.findall(strip_comments(p.read_text())):
        active(child if child.endswith('.tex') else child + '.tex', old, found)
    return found

def conservation(records: dict) -> dict:
    require(len(records) == 929, 'Unexpected v71 inventory')
    changed = []
    for name, rec in records.items():
        p, old = ROOT / name, old_path(name)
        require(p.is_file() and old.is_file(), 'Lost inherited path: ' + name)
        require(matches(old.read_bytes(), rec), 'Changed preserved original: ' + name)
        for q in (p, old):
            require(stat.S_IMODE(q.stat().st_mode) in (int(rec['mode'], 8) & 0o777, 0o444),
                    'Unexpected mode: ' + name)
        if not matches(p.read_bytes(), rec):
            changed.append(name)
    require(set(changed) == EDITED, 'Unexpected edited set: ' + repr(changed))
    for name in CORE:
        require(matches((ROOT / name).read_bytes(), records[name]), 'Core edit: ' + name)
    old = {e: active(e, True) for e in ENTRIES}
    new = {e: active(e) for e in ENTRIES}
    ou, nu = set().union(*old.values()), set().union(*new.values())
    require(len(ou) == 141 and ou <= nu and nu - ou == NEW_INPUTS, 'Active-input regression')
    for e in ENTRIES:
        require(old[e] <= new[e], 'Entry-specific lost input: ' + e)
    intro = 'article/00i_main_thesis_v70.tex'
    rx = r'\\begin\{theorem\}.*?\\end\{theorem\}'
    require(re.findall(rx, (ROOT / intro).read_text(), re.S) ==
            re.findall(rx, old_path(intro).read_text(), re.S), 'Old main statements changed')
    require(not matches((ROOT / CORE[0]).read_bytes() + b'bad', records[CORE[0]]),
            'Corruption negative control')
    require(not ou <= (nu - {CORE[0]}), 'Deleted-input negative control')
    return {'inherited_files': len(records), 'unchanged_in_place': len(records)-len(changed),
            'edited_originals_preserved': sorted(changed), 'core_files_byte_exact': list(CORE),
            'old_active_union': len(ou), 'new_active_union': len(nu),
            'new_inputs': sorted(NEW_INPUTS), 'active_by_entry': {e: len(v) for e,v in new.items()},
            'old_lead_theorem_statements_unchanged': True,
            'review_commit': '7bb8971f6b792894ee961f6fab5c6f68847d373d',
            'reviewed_source': 'b0a0c9a42e61422cdf7c82df3fb80bedc0d105af',
            'reviewed_source_tree': '8549bb0789d5e6cdce8ae12f70ed7c100f81510b'}

def algebra() -> dict:
    # Rational identity checks only; no numerical trajectory model is substituted for a proof.
    u,v,a,d,p,x,y = sp.symbols('u v a d p x y', nonzero=True)
    ratio = d*(d-x-y)/((d-x)*(d-y))
    require(sp.cancel(ratio - (1-x*y/((d-x)*(d-y)))) == 0, 'Rank-one identity')
    checks = 0
    for pp in (sp.Rational(1,3), sp.Rational(-2,5), sp.Rational(4,7)):
        for dd in (sp.Rational(2), sp.Rational(7,3)):
            A = -pp*u + sp.Rational(3,5)*u**2 + sp.Rational(1,7)*u**3
            C = pp*v + sp.Rational(7,8)*v**2 - sp.Rational(2,9)*v**3
            U, V = A/(dd-A), C/(dd-C)
            R = 1-U*V
            k = sp.diff(R,u,v).subs({u:0,v:0})
            require(sp.simplify(k-pp**2/dd**2) == 0, 'Clock identity')
            dh = abs(pp)/sp.sqrt(k)
            require(sp.simplify(dh-dd) == 0, 'Wrong positive clock branch')
            for aa in (sp.Rational(1,50), sp.Rational(-1,60)):
                va = sp.simplify(dd/pp*sp.diff(R,u).subs({u:0,v:aa}))
                ua = sp.simplify(-dd/pp*sp.diff(R,v).subs({u:aa,v:0}))
                require(va != 0 and ua != 0, 'Vanishing test anchor')
                Uh = sp.cancel((1-R.subs(v,aa))/va)
                Vh = sp.cancel((1-R.subs(u,aa))/ua)
                require(sp.cancel(dd*Uh/(1+Uh)-A) == 0, 'Future action recovery')
                require(sp.cancel(dd*Vh/(1+Vh)-C) == 0, 'Past action recovery')
                bm, bp = 1+u/9+u**2, 1-v/11+v**2
                require(sp.cancel(bm*(dd-A)/dd*(1+Uh)-bm) == 0, 'Left amplitude')
                require(sp.cancel(bp*(dd-C)/dd*(1+Vh)-bp) == 0, 'Right amplitude')
                require(sp.cancel(dd*(-Uh)/(1-Uh)-A) != 0, 'Sign-error negative control')
                checks += 1
    # The factorization is invariant under an arbitrary overall normalization and endpoint factors.
    z,bm,bp,bm0,bp0 = sp.symbols('z bm bp bm0 bp0', nonzero=True)
    rr = ((z*bm*bp*(d-x-y))*(z*bm0*bp0*d) /
          ((z*bm*bp0*(d-x))*(z*bm0*bp*(d-y))))
    require(sp.cancel(rr-ratio) == 0, 'Normalization/amplitude cancellation')
    # Normal-incidence boundary of the new formula; no no-go theorem is inferred.
    require((p**2/d**2).subs(p,0) == 0, 'Normal-incidence control')
    alpha,omega,Gamma = sp.symbols('alpha omega Gamma', positive=True)
    beta = alpha*omega/(omega+alpha*Gamma)
    require(sp.simplify(alpha*(1-alpha*Gamma/(omega+alpha*Gamma))-beta)==0,
            'Charged exponent balance')
    return {'signed_rational_cases': checks, 'rank_one_identity': True,
            'unknown_positive_offset': True, 'unequal_cubic_actions': True,
            'nonconstant_amplitudes': True, 'normalization_cancellation': True,
            'signed_anchor_negative_controls': checks, 'zero_momentum_control': True,
            'charged_exponent_balance': True,
            'scope': 'Finite algebra, not nonlinear billiard or statistical proof certification'}

def authentic_previous(records: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix='a2-v71-authentic-') as tmp:
        root = Path(tmp)
        for name, rec in records.items():
            p = root / safe_relative(name)
            p.parent.mkdir(parents=True, exist_ok=True)
            b = old_path(name).read_bytes()
            require(matches(b,rec), 'Invalid historical reconstruction')
            p.write_bytes(b); p.chmod(int(rec['mode'],8)&0o777)
        cmd = [sys.executable,'-B'] + (['-O'] if sys.flags.optimize else [])
        cp = subprocess.run(cmd+[str(root/'tools/check_revision_v71.py')], cwd=root,
                            capture_output=True,text=True,check=False)
        require(cp.returncode == 0, 'Historical v71 check failed: '+cp.stderr)
        result = json.loads(cp.stdout)
    return {'scope': 'Unchanged v71 checker on exact reconstructed v71 bytes and modes',
            'result': result}

def main() -> None:
    records = json.loads((BASE/'SOURCE_MANIFEST.json').read_text())['files']
    print(json.dumps({'scope': 'Author-side source and finite controls; not mathematical certification',
                      'source': conservation(records), 'algebra': algebra(),
                      'authentic_v71': authentic_previous(records)}, indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
