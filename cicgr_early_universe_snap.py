#!/usr/bin/env python3
"""
cicgr_early_universe_snap.py

CIC-GR Early Universe Phase Snap Toy Model
Big Bang interpreted as causal/information phase transition
of parent black hole horizon saturation

Author: Boldwin / CIC-GR collaboration
Date: January 2026

Features:
- Radial 1D spherical symmetry
- Localized Δσ Gaussian shell representing parent horizon
- Time-dependent snap strength decay
- Radiation-dominated dilution in very early phase
- Logarithmic scale factor update for numerical stability
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ────────────────────────────────────────────────
# Physical & conversion constants
# ────────────────────────────────────────────────
G_si       = 6.67430e-11               # m³ kg⁻¹ s⁻²
Mpc_to_m   = 3.085677581467192e22      # m/Mpc
km_to_m    = 1000.0
sec_per_yr = 3.15576e7

K          = np.pi                     # causal closure constant

# ────────────────────────────────────────────────
# Model parameters
# ────────────────────────────────────────────────
alpha_snap_initial = 8e-11             # illustrative strong coupling during snap
snap_decay_time    = 2.5e5             # years - characteristic decay timescale

r_max          = 600.0                 # Mpc
nr             = 320
r              = np.linspace(2.0, r_max, nr)

r_snap         = 60.0                  # location of parent horizon shell
snap_width     = 18.0                  # width of the snap shell

t_start        = 1e-2                  # avoid t=0
t_max          = 1.2e6                 # years (~1.2 Myr)
nt             = 1400
t              = np.linspace(t_start, t_max, nt)
dt             = t[1] - t[0]           # years per step

# Very high initial energy density (toy placeholder)
rho0_si        = 5e7                   # kg/m³
rho            = np.ones(nr) * rho0_si

# Extremely contracted initial scale factor
a              = np.full(nr, 1e-13)
a_prev         = a.copy()

# History arrays
H_hist         = np.zeros((nt, nr))
Delta_hist     = np.zeros((nt, nr))
a_avg_hist     = np.zeros(nt)

# Optional: prepare for animation frames
SAVE_FRAMES    = True
frame_dir      = "snap_frames"
if SAVE_FRAMES:
    os.makedirs(frame_dir, exist_ok=True)

# ────────────────────────────────────────────────
# Δσ shell function (single shell version)
# ────────────────────────────────────────────────
def sigma_snap(r):
    """Single Gaussian shell representing parent BH horizon"""
    return K * np.exp(-((r - r_snap) / snap_width)**2)

    # Alternative: multiple nested shells (uncomment to try)
    # total = 0.0
    # total += 1.00 * K * np.exp(-((r - 60.0)/18.0)**2)
    # total += 0.60 * K * np.exp(-((r - 140.0)/28.0)**2)
    # total += 0.30 * K * np.exp(-((r - 280.0)/45.0)**2)
    # return np.minimum(total, K * 1.15)

# ────────────────────────────────────────────────
# Main time evolution loop
# ────────────────────────────────────────────────
for it in range(nt):
    # Current snap strength (decaying)
    alpha_current = alpha_snap_initial * np.exp(-t[it] / snap_decay_time)
    
    # Information deficit / boundary term
    Delta_sigma = sigma_snap(r)
    
    # Hubble parameter squared (SI units)
    H_sq = (8 * np.pi * G_si / 3.0) * rho \
         + (alpha_current / 3.0) * Delta_sigma
    
    H = np.sqrt(np.maximum(H_sq, 0.0))
    
    # Logarithmic scale factor update - prevents explosion
    dln_a = H * dt * sec_per_yr
    a *= np.exp(np.clip(dln_a, -3.0, 0.7))  # strong caps for stability
    
    # Radiation-like dilution (very early universe)
    if it > 0:
        rho *= (a / a_prev) ** -4.0
    
    # Store history
    H_hist[it]     = H * (Mpc_to_m / km_to_m) * sec_per_yr
    Delta_hist[it] = Delta_sigma
    a_avg_hist[it] = np.mean(a)
    
    a_prev = a.copy()
    
    # Optional: save animation frame
    if SAVE_FRAMES and (it % 20 == 0 or it == nt-1):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.2))
        
        ax1.plot(r, Delta_hist[it], 'C0', lw=2.1)
        ax1.set_title(f"Δσ(t)  —  {t[it]/1e3:.1f} kyr")
        ax1.set_ylabel("Δσ")
        ax1.grid(alpha=0.35)
        
        ax2.plot(r, H_hist[it], 'C1', lw=2.1)
        ax2.axhline(np.mean(H_hist[it]), color='k', ls='--', alpha=0.65)
        ax2.set_title(f"H(r) [km/s/Mpc]  —  {t[it]/1e3:.1f} kyr")
        ax2.grid(alpha=0.35)
        
        plt.suptitle(f"CIC-GR Phase Snap Evolution  frame {it//20:03d}")
        plt.tight_layout()
        plt.savefig(f"{frame_dir}/snap_{it:05d}.png", dpi=150, bbox_inches='tight')
        plt.close(fig)

# ────────────────────────────────────────────────
# Final plots
# ────────────────────────────────────────────────
fig, axs = plt.subplots(3, 1, figsize=(11, 14))

axs[0].plot(r, Delta_hist[-1], 'C0', lw=2.4)
axs[0].set_title("Final Δσ distribution")
axs[0].set_xlabel("Comoving radius [Mpc]")
axs[0].set_ylabel("Δσ")
axs[0].grid(alpha=0.35)

axs[1].plot(r, H_hist[-1], 'C1', lw=2.4, label="final H(r)")
axs[1].axhline(np.mean(H_hist[-1]), color='k', ls='--', alpha=0.7, label="mean")
axs[1].set_title("Hubble parameter after phase snap")
axs[1].set_xlabel("Comoving radius [Mpc]")
axs[1].set_ylabel("H [km/s/Mpc]")
axs[1].grid(alpha=0.35)
axs[1].legend()

axs[2].plot(t/1000, a_avg_hist, 'C3', lw=2.3, label="<a(t)>")
axs[2].set_yscale('log')
axs[2].set_title("Scale factor evolution – snap-driven burst")
axs[2].set_xlabel("Time [kyr]")
axs[2].set_ylabel("Average scale factor (log)")
axs[2].grid(alpha=0.35)
axs[2].legend()

plt.tight_layout()
plt.show()

# Summary statistics
print("\n" + "="*60)
print("CIC-GR Early Universe Phase Snap - Summary")
print("="*60)
print(f"Max early H (during burst):   {np.max(H_hist[20:150]):.2e} km/s/Mpc")
print(f"Final mean H:                 {np.mean(H_hist[-1]):.2e} km/s/Mpc")
print(f"Total expansion factor:       {a_avg_hist[-1]/a_avg_hist[0]:.1e}x")
print(f"Peak Δσ location:             {r[np.argmax(Delta_hist[-1]):.1f} Mpc")
print(f"Final snap strength (alpha):  {alpha_current:.2e}")
print("="*60)

if SAVE_FRAMES:
    print(f"\nFrames saved in: {frame_dir}/")
    print("To create animation:")
    print("ffmpeg -framerate 15 -i snap_frames/snap_%05d.png -c:v libx264 -pix_fmt yuv420p cicgr_snap_propagation.mp4")
