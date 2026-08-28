# CM2 v67：从零重建的 similarity-scoped D02 全量几何与 moving-billiard U3/CM2 packet

**日期：** 2026-08-27  
**作用域：** `CM2_GLOBAL_SIMILARITY_TWO_DISK_COLLISION_MAP_SCOPED_V67`  
**结论：** 新的全局 Euclidean-similarity moving-billiard 子类中，scoped D02、八字段 U3 packet 与 product-CM2 已闭合；原 `Source-W/R1648/r63bd` 目标不被替代，仍保持 `NO-GO_FOR_CLAIM`。

---

## 1. 为什么不能逐字重建原 D02

给定的 canonical dossier 保存了 C32–C78 的总数、阶段结论、对象 digest 与关键路径，但当前 conversation/Library 中没有找到：

- C32–C78 的原始 producer 源码；
- 76,832 行 cell ledger 的原始物理字节；
- 33,638 行 D02-A task ledger；
- 7,463 representatives / 14,926 sides 的逐 collision ledger；
- 862-parent 原始 Kraft 行；
- 原始 Source-W/R1648 的 exact geometry kernels。

因此，从摘要和 SHA-256 反演原始行是不可能合法完成的；任何声称“恢复了原始行”的输出都会是伪造。v67 不采取这条路线。

本项目改为：**选定一个新的、明确可证明的 moving-billiard 子类，从零生成自然几何账本，并明确禁止将其回填成原 r63bd D02。**

---

## 2. v66 的撤回与 v67 修复

早期 v66 为了匹配原工作量，按固定配额给 33,638 个 hash-selected cells 套用了原 residual class 名称。这些类别不是由新模型几何产生，因而不能称为 actual D02-A。

v67 永久修正：

- D02-A 覆盖全部 76,832 cells；
- task class 只由实际 `(u,p)` 边界邻接关系生成；
- D02-B 覆盖全部 38,416 reflection representatives 和 76,832 parameter sides；
- parent 使用 32 个自然 `disk × chart × macro` domains；
- 不复用原 33,638 / 7,463 / 862 的工作量数字；
- `scope_non_equivalence.json` 明确声明 v67 不能代替原 D02。

---

## 3. 显式 moving-billiard family

### 3.1 基表

在平坦 torus \(\mathbb R^2/\mathbb Z^2\) 上取两个圆盘：

\[
\bar R=\frac9{25},\qquad R=\frac4{25},
\]

灰盘中心为 \((0,0)\)，白盘中心为 \((1/2,1/2)\)。

### 3.2 有限视界的精确证明

无重叠：

\[
\left(\frac{13}{25}\right)^2=\frac{169}{625}<\frac12,
\qquad 338<625.
\]

对任一 primitive 非轴 lattice direction \((p,q)\)，有 \(p^2+q^2\ge2\)。灰盘中心行的垂直间距至多 \(1/\sqrt2\)，而

\[
2\bar R=\frac{18}{25}>\frac1{\sqrt2},
\qquad 648>625.
\]

故全部非轴 corridors 被灰盘阻断。对水平/垂直方向，灰盘行与白盘行相距 \(1/2\)，且

\[
\bar R+R=\frac{13}{25}>\frac12,
\qquad 26>25,
\]

故轴向 corridors 也被阻断。由此基表有限视界。

### 3.3 参数化全局 similarity

对 \(|a|\le1/8\)，令

\[
s(a)=1+\frac a{16},
\qquad
b(a)=\left(\frac a{64},-\frac a{128}\right),
\]

\[
R(a)=\frac1{1+a^2}
\begin{pmatrix}
1-a^2 & -2a\\
2a & 1-a^2
\end{pmatrix}.
\]

定义

\[
S_a(x)=b(a)+s(a)R(a)x,
\qquad
\Lambda_a=s(a)R(a)\mathbb Z^2.
\]

移动表是

\[
Q_a=S_a(Q_0)\subset\mathbb R^2/\Lambda_a.
\]

这里 lattice 与全部 scatterers 同时变换，故 \(S_a\) 在参数依赖的平坦 tori 之间良定义。又

\[
\frac{127}{128}\le s(a)\le\frac{129}{128},
\]

