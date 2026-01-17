import numpy as np
import matplotlib.pyplot as plt

# Constants
G_si       = 6.67430e-11
Mpc_to_m   = 3.085677581467192e22
km_to_m    = 1000.0
sec_per_yr = 3.15576e7

K          = np.pi
alpha_snap = 5e-10          # Illustrative large value during snap phase
r_max      = 500.0
nr         = 300
r          = np.linspace(1.0, r_max, nr)

r_snap     = 50.0           # parent horizon shell location (toy scale)
snap_width = 12.0

t_max      = 1e6            # 1 Myr – snap duration
nt         = 1200
t          = np.linspace(1e-3, t_max, nt)
dt         = t[1] - t[0]    # years

# Initial ultra-high density (very rough placeholder)
rho0_si    = 1e8            # kg/m³ → tuned so matter term doesn't overwhelm snap
rho        = np.ones(nr) * rho0_si
a          = np.full(nr, 1e-12)  # extremely small initial scale factor

H_hist     = np.zeros((nt, nr))
a_avg_hist = np.zeros(nt)
Delta_hist = np.zeros((nt, nr))

def sigma_snap(r):
    return K * np.exp(-((r - r_snap)/snap_width)**2)

a_prev = a.copy()  # initialize

for it in range(nt):
    Delta_sigma = sigma_snap(r)
    
    # Fade the snap strength over time
    alpha_current = alpha_snap * np.exp(-t[it] / 2e5)  # decay ~200 kyr
    
    # Hubble squared (SI)
    H_sq = (8 * np.pi * G_si / 3.0) * rho + (alpha_current / 3.0) * Delta_sigma
    H = np.sqrt(np.maximum(H_sq, 0.0))
    
    # Log update with stronger cap
    dln_a = H * dt * sec_per_yr
    a *= np.exp(np.clip(dln_a, -2.0, 0.6))  # tighter control
    
    # Radiation dilution
    if it > 0:
        rho *= (a / a_prev) ** -4.0
    
    H_hist[it]     = H * (Mpc_to_m / km_to_m) * sec_per_yr
    Delta_hist[it] = Delta_sigma
    a_avg_hist[it] = np.mean(a)
    a_prev         = a.copy()

# ─── Plots ───────────────────────────────────────────────────────────────
fig, axs = plt.subplots(3, 1, figsize=(11, 14))

axs[0].plot(r, Delta_hist[-1], 'C0', lw=2.4)
axs[0].set_title("Δσ – Parent BH Horizon Shell (late time)")
axs[0].set_xlabel("Comoving radius [Mpc]")
axs[0].set_ylabel("Δσ")
axs[0].grid(alpha=0.35)

axs[1].plot(r, H_hist[-1], 'C1', lw=2.4, label="final H(r)")
axs[1].axhline(np.mean(H_hist[-1]), color='k', ls='--', alpha=0.6, label="mean")
axs[1].set_title("Hubble parameter after snap")
axs[1].set_xlabel("Comoving radius [Mpc]")
axs[1].set_ylabel("H [km/s/Mpc]")
axs[1].grid(alpha=0.35)
axs[1].legend()

axs[2].plot(t/1e3, a_avg_hist, 'C3', lw=2.3, label="<a(t)>")
axs[2].set_yscale('log')
axs[2].set_title("Scale factor growth – snap driven burst")
axs[2].set_xlabel("Time [kyr]")
axs[2].set_ylabel("Average scale factor (log)")
axs[2].grid(alpha=0.35)
axs[2].legend()

plt.tight_layout()
plt.show()

# Summary stats
print(f"Max early H (step ~10):  {np.max(H_hist[10]):.2e} km/s/Mpc")
print(f"Final mean H:            {np.mean(H_hist[-1]):.2e} km/s/Mpc")
print(f"Expansion factor:        {a_avg_hist[-1]/a_avg_hist[0]:.1e}x")
print(f"Peak Δσ location:        {r[np.argmax(Delta_hist[-1]):.1f} Mpc")
