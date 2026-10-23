from pathlib import Path
p=Path(__file__).parent/'46-mean-contrast.tex'
s=p.read_text()
pre=s[:s.index('\\begin{theorem}[Sharp coefficient synthesis')]
matstatement=s[s.index('Let $n\\ge5$, $P=I-J/n$'):s.index('For the group response, let')]
groupstatement=s[s.index('For the group response, let'):s.index('For $0<p\\le p_0$ and $a=F_n(p)$, all minimum')]
rigiditystatement=s[s.index('For $0<p\\le p_0$ and $a=F_n(p)$, all minimum'):s.index('\\end{theorem}',s.index('For $0<p\\le p_0$ and $a=F_n(p)$, all minimum'))]
rigiditystatement=rigiditystatement.replace('all minimum permutation-core\nfactorizations, up to orbit and simultaneous natural-coordinate\nrelabeling, are','all width-$n-1$ factorizations in (ii), up to factor and simultaneous\ncoordinate relabeling, are')
rigiditystatement=rigiditystatement.replace('all minimum permutation-core factorizations have exactly the form','all width-$n-1$ factorizations in (ii) have exactly the form')
rigiditystatement=rigiditystatement[:rigiditystatement.index('At $p=p_0$ these classifications agree.')]+'''At $p=p_0$ these classifications agree. In the middle interval the
coefficient pair $(A,u)$ itself is unique up to simultaneous coordinate
permutation; the proof gives it explicitly.
'''
groupproof=s[s.index('It suffices to treat $a>0$'):s.index('Suppose a realization on $n-1$ natural orbits exists.')]
groupcoefficient=s[s.index('Suppose a realization on $n-1$ natural orbits exists.'):s.index('More generally, start with any')]
groupcoefficient=groupcoefficient.replace('$\\operatorname{rank}[A\\ \\ u]<n$. ', '$\\operatorname{rank}[A\\ \\ u]<n$.\n')
converse=s[s.index('A nonzero common left null vector $v$'):s.index('We give matching constructions at that boundary.')]
construct=s[s.index('We give matching constructions at that boundary.'):s.index('The retained pure-start formula gives')]
construct=construct.replace('attainment at $F_n(p)$, and hence the exact core law. The same','attainment at $F_n(p)$. The same')
rigproof=s[s.index('For the first rigidity statement, the equality case'):s.index('\\end{proof}',s.index('For the first rigidity statement, the equality case'))]
physical=s[s.index('\\paragraph{Physical realization and scope.}'):]
mathead='''\\begin{theorem}[Sharp synthesis for bounded centered coefficients]
\\label{thm:r76-bounded-coefficients}
'''
matproof='''\\begin{proof}
Start with any matrix pair in (i); no positive factorization is assumed
in the converse. Put $B=u\\mathbf1^{\\mathsf T}-A\\ge0$.
'''+converse+construct+'\n'+rigproof+'''\\end{proof}

'''
newgroupstatement=groupstatement.replace('For the group response, let $(p,a)$ satisfy','Let $n\\ge5$ and let $(p,a)$ satisfy')
newgroupstatement+='''At the nontrivial boundary $a=F_n(p)$ with $0<p\\le2/n$, all
minimum permutation-core factorizations are exactly those in
\\eqref{eq:r76-low-mean-rigidity} and \\eqref{eq:r76-middle-rigidity}.
For negative contrast, exchange the two output labels. This classifies
minimum permutation cores, without asserting uniqueness of every
unreduced stochastic machine.
'''
newgroupproof='''\\begin{proof}
'''+groupproof+groupcoefficient+'''The matrix criterion in
Theorem~\\ref{thm:r76-bounded-coefficients} is therefore necessary.
Conversely its width-$n-1$ positive factorizations give exactly
$n-1$ natural-orbit preparations and valid binary decoders.
Their coefficient identities imply the required response for every
permutation. Hence a core below $n^2$ exists exactly when $a\\le F_n(p)$,
and then the module lower bound makes its size $n(n-1)$.
The retained pure-start formula gives $m=\\min\\{n!,1+\\kappa\\}$,
which equals $1+\\kappa$ because $n^2+1<n!$ for $n\\ge5$.
At $a=0$ the constant decoder uses one state. Every minimum core on the
nontrivial boundary consists of $n-1$ natural orbits, so the factor
classification follows from the matrix theorem.
\\end{proof}

'''
p.write_text(pre+mathead+matstatement+rigiditystatement+'\\end{theorem}\n'+matproof+'\\begin{corollary}[Exact memory throughout the mean--contrast plane]\n\\label{thm:r76-mean-contrast}\n'+newgroupstatement+'\\end{corollary}\n'+newgroupproof+physical)
