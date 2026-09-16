#!/usr/bin/env python3
"""Independent finite checks for A2 v64, not proofs of the infinite-dimensional limits.
Requires NumPy and SciPy; imports no author code and uses no removable assertions.
Exact transfer/continuant identities and finite physical three-disk chains.
"""
from fractions import Fraction as F
from functools import lru_cache
import json, math
import numpy as np
from scipy.linalg import solve_banded

def require(ok, text):
    if not ok: raise RuntimeError(text)

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def exact_reference():
    count=0; wrong_order=0; wrong_endpoint=0; phase_tests=0
    for P in [2,4,6]:
        for seed in range(1,7):
            ks=[F(2+(i*3+seed)%7,2+(i+seed)%4) for i in range(P)]
            ms=[F(1+(i*2+seed)%5,3+(2*i+seed)%4) for i in range(P)]
            traces=[]
            for b in range(P):
                qs=[];M=[[F(1),F(0)],[F(0),F(1)]]
                for i in range(P):
                    k,m=ks[(b+i)%P],ms[(b+i)%P]
                    Q=[[1+m/k,1/k],[m,F(1)]];qs.append(Q);M=mul(Q,M)
                tr=M[0][0]+M[1][1];traces.append(tr)
                require(M[0][0]*M[1][1]-M[0][1]*M[1][0]==1 and tr>2,'Monodromy')
                power=[[F(1),F(0)],[F(0),F(1)]];prev=F(0);U=F(1)
                for n in range(1,5):
                    power=mul(M,power);N=n*P
                    k=[ks[(b+i)%P] for i in range(N)];m=[ms[(b+i)%P] for i in range(N+1)]
                    # Determinant of Dirichlet interior Hessian by continuants, independently of transfer.
                    d0=F(1);d1=k[0]+k[1]+m[1]
                    for j in range(2,N):d0,d1=d1,(k[j-1]+k[j]+m[j])*d1-k[j-1]**2*d0
                    D=math.prod(k)/d1
                    require(D==1/power[0][1],'Dirichlet cofactor / transfer disagreement')
                    require(power[0][1]==M[0][1]*U,'Chebyshev power identity')
                    prev,U=U,tr*U-prev
                    # Endpoint derivative: use u=2/7,v=-1/5, transfer to x1.
                    u,v=F(2,7),F(-1,5);z=(v-power[0][0]*u)/power[0][1]
                    x1=(1+m[0]/k[0])*u+z/k[0]
                    left=k[0]*(u-x1)+m[0]*u/2
                    require(left==-z-m[0]*u/2,'Endpoint half mass')
                    require(left!=-z,'Missing endpoint half mass not detected');wrong_endpoint+=1
                    if n==1:
                        rev=[[F(1),F(0)],[F(0),F(1)]]
                        for Q in qs: rev=mul(rev,Q)
                        if rev[0][1]!=M[0][1]:wrong_order+=1
                    count+=1
            require(all(t==traces[0] for t in traces),'Phase-dependent trace');phase_tests+=1
    return {'exact_transfer_continuant_cases':count,'phase_trace_tests':phase_tests,
            'half_endpoint_mass_negative_controls':wrong_endpoint,
            'noncommutative_product_order_negative_controls':wrong_order}

