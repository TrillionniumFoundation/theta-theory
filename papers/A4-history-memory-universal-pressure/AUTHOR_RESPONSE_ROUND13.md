# Author response — Round Thirteen — A4-history-memory-universal-pressure

**Referee report:** `papers/A4-history-memory-universal-pressure/REFEREE_REPORT_ROUND12_GPT56_PRO.md`  
**Locked report tree:** `0b58d25307d28a9f06313aea4ef32c4d6e58c16e`  
**Controlling proof source:** `revision/round13-referee-final/A4_WASSERSTEIN_DOOB_DESCRIPTOR_MEMORY.tex`  
**Objections addressed: 8/8**

Doeblin is replaced by weighted Wasserstein contraction; the Poisson martingale is exactly centered; the Doob, renewal-resolvent, zero-multiplicity and inverse-Laplace steps are separately proved.

## Objection-to-proof map

### 1. Doeblin minorization is impossible on a complete-past history state

Resolved in: `thm:r13-a4-wasserstein`.

### 2. The Harris proof therefore does not establish the claimed spectral gap

Resolved in: `thm:r13-a4-wasserstein`.

### 3. The Feynman–Kac eigenpair is not supplied by the Harris theorem

Resolved in: `thm:r13-a4-doob`.

### 4. The renewal-resolvent strip depends on A2's false high-frequency theorem

Resolved in: `thm:r13-a4-renewal`.

### 5. The transmission-zero decomposition omits higher-order zero structure

Resolved in: `thm:r13-a4-memory`.

### 6. Stability of all descriptor exponents is not established

Resolved in: `thm:r13-a4-memory`.

### 7. The quenched rough theorem is stronger than the established input

Resolved in: `thm:r13-a4-rough`.

### 8. Downstream consequences are therefore conditional

Resolved in: `thm:r13-a4-main`.

## Scope

The response preserves the paper and its positive theorem program.  The superseded mechanism is not used in the controlling source.  Repository verification establishes source identity, proof-structure coverage, regression checks, and reproducible compilation; external mathematical review remains separate.
