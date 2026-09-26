"""Preserve both numbered v169 replies and add separately identified v170 responses."""
from __future__ import annotations
import re, shutil
from pathlib import Path
SECOND={
1:'Theorem `thm:ramified-boundary-v170` distinguishes the integral Hilbert graph Y, its normalization Z, and the parameter fibre F. They are not identified with the raw list of maximal minors.',
3:'No new bound is obtained by relabelling raw content. The sharp marked-family bound from v169 is retained. The new normalized root label is additional information, not something recoverable from a Hilbert point alone; see `cor:hilbert-lifts-v170`.',
4:'The rays, conductor, fibre lengths, residue degrees, and cyclic quotient charts in `thm:ramified-boundary-v170` are independent of m. In contrast, the exponents E_j still occur in the graded Rees algebra `eq:ramified-rees-v170` and are not declared degree-independent.',
5:'Proposition `prop:ramified-rees-v170` computes the integral closure in every Rees degree after every diagonal coefficient cover, including unequal powers. The raw algebra need not be normal; it is not silently equated with its integral closure. A full-B_a closure formula remains outside this theorem.',
6:'For all a,rho,sigma, the primitive Rees valuations are (i sigma/g_i,rho/g_i), with g_i=gcd(rho,i sigma). Their ramification indices and residue degrees are respectively rho sigma/g_i and g_i. See `prop:ramified-rees-v170` and `eq:root-residue-v170`.',
9:'Proposition `prop:log-compatibility-v170` adds coherent root-cover comparison and gluing under units on two marked Cartier boundaries. It does not assert that arbitrary unmarked coordinate changes preserve this fan; the larger fixed-degree equivariance remains the separate v169 theorem.',
10:'The distinction is maintained. None of the new conductor, normality, parameter-fibre, or root-label formulas uses the raw minor order.',
12:'The new normalization is specified by a two-dimensional fan and the finite inequalities in `eq:ramified-rees-v170`, rather than a larger matrix. The conductor is a divisorial ideal with explicit orders; all crossing conditions are settled by `lem:conductor-depth-v170`.',
13:'The universal curve on Z is the flat pullback of the same low-degree monic family. Parameter normalization does not normalize its embedded curve fibres; their original ideals and punctual modules remain in the manuscript.',
19:'The root-label statement `cor:hilbert-lifts-v170` applies to arbitrary DVR arcs in the stated marked family with positive u,v orders, not merely exact monomial coefficient arcs. It is not promoted to a classification of arbitrary arcs in B_a.',
21:'Successive monomial root maps are now treated geometrically: normalizing the iterated pullback canonically gives Z_(a,rho r,sigma s), with associative comparison maps. The marked-unit gluing is proved in `prop:log-compatibility-v170`.',
22:'The bend loci of the functions min(rho p,j sigma q) give the minimal marked normal fan. Its root residues contain information beyond those valuations. This does not identify it with the tropical Grassmannian or an intrinsic fan of all coefficient charts.',
24:'Every bend ray is required for simultaneous principalization, and the inherited wall curves identify the corresponding Hilbert degeneration. No redundant hyperplane refinement is inserted. See `prop:log-compatibility-v170`.',
25:'Example `ex:third-ramified-v170` has rays (3,2),(3,1),(9,2), four explicit cyclic quotient indices, and a nonreduced parameter fibre. The theorem proves these formulas for all contact orders and all powers; the order-three instance is only an illustration.',
26:'Theorem `thm:ramified-boundary-v170` gives all a components, generic lengths, node adjacencies of the reduced fibre, and no embedded associated points after arbitrary ramification. The open residue strata are G_m with finite power maps of degree g_i; their endpoints and lifts are explicit.',
28:'This is a substantive change relative to v169: `cor:hilbert-lifts-v170` exhibits g_i different normalization points with identical retained coefficients and identical embedded Hilbert limit. Every root label is realized by an arc; at torus-fixed boundary points the lift is unique.',
29:'Embedded equality still does not imply target-automorphism or abstract isomorphism classification. The new corollary additionally separates embedded equality from equality on the normalization.',
30:'The inherited target-action criterion is unchanged. The new root labels cannot be distinguished by any invariant of the embedded curve alone, since their embedded curves are literally equal at the same coefficient centre.',
32:'The transformed Newton polygon has primitive normals (i sigma/g_i,rho/g_i). Its supporting inequalities give all normalized Rees degrees in `prop:ramified-rees-v170`.',
33:'Equation `eq:ramified-rees-v170` and chart formula `eq:normal-chart-v170` explicitly compute the normalized algebra and all overlaps for arbitrary covers. Unlike the unramified case, normality is not asserted for the raw Rees algebra.',
34:'Proposition `prop:ramified-singularities-v170` adds all cyclic chart class groups, axis divisors, rational intersection numbers, and relative canonical coefficients. These are Weil/Q-Cartier statements where appropriate, not an unsupported Cartier Picard assertion on a singular surface.',
35:'The inherited unramified contractions remain. The normalized fan supplies toric contraction maps by coarsening; the new minimality statement concerns simultaneous principalization of the marked ideals, not a claim that every contraction is smooth.',
36:'The same universal curve is pulled back, so the earlier Quot and cycle comparisons remain valid. Distinct normalization root labels above one Hilbert point are an additional loss of parameter information, separate from loss of a punctual curve nilradical.',
37:'The order-three unequal-cover example is completely specified by the general theorem. Its conductor is (2,3,8), fibre lengths (2,1,2), and residue degrees (1,2,1); see `ex:third-ramified-v170`.',
38:'The inherited source-moving orbit family is retained. Marked smooth/etale coefficient charts can additionally carry the root-cover construction, but this does not turn f=(x-alpha)^a into an arbitrary monic-f coefficient slice.',
39:'The inherited invertible target changes remain applicable to the pulled-back universal curves. No arbitrary mixed-coefficient full-neighbourhood classification is claimed.',
40:'The old smooth model has unique lifts. The covers now exhibit genuine multiple normalization lifts, computed on every wall by `eq:root-residue-v170`; crossings still have unique lifts. They must not be confused with different irreducible components of the integral total surface.',
41:'Every normal local chart is the explicit semigroup ring `eq:normal-chart-v170`. The raw charts `eq:raw-cover-charts-v170` are hypersurfaces or complete intersections; their conductor has no further isolated condition at the crossing. Equal powers give explicit principal conductor generators in `cor:equal-power-v170`.',
42:'Proposition `prop:log-compatibility-v170` proves the terminal normal principalization property for the marked ideal system and compatible root covers. It extends to two specified transverse Cartier divisors; it is not an unmarked all-pencil modular universal property.',
43:'The new complete fibre theorem is for every ramified marked family and includes a=3. It does not compute the entire full-B_3 fibre. That distinction remains explicit in the theorem, abstract, and review entry, rather than being counted as closure of this broader request.',
44:'For the ramified marked parameter fibre, the exact answer is a one-dimensional components, all P1 after reduction, with chain incidences and lengths min(rho,i sigma)/g_i. This is proved scheme-theoretically, not asserted as the component list of the full B_3 fibre.',
45:'The parameter-fibre nilradical now has exact order max_i min(rho,i sigma)/g_i and no embedded associated points (`lem:coordinate-ideal-v170`). The separate punctual nilradical of the embedded universal curves remains as computed in v169. These two statements concern different rings.',
46:'All normalization charts, branch power maps, and crossings of the marked ramified graph are computed; the global conductor records the gluing defect. This is a new example of nontrivial normalization branches, not a full-B_3 branch classification.',
47:'The contact order a is unchanged by coefficient ramification. The extra integers rho,sigma specify the family direction and are not recoverable from the Smith exponent alone. The new formulas retain this data explicitly.',
48:'The all-order ramified corank-two construction is not a higher-corank Hilbert-fibre theorem. The existing higher-corank inverse data are preserved without claiming they supply a missing adjugate graph.',
49:'No arbitrary singular-Kronecker Hilbert fibre is asserted. Existing singular-pencil mathematics remains intact; the new graph is the nonzero marked rational-map family explicitly stated in the theorem.',
50:'Root-cover compatibility preserves one generic Hilbert polynomial throughout. It does not evade the constancy obstruction for different unaugmented degrees proved in `prop:conservation-v169`.',
51:'The new global result is the normalized marked root-cover model with proved overlaps and conductor gluing. It is not named a compactification of all pencil strata.',
52:'The new marked boundary complex is the path on D_1,...,D_a with explicit multiplicities, cyclic cone indices, and root maps. Its compatibility under marked units and root covers is proved. No canonical complex for all unmarked Kronecker strata is inferred.',
53:'The inherited fixed-target complete-quadric comparison remains a specified-family application. The toric root cover acts on coefficients and normalizes parameters, not a different complete-quadric target.',
54:'The v169 full-degree equivariance is retained. The additional marked logarithmic construction is invariant under changes of boundary trivializations and admits associative root-cover maps; its smaller symmetry category is stated.',
55:'The new boundary theorem and `cor:toric-fibres-v170` do not use Paper I. The effective failure-family application still uses reconstruction first, with its original hypotheses.',
56:'No internal operator on an isolated finite algebra has been added or claimed. Root exponents and arc residues are data of the specified coefficient family.',
57:'An external independent full audit has not been obtained. All 465 predecessor mathematical blocks are preserved; the new checks and proof-dependency map are not substituted for that audit.',
58:'The permanent narrowing of historical claims is retained in both papers. The new primary-source record does not claim to have obtained the missing Ballico original text.',
59:'The record now adds theorem-level comparisons with semigroup normalization/monomial blow-ups (Gonzalez Perez--Teissier, Proposition 5 and Section 2.6), toric cover ramification (Alexeev--Pardini, Definition 1 and Lemma 1), and the Stacks blow-up/normalization lemmas. Only consulted sources are described as consulted.',
60:'The introduction expressly treats semigroup normalization and the toric-cover lattice rule as classical. The complete parameter-fibre ideal, global conductor through crossings, and Hilbert-root identifications are proved calculations for the stated family, not claimed new representability machinery.',
61:'The full prior mathematical bodies remain in the papers and preservation master; the new front matter is centred on one ramified-boundary theorem. No existing content is deleted, and the master remains an audit object rather than a third submission.',
62:'The new proof route is chain model -> normalized Rees fan -> divisorial coordinate ideal -> complete parameter fibre; and raw lci charts -> binomial conductor -> depth lemma -> global conductor. Root-lift and logarithmic consequences then follow. `THEOREM_DEPENDENCIES_V170.md` makes both routes explicit.',
63:'The new checks use exact semigroup membership, finite normalization-module representatives, binomial gap counts, lattice indices, intersection identities, and root-cover composition. They are auxiliary finite regressions; the proofs of the general statements are in the manuscript.',
64:'Corollary `cor:toric-fibres-v170` gives the entire origin fibre of any normal toric surface modification of A2, with no reconstruction input. The new result is not advertised as solving a recognized named open problem.',
65:'Paper I proves reconstruction. The new main boundary theorem is independent of it and belongs to Paper II; the final effective-family interpretation is the only link requiring the inverse. The master preserves both, not a claimed indivisible top-four theorem.',
66:'The advance relative to full v169 is the all-order ramified normalization, complete parameter fibre, conductor across every crossing, and all lost root labels with compatible root-cover maps. It is not merely another order-three chart or a larger test count. Its significance remains for mathematical referees to evaluate; no acceptance claim is made.'}
FIRST={
9:SECOND[28],11:SECOND[5],12:SECOND[12],16:SECOND[10],18:SECOND[21],19:'The theorem is stated over an algebraically closed field of characteristic zero. The geometric root counts use that hypothesis; residue-field extensions at generic boundary points are explicitly computed, not silently replaced by k.',
28:SECOND[28],29:SECOND[13],31:SECOND[24],32:SECOND[9],33:SECOND[26],34:'The wall strata remain algebraic G_m families. Root covers now have a precise finite power-map identification on each family; this is not a finite classification of all automorphism types.',
36:SECOND[42],38:SECOND[45],40:SECOND[6],41:SECOND[28],42:SECOND[33],43:SECOND[34],44:SECOND[43],45:SECOND[37],46:'The coefficient map b=u^rho,c=v^sigma is finite flat. Thus the full base change Y is already the Hilbert graph; no vertical component is removed. Its normalization Z is a separate finite operation with explicitly computed conductor.',47:SECOND[42],48:SECOND[42],49:'No finite-type inverse limit of all possible refinements is asserted. The theorem gives a terminal normalized principalization for one finite marked ideal system and associative comparisons for its specified root covers.',
50:SECOND[45],51:'The inherited local Ext/nilradical distinction remains. The new conductor ideal and parameter-fibre nilradical are also kept separate from the square-zero obstruction sheaf and the embedded-curve genus-correction module.',52:SECOND[34],53:SECOND[34],54:SECOND[13],55:SECOND[62],56:SECOND[61],57:SECOND[59],58:SECOND[36],59:SECOND[43],60:SECOND[44],61:SECOND[57],62:SECOND[58],63:SECOND[63],64:'The replies explicitly separate new v170 results, retained v169 results, and requests not completed. The count of 66 replies is not a claim of mathematical closure of every request.',65:SECOND[66],66:'The requested top-four mathematical standard is addressed through explicit hypotheses, complete proofs, a central theorem, and precise publication units. No arbitrary deletion, substitute editorial downgrading, or claim of guaranteed journal acceptance is made.'}

