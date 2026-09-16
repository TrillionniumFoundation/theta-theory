from pathlib import Path
import re, json, hashlib
p=Path(__file__).resolve().parent.parent
BASE_BLOBS={'main.tex':'0bfeb7170725c7359545bf12ef3368c7c0ddf5f6', 'rigidity.tex':'255e35bda3375ad1b39bec84c1cd9f2d27c13c09'}
def blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if blob((p/'journal/00_principal_introduction_v56.tex').read_bytes())!='894053803abbe5cbcdcab1ef1f04c35257fb89dc':
 raise RuntimeError('The frozen introduction changed')
old=(p/'journal/00_principal_introduction_v56.tex').read_text()
opening=r'''\section{Introduction}
\label{sec:v56-introduction}

A long alternating billiard bridge has two different geometric scales.
Its middle approaches a hyperbolic two-periodic orbit, whereas its
transverse endpoints remain in a fixed contact collar.  Does conditioning
on this increasingly rare event retain the nonlinear geometry of the
reflecting boundaries, or only their contact Hessians?  We prove that it
retains the two signed half-line actions and that these actions determine
every finite contact jet.  For analytic periodic tables, a finite selected
set of marked channels then determines complete obstacle images and the
unknown marked lattice, with finite ambiguity in the noncircular class
and uniqueness in the properly asymmetric class.

The offset and the flight number play different roles.  We let the number
of flights tend to infinity at a \emph{fixed positive excess time}; we do
not replace that positive-offset law by its leading small-offset term.
The unconditioned mass decays exponentially.  The normalized law,
however, retains a nonlinear endpoint interaction on a collar independent
of flight number.  Thus a long-flight limit is not a quadratic truncation.
The separation is realized by actual periodic tables: an analytic family
has the same gap, free area, contact curvatures, and leading endpoint
metrics and count amplitudes at every flight number, but different
nonlinear limiting laws.  Its construction and its nonzero response are
proved in Theorem~\ref{thm:v4-jet-fiber}.

There are two analytical steps.  First, one must control the physical
mixed derivative relative to an exponentially small reference twist.
An absolute estimate for the stationary action cannot do this.  An exact
cofactor identity followed by a two-ended trace-class comparison produces
the relative limit before conditioning and before offset differentiation.
Second, one must show that the action jet is a function of the actual
boundary jet, independent of arbitrary smooth remainders.  A finite
stationary-envelope identity, with its terminal term retained until it
vanishes, proves this factorization.  The resulting signed inverse has a
determinant-one block at every order, without reflection symmetry or
equal contact curvatures.  These are the two uses of the boundary-layer
construction on which the reconstruction rests.

'''
s=opening+old[old.index('\\subsection{The local relative and smooth inverse mechanism}'):]
s=s.replace('The estimates have different roles.  To prove the relative estimate one', '\\subsection{Why the relative estimate is the relevant limit}\n\nThe estimates have different roles.  To prove the relative estimate one',1)
needle='The geometric parameter restriction also identifies where an\nall-order conditioning issue can occur.'
insert=r'''The distinction can be stated directly at the level of the observation.
On a fixed positive interior square, integrating out the residual time
and normalizing gives
\[
 f_{j,b,d}(u,v)=
 \frac{b_{j,b}(u,v)\{d-E_{j,b}(u,v)\}}
 {\int (d-E_{j,b})_+b_{j,b}}.
\]
The exponentially small reference twist cancels from this quotient.
That cancellation is useful only after $b_{j,b}$, not merely $E_{j,b}$,
has been controlled.  The relative estimate supplies the amplitude and
normalization bounds needed for the positive-offset limit.  In particular,
Corollary~\ref{cor:v26-finite-flight-inverse} gives, at each fixed order
$M$, the geometric error $C_M(\tau^j+\epsilon+\epsilon_g)$ from a
finite-flight interior $C^M$ density error $\epsilon$ and gap error
$\epsilon_g$.  This connects the relative limit to its inverse without
an assumption of order-uniform real differentiation or a bound on the
number of preparations required to estimate the density.

\subsection{The action as a nonlinear boundary coordinate}

'''
s=s.replace(needle,insert+needle,1)
needle='\n\nThe density algebra has a separate, simpler role.'
s=s.replace(needle,r'''

The analytic inverse is another consequence of the stationary envelope,
not a consequence of the determinant of each finite block alone.
The scalar restriction estimate and the interior interpolation used in
the real-observation theorem have a different role: they transfer that
inverse to a weaker observation topology under stated priors.  They are
not additional mechanisms for reconstructing a billiard boundary.
In particular, the all-order conditional estimate and the fixed-order
finite-flight estimate above answer different questions and retain their
different hypotheses.

The density algebra has a separate, simpler role.''',1)
needle='\n\\input{journal/01_structural_statements_v56}'
insert=r'''

For fixed contact conventions, the sequence of recoveries is therefore
\[
 (g,f_0,f_1)\longmapsto(g,S_0,S_1)
       \longmapsto (j_0^M\psi_0,j_0^M\psi_1),\qquad M\ge2.
\]
The first arrow is an explicit operation on the interaction of the law;
the second is the inverse of a well-defined map on actual smooth jets.
On an analytic inverse neighborhood the second arrow recovers the entire
contact pair.  This formulation does not identify arbitrary smooth germs
with their jets, nor does it assert that every pair of observed densities
is realized by a billiard.  The theorems reconstruct within the specified
physical class.
'''
s=s.replace(needle,insert+needle,1)
needle='The three most direct comparison cases are proved in the article.'
insert=r'''For the leading-data comparison the geometric distinction is explicit.
The area-preserving support family in Theorem~\ref{thm:v4-jet-fiber}
has $g=1$, $A=12-\pi$ and $\kappa_0=\kappa_1=1$, while its
fourth graph derivative is $q_s=3-24s$.  The normalized onset response
satisfies
\[
 \left.\frac{d}{ds}\partial_d\mathcal F^{(s)}(0)\right|_{s=0}
                         =\frac{\sqrt3}{2}.
\]
The full proof computes both the action and determinant contributions;
it does not infer this coefficient from an uncontrolled absolute error.
Independently, the signed action inverse separates the fixed-positive-offset
endpoint laws when the fourth contact jets differ.  The example establishes
strict additional geometric information beyond the leading record.  It
does not compare the information of endpoint laws with that of a marked
length spectrum, and its symmetric realization is not an assumption in
the general signed inverse.

'''
s=s.replace(needle,insert+needle,1)
needle='\\subsection{Relation to earlier inverse problems}'
insert=r'''The periodic conclusion addresses a further question after local
reconstruction.  The recovered obstacle images lie in separate channel
frames, not in one supplied Euclidean frame.  Noncircularity makes the
possible incidence congruences finite; the marked cycle gains then turn
the recovered displacement cochain into the unknown lattice.  Thus the
lattice is an output, not hidden metric information in the channel marks.
The congruence and cochain arguments are consequences of the local
reconstruction, rather than independent substitutes for its analytical
content.  Their complete proofs also show why finite rotational symmetry
and a continuous infinitesimal ambiguity must be distinguished.

'''
s=s.replace(needle,insert+needle,1)
# All inherited labelled mathematical environments are retained byte-for-byte.
for env in ('theorem','proof','equation','align'):
 pat=r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}'
 for b in re.findall(pat,old,flags=re.S):
  if b not in s: raise RuntimeError('lost '+env)
