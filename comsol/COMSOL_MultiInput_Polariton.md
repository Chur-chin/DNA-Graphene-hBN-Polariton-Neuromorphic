# COMSOL Multiphysics - Multi-Input DNA-Graphene-hBN Polariton System

## Model Information
- **Physics**: Electromagnetic Waves, Frequency Domain (emw)
- **Study Type**: Frequency Domain + Parametric Sweep

## Geometry (Unit: μm)
- **DNA Origami Input Zone**: 4 rectangular bundles at x ≈ -19 μm
  - Channel 1: y = 5.5, width=4.2, height=5.6
  - Channel 2: y = 2.0
  - Channel 3: y = -2.0
  - Channel 4: y = -5.5

- **Water Region**: x = -15 ~ +6 μm
- **Serpentine Graphene Waveguide**: Parametric curve (Spline)
  - y = 0.85*sin(0.72*x) + 0.38*sin(1.85*x) + 0.13*x
  - Width = 2.0 μm
- **hBN Output Zone**: Rectangle (x=6~23 μm, y=-9.5~9.5 μm)

## Materials
**Graphene** (Surface Current):
- Conductivity: Kubo formula (user-defined function)
```matlab
sigma = (1i*e_const^2*Ef)/(pi*hbar^2*(2*pi*f + 1i*gamma))
