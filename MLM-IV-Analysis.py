import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
from scipy.signal import savgol_filter, find_peaks
from scipy.optimize import curve_fit
import scipy.constants as const

# Physical constants
e = 1.602e-19  # Elementary charge in C
kb = 1.38e-23  # Boltzmann constant in J/K
me = 9.11e-31  # Electron mass in kg
mi = 1.67e-27  # Ion mass (assumed proton) in kg

# Load the data
data = np.load('LMSIMData\\20241126-112819-LangmuirSIM_eV2_theory.npy')
voltage = data[0]
current = data[1]

# Smooth the derivative for accurate Vp detection
current_derivative = savgol_filter(np.gradient(current, voltage), 21, 3)

# Detect the primary peak in the smoothed derivative for plasma potential (Vp)
peaks, _ = find_peaks(current_derivative)
primary_peak_index = peaks[np.argmax(current_derivative[peaks])]
Vp = voltage[primary_peak_index]

# Fit a linear function for ion saturation in the range -20V to -5V
def linear_func(x, a, b):
    return a * x + b

# Ion saturation fit (for subtraction only)
ion_saturation_mask = (voltage >= -20) & (voltage <= -5)
ion_fit_params, _ = curve_fit(linear_func, voltage[ion_saturation_mask], current[ion_saturation_mask])
ion_saturation_fit = linear_func(voltage, *ion_fit_params)

# Calculate Ii_sat by extending the ion saturation fit to Vp
Ii_sat = linear_func(Vp, *ion_fit_params)

# Subtract ion saturation fit up to Vp and calculate Ln(I) after subtraction
subtracted_current = current - ion_saturation_fit
ln_subtracted_current = np.log(np.clip(subtracted_current, 1e-15, None))

# Define specific range for electron retardation fit, close to Vp (Vp to Vp - 5 volts)
electron_retardation_mask = (voltage >= Vp - 5) & (voltage <= Vp)
retardation_fit_params, _ = curve_fit(linear_func, voltage[electron_retardation_mask], ln_subtracted_current[electron_retardation_mask])

# Define electron saturation region in the original voltage range and fit
electron_saturation_mask = voltage >= Vp + 1
saturation_fit_params, _ = curve_fit(linear_func, voltage[electron_saturation_mask], np.log(current[electron_saturation_mask]))

# Calculate intersection of the two fits for another Vp and Ie_sat estimate
intersection_voltage = (saturation_fit_params[1] - retardation_fit_params[1]) / (retardation_fit_params[0] - saturation_fit_params[0])
intersection_current = linear_func(intersection_voltage, *saturation_fit_params)

# Plot in a subplot layout
fig = sp.make_subplots(rows=2, cols=2, subplot_titles=[
    "I-V Curve", "Derivative of I-V Curve", "Ion Saturation Fit", "Ln(I) After Subtraction with Fits and Intersection"
])

# Plot I-V Curve
fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name="I-V Curve"), row=1, col=1)

# Plot Derivative of I-V Curve
fig.add_trace(go.Scatter(x=voltage, y=current_derivative, mode='lines', name="dI/dV", line=dict(color="red")), row=1, col=2)
fig.add_vline(x=Vp, line=dict(color="purple", dash="dash"), row=1, col=2, annotation_text=f"Vp={Vp:.2f} V")

# Plot Ion Saturation Fit
fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name="I-V Curve"), row=2, col=1)
fig.add_trace(go.Scatter(x=voltage[ion_saturation_mask], y=current[ion_saturation_mask], mode='markers', name="Ion Saturation Region"), row=2, col=1)
fig.add_trace(go.Scatter(x=voltage, y=ion_saturation_fit, mode='lines', line=dict(color="green"), name="Ion Saturation Fit (Full Range)"), row=2, col=1)
fig.add_hline(y=Ii_sat, line=dict(color="blue", dash="dot"), annotation_text=f"Ii_sat={Ii_sat:.2e} A", row=2, col=1)

# Ln(I) After Subtraction with Fits and Intersection
fig.add_trace(go.Scatter(x=voltage[voltage >= -5], y=ln_subtracted_current[voltage >= -5], mode='markers', name="Ln(I) After Subtraction"), row=2, col=2)

# Retardation Fit
retardation_line = linear_func(voltage, *retardation_fit_params)
fig.add_trace(go.Scatter(x=voltage[voltage >= -5], y=retardation_line[voltage >= -5], mode='lines', line=dict(color="cyan"), name="Retardation Fit"), row=2, col=2)

# Saturation Fit
saturation_line = linear_func(voltage, *saturation_fit_params)
fig.add_trace(go.Scatter(x=voltage[voltage >= -5], y=saturation_line[voltage >= -5], mode='lines', line=dict(color="magenta", dash="dash"), name="Saturation Fit"), row=2, col=2)

# Add horizontal and vertical lines at the intersection
fig.add_hline(y=intersection_current, line=dict(color="purple", dash="dot"), annotation_text=f"Ie_sat={np.exp(intersection_current):.2e} A", row=2, col=2)
fig.add_vline(x=intersection_voltage, line=dict(color="purple", dash="dot"), annotation_text=f"Vp={intersection_voltage:.2f} V", row=2, col=2)

# Update layout
fig.update_layout(
    title="Langmuir Probe Analysis with Fits and Intersection",
    height=800,
    showlegend=True
)

fig.show()

# Print estimated parameters
Te = abs(-1 / retardation_fit_params[0])  # Electron temperature in eV
Te_K = max(Te * 11600, 1e-10)  # Ensure Te_K is positive and non-zero  # Convert electron temperature to Kelvin
Ie_sat = np.exp(intersection_current)  # Electron saturation current

ProbeDia = 2.5e-3  # Probe diameter in m
ProbeLength = 0.000275  # Probe length in m (added length parameter)
Aprobe = (2 * np.pi * (ProbeDia / 2) * ProbeLength) + (np.pi * (ProbeDia / 2) ** 2)  # Probe area including cylindrical surface and end area in m^2

ve_th = np.sqrt(8 * kb * Te_K / (np.pi * me))  # Thermal velocity of electrons
ne = Ie_sat / (0.25 * e * ve_th * Aprobe)  # Electron density

# Calculate ion density (ni) using Bohm current equation
ni = Ii_sat / (0.6 * e * Aprobe * np.sqrt(max(kb * Te_K / mi, 1e-10)))  # Ensure non-negative value under sqrt

print(f"Estimated Electron Temperature (Te) = {Te:.2f} eV")
print(f"Estimated Plasma Potential (Vp) = {Vp:.2f} V (from derivative peak)")
print(f"Estimated Plasma Potential (Vp) = {intersection_voltage:.2f} V (from line crossing)")
print(f"Estimated Electron Saturation Current (Ie_sat) = {Ie_sat:.2e} A")
print(f"Estimated Ion Saturation Current (Ii_sat) = {Ii_sat:.2e} A")
print(f"Estimated Electron Density (ne) = {ne:.2e} m^-3 (calculated using thermal velocity)")
print(f"Estimated Ion Density (ni) = {ni:.2e} m^-3")