(p/'journal/00_principal_introduction_v61.tex').write_text(s)
# Existing introduction stays in the tree as historical source.
for f in ['main.tex','rigidity.tex']:
 archive=p/'history/v60-review-baseline'/f
 archive.parent.mkdir(parents=True,exist_ok=True)
 data=archive.read_bytes() if archive.exists() else (p/f).read_bytes()
 if blob(data)!=BASE_BLOBS[f]: raise RuntimeError('The frozen entry changed: '+f)
 if not archive.exists(): archive.write_bytes(data)
 a=data.decode('utf-8')
 a=a.replace('revision 60','revision 61').replace('A2 v60.','A2 v61.')
 if f=='rigidity.tex':
  a=a.replace('journal/00_principal_introduction_v56','journal/00_principal_introduction_v61')
  start=a.index('\\begin{abstract}')
  end=a.index('\\end{abstract}',start)
  a=a[:start]+r'''\begin{abstract}
We determine the nonlinear geometry retained by long alternating bridges
in a dispersing billiard.  At a fixed positive excess time, a relative
limit on a flight-independent collar preserves two half-line actions
although the reference twist is exponentially small.  An exact cofactor
normalization and a two-ended trace-class comparison establish this limit.
A finite stationary-envelope argument then identifies the action filtration
for actual smooth boundaries; its signed contact inverse has determinant-one
blocks at every order, with order-uniform bounds under geometric
admissibility.  The gap and two same-type conditional endpoint laws determine
all finite contact jets without supplied curvatures or flux amplitudes.
For analytic contacts, the complete action map has a local analytic inverse,
and a local analytic prior yields conditional H\"older stability for complete
contact germs on a smaller disc from real density error.
For noncircular analytic periodic tables, selected marked channels determine
finitely many complete realizations, including the unknown marked lattice;
proper asymmetry gives uniqueness.  Reconstruction remains valid on visible
interior windows with unknown transverse origins and separate positive
recording factors.  The differential has precisely the common Euclidean
kernel, and immersed finite-dimensional models admit finite observable
coordinates.  Realized comparisons separate nonlinear information from
leading endpoint data, finite matching ambiguity, and continuous symmetry.
''' + a[end:]
 else:
  a=a.replace('We reconstruct the signed contact jets of a dispersing billiard channel',
              'We determine the nonlinear geometry retained by long alternating bridges.\nWe reconstruct the signed contact jets of a dispersing billiard channel',1)
 (p/f).write_text(a)
print(json.dumps({'revision':61,'principal_introduction_lines':len(s.splitlines()),'inherited_intro_environments_retained':True,'new_theorems':0},sort_keys=True))
