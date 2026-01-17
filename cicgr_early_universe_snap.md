# CIC-GR Early Universe Phase Snap – Toy Model

**cicgr_early_universe_snap.py**

**CIC-GR** (Causal Information Cosmology – General Relativity)  
**Phase Snap** interpretation of the early universe / Big Bang

**Author**: ₿oldwin (@MRicardG)  
**Date**: January 2026  
**License**: Unhinged open-source wisdom – share freely, cite if you dare

## Core Idea in One Sentence

The Big Bang was **not** a classical singularity explosion.  
It was a violent **Phase Snap** — a discrete, topology-driven release of a parent black hole's event horizon once trapped information density saturated the exact geometric limit **K = π**.

When the integrated causal information flux over a closed spherical boundary reaches **precisely π** (from pure holographic + geometric reasons — no free parameters), the horizon can no longer stably contain the information without violating causality or closure.  
→ Geometry **snaps** outward → parent black hole horizon transitions into an expanding white-hole-like manifold → our observable universe is born.

This model:

- resolves the **black hole information paradox** (info is never lost — it's geometrically released in the daughter cosmos),
- avoids classical singularities (no point-like collapse — forced topological bounce/expansion),
- explains primordial gravitational waves as the **snap echo**,
- embeds **K = π** as a universal causal saturation constant (the circle constant emerges naturally from spherical boundary integration).

## What the Toy Model Does

This 1D radial, spherically symmetric numerical toy model simulates the **very early phase** of the daughter universe immediately after the Phase Snap.

Main features:

- Gaussian Δσ shell(s) representing residual parent-horizon information saturation (peaked around the "memory" of the parent horizon location)
- Time-decaying snap-driving coupling strength α(t)
- Hubble parameter H(r,t) boosted by both ordinary matter/radiation **and** the snap term ∝ α × Δσ
- Radiation-dominated dilution (ρ ∝ a⁻⁴) in the earliest phase
- Logarithmic scale factor update + strong clipping → numerical stability despite huge initial expansion burst
- Tracks spatial profiles of Δσ(r) and H(r), and mean scale factor evolution

Result: a violent, short-lived **expansion burst** driven by the decaying snap term → rapid growth of the scale factor → transition toward more standard cosmological behaviour once α(t) dies away.

## Key Equations

```text
H²(r,t) = (8πG/3) ρ(r,t)  +  (α(t)/3) Δσ(r)

Δσ(r)   = K × Gaussian(r; r_snap, width)     with K = π

α(t)    = α_initial × exp(-t / τ_decay)

da/dt   → implemented as d(ln a)/dt = H    → a ← a × exp( H Δt × sec_per_yr )
          (with hard clipping to avoid NaN/explosion)

ρ(t)    ∝ a⁻⁴   (radiation-like dilution, very early universe approximation)
