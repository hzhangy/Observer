/-
  OP-O3: Z_n Insolvency on the 1D Skeletal Edge
  =============================================
  Reference: N.E.A. Volume O, §8.2, Lemma 8.2.

  H_min(n) = 3/(1+π) + 2π²/n²   (n ≥ 3)
  H_min(2) = 3/(1+π)            (special: H_flow(2) = 0)

  Targets:
    (T1) n = 2: H_min(2) ≤ 1     (solvent)
    (T2) n = 3: H_min(3) > 1     (insolvent)
    (T3) 4 ≤ n ≤ 8: H_min(n) > 1 (insolvent)

  π bounds used: only `Real.pi_gt_three : 3 < π` and
  `Real.pi_lt_four : π < 4`. All other inequalities derived.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

namespace NEA.OPO3

open Real

/-! ## Definitions -/

noncomputable def H_min (n : ℕ) : ℝ :=
  3 / (1 + Real.pi) + 2 * Real.pi ^ 2 / (n : ℝ) ^ 2

noncomputable def H_min_two : ℝ := 3 / (1 + Real.pi)

/-! ## π bounds -/

lemma pi_gt_three' : (3 : ℝ) < Real.pi := Real.pi_gt_three
lemma pi_lt_four' : Real.pi < (4 : ℝ) := Real.pi_lt_four

/-! ## Helper: positive denominator -/

lemma one_plus_pi_pos : (0 : ℝ) < 1 + Real.pi := by linarith [pi_gt_three']

/-! ## Helper: π² > 9 -/

lemma pi_sq_gt_nine : (9 : ℝ) < Real.pi ^ 2 := by
  nlinarith [pi_gt_three']

/-! ## Polynomial positivity for n ∈ [4, 8]

  P(n) := 2π³ + 2π² − n²π + 2n²
        = (π−3)(2π² + 8π + 24 − n²) + (72 − n²)

  Both summands ≥ 0 when π > 3 and n ≤ 8.
-/

lemma P_pos (n : ℕ) (_hn4 : 4 ≤ n) (hn8 : n ≤ 8) :
    2 * Real.pi ^ 3 + 2 * Real.pi ^ 2 - (n : ℝ) ^ 2 * Real.pi
      + 2 * (n : ℝ) ^ 2 > 0 := by
  have hfact :
      2 * Real.pi ^ 3 + 2 * Real.pi ^ 2 - (n : ℝ) ^ 2 * Real.pi
        + 2 * (n : ℝ) ^ 2
      = (Real.pi - 3) * (2 * Real.pi ^ 2 + 8 * Real.pi + 24 - (n : ℝ) ^ 2)
        + (72 - (n : ℝ) ^ 2) := by ring
  rw [hfact]
  -- First summand ≥ 0
  have h1 : (Real.pi - 3) ≥ 0 := by linarith [pi_gt_three']
  have hn2 : (n : ℝ) ^ 2 ≤ 64 := by
    have : (n : ℝ) ≤ 8 := by exact_mod_cast hn8
    have : (n : ℝ) ≥ 0 := by exact_mod_cast (Nat.zero_le n)
    nlinarith
  have h2 : 2 * Real.pi ^ 2 + 8 * Real.pi + 24 - (n : ℝ) ^ 2 > 0 := by
    nlinarith [pi_sq_gt_nine]
  have hprod : (Real.pi - 3) * (2 * Real.pi ^ 2 + 8 * Real.pi + 24 - (n : ℝ) ^ 2) ≥ 0 :=
    mul_nonneg h1 (le_of_lt h2)
  -- Second summand ≥ 8 > 0
  have h3 : (72 : ℝ) - (n : ℝ) ^ 2 ≥ 8 := by linarith
  linarith

/-! ## Helper: n² > 0 for n ≥ 4 -/

lemma n_sq_pos (n : ℕ) (hn4 : 4 ≤ n) : (0 : ℝ) < (n : ℝ) ^ 2 := by
  have : (4 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn4
  nlinarith

/-! ## T1: Z_2 is solvent: 3/(1+π) ≤ 1 -/

theorem Z2_solvent : H_min_two ≤ 1 := by
  unfold H_min_two
  -- Since π > 3, we have 1 + π > 4 > 3, hence 3/(1+π) < 1.
  have h : (3 : ℝ) < 1 + Real.pi := by linarith [pi_gt_three']
  exact (div_lt_one one_plus_pi_pos).mpr h |>.le

/-! ## T2: Z_3 is insolvent: 1 < 3/(1+π) + 2π²/9 -/

theorem Z3_insolvent : 1 < H_min 3 := by
  unfold H_min
  -- Key: 2π²/9 > 2 > 1, and 3/(1+π) > 0.
  have h_flow_gt_one : (1 : ℝ) < 2 * Real.pi ^ 2 / 9 := by
    calc (1 : ℝ)
        = 9 / 9 := by norm_num
      _ < 2 * Real.pi ^ 2 / 9 := by
          gcongr
          nlinarith [pi_sq_gt_nine]
  have h_coord_pos : (0 : ℝ) < 3 / (1 + Real.pi) :=
    div_pos (by norm_num) one_plus_pi_pos
  linarith

/-! ## T3: Z_n insolvent for 4 ≤ n ≤ 8 -/

theorem Zn_insolvent_4_to_8 (n : ℕ) (hn4 : 4 ≤ n) (hn8 : n ≤ 8) :
    1 < H_min n := by
  unfold H_min
  have hP :
      2 * Real.pi ^ 3 + 2 * Real.pi ^ 2 - (n : ℝ) ^ 2 * Real.pi
        + 2 * (n : ℝ) ^ 2 > 0 :=
    P_pos n hn4 hn8
  have hpos : (0 : ℝ) < 1 + Real.pi := one_plus_pi_pos
  have hn2_pos : (0 : ℝ) < (n : ℝ) ^ 2 := n_sq_pos n hn4
  have h_denom : (0 : ℝ) < (n : ℝ) ^ 2 * (1 + Real.pi) := by positivity
  -- Multiply both sides of the goal by n²(1+π) > 0.
  -- Goal becomes: n²(1+π) < 3n² + 2π²(1+π)
  -- i.e.  2π³ + 2π² − n²π + 2n² > 0   (exactly P_pos)
  suffices h_suff :
      (1 : ℝ) * ((n : ℝ) ^ 2 * (1 + Real.pi)) <
      (3 / (1 + Real.pi) + 2 * Real.pi ^ 2 / (n : ℝ) ^ 2)
        * ((n : ℝ) ^ 2 * (1 + Real.pi)) by
    exact (mul_lt_mul_iff_of_pos_right h_denom).mp h_suff
  have h1 : (1 : ℝ) * ((n : ℝ) ^ 2 * (1 + Real.pi))
           = (n : ℝ) ^ 2 * (1 + Real.pi) := by ring
  have h2 :
      (3 / (1 + Real.pi) + 2 * Real.pi ^ 2 / (n : ℝ) ^ 2)
        * ((n : ℝ) ^ 2 * (1 + Real.pi))
      = 3 * (n : ℝ) ^ 2 + 2 * Real.pi ^ 2 * (1 + Real.pi) := by
    field_simp
  rw [h1, h2]
  -- Goal: n²(1+π) < 3n² + 2π²(1+π), i.e. P > 0
  nlinarith [hP]

end NEA.OPO3
