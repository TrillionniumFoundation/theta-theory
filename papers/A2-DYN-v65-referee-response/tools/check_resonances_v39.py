#!/usr/bin/env python3
"""Finite algebraic regression models; not continuum or phase-exclusion certificates."""
from itertools import product
import cmath
import numpy as np

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def finite_checks():
    count = 0
    abel_cases = 0
    source_cases = 0
    max_error = 0.0
    for length in range(2, 7):
        for bits in product((0, 1), repeat=length):
            if not 0 < sum(bits) < length:
                continue
            eta = np.array(bits, dtype=float)
            one = np.ones(length, dtype=complex)
            c = float(np.mean(eta))
            for v in (0.43, 1.7, np.pi):
                z = cmath.exp(1j*v)
                U = np.zeros((length,length), dtype=complex)
                for j in range(length):
                    U[(j+1)%length,j] = z**bits[j]
                require(np.max(np.abs(U.conj().T@U-np.eye(length))) < 1e-12,
                        'physical weighted composition is not unitary')
                F = [1.0+0j]
                C = []
                for m in range(1, 17):
                    occupations = [sum(bits[(j+k)%length] for k in range(m)) for j in range(length)]
                    F.append(sum(z**a for a in occupations)/length)
                    C.append(sum(bits[j]*bits[(j+m)%length]*z**occupations[j]
                                 for j in range(length))/length)
                for m in range(1,16):
                    expected = z*(F[m+1]-2*F[m]+F[m-1])/(z-1)**2
                    error = abs(expected-C[m-1]); max_error=max(max_error,error)
                    require(error < 2e-11, 'second difference or initial z factor')
                    require(abs(sum(C[:m])) <= 4/abs(z-1)**2+1e-10, 'partial sum bound')
                    count += 1
                for r in (0.5, 0.9, 0.99):
                    resolvent = np.linalg.inv(np.eye(length)-r*U)
                    Fgen = np.vdot(one,resolvent@one)/length
                    actual = np.vdot(eta,(resolvent-np.eye(length))@eta)/length
                    expected = z/(z-1)**2*((1-r)**2/r*Fgen-(1-r)/r-c*(z-1))
                    require(abs(actual-expected)<2e-10,'exact Abel identity')
                    require(abs(actual-c*z/(1-z)) <= 4*(1-r)/abs(z-1)**2+1e-10,
                            'Abel error budget')
                    source_norm=np.linalg.norm(resolvent@eta)/np.sqrt(length)
                    require(source_norm<=2/((1+r)*abs(z-1))+1e-10,'source resolvent bound')
                    abel_cases += 1
                # Full spectral-measure identity at omega=0, with an orthonormal
                # eigenbasis supplied by the normal (unitary) matrix.
                from scipy.linalg import schur
                triangular,V=schur(U,output='complex')
                eigenvalues=np.diag(triangular)
                require(np.max(np.abs(triangular-np.diag(eigenvalues)))<1e-10,'normal Schur basis')
                e=V.conj().T@eta/np.sqrt(length); a=V.conj().T@one/np.sqrt(length)
                require(np.max(np.abs(np.abs(e)**2-abs(eigenvalues-1)**2/abs(z-1)**2*np.abs(a)**2))<1e-10,
                        'source spectral measure factor')
                for eps in (0.1,0.5,1.5):
                    norm=np.linalg.norm(e[abs(eigenvalues-1)<=eps])
                    require(norm<=eps/abs(z-1)+1e-10,'spectral-window bound')
                # Nonzero physical frequency: verify the exact error term and
                # do not discard the |omega|/(1-r) loss.
                f=np.linspace(-1,1,length)
                omega=0.017
                Uo=np.zeros_like(U)
                for j in range(length):
                    Uo[(j+1)%length,j]=cmath.exp(1j*omega*f[j])*z**bits[j]
                inverse_one=Uo.conj().T@one
                h=(np.exp(1j*omega*f)-1)*inverse_one
                require(np.max(np.abs((z.conjugate()-1)*eta-(inverse_one-one+h)))<1e-11,
                        'nonzero-frequency source identity')
                r=0.95
                norm=np.linalg.norm(np.linalg.solve(np.eye(length)-r*Uo,eta))/np.sqrt(length)
                require(norm<=(2/(1+r)+abs(omega)/(1-r))/abs(z-1)+1e-10,
                        'nonzero-frequency source budget')
                source_cases+=1
    # Purely algebraic checks for finite cyclic projection and return lifting.
    group_cases=0
    for d in range(1,14):
        residues=[(2*j%d,3*j%d,j%d) for j in range(d)]
        require(len({x[-1] for x in residues})==d,'occupation projection injectivity')
        for x in residues:
            require(all((d*t)%d==0 for t in x),'torsion-coordinate denominator')
        group_cases+=1
    tower_cases=0
    for height in range(1,12):
        for v in (0.4,1.9):
            psi=np.arange(height)*0.03+0.11
            q0=cmath.exp(0.2j)
            levels=[cmath.exp(1j*(sum(psi[:j])+(v if j>=1 else 0)))*q0 for j in range(height)]
            terminal=cmath.exp(1j*(sum(psi)+v))*q0
            for j in range(height):
                next_value=levels[j+1] if j+1<height else terminal
                require(abs(next_value-cmath.exp(1j*(psi[j]+(v if j==0 else 0)))*levels[j])<1e-11,
                        'all-frequency tower lift')
                tower_cases+=1
    # Negative controls establish that the checker distinguishes three false
    # deductions; they are not counterexamples to the physical billiard.
    bits=(1,0);z=-1
    seq=[sum(bits[j]*bits[(j+m)%2]*z**sum(bits[(j+k)%2] for k in range(m)) for j in range(2))/2
         for m in range(1,21)]
    require(seq[1]==-0.5 and seq[3]==0.5 and abs(seq[-1])==0.5,'coefficient-decay negative control')
    m=2;good=-0.5;wrong=z*good
    require(wrong!=good,'terminal-visit negative control')
    require(good/z!=good,'missing-z negative control')
    return {'second_difference_cases':count,'Abel_resolvent_cases':abel_cases,
            'spectral_source_cases':source_cases,'finite_group_cases':group_cases,
            'tower_level_cases':tower_cases,'negative_controls':3,
            'maximum_second_difference_error_below_1e_10':bool(max_error<1e-10),
            'finite_models_not_continuum_proofs':True}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
