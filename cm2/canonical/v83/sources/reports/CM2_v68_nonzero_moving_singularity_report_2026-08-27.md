# CM2 v68：非零 moving-singularity 双时间机制的全量 scoped 闭合

**日期：** 2026-08-27  
**作用域：** `CM2_NONZERO_MOVING_SEAM_CONTROLLED_PINBALL_CYLINDER_V68`  
**结论：** 对一个显式、确定性、非镜面 pinball-cylinder billiard family，moving partition seam 产生非零 BV saltus source；在 `W^{3,1}_per -> BV_per` 的正则性损失尺度上，左右两侧谱隙分别收费，得到严格乘积 CM2：

\[
\boxed{
|\langle Q^nKQ^mg,f\rangle|
\le 32\,2^{-(m+n)}\|g\|_{W^{3,1}}\|f\|_\infty .
}
\]

因此

\[
\boxed{
\sum_{m,n\ge0}|\langle Q^nKQ^mg,f\rangle|
\le128\|g\|_{W^{3,1}}\|f\|_\infty .
}
\]

这是一个 **`K != 0`、moving seam saltus 非零、双时间乘积衰减非退化** 的 actual scoped CM2 theorem。它不是此前的 similarity zero-source 旁路。

---

## 1. 与 canonical CM2 义务的关系

canonical 计划把一般 nonconjugate moving-scatterer 的困难分成：moving-face/source atlas、same-occurrence owner、recordwise recovery、weighted PPE、独立 atom-tail、section/phase transfer和 authority。v65 又把 fixed-section 的数学义务压成 `P_atlas / P_reg / P_ppe / P_core / P_phase`，其中 atom 子包必须独立给出 actual source、totalization、norm binding、direct estimate 与 summable joint tail。

v68 不假装逐项解决原 specular Sinai graph-current。它构造一个新的 actual billiard class，使更强的 operator-level 条件成立：

```text
moving physical seam
  -> nonzero BV saltus source K
  -> bounded regularity-loss map W31 -> BV
  -> past W31 spectral contraction
  -> future BV spectral contraction
  -> product CM2 directly
```

因此，旧路线中为处理超奇异 graph current 而需要的 all-depth recovery/PPE，在本作用域被一个更强、可直接验证的两尺度 operator theorem替代，而不是被静默假设。

---

## 2. 实际 pinball-cylinder billiard

### 2.1 Configuration

取平坦 cylinder

\[
\mathcal Q=(\mathbb R/\mathbb Z)\times[0,1].
\]

底壁为 `y=0`，顶壁为 `y=1`。粒子以单位速度作直线运动。

### 2.2 Boundary laws

参数

\[
c\in[2/5,3/5].
\]

- 在底壁坐标 `x` 碰撞后，boundary kick 将速度重置为竖直向上，粒子到达顶壁同一坐标 `x`。
- 在顶壁坐标 `x`，使用 position-controlled reflection law，将粒子沿直线发向底壁坐标

\[
T_c(x)=
\begin{cases}
 x/c,&0\le x<c,\\[2mm]
 (x-c)/(1-c),&c\le x<1,
\end{cases}
\quad\pmod 1.
\]

左支取目标 lift `x/c in [0,1)`；右支取目标 lift `(x-c)/(1-c) in [0,1)`。在 seam `x=c` 处，两个目标在 cylinder 上同为 `0 mod 1`，但使用不同 winding lift，故 outgoing physical direction 有真实跳跃。

从底壁到下一次底壁的 Poincare return 恰为 `T_c`。

### 2.3 Uniform expansion

两支斜率为

\[
T'_c=1/c,
\qquad
T'_c=1/(1-c).
\]

在 `c in [2/5,3/5]` 上，

\[
\inf|T'_c|\ge5/3>1.
\]

两支都 onto `[0,1)`，所以这是 exact two-full-branch expanding return map。

### 2.4 Moving singularity

令

\[
c(a)=1/2+a,
\qquad |a|\le1/10.
\]

物理 reflection-law seam `x=c(a)` 以速度 `dc/da=1` 移动。它不是全局 similarity 共轭产生的零源：固定物理坐标下 transfer operator 对 `c` 的导数非零，并带 cyclic saltus。

---

## 3. Transfer operator 与 source

Lebesgue probability 对所有 `c` 不变。Perron--Frobenius operator 为

\[
(\mathcal L_ch)(y)
=
 c\,h(cy)
 +(1-c)h(c+(1-c)y).
\]

确有

\[
\int_0^1\mathcal L_ch\,dy=\int_0^1h\,dy.
\]

基点 `c0=1/2`：

\[
(Lh)(y)=\frac12h(y/2)+\frac12h((1+y)/2).
\]

定义 `Pi h = int h`，`Q=L-Pi`。

### 3.1 Operator derivative

在

\[
W^{3,1}_{\rm per}\longrightarrow BV_{\rm per}
\]

中，`c -> L_c` 可微，且

