"""
Multi-Input (4-source) Polariton Solver for Spatial Summation Study
DNA Origami zone에 4개의 독립적인 THz source를 배치
"""

import numpy as np
from scipy.fft import fft2, ifft2, fftfreq

class MultiInputPolaritonSolver:
    def __init__(self, config):
        self.config = config
        self.Nx, self.Ny = config.Nx, config.Ny
        self.Lx, self.Ly = config.Lx, config.Ly
        self.dx = self.Lx / self.Nx
        self.dy = self.Ly / self.Ny
        
        self.x = np.linspace(-self.Lx/2, self.Lx/2, self.Nx)
        self.y = np.linspace(-self.Ly/2, self.Ly/2, self.Ny)
        self.X, self.Y = np.meshgrid(self.x, self.y, indexing='xy')
        
        # Fourier grid
        self.kx = 2 * np.pi * fftfreq(self.Nx, d=self.dx)
        self.ky = 2 * np.pi * fftfreq(self.Ny, d=self.dy)
        self.KX, self.KY = np.meshgrid(self.kx, self.ky, indexing='xy')
        self.K2 = self.KX**2 + self.KY**2
        
        self.k0 = 3.0
        
        # 4-channel DNA Origami masks
        self.dna_masks = self._create_4channel_dna_origami()
        self.transition_mask = self._create_transition_zone()
        self.graphene_mask = self._create_serpentine_graphene()
        self.hbn_mask = self._create_hbn_output_zone()
        
        print("Multi-Input (4-source) Polariton Solver initialized.")

    def _create_4channel_dna_origami(self):
        """4개의 독립적인 DNA bundle channel"""
        masks = []
        y_centers = [5.5, 2.0, -2.0, -5.5]
        for yc in y_centers:
            mask = np.zeros((self.Ny, self.Nx))
            mask |= (np.abs(self.X + 18.5) < 4.2) & (np.abs(self.Y - yc) < 2.8)
            masks.append(mask.astype(float))
        return masks

    def _create_transition_zone(self):
        mask = np.zeros((self.Ny, self.Nx))
        mask |= (np.abs(self.X + 13.0) < 7.0) & (np.abs(self.Y) < 8.0)
        return mask.astype(float)

    def _create_serpentine_graphene(self):
        y_path = 0.85*np.sin(0.72*self.X) + 0.38*np.sin(1.85*self.X) + 0.13*self.X
        thickness = 1.9
        mask = np.abs(self.Y - y_path) < thickness
        mask |= np.abs(self.Y - (y_path + 0.7*np.sin(0.45*self.X))) < 1.0
        return mask.astype(float)

    def _create_hbn_output_zone(self):
        return ((self.X > 5.0) & (np.abs(self.Y) < 9.0)).astype(float)

    def propagate(self, phases, amps, Ef=0.55):
        """
        phases: list or array of 4 phases (radians)
        amps: list or array of 4 amplitudes
        """
        E = np.zeros((self.Ny, self.Nx), dtype=complex)
        
        # 1. DNA Origami Zone - 4 independent sources
        for i in range(4):
            phase_mod = 3.8 * np.sin(1.45 * self.Y + i * np.pi / 2)  # channel-specific modulation
            contrib = amps[i] * np.exp(1j * (phases[i] + phase_mod))
            E += contrib * self.dna_masks[i]
        
        # 2. Transition zone
        E[self.transition_mask > 0] *= (1.15 + 0.7j)
        
        # 3. Water region (realistic loss)
        E *= np.exp(-0.078 * np.abs(self.X + 6))
        
        # 4. Graphene plasmon with Fermi level tuning
        graphene_factor = (1.82 + 0.48j) * (Ef / 0.45)
        E += E * self.graphene_mask * graphene_factor
        
        # 5. hBN phonon polariton output
        E[self.hbn_mask > 0] *= (1.48 + 1.28j)
        
        # Global damping
        E *= np.exp(-0.052 * np.abs(self.X) / 28)
        
        # Pseudospectral propagation
        E_fft = fft2(E)
        propagator = np.exp(-0.019 * np.sqrt(self.K2)) * np.exp(1j * 0.37 * np.sqrt(self.K2))
        E = ifft2(E_fft * propagator)
        
        return E
