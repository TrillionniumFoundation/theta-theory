"""Verbatim finite_block_row from reviewed v12 tools/verify_v12.py.
Source blob: 8275ed32e19929d05a7c75125a88e9b69b871fad.
Only its standard-library import and two scalar helpers are included.
"""
from fractions import Fraction as F
import math

def sh(l,k):return (l**(-k)-l**k)/2
def ch(l,k):return (l**(-k)+l**k)/2

def finite_block_row(l,r,g,m,j,b):
    """Finite Dirichlet Green diagonal + full ellipse moments.
    This route sums both endpoint influence vectors before integrating;
    it does not insert the limiting half-line action/amplitude formulas.
    The output is the derivative of the finite same-type law coefficient.
    """
    a=[r*sh(l,1)/g,sh(l,1)/(r*g)]
    rb=r if b==0 else 1/r
    shj=sh(l,j);cj=ch(l,j)/shj
    action=[F(0),F(0)];determinant=[F(0),F(0)]
    for i in range(j+1):
        typ=(b+i)%2;ratio=F(1) if i%2==0 else rb
        left=ratio*sh(l,j-i)/shj;right=ratio*sh(l,i)/shj
        # Variance under the inverse endpoint Hessian.
        nu=(cj*(left*left+right*right)+2*left*right/shj)/a[b]
        action[typ]+=(1 if i in (0,j) else 2)*nu**m
        if i not in(0,j):
            G=(1-l**(2*i))*(1-l**(2*(j-i)))/(2*a[typ]*(1-l**(2*j)))
            determinant[typ]+=G*nu**(m-1)
    A=F(2,2**m*(m+1)*math.factorial(m)**2)
    B=F(4,2**(m-1)*m*(m+1)*math.factorial(m-1)**2)
    return [-A*x-B*y for x,y in zip(action,determinant)]
