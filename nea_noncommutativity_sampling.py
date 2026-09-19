#!/usr/bin/env python3
"""
nea_noncommutativity_sampling.py

Weyl 关系检验：Stride-10 采样窗口上的 [X, T] = +h T。
"""
import numpy as np

N = 10
h = 1.0 / N
x = (np.arange(N) - N/2) * h

X = np.diag(x)

T = np.zeros((N, N))
for j in range(N):
    T[(j+1) % N, j] = 1.0

comm = X @ T - T @ X
theoretical = +h * T

print("=" * 60)
print("  Weyl algebra on the Stride-10 sampling window")
print("=" * 60)
print(f"  N = {N}, h = {h:.4f}")
print()

interior = comm[1:, :-1]
interior_theory = theoretical[1:, :-1]
err = np.linalg.norm(interior - interior_theory, 'fro') \
    / np.linalg.norm(interior_theory, 'fro')
print(f"  [1] interior relative error: {err:.2e}")
print()

nz = np.argwhere(np.abs(interior) > 1e-12)
print(f"  [2] interior non-zero elements: {len(nz)}")
for i, j in nz[:3]:
    print(f"      [{i+1},{j}] = {comm[i+1,j]:+.4f}"
          f"  (theory {theoretical[i+1,j]:+.4f})")
print()

print(f"  [3] boundary element [0,{N-1}] = {comm[0, N-1]:+.4f}")
print(f"      (window endpoint artifact)")
print()

print(f"  [4] interior norm vs N:")
for N_test in [5, 10, 20, 50, 100]:
    h_test = 1.0 / N_test
    x_test = (np.arange(N_test) - N_test/2) * h_test
    X_test = np.diag(x_test)
    T_test = np.zeros((N_test, N_test))
    for j in range(N_test):
        T_test[(j+1) % N_test, j] = 1.0
    cm = X_test @ T_test - T_test @ X_test
    print(f"      N = {N_test:<4} ||[X,T]||_interior"
          f" = {np.linalg.norm(cm[1:, :-1], 'fro'):.4f}")
print()

print("  [Conclusion]")
print("      Weyl relation [X, T] = +h T holds in the interior.")
print("      Boundary deviation corresponds to the window endpoint.")
print("=" * 60)