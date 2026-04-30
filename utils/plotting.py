"""
Publication-quality plotting module for Multi-Stage DNA-Graphene-hBN Polariton System
- Main 4-panel figure
- Supplementary Fermi Level Sweep Figure (완전 연동 버전)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import PowerNorm
import matplotlib.patheffects as path_effects
from pathlib import Path


def plot_4panel_with_inset(solver, results, config, save_path=None):
    """Main Figure: 4-panel intensity distribution"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12), dpi=300)
    axes = axes.ravel()

    inputs = [(0,0), (0,1), (1,0), (1,1)]
    titles = ['(a) Input 00', '(b) Input 01', '(c) Input 10', '(d) Input 11']

    intensities = {}
    for a, b in inputs:
        phi_A = a * np.pi
        phi_B = b * np.pi + config.phase_bias
        E = solver.propagate(phi_A=phi_A, phi_B=phi_B, 
                           amp_A=config.amp_A, amp_B=config.amp_B, Ef=config.Ef)
        intensities[(a,b)] = np.abs(E)**2

    global_max = max(I.max() for I in intensities.values())

    for i, (inp, title) in enumerate(zip(inputs, titles)):
        ax = axes[i]
        I_norm = intensities[inp] ** 0.55   # contrast enhancement

        im = ax.imshow(I_norm, 
                       extent=[-config.Lx/2, config.Lx/2, -config.Ly/2, config.Ly/2],
                       origin='lower', 
                       cmap='plasma', 
                       norm=PowerNorm(gamma=0.55, vmin=0, vmax=global_max**0.55))

        # Zone overlays
        ax.contour(solver.graphene_mask, levels=[0.5], colors='white', linewidths=2.8, alpha=0.9)
        
        # DNA Origami Zone
        ax.add_patch(Rectangle((-21, -6), 10, 12, fill=False, edgecolor='magenta', 
                              linestyle='--', linewidth=2.2, alpha=0.85))
        ax.text(-19, 7, 'DNA Origami', color='magenta', fontsize=11, fontweight='bold',
                path_effects=[path_effects.withStroke(linewidth=3, foreground='white')])

        # hBN Output Zone
        ax.add_patch(Rectangle((5, -9), 18, 18, fill=False, edgecolor='cyan', 
                              linestyle='--', linewidth=2.8, alpha=0.9))
        ax.text(12, 10, 'hBN Zone', color='cyan', fontsize=11, fontweight='bold',
                path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])

        # Readout points
        for pos in config.readout_points:
            ax.plot(pos[0], pos[1], '*', color='red', markersize=13, 
                   markeredgecolor='white', markeredgewidth=2)

        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.set_xlabel('x (μm)', fontsize=12)
        ax.set_ylabel('y (μm)', fontsize=12)
        ax.grid(False)

    # Colorbar
    cbar = fig.colorbar(im, ax=axes.tolist(), shrink=0.82, pad=0.02)
    cbar.set_label('|E|² (normalized)', fontsize=13)

    # Scale bar
    scale_ax = axes[3]
    scale_ax.plot([-20, -15], [-14.5, -14.5], 'w-', linewidth=5)
    scale_ax.text(-17.5, -15.8, '5 μm', color='white', ha='center', va='top', 
                 fontsize=12, fontweight='bold')

    fig.suptitle('Multi-Stage Hybrid Polariton Neuromorphic Platform\n'
                 'DNA Origami → Water → Serpentine Graphene → hBN\n'
                 f'Dual-frequency THz (5.0 & 5.8 THz), Ef = {config.Ef} eV', 
                 fontsize=16, fontweight='bold', y=0.96)

    plt.tight_layout(rect=[0, 0, 1, 0.94])

    if save_path:
        Path(save_path).parent.mkdir(exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Main Figure saved: {save_path}")

    return fig


def plot_fermi_sweep_supplementary(results, ef_values, config, save_path=None):
    """
    Supplementary Figure: Fermi Level Sweep Analysis
    results: dict with structure {Ef: {(a,b): {'avg_intensity': , 'Vout': , 'binary': }}}
    """
    fig = plt.figure(figsize=(16, 13), dpi=300)
    
    # (a) Average Intensity Bar Plot
    ax1 = plt.subplot(2, 2, 1)
    x = np.arange(4)
    width = 0.18
    labels = ['00', '01', '10', '11']
    
    for i, Ef in enumerate(ef_values):
        intensities = [results[Ef][inp]['avg_intensity'] for inp in [(0,0),(0,1),(1,0),(1,1)]]
        ax1.bar(x + i*width - width*1.5, intensities, width=width, label=f'Ef = {Ef} eV', alpha=0.9)
    
    ax1.set_title('(a) Average Intensity at Multi-Readout', fontsize=14, fontweight='bold')
    ax1.set_ylabel('|E|² (a.u.)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # (b) Vout Heatmap
    ax2 = plt.subplot(2, 2, 2)
    vout_matrix = np.zeros((len(ef_values), 4))
    for i, Ef in enumerate(ef_values):
        for j, inp in enumerate([(0,0),(0,1),(1,0),(1,1)]):
            vout_matrix[i, j] = results[Ef][inp]['Vout']
    
    im = ax2.imshow(vout_matrix, cmap='viridis', aspect='auto')
    ax2.set_yticks(range(len(ef_values)))
    ax2.set_yticklabels([f'{ef}' for ef in ef_values])
    ax2.set_xticks(range(4))
    ax2.set_xticklabels(labels)
    ax2.set_title('(b) Vout after tanh(α·I) Mapping', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Input Combination')
    ax2.set_ylabel('Fermi Level Ef (eV)')
    plt.colorbar(im, ax=ax2, label='Vout')

    # (c) Contrast Analysis
    ax3 = plt.subplot(2, 2, 3)
    contrasts = []
    for Ef in ef_values:
        I00 = results[Ef][(0,0)]['avg_intensity']
        I_exc = (results[Ef][(0,1)]['avg_intensity'] + results[Ef][(1,0)]['avg_intensity']) / 2
        contrast = I_exc - I00
        contrasts.append(contrast)
    
    ax3.plot(ef_values, contrasts, 'o-', color='red', linewidth=2.5, markersize=8)
    ax3.set_title('(c) Contrast (EPSP - IPSP)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Graphene Fermi Level Ef (eV)')
    ax3.set_ylabel('Contrast (Δ|E|²)')
    ax3.grid(True, alpha=0.3)

    # (d) Example Intensity Map at optimal Ef
    ax4 = plt.subplot(2, 2, 4)
    optimal_ef = 0.6
    if optimal_ef in results:
        I_opt = np.abs(solver.propagate(phi_A=np.pi, phi_B=np.pi, 
                                      amp_A=config.amp_A, amp_B=config.amp_B, Ef=optimal_ef))**2 ** 0.55
        im4 = ax4.imshow(I_opt, extent=[-config.Lx/2, config.Lx/2, -config.Ly/2, config.Ly/2],
                        origin='lower', cmap='plasma')
        ax4.set_title(f'(d) |E|² at Ef = {optimal_ef} eV (Input 11)', fontsize=13)
        plt.colorbar(im4, ax=ax4, shrink=0.8)

    fig.suptitle('Supplementary Figure S1. Effect of Graphene Fermi Level Tuning\n'
                 'on Multi-Stage Hybrid Polariton Neuromorphic Response', 
                 fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    if save_path:
        Path(save_path).parent.mkdir(exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Supplementary Fermi Sweep Figure saved: {save_path}")

    return fig
