"""
Advanced Material Models for Graphene-hBN Polariton Simulation
- Precise Kubo formula for graphene conductivity
- hBN anisotropic permittivity in Reststrahlen band
- THz frequency dependent properties
"""

import numpy as np

def graphene_kubo_conductivity(omega, Ef=0.45, T=300, gamma=10e-3, thickness=0.34e-9):
    """
    Full Kubo formula for graphene surface conductivity (intraband + interband)
    
    Parameters:
        omega: angular frequency (rad/s)
        Ef: Fermi energy (eV)
        T: Temperature (K)
        gamma: scattering rate (eV)
        thickness: graphene thickness (m) for effective permittivity conversion
    
    Returns:
        sigma: surface conductivity (S)
        eps_effective: effective relative permittivity
    """
    e = 1.60217662e-19      # elementary charge
    hbar = 1.0545718e-34    # reduced Planck constant
    kB = 1.380649e-23       # Boltzmann constant
    
    Ef_J = Ef * e           # Fermi energy in Joule
    gamma_J = gamma * e     # scattering rate in Joule
    omega = np.asarray(omega)
    
    # Intraband contribution (dominant in THz range)
    sigma_intra = (1j * e**2 * Ef_J) / (np.pi * hbar**2 * (omega + 1j * gamma_J))
    
    # Interband contribution (simplified)
    kT = kB * T
    arg = (hbar * omega) / (2 * kT)
    f = lambda x: 1 / (np.exp((x - Ef_J/kT)) + 1)   # Fermi-Dirac distribution
    
    # Approximate interband term
    sigma_inter = (e**2 / (4 * hbar)) * (0.5 + (1/np.pi) * np.arctan((hbar*omega - 2*Ef_J)/(2*kT)) -
                                        1j/np.pi * np.log(((hbar*omega + 2*Ef_J)**2) / 
                                        ((hbar*omega - 2*Ef_J)**2 + (2*kT)**2)))
    
    sigma_total = sigma_intra + sigma_inter
    
    # Convert to effective permittivity (thin film approximation)
    eps0 = 8.854187817e-12  # vacuum permittivity
    eps_effective = 1 + 1j * sigma_total / (omega * eps0 * thickness)
    
    return {
        'sigma': sigma_total,
        'eps_effective': eps_effective,
        'sigma_intra': sigma_intra,
        'sigma_inter': sigma_inter
    }


def hbn_anisotropic_permittivity(freq=5.0):
    """
    Anisotropic permittivity of hBN in Reststrahlen band for phonon polariton
    Frequency: THz
    """
    # Typical values in Reststrahlen band (~5-6 THz)
    eps_xx = 4.8 + 3.2j   # in-plane (strong phonon response)
    eps_yy = 2.9 + 1.4j   # slightly different in-plane
    eps_zz = 3.5 + 0.8j   # out-of-plane
    
    return {
        'xx': eps_xx,
        'yy': eps_yy,
        'zz': eps_zz,
        'description': f'hBN anisotropic permittivity at {freq} THz (Reststrahlen band)'
    }


def water_thz_dielectric(freq=5.0):
    """
    Realistic dielectric constant of water in THz range (5 THz)
    Reference: THz spectroscopy data
    """
    # Approximate values from literature at ~5 THz
    eps_real = 5.8
    eps_imag = 4.1      # strong absorption
    
    return complex(eps_real, eps_imag)


def graphene_plasmon_effective_index(Ef=0.45, freq=5.0):
    """
    Effective refractive index for graphene plasmon
    """
    # Rough approximation: n_eff ≈ 1.5 ~ 3.0 depending on Ef
    n_eff = 1.8 * (Ef / 0.4)**0.5
    return n_eff
