# Author response — Round Thirteen — B3-hamilton-boltzmann-cotangents

**Referee report:** `papers/B3-hamilton-boltzmann-cotangents/REFEREE_REPORT_ROUND12_GPT56_PRO.md`  
**Locked report tree:** `0b58d25307d28a9f06313aea4ef32c4d6e58c16e`  
**Controlling proof source:** `revision/round13-referee-final/B3_JOINT_CONTACT_GAUSSIAN_FORM.tex`  
**Objections addressed: 8/8**

The Gaussian driver lives on collision space and acts on $\Delta p+\psi$, so contact-contact and density-contact brackets are explicit.  The covariance inverse and process tightness are correctly typed.

## Objection-to-proof map

### 1. The displayed Gaussian noise omits the contact coordinate

Resolved in: `thm:r13-b3-joint`.

### 2. The “exact covariance kernel” is therefore the wrong kernel

Resolved in: `thm:r13-b3-kernel`.

### 3. The density martingale problem cannot determine the joint process

Resolved in: `thm:r13-b3-process`.

### 4. The second epi-derivative argument assumes the noise representation it is meant to identify

Resolved in: `thm:r13-b3-mosco`.

### 5. Deterministic interval cumulants do not prove the stated stopping-time estimate

Resolved in: `lem:r13-b3-cumulants`.

### 6. The perturbative hypocoercive chart is not shown to contain all exposed paths used downstream

Resolved in: `thm:r13-b3-energy`.

### 7. The contact trace is not continuous in the displayed energy norm

Resolved in: `thm:r13-b3-energy`.

### 8. Upstream inputs remain open

Resolved in: `thm:r13-b3-main`.

## Scope

The response preserves the paper and its positive theorem program.  The superseded mechanism is not used in the controlling source.  Repository verification establishes source identity, proof-structure coverage, regression checks, and reproducible compilation; external mathematical review remains separate.