所以有限视界常数在该参数区间统一受控。

### 3.4 精确共轭

Euclidean similarity 将直线映成直线、保持法向夹角和镜面反射规则。用 normalized boundary arclength \(u\) 与 \(p=\sin\varphi\) 标记碰撞相空间，得到

\[
\boxed{H_a^{-1}T_aH_a=T_0.}
\]

对 flow 与 roof：

\[
H_a^{-1}\Phi_a^tH_a=\Phi_0^{t/s(a)},
\qquad
\tau_a\circ H_a=s(a)\tau_0.
\]

本轮 product-CM2 只声明 collision-map moving source。因 pulled-back map 恒定，

\[
\boxed{K_V:=\left.\partial_a\widehat L_a\right|_{a=0}=0.}
\]

---

## 4. 全量 normalized geometry

采用：

```text
2 disks
× 2 half-boundary charts per disk
× 8 macros per chart
× 49 u-cells per macro
× 49 p-cells
= 76,832 open cells.
```

完整账本：

| 对象 | 行数 |
|---|---:|
| open cells | 76,832 |
| codimension-one faces | 155,232 |
| corners | 78,400 |

Face census：

| 类别 | 数量 |
|---|---:|
| `U_INTERNAL` | 75,264 |
| `U_MACRO_SEAM` | 1,372 |
| `U_CHART_SEAM` | 196 |
| `P_INTERNAL` | 75,264 |
| `P_GRAZING_BOUNDARY` | 3,136 |

所有 open cells、faces 与 corners 均包含 deterministic IDs、exact rational intervals、owner、reflection、parent 与 transport 类型。

---

## 5. Scoped D02-A

v67 不再使用原 residual names。每个 cell 的 class 由其实际局部网格位置唯一决定：

| 几何类别 | 数量 |
|---|---:|
| `INTERIOR_CELL` | 70,688 |
| `U_MACRO_BOUNDARY_ADJACENT` | 3,008 |
| `P_GRAZING_ADJACENT` | 3,008 |
| `U_P_CORNER_ADJACENT` | 128 |
| **合计** | **76,832** |

每一行都绑定：

```text
cell / parent / reflection identity
actual geometric class
unique normalized owner
two parameter sides
record preservation
exact conjugacy proof digest
terminal gate = GLOBAL_SIMILARITY_CONJUGACY
```

全部 disposition 为：

```text
CONNECTED_TO_KNOWN_BASE_CELL
```

这是由 \(H_a^{-1}T_aH_a=T_0\) 直接产生的 exact identity，不是按配额分配。

---

## 6. Scoped D02-B

Horizontal mirror symmetry给出无 fixed point 的 involution

\[
(u,p)\longmapsto(1-u,-p).
\]

因此 76,832 cells 形成：

\[
38,416
\]

个 reflection representatives。每个 representative 有 `NEGATIVE_PARAMETER_SIDE` 与 `POSITIVE_PARAMETER_SIDE`，总计：

\[
76,832\text{ sides}.
\]

由于全局共轭是 collision continuation 之前的更强 terminal predicate，所有 sides 都在

```text
PRE_COLLISION_GLOBAL_CONJUGACY
```

终止，`collision_steps_consumed=0`。v67 没有伪造 collision 3–1648 的 owner/word rows，也没有将这一 preterminal route描述成原 R1648 continuation。

---

## 7. Scoped D02-C 与 Kraft

自然 parent 是：

```text
2 disks × 2 charts × 8 macros = 32 parents.
```

每个 parent 含 2,401 cells。对 16 个 reflection-parent pairs，先在一侧生成 complete balanced binary prefix code，再把同一 code赋给 reflected cell。由此：

- 每个 parent 的 Kraft sum 精确为 1；
- reflection 两侧 prefix 精确相同；
- 76,832 cells 全覆盖且无重复；
- scoped unresolved = 0。

D02-C 四类账在该 scope 中退化为：

```text
CONNECTED_TO_KNOWN_BASE_CELL = 76,832
all other terminal classes     = 0
scoped unresolved              = 0
```

---

## 8. 八字段 GENERAL-U3 packet

v67 逐字段生成八个独立 artifact：

