#!/usr/bin/env python3
"""
nea_hydrogen_convergence.py
收敛性研究：dx → 0 时，C8 格点上的氢原子能级是否收敛到 -13.6 eV？
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def solve_hydrogen(L, dx):
    """在 L×L×L 格点上求解氢原子基态"""
    N = L**3
    center = L//2
    
    # 1D 拉普拉斯
    off = np.ones(L-1)
    diag = -2*np.ones(L)
    Lap1 = sp.diags([off, diag, off], [-1,0,1], shape=(L,L)) / dx**2
    I = sp.eye(L)
    Lap3 = sp.kronsum(Lap1, sp.kronsum(Lap1, Lap1))
    T = -0.5 * Lap3
    
    # 库仑势（无涂抹，用 dx/2 截断原点）
    V = np.zeros(N)
    for i in range(L):
        for j in range(L):
            for k in range(L):
                r = np.sqrt((i-center)**2+(j-center)**2+(k-center)**2)*dx
                r = max(r, dx/2)
                V[i*L*L+j*L+k] = -1.0/r
    
    H = T + sp.diags(V)
    vals, _ = spla.eigsh(H, k=1, sigma=-0.6, which='LM')
    return vals[0]

print("="*60)
print("  C8 格点氢原子收敛性研究")
print("="*60)
print(f"  {'dx (a0)':<10} {'L':<6} {'E1 (Hartree)':<15} {'E1 (eV)':<12} {'偏差':<10}")
print("-"*55)

configs = [(15, 0.8), (20, 0.5), (25, 0.4), (30, 0.3), (40, 0.25)]
for L, dx in configs:
    E = solve_hydrogen(L, dx)
    E_eV = E * 27.2114
    dev = abs(E_eV/(-13.6057)-1)*100
    print(f"  {dx:<10.2f} {L:<6d} {E:<15.6f} {E_eV:<12.4f} {dev:<8.2f}%")

print("-"*55)
print("  理论极限 (dx→0): E1 = -0.5 Hartree = -13.6057 eV")
print("  如果偏差随 dx 减小而趋向 0，说明 C8 格点正确收敛。")
print("="*60)