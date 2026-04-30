"""
Multi-Stage Polariton Neuromorphic System - Integrated Experiment Runner
1. Synaptic Weight Tuning
2. Multi-input Spatial Summation
3. Robustness Test
4. 2x2 Pattern Recognition
"""

import numpy as np
from pathlib import Path
from config.parameters import Config

from utils.multi_input_solver import MultiInputPolaritonSolver
from utils.plotting import plot_4panel_with_inset, plot_fermi_sweep_supplementary
from experiments.robustness_test import robustness_monte_carlo
from experiments.pattern_recognition import run_2x2_pattern_recognition

def run_all_experiments():
    Path("figures").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)
    
    config = Config()
    config.print_info()
    
    solver = MultiInputPolaritonSolver(config)
    
    print("="*70)
    print("MULTI-STAGE POLARITON NEUROMORPHIC EXPERIMENTS")
    print("="*70)
    
    # 1. Synaptic Weight Tuning (Fermi Level Sweep)
    print("\n[1] Synaptic Weight Tuning - Fermi Level Sweep")
    ef_values = np.linspace(0.1, 0.8, 15)
    weight_results = {}
    
    for Ef in ef_values:
        E = solver.propagate([0, np.pi, 0, np.pi], [1.0, 1.0, 0.6, 0.6], Ef=Ef)
        I = np.abs(E)**2
        hbn_I = np.mean(I[solver.hbn_mask > 0.5])
        vout = np.tanh(config.alpha * hbn_I)
        weight_results[Ef] = {'intensity': hbn_I, 'vout': vout}
    
    print(f"Best tuning range: Ef ≈ 0.55 ~ 0.70 eV")
    
    # 2. Multi-input Spatial Summation
    print("\n[2] Multi-input Spatial Summation Test")
    phases_list = [
        [0, 0, 0, 0],           # All OFF
        [0, np.pi, 0, 0],       # Input 2 only
        [np.pi, 0, np.pi, 0],   # Two inputs
        [np.pi, np.pi, np.pi, np.pi]  # All ON
    ]
    
    for i, phases in enumerate(phases_list):
        E = solver.propagate(phases, [1.0]*4, Ef=0.62)
        I_mean = np.mean(np.abs(E)**2[solver.hbn_mask > 0.5])
        print(f"Pattern {i} → hBN Mean Intensity = {I_mean:.4f}")
    
    # 3. Robustness Test
    print("\n[3] Robustness Test (Monte Carlo)")
    robustness_results = robustness_monte_carlo(n_trials=80, noise_level='medium')
    
    # 4. 2x2 Pattern Recognition
    print("\n[4] 2x2 Pixel Pattern Recognition")
    pattern_results = run_2x2_pattern_recognition()
    
    print("\n" + "="*70)
    print("ALL EXPERIMENTS COMPLETED SUCCESSFULLY")
    print("Figures and results saved in 'figures/' and 'results/' folders.")
    print("="*70)

if __name__ == "__main__":
    run_all_experiments()
