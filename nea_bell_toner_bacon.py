#!/usr/bin/env python3
"""
nea_bell_toner_bacon.py

N.E.A. 1D 骨架因果闭合模型（基于 Toner-Bacon 协议）
核心物理：
1. Alice 和 Bob 共享 1D 骨架的单位球空间关联基底 (lambda_1, lambda_2)。
2. Alice 在角度 a 测量，产生结果 A，并在 1D 骨架上沉淀 1 bit 的带宽劫持标志 m ∈ {-1, +1}。
3. Bob 沿着 1D 骨架接收到这 1 bit 的拓扑锁定，在角度 b 输出结果 B。
4. 验证：能否完全重现 E(a,b) = -cos(a-b) 并达到 Tsirelson 界 S = 2*sqrt(2)？
"""

import numpy as np

N_samples = 1_000_000
rng = np.random.default_rng(42)

print("=" * 76)
print("     N.E.A. 1D 骨架因果闭合 Bell 检验（Toner-Bacon 协议）")
print("=" * 76)

# 1. 1D 骨架在正交方向上的三维随机矢量基底 (模拟八面体 3D 空间的基底展开)
def random_unit_vectors(N):
    # 生成均匀分布在三维球面上的随机单位向量
    phi = rng.uniform(0, 2*np.pi, N)
    costheta = rng.uniform(-1, 1, N)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.stack([x, y, z], axis=1)

lam1 = random_unit_vectors(N_samples)
lam2 = random_unit_vectors(N_samples)

# 2. 测量方向：在 xy 平面上的测量角转化为三维单位矢量
def get_vector(angle):
    return np.array([np.cos(angle), np.sin(angle), 0.0])

# 3. 测量协议 (Alice 测量并向 1D 骨架写入 1 bit 存在税)
def measure(a_angle, b_angle):
    a_vec = get_vector(a_angle)
    b_vec = get_vector(b_angle)
    
    # Alice 处的点积
    a_dot_lam1 = np.sum(lam1 * a_vec, axis=1)
    a_dot_lam2 = np.sum(lam2 * a_vec, axis=1)
    
    # Alice 的测量输出
    A = np.sign(a_dot_lam1)
    
    # Alice 的测量动作在 1D 骨架上留下的 1 bit 拓扑标志 (B = 1 存在税)
    # m 代表骨架两端相位的符号锁定
    m = np.sign(a_dot_lam1) * np.sign(a_dot_lam2)
    
    # Bob 沿着 1D 骨架读取：他的有效基底被 Alice 写入的 1 bit 标志所调制
    # 有效基底 = lam1 + m * lam2
    eff_lam = lam1 + m[:, np.newaxis] * lam2
    b_dot_eff = np.sum(eff_lam * b_vec, axis=1)
    
    # Bob 的测量输出 (单态反相关)
    B = -np.sign(b_dot_eff)
    
    return A, B

def E(a_angle, b_angle):
    A, B = measure(a_angle, b_angle)
    return np.mean(A * B)

# ==============================================================================
# 检验 1：相关函数 E(a,b) 是否为严格的余弦波 -cos(a-b)
# ==============================================================================
print("\n[1] 关联函数 E(a,b) 曲线检验（对比理论 -cos(diff)）：")
print(f"    {'夹角 (rad)':<14} {'模拟 E(a,b)':<16} {'理论 -cos':<16} {'绝对偏差'}")
print("    " + "-" * 56)

test_diffs = [0.0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, 3*np.pi/4, np.pi]
for diff in test_diffs:
    e_sim = E(0.0, diff)
    e_theory = -np.cos(diff)
    print(f"    {diff:<14.4f} {e_sim:<16.4f} {e_theory:<16.4f} {abs(e_sim - e_theory):.6f}")

# ==============================================================================
# 检验 2：CHSH 不等式与 Tsirelson 界计算
# ==============================================================================
print("\n[2] CHSH 不等式测试（选取量子最大违背角：0, pi/2 与 pi/4, 3pi/4）：")
a = 0.0
a_p = np.pi / 2.0
b = np.pi / 4.0
b_p = 3.0 * np.pi / 4.0

E_ab   = E(a, b)
E_abp  = E(a, b_p)
E_apb  = E(a_p, b)
E_apbp = E(a_p, b_p)

# CHSH 表达式 S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')|
S = abs(E_ab - E_abp + E_apb + E_apbp)

print(f"    E(a,  b ) = {E_ab:+.4f}   (理论: {-np.cos(np.pi/4):+.4f})")
print(f"    E(a,  b') = {E_abp:+.4f}   (理论: {-np.cos(3*np.pi/4):+.4f})")
print(f"    E(a', b ) = {E_apb:+.4f}   (理论: {-np.cos(-np.pi/4):+.4f})")
print(f"    E(a', b') = {E_apbp:+.4f}   (理论: {-np.cos(np.pi/4):+.4f})")
print("-" * 56)
print(f"    计算所得 CHSH 值 S = {S:.4f}")
print(f"    经典局域隐变量界 S_classical <= 2.0000")
print(f"    量子力学 Tsirelson 界 S_quantum = 2*sqrt(2) = {2*np.sqrt(2):.4f}")

dev_tsirelson = abs(S - 2*np.sqrt(2))
if S > 2.0:
    print(f"\n    ==> 结论：【成功打破经典贝尔界！】(S = {S:.4f} > 2.0)")
if dev_tsirelson < 0.01:
    print(f"    ==> 结论：【精确命中 Tsirelson 量子极限！】(偏差仅 {dev_tsirelson:.4f})")
print("=" * 76 + "\n")