[[Welcome]]


|     |     |
| --- | --- |
|     |     |
```
# ------------------ Constants ------------------

e = 1.602e-19  # Elementary charge in C

kb = 1.38e-23  # Boltzmann constant in J/K

me = 9.11e-31  # Electron mass in kg

mi = 1.67e-27  # Ion mass (proton) in kg

ProbeDia = 3e-3  # Probe diameter in m

Aprobe = np.pi * (ProbeDia / 2) ** 2

ne = 1e16

ni = 1e16

Tp = 0.03

V_min = -20

V_max = 20

V_points = 1000

V_range = np.linspace(V_min, V_max, V_points)
```
$$\omega _{p} = \sqrt{\frac{n_{e}e^{2}}{\varepsilon _{0}m_{e}}}$$
![[Argon Plasma Comsol Multiphysics.canvas]]