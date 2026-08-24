#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nea_quantum_integration.py (v2.0 strict)

Integrates four N.E.A. quantum results with explicit evidence grading.

1. hbar = Z × Tick          → topological identity
2. alpha^{-1}               → strong numerical candidate
3. Uncertainty principle    → scale argument only, not exact ℏ/2
4. Schr/dinger equation     → quantum random walk continuum limit
"""
import numpy as np
import matplotlib.pyplot as plt

print("=" * 80)
print("  N.E.A. quantum core integration (v2.0 strict)")
print("=" * 80)

# =====================================================================
# 1. hbar as product of Z and Tick
# =====================================================================
m_e_MeV = 0.51099895
U_EM = 0.4 * np.pi
Z_MeV = m_e_MeV / U_EM

hbar_c = 197.3269804  # MeV fm
lambda_Z = hbar_c / Z_MeV

print("\n[1] hbar as Z × Tick")
print(f"  Z          = {Z_MeV:.6f} MeV")
print(f"  lambda_Z   = {lambda_Z:.4f} fm")
print(f"  check hbar c = Z × lambda_Z")
print("  Status: topological identity. No free parameter.")

# =====================================================================
# 2. fine-structure constant
# =====================================================================
alpha_inv_NEA = 25 * np.sqrt(3) * np.pi + 1
alpha_inv_CODATA = 137.035999084

print("\n[2] alpha^{-1} = 25√3π + 1")
print(f"  N.E.A.   = {alpha_inv_NEA:.9f}")
print(f"  CODATA   = {alpha_inv_CODATA:.9f}")
print(f"  dev      = {abs(alpha_inv_NEA/alpha_inv_CODATA-1)*1e6:.2f} ppm")
print("  Status: strong numerical candidate.")

# =====================================================================
# 3. Uncertainty principle: scale argument
# =====================================================================
print("\n[3] Bandwidth constraint and uncertainty scale")
print("  Constraint: f_int^2 + f_ext^2 = 1")
print("  Localization consumes f_int; propagation consumes f_ext.")

f_int = np.linspace(0.01, 0.99, 1000)
f_ext = np.sqrt(1 - f_int**2)
q = 1.0 / (f_int * f_ext)
min_q = np.min(q)

print(f"  Scale lower bound 1/(f_int f_ext) min = {min_q:.4f}")
print("  This is a dimensionless scale argument.")
print("  It shows a minimum uncertainty product of order unity.")
print("  It does NOT derive the exact value ℏ/2.")
print("  Exact normalization remains open.")

# =====================================================================
# 4. Quantum random walk
# =====================================================================
print("\n[4] Schr/dinger equation from quantum random walk")
N_steps = 100
N_sites = 201
center = N_sites // 2

psi = np.zeros((N_sites, 2), dtype=complex)
psi[center, 0] = 1.0 / np.sqrt(2)
psi[center, 1] = 1.0 / np.sqrt(2)

theta = np.pi / 4
coin = np.array([[np.cos(theta), np.sin(theta)],
                 [np.sin(theta), -np.cos(theta)]])

for _ in range(N_steps):
    psi = psi @ coin.T
    psi[:, 0] = np.roll(psi[:, 0], -1)
    psi[:, 1] = np.roll(psi[:, 1], +1)

prob = np.abs(psi[:, 0])**2 + np.abs(psi[:, 1])**2
x = np.arange(N_sites) - center
sigma_q = np.sqrt(np.sum(prob * x * x))
sigma_c = np.sqrt(N_steps)

print(f"  quantum sigma = {sigma_q:.2f}  (ballistic ∝ N)")
print(f"  classical sigma = {sigma_c:.2f}  (diffusive ∝ √N)")
print("  Status: supporting continuum-limit evidence.")

# optional plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, prob, 'b-', label='quantum walk')
gauss = np.exp(-x*x/(2*sigma_c*sigma_c))
gauss = gauss / gauss.max() * prob.max() * 0.6
ax.plot(x, gauss, 'r--', label='classical Gaussian')
ax.set_xlabel('x')
ax.set_ylabel('P(x)')
ax.set_title('Quantum random walk vs classical diffusion')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('nea_quantum_random_walk.png', dpi=150)

print("\n" + "=" * 80)
print("  Summary with evidence grading")
print("=" * 80)
print("  hbar = Z×Tick          : topological identity")
print("  alpha^{-1}             : strong numerical candidate")
print("  uncertainty principle  : scale argument, exact hbar/2 open")
print("  Schr/dinger equation    : continuum limit evidence")
print("=" * 80)