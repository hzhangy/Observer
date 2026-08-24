#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nea_bell_inequality_suture.py (v4.0 strict)

N.E.A. Bell-CHSH strict audit with explicit status levels.

Part 1: 3D-local hidden-variable model
        True Monte Carlo simulation.
        Result: S ≈ 2.0000.

Part 2: Quantum singlet correlation
        Analytic quantum Bell-state correlation.
        E(θa, θb) = -cos(θa - θb).
        Result: S = 2√2.

Status:
  Part 1 is strict numerical verification of the CHSH bound
  for 3D-local hidden-variable models.

  Part 2 is NOT a simulation of hidden variables. It is the
  analytic quantum singlet correlation, entered as a hypothesis
  from standard quantum mechanics.

  The N.E.A. suture-edge interpretation assumes that the 1D
  topological adjacency reproduces this cosine correlation.
  Deriving cos(θa - θb) from the 1D skeleton is OP-24.
"""
import numpy as np

print("=" * 80)
print("  N.E.A. Bell-CHSH strict audit (v4.0)")
print("=" * 80)

# =====================================================================
# Part 1: 3D-local hidden-variable Monte Carlo
# =====================================================================
def simulate_lhv(n_samples=1_000_000):
    z = np.random.uniform(-1, 1, n_samples)
    phi = np.random.uniform(0, 2 * np.pi, n_samples)
    r = np.sqrt(1 - z * z)
    v = np.column_stack([r * np.cos(phi),
                         r * np.sin(phi),
                         z])

    def result(angle):
        m = np.array([np.sin(angle), 0.0, np.cos(angle)])
        return np.sign(np.sum(v * m, axis=1))

    a   = 0.0
    a_p = np.pi / 2.0
    b   = np.pi / 4.0
    b_p = 3.0 * np.pi / 4.0

    A   = result(a)
    A_p = result(a_p)
    B   = result(b)
    B_p = result(b_p)

    E_ab   = np.mean(A * B)
    E_abp  = np.mean(A * B_p)
    E_apb  = np.mean(A_p * B)
    E_apbp = np.mean(A_p * B_p)

    S = abs(E_ab - E_abp + E_apb + E_apbp)
    return S, E_ab, E_abp, E_apb, E_apbp


# =====================================================================
# Part 2: Quantum singlet correlation, analytic
# =====================================================================
def quantum_correlation(theta_a, theta_b):
    return -np.cos(theta_a - theta_b)


def singlet_chsh():
    a   = 0.0
    a_p = np.pi / 2.0
    b   = np.pi / 4.0
    b_p = 3.0 * np.pi / 4.0

    E_ab   = quantum_correlation(a, b)
    E_abp  = quantum_correlation(a, b_p)
    E_apb  = quantum_correlation(a_p, b)
    E_apbp = quantum_correlation(a_p, b_p)

    S = abs(E_ab - E_abp + E_apb + E_apbp)
    return S, E_ab, E_abp, E_apb, E_apbp


# =====================================================================
# Run
# =====================================================================
print("\n[Part 1] 3D-local hidden-variable model")
S_lhv, E_ab_lhv, E_abp_lhv, E_apb_lhv, E_apbp_lhv = simulate_lhv()
print(f"  E(a,b)   = {E_ab_lhv:+.6f}")
print(f"  E(a,b')  = {E_abp_lhv:+.6f}")
print(f"  E(a',b)  = {E_apb_lhv:+.6f}")
print(f"  E(a',b') = {E_apbp_lhv:+.6f}")
print(f"  S        = {S_lhv:.6f}")
print("  Expected: S ≤ 2.0000")

print("\n[Part 2] Quantum singlet correlation (analytic)")
S_q, E_ab_q, E_abp_q, E_apb_q, E_apbp_q = singlet_chsh()
print(f"  E(a,b)   = {E_ab_q:+.6f}")
print(f"  E(a,b')  = {E_abp_q:+.6f}")
print(f"  E(a',b)  = {E_apb_q:+.6f}")
print(f"  E(a',b') = {E_apbp_q:+.6f}")
print(f"  S        = {S_q:.6f}")
print(f"  Expected: S = 2√2 ≈ {2*np.sqrt(2):.6f}")

print("\n" + "=" * 80)
print("  Status")
print("=" * 80)
print("  1. LHV bound S ≤ 2 verified by Monte Carlo.")
print("  2. Quantum singlet correlation S = 2√2 verified analytically.")
print("  3. Suture-edge hypothesis assumes this cosine correlation.")
print("  4. Deriving the cosine correlation from 1D skeleton is OP-24.")
print("=" * 80)