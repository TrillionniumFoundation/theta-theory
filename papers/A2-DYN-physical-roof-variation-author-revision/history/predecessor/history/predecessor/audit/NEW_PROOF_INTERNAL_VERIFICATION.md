# Internal verification of the reconstructed boundary-localization and clearance bodies

## Recovery identity and status

This author-side verification record was reconstructed after workspace maintenance. The former record had SHA-256 bb90dd42e29d94af2ecd829bf750192a2e87831d8db762d6afee0a2f29ecb6cc. Its old byte identity is not claimed here. The former native 304 and 307 identities remain recorded in the recovery comments of those source files and in the pre-maintenance inventory. The new complete proof bodies were independently reread after reconstruction. This is not a new referee report or a human-specialist certification.

The immutable native modules 260--303 were recovered from their original Git blobs and verified against the complete pre-maintenance inventory. The rebuilt 304/307 continue their actual physical disk-word problem. This audit checks their mathematical statements; fresh executable results and compilation belong to the new execution records.

## 304: signs, support, and the cutoff identity

For an internal reference contact, the physical gradient is g_i^Q=v_{i-1}-v_i=-2c_i n_i. The disk support inequality gives n_i dot delta_i <= -|delta_i|^2/(2R), and therefore g_i^Q dot delta_i >= H_i/R. The coordinate minimum condition gives g_i^Y dot delta_i <=0. Since g_i^Q-g_i^Y=e_i-e_{i-1}, the sign in (e_i-e_{i-1}) dot delta_i >= H_i/R is correct, including inactive or interior comparison vertices.

Finite summation by parts against eta_i^2 delta_i gives a negative cutoff-work term and a positive kinetic term on the left. The exact edge identity is e_i dot (delta_{i+1}-delta_i)=(ell_i+tau_i)|e_i|^2/2. With a_i=(eta_i^2+eta_{i+1}^2)/2 and b_i=eta_{i+1}^2-eta_i^2, Young's payment leaves a_i(ell_i+tau_i)|e_i|^2/4. The remaining term is bounded by the stated 1/tau_- coefficient because b_i^2/a_i <=4(eta_{i+1}-eta_i)^2, |average delta|^2 <= (|delta_i|^2+|delta_{i+1}|^2)/2, and ell_i+tau_i>=2tau_-. The case a_i=0 has zero work and needs no division. Endpoint cutoff values vanish.

Every feasible comparison edge, without a minimum assumption, satisfies ell_i<=tau_i+|delta_i|+|delta_{i+1}|<=28/5+4r=187/25=T. This bound does not follow from total action alone; the reconstructed source states the actual geometric reason.

## 304: local coercivity and index coverage

At an anchor, |delta_i|^4<=4r^2 H_i/a. At a nonanchor use the last preceding physical anchor inside the preceding N-flight block. The block supplies a strict internal anchor j with 0<i-j<N. The incoming transverse coordinate telescopes as the sum of its anchor value, ell_l v_l-perp dot e_l, and the physical turning corrections. Cauchy--Schwarz gives the coefficients 3N T and 12N. Each anchor, flight and contact is reused at most N times.

Resolving the disk support inequality into incoming and transverse components gives |delta_i|^4<=8r^2(H_i+b_i^2). Summing anchors separately produces the displayed A_H and A_F. The local argument uses only feasibility of the comparison polygon. During the post-maintenance review, an explicit sentence was requested in the lemma statement so its use in 307 for arbitrary feasible polygons has precisely that scope rather than inheriting the minimum assumption of the surrounding section.

For the depth recurrence, nonempty target S_{k+L+N} implies that the two cutoff layers do not overlap. Their 2L flights involve at most 4L vertex occurrences, with vertex multiplicity at most two. The stated bound 4 sqrt(L S_k) is conservative and valid. On the unit-cutoff interval, contact mass is at most r times the cutoff work and flight mass at most four times that work. The target lies inside the local-coercivity target interval, including a central singleton.

The recurrence constant is C_cut=4(r A_H+4A_F)/tau_-. For d>=4N, k=floor(d/2) and L=d-k-N satisfy L>=1 and L(k+1)>=(d+1)^2/16. The coefficient 64 in the induction is therefore correct. For d<4N, K_tail>=2rC(4N)^3 pays the initial global budget. The energy cutoff without anchor offset gives coefficients 32r sqrt(K_tail)/tau_- and 128 sqrt(K_tail)/tau_-. Empty sums and the single central contact are retained correctly.

## 307: a comparison strip with no omitted obstacle