def write_responses(here:Path,prev:Path)->None:
 for which,updates in [('SECOND',SECOND),('FIRST',FIRST)]:
  name=f'RESPONSE_TO_{which}_V167_REPORT.md';old=(prev/name).read_text()
  shutil.copyfile(prev/name,here/('PREVIOUS_'+name.replace('.md','')+'_V169.md'))
  blocks=re.split(r'(?=^### \d+\.)',old,flags=re.M)[1:]
  assert len(blocks)==66
  intro=f'''# A2 v170 response to the {which.lower()} independent v167 report

This response is incremental relative to the **complete v169 manuscript**, commit
`81e0870e31078a3aaac6006b676ca54667e6d77a`. The controlling latest report is the
second v167 report at `f50f6a7b194adbb42813988d3e68a43d71ccc520`; the earlier
report is at `be1987dd1a37064c0bea291d7ad38ccd12cc5951`. Both report texts are
byte-locked in this package. Neither report is falsely described as a review of v169.

The new principal theorem treats **all a>=2 and all coefficient powers rho,sigma>=1**:
normalization of the full pulled-back Hilbert graph, complete parameter-fibre
scheme structure, a global conductor without hidden crossing conditions,
normalization root labels, and coherent marked root-cover comparisons. Its
proofs are in `ramified-boundary-v170.tex` and `conductors-and-lifts-v170.tex`.
The original embedded-curve equations and their punctual modules remain intact.

Each numbered item below first retains the v169 response verbatim, then identifies
what v170 adds or does not add. Earlier work is not relabelled as new work.
All requests have a response; not every full-B_a, higher-corank, or documentary
request has thereby been completed. See `REFEREE_CROSSWALK_V170.md` for actual
compiled theorem/page locators and `THEOREM_DEPENDENCIES_V170.md` for the proof route.

'''
  text=intro
  for number,block in enumerate(blocks,1):
   heading,body=block.split('\n',1)
   text+=heading+'\n\n**Retained v169 response.**\n\n'+body.strip()+'\n\n'
   text+='**v170 amendment.** '+updates.get(number,'The retained response continues to apply. No additional mathematical closure of this request is asserted by the ramified-boundary theorem.')+'\n\n'
  (here/name).write_text(text)