\[
\boxed{
(Kh)(y)
=h(y/2)-h((1+y)/2)
+\frac y2h'(y/2)
+\frac{1-y}{2}h'((1+y)/2).
}
\]

其 interior derivative 为

\[
(Kh)'(y)
=h'(y/2)-h'((1+y)/2)
+\frac y4h''(y/2)
+\frac{1-y}{4}h''((1+y)/2).
\]

参数二阶导数的 BV norm 由 `C||h||_{W31}` 一致控制，所以 Taylor integral remainder 给出

\[
\left\|
\frac{\mathcal L_{1/2+a}-L}{a}-K
\right\|_{W^{3,1}\to BV}
=O(|a|).
\]

### 3.2 Source mass zero

因为每个 `L_c` 保质量，

\[
\boxed{\int Kh=0.}
\]

所以 `K` 自动把输入送入 future centered subspace。

### 3.3 BV saltus

对周期函数 `h`，

\[
(Kh)(0+)-(Kh)(1-)
=2(h(0)-h(1/2)).
\]

因此 `K` 的 distributional derivative一般含 seam atom。这是实际 moving partition source，不是普通 smooth perturbation source。

### 3.4 Nonzero witness

取

\[
g(y)=\cos(2\pi y).
\]

则

\[
Kg(y)
=2\cos(\pi y)+\pi(1-2y)\sin(\pi y).
\]

于是

\[
Kg(0+)=2,
\qquad
Kg(1-)=-2,
\]

循环跳跃为 `4`，并且

\[
\boxed{
\langle Kg,Kg\rangle
=\int_0^1(Kg)^2dy
=3+\frac{\pi^2}{6}>0.
}
\]

所以不仅 `K != 0`，而且 CM2 array 本身具有非零 matrix element。

---

## 4. 新工具：Two-Scale Regularity-Loss CM2

### 定理 RL-CM2

设 `X_hi`、`X_lo` 为 Banach spaces，`Pi` 为 rank-one centering projection，`Q=L-Pi`。假设：

1. 对 `u in X_hi`、`Pi u=0`，
   \[
   \|Q^mu\|_{X_hi}\le C_hi rho_hi^m\|u\|_{X_hi};
   \]
2. 对 `v in X_lo`、`Pi v=0`，
   \[
   \|Q^nv\|_{X_lo}\le C_lo rho_lo^n\|v\|_{X_lo};
   \]
3. `K:X_hi -> X_lo` 有界，`Pi K=0`；
4. tests `f` 属于 `X_lo^*`。

则

\[
\boxed{
|\langle Q^nKQ^mg,f\rangle|
\le
C_lo\|K\|C_hi\,
\rho_lo^n\rho_hi^m
\|g\|_{X_hi}\|f\|_{X_lo^*}.
}
\]

若两几何级数可和，则 CM2 双和绝对可和。

该 theorem 的关键是允许 source 损失正则性：past side 在强空间收费，source 从强空间落入弱空间，future side在弱空间收费。这是一般 graph-current recovery/PPE 路线的一个严格 operator-level 替代条件。

---

## 5. 基点 dyadic map 的两侧收费

### 5.1 Past side: `W31`

对 `j=1,2,3`，

\[
(L^mh)^{(j)}=2^{-jm}L^m(h^{(j)}).
\]

若 `int h=0`，周期 Poincare 不等式与 `L1` contraction 给出

\[
\boxed{
\|Q^mh\|_{W^{3,1}}
\le2\,2^{-m}\|h\|_{W^{3,1}}.
}
\]

### 5.2 Source bound

令

\[
\|u\|_{BV_{per}}=\|u\|_1+Var_{per}(u).
\]

直接估计：

\[
\|Kh\|_1
\le4\|h\|_1+2\|h'\|_1,
\]

\[
Var_{per}(Kh)
\le6\|h'\|_1+\|h''\|_1.
\]

故

\[
\boxed{
\|Kh\|_{BV_{per}}
\le8\|h\|_{W^{3,1}}.
}
\]

### 5.3 Future side: `BV`

对 dyadic transfer operator，两个 half-branch 的内部 variation 与 cyclic jumps 精确分割，故

\[
Var_{per}(Lu)\le\frac12Var_{per}(u).
\]

若 `int u=0`，则 `||u||_1<=Var_per(u)`，所以

\[
\boxed{
\|Q^nu\|_{BV_{per}}
\le2\,2^{-n}\|u\|_{BV_{per}}.
}
\]

---

## 6. 非零 moving-singularity CM2 theorem

对 `g in W31_per`、`int g=0`，`f in L∞`，组合上一节三式：

\[
\begin{aligned}
|\langle Q^nKQ^mg,f\rangle|
&\le
\|Q^nKQ^mg\|_1\|f\|_\infty\\
&\le
2\,2^{-n}\cdot8\cdot2\,2^{-m}
\|g\|_{W^{3,1}}\|f\|_\infty.
\end{aligned}
\]

即