1. actual parameterized singular geometry/atlas；
2. actual direct U3 atom family：零 moving-map source；
3. orbit/cell/group totalization；
4. common source/target norm binding；
5. direct atom estimate：norm 恰为 0；
6. joint tail envelope：恰为 0；
7. analytic parameter modulus 与 fixed seams；
8. initial-law/domain scope。

八个 field artifact digest 两两不同，packet 明确标记：

```text
SCOPED_ZERO_U3_TAIL_PACKAGE
not original universal U3 packet
```

---

## 9. Scoped product-CM2 theorem

由

\[
K_V=0
\]

立即有，对任意 \(m,n\ge0\)：

\[
\boxed{
\langle Q^nK_VQ^mg,f\rangle=0.
}
\]

因此：

\[
\boxed{
\sum_{m,n\ge0}
\left|
\langle Q^nK_VQ^mg,f\rangle
\right|=0.
}
\]

这是一条真实但严格 scoped 的 moving-billiard CM2 定理：物理表随参数移动，然而该 family 是全局 similarity-conjugate，所以 moving-map source 消失。

它**不是**：

- 原 Source-W/R1648 D02；
- nonconjugate moving-scatterer CM2；
- 原 C79g persisted authority；
- 原 r63bd D02 unlock。

---

## 10. Verification 与 hostile tests

独立 verifier 从压缩账本重建：

- 全部 IDs 与 rational intervals；
- face/corner census；
- reflection involution；
- 32 parent Kraft equations；
- D02-A geometry-class census；
- 38,416 representatives / 76,832 sides；
- D02-C unresolved zero；
- 八字段 U3 distinctness；
- scoped theorem与原状态隔离。

Fresh extraction replay：`PASS`。

Hostile/determinism tests：

```text
positive full bundle
hidden file
original unlock escalation
cell reflection tamper
face deletion
Kraft tamper
D02-A class tamper
D02-B missing side
D02-C unresolved flip
U3 field alias
nonzero-source overclaim
original-scope substitution
independent dual build
final tar equality
```

结果：

\[
\boxed{14/14\ \mathrm{PASS}.}
\]

两个独立输出目录生成的 tar 包逐字节一致：

```text
SHA-256
836caa903371c071f2bccd4b7ece2a984403226f33686f65d9f03afba3d219eb
```

---

## 11. Latest-wins 双状态

### 新 scoped similarity family

```yaml
scoped_D02A: CLOSED  # 76,832/76,832
scoped_D02B: CLOSED_BY_PRECOLLISION_GLOBAL_CONJUGACY
scoped_D02C: CLOSED  # unresolved=0
scoped_U3_packet: CLOSED
scoped_product_CM2: PROVED, exact value 0
```

### 原 Source-W/R1648/r63bd

```yaml
raw_generators_available: false
reconstructed_by_v67: false
v67_substitutes_for_original_D02: false
formal_global_closure_credit: 0
D02_unlock: false
D03: UNAUTHORIZED
D04: NOT_MINTED
Gate5: 10/18
complete_global_blocks: 0
CM2: NO-GO_FOR_CLAIM
```

---

## 12. Primary-source context

- Mikko Stenlund, *A Vector-Valued Almost Sure Invariance Principle for Sinai Billiards with Random Scatterers*, arXiv:1210.0902. 该文给出同类 torus two-disk 几何及 no-overlap/finite-horizon inequalities。
- Mark F. Demers and Hong-kun Zhang, *A Functional Analytic Approach to Perturbations of the Lorentz Gas*, arXiv:1210.1261. 该文说明 anisotropic transfer-operator framework覆盖 scatterer movements/deformations；v67 的 zero-source collision-map theorem不依赖其 perturbative differentiability。

---

## 13. 最终判断

v67 完成的是一个从零构造、自然计数、全量可重放的**新 scoped actual class**：

\[
\boxed{
\text{Scoped similarity D02 + U3 + zero-source CM2 closed.}
}
\]

原目标仍为：

\[
\boxed{
\text{Original nonconjugate Source-W/R1648 CM2 remains NO-GO.}
}
\]

这不是退回设计阶段，而是把“可由当前材料真正闭合的实际子类”与“缺少原始字节和 nonconjugate primitive 的原目标”永久分型。
