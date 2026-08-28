# CM2 v75 V2：径向 specular 图流攻坚的 hostile 修正与真实 frontier

**日期：** 2026-08-27  
**活动作用域：** `SPECULAR_NONCONJUGATE_RADIAL_TWO_DISK_FRONTIER_V75V2`

## 结论

本轮实际证明了一个新的 exact high-power separated projective gate、Palm-to-Gibbs minorization 编译器、regenerative Frostman/PPE 编译器，以及不经过 moving BDL resolvent 的 Roof-cell Fubini suspension 编译器。 hostile audit 同时否决了一个原本可能导致虚假晋级的跳步：

```text
local exact proximal/QNL seeds
+ one positive clean coarea cylinder
!=
global parent-uniform face-to-gate RN/minorization.
```

因此，TG2--TG8 没有被错误写成全 PASS。实际 truth-changing frontier 已压缩为 R75.1--R75.6。

## 1. 实际非共轭径向族

在有限视界双圆盘 periodic Lorentz gas 中固定所有中心，仅令白盘半径

\[
R_w(s)=\frac4{25}+s,
\qquad |s|\le 10^{-4}.
\]

该 family 保持 specular、严格 dispersing、无重叠和有限视界。正常 period-two orbit 的 multiplier 随 \(s\) 严格变化，因此 family 非 \(C^1\) 共轭。

## 2. TG2：同一 occurrence atlas 的实际与缺口

实际可构造的 countable label 包含：source collision、target scatterer、finite impact word、physical face、incident side、homogeneity itinerary、parameter chart 与 recovery descendants。人工 cuts 只在 same face/same owner/same occurrence/opposite orientation 时抵消。

已证明：finite-word impact equations、positive-mass clean first-hit coarea、same-label renormalized grazing blocks。尚缺：全部 recovered Jordan parents 到同一 gate law 的 uniform RN/minorization，以及 complete lower-stratum disposition。

## 3. 新定理：Palm-to-Gibbs Nummelin bridge

若每个 signed face Jordan component 在有限随机恢复后成为 proper measured unstable family，magnet entrance holonomy 的 RN Jacobian上下有界，并且两个 gate branches 对每个 stopped parent 都有统一正质量 floor，则 entrance law 可写成

\[
\nu_{\rm ent}=\delta\,\nu_{\rm gate}+ (1-\delta)\nu_{\rm res},
\]

其中 \(\delta>0\) 与 parent/parameter 无关，且 gate coin 只在 physical law 固定以后引入。证明只是 measure minorization，不使用 CM2。

径向族目前只在 local clean component 上验证该结构；global face law 尚未验证。

## 4. 新定理：Regenerative separated-projective Frostman

若每次 regeneration 有两个 disjoint projective contractions、共同 contraction ratio \(r<1\)、gate coin floor \(\delta>0\)、exponential regeneration moment 和 bounded context distortion，则 stopped conditional projective law具有 uniform Frostman exponent。若 physical slope 是该 projective coordinate 的 uniformly transverse Möbius map，且 complete amplitude 有 conditional \(L^p\) moment，则 weighted PPE exponent 为原 exponent 的 \(1/p'\) 部分。

exact radial gate seeds已验证；uniform face-law regeneration、global slope identity和complete weighted moment尚未验证。

## 5. TG4/TG5 状态

所有 abstract rectangular compilers 均已闭合；但径向族的 actual rectangular CM2仍等待：

```text
R75.1 FACE_TO_GATE_RN
R75.2 GATE_REPEAT
R75.3 SLOPE_BINDING
R75.4 WEIGHT_LEDGER
```

finite-DQ 又要求这些 rows 在同一 parameter common atlas 上统一成立，即 R75.5。

## 6. 新定理：Roof-cell Fubini

对 suspension observable \(A,B\)，先在每个 roof cell 内积分：

\[
\bar A(x)=\int_0^{\tau(x)}A(x,u)\,du,
\qquad
\bar B(x)=\int_0^{\tau(x)}B(x,u)\,du.
\]

完整 time-integrated correlation 可精确拆为 finite same-flight term，加上以 \(\bar A,\bar B\) 为 observables 的 collision correlation series，再除以 mean roof。其参数导数只产生 roof upper-boundary current、roof-integrated observable derivative、mean-roof derivative和collision response。

因此 integrated Green--Kubo response不必先构造 moving-family BDL generator resolvent。pointwise-time/twisted-resolvent response仍需 R75.6 的 common moving graph domain。

## 7. 最新严格状态

```yaml
TG2: PARTIAL_ACTUAL
TG3: PARTIAL_ACTUAL
TG4: OPEN_ACTUAL
TG5: OPEN_ACTUAL
TG6: PARTIAL_COMPILER
TG7: OPEN_ACTUAL
TG8: PARTIAL_ACTUAL
all_positive_actual_gaps_closed: false
formal_credit: 0
```

本轮改变了 proof frontier，但没有把局部 exact gate 冒充全局 CM2。
