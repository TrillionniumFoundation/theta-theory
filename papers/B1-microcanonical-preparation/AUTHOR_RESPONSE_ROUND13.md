# Author response — Round Thirteen — B1-microcanonical-preparation

**Referee report:** `papers/B1-microcanonical-preparation/REFEREE_REPORT_ROUND12_GPT56_PRO.md`  
**Locked report tree:** `0b58d25307d28a9f06313aea4ef32c4d6e58c16e`  
**Controlling proof source:** `revision/round13-referee-final/B1_NUMBER_COEFFICIENT_MICROCANONICAL.tex`  
**Objections addressed: 8/8**

The empty grand-canonical atom is removed by extracting the exact particle-number coefficient first.  All Fourier estimates and the full Hessian are then proved in the canonical coefficient law.

## Objection-to-proof map

### 1. The claimed speed-dependent power tail contradicts the compound-Poisson formula

Resolved in: `thm:r13-b1-coefficient-expansion`, `thm:r13-b1-fourier`.

### 2. The pressure inequality has the same contradiction

Resolved in: `thm:r13-b1-fourier`.

### 3. The connected polymer remainder cannot repair the empty-sector atom

Resolved in: `thm:r13-b1-coefficient-expansion`.

### 4. The high-frequency Fourier inversion is therefore invalid

Resolved in: `thm:r13-b1-local`.

### 5. The singleton covariance proof also suppresses the Poisson number direction

Resolved in: `lem:r13-b1-meanmap`.

### 6. The complex aperiodicity argument is not uniform for the full dynamical source

Resolved in: `thm:r13-b1-fourier`.

### 7. The shell theorem depends on a false frequency theorem

Resolved in: `thm:r13-b1-local`.

### 8. The microcanonical transfer and all downstream uses remain blocked

Resolved in: `thm:r13-b1-transfer`.

## Scope

The response preserves the paper and its positive theorem program.  The superseded mechanism is not used in the controlling source.  Repository verification establishes source identity, proof-structure coverage, regression checks, and reproducible compilation; external mathematical review remains separate.
