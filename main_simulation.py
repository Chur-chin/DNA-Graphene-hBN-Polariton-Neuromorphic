"""
DNA Origami - Graphene - hBN Multi-Stage Hybrid Polariton Neuromorphic Simulator
Main execution script
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from config.parameters import Config
from utils.wave_solver import MultiStagePolaritonSolver
from utils.plotting import plot_4panel_with_inset, plot_fermi_sweep_supplementary

def main():
    # Configuration
    config = Config()
    config.print_info()
    
    # Create output directory
    Path("figures").mkdir(exist_ok=True)
    
    # Initialize Multi-Stage Solver
    solver = MultiStagePolaritonSolver(config)
    
    # Input combinations
    inputs = [(0,0), (0,1), (1,0), (1,1)]
    results = {}
    
    print("Running simulations for 4 input combinations...\n")
    
    for a, b in inputs:
        phi_A = a * np.pi
        phi_B = b * np.pi + config.phase_bias
        
        E_total = solver.propagate(phi_A=phi_A, phi_B=phi_B, 
                                  amp_A=config.amp_A, amp_B=config.amp_B)
        I = np.abs(E_total)**2
        
        # Multi-readout
        intensities = []
        for pos in config.readout_points:
            ix = int((pos[0] + config.Lx/2) / config.Lx * config.Nx)
            iy = int((pos[1] + config.Ly/2) / config.Ly * config.Ny)
            ix = np.clip(ix, 0, config.Nx-1)
            iy = np.clip(iy, 0, config.Ny-1)
            intensities.append(I[iy, ix])
        
        avg_I = np.mean(intensities)
        Vout = np.tanh(config.alpha * avg_I)
        binary = 1 if Vout > 0.5 else 0
        
        results[(a,b)] = {
            'avg_intensity': avg_I,
            'Vout': Vout,
            'binary': binary,
            'intensities': intensities
        }
        
        print(f"Input ({a},{b}) → Avg I = {avg_I:.4f}, Vout = {Vout:.4f}, Binary = {binary}")
    
    # Main Figure
    print("\nGenerating Main Figure...")
    fig_main = plot_4panel_with_inset(solver, results, config, 
                                     save_path="figures/main_figure_multi_stage.png")
    
    # Supplementary Figure (Fermi Level Sweep)
    print("Generating Supplementary Figure (Fermi Level Sweep)...")
    fig_supp = plot_fermi_sweep_supplementary(solver, config, 
                                             save_path="figures/supplementary_figure_fermi_sweep.png")
    
    print("\n=== Simulation Completed Successfully ===")
    print("Main Figure saved to: figures/main_figure_multi_stage.png")
    print("Supplementary Figure saved to: figures/supplementary_figure_fermi_sweep.png")
    plt.show()

if __name__ == "__main__":
    main()
