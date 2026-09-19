#!/usr/bin/env python3
"""
nea_interference_sampling.py

验证：Stride-10 采样窗口的线性性是否给出干涉和延迟擦除？

物理设置：
    - 两条路径，振幅 e^{iφ₁}, e^{iφ₂}
    - Case 1：无 which-path 信息 → 两条路径相位叠加 → 干涉
    - Case 2：有 which-path 信息，编码到环境 → 迹掉环境后干涉消失
"""
import numpy as np

N_trials = 100000
rng = np.random.default_rng(42)

# 路径相位
phi1 = rng.uniform(0, 2*np.pi, N_trials)
phi2 = rng.uniform(0, 2*np.pi, N_trials)

print("=" * 70)
print("  干涉和延迟擦除的采样窗口验证")
print("=" * 70)
print()

# =====================================================
# Case 1: 相干叠加
# =====================================================
psi1 = np.exp(1j * phi1) / np.sqrt(2)
psi2 = np.exp(1j * phi2) / np.sqrt(2)
psi = psi1 + psi2
prob_coherent = np.abs(psi)**2

print(f"  [Case 1] 无 which-path 信息：")
print(f"      样本数 = {N_trials}")
print(f"      <P> = {prob_coherent.mean():.4f}  (理论上 = 1.0)")
print(f"      std(P) = {prob_coherent.std():.4f}  (干涉振荡幅度)")
print()

# =====================================================
# Case 2: 有 which-path 信息（环境相位）
# =====================================================
# 环境相位与路径关联
theta_env = rng.uniform(0, 2*np.pi, N_trials)
psi1_env = np.exp(1j * (phi1 + theta_env)) / np.sqrt(2)
psi2_env = np.exp(1j * (phi2 - theta_env)) / np.sqrt(2)
psi_env = psi1_env + psi2_env
prob_env = np.abs(psi_env)**2

print(f"  [Case 2] 有 which-path 信息（环境相位）：")
print(f"      <P> = {prob_env.mean():.4f}")
print(f"      std(P) = {prob_env.std():.4f}")
print()

# =====================================================
# Case 3: 环境相位被迹掉
# =====================================================
# 这是 Case 2 的物理含义：观察者看不到 θ_env
# 那么 σ(P) 应该接近 0（无干涉项）
# 通过采样多次 θ_env 平均来模拟

prob_avg = np.zeros(N_trials)
for _ in range(100):
    theta_i = rng.uniform(0, 2*np.pi, N_trials)
    p1 = np.exp(1j * (phi1 + theta_i)) / np.sqrt(2)
    p2 = np.exp(1j * (phi2 - theta_i)) / np.sqrt(2)
    prob_avg += np.abs(p1 + p2)**2
prob_avg /= 100

print(f"  [Case 3] 环境相位被平均（观察者无法分辨）：")
print(f"      <P> = {prob_avg.mean():.4f}")
print(f"      std(P) = {prob_avg.std():.4f}  (应该 ≈ 0)")
print()

# =====================================================
# 结论
# =====================================================
print(f"  [结论]：")
if prob_coherent.std() > 0.3:
    print(f"      ✓ Case 1 有强干涉（std = {prob_coherent.std():.3f}）")
else:
    print(f"      ✗ Case 1 干涉弱")

if prob_avg.std() < 0.1:
    print(f"      ✓ Case 3 干涉被擦除（std = {prob_avg.std():.4f}）")
else:
    print(f"      ✗ Case 3 干涉未被擦除（std = {prob_avg.std():.4f}）")
print("=" * 70)