Intersect each incident disk with the strip of half-width beta_i about the original flight. Their longitudinal projections are disjoint: overlapping projections would produce two disk points at distance at most 2beta_i<tau_-, contrary to fixed disk separation. The intervals contain the original start and end coordinates, so their order is the original flight order.

The comparison segment's middle part is within beta_i of the actual closed reference flight. A left extension is within beta_i of a segment inside the first incident disk, by using the same convex parameter and the intersection at longitudinal coordinate zero; the right extension has the analogous property. Every third disk is at distance at least tau_- from each incident disk. Thus the full segment has clearance at least min(Gamma_i(Q),tau_-)-beta_i. All third centers are included, including centers visited elsewhere in the word. The proof concerns closed segments, not infinite supporting lines, and permits changes of the nearest center and projection foot.

## 307: endpoint support and the shared global budget

Let b_i be the incoming transverse contact coordinate. At an internal contact, |v_i-perp dot delta_i|^2<=2b_i^2+8H_i, so summing beta_i^2 costs at most three copies of internal b_i^2, eight copies of H_i, and the two endpoint transverse terms.

The exact endpoint support gaps give b_0^2<=4r(h_0+E_0) and b_m^2<=4r(h_m+E_m), where E_0+E_m=E_R(Q). Indeed the reference and comparison transverse squares relative to the disk center are each bounded by twice R times their respective support deficits. This controls actual endpoint displacement without an endpoint incidence lower bound.

For nonanchors before the first physical anchor, the telescope starts at endpoint 0 and has no fictitious reflection term there. At most N such indices spend at most 3N b_0^2. Set alpha=(1+3N)/a. Since alpha>=12N, the anchor support payment alpha r sum_anchor h_i and the initial endpoint payment 12Nr h_0 are bounded together by alpha r G. They do not require two copies of that part of the positive gap. The remaining flight and contact terms use sum F_i<=2G and sum H_i<=rG. Hence

sum_internal b_i^2 <= [alpha r+6N^2 T+12N^2r]G+12Nr E.

Combining the endpoint pair, the eight-contact term, and the three transverse copies gives exactly

B_G=3r/a+9Nr/a+18N^2T+36N^2r+12r=167591049,
B_E=36Nr+4r=39809/25.

The local coefficients are B_H=3[(1+3N)/a+12N^2]+8=354045464 and B_F=9N^2T=14870988/25. The theorem's arbitrary-feasible scope is legitimate: G is the nonnegative dual gap for every feasible polygon. Only the later substitution G<=E requires the variational sublevel or a global minimum.

## 307: depth, inactivity, Borel source, and normalization

For d>=2N, the local interval [d-N,m-d+N] contains every target flight. Its contact and flight energies lie at depth at least d-N>=d/2. The factor eight from (d-N)^-3 gives the stated K_perp=(256rB_H+1024B_F)sqrt(K_tail)/tau_-.

At an inactive comparison contact, 2c_i<=|e_i|+|e_{i-1}|. Both adjacent flights occur at depth d_i-1, including a central singleton. The inequality (d_i-1)^-3<=8d_i^-3 for d_i>=2 gives C_inactive^2=512sqrt(K_tail)/tau_-^2. No inverse comparison incidence is used.

For fixed R,m and word, the existence of a bad global minimum depends only on those disks. The exceptional source is therefore a countable union of original physical word cells. No projection over uncountably many minima is used to assert Borel measurability. Its complement supplies the desired conclusion for every minimum.

The small-clearance and small-incidence witnesses are explicit original observables. At the prescribed D_0, clearance widths are at most delta_flux/2, so decreasing slightly larger open widths remains inside the strict valid flux range. The invariant flux is paid by u/R, and the incidence law by u^2. Multiply the entire finite union bound by the original exact event, any 0<=h<=1 and an original roof test before dropping these selectors on the upper side. The conditional section factor c_*^-1 is paid once.

At most two indices have each depth. The tails sum d^-3/2<=2(D-1)^-1/2 and sum d^-3<=1/[2(D-1)^2] yield the exact displayed mass coefficients. The full physical source is included before all suprema. This proves total mass/total variation, not normalized essential roof height, not singular pairing-trace domination, and not the original ordered shortage limit.

Outside the source, active contacts satisfy the exterior specular law with positive incidence. Third-disk clearance together with the two incident-disk conditions proves actual first-hit central trajectories. No omitted endpoint portion is declared physical.

## Result

The reconstructed arguments were independently rechecked for the issues above. The only identified formal issue was to declare the feasible-polygon scope of local coercivity explicitly; no substantive coefficient, sign, or normalization gap was found. The exact old auxiliary rational receipt is separately preserved with its original source hashes. Fresh execution of reconstructed source is a separate required gate.

