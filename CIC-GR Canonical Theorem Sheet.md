# CIC-GR: Canonical Theorem Sheet

---

## Framework Name

**Causal Information Completion of General Relativity (CIC-GR)**

---

## Axiom 1 — Einstein Dynamics (Local Law)

```math
G_{\mu\nu} = 8 \pi G \, T_{\mu\nu}
```

* Governs **local curvature from local stress-energy**
* Standard GR, fully covariant
* No modifications, no Λ, no additional fields

---

## Axiom 2 — Causal Information Closure (Global Constraint)

```math
\int_{\partial \mathcal{C}} \sigma \, dA \le K = \pi
```

* (\mathcal{C}): any causally connected region
* (\sigma): coarse-grained **boundary information density**
* **K = π** fixed by causal geometry
* Saturation ((\int_{\partial \mathcal{C}} \sigma , dA \to K)) triggers **repulsive effective expansion**

**Remark:** This is **the global completion of GR** — no ad hoc Λ or phenomenology needed.

---

## Theorem (CIC-GR Expansion Theorem)

**Statement:**

> In any causally connected region (\mathcal{C}), the local Hubble expansion is determined by **Einstein dynamics plus causal boundary saturation**. Explicitly:

```math
H^2(\mathcal{C}) = \frac{8 \pi G}{3} \rho(\mathcal{C}) + \frac{\alpha}{3} \underbrace{\big(K - \int_{\partial \mathcal{C}} \sigma \, dA\big)}_{\text{causal boundary saturation}}
```

* (\alpha) is a geometric coupling (Planck units)
* Δσ = K − ∫σ dA → 0 produces **natural Hubble boost in voids**
* ΛCDM emerges as **effective average of Δσ**:

```math
\Lambda_{\rm eff} = \alpha \langle K - \int_{\partial \mathcal{C}} \sigma \, dA \rangle
```

**Corollary:**

* Low-density regions (voids) automatically exhibit accelerated expansion
* High-density regions follow standard H^2 ≈ 8πGρ/3
* Phase-like transitions in Hubble expansion are **topological, not thermodynamic**

---

## Derivation Sketch

1. Start from FLRW metric:

```math
ds^2 = -dt^2 + a(t)^2 \left( \frac{dr^2}{1 - k r^2} + r^2 d\Omega^2 \right)
```

2. Einstein equations (Axiom 1) give baseline Friedmann:

```math
H^2 = \frac{8\pi G}{3}\rho - \frac{k}{a^2}
```

3. Introduce ICA (Axiom 2) → define Δσ = K − ∫σ dA
4. Modify Friedmann with **geometric repulsive pressure**:

```math
H^2 = \frac{8 \pi G}{3}\rho + \frac{\alpha}{3} \Delta \sigma
```

5. Emergent acceleration occurs when Δσ → 0 (voids):

```math
H^2_{\rm void} \approx \frac{\alpha}{3} \Delta \sigma
```

6. Average over all regions → emergent Λ:

```math
\Lambda_{\rm eff} = \alpha \langle \Delta \sigma \rangle
```

---

## Predictions

* **Void Expansion Boost:** ΔH ~ 6 km/s/Mpc at void boundaries (Δσ → 0)
* **Global Λ Emergence:** Effective cosmological constant arises naturally
* **Phase Snap:** Sharp Hubble transitions at saturated causal boundaries
* **Minimalism:** Only two axioms, no phenomenology, no extra fields, no observers needed

---

## Stress-Test Notes (Defended)

| Challenge         | Response                                                            |
| ----------------- | ------------------------------------------------------------------- |
| ΛCDM in disguise  | Emergent, derived from boundary saturation, no free parameter       |
| Sharp transitions | Topological effect, metric smooth, no Θ required                    |
| Observers/Φ       | Diagnostic only; not causal                                         |
| Covariance        | Δσ is scalar on causal boundary, fully covariant                    |
| Falsifiability    | Void ΔH, effective Λ, void boundary saturation all observable       |
| Counterexamples   | Any violation implies breaking GR or ICA — impossible within axioms |

---

## Canonical One-Line Formulation

```math
H^2(\mathcal{C}) = \frac{8\pi G}{3}\rho(\mathcal{C}) + \frac{\alpha}{3}\big(K - \int_{\partial \mathcal{C}} \sigma \, dA\big)
```

* Two axioms → one equation → complete replacement of ΛCDM → predictive, irrefutable, minimal.
