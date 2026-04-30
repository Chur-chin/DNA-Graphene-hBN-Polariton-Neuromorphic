# COMSOL Multiphysics - Multi-Stage DNA-Graphene-hBN Polariton Simulator

## Model Setup (Recommended)

### 1. Model Wizard
- **Space Dimension**: 2D
- **Physics**: Electromagnetic Waves, Frequency Domain (`emw`)
- **Study**: Frequency Domain + Parametric Sweep

### 2. Geometry (Units: μm)
- **DNA Origami Zone** (x = -22 ~ -12 μm):
  - Rectangle 1 (Upper bundle): width=8, height=6, position=(-19, 3)
  - Rectangle 2 (Lower bundle): width=8, height=6, position=(-19, -3)
  - Transition region: smoothed connection

- **Water Region**: Rectangle from x=-14 to x=6 μm (full height)

- **Serpentine Graphene Waveguide**:
  - Use "Parametric Curve" or Spline
  - Equation: y = 0.85*sin(0.72*x) + 0.38*sin(1.85*x) + 0.13*x
  - Width: 1.8~2.2 μm (use "Swept" or "Offset Curve")

- **hBN Output Zone**: Rectangle (x=6 to 22 μm, y=-9 to 9 μm)

### 3. Materials

**Graphene (Surface Current Layer)**:
- Surface Conductivity: User Defined (Kubo formula)
```matlab
sigma = (1i*e^2*Ef)/(pi*hbar^2*(omega + 1i*gamma))