class Triangle:
    def __init__(self, scalene):
        a=2.5/math.sqrt(3)-1
        angles=np.arange(3)*2*math.pi/3
        self.q=a*np.column_stack((np.cos(angles),np.sin(angles)))
        self.R=np.ones(3)
        if scalene:
            self.q=self.q*np.array([1.06,.94])+np.array([[.03,-.01],[0,0],[-.02,.04]])
            self.R=np.array([.96,1.04,1.00])
        ahead=np.roll(self.q,-1,axis=0)-self.q;back=np.roll(self.q,1,axis=0)-self.q
        self.length=np.linalg.norm(ahead,axis=1); e=ahead/self.length[:,None]
        n=e+back/np.linalg.norm(back,axis=1)[:,None];self.n=n/np.linalg.norm(n,axis=1)[:,None]
        self.t=np.column_stack((-self.n[:,1],self.n[:,0]));self.c=self.q-self.R[:,None]*self.n
        self.nu=np.sum(self.n*e,axis=1);self.k=1/self.length;self.mass=2/(self.R*self.nu)
        self.p=np.array([(-1.)**i*np.dot(e[i%3],self.t[i%3])/self.nu[i%3] for i in range(6)])
        self.name='scalene' if scalene else 'equilateral'
        require(np.min(self.nu)>0 and np.max(self.nu)<1,'Nongrazing nonnormal condition')
        self.disjoint_margin=min(np.linalg.norm(self.c[i]-self.c[j])-self.R[i]-self.R[j] for i in range(3) for j in range(i))
        require(self.disjoint_margin>0,'Disk overlap')
        self.clearance=[]
        for i in range(3):
            j=(i+1)%3;o=(i+2)%3;v=self.q[j]-self.q[i]
            t=np.clip(np.dot(self.c[o]-self.q[i],v)/np.dot(v,v),0,1)
            self.clearance.append(float(np.linalg.norm(self.c[o]-(self.q[i]+t*v))-self.R[o]))
        require(min(self.clearance)>0,'Blocked third-disk flight')
        self.reflection_error=max(np.linalg.norm(e[i]-((self.q[i]-self.q[(i-1)%3])/self.length[(i-1)%3]+2*self.nu[i]*self.n[i])) for i in range(3))
        require(self.reflection_error<1e-13,'Reflection')

    def curve(self, phases, x):
        types=phases%3;sgn=(-1.)**phases;nu=self.nu[types];R=self.R[types]
        ang=sgn*x/(nu*R);rad=np.cos(ang)[:,None]*self.n[types]+np.sin(ang)[:,None]*self.t[types]
        r=self.c[types]+R[:,None]*rad
        v=(sgn/nu)[:,None]*(-np.sin(ang)[:,None]*self.n[types]+np.cos(ang)[:,None]*self.t[types])
        acc=-rad/(nu*nu*R)[:,None]
        return r,v,acc

    def edges(self,b,x):
        phases=b+np.arange(len(x));r,v,acc=self.curve(phases,x)
        dr=np.diff(r,axis=0);ell=np.linalg.norm(dr,axis=1);e=dr/ell[:,None]
        A=np.sum(e*v[:-1],axis=1);B=np.sum(e*v[1:],axis=1)
        f1=-A;f2=B
        h11=(np.sum(v[:-1]**2,axis=1)-A*A)/ell-np.sum(e*acc[:-1],axis=1)
        h22=(np.sum(v[1:]**2,axis=1)-B*B)/ell+np.sum(e*acc[1:],axis=1)
        h12=-(np.sum(v[:-1]*v[1:],axis=1)-A*B)/ell
        return ell,f1,f2,h11,h22,h12

    def reference(self,b,n):
        M=np.eye(2)
        for i in range(6):
            k,m=self.k[(b+i)%3],self.mass[(b+i)%3]
            M=np.array([[1+m/k,1/k],[m,1.]])@M
        chi=math.acosh(np.trace(M)/2)
        logD=math.log(math.sinh(chi))-math.log(M[0,1])-math.log(math.sinh(n*chi))
        return chi,logD

    @lru_cache(maxsize=None)
    def solve(self,b,n,u,v):
        N=6*n;x=np.zeros(N+1);x[0]=u;x[-1]=v
        for _ in range(25):
            ell,f1,f2,a,d,c=self.edges(b,x);grad=f2[:-1]+f1[1:]
            diag=d[:-1]+a[1:];off=c[1:-1]
            ab=np.zeros((3,N-1));ab[1]=diag;ab[0,1:]=off;ab[2,:-1]=off
            if np.max(np.abs(grad))<8e-14: break
            x[1:-1]-=solve_banded((1,1),ab,grad)
        ell,f1,f2,a,d,c=self.edges(b,x);grad=f2[:-1]+f1[1:];diag=d[:-1]+a[1:];off=c[1:-1]
        require(np.max(np.abs(grad))<5e-12,'Finite chain stationarity')
        require(np.min(diag-np.r_[0,np.abs(off)]-np.r_[np.abs(off),0])>0,'Hessian dominance')
        require(np.max(c)<0,'Twist sign')
        piv=diag.copy()
        for i in range(1,len(piv)):piv[i]-=off[i-1]**2/piv[i-1]
        logtwist=np.log(-c).sum()-np.log(piv).sum()
        chi,logD=self.reference(b,n)
        beta=math.exp(logtwist-logD)
        residual=float(np.sum(ell-self.length[(b+np.arange(N))%3]))
        E=residual+self.p[b%6]*(u-v)
        ab=np.zeros((3,N-1));ab[1]=diag;ab[0,1:]=off;ab[2,:-1]=off
        rhs=np.zeros(N-1);rhs[0]=-c[0];sens=solve_banded((1,1),ab,rhs)
        return {'x':x,'beta':beta,'E':E,'physical_excess':residual,'chi':chi,
                'period_derivative':float(sens[5]) if n>1 else None,
                'stationarity_residual':float(np.max(np.abs(grad)))}