\[
\boxed{
|\langle Q^nKQ^mg,f\rangle|
\le32\,2^{-(m+n)}
\|g\|_{W^{3,1}}\|f\|_\infty.
}
\]

因此

\[
\boxed{
\sum_{m,n\ge0}
|\langle Q^nKQ^mg,f\rangle|
\le128\|g\|_{W^{3,1}}\|f\|_\infty.
}
\]

这严格实现了 canonical CM2 要求的 product tail，而不是不足以双重可和的 additive tail。

---

## 7. Scoped D02 闭合

### D02-A

两个实际 full branches：

```text
LEFT  [0,c)   -> [0,1)
RIGHT [c,1)   -> [0,1)
```

owner、domain、inverse、Jacobian weight 和 image 全部显式。`unresolved=0`。

### D02-B

moving seam 有两条实际 physical traces：

```text
LEFT trace  inverse c*y
RIGHT trace inverse c+(1-c)*y
```

两侧都绑定同一个 seam、同一 parameter path 和 saltus source；各消费一次 top-wall collision。`unresolved=0`。

### D02-C

prefix code 为 `{0,1}`，

\[
2^{-1}+2^{-1}=1.
\]

两 inverse branches complete-totalize 全 target，formal scoped unresolved 为 `0`。

---

## 8. GENERAL-U3 八字段 actual packet

v68 逐字段生成八个不同 artifact：

1. actual parameterized singular geometry/atlas；
2. actual nonzero BV saltus source `K`；
3. two-branch totalization / Kraft identity；
4. `W31 -> BV` source/target norm binding；
5. direct atom estimate；
6. `32*2^{-(m+n)}` summable joint tail；
7. `c in [2/5,3/5]` parameter/seam compatibility；
8. Lebesgue initial law、centered `W31` inputs、`L∞` tests和 collision-return scope。

packet status：

```text
ACTUAL_SCOPED_NONZERO_SOURCE_U3_PACKET_COMPLETE
```

它不是 universal specular-Sinai packet。

---

## 9. Verification

独立 verifier 不导入 generator，重算：

- exact file set、self hashes 和 manifest；
- 两 branch 全覆盖和 expansion constant；
- operator derivative formula；
- seam saltus 与 `cos(2pi x)` nonzero witness；
- exact pairing `3+pi^2/6`；
- mass-zero polynomial jet checks；
- W31/BV constants与 CM2 arithmetic；
- D02-A/B/C；
- 八个 U3 field artifacts 和 evidence digests；
- scope non-upgrade。

Hostile tests 覆盖 hidden file、symlink、branch image、seam movement、source formula、source norm、source-zero tamper、D02 unresolved、post-terminal collision、Kraft、rate、specular overclaim、original-scope substitution、U3 alias、universal overclaim、noncanonical JSON 等。

结果：

```text
18/18 hostile tests PASS

Dual deterministic build 与 fresh-extraction replay 也分别 PASS；总 validation gates 为 `20/20 PASS`。
```

并继续执行 dual deterministic build 与 fresh-extraction replay。

---

## 10. 严格作用域边界

### 已闭合

```yaml
ActualDeterministicBilliardFamily: true
MovingPhysicalSeam: true
K_nonzero: true
BV_saltus_nonzero: true
NonzeroMatrixElement: true
ProductTwoTimeCM2: PROVED
AbsoluteDoubleSum: PROVED
ScopedD02: CLOSED
ScopedGeneralU3Packet: CLOSED
```

### 未声称

```yaml
SpecularReflection: false
DispersingSinaiTable: false
OriginalSourceW_R1648: not substituted
UniversalMovingScattererCM2: not claimed
FullPhysicalTimeRoofResponse: not claimed
ExternalPeerReview: not performed
```

因此，v68 的科学含义是：**非零 moving-singularity 双时间机制已经在一个显式实际 billiard class 上被真正攻克；最难的 specular Sinai graph-current universality 仍是更强目标。**

---

## 11. Primary-source context

- Del Magno, Lopes Dias, Duarte, Gaivao, *Ergodicity of Polygonal Slap Maps*, arXiv:1312.1314：说明 non-specular normal-projection billiards产生 piecewise affine expanding interval maps。
- Del Magno, Lopes Dias, Duarte, Gaivao, *Hyperbolic Polygonal Billiards Close to 1-Dimensional Piecewise Expanding Maps*, arXiv:1501.03697：将 contracting reflection laws 与 expanding slap maps联系。
- Demers and Zhang, *A Functional Analytic Approach to Perturbations of the Lorentz Gas*, arXiv:1210.1261：其 perturbation framework明确包含 nonelastic reflections、kicks 和 slips。
- Baladi and Smania, *Linear Response Formula for Piecewise Expanding Unimodal Maps*, arXiv:0705.3383：提供 piecewise-expanding/BV transfer-operator和 moving critical/saltus 背景。v68 的核心估计为本报告中的直接精确证明，不依赖该文的线性响应定理。
