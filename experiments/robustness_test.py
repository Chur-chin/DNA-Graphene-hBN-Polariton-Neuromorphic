"""
Robustness Test with Noise Injection (Monte Carlo Simulation)
"""

import numpy as np
from pathlib import Path
from config.parameters import Config
from utils.multi_input_solver import MultiInputPolaritonSolver

def robustness_monte_carlo(n_trials=100, noise_level='medium'):
    config = Config()
    solver = MultiInputPolaritonSolver(config)
    
    # Test patterns
    patterns = {
        '00': [0, 0, 0, 0],
        '01': [0, 1, 0, 0],
        '10': [1, 0, 0, 0],
        '11': [1, 1, 1, 1]
    }
    
    results = {level: {'contrast': [], 'accuracy': []} for level in ['low', 'medium', 'high']}
    
    noise_levels = {
        'low': 0.25,
        'medium': 0.55,
        'high': 0.85
    }
    
    print(f"Starting Monte Carlo Robustness Test ({n_trials} trials)...\n")
    
    for noise_name, nl in noise_levels.items():
        print(f"Testing {noise_name} noise level...")
        contrast_list = []
        correct = 0
        
        for trial in range(n_trials):
            # Add noise
            phases = np.zeros(4)
            amps = np.array([1.0, 1.0, 1.0, 1.0])
            
            # Phase noise (DNA twist error)
            phase_noise = np.random.normal(0, nl * np.pi, 4)
            phases += phase_noise
            
            # Amplitude noise
            amp_noise = np.random.normal(1.0, nl * 0.15, 4)
            amps *= amp_noise
            
            # Water loss variation
            water_loss_var = 0.078 * (1 + np.random.normal(0, nl * 0.3))
            
            # Run simulation (simplified)
            E = solver.propagate(phases, amps, Ef=0.6)
            I = np.abs(E)**2
            
            # Multi-readout (hBN zone)
            hbn_I = I[solver.hbn_mask > 0.5]
            avg_I = np.mean(hbn_I) if len(hbn_I) > 0 else 0.0
            
            # Simple classification (threshold based)
            pred = 1 if avg_I > 0.8 else 0
            true = 1 if noise_name != '00' else 0   # simplistic
            
            if pred == true:
                correct += 1
            
            # Contrast calculation (simplified)
            contrast_list.append(avg_I)
        
        accuracy = correct / n_trials
        mean_contrast = np.mean(contrast_list)
        
        results[noise_name]['contrast'] = mean_contrast
        results[noise_name]['accuracy'] = accuracy
        
        print(f"  {noise_name:7} → Accuracy: {accuracy:.1%}, Mean Contrast: {mean_contrast:.4f}")
    
    return results