def physical_checks():
    summary=[];hessian_cases=0;gauge_controls=0;relative_records=[];linearizer_errors=[];worst_grad=0.
    for scalene in [False,True]:
        T=Triangle(scalene)
        for b in range(6):
            ell,f1,f2,a,d,c=T.edges(b,np.zeros(7))
            for i in range(6):
                j=(b+i)%3;k=T.k[j]
                require(abs(a[i]-(k+T.mass[j]/2))<1e-12,'Geometric left Hessian')
                require(abs(d[i]-(k+T.mass[(j+1)%3]/2))<1e-12,'Geometric right Hessian')
                require(abs(c[i]+k)<1e-12,'Geometric scaled mixed Hessian')
                require(abs(f1[i]+T.p[(b+i)%6])<1e-12,'Initial momentum')
                require(abs(f2[i]-T.p[(b+i+1)%6])<1e-12,'Final momentum')
                hessian_cases+=1
            for u,v in [(.02,-.015),(-.025,.01)]:
                bm=T.solve(b,8,u,0.)['beta'];bp=T.solve(b,8,0.,v)['beta']
                errs=[]
                for n in [1,2,3,4]:
                    s=T.solve(b,n,u,v);err=abs(s['beta']/(bm*bp)-1);errs.append(err)
                    correct=.1-s['E']+T.p[b]*(u-v);direct=.1-s['physical_excess']
                    require(abs(correct-direct)<1e-12 and correct>0,'Restored physical residual')
                    require(abs((.1-s['E'])-direct)>.005,'Missing momentum negative control')
                    gauge_controls+=1;worst_grad=max(worst_grad,s['stationarity_residual'])
                require(errs[-1]<2e-10,'Two-ended relative factorization finite check')
                relative_records.append({'geometry':T.name,'phase':b,'u':u,'v':v,'n_1_2_3_4_relative_errors':errs})
                s=T.solve(b,8,u,0.);w=float(s['x'][6]);der=s['period_derivative']
                bw=T.solve(b,8,w,0.)['beta'];err=abs(bw*der/(math.exp(-s['chi'])*bm)-1)
                require(err<2e-8,'Stable-return amplitude finite check');linearizer_errors.append(err)
        summary.append({'name':T.name,'flight_lengths':T.length.tolist(),'normal_cosines':T.nu.tolist(),
                        'radii':T.R.tolist(),'disk_disjointness_margin':float(T.disjoint_margin),
                        'third_disk_clearance':T.clearance,'reflection_residual':float(T.reflection_error)})
    return {'geometries':summary,'geometric_hessian_cases':hessian_cases,'restored_gauge_negative_controls':gauge_controls,
            'two_ended_configurations':len(relative_records),'records':relative_records,
            'stable_linearizer_checks':len(linearizer_errors),'max_linearizer_relative_error':max(linearizer_errors),
            'max_stationarity_residual':worst_grad}

if __name__=='__main__':
    print(json.dumps({'scope':'Finite scalar identities and finite three-disk orbit computations only. Not a proof of uniform infinite-chain limits, family derivatives, analytic inversion, or statistical rates.',
                      'imports_author_checker':False,'reference':exact_reference(),'physical':physical_checks()},indent=2,sort_keys=True))
