"""
CIC-GR Delta Sigma Toy Model - Experiment Version (Jan 2026)
Focus: Φ-term, void scaling, animation, parameter scans, perturbative collapse
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ────────────────────────────────────────────────
# Physical & conversion constants
# ────────────────────────────────────────────────
G_si       = 6.67430e-11
Mpc_to_m   = 3.085677581467192e22
km_to_m    = 1000.0
sec_per_yr = 3.15576e7

H0_km_s_Mpc = 70.0
H0_si       = H0_km_s_Mpc * (km_to_m / Mpc_to_m) / sec_per_yr
rho_crit_si = 3 * H0_si**2 / (8 * np.pi * G_si)

# ────────────────────────────────────────────────
# Simulation grid
# ────────────────────────────────────────────────
r_max      = 1300.0
nr         = 420
r          = np.linspace(30.0, r_max, nr)

t_max      = 13.8e9
nt         = 520
t          = np.linspace(0, t_max, nt)
dt_yr      = t[1] - t[0]

K = np.pi

# ────────────────────────────────────────────────
# Tunable physics parameters
# ────────────────────────────────────────────────
phi_strength     = 0.80          # >0 → complexity boost in voids
collapse_strength = 0.008        # small → perturbative infall

# Base values (will be scanned)
alpha_base       = 2.8e-35
horizon_factor_base = 4800.0     # comoving horizon scale factor × <a>
sigma_pref_base  = 2.4e-6

# ────────────────────────────────────────────────
# Output folders
# ────────────────────────────────────────────────
os.makedirs("frames", exist_ok=True)
os.makedirs("scans", exist_ok=True)

# ────────────────────────────────────────────────
# Density profile generator with controlled void depth/size
# ────────────────────────────────────────────────
def generate_density(void_depth=0.68, void_width=130, seed=42):
    np.random.seed(seed)
    rho = np.ones_like(r) * 1.0
    
    # 4 voids + 3 walls (base pattern)
    void_centers = [220, 480, 780, 1050]
    wall_centers = [340, 620, 920]
    
    for c in void_centers:
        rho *= (1 - void_depth * np.exp(-((r - c)/void_width)**2))
    
    for c in wall_centers:
        rho *= (1 + 1.9 * np.exp(-((r - c)/110)**2))
    
    return rho

# ────────────────────────────────────────────────
# Sigma & Phi
# ────────────────────────────────────────────────
def compute_sigma(rho):
    return sigma_pref * rho

def compute_phi(rho, rho_bg=1.0):
    und = np.maximum(1.0 - rho/rho_bg, 0.0)
    return phi_strength * und**1.5   # stronger in deep voids

# ────────────────────────────────────────────────
# Single realization runner (returns final ΔH & saves animation frames)
# ────────────────────────────────────────────────
def run_realization(alpha, horizon_factor, sigma_pref, realization_id=0):
    global sigma_pref  # for function access
    
    rho = generate_density(void_depth=0.68, void_width=130, seed=42+realization_id*13)
    a   = np.ones(nr)
    a_prev = a.copy()
    
    H_frames   = []
    Delta_frames = []
    frame_times = []
    
    for it in range(nt):
        a_avg = np.mean(a)
        horizon_comov = horizon_factor * a_avg
        A_eff = 4 * np.pi * horizon_comov**2
        
        sigma_shell = compute_sigma(rho)
        integ = sigma_shell * A_eff
        Delta_sigma = np.maximum(K - integ, 0.0)
        
        Phi = compute_phi(rho)
        
        # Hubble (SI)
        H_sq_si = (8*np.pi*G_si/3) * (rho * rho_crit_si) \
                + (alpha/3) * Delta_sigma \
                + (alpha/3) * 0.6 * Phi
        
        H_si = np.sqrt(np.maximum(H_sq_si, 0.0))
        H_kms = H_si * (Mpc_to_m / km_to_m) * sec_per_yr
        
        # Update scale factor
        da_dt = H_si * a
        a += da_dt * dt_yr * 8e-10   # tuned stability
        
        # Density: Hubble dilution + perturbative collapse
        rho *= (a / a_prev)**(-3.0)
        
        # Crude mass flux → overdensities (very simple!)
        if collapse_strength > 0 and it % 8 == 0:
            grad_rho = np.gradient(rho, r)
            flux = -collapse_strength * grad_rho
            rho += dt_yr * 1e-9 * np.gradient(rho * flux, r)
        
        a_prev = a.copy()
        
        # Save frames every ~40 steps + final
        if it % 40 == 0 or it == nt-1:
            H_frames.append(H_kms.copy())
            Delta_frames.append(Delta_sigma.copy())
            frame_times.append(t[it]/1e9)
    
    # Final ΔH
    H_final = H_frames[-1]
    delta_H = np.max(H_final) - np.min(H_final)
    
    # Save animation frames
    for i, (H_i, Delta_i, time_i) in enumerate(zip(H_frames, Delta_frames, frame_times)):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        
        ax1.plot(r, Delta_i, 'C0', lw=2.1)
        ax1.set_title(f"Δσ(r)  –  t = {time_i:.2f} Gyr")
        ax1.set_ylabel("Δσ")
        ax1.grid(alpha=0.3)
        
        ax2.plot(r, H_i, 'C1', lw=2.1, label=f"ΔH = {delta_H:.2f}")
        ax2.axhline(np.mean(H_i), color='k', ls='--', lw=1.0)
        ax2.set_title("H(r) [km/s/Mpc]")
        ax2.set_ylabel("H [km/s/Mpc]")
        ax2.grid(alpha=0.3)
        ax2.legend()
        
        plt.suptitle(f"Realization {realization_id+1} – Φ={phi_strength}")
        plt.tight_layout()
        plt.savefig(f"frames/anim_{realization_id:02d}_frame_{i:03d}.png", dpi=160)
        plt.close()
    
    return delta_H

# ────────────────────────────────────────────────
# Parameter scan + void depth/size experiment
# ────────────────────────────────────────────────
print("\n=== Parameter Scan & Void Scaling Experiment ===\n")

alphas         = [1.8e-35, 2.8e-35, 4.2e-35]
horizon_factors = [4400, 4800, 5200]
sigma_prefs    = [2.0e-6, 2.4e-6, 2.9e-6]

void_depths    = [0.55, 0.68, 0.80]
void_widths    = [90, 130, 180]

results = []

for vd in void_depths:
    for vw in void_widths:
        delta_Hs = []
        for alpha in alphas:
            for hf in horizon_factors:
                for sp in sigma_prefs:
                    sigma_pref = sp
                    dh = run_realization(alpha, hf, sp, realization_id=0)
                    delta_Hs.append(dh)
        
        mean_dh = np.mean(delta_Hs)
        std_dh  = np.std(delta_Hs)
        results.append((vd, vw, mean_dh, std_dh))
        print(f"Void depth={vd:.2f}, width={vw:.0f} Mpc → ΔH = {mean_dh:.2f} ± {std_dh:.2f} km/s/Mpc")

# Save summary table
np.savetxt("scans/void_scaling_summary.txt",
           np.array(results),
           header="void_depth  void_width  mean_ΔH  std_ΔH",
           fmt="%.3f")

print("\nVoid scaling results saved to scans/void_scaling_summary.txt")
print("\nAnimation frames saved in 'frames/' – ready for ffmpeg:")
print("   ffmpeg -framerate 8 -i frames/anim_00_frame_%03d.png -c:v libx264 -pix_fmt yuv420p cicgr_snap.mp4")

print("\nExperiment complete. Explore the frames & summary table!")
