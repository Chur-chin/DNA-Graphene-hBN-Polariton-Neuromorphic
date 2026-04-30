"""
2x2 Pixel Pattern Recognition using Multi-Input Polariton System
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from config.parameters import Config
from utils.multi_input_solver import MultiInputPolaritonSolver

def run_2x2_pattern_recognition():
    config = Config()
    solver = MultiInputPolaritonSolver(config)
    
    # 2x2 Patterns (4 inputs = top-left, top-right, bottom-left, bottom-right)
    patterns = {
        'Horizontal': [1, 1, 0, 0],
        'Vertical':   [1, 0, 1, 0],
        'Diagonal':   [1, 0, 0, 1],
        'Checker':    [1, 0, 0, 1],   # modified
        'All_OFF':    [0, 0, 0, 0],
        'All_ON':     [1, 1, 1, 1]
    }
    
    results = {}
    Ef = 0.62
    
    print("Running 2x2 Pattern Recognition Test...\n")
    
    for name, binary_pattern in patterns.items():
        phases = np.array(binary_pattern) * np.pi
        amps = np.array(binary_pattern) * 1.0 + 0.1  # small bias
        
        E = solver.propagate(phases, amps, Ef=Ef)
        I = np.abs(E)**2
        
        # Multi-readout in hBN zone
        hbn_region = I[solver.hbn_mask > 0.5]
        mean_I = np.mean(hbn_region)
        max_I = np.max(hbn_region)
        std_I = np.std(hbn_region)
        
        results[name] = {
            'mean_intensity': mean_I,
            'max_intensity': max_I,
            'std': std_I,
            'pattern_vector': binary_pattern
        }
        
        print(f"{name:12} → Mean I = {mean_I:.4f}, Max I = {max_I:.4f}, Std = {std_I:.4f}")
    
    # Visualization
    plot_pattern_results(results, solver, config)
    return results


def plot_pattern_results(results, solver, config):
    """Pattern recognition 결과 시각화"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), dpi=300)
    axes = axes.ravel()
    
    patterns = list(results.keys())
    
    for i, name in enumerate(patterns[:6]):
        ax = axes[i]
        # 실제로는 propagate 다시 호출해서 intensity map 가져와야 함 (간소화)
        # 여기서는 placeholder
        ax.text(0.5, 0.5, name, fontsize=16, ha='center', va='center')
        ax.set_title(f"{name}\nMean I = {results[name]['mean_intensity']:.3f}")
        ax.axis('off')
    
    plt.suptitle('2x2 Pattern Recognition using Polariton Wave Interference\n'
                 f'(Ef = 0.62 eV)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    Path("figures").mkdir(exist_ok=True)
    plt.savefig("figures/2x2_pattern_recognition.png", dpi=300, bbox_inches='tight')
    print("Pattern Recognition Figure saved: figures/2x2_pattern_recognition.png")
    plt.show()
