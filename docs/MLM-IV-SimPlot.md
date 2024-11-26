---
​---
title: Live Share
permalink: /MLM-IV/MLM-IV-SimPlot/
​---
---

# MLM-IV-SIMPLOT

[**INDEX**](index.md)

The MLM-TheoryPlots generates one plot:

1.  Simulated IV curves of a number of different electron temperatures (point plot) including the capacitive effect on measured current, and added leakage currents for both ions and electrons, hereto the data are sampled using a gaussian noise function to create a realistic experimental data set - the theoretical curve by Merlino 2007 is shown as a solid line.
2. Data files with the average current for each curve are saved in the NPY data format, that can be read by MLM-IV-Analysis, and MLM-IV-EEDF-Analysis and which is compatible with PlasmaPy (its the same data format), and therefore data generated can also be analyzed by PlasmaPy for comparison.

![First plot](.\images\xSimplot.png)

In the plot below the gaussian noise has been increased

![First plot](.\images\ySimplot2.png)

In the plot below the gaussian noise is the same as in the plot above but the number of sampled points per bias voltage have been reduced from 10 to 2.

![MLM-IV-SimPlot3](.\images\zSimPlot3.png)

The parameter section of the script makes it very easy to modify the settings:

```python
# Physical constants
e = 1.602e-19  # Elementary charge in C
kb = 1.38e-23  # Boltzmann constant in J/K
me = 9.11e-31  # Electron mass in kg
mi = 1.67e-27  # Ion mass (assumed proton) in kg

# Experimental parameters
ProbeDia = 2.5e-3  # Probe diameter in m
ProbeLength = 0.000275  # Probe length in m (added length parameter)
Aprobe = (2 * np.pi * (ProbeDia / 2) * ProbeLength) + (np.pi * (ProbeDia / 2) ** 2)  # Probe area including cylindrical surface and end area in m^2
ne = 1e16  # Electron density in m^-3
ni = 1e16  # Ion density in m^-3

# Plasma Temperature for electrons and ions
Te_values = [0.1, 0.25, 0.5, 1, 2]  # Electron temperatures in eV
Tp = 0.03  # Ion temperature in eV

# Langmuir IV curve voltage parameters
V_min = -20  # Minimum voltage in V
V_max = 20  # Maximum voltage in V
V_points = 1000  # Number of points in voltage range

# Ion and electron current smoothing and leakage parameters, and due to plasma noise or averaging effects.
height_modifier = 0.9   # Electron current simulated max of theoretical max
stretch_modifier = 10.5 # Electron current simulation horizontal spread
slope_ion = 0.5e-5      # Slope for ion current leakage below Vp
slope_electron = 0.2e-4 # Slope for electron current leakage above Vp

# Noise parameters for simulated data
num_samples = 2  # Number of noisy samples to generate
noise_amplitude = 0.00018  # Amplitude of Gaussian noise
```

